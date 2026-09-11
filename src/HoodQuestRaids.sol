// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ReentrancyGuard } from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import { Math } from "@openzeppelin/contracts/utils/math/Math.sol";
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

contract HoodQuestRaids is ReentrancyGuard {
    using Math for uint256;

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
    uint256 public constant DROP_SCALE = 1_000_000_000;

    uint256 public constant CHANCE_GILDED_BOW       =         125; // 0.0000125%
    uint256 public constant CHANCE_COMMON_WEAPON    =       2_500; // 0.00025%
    uint256 public constant CHANCE_FEAST_BASKET     =   5_000_000; // 0.5%
    uint256 public constant CHANCE_GREENWOOD_ELIXIR =   8_000_000; // 0.8%
    uint256 public constant CHANCE_SHERWOOD_YEW     = 250_000_000; // 25.0%
    uint256 public constant CHANCE_NOTTINGHAM_IRON  = 200_000_000; // 20.0%

    // Item IDs
    uint256 public constant GREENWOOD_ELIXIR  = 5;
    uint256 public constant FEAST_BASKET      = 7;
    uint256 public constant GILDED_BOW        = 3;
    uint256 public constant YEW_LONGBOW       = 13;
    uint256 public constant QUARTERSTAFF      = 14;
    uint256 public constant POACHER_DAGGERS   = 15;
    uint256 public constant GOLDEN_ARROW      = 4;
    uint256 public constant FRIARS_CORNUCOPIA = 9;

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
        require(_hood != address(0), "Invalid Hood address");
        require(_treasures != address(0), "Invalid Treasures address");
        require(_worldState != address(0), "Invalid WorldState address");
        hoodContract = IHoodQuest(_hood);
        treasuresContract = IHoodQuestTreasures(_treasures);
        worldStateContract = IHoodQuestWorldState(_worldState);
    }

    // ================================================================
    //                     HEIST STATE MACHINE
    // ================================================================

    function requestHeistBatch(uint256 hoodId, uint8 count, address rewardRecipient) external returns (uint256 requestId) {
        require(hoodContract.activeEngine(address(this)), "Engine not active");
        require(count >= 1 && count <= 5, "Count must be 1..5");
        require(rewardRecipient != address(0), "Invalid recipient");
        address owner = hoodContract.ownerOf(hoodId);
        if (msg.sender != owner) {
            require(hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
            require(rewardRecipient == owner, "Delegates can only direct rewards to Hood owner");
        }
        require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        require(!hoodContract.bazaarEscrowed(hoodId), "Hero is listed in Bazaar");
        require(!hoodContract.hasPendingNormalHeist(hoodId), "Pending heist batch already exists");
        
        bytes32 seed = hoodContract.heroSeed(hoodId);
        require(seed != bytes32(0), "Hero seed not finalized");
        
        (uint8 baseConsumed, uint8 bonusConsumed) = hoodContract.consumeStaminaBatch(hoodId, count);
        
        // Active adventuring sustains hero upkeep for 7 days
        hoodContract.refreshActivitySustained(hoodId);
        
        HeistSnapshot memory snap = hoodContract.captureHeistSnapshot(hoodId);
        
        requestId = ++nonce;
        uint256 target = ArbSys(address(0x64)).arbBlockNumber() + 2;
        
        heistRequests[requestId] = HeistRequest({
            hoodId: hoodId,
            rewardRecipient: rewardRecipient,
            targetBlock: target,
            count: count,
            baseCount: baseConsumed,
            bonusCount: bonusConsumed,
            monthEpochAtRequest: hoodContract.currentMonthEpoch(),
            heroSeed: seed,
            snapshot: snap
        });
        
        hoodContract.setPendingNormalHeist(hoodId, true);
        hoodContract.incrementPendingGameplay(hoodId, count);
        pendingRequestsByEngine[address(this)]++;
        emit HeistBatchRequested(requestId, hoodId, count, target, rewardRecipient);
    }

    function updateHeistRewardRecipient(uint256 requestId, address newRecipient) external {
        HeistRequest storage req = heistRequests[requestId];
        require(req.targetBlock > 0, "Non-existent request");
        require(newRecipient != address(0), "Invalid recipient");
        
        address currentOwner = hoodContract.ownerOf(req.hoodId);
        if (msg.sender == currentOwner) {
            req.rewardRecipient = newRecipient;
        } else {
            require(hoodContract.isGameDelegate(req.hoodId, msg.sender), "Not authorized");
            require(newRecipient == currentOwner, "Delegates can only direct rewards to current Hood owner");
            req.rewardRecipient = newRecipient;
        }
        emit HeistRewardRecipientUpdated(requestId, req.hoodId, newRecipient);
    }

    function resolveHeist(uint256 requestId) external nonReentrant {
        HeistRequest memory req = heistRequests[requestId];
        require(req.targetBlock > 0, "Non-existent request");
        
        uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
        require(currentBlock > req.targetBlock, "Target block not reached");
        
        delete heistRequests[requestId];
        hoodContract.setPendingNormalHeist(req.hoodId, false);
        hoodContract.decrementPendingGameplay(req.hoodId, req.count);
        
        RewardBundle memory bundle;
        bool fatigueActive = req.snapshot.initialFatigue;
        
        if (req.baseCount > 0) {
            worldStateContract.recordMonthlyActiveHood(req.hoodId, req.monthEpochAtRequest);
        }
        
        if (currentBlock <= req.targetBlock + 256) {
            bytes32 arbHash = ArbSys(address(0x64)).arbBlockHash(req.targetBlock);
            for (uint8 i = 0; i < req.count; i++) {
                bool isBonusRoll = (i >= req.baseCount);
                fatigueActive = _resolveSequentialRoll(
                    req.hoodId,
                    req.snapshot,
                    arbHash,
                    requestId,
                    i,
                    isBonusRoll,
                    fatigueActive,
                    bundle
                );
            }
            emit HeistBatchResolved(requestId, req.hoodId, req.count);
        } else {
            for (uint8 i = 0; i < req.count; i++) {
                _resolveFallbackRoll(req.hoodId, req.snapshot, bundle);
            }
            fatigueActive = false;
            emit HeistFallbackResolved(requestId, req.hoodId, req.count);
        }
        
        hoodContract.setFatigue(req.hoodId, fatigueActive);
        
        // 1. Reserve/trim scarce capped drops
        if (bundle.elixirs > 0) {
            bundle.elixirs = treasuresContract.reserveItem(GREENWOOD_ELIXIR, MintSource.DROP, bundle.elixirs);
        }
        if (bundle.gildedBows > 0) {
            bundle.gildedBows = treasuresContract.reserveItem(GILDED_BOW, MintSource.DROP, bundle.gildedBows);
        }
        if (bundle.yewLongbows > 0) {
            bundle.yewLongbows = treasuresContract.reserveItem(YEW_LONGBOW, MintSource.DROP, bundle.yewLongbows);
        }
        if (bundle.quarterstaffs > 0) {
            bundle.quarterstaffs = treasuresContract.reserveItem(QUARTERSTAFF, MintSource.DROP, bundle.quarterstaffs);
        }
        if (bundle.poacherDaggers > 0) {
            bundle.poacherDaggers = treasuresContract.reserveItem(POACHER_DAGGERS, MintSource.DROP, bundle.poacherDaggers);
        }

        // 2. Atomic settlement directly to snapshotted recipient (Zero Unclaimed Storage)
        treasuresContract.settleHeistRewardBundle(req.rewardRecipient, bundle);
        
        pendingRequestsByEngine[address(this)]--;
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
        // 1. Difficulty & Combat Power Equation (HQ-COMBAT-001)
        bytes32 combatEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMBAT"));
        uint256 difficulty = 50 + (uint256(combatEntropy) % 51); // 50..100
        
        bytes32 critEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "CRIT"));
        bool isCrit = (uint256(critEntropy) % 10000) < snap.critBps;
        
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
        int256 deltaPower = int256(power) - int256(difficulty);
        int256 rareCalc = 10000 + deltaPower * 100;
        uint256 combatBps;
        if (rareCalc < 10000) combatBps = 10000;
        else if (rareCalc > 20000) combatBps = 20000;
        else combatBps = uint256(rareCalc);
        
        // 4. Token-Bound Gold Carry Settled in Core (HQ-ECO-001)
        bytes32 goldEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GOLD"));
        uint256 baseGold = 1 + (uint256(goldEntropy) % 3); // 1, 2, or 3 Gold
        uint256 scaled = baseGold * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps);
        uint256 wholeGold = hoodContract.settleGoldFraction(hoodId, scaled);
        bundle.gold += wholeGold;
        
        // 5. Probabilistic Drops: Yew, Iron, Consumables, Gear
        bytes32 yewEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "YEW"));
        if ((uint256(yewEntropy) % DROP_SCALE) < effectiveChance(CHANCE_SHERWOOD_YEW, combatBps, currentFatigue, snap.economicRewardBps)) {
            bundle.yew += 1;
        }
        
        bytes32 ironEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "IRON"));
        if ((uint256(ironEntropy) % DROP_SCALE) < effectiveChance(CHANCE_NOTTINGHAM_IRON, combatBps, currentFatigue, snap.economicRewardBps)) {
            bundle.iron += 1;
        }
        
        bytes32 basketEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "BASKET"));
        if ((uint256(basketEntropy) % DROP_SCALE) < effectiveChance(CHANCE_FEAST_BASKET, combatBps, currentFatigue, snap.economicRewardBps)) {
            bundle.baskets += 1;
        }
        
        // Greenwood Elixir (0.8% - strictly BASE rolls only; 0% recursive drop)
        if (!isBonusRoll) {
            bytes32 elixirEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "ELIXIR"));
            if ((uint256(elixirEntropy) % DROP_SCALE) < effectiveChance(CHANCE_GREENWOOD_ELIXIR, combatBps, currentFatigue, snap.economicRewardBps)) {
                bundle.elixirs += 1;
            }
        }
        
        bytes32 gildedEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GILDED"));
        if ((uint256(gildedEntropy) % DROP_SCALE) < effectiveChance(CHANCE_GILDED_BOW, combatBps, currentFatigue, snap.economicRewardBps)) {
            bundle.gildedBows += 1;
        }
        
        // Common Finished Weapons (0.00025%) with 3-way split: #13 Longbow, #14 Quarterstaff, #15 Daggers
        bytes32 commonEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMMON_WEAPON"));
        if ((uint256(commonEntropy) % DROP_SCALE) < effectiveChance(CHANCE_COMMON_WEAPON, combatBps, currentFatigue, snap.economicRewardBps)) {
            bytes32 typeEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMMON_WEAPON_TYPE"));
            uint256 wType = uint256(typeEntropy) % 3;
            if (wType == 0) bundle.yewLongbows += 1;
            else if (wType == 1) bundle.quarterstaffs += 1;
            else bundle.poacherDaggers += 1;
        }
    }

    function _resolveFallbackRoll(
        uint256 hoodId,
        HeistSnapshot memory snap,
        RewardBundle memory bundle
    ) internal {
        // Settles through Core-owned fractional accumulator
        uint256 scaled = 1 * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps);
        bundle.gold += hoodContract.settleGoldFraction(hoodId, scaled);
    }

    function effectiveChance(
        uint256 baseChance,
        uint256 combatBps,
        bool isFatigued,
        uint256 economicRewardBps
    ) public pure returns (uint256) {
        uint256 fatigueBps = isFatigued ? 7500 : 10_000;
        return Math.mulDiv(
            baseChance,
            combatBps * fatigueBps * economicRewardBps,
            10_000 * 10_000 * 10_000
        );
    }

    // ================================================================
    //                 WORLD EVENTS ENGINE & SCHEDULING
    // ================================================================

    function syncWorldEvents() public {
        uint256 genesis = hoodContract.GENESIS_TIME();
        uint256 elapsed = block.timestamp - genesis;
        uint32 year = uint32(elapsed / 365 days) + 1;
        uint256 day = (elapsed % 365 days) / 1 days;
        uint32 mEpoch = uint32(elapsed / 365 days) * 12 + uint32(day < 360 ? day / 30 : 11);
        
        // 1. Monthly Castle Event (Days 28-30 of Months 1-11; indices 27..29)
        if (day < 330 && (day % 30) >= 27) {
            uint256 castleEventId = 1_000_000 + mEpoch;
            if (!worldStateContract.getEvent(castleEventId).exists) {
                uint64 mStart = uint64(genesis + (mEpoch / 12) * 365 days + (mEpoch % 12) * 30 days + 27 days);
                worldStateContract.createEvent(castleEventId, EventConfig(true, EventKind.CASTLE, year, mStart, mStart + 3 days, 5_000));
            }
        }
        
        // 2. Annual Solstice Championship (Days 359-365; indices 358..364)
        if (day >= 358) {
            uint256 solsticeId = 2_000_000 + year;
            if (!worldStateContract.getEvent(solsticeId).exists) {
                uint64 sStart = uint64(genesis + (year - 1) * 365 days + 358 days);
                worldStateContract.createEvent(solsticeId, EventConfig(true, EventKind.SOLSTICE, year, sStart, sStart + 7 days, 10_000));
            }
        }
        
        // 3. Sherwood Jubilee (Days 351-357 of Years 5, 10, 15, 20, 25; indices 350..356)
        if (year % 5 == 0 && year <= 25 && day >= 350 && day <= 356) {
            uint256 jubileeId = 3_000_000 + year;
            if (!worldStateContract.getEvent(jubileeId).exists) {
                uint64 jStart = uint64(genesis + (year - 1) * 365 days + 350 days);
                worldStateContract.createEvent(jubileeId, EventConfig(true, EventKind.JUBILEE, year, jStart, jStart + 7 days, 25_000));
            }
        }
        
        // 4. Tax Train World Boss (Economy-driven threshold)
        if (!worldStateContract.isTaxTrainActive() && block.timestamp >= worldStateContract.getBossCooldown()) {
            if (treasuresContract.cumulativeGoldBurned() >= worldStateContract.getTaxTrainThreshold()) {
                bool jubileeYear = (year % 5 == 0 && year <= 25);
                uint256 protectedStart = jubileeYear ? 350 : 358;
                bool overlapsFestival = (day + 7 >= protectedStart);
                if (!overlapsFestival) {
                    uint256 ttId = 4_000_000 + block.timestamp;
                    worldStateContract.setTaxTrainActive(true, ttId);
                    worldStateContract.createEvent(ttId, EventConfig(true, EventKind.TAX_TRAIN, year, uint64(block.timestamp), uint64(block.timestamp + 7 days), 25_000));
                }
            }
        }
    }

    function getBreachTarget(uint32 mEpoch) public view returns (uint256) {
        uint256 prevActive = (mEpoch == 0) ? 0 : worldStateContract.getMonthlyActiveHoodCount(mEpoch - 1);
        uint256 target = prevActive * 60;
        return target < 1000 ? 1000 : target;
    }

    function _consumeEventAttempt(uint256 hoodId, uint256 eventId, ActionKind kind) internal {
        if (kind == ActionKind.CASTLE) {
            require(castleManeuversUsed[eventId][hoodId] < 5, "Exceeds 5 Castle maneuvers");
            castleManeuversUsed[eventId][hoodId]++;
        } else if (kind == ActionKind.JUBILEE) {
            require(jubileeManeuversUsed[eventId][hoodId] < 5, "Exceeds 5 Jubilee maneuvers");
            jubileeManeuversUsed[eventId][hoodId]++;
        } else if (kind == ActionKind.TAX_TRAIN) {
            uint32 today = hoodContract.currentUtcDay();
            require(taxTrainLastAttackDay[eventId][hoodId] < today, "Already attacked Tax Train today");
            taxTrainLastAttackDay[eventId][hoodId] = today;
        }
    }

    function requestActionEvent(
        uint256 hoodId,
        uint256 eventId,
        ActionKind kind,
        uint8 sector
    ) external returns (uint256 requestId) {
        require(hoodContract.activeEngine(address(this)), "Engine not active");
        syncWorldEvents();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        require(cfg.exists, "Event does not exist");
        require(cfg.kind != EventKind.SOLSTICE, "Solstice requires commitSolsticeManeuver");
        require(uint8(cfg.kind) == uint8(kind), "Kind mismatch");
        require(sector <= 4, "Invalid tactical sector");
        require(msg.sender == hoodContract.ownerOf(hoodId) || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
        require(!hoodContract.economicActionsPaused(), "Paused");
        require(!hoodContract.bazaarEscrowed(hoodId), "Hero listed in Bazaar");
        require(hoodContract.heroSeed(hoodId) != bytes32(0), "Seed not finalized");
        require(block.timestamp >= cfg.startTime && block.timestamp <= cfg.endTime - 1 hours, "Action cutoff reached");
        
        _consumeEventAttempt(hoodId, eventId, kind);
        
        // Active adventuring sustains hero upkeep for 7 days
        hoodContract.refreshActivitySustained(hoodId);
        
        CombatSnapshot memory snap = hoodContract.captureCombatSnapshot(hoodId);
        requestId = ++nonce;
        uint64 target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);
        
        actionRequests[requestId] = ActionRequest(hoodId, eventId, target, kind, sector, snap);
        hoodContract.incrementPendingGameplay(hoodId, 1);
        pendingRequestsByEngine[address(this)]++;
        emit ActionRequested(requestId, hoodId, eventId, kind);
    }

    function resolveActionEvent(uint256 requestId) external nonReentrant {
        ActionRequest memory req = actionRequests[requestId];
        require(req.targetBlock > 0, "Non-existent request");
        
        uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
        require(currentBlock > req.targetBlock, "Target not reached");
        
        delete actionRequests[requestId];
        hoodContract.decrementPendingGameplay(req.hoodId, 1);
        pendingRequestsByEngine[address(this)]--;
        
        EventConfig memory cfg = worldStateContract.getEvent(req.eventId);
        if (currentBlock <= req.targetBlock + 256 && block.timestamp <= cfg.endTime + 2 hours) {
            bytes32 entropy = ArbSys(address(0x64)).arbBlockHash(req.targetBlock);
            uint256 points = _computeEventPoints(req, entropy);
            
            if (points > 0) {
                (bool firstPositive, uint256 cumulative) = worldStateContract.addContribution(req.eventId, req.hoodId, points);
                if (firstPositive) {
                    hoodContract.incrementPendingEventEntitlement(req.hoodId);
                }
                
                if (req.kind == ActionKind.CASTLE) {
                    uint32 mEpoch = uint32(req.eventId - 1_000_000);
                    worldStateContract.addCastleBreach(req.eventId, points, getBreachTarget(mEpoch));
                } else if (req.kind == ActionKind.JUBILEE) {
                    worldStateContract.updateJubileeTop5(req.eventId, req.hoodId, cumulative);
                }
            }
            emit ActionResolved(requestId, req.hoodId, req.eventId, points);
        } else {
            emit ActionResolved(requestId, req.hoodId, req.eventId, 0);
        }
    }

    function _computeEventPoints(ActionRequest memory req, bytes32 entropy) internal pure returns (uint256 points) {
        if (req.kind == ActionKind.CASTLE) {
            uint256 roll = uint256(entropy) % 100; // 0..99
            uint256 statBonus = 0;
            if (req.sector == 0) statBonus = req.snapshot.atk; // Watchtowers (Sniping)
            else if (req.sector == 1) statBonus = req.snapshot.def; // Portcullis (Breach)
            else if (req.sector == 2) statBonus = req.snapshot.stealth; // Vault Tumblers (Lockpick)
            else if (req.sector == 3) statBonus = (uint256(req.snapshot.atk) + uint256(req.snapshot.def)) / 2; // Riot (Diversion)
            else if (req.sector == 4) statBonus = req.snapshot.stealth; // Greenwood Smokescreen
            
            // Morale (+10 from Silver Rallying Horn Castle Infiltration Aura) adds directly to the breach check
            uint256 effectiveRoll = roll + statBonus + req.snapshot.morale;
            if (effectiveRoll >= 45) {
                points = 25 + (uint256(entropy >> 16) % 15); // 25..39 points
            } else {
                points = 0;
            }
        } else if (req.kind == ActionKind.TAX_TRAIN) {
            points = 20 + (uint256(req.snapshot.atk) + uint256(req.snapshot.stealth) / 2) / 2 + (uint256(entropy) % 11);
        } else if (req.kind == ActionKind.JUBILEE) {
            points = 30 + (uint256(req.snapshot.atk) + uint256(req.snapshot.def) + uint256(req.snapshot.stealth)) / 3 + (uint256(entropy) % 21);
        }
    }

    // ================================================================
    //                   SOLSTICE CHAMPIONSHIP ENGINE
    // ================================================================

    function commitSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secretHash, uint8 maneuverIndex) external returns (uint64 target) {
        require(hoodContract.activeEngine(address(this)), "Engine not active");
        syncWorldEvents();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        require(cfg.exists && cfg.kind == EventKind.SOLSTICE, "Invalid Solstice event");
        require(block.timestamp >= cfg.startTime && block.timestamp <= cfg.endTime - 1 hours, "Action cutoff reached");
        require(msg.sender == hoodContract.ownerOf(hoodId), "Owner only");
        require(!hoodContract.economicActionsPaused(), "Paused");
        require(!hoodContract.bazaarEscrowed(hoodId), "Hero listed in Bazaar");
        require(hoodContract.heroSeed(hoodId) != bytes32(0), "Seed not finalized");
        require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
        require(!solsticeCommitments[eventId][hoodId].active, "Prior commitment unresolved");
        require(maneuverIndex == currentSolsticeManeuver[eventId][hoodId], "Out of sequence maneuver");
        require(maneuverIndex < 5, "All 5 maneuvers completed");
        
        // Active adventuring sustains hero upkeep for 7 days
        hoodContract.refreshActivitySustained(hoodId);
        
        target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);
        solsticeCommitments[eventId][hoodId] = SolsticeCommitment(secretHash, cfg.eventYear, target, maneuverIndex, true);
        hoodContract.incrementSolsticeCommitment(hoodId);
        pendingRequestsByEngine[address(this)]++;
        emit SolsticeManeuverCommitted(hoodId, maneuverIndex, target);
    }

    function revealSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secret) external nonReentrant {
        SolsticeCommitment memory sc = solsticeCommitments[eventId][hoodId];
        require(sc.active, "No active commitment");
        
        uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
        require(currentBlock > sc.targetBlock, "Target block not reached");
        require(keccak256(abi.encode(secret, hoodId, sc.eventYear, sc.maneuverIndex, address(this), block.chainid)) == sc.secretHash, "Invalid secret");
        
        delete solsticeCommitments[eventId][hoodId];
        hoodContract.decrementSolsticeCommitment(hoodId);
        pendingRequestsByEngine[address(this)]--;
        currentSolsticeManeuver[eventId][hoodId]++;
        
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        if (currentBlock <= sc.targetBlock + 256 && block.timestamp <= cfg.endTime + 2 hours) {
            bytes32 entropy = keccak256(abi.encodePacked(
                ArbSys(address(0x64)).arbBlockHash(sc.targetBlock),
                secret,
                hoodId,
                sc.eventYear,
                sc.maneuverIndex,
                block.chainid
            ));
            uint256 points = 50 + (uint256(entropy) % 51);
            
            // Accrues both canonical hoodContribution and solsticeRenown via WorldState
            (bool firstPositive, ) = worldStateContract.addContribution(eventId, hoodId, points);
            if (firstPositive) {
                hoodContract.incrementPendingEventEntitlement(hoodId);
            }
            worldStateContract.addSolsticeRenown(eventId, hoodId, points);
            
            emit SolsticeManeuverRevealed(hoodId, sc.maneuverIndex, points);
        } else {
            emit SolsticeManeuverRevealed(hoodId, sc.maneuverIndex, 0);
        }
    }

    function expireSolsticeManeuver(uint256 eventId, uint256 hoodId) external {
        SolsticeCommitment memory sc = solsticeCommitments[eventId][hoodId];
        require(sc.active, "No active commitment");
        uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        require(currentBlock > sc.targetBlock + 256 || block.timestamp > cfg.endTime + 2 hours, "Window still open");
        
        delete solsticeCommitments[eventId][hoodId];
        hoodContract.decrementSolsticeCommitment(hoodId);
        pendingRequestsByEngine[address(this)]--;
        currentSolsticeManeuver[eventId][hoodId]++;
        emit SolsticeManeuverExpired(eventId, hoodId, sc.maneuverIndex);
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
        require(hoodContract.activeEngine(address(this)), "Engine not active");
        syncWorldEvents();
        EventConfig memory cfg = worldStateContract.getEvent(eventId);
        require(cfg.exists, "Event does not exist");
        require(block.timestamp > cfg.endTime + 2 hours, "Grace period active");
        // WorldState owns the canonical one-time finalization lock across engine upgrades
        worldStateContract.markEventFinalized(eventId);

        EventRecord storage e = eventRecords[eventId];
        require(!e.finalized, "Already finalized");
        
        e.totalContribution = worldStateContract.getTotalContribution(eventId);
        
        bool payableEvent = true;
        if (cfg.kind == EventKind.CASTLE && !worldStateContract.isCastleBreached(eventId)) {
            payableEvent = false;
        }
        
        // Initialize participants before payable check to protect failed breaches
        eventParticipantsOutstanding[eventId] = worldStateContract.eventParticipantCount(eventId);

        if (e.totalContribution == 0 || !payableEvent) {
            e.finalBudget = 0;
            eventGoldSettled[eventId] = true;
        } else {
            e.finalBudget = treasuresContract.reserveEventBudget(eventId, cfg.cap);
            _reserveEventTrophies(eventId, cfg);
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

    function _reserveEventTrophies(uint256 eventId, EventConfig memory cfg) internal {
        if (cfg.kind == EventKind.SOLSTICE && cfg.eventYear <= 20) {
            (uint256 leader, ) = worldStateContract.getSolsticeLeaderHood(eventId);
            if (leader != 0) {
                treasuresContract.reserveEventTrophy(eventId, GOLDEN_ARROW, 1);
                eventTrophyEntitlement[eventId][leader][GOLDEN_ARROW] = true;
                eventTrophiesOutstanding[eventId]++;
            }
        } else if (cfg.kind == EventKind.JUBILEE) {
            (uint256 champion, ) = worldStateContract.getJubileeTopHood(eventId, 0);
            if (champion != 0) {
                treasuresContract.reserveEventTrophy(eventId, GOLDEN_ARROW, 1);
                eventTrophyEntitlement[eventId][champion][GOLDEN_ARROW] = true;
                eventTrophiesOutstanding[eventId]++;
            }
            for (uint8 i = 0; i < 5; i++) {
                (uint256 hood, ) = worldStateContract.getJubileeTopHood(eventId, i);
                if (hood != 0) {
                    treasuresContract.reserveEventTrophy(eventId, FRIARS_CORNUCOPIA, 1);
                    eventTrophyEntitlement[eventId][hood][FRIARS_CORNUCOPIA] = true;
                    eventTrophiesOutstanding[eventId]++;
                }
            }
        }
    }

    function claimEventReward(uint256 eventId, uint256 hoodId, address recipient) external nonReentrant {
        require(recipient != address(0), "Invalid recipient");
        address owner = hoodContract.ownerOf(hoodId);
        if (msg.sender != owner) {
            require(hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
            require(recipient == owner, "Delegates can only claim to Hood owner");
        }
        
        EventRecord storage e = eventRecords[eventId];
        require(e.finalized, "Not finalized");
        require(block.timestamp < e.claimDeadline, "Claim window expired");
        require(!eventClaimed[eventId][hoodId], "Already claimed");
        
        uint256 userContribution = worldStateContract.getHoodContribution(eventId, hoodId);
        require(userContribution > 0, "Zero contribution");
        
        eventClaimed[eventId][hoodId] = true;
        hoodContract.decrementPendingEventEntitlement(hoodId);
        eventParticipantsOutstanding[eventId]--;
        
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
        require(recipient != address(0), "Invalid recipient");
        require(msg.sender == hoodContract.ownerOf(hoodId), "Not owner");
        require(eventTrophyEntitlement[eventId][hoodId][itemId], "No trophy entitlement");
        
        EventRecord storage e = eventRecords[eventId];
        require(block.timestamp < e.claimDeadline, "Claim deadline expired");
        
        delete eventTrophyEntitlement[eventId][hoodId][itemId];
        eventTrophiesOutstanding[eventId]--;
        
        treasuresContract.mintReservedTrophy(eventId, recipient, itemId);
        _tryCloseEventLiability(eventId);
        emit EventTrophyClaimed(eventId, hoodId, itemId, recipient);
    }

    function expireHoodEventParticipation(uint256 eventId, uint256 hoodId) external nonReentrant {
        EventRecord storage e = eventRecords[eventId];
        require(e.finalized, "Event not finalized");
        require(block.timestamp >= e.claimDeadline, "Claim deadline not reached");
        require(!eventClaimed[eventId][hoodId], "Already claimed");
        
        uint256 userContribution = worldStateContract.getHoodContribution(eventId, hoodId);
        require(userContribution > 0, "No contribution");
        
        eventClaimed[eventId][hoodId] = true;
        hoodContract.decrementPendingEventEntitlement(hoodId);
        eventParticipantsOutstanding[eventId]--;
        _tryCloseEventLiability(eventId);
        emit HoodEventParticipationExpired(eventId, hoodId);
    }

    function forfeitUnclaimedTrophy(uint256 eventId, uint256 hoodId, uint256 itemId) external nonReentrant {
        EventRecord storage e = eventRecords[eventId];
        require(e.finalized, "Not finalized");
        require(block.timestamp >= e.claimDeadline, "Claim deadline active");
        require(eventTrophyEntitlement[eventId][hoodId][itemId], "No trophy entitlement");
        
        delete eventTrophyEntitlement[eventId][hoodId][itemId];
        eventTrophiesOutstanding[eventId]--;
        
        treasuresContract.forfeitReservedTrophy(eventId, itemId);
        _tryCloseEventLiability(eventId);
        emit TrophyForfeited(eventId, hoodId, itemId);
    }

    function refundUnclaimedEventBudget(uint256 eventId) external {
        EventRecord storage e = eventRecords[eventId];
        require(e.finalized, "Not finalized");
        require(block.timestamp >= e.claimDeadline, "Claim window active");
        require(!eventGoldSettled[eventId], "Gold already settled");
        
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
