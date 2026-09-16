// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ERC721Enumerable } from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import { IERC721Receiver } from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
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

contract HoodQuest is ERC721Enumerable, IERC721Receiver, IHoodQuest {

    uint8 private _reentrantLock;
    modifier nonReentrant() {
        if (_reentrantLock != 0) revert();
        _reentrantLock = 1;
        _;
        _reentrantLock = 0;
    }

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
    uint32 internal constant GILDED_BOW = 3;
    uint32 internal constant GOLDEN_ARROW = 4;
    uint32 internal constant LOCKSLEY_CLOAK = 6;
    uint32 internal constant SILVER_RALLYING_HORN = 8;
    uint32 internal constant FRIARS_CORNUCOPIA = 9;
    uint32 internal constant YEW_LONGBOW = 13;
    uint32 internal constant QUARTERSTAFF = 14;
    uint32 internal constant POACHER_DAGGERS = 15;

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
    mapping(uint32 => uint8) public expansionItemSlot;
    event ExpansionItemSlotRegistered(uint32 indexed itemId, uint8 slot);

    function canonicalItemSlot(uint32 itemId) public view returns (uint8) {
        if (itemId == 3 || itemId == 13 || itemId == 14 || itemId == 15) return 0;
        if (itemId == 6) return 1;
        if (itemId == 4) return 2;
        if (itemId == 8) return 3;
        if (itemId == 9) return 4;
        if (itemId == 2) return 5;
        uint8 exp = expansionItemSlot[itemId];
        return exp > 0 ? exp - 1 : 255;
    }
    function isEquippable(uint32 itemId) public view returns (bool) {
        return canonicalItemSlot(itemId) <= 5;
    }
    function setExpansionItemSlot(uint32 itemId, uint8 slot) external onlyTimelock {
        if (slot > 5) revert();
        expansionItemSlot[itemId] = slot + 1;
        emit ExpansionItemSlotRegistered(itemId, slot);
    }
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
    event UnequipCancelled(uint256 indexed hoodId, uint8 slot);
    event PetBonded(uint256 indexed hoodId, uint256 petId);
    event DebondInitiated(uint256 indexed hoodId, uint256 petId, uint256 maturesAt);
    event DebondFinalized(uint256 indexed hoodId, uint256 petId);
    event DebondCancelled(uint256 indexed hoodId, uint256 petId);
    event EmergencyPauseTriggered(uint64 pauseUntil);
    event MetadataUpdate(uint256 _tokenId);

    modifier onlyTimelock() {
        if (msg.sender != timelock) revert();
        _;
    }

    modifier onlyActiveEngine() {
        if (!activeEngine[msg.sender]) revert();
        _;
    }

    modifier onlyResolverEngine() {
        if (!resolverEngine[msg.sender]) revert();
        _;
    }

    function _checkOwnerNotBazaar(uint256 hoodId) internal view {
        if (msg.sender != ownerOf(hoodId) || bazaarEscrowed[hoodId]) revert();
    }

    constructor(
        uint256 mintPriceWei_,
        address proceedsRecipient_,
        uint256 genesisTime_,
        address timelock_,
        address guardian_
    ) ERC721("HoodQuest", "HQ") {
        if (proceedsRecipient_ == address(0) || genesisTime_ > block.timestamp || timelock_ == address(0) || guardian_ == address(0)) revert();
        MINT_PRICE_WEI = mintPriceWei_;
        PROCEEDS_RECIPIENT = proceedsRecipient_;
        GENESIS_TIME = genesisTime_;
        timelock = timelock_;
        guardian = guardian_;

    }

    function setGuardian(address guardian_) external onlyTimelock {
        if (guardian_ == address(0)) revert();
        guardian = guardian_;
        emit GuardianUpdated(guardian_);
    }

    function setBazaarContract(address bazaar_) external onlyTimelock {
        if (bazaar_ == address(0)) revert();
        bazaarContract = IHoodQuestBazaar(bazaar_);
    }

    function setCompanionContract(address companions_) external onlyTimelock {
        if (companions_ == address(0)) revert();
        companionContract = IHoodQuestCompanions(companions_);
    }

    function setTreasuresContract(address treasures_) external onlyTimelock {
        if (treasures_ == address(0)) revert();
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
        if (msg.sender != address(companionContract) || expectedPetDeposit[petId] != from) revert();
        return IERC721Receiver.onERC721Received.selector;
    }

    function _arbBlock() internal view returns (uint256) {
        try ArbSys(address(0x64)).arbBlockNumber() returns (uint256 bn) { return bn; }
        catch { return block.number; }
    }

    function mintHoods(uint8 count) external payable nonReentrant {
        if (count == 0 || count > 5 || totalHoodsMinted + count > MAX_HOOD_SUPPLY) revert();
        if (msg.value != MINT_PRICE_WEI * count) revert();
        
        uint256 currentArbBlock = _arbBlock();
        uint32 initCareDay = currentUtcDay() > 0 ? currentUtcDay() - 1 : 0;
        uint64 nowTs = uint64(block.timestamp);

        for (uint8 i = 0; i < count; i++) {
            uint256 id = ++totalHoodsMinted;
            mintTimestamp[id] = nowTs;
            lastCareTimestamp[id] = nowTs;
            lastCareDay[id] = initCareDay;
            delegateEpoch[id] = 1;
            rationsUntil[id] = nowTs + 7 days;
            slumberAccountedUntil[id] = nowTs;
            seedTargetBlock[id] = currentArbBlock + 2;
            _safeMint(msg.sender, id);
        }
    }

    function withdrawMintProceeds() external nonReentrant {
        uint256 balance = address(this).balance;
        if (balance == 0) revert();
        (bool success, ) = PROCEEDS_RECIPIENT.call{value: balance}("");
        if (!success) revert();
    }

    function finalizeHeroSeed(uint256 tokenId) external {
        if (heroSeed[tokenId] != bytes32(0)) revert();
        uint256 target = seedTargetBlock[tokenId];
        if (target == 0) revert();
        uint256 current = _arbBlock();
        if (current <= target) revert();
        bytes32 bHash;
        if (current <= target + 256) {
            try ArbSys(address(0x64)).arbBlockHash(target) returns (bytes32 bh) {
                bHash = bh;
            } catch {
                bHash = blockhash(target);
            }
        }
        if (bHash != bytes32(0)) {
            heroSeed[tokenId] = keccak256(abi.encode(bHash, tokenId, address(this), block.chainid));
        } else {
            heroSeed[tokenId] = keccak256(abi.encode("STANDARD_GENESIS", tokenId, GENESIS_TIME));
            standardGenesis[tokenId] = true;
        }
        heroArchetype[tokenId] = uint8(uint256(heroSeed[tokenId]) % 5);
        emit HeroSeedFinalized(tokenId, heroSeed[tokenId]);
    }

    function _refreshActivity(uint256 hoodId) internal {
        activitySustainedUntil[hoodId] = uint64(block.timestamp + 7 days);
        emit ActivitySustainedRefreshed(hoodId, activitySustainedUntil[hoodId]);
    }

    function refreshActivitySustained(uint256 hoodId) external onlyActiveEngine {
        _refreshActivity(hoodId);
    }

    function touchActivity(uint256 hoodId) external override onlyActiveEngine {
        _refreshActivity(hoodId);
    }

    function _setBazaarEscrowed(uint256 hoodId, bool escrowed) internal {
        if (msg.sender != address(bazaarContract)) revert();
        bazaarEscrowed[hoodId] = escrowed;
    }

    function setBazaarEscrowed(uint256 hoodId, bool escrowed) external override {
        _setBazaarEscrowed(hoodId, escrowed);
    }

    function bazaarLock(uint256 tokenId) external override {
        _setBazaarEscrowed(tokenId, true);
    }

    function bazaarUnlock(uint256 tokenId) external override {
        _setBazaarEscrowed(tokenId, false);
    }

    function currentMonthEpoch() public view returns (uint32) {
        if (block.timestamp < GENESIS_TIME) return 0;
        uint256 elapsed = block.timestamp - GENESIS_TIME;
        uint256 day = (elapsed % 365 days) / 1 days;
        return uint32(elapsed / 365 days) * 12 + uint32(day < 360 ? day / 30 : 11);
    }

    function currentUtcDay() public view override returns (uint32) {
        return uint32(block.timestamp / 1 days);
    }

    function setPendingNormalHeist(uint256 hoodId, bool pending) external override {
        if (pending) {
            if (!activeEngine[msg.sender]) revert();
            hasPendingNormalHeist[hoodId] = true;
        } else {
            if (!resolverEngine[msg.sender]) revert();
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
        if (pendingGameplayCount[hoodId] < count) revert();
        pendingGameplayCount[hoodId] -= count;
    }

    function incrementPendingEventEntitlement(uint256 hoodId) external onlyResolverEngine {
        pendingEventEntitlementCount[hoodId]++;
    }
    function decrementPendingEventEntitlement(uint256 hoodId) external override {
        if (!settlementEngine[msg.sender] || pendingEventEntitlementCount[hoodId] == 0) revert();
        pendingEventEntitlementCount[hoodId]--;
    }

    function incrementSolsticeCommitment(uint256 hoodId) external override onlyActiveEngine {
        activeSolsticeCommitmentCount[hoodId]++;
    }
    function decrementSolsticeCommitment(uint256 hoodId) external override onlyResolverEngine {
        if (activeSolsticeCommitmentCount[hoodId] == 0) revert();
        activeSolsticeCommitmentCount[hoodId]--;
    }

    function solsticeCommitmentCount(uint256 tokenId) external view override returns (uint8) {
        return uint8(activeSolsticeCommitmentCount[tokenId]);
    }

    function canList(uint256 hoodId) public view override returns (bool allowed, uint256 reasonFlags) {
        if (pendingGameplayCount[hoodId] != 0) reasonFlags |= 1;
        if (pendingUnequipCount[hoodId] != 0) reasonFlags |= 2;
        if (pendingDebondMaturesAt[hoodId] != 0) reasonFlags |= 4;
        if (activeSolsticeCommitmentCount[hoodId] != 0) reasonFlags |= 8;
        if (pendingEventEntitlementCount[hoodId] != 0) reasonFlags |= 16;
        if (bazaarEscrowed[hoodId]) reasonFlags |= 32;
        allowed = (reasonFlags == 0);
    }

    function setBazaarTransferMode(BazaarTransferMode mode) external override {
        if (msg.sender != address(bazaarContract)) revert();
        bazaarTransferMode = mode;
    }

    function _update(address to, uint256 tokenId, address auth) internal override returns (address from) {
        from = super._update(to, tokenId, auth);
        
        if (to == address(bazaarContract) && bazaarContract.expectedDeposit(tokenId) != from) revert();
        
        if (from != address(0) && to != address(0) && from != to) {
            for (uint8 s = 0; s < 6; ++s) {
                delete pendingUnequip[tokenId][s];
            }
            pendingUnequipCount[tokenId] = 0;
            delete pendingDebondMaturesAt[tokenId];
            
            if (msg.sender != address(bazaarContract) || bazaarTransferMode == BazaarTransferMode.SALE_PURCHASE) {
                postTransferUnequipLockedUntil[tokenId] = uint64(block.timestamp + 24 hours);
                delegateEpoch[tokenId]++;
            }
        }
    }

    function isGameDelegate(uint256 hoodId, address operator) public view override returns (bool) {
        return delegateGrantedEpoch[hoodId][operator] == delegateEpoch[hoodId] && delegateEpoch[hoodId] > 0;
    }

    function setGameDelegate(uint256 hoodId, address operator, bool authorized) external {
        if (ownerOf(hoodId) != msg.sender) revert();
        if (authorized) {
            delegateGrantedEpoch[hoodId][operator] = delegateEpoch[hoodId];
        } else {
            delegateGrantedEpoch[hoodId][operator] = 0;
        }
    }

    function economicActionsPaused() public view override returns (bool) {
        return block.timestamp < guardianPauseUntil;
    }

    function triggerGuardianPause() external {
        if (msg.sender != guardian || block.timestamp < guardianPauseUntil || block.timestamp < lastGuardianPauseStarted + 7 days) revert();
        guardianPauseUntil = uint64(block.timestamp + 72 hours);
        lastGuardianPauseStarted = uint64(block.timestamp);
        emit EmergencyPauseTriggered(guardianPauseUntil);
    }

    function protectedUntil(uint256 id) public view returns (uint64) {
        uint64 care = lastCareTimestamp[id] + 3 days;
        uint64 act = activitySustainedUntil[id];
        if (equippedSlot[id][4] == FRIARS_CORNUCOPIA) {
            return care > act ? care : act;
        }
        uint64 r = rationsUntil[id];
        uint64 s = act > r ? act : r;
        return care > s ? care : s;
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

    function _checkOwnerOrDelegate(uint256 hoodId) internal view {
        if (msg.sender != ownerOf(hoodId) && !isGameDelegate(hoodId, msg.sender)) revert();
    }

    function dailyCare(uint256 hoodId) external {
        _checkOwnerOrDelegate(hoodId);
        uint32 today = currentUtcDay();
        if (lastCareDay[hoodId] >= today || bazaarEscrowed[hoodId]) revert();
        
        _settleSlumber(hoodId);
        lastCareDay[hoodId] = today;
        lastCareTimestamp[hoodId] = uint64(block.timestamp);
        emit DailyCarePerformed(hoodId, today);
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
        _checkOwnerOrDelegate(hoodId);
        if (isSlumbering(hoodId) || bazaarEscrowed[hoodId]) revert();
        
        _settleSlumber(hoodId);
        treasuresContract.burnRationBasket(msg.sender, 1);
        
        uint256 currentRations = rationsUntil[hoodId];
        uint256 baseTime = currentRations > block.timestamp ? currentRations : block.timestamp;
        uint256 newRations = baseTime + 7 days;
        if (newRations > block.timestamp + 56 days) revert();
        
        rationsUntil[hoodId] = uint64(newRations);
        emit HeroFed(hoodId, newRations);
    }

    function effectiveEconomicRewardBps(uint256 hoodId) public view returns (uint256) {
        return (equippedSlot[hoodId][4] == FRIARS_CORNUCOPIA ||
            block.timestamp <= activitySustainedUntil[hoodId] ||
            block.timestamp <= rationsUntil[hoodId]) ? 10000 : 5000;
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
        uint32 today = currentUtcDay();
        if (today > lastHeistDay[hoodId]) {
            baseHeistsUsed[hoodId] = 0;
            bonusHeistsUsed[hoodId] = 0;
            lastHeistDay[hoodId] = today;
        }
        
        uint8 baseRemaining = 5 - baseHeistsUsed[hoodId];
        if (count <= baseRemaining) {
            baseHeistsUsed[hoodId] += count;
            return (count, 0);
        } else {
            baseConsumed = baseRemaining;
            bonusConsumed = count - baseConsumed;
            if (lastElixirDay[hoodId] != today || bonusHeistsUsed[hoodId] + bonusConsumed > 5) revert();
            baseHeistsUsed[hoodId] = 5;
            bonusHeistsUsed[hoodId] += bonusConsumed;
            return (baseConsumed, bonusConsumed);
        }
    }

    function useElixir(uint256 hoodId) external {
        _checkOwnerOrDelegate(hoodId);
        uint32 today = currentUtcDay();
        if (economicActionsPaused() || isSlumbering(hoodId) || bazaarEscrowed[hoodId] || lastElixirDay[hoodId] >= today) revert();
        
        treasuresContract.burnElixir(msg.sender, 1);
        lastElixirDay[hoodId] = today;
        emit ElixirUsed(hoodId, today);
    }

    function _equipSingle(uint256 hoodId, uint8 slot, uint32 itemId) internal {
        if (slot > 5 || !isEquippable(itemId) || canonicalItemSlot(itemId) != slot || equippedSlot[hoodId][slot] != 0 || pendingUnequip[hoodId][slot].maturesAt != 0 || block.timestamp < postTransferUnequipLockedUntil[hoodId]) revert();
        
        if (slot == 2 && itemId == GOLDEN_ARROW) {
            uint32 w = equippedSlot[hoodId][0];
            if (w != GILDED_BOW && w != YEW_LONGBOW) revert();
            if (pendingUnequip[hoodId][0].maturesAt != 0) revert();
        }
        
        if (slot == 4 && itemId == FRIARS_CORNUCOPIA) {
            _settleSlumber(hoodId);
            cornucopiaBoundTimestamp[hoodId] = uint64(block.timestamp);
            slumberAccountedUntil[hoodId] = uint64(block.timestamp);
        }
        
        equippedSlot[hoodId][slot] = itemId;
        boundCount[itemId]++;
        
        treasuresContract.safeTransferFrom(msg.sender, address(this), itemId, 1, "");
        emit ItemEquipped(hoodId, slot, itemId);
    }

    function equipItem(uint256 hoodId, uint8 slot, uint32 itemId) external nonReentrant {
        _checkOwnerNotBazaar(hoodId);
        _equipSingle(hoodId, slot, itemId);
        _touchLoadout(hoodId);
    }

    function equipBatch(uint256 hoodId, uint8[] calldata slots, uint32[] calldata itemIds) external nonReentrant {
        _checkOwnerNotBazaar(hoodId);
        uint256 len = slots.length;
        if (len != itemIds.length || len == 0 || len > 6) revert();
        for (uint256 i = 0; i < len; ++i) {
            _equipSingle(hoodId, slots[i], itemIds[i]);
        }
        _touchLoadout(hoodId);
    }

    function initiateUnequip(uint256 hoodId, uint8 slot) external {
        _checkOwnerNotBazaar(hoodId);
        uint32 itemId = equippedSlot[hoodId][slot];
        if (itemId == 0 || pendingUnequip[hoodId][slot].maturesAt != 0 || block.timestamp < postTransferUnequipLockedUntil[hoodId]) revert();
        
        if (slot == 0 && equippedSlot[hoodId][2] == GOLDEN_ARROW) revert();
        if (slot == 4 && itemId == FRIARS_CORNUCOPIA && block.timestamp < cornucopiaBoundTimestamp[hoodId] + 7 days) revert();
        
        pendingUnequip[hoodId][slot] = UnequipRequest(uint64(block.timestamp + 24 hours), itemId);
        pendingUnequipCount[hoodId]++;
        emit UnequipInitiated(hoodId, slot, itemId, block.timestamp + 24 hours);
    }

    function cancelUnequip(uint256 hoodId, uint8 slot) external {
        _checkOwnerNotBazaar(hoodId);
        if (slot > 5 || pendingUnequip[hoodId][slot].maturesAt == 0) revert();
        delete pendingUnequip[hoodId][slot];
        if (pendingUnequipCount[hoodId] > 0) {
            pendingUnequipCount[hoodId]--;
        }
        _touchLoadout(hoodId);
        emit UnequipCancelled(hoodId, slot);
    }

    function finalizeUnequip(uint256 hoodId, uint8 slot) external nonReentrant {
        _checkOwnerNotBazaar(hoodId);
        UnequipRequest memory req = pendingUnequip[hoodId][slot];
        if (req.maturesAt == 0 || block.timestamp < req.maturesAt || equippedSlot[hoodId][slot] != req.itemId) revert();
        
        if (slot == 0 && equippedSlot[hoodId][2] == GOLDEN_ARROW) revert();
        
        if (slot == 4 && req.itemId == FRIARS_CORNUCOPIA) {
            if (isSlumbering(hoodId)) revert();
            _settleSlumber(hoodId);
            slumberAccountedUntil[hoodId] = uint64(block.timestamp);
        }
        
        delete pendingUnequip[hoodId][slot];
        pendingUnequipCount[hoodId]--;
        equippedSlot[hoodId][slot] = 0;
        boundCount[req.itemId]--;
        
        _touchLoadout(hoodId);
        treasuresContract.safeTransferFrom(address(this), msg.sender, req.itemId, 1, "");
        emit UnequipFinalized(hoodId, slot, req.itemId);
    }

    function _touchLoadout(uint256 hoodId) internal {
        loadoutVersion[hoodId]++;
        emit MetadataUpdate(hoodId);
    }

    function bondPet(uint256 hoodId, uint256 petId) external nonReentrant {
        _checkOwnerNotBazaar(hoodId);
        if (companionContract.ownerOf(petId) != msg.sender || hoodBoundPet[hoodId] != 0 || petBoundToHood[petId] != 0) revert();
        
        petBoundToHood[petId] = hoodId;
        hoodBoundPet[hoodId] = petId;
        petBondedAt[petId] = uint64(block.timestamp);
        companionContract.recordBondAge(petId, uint64(effectiveBiologicalAge(hoodId)));
        
        expectedPetDeposit[petId] = msg.sender;
        companionContract.safeTransferFrom(msg.sender, address(this), petId);
        delete expectedPetDeposit[petId];
        
        _touchLoadout(hoodId);
        emit PetBonded(hoodId, petId);
    }

    function initiateDebond(uint256 hoodId) external {
        _checkOwnerNotBazaar(hoodId);
        uint256 petId = hoodBoundPet[hoodId];
        if (petId == 0 || block.timestamp < petBondedAt[petId] + 12 hours || pendingDebondMaturesAt[hoodId] != 0) revert();
        
        pendingDebondMaturesAt[hoodId] = uint64(block.timestamp + 12 hours);
        emit DebondInitiated(hoodId, petId, block.timestamp + 12 hours);
    }

    function finalizeDebond(uint256 hoodId) external nonReentrant {
        _checkOwnerNotBazaar(hoodId);
        if (pendingDebondMaturesAt[hoodId] == 0 || block.timestamp < pendingDebondMaturesAt[hoodId]) revert();
        
        uint256 petId = hoodBoundPet[hoodId];
        delete pendingDebondMaturesAt[hoodId];
        delete hoodBoundPet[hoodId];
        delete petBoundToHood[petId];
        
        companionContract.settleDebondAge(petId, uint64(effectiveBiologicalAge(hoodId)));
        
        _touchLoadout(hoodId);
        companionContract.safeTransferFrom(address(this), msg.sender, petId);
        emit DebondFinalized(hoodId, petId);
    }

    function cancelDebond(uint256 hoodId) external {
        _checkOwnerNotBazaar(hoodId);
        if (pendingDebondMaturesAt[hoodId] == 0) revert();
        delete pendingDebondMaturesAt[hoodId];
        _touchLoadout(hoodId);
        emit DebondCancelled(hoodId, hoodBoundPet[hoodId]);
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

    function _calcCombatStats(uint256 hoodId) internal view returns (
        uint8 atk,
        uint8 def,
        uint8 stealth,
        uint16 critBps,
        uint16 goldBonusBps
    ) {
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
            if (rank >= 2 && rank <= 5) {
                if (sp == 0) {
                    def += rank == 5 ? 10 : (rank - 1) * 2;
                } else if (sp == 1) {
                    critBps = rank == 5 ? 800 : (rank - 1) * 160;
                } else if (sp == 2) {
                    stealth += rank == 5 ? 5 : (rank - 1);
                    goldBonusBps = rank == 5 ? 1000 : (rank - 1) * 200;
                } else if (sp == 3) {
                    stealth += rank == 5 ? 8 : (rank - 1) * 2;
                    critBps = rank == 5 ? 400 : (rank - 1) * 80;
                }
            }
        }
        
        if (atk > 45) atk = 45;
        if (def > 30) def = 30;
        if (stealth > 30) stealth = 30;
    }

    function captureHeistSnapshot(uint256 hoodId) public view override returns (HeistSnapshot memory) {
        (uint8 atk, uint8 def, uint8 stealth, uint16 critBps, uint16 goldBonusBps) = _calcCombatStats(hoodId);
        
        if (equippedSlot[hoodId][0] == GILDED_BOW) {
            goldBonusBps += 2000;
        }
        goldBonusBps += devotionBonusBps(hoodId);
        if (goldBonusBps > 4000) goldBonusBps = 4000;
        
        return HeistSnapshot(
            atk,
            def,
            stealth,
            critBps,
            goldBonusBps,
            uint16(effectiveEconomicRewardBps(hoodId)),
            isHeroFatigued[hoodId]
        );
    }

    function captureCombatSnapshot(uint256 hoodId) external view override returns (CombatSnapshot memory) {
        HeistSnapshot memory h = captureHeistSnapshot(hoodId);
        uint8 morale = (equippedSlot[hoodId][3] == SILVER_RALLYING_HORN) ? 10 : 0;
        return CombatSnapshot(
            h.atk,
            h.def,
            h.stealth,
            h.critBps,
            h.goldBonusBps,
            h.economicRewardBps,
            h.initialFatigue,
            morale
        );
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        return address(renderer) != address(0) ? renderer.tokenURI(tokenId) : "";
    }

    function onERC1155Received(address, address, uint256, uint256, bytes calldata) external pure returns (bytes4) {
        return 0xf23a6e61;
    }
    function onERC1155BatchReceived(address, address, uint256[] calldata, uint256[] calldata, bytes calldata) external pure returns (bytes4) {
        return 0xbc197c81;
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721Enumerable, IERC165) returns (bool) {
        return interfaceId == 0xd9b67a26 || super.supportsInterface(interfaceId);
    }
}
