// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {
    SupplyMode,
    MintSource,
    EventKind,
    ActionKind,
    HeistSnapshot,
    CombatSnapshot,
    RewardBundle,
    EventConfig,
    CraftRecipe
} from "./HoodQuestTypes.sol";
import { IHoodQuest } from "./interfaces/IHoodQuest.sol";
import { IHoodQuestTreasures } from "./interfaces/IHoodQuestTreasures.sol";
import { IHoodQuestWorldState } from "./interfaces/IHoodQuestWorldState.sol";

interface ArbSys {
    function arbBlockNumber() external view returns (uint256);
    function arbBlockHash(uint256 blockNum) external view returns (bytes32);
}

contract HoodQuestRaids {
    uint8 private _reentrantLock;
    modifier nonReentrant() {
        if (_reentrantLock != 0) revert();
        _reentrantLock = 1;
        _;
        _reentrantLock = 0;
    }

    // --- State Variables ---
    uint256 public nonce;
    IHoodQuest public immutable hoodContract;
    IHoodQuestTreasures public immutable treasuresContract;
    IHoodQuestWorldState public immutable worldStateContract;

    // Multi-Counter Retirement Protocol (HQ-GOV-004)
    mapping(address => uint256) public pendingRequestsByEngine;
    mapping(address => uint256) public outstandingEventLiabilitiesByEngine;

    // Heist Data Structures
    struct HeistRequest {
        uint256 hoodId;
        address rewardRecipient; // Snapshotted settlement recipient
        uint256 targetBlock;
        uint8 count;          // 1 to 5
        uint8 baseCount;      // Rolls i < baseCount are BASE rolls
        uint8 bonusCount;     // Rolls i >= baseCount are BONUS rolls
        uint32 monthEpochAtRequest;
        bytes32 heroSeed;
        HeistSnapshot snapshot;
    }

    mapping(uint256 => HeistRequest) public heistRequests;

    // Action Event Data Structures
    struct ActionRequest {
        uint256 hoodId;
        uint256 eventId;
        uint64 targetBlock;
        ActionKind kind;
        uint8 sector; // 0..4
        CombatSnapshot snapshot;
    }

    mapping(uint256 => ActionRequest) public actionRequests;
    mapping(uint256 => mapping(uint256 => uint8)) public castleManeuversUsed;
    mapping(uint256 => mapping(uint256 => uint8)) public jubileeManeuversUsed;
    mapping(uint256 => mapping(uint256 => uint32)) public taxTrainLastAttackDay;

    // Solstice Data Structures
    struct SolsticeCommitment {
        bytes32 secretHash;
        uint32 eventYear;
        uint64 targetBlock;
        uint8 maneuverIndex; // 0..4
        bool active;
    }

    mapping(uint256 => mapping(uint256 => SolsticeCommitment)) public solsticeCommitments;
    mapping(uint256 => mapping(uint256 => uint8)) public currentSolsticeManeuver;

    // Event Settlement Records
    struct EventRecord {
        uint256 finalBudget;
        uint256 totalContribution;
        uint256 claimDeadline;
        uint256 claimedTotal;
        bool finalized;
    }

    mapping(uint256 => EventRecord) public eventRecords;
    mapping(uint256 => mapping(uint256 => bool)) public eventClaimed;
    mapping(uint256 => mapping(uint256 => mapping(uint256 => bool))) public eventTrophyEntitlement;

    mapping(uint256 => bool) public eventLiabilityOpen;
    mapping(uint256 => bool) public eventGoldSettled;
    mapping(uint256 => uint8) public eventTrophiesOutstanding;
    mapping(uint256 => uint32) public eventParticipantsOutstanding;

    // --- Constants ---
    uint256 internal constant DROP_SCALE = 1_000_000_000;

    uint256 internal constant CHANCE_GILDED_BOW       =         125; // 0.0000125%
    uint256 internal constant CHANCE_COMMON_WEAPON    =       2_500; // 0.00025%
    uint256 internal constant CHANCE_FEAST_BASKET     =   5_000_000; // 0.5%
    uint256 internal constant CHANCE_GREENWOOD_ELIXIR =   8_000_000; // 0.8%
    uint256 internal constant CHANCE_SHERWOOD_YEW     = 250_000_000; // 25.0%
    uint256 internal constant CHANCE_NOTTINGHAM_IRON  = 200_000_000; // 20.0%

    // Item IDs
    uint256 internal constant GREENWOOD_ELIXIR  = 5;
    uint256 internal constant FEAST_BASKET      = 7;
    uint256 internal constant GILDED_BOW        = 3;
    uint256 internal constant YEW_LONGBOW       = 13;
    uint256 internal constant QUARTERSTAFF      = 14;
    uint256 internal constant POACHER_DAGGERS   = 15;
    uint256 internal constant GOLDEN_ARROW      = 4;
    uint256 internal constant FRIARS_CORNUCOPIA = 9;

    // --- Events ---
    event HeistBatchRequested(uint256 indexed requestId, uint256 indexed hoodId, uint8 count, uint256 targetBlock, address rewardRecipient);
    event HeistRewardRecipientUpdated(uint256 indexed requestId, uint256 indexed hoodId, address indexed newRecipient);
    event HeistBatchResolved(uint256 indexed requestId, uint256 indexed hoodId, uint8 count);
    event HeistFallbackResolved(uint256 indexed requestId, uint256 indexed hoodId, uint8 count);
    event ActionRequested(uint256 indexed requestId, uint256 indexed hoodId, uint256 indexed eventId, ActionKind kind);
    event ActionResolved(uint256 indexed requestId, uint256 indexed hoodId, uint256 indexed eventId, uint256 points);
    event SolsticeManeuverCommitted(uint256 indexed hoodId, uint8 maneuverIndex, uint64 targetBlock);
    event SolsticeManeuverRevealed(uint256 indexed hoodId, uint8 maneuverIndex, uint256 points);
    event SolsticeManeuverExpired(uint256 indexed eventId, uint256 indexed hoodId, uint8 maneuverIndex);
    event EventFinalized(uint256 indexed eventId, uint256 finalBudget, uint256 totalContribution);
    event EventLiabilityClosed(uint256 indexed eventId);
    event EventRewardClaimed(uint256 indexed eventId, uint256 indexed hoodId, address indexed recipient, uint256 reward);
    event EventTrophyClaimed(uint256 indexed eventId, uint256 indexed hoodId, uint256 indexed itemId, address recipient);
    event HoodEventParticipationExpired(uint256 indexed eventId, uint256 indexed hoodId);
    event TrophyForfeited(uint256 indexed eventId, uint256 indexed hoodId, uint256 indexed itemId);
    event UnclaimedBudgetRefunded(uint256 indexed eventId, uint256 unclaimed);

    constructor(address _hood, address _treasures, address _worldState) {
        if (_hood == address(0) || _treasures == address(0) || _worldState == address(0)) revert();
        hoodContract = IHoodQuest(_hood);
        treasuresContract = IHoodQuestTreasures(_treasures);
        worldStateContract = IHoodQuestWorldState(_worldState);
    }

    function _arbBlock() private view returns (uint256) {
        return ArbSys(address(0x64)).arbBlockNumber();
    }
    function _arbHash(uint256 b) private view returns (bytes32) {
        return ArbSys(address(0x64)).arbBlockHash(b);
    }

    function _isEventActive(uint256 eventId, uint256 currentBlock, uint64 target) private view returns (bool) {
        return currentBlock <= target + 256 && block.timestamp <= worldStateContract.getEvent(eventId).endTime + 2 hours;
    }

    function _checkActive() internal view {
        require(hoodContract.activeEngine(address(this)), "Engine not active");
    }

    function _validateHero(uint256 hoodId) internal view {
        require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
        if (hoodContract.economicActionsPaused() ||
            hoodContract.bazaarEscrowed(hoodId) ||
            hoodContract.heroSeed(hoodId) == bytes32(0)) revert();
    }

    // ================================================================
    //                     HEIST STATE MACHINE
    // ================================================================

    function _checkAuthorized(uint256 hoodId) internal view returns (address owner) {
        owner = hoodContract.ownerOf(hoodId);
        if (msg.sender != owner && !hoodContract.isGameDelegate(hoodId, msg.sender)) revert();
    }

    function requestHeistBatch(uint256 hoodId, uint8 count, address rewardRecipient) external returns (uint256 requestId) {
        _checkActive();
        if (count == 0 || count > 5 || rewardRecipient == address(0)) revert();
        address owner = _checkAuthorized(hoodId);
        if (msg.sender != owner) {
            require(rewardRecipient == owner, "Delegates can only direct rewards to Hood owner");
        }
        _validateHero(hoodId);
        require(!hoodContract.hasPendingNormalHeist(hoodId), "Pending heist batch already exists");
        
        bytes32 seed = hoodContract.heroSeed(hoodId);
        (uint8 baseConsumed, uint8 bonusConsumed) = hoodContract.consumeStaminaBatch(hoodId, count);
        
        // Active adventuring sustains hero upkeep for 7 days
        hoodContract.refreshActivitySustained(hoodId);
        
        HeistSnapshot memory snap = hoodContract.captureHeistSnapshot(hoodId);
        
        requestId = ++nonce;
        uint256 target = _arbBlock() + 2;
        
        HeistRequest storage req = heistRequests[requestId];
        req.hoodId = hoodId;
        req.rewardRecipient = rewardRecipient;
        req.targetBlock = target;
        req.count = count;
        req.baseCount = baseConsumed;
        req.bonusCount = bonusConsumed;
        req.monthEpochAtRequest = hoodContract.currentMonthEpoch();
        req.heroSeed = seed;
        req.snapshot = snap;
        
        hoodContract.setPendingNormalHeist(hoodId, true);
        hoodContract.incrementPendingGameplay(hoodId, count);
        pendingRequestsByEngine[address(this)]++;
        emit HeistBatchRequested(requestId, hoodId, count, target, rewardRecipient);
    }

    function updateHeistRewardRecipient(uint256 requestId, address newRecipient) external {
        HeistRequest storage req = heistRequests[requestId];
        if (req.targetBlock == 0 || newRecipient == address(0)) revert();
        
        address owner = _checkAuthorized(req.hoodId);
        if (msg.sender != owner && newRecipient != owner) revert();
        req.rewardRecipient = newRecipient;
        emit HeistRewardRecipientUpdated(requestId, req.hoodId, newRecipient);
    }

    function resolveHeist(uint256 requestId) external nonReentrant {
        HeistRequest storage req = heistRequests[requestId];
        uint256 target = req.targetBlock;
        if (target == 0) revert();
        
        uint256 currentBlock = _arbBlock();
        require(currentBlock > target, "Target block not reached");
        
        uint256 hId = req.hoodId;
        uint8 count = req.count;
        uint8 baseCount = req.baseCount;
        address recipient = req.rewardRecipient;
        HeistSnapshot memory snap = req.snapshot;
        uint32 mEpoch = req.monthEpochAtRequest;

        delete heistRequests[requestId];
        hoodContract.setPendingNormalHeist(hId, false);
        hoodContract.decrementPendingGameplay(hId, count);
        
        RewardBundle memory bundle;
        bool fatigueActive = snap.initialFatigue;
        
        if (baseCount > 0) {
            worldStateContract.recordMonthlyActiveHood(hId, mEpoch);
        }
        
        if (currentBlock <= target + 256) {
            bytes32 arbHash = _arbHash(target);
            for (uint8 i = 0; i < count; i++) {
                fatigueActive = _resolveSequentialRoll(
                    hId,
                    snap,
                    arbHash,
                    requestId,
                    i,
                    (i >= baseCount),
                    fatigueActive,
                    bundle
                );
            }
            emit HeistBatchResolved(requestId, hId, count);
        } else {
            for (uint8 i = 0; i < count; i++) {
                _resolveFallbackRoll(hId, snap, bundle);
            }
            fatigueActive = false;
            emit HeistFallbackResolved(requestId, hId, count);
        }
        
        hoodContract.setFatigue(hId, fatigueActive);
        
        bundle.elixirs = _reserve(GREENWOOD_ELIXIR, bundle.elixirs);
        bundle.gildedBows = _reserve(GILDED_BOW, bundle.gildedBows);
        bundle.yewLongbows = _reserve(YEW_LONGBOW, bundle.yewLongbows);
        bundle.quarterstaffs = _reserve(QUARTERSTAFF, bundle.quarterstaffs);
        bundle.poacherDaggers = _reserve(POACHER_DAGGERS, bundle.poacherDaggers);

        treasuresContract.settleHeistRewardBundle(recipient, bundle);
        
        pendingRequestsByEngine[address(this)]--;
    }

    function _reserve(uint256 itemId, uint256 amt) private returns (uint256) {
        return amt > 0 ? treasuresContract.reserveItem(itemId, MintSource.DROP, amt) : 0;
    }

    struct RollCtx {
        bytes32 arbHash;
        uint256 requestId;
        uint256 hoodId;
        uint8 rollIndex;
        uint256 mult;
    }

    function _entropy(RollCtx memory ctx, string memory tag) private pure returns (uint256) {
        return uint256(keccak256(abi.encode(ctx.arbHash, ctx.requestId, ctx.hoodId, ctx.rollIndex, tag)));
    }

    function _checkDrop(RollCtx memory ctx, string memory tag, uint256 chance) private pure returns (bool) {
        return (_entropy(ctx, tag) % DROP_SCALE) < (chance * ctx.mult) / 1e12;
    }

    function _resolveSequentialRoll(
        uint256 hoodId,
        HeistSnapshot memory snap,
        bytes32 arbHash,
        uint256 requestId,
        uint8 rollIndex,
        bool isBonusRoll,
        bool currentFatigue,
        RewardBundle memory bundle
    ) internal returns (bool nextFatigue) {
        RollCtx memory ctx = RollCtx(arbHash, requestId, hoodId, rollIndex, 0);

        // 1. Difficulty & Combat Power Equation (HQ-COMBAT-001)
        uint256 difficulty = 50 + (_entropy(ctx, "COMBAT") % 51);
        bool isCrit = (_entropy(ctx, "CRIT") % 10000) < snap.critBps;
        uint256 power = 50 + snap.atk + (snap.stealth / 2) + (isCrit ? 15 : 0);
        
        // 2. Fatigue Generation & Next-Roll Propagation (HQ-COMBAT-002)
        if (power < difficulty) {
            uint256 delta = difficulty - power;
            uint256 mitigatedDamage = (delta * (3000 - uint256(snap.def) * 100)) / 3000;
            nextFatigue = (mitigatedDamage > 20);
        } else {
            nextFatigue = false;
        }
        
        // 3. Rare Drop Multiplier (Clamped between 1.0x and 2.0x)
        uint256 combatBps = 10000;
        if (power > difficulty) {
            uint256 c = 10000 + (power - difficulty) * 100;
            combatBps = c > 20000 ? 20000 : c;
        }
        ctx.mult = combatBps * (currentFatigue ? 7500 : 10_000) * snap.economicRewardBps;
        
        // 4. Token-Bound Gold Carry Settled in Core (HQ-ECO-001)
        uint256 baseGold = 1 + (_entropy(ctx, "GOLD") % 3);
        uint256 scaled = baseGold * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps);
        bundle.gold += hoodContract.settleGoldFraction(hoodId, scaled);
        
        // 5. Probabilistic Drops: Yew, Iron, Consumables, Gear
        if (_checkDrop(ctx, "YEW", CHANCE_SHERWOOD_YEW)) bundle.yew++;
        if (_checkDrop(ctx, "IRON", CHANCE_NOTTINGHAM_IRON)) bundle.iron++;
        if (_checkDrop(ctx, "BASKET", CHANCE_FEAST_BASKET)) bundle.baskets++;
        if (!isBonusRoll && _checkDrop(ctx, "ELIXIR", CHANCE_GREENWOOD_ELIXIR)) bundle.elixirs++;
        if (_checkDrop(ctx, "GILDED", CHANCE_GILDED_BOW)) bundle.gildedBows++;
        if (_checkDrop(ctx, "COMMON_WEAPON", CHANCE_COMMON_WEAPON)) {
            uint256 wType = _entropy(ctx, "COMMON_WEAPON_TYPE") % 3;
            if (wType == 0) bundle.yewLongbows++;
            else if (wType == 1) bundle.quarterstaffs++;
            else bundle.poacherDaggers++;
        }
    }

    function _resolveFallbackRoll(
        uint256 hoodId,
        HeistSnapshot memory snap,
        RewardBundle memory bundle
    ) internal {
        // Settles through Core-owned fractional accumulator
        bundle.gold += hoodContract.settleGoldFraction(hoodId, (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps));
    }

    function effectiveChance(
        uint256 baseChance,
        uint256 combatBps,
        bool isFatigued,
        uint256 economicRewardBps
    ) public pure returns (uint256) {
        return (baseChance * combatBps * (isFatigued ? 7500 : 10_000) * economicRewardBps) / 1e12;
    }

    // ================================================================
    //                 WORLD EVENTS ENGINE & SCHEDULING
    // ================================================================

    function _createEventIfMissing(uint256 eId, EventKind k, uint32 y, uint64 sStart, uint64 dur, uint32 cap) private {
        if (!worldStateContract.getEvent(eId).exists) {
            worldStateContract.createEvent(eId, EventConfig(true, k, y, sStart, sStart + dur, cap));
        }
    }

    function syncWorldEvents() public {
        uint256 genesis = hoodContract.GENESIS_TIME();
        uint256 elapsed = block.timestamp - genesis;
        uint32 year = uint32(elapsed / 365 days) + 1;
        uint256 day = (elapsed % 365 days) / 1 days;
        uint32 mEpoch = (year - 1) * 12 + uint32(day < 360 ? day / 30 : 11);
        uint64 yearStart = uint64(genesis + (year - 1) * 365 days);
        
        // 1. Monthly Castle Event (Days 28-30 of Months 1-11; indices 27..29)
        if (day < 330 && (day % 30) >= 27) {
            _createEventIfMissing(1_000_000 + mEpoch, EventKind.CASTLE, year, yearStart + uint64((mEpoch % 12) * 30 days + 27 days), 3 days, 5_000);
        }
        
        // 2. Annual Solstice Championship (Days 359-365; indices 358..364)
        if (day >= 358) {
            _createEventIfMissing(2_000_000 + year, EventKind.SOLSTICE, year, yearStart + 358 days, 7 days, 10_000);
        }
        
        // 3. Sherwood Jubilee (Days 351-357 of Years 5, 10, 15, 20, 25; indices 350..356)
        if (year % 5 == 0 && year <= 25 && day >= 350 && day <= 356) {
            _createEventIfMissing(3_000_000 + year, EventKind.JUBILEE, year, yearStart + 350 days, 7 days, 25_000);
        }
        
        // 4. Tax Train World Boss (Economy-driven threshold)
        if (!worldStateContract.isTaxTrainActive() && block.timestamp >= worldStateContract.getBossCooldown()) {
            if (treasuresContract.cumulativeGoldBurned() >= worldStateContract.getTaxTrainThreshold()) {
                if (day + 7 < (year % 5 == 0 && year <= 25 ? 350 : 358)) {
                    uint256 ttId = 4_000_000 + block.timestamp;
                    worldStateContract.setTaxTrainActive(true, ttId);
                    _createEventIfMissing(ttId, EventKind.TAX_TRAIN, year, uint64(block.timestamp), 7 days, 25_000);
                }
            }
        }
    }

    function getBreachTarget(uint32 mEpoch) public view returns (uint256) {
        uint256 target = (mEpoch == 0 ? 0 : worldStateContract.getMonthlyActiveHoodCount(mEpoch - 1)) * 60;
        return target < 1000 ? 1000 : target;
    }

    function _consumeEventAttempt(uint256 hoodId, uint256 eventId, ActionKind kind) internal {
        if (kind == ActionKind.CASTLE) {
            uint8 u = castleManeuversUsed[eventId][hoodId];
            if (u >= 5) revert();
            castleManeuversUsed[eventId][hoodId] = u + 1;
        } else if (kind == ActionKind.JUBILEE) {
            uint8 u = jubileeManeuversUsed[eventId][hoodId];
            if (u >= 5) revert();
            jubileeManeuversUsed[eventId][hoodId] = u + 1;
        } else if (kind == ActionKind.TAX_TRAIN) {
            uint32 today = hoodContract.currentUtcDay();
            if (taxTrainLastAttackDay[eventId][hoodId] >= today) revert();
            taxTrainLastAttackDay[eventId][hoodId] = today;
        }
    }

    function requestActionEvent(
        uint256 hoodId,
        uint256 eventId,
        ActionKind kind,
        uint8 sector
    ) external returns (uint256 requestId) {
        _checkActive();
        syncWorldEvents();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        if (!cfg.exists || cfg.kind == EventKind.SOLSTICE || uint8(cfg.kind) != uint8(kind) || sector > 4) revert();
        _checkAuthorized(hoodId);
        _validateHero(hoodId);
        if (block.timestamp < cfg.startTime || block.timestamp > cfg.endTime - 1 hours) revert();
        
        _consumeEventAttempt(hoodId, eventId, kind);
        
        // Active adventuring sustains hero upkeep for 7 days
        hoodContract.refreshActivitySustained(hoodId);
        
        CombatSnapshot memory snap = hoodContract.captureCombatSnapshot(hoodId);
        requestId = ++nonce;
        uint64 target = uint64(_arbBlock() + 2);
        
        ActionRequest storage req = actionRequests[requestId];
        req.hoodId = hoodId;
        req.eventId = eventId;
        req.targetBlock = target;
        req.kind = kind;
        req.sector = sector;
        req.snapshot = snap;

        hoodContract.incrementPendingGameplay(hoodId, 1);
        pendingRequestsByEngine[address(this)]++;
        emit ActionRequested(requestId, hoodId, eventId, kind);
    }

    function resolveActionEvent(uint256 requestId) external nonReentrant {
        ActionRequest storage req = actionRequests[requestId];
        uint64 target = req.targetBlock;
        if (target == 0) revert();
        
        uint256 currentBlock = _arbBlock();
        if (currentBlock <= target) revert();
        
        uint256 hId = req.hoodId;
        uint256 eId = req.eventId;
        ActionKind kind = req.kind;
        uint8 sector = req.sector;
        CombatSnapshot memory snap = req.snapshot;

        delete actionRequests[requestId];
        hoodContract.decrementPendingGameplay(hId, 1);
        pendingRequestsByEngine[address(this)]--;
        
        if (_isEventActive(eId, currentBlock, target)) {
            bytes32 entropy = _arbHash(target);
            uint256 points = _computeEventPoints(kind, sector, snap, entropy);
            
            if (points > 0) {
                (bool firstPositive, uint256 cumulative) = worldStateContract.addContribution(eId, hId, points);
                if (firstPositive) {
                    hoodContract.incrementPendingEventEntitlement(hId);
                }
                
                if (kind == ActionKind.CASTLE) {
                    uint32 mEpoch = uint32(eId - 1_000_000);
                    worldStateContract.addCastleBreach(eId, points, getBreachTarget(mEpoch));
                } else if (kind == ActionKind.JUBILEE) {
                    worldStateContract.updateJubileeTop5(eId, hId, cumulative);
                }
            }
            emit ActionResolved(requestId, hId, eId, points);
        } else {
            emit ActionResolved(requestId, hId, eId, 0);
        }
    }

    function _computeEventPoints(ActionKind kind, uint8 sector, CombatSnapshot memory snap, bytes32 entropy) internal pure returns (uint256) {
        if (kind == ActionKind.CASTLE) {
            uint256 roll = uint256(entropy) % 100;
            uint256 statBonus = (sector == 1 ? snap.def : (sector == 3 ? (uint256(snap.atk) + uint256(snap.def)) / 2 : (sector == 0 ? snap.atk : snap.stealth)));
            if (roll + statBonus + snap.morale >= 45) return 25 + (uint256(entropy >> 16) % 15);
            return 0;
        }
        if (kind == ActionKind.TAX_TRAIN) return 20 + (uint256(snap.atk) + uint256(snap.stealth) / 2) / 2 + (uint256(entropy) % 11);
        return 30 + (uint256(snap.atk) + uint256(snap.def) + uint256(snap.stealth)) / 3 + (uint256(entropy) % 21);
    }

    // ================================================================
    //                   SOLSTICE CHAMPIONSHIP ENGINE
    // ================================================================

    function commitSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secretHash, uint8 maneuverIndex) external returns (uint64 target) {
        _checkActive();
        syncWorldEvents();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        if (!cfg.exists || cfg.kind != EventKind.SOLSTICE) revert();
        if (block.timestamp < cfg.startTime || block.timestamp > cfg.endTime - 1 hours) revert();
        if (msg.sender != hoodContract.ownerOf(hoodId)) revert();
        _validateHero(hoodId);
        if (solsticeCommitments[eventId][hoodId].active || maneuverIndex != currentSolsticeManeuver[eventId][hoodId] || maneuverIndex >= 5) revert();
        
        // Active adventuring sustains hero upkeep for 7 days
        hoodContract.refreshActivitySustained(hoodId);
        
        target = uint64(_arbBlock() + 2);
        SolsticeCommitment storage sc = solsticeCommitments[eventId][hoodId];
        sc.secretHash = secretHash;
        sc.eventYear = cfg.eventYear;
        sc.targetBlock = target;
        sc.maneuverIndex = maneuverIndex;
        sc.active = true;

        hoodContract.incrementSolsticeCommitment(hoodId);
        pendingRequestsByEngine[address(this)]++;
        emit SolsticeManeuverCommitted(hoodId, maneuverIndex, target);
    }

    function _closeSolstice(uint256 eventId, uint256 hoodId) private {
        delete solsticeCommitments[eventId][hoodId];
        hoodContract.decrementSolsticeCommitment(hoodId);
        pendingRequestsByEngine[address(this)]--;
        currentSolsticeManeuver[eventId][hoodId]++;
    }

    function revealSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secret) external nonReentrant {
        SolsticeCommitment storage sc = solsticeCommitments[eventId][hoodId];
        if (!sc.active) revert();
        
        uint256 currentBlock = _arbBlock();
        uint64 target = sc.targetBlock;
        if (currentBlock <= target) revert();
        uint32 eYear = sc.eventYear;
        uint8 mIndex = sc.maneuverIndex;
        if (keccak256(abi.encode(secret, hoodId, eYear, mIndex, address(this), block.chainid)) != sc.secretHash) revert();
        
        _closeSolstice(eventId, hoodId);
        
        if (_isEventActive(eventId, currentBlock, target)) {
            bytes32 entropy = keccak256(abi.encodePacked(
                _arbHash(target),
                secret,
                hoodId,
                eYear,
                mIndex,
                block.chainid
            ));
            uint256 points = 50 + (uint256(entropy) % 51);
            
            // Accrues both canonical hoodContribution and solsticeRenown via WorldState
            (bool firstPositive, ) = worldStateContract.addContribution(eventId, hoodId, points);
            if (firstPositive) {
                hoodContract.incrementPendingEventEntitlement(hoodId);
            }
            worldStateContract.addSolsticeRenown(eventId, hoodId, points);
            
            emit SolsticeManeuverRevealed(hoodId, mIndex, points);
        } else {
            emit SolsticeManeuverRevealed(hoodId, mIndex, 0);
        }
    }

    function expireSolsticeManeuver(uint256 eventId, uint256 hoodId) external {
        SolsticeCommitment storage sc = solsticeCommitments[eventId][hoodId];
        if (!sc.active) revert();
        uint256 currentBlock = _arbBlock();
        uint64 target = sc.targetBlock;
        uint8 mIndex = sc.maneuverIndex;
        if (_isEventActive(eventId, currentBlock, target)) revert();
        
        _closeSolstice(eventId, hoodId);
        emit SolsticeManeuverExpired(eventId, hoodId, mIndex);
    }

    // ================================================================
    //           EVENT FINALIZATION & SETTLEMENT LIFECYCLE
    // ================================================================

    function _tryCloseEventLiability(uint256 eventId) internal {
        if (eventLiabilityOpen[eventId] && 
            eventGoldSettled[eventId] && 
            eventTrophiesOutstanding[eventId] == 0 && 
            eventParticipantsOutstanding[eventId] == 0) {
            eventLiabilityOpen[eventId] = false;
            if (outstandingEventLiabilitiesByEngine[address(this)] > 0) {
                outstandingEventLiabilitiesByEngine[address(this)]--;
            }
            emit EventLiabilityClosed(eventId);
        }
    }

    function finalizeEvent(uint256 eventId) external nonReentrant {
        _checkActive();
        syncWorldEvents();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        if (!cfg.exists || block.timestamp <= cfg.endTime + 2 hours) revert();
        // WorldState owns the canonical one-time finalization lock across engine upgrades
        worldStateContract.markEventFinalized(eventId);

        EventRecord storage e = eventRecords[eventId];
        if (e.finalized) revert();
        
        e.totalContribution = worldStateContract.getTotalContribution(eventId);
        
        bool payableEvent = (cfg.kind != EventKind.CASTLE || worldStateContract.isCastleBreached(eventId));
        
        // Initialize participants before payable check to protect failed breaches
        eventParticipantsOutstanding[eventId] = worldStateContract.eventParticipantCount(eventId);

        if (e.totalContribution == 0 || !payableEvent) {
            e.finalBudget = 0;
            eventGoldSettled[eventId] = true;
        } else {
            e.finalBudget = treasuresContract.reserveEventBudget(eventId, cfg.cap);
            _reserveEventTrophies(eventId, cfg.kind, cfg.eventYear);
        }

        // Open liability whenever any participant, Gold, or trophy obligation exists
        if (e.finalBudget > 0 || eventTrophiesOutstanding[eventId] > 0 || eventParticipantsOutstanding[eventId] > 0) {
            eventLiabilityOpen[eventId] = true;
            outstandingEventLiabilitiesByEngine[address(this)]++;
        }
        
        e.finalized = true;
        e.claimDeadline = block.timestamp + 90 days;
        
        if (cfg.kind == EventKind.TAX_TRAIN) {
            worldStateContract.setTaxTrainActive(false, 0);
            worldStateContract.setBossCooldown(uint64(block.timestamp + 14 days));
            worldStateContract.setTaxTrainThreshold(treasuresContract.cumulativeGoldBurned() + 150_000);
        }
        
        _tryCloseEventLiability(eventId);
        emit EventFinalized(eventId, e.finalBudget, e.totalContribution);
    }

    function _addTrophy(uint256 eventId, uint256 hoodId, uint256 itemId) private {
        treasuresContract.reserveEventTrophy(eventId, itemId, 1);
        eventTrophyEntitlement[eventId][hoodId][itemId] = true;
        eventTrophiesOutstanding[eventId]++;
    }

    function _reserveEventTrophies(uint256 eventId, EventKind kind, uint32 eventYear) internal {
        if (kind == EventKind.SOLSTICE && eventYear <= 20) {
            (uint256 leader, ) = worldStateContract.getSolsticeLeaderHood(eventId);
            if (leader != 0) _addTrophy(eventId, leader, GOLDEN_ARROW);
        } else if (kind == EventKind.JUBILEE) {
            for (uint8 i = 0; i < 5; i++) {
                (uint256 hood, ) = worldStateContract.getJubileeTopHood(eventId, i);
                if (hood != 0) {
                    if (i == 0) _addTrophy(eventId, hood, GOLDEN_ARROW);
                    _addTrophy(eventId, hood, FRIARS_CORNUCOPIA);
                }
            }
        }
    }

    function _getEvent(uint256 eventId, bool requireOpen) internal view returns (EventRecord storage e) {
        e = eventRecords[eventId];
        if (!e.finalized || (requireOpen ? block.timestamp >= e.claimDeadline : block.timestamp < e.claimDeadline)) revert();
    }

    function _closeParticipant(uint256 eventId, uint256 hoodId) internal returns (uint256 userContribution) {
        userContribution = worldStateContract.getHoodContribution(eventId, hoodId);
        if (userContribution == 0 || eventClaimed[eventId][hoodId]) revert();
        eventClaimed[eventId][hoodId] = true;
        hoodContract.decrementPendingEventEntitlement(hoodId);
        eventParticipantsOutstanding[eventId]--;
    }

    function _closeTrophy(uint256 eventId, uint256 hoodId, uint256 itemId) internal {
        if (!eventTrophyEntitlement[eventId][hoodId][itemId]) revert();
        delete eventTrophyEntitlement[eventId][hoodId][itemId];
        eventTrophiesOutstanding[eventId]--;
    }

    function claimEventReward(uint256 eventId, uint256 hoodId, address recipient) external nonReentrant {
        if (recipient == address(0)) revert();
        address owner = _checkAuthorized(hoodId);
        if (msg.sender != owner && recipient != owner) revert();
        
        EventRecord storage e = _getEvent(eventId, true);
        uint256 userContribution = _closeParticipant(eventId, hoodId);
        
        uint256 reward = (e.finalBudget * userContribution) / e.totalContribution;
        e.claimedTotal += reward;
        
        treasuresContract.mintReservedEventGold(recipient, eventId, reward);
        if (e.claimedTotal == e.finalBudget) {
            eventGoldSettled[eventId] = true;
        }
        _tryCloseEventLiability(eventId);
        emit EventRewardClaimed(eventId, hoodId, recipient, reward);
    }

    function claimEventTrophy(uint256 eventId, uint256 hoodId, uint256 itemId, address recipient) external nonReentrant {
        if (recipient == address(0) || msg.sender != hoodContract.ownerOf(hoodId)) revert();
        _getEvent(eventId, true);
        _closeTrophy(eventId, hoodId, itemId);
        
        treasuresContract.mintReservedTrophy(eventId, recipient, itemId);
        _tryCloseEventLiability(eventId);
        emit EventTrophyClaimed(eventId, hoodId, itemId, recipient);
    }

    function expireHoodEventParticipation(uint256 eventId, uint256 hoodId) external nonReentrant {
        _getEvent(eventId, false);
        _closeParticipant(eventId, hoodId);
        _tryCloseEventLiability(eventId);
        emit HoodEventParticipationExpired(eventId, hoodId);
    }

    function forfeitUnclaimedTrophy(uint256 eventId, uint256 hoodId, uint256 itemId) external nonReentrant {
        _getEvent(eventId, false);
        _closeTrophy(eventId, hoodId, itemId);
        treasuresContract.forfeitReservedTrophy(eventId, itemId);
        _tryCloseEventLiability(eventId);
        emit TrophyForfeited(eventId, hoodId, itemId);
    }

    function refundUnclaimedEventBudget(uint256 eventId) external {
        EventRecord storage e = _getEvent(eventId, false);
        if (eventGoldSettled[eventId]) revert();
        
        uint256 unclaimed = e.finalBudget - e.claimedTotal;
        e.claimedTotal = e.finalBudget;
        eventGoldSettled[eventId] = true;
        
        if (unclaimed > 0) {
            treasuresContract.refundEventBudget(eventId, unclaimed);
        }
        _tryCloseEventLiability(eventId);
        emit UnclaimedBudgetRefunded(eventId, unclaimed);
    }
}
