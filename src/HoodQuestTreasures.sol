// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ERC1155Supply } from "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import { ERC1155 } from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import { ReentrancyGuard } from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import { SupplyMode, MintSource, RewardBundle, CraftRecipe } from "./HoodQuestTypes.sol";
import { IHoodQuestTreasures } from "./interfaces/IHoodQuestTreasures.sol";
import { IHoodQuest } from "./interfaces/IHoodQuest.sol";
import { IHoodQuestCompanions } from "./interfaces/IHoodQuestCompanions.sol";

contract HoodQuestTreasures is ERC1155Supply, ReentrancyGuard, IHoodQuestTreasures {
    address public immutable timelock;
    IHoodQuest public immutable hoodContract;
    IHoodQuestCompanions public companionContract;
    address public bazaarContract;

    uint256 public constant GOLD = 1;
    uint256 public constant MEAD_CASK = 2;
    uint256 public constant GILDED_BOW = 3;
    uint256 public constant GOLDEN_ARROW = 4;
    uint256 public constant GREENWOOD_ELIXIR = 5;
    uint256 public constant VELVET_CLOAK = 6;
    uint256 public constant FEAST_BASKET = 7;
    uint256 public constant RALLYING_HORN = 8;
    uint256 public constant FRIARS_CORNUCOPIA = 9;
    uint256 public constant YEW_LONGBOW = 13;
    uint256 public constant QUARTERSTAFF = 14;
    uint256 public constant POACHER_DAGGERS = 15;
    uint256 public constant YEW = 16;
    uint256 public constant IRON = 17;
    uint256 public constant GOLDEN_GRAIL = 20;

    mapping(address => bool) public activeRaidEngine;    // May request heists, consume stamina, create events
    mapping(address => bool) public resolverApproved;     // May resolve existing requests & reserve drops/trophies
    mapping(address => bool) public settlementApproved;   // May settle existing reward claims & event liabilities

    // Item configurations & caps
    mapping(uint256 => SupplyMode) public itemSupplyMode;
    mapping(uint256 => uint256) public itemLifetimeCap;
    mapping(uint256 => uint256) public lifetimeMinted;
    mapping(uint256 => uint256) public reservedUnclaimed;

    uint256 public droppedGildedBows;
    uint256 public dropReservedGildedBows;
    uint256 public forgedGildedBows;

    // Rebate reserve state
    uint256 public cumulativeGoldBurned;
    uint16 public rebateCarryBps;
    uint256 public cumulativeRebateCredits;
    uint256 public freeRebateReserve;
    uint256 public outstandingEventGold;
    uint256 public cumulativeEventGoldMinted;

    // Event reservations
    mapping(address => mapping(uint256 => uint256)) public eventGoldReserved;
    mapping(address => mapping(uint256 => uint256)) public eventGoldMinted;
    mapping(address => mapping(uint256 => mapping(uint256 => uint256))) public eventTrophyReserved;
    mapping(uint256 => uint256) public forfeitedGrails;

    // Blacksmith recipes
    mapping(uint256 => CraftRecipe) public craftRecipes;

    // Expansion module state
    uint256 public constant MAX_EXPANSION_DAILY_CAP = 25_000;
    uint256 public totalAllocatedDailyCap;
    mapping(uint256 => bool) public itemRegistered;
    mapping(uint256 => address) public itemAuthorizedModule;
    mapping(address => uint256) public moduleDailyCap;
    mapping(address => bool) public isModuleAuthorized;
    mapping(address => uint32) public moduleMintDay;
    mapping(address => uint256) public moduleMintedToday;

    event EngineRolesChanged(address indexed engine, bool active, bool resolver, bool settlement);
    event EventBudgetReserved(uint256 indexed eventId, uint256 budget);
    event EventBudgetRefunded(uint256 indexed eventId, uint256 amount);
    event EventTrophyReserved(address indexed engine, uint256 indexed eventId, uint256 indexed itemId, uint256 quantity);
    event TrophyPermanentlyForfeited(uint256 indexed eventId, uint256 indexed itemId);
    event ItemCrafted(address indexed crafter, uint256 indexed itemId, uint256 quantity);
    event ExpansionItemRegistered(uint256 indexed id, address indexed module, SupplyMode mode, uint256 cap);
    event ExpansionItemMinted(address indexed module, address indexed to, uint256 indexed itemId, uint256 amount);
    event ExpansionGoldRewarded(address indexed module, address indexed to, uint256 amount);
    event ModuleAuthorizationChanged(address indexed module, bool authorized, uint256 dailyCap);
    event HeistRewardsSettled(address indexed recipient, RewardBundle bundle);
    event BazaarPaymentSettled(address indexed buyer, address indexed seller, uint256 price, uint256 fee);

    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
        _;
    }
    modifier onlyResolverApproved() {
        require(resolverApproved[msg.sender], "Not resolver approved");
        _;
    }
    modifier onlySettlementApproved() {
        require(settlementApproved[msg.sender], "Not settlement approved");
        _;
    }
    modifier onlyCompanions() {
        require(msg.sender == address(companionContract), "Not companions");
        _;
    }
    modifier onlyBazaar() {
        require(msg.sender == bazaarContract, "Not bazaar");
        _;
    }
    modifier onlyHoodQuest() {
        require(msg.sender == address(hoodContract), "Not HoodQuest Core");
        _;
    }

    constructor(address timelock_, address hoodContract_) ERC1155("") {
        require(timelock_ != address(0), "Invalid timelock");
        require(hoodContract_ != address(0), "Invalid hood contract");
        timelock = timelock_;
        hoodContract = IHoodQuest(hoodContract_);

        // Initialize Canonical Item Modes & Caps
        itemSupplyMode[GOLD] = SupplyMode.UNCAPPED;

        itemSupplyMode[MEAD_CASK] = SupplyMode.MAX_CIRCULATING;
        itemLifetimeCap[MEAD_CASK] = 5_000;
        craftRecipes[MEAD_CASK] = CraftRecipe(true, SupplyMode.MAX_CIRCULATING, 5_000, 5, 0, 0);

        itemSupplyMode[GILDED_BOW] = SupplyMode.SPLIT;
        itemLifetimeCap[GILDED_BOW] = 1_000;
        craftRecipes[GILDED_BOW] = CraftRecipe(true, SupplyMode.SPLIT, 1_000, 60, 5, 5);

        itemSupplyMode[GOLDEN_ARROW] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[GOLDEN_ARROW] = 25;

        itemSupplyMode[GREENWOOD_ELIXIR] = SupplyMode.MAX_CIRCULATING;
        itemLifetimeCap[GREENWOOD_ELIXIR] = 2_500;
        craftRecipes[GREENWOOD_ELIXIR] = CraftRecipe(true, SupplyMode.MAX_CIRCULATING, 2_500, 25, 0, 0);

        itemSupplyMode[VELVET_CLOAK] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[VELVET_CLOAK] = 750;
        craftRecipes[VELVET_CLOAK] = CraftRecipe(true, SupplyMode.MAX_LIFETIME, 750, 30, 2, 2);

        itemSupplyMode[FEAST_BASKET] = SupplyMode.UNCAPPED;
        craftRecipes[FEAST_BASKET] = CraftRecipe(true, SupplyMode.UNCAPPED, 0, 14, 0, 0);

        itemSupplyMode[RALLYING_HORN] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[RALLYING_HORN] = 500;
        craftRecipes[RALLYING_HORN] = CraftRecipe(true, SupplyMode.MAX_LIFETIME, 500, 35, 3, 3);

        itemSupplyMode[FRIARS_CORNUCOPIA] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[FRIARS_CORNUCOPIA] = 25;

        itemSupplyMode[YEW_LONGBOW] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[YEW_LONGBOW] = 10_000;
        craftRecipes[YEW_LONGBOW] = CraftRecipe(true, SupplyMode.MAX_LIFETIME, 10_000, 10, 2, 0);

        itemSupplyMode[QUARTERSTAFF] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[QUARTERSTAFF] = 2_500;
        craftRecipes[QUARTERSTAFF] = CraftRecipe(true, SupplyMode.MAX_LIFETIME, 2_500, 20, 3, 1);

        itemSupplyMode[POACHER_DAGGERS] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[POACHER_DAGGERS] = 1_500;
        craftRecipes[POACHER_DAGGERS] = CraftRecipe(true, SupplyMode.MAX_LIFETIME, 1_500, 25, 1, 3);

        itemSupplyMode[YEW] = SupplyMode.UNCAPPED;
        itemSupplyMode[IRON] = SupplyMode.UNCAPPED;

        itemSupplyMode[GOLDEN_GRAIL] = SupplyMode.MAX_LIFETIME;
        itemLifetimeCap[GOLDEN_GRAIL] = 25;
    }

    function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyTimelock {
        activeRaidEngine[engine] = active;
        resolverApproved[engine] = resolver;
        settlementApproved[engine] = settlement;
        emit EngineRolesChanged(engine, active, resolver, settlement);
    }

    function setBazaarContract(address bazaar_) external onlyTimelock {
        require(bazaar_ != address(0), "Invalid bazaar");
        bazaarContract = bazaar_;
    }

    function setCompanionContract(address companions_) external onlyTimelock {
        require(companions_ != address(0), "Invalid companions");
        companionContract = IHoodQuestCompanions(companions_);
    }

    function reserveItem(
        uint256 itemId,
        MintSource source,
        uint256 requestedAmount
    ) external onlyResolverApproved returns (uint256 reservedAmount) {
        if (requestedAmount == 0) return 0;
        
        if (itemId == GILDED_BOW) {
            require(source == MintSource.DROP, "Gilded Bow reserved strictly from drops");
            uint256 dropAvail = 0;
            if (droppedGildedBows + dropReservedGildedBows < 250) {
                dropAvail = 250 - (droppedGildedBows + dropReservedGildedBows);
            }
            uint256 totalAvail = 0;
            if (lifetimeMinted[itemId] + reservedUnclaimed[itemId] < 1000) {
                totalAvail = 1000 - (lifetimeMinted[itemId] + reservedUnclaimed[itemId]);
            }
            uint256 avail = dropAvail < totalAvail ? dropAvail : totalAvail;
            reservedAmount = requestedAmount <= avail ? requestedAmount : avail;
            dropReservedGildedBows += reservedAmount;
            reservedUnclaimed[itemId] += reservedAmount;
            return reservedAmount;
        }
        
        SupplyMode mode = itemSupplyMode[itemId];
        uint256 cap = itemLifetimeCap[itemId];
        if (mode == SupplyMode.UNCAPPED) return requestedAmount;
        
        if (mode == SupplyMode.MAX_CIRCULATING) {
            uint256 current = totalSupply(itemId) + reservedUnclaimed[itemId];
            if (current >= cap) return 0;
            uint256 avail = cap - current;
            reservedAmount = requestedAmount <= avail ? requestedAmount : avail;
            reservedUnclaimed[itemId] += reservedAmount;
            return reservedAmount;
        }
        
        if (mode == SupplyMode.MAX_LIFETIME) {
            uint256 current = lifetimeMinted[itemId] + reservedUnclaimed[itemId];
            if (current >= cap) return 0;
            uint256 avail = cap - current;
            reservedAmount = requestedAmount <= avail ? requestedAmount : avail;
            reservedUnclaimed[itemId] += reservedAmount;
            return reservedAmount;
        }
        
        return 0;
    }

    function reserveEventBudget(uint256 eventId, uint256 cap) external onlyResolverApproved returns (uint256 budget) {
        budget = cap < freeRebateReserve ? cap : freeRebateReserve;
        freeRebateReserve -= budget;
        outstandingEventGold += budget;
        eventGoldReserved[msg.sender][eventId] = budget;
        emit EventBudgetReserved(eventId, budget);
    }

    function mintReservedEventGold(address recipient, uint256 eventId, uint256 amount) external onlySettlementApproved nonReentrant {
        require(eventGoldMinted[msg.sender][eventId] + amount <= eventGoldReserved[msg.sender][eventId], "Exceeds reserved budget");
        eventGoldMinted[msg.sender][eventId] += amount;
        outstandingEventGold -= amount;
        cumulativeEventGoldMinted += amount;
        _mint(recipient, 1, amount, "");
    }

    function refundEventBudget(uint256 eventId, uint256 amount) external onlySettlementApproved {
        require(eventGoldMinted[msg.sender][eventId] + amount <= eventGoldReserved[msg.sender][eventId], "Refund exceeds reserved");
        eventGoldReserved[msg.sender][eventId] -= amount;
        outstandingEventGold -= amount;
        freeRebateReserve += amount;
        emit EventBudgetRefunded(eventId, amount);
    }

    function reserveEventTrophy(uint256 eventId, uint256 itemId, uint256 quantity) external onlyResolverApproved {
        require(lifetimeMinted[itemId] + reservedUnclaimed[itemId] + forfeitedGrails[itemId] + quantity <= 25, "Grail cap exceeded");
        reservedUnclaimed[itemId] += quantity;
        eventTrophyReserved[msg.sender][eventId][itemId] += quantity;
        emit EventTrophyReserved(msg.sender, eventId, itemId, quantity);
    }

    function settleEventTrophy(uint256 eventId, address recipient, uint256 itemId, uint256 amount) public onlySettlementApproved nonReentrant {
        require(eventTrophyReserved[msg.sender][eventId][itemId] >= amount, "No event trophy reservation");
        require(reservedUnclaimed[itemId] >= amount, "No global reservation");
        eventTrophyReserved[msg.sender][eventId][itemId] -= amount;
        reservedUnclaimed[itemId] -= amount;
        lifetimeMinted[itemId] += amount;
        _mint(recipient, itemId, amount, "");
    }

    function forfeitEventTrophy(uint256 eventId, uint256 itemId, uint256 amount) public onlySettlementApproved {
        require(eventTrophyReserved[msg.sender][eventId][itemId] >= amount, "No event trophy reservation");
        require(reservedUnclaimed[itemId] >= amount, "No global reservation");
        eventTrophyReserved[msg.sender][eventId][itemId] -= amount;
        reservedUnclaimed[itemId] -= amount;
        forfeitedGrails[itemId] += amount;
        emit TrophyPermanentlyForfeited(eventId, itemId);
    }

    function mintReservedTrophy(uint256 eventId, address recipient, uint256 itemId) external onlySettlementApproved nonReentrant {
        require(eventTrophyReserved[msg.sender][eventId][itemId] > 0, "No event trophy reservation");
        require(reservedUnclaimed[itemId] > 0, "No global reservation");
        eventTrophyReserved[msg.sender][eventId][itemId]--;
        reservedUnclaimed[itemId]--;
        lifetimeMinted[itemId]++;
        _mint(recipient, itemId, 1, "");
    }

    function forfeitReservedTrophy(uint256 eventId, uint256 itemId) external onlySettlementApproved {
        require(eventTrophyReserved[msg.sender][eventId][itemId] > 0, "No event trophy reservation");
        require(reservedUnclaimed[itemId] > 0, "No global reservation");
        eventTrophyReserved[msg.sender][eventId][itemId]--;
        reservedUnclaimed[itemId]--;
        forfeitedGrails[itemId]++;
        emit TrophyPermanentlyForfeited(eventId, itemId);
    }

    function _burnGold(address from, uint256 amount) internal {
        _burn(from, 1, amount);
        cumulativeGoldBurned += amount;
        uint256 scaled = amount * 2500 + rebateCarryBps;
        uint256 credit = scaled / 10_000;
        rebateCarryBps = uint16(scaled % 10_000);
        cumulativeRebateCredits += credit;
        freeRebateReserve += credit;
    }

    function registerExpansionItem(
        uint256 id,
        address module,
        SupplyMode mode,
        uint256 cap
    ) external onlyTimelock {
        require(id >= 21, "IDs 1..20 reserved for core");
        require(!itemRegistered[id], "Item already registered");
        require(mode != SupplyMode.SPLIT, "Expansion SPLIT mode unsupported in V1");
        require(module != address(0), "Invalid module address");
        
        itemRegistered[id] = true;
        itemSupplyMode[id] = mode;
        itemLifetimeCap[id] = cap;
        itemAuthorizedModule[id] = module;
        emit ExpansionItemRegistered(id, module, mode, cap);
    }

    function mintExpansionItem(address to, uint256 itemId, uint256 amount) external nonReentrant {
        require(itemRegistered[itemId], "Item not registered");
        require(msg.sender == itemAuthorizedModule[itemId], "Not authorized module");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        require(to != address(0), "Invalid recipient");

        SupplyMode mode = itemSupplyMode[itemId];
        uint256 cap = itemLifetimeCap[itemId];

        if (mode == SupplyMode.MAX_LIFETIME) {
            require(lifetimeMinted[itemId] + amount <= cap, "Lifetime cap exceeded");
            lifetimeMinted[itemId] += amount;
        } else if (mode == SupplyMode.MAX_CIRCULATING) {
            require(totalSupply(itemId) + amount <= cap, "Circulating cap exceeded");
        }
        // SupplyMode.UNCAPPED allows minting without cap check

        _mint(to, itemId, amount, "");
        emit ExpansionItemMinted(msg.sender, to, itemId, amount);
    }

    function settleHeistRewardBundle(address recipient, RewardBundle calldata bundle) external onlySettlementApproved nonReentrant {
        require(recipient != address(0), "Invalid recipient");
        if (bundle.gold > 0) _mint(recipient, 1, bundle.gold, "");
        if (bundle.yew > 0) _mint(recipient, YEW, bundle.yew, "");
        if (bundle.iron > 0) _mint(recipient, IRON, bundle.iron, "");
        if (bundle.baskets > 0) _mint(recipient, FEAST_BASKET, bundle.baskets, "");
        if (bundle.elixirs > 0) {
            lifetimeMinted[GREENWOOD_ELIXIR] += bundle.elixirs;
            reservedUnclaimed[GREENWOOD_ELIXIR] -= bundle.elixirs;
            _mint(recipient, GREENWOOD_ELIXIR, bundle.elixirs, "");
        }
        if (bundle.gildedBows > 0) {
            droppedGildedBows += bundle.gildedBows;
            dropReservedGildedBows -= bundle.gildedBows;
            reservedUnclaimed[GILDED_BOW] -= bundle.gildedBows;
            lifetimeMinted[GILDED_BOW] += bundle.gildedBows;
            _mint(recipient, GILDED_BOW, bundle.gildedBows, "");
        }
        if (bundle.yewLongbows > 0) {
            lifetimeMinted[YEW_LONGBOW] += bundle.yewLongbows;
            reservedUnclaimed[YEW_LONGBOW] -= bundle.yewLongbows;
            _mint(recipient, YEW_LONGBOW, bundle.yewLongbows, "");
        }
        if (bundle.quarterstaffs > 0) {
            lifetimeMinted[QUARTERSTAFF] += bundle.quarterstaffs;
            reservedUnclaimed[QUARTERSTAFF] -= bundle.quarterstaffs;
            _mint(recipient, QUARTERSTAFF, bundle.quarterstaffs, "");
        }
        if (bundle.poacherDaggers > 0) {
            lifetimeMinted[POACHER_DAGGERS] += bundle.poacherDaggers;
            reservedUnclaimed[POACHER_DAGGERS] -= bundle.poacherDaggers;
            _mint(recipient, POACHER_DAGGERS, bundle.poacherDaggers, "");
        }
        emit HeistRewardsSettled(recipient, bundle);
    }

    function craft(uint256 itemId, uint256 quantity) external nonReentrant {
        require(quantity > 0, "Quantity must be > 0");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        
        CraftRecipe memory r = craftRecipes[itemId];
        require(r.isValid, "Item not craftable");
        
        if (r.mode == SupplyMode.SPLIT && itemId == GILDED_BOW) {
            require(forgedGildedBows + quantity <= 750, "Forge cap reached");
            forgedGildedBows += quantity;
        } else if (r.mode == SupplyMode.MAX_LIFETIME) {
            require(lifetimeMinted[itemId] + reservedUnclaimed[itemId] + quantity <= r.cap, "Lifetime cap reached");
        } else if (r.mode == SupplyMode.MAX_CIRCULATING) {
            require(totalSupply(itemId) + reservedUnclaimed[itemId] + quantity <= r.cap, "Circulating cap reached");
        }
        
        _burnGold(msg.sender, r.goldCost * quantity);
        if (r.yewCost > 0) _burn(msg.sender, YEW, r.yewCost * quantity);
        if (r.ironCost > 0) _burn(msg.sender, IRON, r.ironCost * quantity);
        
        lifetimeMinted[itemId] += quantity;
        _mint(msg.sender, itemId, quantity, "");
        emit ItemCrafted(msg.sender, itemId, quantity);
    }

    function burnAdoptionGold(address from, uint256 amount) external onlyCompanions {
        _burnGold(from, amount);
    }

    function mintForageMaterial(address to, uint256 itemId, uint256 amount) external onlyCompanions {
        require(itemId == YEW || itemId == IRON, "Invalid forage item");
        _mint(to, itemId, amount, "");
    }

    function burnElixir(address from, uint256 amount) external onlyHoodQuest {
        _burn(from, GREENWOOD_ELIXIR, amount);
    }

    function burnRationBasket(address from, uint256 amount) external onlyHoodQuest {
        _burn(from, FEAST_BASKET, amount);
    }

    function settleBazaarPayment(
        address buyer,
        address seller,
        uint256 price,
        uint256 fee
    ) external onlyBazaar nonReentrant returns (uint256 sellerProceeds) {
        require(price >= fee, "Fee exceeds price");
        sellerProceeds = price - fee;
        
        _burnGold(buyer, fee);
        _safeTransferFrom(buyer, msg.sender, 1, sellerProceeds, "");
        emit BazaarPaymentSettled(buyer, seller, price, fee);
    }

    function setModuleAuthorization(address module, uint256 dailyCap, bool authorized) external onlyTimelock {
        if (authorized && !isModuleAuthorized[module]) {
            require(dailyCap > 0, "Cap must be > 0");
            require(totalAllocatedDailyCap + dailyCap <= MAX_EXPANSION_DAILY_CAP, "Exceeds 25k daily cap");
            totalAllocatedDailyCap += dailyCap;
            moduleDailyCap[module] = dailyCap;
            isModuleAuthorized[module] = true;
        } else if (!authorized && isModuleAuthorized[module]) {
            totalAllocatedDailyCap -= moduleDailyCap[module];
            moduleDailyCap[module] = 0;
            isModuleAuthorized[module] = false;
        }
        emit ModuleAuthorizationChanged(module, authorized, dailyCap);
    }

    function rewardExpansionGold(address to, uint256 amount) external nonReentrant {
        require(isModuleAuthorized[msg.sender], "Unauthorized module");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        require(to != address(0), "Invalid recipient");
        
        uint32 today = uint32(block.timestamp / 1 days);
        if (today > moduleMintDay[msg.sender]) {
            moduleMintDay[msg.sender] = today;
            moduleMintedToday[msg.sender] = 0;
        }
        
        require(moduleMintedToday[msg.sender] + amount <= moduleDailyCap[msg.sender], "Exceeds daily module cap");
        moduleMintedToday[msg.sender] += amount;
        _mint(to, 1, amount, "");
        emit ExpansionGoldRewarded(msg.sender, to, amount);
    }

    function _update(address from, address to, uint256[] memory ids, uint256[] memory values) internal override {
        if (to == address(hoodContract)) {
            require(msg.sender == address(hoodContract), "Unsolicited armory deposit");
        }
        for (uint256 i = 0; i < ids.length; i++) {
            if (ids[i] == YEW || ids[i] == IRON) {
                require(from == address(0) || to == address(0), "Soulbound: non-transferable");
            }
        }
        super._update(from, to, ids, values);
    }
}
