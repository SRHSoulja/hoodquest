// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ERC721Enumerable } from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import { IERC721Receiver } from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import { ERC1155Holder } from "@openzeppelin/contracts/token/ERC1155/utils/ERC1155Holder.sol";
import { ReentrancyGuard } from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import { Strings } from "@openzeppelin/contracts/utils/Strings.sol";
import { IERC165 } from "@openzeppelin/contracts/utils/introspection/IERC165.sol";

import {
    HeistSnapshot,
    CombatSnapshot,
    BazaarTransferMode,
    UnequipRequest
} from "./HoodQuestTypes.sol";

import { IHoodQuest } from "./interfaces/IHoodQuest.sol";
import { IHoodQuestCompanions } from "./interfaces/IHoodQuestCompanions.sol";
import { IHoodQuestTreasures } from "./interfaces/IHoodQuestTreasures.sol";
import { IHoodQuestBazaar } from "./interfaces/IHoodQuestBazaar.sol";
import { IRenderer } from "./interfaces/IRenderer.sol";

interface ArbSys {
    function arbBlockNumber() external view returns (uint256);
    function arbBlockHash(uint256 blockNum) external view returns (bytes32);
}

contract HoodQuest is ERC721Enumerable, ERC1155Holder, ReentrancyGuard, IERC721Receiver, IHoodQuest {
    using Strings for uint256;

    uint256 public constant MAX_HOOD_SUPPLY = 10_000;
    uint256 public immutable MINT_PRICE_WEI;
    address public immutable PROCEEDS_RECIPIENT;
    uint256 public immutable GENESIS_TIME;

    address public immutable timelock;
    address public guardian;
    IHoodQuestCompanions public companionContract;
    IHoodQuestTreasures public treasuresContract;
    IHoodQuestBazaar public bazaarContract;
    IRenderer public renderer;

    uint32 public constant GILDED_BOW = 3;
    uint32 public constant GOLDEN_ARROW = 4;
    uint32 public constant LOCKSLEY_CLOAK = 6;
    uint32 public constant SILVER_RALLYING_HORN = 8;
    uint32 public constant FRIARS_CORNUCOPIA = 9;
    uint32 public constant YEW_LONGBOW = 13;
    uint32 public constant QUARTERSTAFF = 14;
    uint32 public constant POACHER_DAGGERS = 15;

    uint256 public totalHoodsMinted;

    // Three-Tier Engine Lifecycle Permissions
    mapping(address => bool) public activeEngine;
    mapping(address => bool) public resolverEngine;
    mapping(address => bool) public settlementEngine;

    // Token-level activity & gating counters
    mapping(uint256 => uint32) public pendingGameplayCount;
    mapping(uint256 => uint32) public pendingEventEntitlementCount;
    mapping(uint256 => uint32) public activeSolsticeCommitmentCount;
    mapping(uint256 => bool) public override hasPendingNormalHeist;
    mapping(uint256 => bool) public isHeroFatigued;
    mapping(uint256 => bool) public override bazaarEscrowed;
    mapping(uint256 => uint256) public goldCarry;
    mapping(uint256 => uint64) public activitySustainedUntil;

    // Hero traits & seeds
    mapping(uint256 => bytes32) public override heroSeed;
    mapping(uint256 => uint8) public override heroArchetype;
    mapping(uint256 => uint256) public seedTargetBlock;
    mapping(uint256 => bool) public standardGenesis;

    // Slumber & care temporal state
    mapping(uint256 => uint64) public mintTimestamp;
    mapping(uint256 => uint64) public lastCareTimestamp;
    mapping(uint256 => uint32) public lastCareDay;
    mapping(uint256 => uint64) public rationsUntil;
    mapping(uint256 => uint64) public completedSlumberSeconds;
    mapping(uint256 => uint64) public slumberAccountedUntil;

    // Stamina & Elixirs
    mapping(uint256 => uint8) public baseHeistsUsed;
    mapping(uint256 => uint8) public bonusHeistsUsed;
    mapping(uint256 => uint32) public lastHeistDay;
    mapping(uint256 => uint32) public lastElixirDay;

    // Delegation
    mapping(uint256 => uint64) public delegateEpoch;
    mapping(uint256 => mapping(address => uint64)) public delegateGrantedEpoch;

    // Guardian Pause
    uint64 public guardianPauseUntil;
    uint64 public lastGuardianPauseStarted;

    // Armory loadout state
    mapping(uint32 => uint8) public canonicalItemSlot;
    mapping(uint32 => bool) public isEquippable;
    mapping(uint256 => mapping(uint8 => uint32)) public override equippedSlot;
    mapping(uint256 => mapping(uint8 => UnequipRequest)) public pendingUnequip;
    mapping(uint256 => uint8) public pendingUnequipCount;
    mapping(uint256 => uint64) public postTransferUnequipLockedUntil;
    mapping(uint256 => uint64) public cornucopiaBoundTimestamp;
    mapping(uint256 => uint256) public boundCount;
    mapping(uint256 => uint256) public loadoutVersion;

    // Companions reverse binding
    mapping(uint256 => address) public override expectedPetDeposit;
    mapping(uint256 => uint256) public override petBoundToHood; // petId => hoodId
    mapping(uint256 => uint256) public hoodBoundPet;            // hoodId => petId
    mapping(uint256 => uint64) public petBondedAt;
    mapping(uint256 => uint64) public pendingDebondMaturesAt;

    // Bazaar Handshake
    BazaarTransferMode public bazaarTransferMode;

    // Events
    event GuardianUpdated(address indexed guardian);
    event RendererUpdated(address indexed renderer);
    event EngineRolesChanged(address indexed engine, bool active, bool resolver, bool settlement);
    event HeroSeedFinalized(uint256 indexed tokenId, bytes32 seed);
    event ActivitySustainedRefreshed(uint256 indexed hoodId, uint64 sustainedUntil);
    event FatigueStateChanged(uint256 indexed hoodId, bool fatigued);
    event DailyCarePerformed(uint256 indexed hoodId, uint32 careDay);
    event HeroFed(uint256 indexed hoodId, uint256 rationsUntil);
    event ElixirUsed(uint256 indexed hoodId, uint32 day);
    event ItemEquipped(uint256 indexed hoodId, uint8 slot, uint32 itemId);
    event UnequipInitiated(uint256 indexed hoodId, uint8 slot, uint32 itemId, uint256 maturesAt);
    event UnequipFinalized(uint256 indexed hoodId, uint8 slot, uint32 itemId);
    event PetBonded(uint256 indexed hoodId, uint256 petId);
    event DebondInitiated(uint256 indexed hoodId, uint256 petId, uint256 maturesAt);
    event DebondFinalized(uint256 indexed hoodId, uint256 petId);
    event EmergencyPauseTriggered(uint64 pauseUntil);
    event MetadataUpdate(uint256 _tokenId);

    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
        _;
    }
    modifier onlyGuardian() {
        require(msg.sender == guardian, "Not guardian");
        _;
    }
    modifier onlyBazaar() {
        require(msg.sender == address(bazaarContract), "Not bazaar");
        _;
    }
    modifier onlyActiveEngine() {
        require(activeEngine[msg.sender], "Not active engine");
        _;
    }
    modifier onlyResolverEngine() {
        require(resolverEngine[msg.sender], "Not resolver engine");
        _;
    }
    modifier onlySettlementEngine() {
        require(settlementEngine[msg.sender], "Not settlement engine");
        _;
    }

    constructor(
        uint256 mintPriceWei_,
        address proceedsRecipient_,
        uint256 genesisTime_,
        address timelock_,
        address guardian_
    ) ERC721("HoodQuest", "HQ") {
        require(proceedsRecipient_ != address(0), "Invalid recipient");
        require(genesisTime_ <= block.timestamp, "Genesis in future");
        require(timelock_ != address(0), "Invalid timelock");
        require(guardian_ != address(0), "Invalid guardian");
        MINT_PRICE_WEI = mintPriceWei_;
        PROCEEDS_RECIPIENT = proceedsRecipient_;
        GENESIS_TIME = genesisTime_;
        timelock = timelock_;
        guardian = guardian_;

        // Initialize Canonical Equippable Slots
        canonicalItemSlot[2] = 5; isEquippable[2] = true;
        canonicalItemSlot[3] = 0; isEquippable[3] = true;
        canonicalItemSlot[4] = 2; isEquippable[4] = true;
        canonicalItemSlot[6] = 1; isEquippable[6] = true;
        canonicalItemSlot[8] = 3; isEquippable[8] = true;
        canonicalItemSlot[9] = 4; isEquippable[9] = true;
        canonicalItemSlot[13] = 0; isEquippable[13] = true;
        canonicalItemSlot[14] = 0; isEquippable[14] = true;
        canonicalItemSlot[15] = 0; isEquippable[15] = true;
    }

    function setGuardian(address guardian_) external onlyTimelock {
        require(guardian_ != address(0), "Invalid guardian");
        guardian = guardian_;
        emit GuardianUpdated(guardian_);
    }

    function setBazaarContract(address bazaar_) external onlyTimelock {
        require(bazaar_ != address(0), "Invalid bazaar");
        bazaarContract = IHoodQuestBazaar(bazaar_);
    }

    function setCompanionContract(address companions_) external onlyTimelock {
        require(companions_ != address(0), "Invalid companions");
        companionContract = IHoodQuestCompanions(companions_);
    }

    function setTreasuresContract(address treasures_) external onlyTimelock {
        require(treasures_ != address(0), "Invalid treasures");
        treasuresContract = IHoodQuestTreasures(treasures_);
    }

    function setRenderer(address newRenderer) external onlyTimelock {
        renderer = IRenderer(newRenderer);
        emit RendererUpdated(newRenderer);
    }

    function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyTimelock {
        activeEngine[engine] = active;
        resolverEngine[engine] = resolver;
        settlementEngine[engine] = settlement;
        emit EngineRolesChanged(engine, active, resolver, settlement);
    }

    function onERC721Received(address, address from, uint256 petId, bytes calldata) external view override returns (bytes4) {
        if (msg.sender == address(companionContract)) {
            require(expectedPetDeposit[petId] == from, "Unsolicited companion deposit");
        } else {
            revert("Direct ERC721 deposits not supported");
        }
        return this.onERC721Received.selector;
    }

    function mintHoods(uint8 count) external payable nonReentrant {
        require(count >= 1 && count <= 5, "Count must be 1..5");
        require(totalHoodsMinted + count <= MAX_HOOD_SUPPLY, "Exceeds max supply");
        require(msg.value == MINT_PRICE_WEI * count, "Exact payment required");
        
        uint256 currentArbBlock;
        try ArbSys(address(0x64)).arbBlockNumber() returns (uint256 bn) {
            currentArbBlock = bn;
        } catch {
            currentArbBlock = block.number;
        }

        for (uint8 i = 0; i < count; i++) {
            uint256 id = ++totalHoodsMinted;
            mintTimestamp[id] = uint64(block.timestamp);
            lastCareTimestamp[id] = uint64(block.timestamp);
            lastCareDay[id] = currentUtcDay() > 0 ? currentUtcDay() - 1 : 0;
            delegateEpoch[id] = 1;
            rationsUntil[id] = uint64(block.timestamp + 7 days);
            slumberAccountedUntil[id] = uint64(block.timestamp);
            seedTargetBlock[id] = currentArbBlock + 2;
            _safeMint(msg.sender, id);
        }
    }

    function withdrawMintProceeds() external nonReentrant {
        uint256 balance = address(this).balance;
        require(balance > 0, "No proceeds");
        (bool success, ) = PROCEEDS_RECIPIENT.call{value: balance}("");
        require(success, "Proceeds transfer failed");
    }

    function finalizeHeroSeed(uint256 tokenId) external {
        require(heroSeed[tokenId] == bytes32(0), "Already finalized");
        uint256 target = seedTargetBlock[tokenId];
        require(target > 0, "Not minted");
        uint256 current;
        try ArbSys(address(0x64)).arbBlockNumber() returns (uint256 bn) {
            current = bn;
        } catch {
            current = block.number;
        }
        require(current > target, "Target not reached");
        if (current <= target + 256) {
            bytes32 bHash;
            try ArbSys(address(0x64)).arbBlockHash(target) returns (bytes32 bh) {
                bHash = bh;
            } catch {
                bHash = blockhash(target);
            }
            if (bHash != bytes32(0)) {
                heroSeed[tokenId] = keccak256(abi.encode(
                    bHash,
                    tokenId,
                    address(this),
                    block.chainid
                ));
            } else {
                heroSeed[tokenId] = keccak256(abi.encode("STANDARD_GENESIS", tokenId, GENESIS_TIME));
                standardGenesis[tokenId] = true;
            }
        } else {
            heroSeed[tokenId] = keccak256(abi.encode("STANDARD_GENESIS", tokenId, GENESIS_TIME));
            standardGenesis[tokenId] = true;
        }
        heroArchetype[tokenId] = uint8(uint256(heroSeed[tokenId]) % 5);
        emit HeroSeedFinalized(tokenId, heroSeed[tokenId]);
    }

    function refreshActivitySustained(uint256 hoodId) external onlyActiveEngine {
        activitySustainedUntil[hoodId] = uint64(block.timestamp + 7 days);
        emit ActivitySustainedRefreshed(hoodId, activitySustainedUntil[hoodId]);
    }

    function touchActivity(uint256 hoodId) external override onlyActiveEngine {
        activitySustainedUntil[hoodId] = uint64(block.timestamp + 7 days);
        emit ActivitySustainedRefreshed(hoodId, activitySustainedUntil[hoodId]);
    }

    function setBazaarEscrowed(uint256 hoodId, bool escrowed) external override onlyBazaar {
        bazaarEscrowed[hoodId] = escrowed;
    }

    function bazaarLock(uint256 tokenId) external override onlyBazaar {
        bazaarEscrowed[tokenId] = true;
    }

    function bazaarUnlock(uint256 tokenId) external override onlyBazaar {
        bazaarEscrowed[tokenId] = false;
    }

    function currentMonthEpoch() public view returns (uint32) {
        if (block.timestamp < GENESIS_TIME) return 0;
        uint256 elapsed = block.timestamp - GENESIS_TIME;
        uint32 yearIndex = uint32(elapsed / 365 days);
        uint256 day = (elapsed % 365 days) / 1 days;
        uint32 monthInYear = uint32(day < 360 ? day / 30 : 11);

        return yearIndex * 12 + monthInYear;
    }

    function currentUtcDay() public view override returns (uint32) {
        return uint32(block.timestamp / 1 days);
    }

    function setPendingNormalHeist(uint256 hoodId, bool pending) external override {
        if (pending) {
            require(activeEngine[msg.sender], "Not active engine");
            hasPendingNormalHeist[hoodId] = true;
        } else {
            require(resolverEngine[msg.sender], "Not resolver engine");
            hasPendingNormalHeist[hoodId] = false;
        }
    }

    function setFatigue(uint256 hoodId, bool fatigued) external onlyResolverEngine {
        isHeroFatigued[hoodId] = fatigued;
        emit FatigueStateChanged(hoodId, fatigued);
    }

    function settleGoldFraction(uint256 hoodId, uint256 scaledNumerator) external onlyResolverEngine returns (uint256 wholeGold) {
        uint256 total = goldCarry[hoodId] + scaledNumerator;
        wholeGold = total / 100_000_000;
        goldCarry[hoodId] = total % 100_000_000;
    }

    function incrementPendingGameplay(uint256 hoodId, uint32 count) external onlyActiveEngine {
        pendingGameplayCount[hoodId] += count;
    }
    function decrementPendingGameplay(uint256 hoodId, uint32 count) external onlyResolverEngine {
        require(pendingGameplayCount[hoodId] >= count, "Gameplay counter underflow");
        pendingGameplayCount[hoodId] -= count;
    }

    function incrementPendingEventEntitlement(uint256 hoodId) external onlyResolverEngine {
        pendingEventEntitlementCount[hoodId]++;
    }
    function decrementPendingEventEntitlement(uint256 hoodId) external onlySettlementEngine {
        require(pendingEventEntitlementCount[hoodId] > 0, "Event entitlement underflow");
        pendingEventEntitlementCount[hoodId]--;
    }

    function incrementSolsticeCommitment(uint256 hoodId) external override onlyActiveEngine {
        activeSolsticeCommitmentCount[hoodId]++;
    }
    function decrementSolsticeCommitment(uint256 hoodId) external override onlyResolverEngine {
        require(activeSolsticeCommitmentCount[hoodId] > 0, "Solstice commitment underflow");
        activeSolsticeCommitmentCount[hoodId]--;
    }

    function solsticeCommitmentCount(uint256 tokenId) external view override returns (uint8) {
        return uint8(activeSolsticeCommitmentCount[tokenId]);
    }

    function canList(uint256 hoodId) public view override returns (bool allowed, uint256 reasonFlags) {
        if (pendingGameplayCount[hoodId] > 0) reasonFlags |= 1;
        if (pendingUnequipCount[hoodId] > 0) reasonFlags |= 2;
        if (pendingDebondMaturesAt[hoodId] > 0) reasonFlags |= 4;
        if (activeSolsticeCommitmentCount[hoodId] > 0) reasonFlags |= 8;
        if (pendingEventEntitlementCount[hoodId] > 0) reasonFlags |= 16;
        if (bazaarEscrowed[hoodId]) reasonFlags |= 32;
        allowed = (reasonFlags == 0);
    }

    function setBazaarTransferMode(BazaarTransferMode mode) external override onlyBazaar {
        bazaarTransferMode = mode;
    }

    function _update(address to, uint256 tokenId, address auth) internal override returns (address from) {
        from = super._update(to, tokenId, auth);
        
        if (to == address(bazaarContract)) {
            require(bazaarContract.expectedDeposit(tokenId) == from, "Unsolicited Bazaar deposit prohibited");
        }
        
        if (from != address(0) && to != address(0) && from != to) {
            for (uint8 s = 0; s < 7; s++) {
                delete pendingUnequip[tokenId][s];
            }
            pendingUnequipCount[tokenId] = 0;
            delete pendingDebondMaturesAt[tokenId];
            
            if (msg.sender == address(bazaarContract)) {
                if (bazaarTransferMode == BazaarTransferMode.CANCEL_WITHDRAWAL) {
                    // Cancellation returns to original seller: no lock, preserve delegateEpoch
                } else if (bazaarTransferMode == BazaarTransferMode.SALE_PURCHASE) {
                    postTransferUnequipLockedUntil[tokenId] = uint64(block.timestamp + 24 hours);
                    delegateEpoch[tokenId]++;
                }
            } else {
                postTransferUnequipLockedUntil[tokenId] = uint64(block.timestamp + 24 hours);
                delegateEpoch[tokenId]++;
            }
        }
    }

    function isGameDelegate(uint256 hoodId, address operator) public view override returns (bool) {
        return delegateGrantedEpoch[hoodId][operator] == delegateEpoch[hoodId] && delegateEpoch[hoodId] > 0;
    }

    function setGameDelegate(uint256 hoodId, address operator, bool authorized) external {
        require(ownerOf(hoodId) == msg.sender, "Not owner");
        if (authorized) {
            delegateGrantedEpoch[hoodId][operator] = delegateEpoch[hoodId];
        } else {
            delegateGrantedEpoch[hoodId][operator] = 0;
        }
    }

    function economicActionsPaused() public view override returns (bool) {
        return block.timestamp < guardianPauseUntil;
    }

    function triggerGuardianPause() external onlyGuardian {
        require(block.timestamp >= guardianPauseUntil, "Already paused");
        require(block.timestamp >= lastGuardianPauseStarted + 7 days, "Pause cooldown active");
        guardianPauseUntil = uint64(block.timestamp + 72 hours);
        lastGuardianPauseStarted = uint64(block.timestamp);
        emit EmergencyPauseTriggered(guardianPauseUntil);
    }

    function protectedUntil(uint256 id) public view returns (uint64) {
        uint64 careProtect = lastCareTimestamp[id] + 3 days;
        uint64 actProtect = activitySustainedUntil[id];

        if (equippedSlot[id][4] == FRIARS_CORNUCOPIA) {
            return careProtect > actProtect ? careProtect : actProtect;
        }

        uint64 rationProtect = rationsUntil[id];
        uint64 maxSustain = actProtect > rationProtect ? actProtect : rationProtect;
        return careProtect > maxSustain ? careProtect : maxSustain;
    }

    function isSlumbering(uint256 id) public view override returns (bool) {
        return block.timestamp > protectedUntil(id);
    }

    function _settleSlumber(uint256 tokenId) internal {
        uint64 protect = protectedUntil(tokenId);
        uint64 start = protect > slumberAccountedUntil[tokenId] ? protect : slumberAccountedUntil[tokenId];
        if (block.timestamp > start) {
            completedSlumberSeconds[tokenId] += uint64(block.timestamp - start);
            slumberAccountedUntil[tokenId] = uint64(block.timestamp);
        }
    }

    function dailyCare(uint256 hoodId) external {
        _requireOwned(hoodId);
        require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(lastCareDay[hoodId] < currentUtcDay(), "Already cared today");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        
        _settleSlumber(hoodId);
        lastCareDay[hoodId] = currentUtcDay();
        lastCareTimestamp[hoodId] = uint64(block.timestamp);
        emit DailyCarePerformed(hoodId, currentUtcDay());
    }

    function effectiveBiologicalAge(uint256 tokenId) public view override returns (uint256) {
        uint256 totalElapsed = block.timestamp - mintTimestamp[tokenId];
        uint256 slumberTime = completedSlumberSeconds[tokenId];
        uint64 protect = protectedUntil(tokenId);
        uint64 start = protect > slumberAccountedUntil[tokenId] ? protect : slumberAccountedUntil[tokenId];
        if (block.timestamp > start) {
            slumberTime += (block.timestamp - start);
        }
        return totalElapsed > slumberTime ? totalElapsed - slumberTime : 0;
    }

    function feed(uint256 hoodId) external {
        _requireOwned(hoodId);
        require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(!isSlumbering(hoodId), "Hero is slumbering");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        
        _settleSlumber(hoodId);
        treasuresContract.burnRationBasket(msg.sender, 1);
        
        uint256 currentRations = rationsUntil[hoodId];
        uint256 baseTime = currentRations > block.timestamp ? currentRations : block.timestamp;
        uint256 newRations = baseTime + 7 days;
        require(newRations <= block.timestamp + 56 days, "Max 8 baskets / 56 days prepayment");
        
        rationsUntil[hoodId] = uint64(newRations);
        emit HeroFed(hoodId, newRations);
    }

    function effectiveEconomicRewardBps(uint256 hoodId) public view returns (uint256) {
        bool hasCornucopia = (equippedSlot[hoodId][4] == FRIARS_CORNUCOPIA);
        bool activityFed = (block.timestamp <= activitySustainedUntil[hoodId]);
        bool rationFed = (block.timestamp <= rationsUntil[hoodId]);
        
        return (hasCornucopia || activityFed || rationFed) ? 10000 : 5000;
    }

    function devotionBonusBps(uint256 tokenId) public view returns (uint16) {
        uint256 awakeDays = effectiveBiologicalAge(tokenId) / 1 days;
        if (awakeDays >= 360) return 1000;
        if (awakeDays >= 180) return 600;
        if (awakeDays >= 90)  return 400;
        if (awakeDays >= 30)  return 200;
        return 0;
    }

    function consumeStamina(uint256 hoodId, uint8 count) external override onlyActiveEngine {
        consumeStaminaBatch(hoodId, count);
    }

    function consumeStaminaBatch(uint256 hoodId, uint8 count) public onlyActiveEngine returns (uint8 baseConsumed, uint8 bonusConsumed) {
        if (currentUtcDay() > lastHeistDay[hoodId]) {
            baseHeistsUsed[hoodId] = 0;
            bonusHeistsUsed[hoodId] = 0;
            lastHeistDay[hoodId] = currentUtcDay();
        }
        
        uint8 baseRemaining = 5 - baseHeistsUsed[hoodId];
        if (count <= baseRemaining) {
            baseHeistsUsed[hoodId] += count;
            return (count, 0);
        } else {
            baseConsumed = baseRemaining;
            bonusConsumed = count - baseConsumed;
            require(lastElixirDay[hoodId] == currentUtcDay(), "Bonus stamina not unlocked");
            require(bonusHeistsUsed[hoodId] + bonusConsumed <= 5, "Exceeds daily bonus stamina");
            baseHeistsUsed[hoodId] = 5;
            bonusHeistsUsed[hoodId] += bonusConsumed;
            return (baseConsumed, bonusConsumed);
        }
    }

    function useElixir(uint256 hoodId) external {
        require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(!economicActionsPaused(), "Economic actions paused");
        require(!isSlumbering(hoodId), "Hero is slumbering");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        require(lastElixirDay[hoodId] < currentUtcDay(), "Elixir already used today");
        
        treasuresContract.burnElixir(msg.sender, 1);
        lastElixirDay[hoodId] = currentUtcDay();
        emit ElixirUsed(hoodId, currentUtcDay());
    }

    function equipItem(uint256 hoodId, uint8 slot, uint32 itemId) external nonReentrant {
        require(msg.sender == ownerOf(hoodId), "Not owner");
        require(slot <= 5, "Invalid gear slot");
        require(isEquippable[itemId], "Item not equippable");
        require(canonicalItemSlot[itemId] == slot, "Item does not belong in this slot");
        require(equippedSlot[hoodId][slot] == 0, "Slot occupied: unequip first");
        require(pendingUnequip[hoodId][slot].maturesAt == 0, "Unequip notice active");
        require(block.timestamp >= postTransferUnequipLockedUntil[hoodId], "Post-transfer unequip lock active");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        
        if (slot == 2 && itemId == GOLDEN_ARROW) {
            uint32 w = equippedSlot[hoodId][0];
            require(w == GILDED_BOW || w == YEW_LONGBOW, "Golden Arrow requires bow");
            require(pendingUnequip[hoodId][0].maturesAt == 0, "Cannot equip Arrow while Bow unequip pending");
        }
        
        if (slot == 4 && itemId == FRIARS_CORNUCOPIA) {
            _settleSlumber(hoodId);
            cornucopiaBoundTimestamp[hoodId] = uint64(block.timestamp);
        }
        
        equippedSlot[hoodId][slot] = itemId;
        boundCount[itemId]++;
        
        if (slot == 4 && itemId == FRIARS_CORNUCOPIA) {
            slumberAccountedUntil[hoodId] = uint64(block.timestamp);
        }
        
        treasuresContract.safeTransferFrom(msg.sender, address(this), itemId, 1, "");
        loadoutVersion[hoodId]++;
        emit MetadataUpdate(hoodId);
        emit ItemEquipped(hoodId, slot, itemId);
    }

    function initiateUnequip(uint256 hoodId, uint8 slot) external {
        require(msg.sender == ownerOf(hoodId), "Not owner");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        uint32 itemId = equippedSlot[hoodId][slot];
        require(itemId != 0, "Slot is empty");
        require(pendingUnequip[hoodId][slot].maturesAt == 0, "Already initiated");
        require(block.timestamp >= postTransferUnequipLockedUntil[hoodId], "Post-transfer lock active");
        
        if (slot == 0) {
            require(equippedSlot[hoodId][2] != GOLDEN_ARROW, "Unequip ammo first");
        }
        if (slot == 4 && itemId == FRIARS_CORNUCOPIA) {
            require(block.timestamp >= cornucopiaBoundTimestamp[hoodId] + 7 days, "Cornucopia 7-day bind lock active");
        }
        
        pendingUnequip[hoodId][slot] = UnequipRequest(uint64(block.timestamp + 24 hours), itemId);
        pendingUnequipCount[hoodId]++;
        emit UnequipInitiated(hoodId, slot, itemId, block.timestamp + 24 hours);
    }

    function finalizeUnequip(uint256 hoodId, uint8 slot) external nonReentrant {
        require(msg.sender == ownerOf(hoodId), "Not owner");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        UnequipRequest memory req = pendingUnequip[hoodId][slot];
        require(req.maturesAt > 0, "No pending unequip");
        require(block.timestamp >= req.maturesAt, "Maturation period not reached");
        require(equippedSlot[hoodId][slot] == req.itemId, "Item mismatch");
        
        if (slot == 0) {
            require(equippedSlot[hoodId][2] != GOLDEN_ARROW, "Cannot finalize Bow removal while Golden Arrow equipped");
        }
        
        if (slot == 4 && req.itemId == FRIARS_CORNUCOPIA) {
            require(!isSlumbering(hoodId), "Care required before Cornucopia removal");
            _settleSlumber(hoodId);
        }
        
        delete pendingUnequip[hoodId][slot];
        pendingUnequipCount[hoodId]--;
        equippedSlot[hoodId][slot] = 0;
        boundCount[req.itemId]--;
        
        if (slot == 4 && req.itemId == FRIARS_CORNUCOPIA) {
            slumberAccountedUntil[hoodId] = uint64(block.timestamp);
        }
        
        loadoutVersion[hoodId]++;
        emit MetadataUpdate(hoodId);
        treasuresContract.safeTransferFrom(address(this), msg.sender, req.itemId, 1, "");
        emit UnequipFinalized(hoodId, slot, req.itemId);
    }

    function bondPet(uint256 hoodId, uint256 petId) external nonReentrant {
        require(msg.sender == ownerOf(hoodId), "Not Hood owner");
        require(companionContract.ownerOf(petId) == msg.sender, "Not pet owner");
        require(hoodBoundPet[hoodId] == 0, "Hood already has companion");
        require(petBoundToHood[petId] == 0, "Pet already bonded");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        
        petBoundToHood[petId] = hoodId;
        hoodBoundPet[hoodId] = petId;
        petBondedAt[petId] = uint64(block.timestamp);
        companionContract.recordBondAge(petId, uint64(effectiveBiologicalAge(hoodId)));
        
        expectedPetDeposit[petId] = msg.sender;
        companionContract.safeTransferFrom(msg.sender, address(this), petId);
        delete expectedPetDeposit[petId];
        
        loadoutVersion[hoodId]++;
        emit MetadataUpdate(hoodId);
        emit PetBonded(hoodId, petId);
    }

    function initiateDebond(uint256 hoodId) external {
        require(msg.sender == ownerOf(hoodId), "Not Hood owner");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        uint256 petId = hoodBoundPet[hoodId];
        require(petId != 0, "No pet bonded");
        require(block.timestamp >= petBondedAt[petId] + 12 hours, "12h initial bond lock active");
        require(pendingDebondMaturesAt[hoodId] == 0, "Debond already active");
        
        pendingDebondMaturesAt[hoodId] = uint64(block.timestamp + 12 hours);
        emit DebondInitiated(hoodId, petId, block.timestamp + 12 hours);
    }

    function finalizeDebond(uint256 hoodId) external nonReentrant {
        require(msg.sender == ownerOf(hoodId), "Not Hood owner");
        require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
        require(pendingDebondMaturesAt[hoodId] > 0, "No pending debond");
        require(block.timestamp >= pendingDebondMaturesAt[hoodId], "Debond timer not mature");
        
        uint256 petId = hoodBoundPet[hoodId];
        delete pendingDebondMaturesAt[hoodId];
        delete hoodBoundPet[hoodId];
        delete petBoundToHood[petId];
        
        companionContract.settleDebondAge(petId, uint64(effectiveBiologicalAge(hoodId)));
        
        loadoutVersion[hoodId]++;
        emit MetadataUpdate(hoodId);
        companionContract.safeTransferFrom(address(this), msg.sender, petId);
        emit DebondFinalized(hoodId, petId);
    }

    function getLoadoutHash(uint256 hoodId) public view override returns (bytes32) {
        return keccak256(abi.encode(
            equippedSlot[hoodId][0], // weapon
            equippedSlot[hoodId][1], // armor
            equippedSlot[hoodId][2], // ammo
            equippedSlot[hoodId][3], // utility
            equippedSlot[hoodId][4], // sustenanceRelic
            equippedSlot[hoodId][5], // decor
            hoodBoundPet[hoodId],    // companion
            loadoutVersion[hoodId]
        ));
    }

    function effectiveCombatStats(uint256 hoodId) public view returns (uint8 atk, uint8 def, uint8 stealth) {
        atk = 0;
        def = 0;
        stealth = 0;
        
        uint32 w = equippedSlot[hoodId][0];
        if (w == GILDED_BOW) atk += 20;
        else if (w == YEW_LONGBOW) atk += 10;
        else if (w == QUARTERSTAFF) def += 15;
        else if (w == POACHER_DAGGERS) stealth += 15;
        
        uint32 a = equippedSlot[hoodId][1];
        if (a == LOCKSLEY_CLOAK) {
            def += 20;
            stealth += 10;
        }
        
        uint32 ammo = equippedSlot[hoodId][2];
        if (ammo == GOLDEN_ARROW) {
            atk += 25;
        }
        
        uint256 petId = hoodBoundPet[hoodId];
        if (petId != 0 && address(companionContract) != address(0)) {
            uint8 sp = companionContract.species(petId);
            uint8 rank = companionContract.bondRank(petId); // 1..5
            if (rank >= 1 && rank <= 5) {
                uint256 idx = rank - 1;
                if (sp == 0) {
                    uint8[5] memory houndDef = [uint8(0), 2, 4, 6, 10];
                    def += houndDef[idx];
                } else if (sp == 2) {
                    uint8[5] memory owlStealth = [uint8(0), 1, 2, 3, 5];
                    stealth += owlStealth[idx];
                }
            }
        }
        
        if (atk > 45) atk = 45;
        if (def > 30) def = 30;
        if (stealth > 30) stealth = 30;
    }

    function captureHeistSnapshot(uint256 hoodId) external view override returns (HeistSnapshot memory) {
        (uint8 atk, uint8 def, uint8 stealth) = effectiveCombatStats(hoodId);
        uint16 critBps = 0;
        uint16 goldBonusBps = 0;
        
        uint256 petId = hoodBoundPet[hoodId];
        if (petId != 0 && address(companionContract) != address(0)) {
            uint8 sp = companionContract.species(petId);
            uint8 rank = companionContract.bondRank(petId); // 1..5
            if (rank >= 1 && rank <= 5) {
                uint256 idx = rank - 1;
                if (sp == 1) {
                    uint16[5] memory falconCrit = [uint16(0), 160, 320, 480, 800];
                    critBps = falconCrit[idx];
                } else if (sp == 2) {
                    uint16[5] memory owlGold = [uint16(0), 200, 400, 600, 1000];
                    goldBonusBps = owlGold[idx];
                }
            }
        }
        
        if (equippedSlot[hoodId][0] == GILDED_BOW) {
            goldBonusBps += 2000;
        }
        goldBonusBps += devotionBonusBps(hoodId);
        if (goldBonusBps > 4000) goldBonusBps = 4000;
        
        return HeistSnapshot({
            atk: atk,
            def: def,
            stealth: stealth,
            critBps: critBps,
            goldBonusBps: goldBonusBps,
            economicRewardBps: uint16(effectiveEconomicRewardBps(hoodId)),
            initialFatigue: isHeroFatigued[hoodId]
        });
    }

    function captureCombatSnapshot(uint256 hoodId) external view override returns (CombatSnapshot memory) {
        HeistSnapshot memory h = this.captureHeistSnapshot(hoodId);
        uint8 morale = (equippedSlot[hoodId][3] == SILVER_RALLYING_HORN) ? 10 : 0;
        return CombatSnapshot({
            atk: h.atk,
            def: h.def,
            stealth: h.stealth,
            critBps: h.critBps,
            goldBonusBps: h.goldBonusBps,
            economicRewardBps: h.economicRewardBps,
            initialFatigue: h.initialFatigue,
            morale: morale
        });
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        address rend = address(renderer);
        if (rend != address(0)) {
            bytes memory callData = abi.encodeWithSelector(IRenderer.tokenURI.selector, tokenId);
            uint256 maxLen = 100_000;
            bool ok;
            uint256 size;
            
            assembly {
                ok := staticcall(2000000, rend, add(callData, 0x20), mload(callData), 0, 0)
                size := returndatasize()
            }
            
            if (ok && size >= 64 && size <= maxLen) {
                bytes memory data = new bytes(size);
                assembly {
                    returndatacopy(add(data, 0x20), 0, size)
                }
                uint256 offset;
                uint256 strLen;
                assembly {
                    offset := mload(add(data, 0x20))
                    strLen := mload(add(data, 0x40))
                }
                if (offset == 32 && strLen <= size - 64) {
                    uint256 padded = (strLen + 31) & ~uint256(31);
                    if (64 + padded <= size) {
                        return abi.decode(data, (string));
                    }
                }
            }
        }
        return _fallbackTokenURI(tokenId);
    }

    function _fallbackTokenURI(uint256 tokenId) internal pure returns (string memory) {
        return string(abi.encodePacked(
            '{"name": "Hood #',
            tokenId.toString(),
            '", "description": "HoodQuest Outlaw"}'
        ));
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721Enumerable, ERC1155Holder, IERC165) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
