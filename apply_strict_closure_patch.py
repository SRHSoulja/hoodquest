import re

with open('/home/arson/rhnftproject/generate_final_blueprint.py', 'r') as f:
    code = f.read()

# ==============================================================================
# 1. Section 0: Covenant update acknowledging authorized changes
# ==============================================================================
old_covenant = '- **No Semantic Mutation Covenant:** Numeric constants, item IDs, item names, supply modes, recipes, drop rates, stat effects, companion rewards, starvation percentages, event dates, and previously approved gameplay formulas are immutable.'

new_covenant = '- **No Semantic Mutation Covenant:** Numeric constants, item IDs, item names, supply modes, recipes, drop rates, stat effects, companion rewards, starvation percentages, event dates, and previously approved gameplay formulas are immutable, subject strictly to the two authorized gameplay closures: (1) Active adventuring substitutes for food upkeep via token-bound activitySustainedUntil, and (2) Normal-heist rewards settle atomically during permissionless resolution directly to a snapshotted recipient.'

assert old_covenant in code, "old_covenant not found"
code = code.replace(old_covenant, new_covenant, 1)

# ==============================================================================
# 2. Section 1: Update Pillars / active gameplay sustenance description
# ==============================================================================
old_pantry_desc = '1. **"25 Years" Means 25 Years of Active Devotion:**'
new_pantry_desc = """1. **Active Adventuring Sustains Heroes (Passive Inactivity Protection):** Active players sustain their Hoods simply by adventuring (`activitySustainedUntil = now + 7 days` refreshed on heists and world events). Forest Feast Baskets (Item #7) exist as passive inactivity protection for owners taking real-world breaks.
2. **"25 Years" Means 25 Years of Active Devotion:**"""

assert old_pantry_desc in code, "old_pantry_desc not found"
code = code.replace(old_pantry_desc, new_pantry_desc, 1)

# ==============================================================================
# 3. Section 2: File-level declarations in HoodQuestTypes.sol
# ==============================================================================
old_types_decl = '''### 0. Canonical Shared Types Library (HoodQuestTypes.sol - HQ-SNAP-001):
To guarantee compile closure and eliminate struct divergence across contracts, all shared types live in `HoodQuestTypes.sol`:
```solidity
library HoodQuestTypes {
    enum SupplyMode { UNCAPPED, MAX_LIFETIME, MAX_CIRCULATING, SPLIT }
    enum MintSource { DROP, EVENT }
    enum EventKind { CASTLE, TAX_TRAIN, JUBILEE, SOLSTICE }
    enum ActionKind { CASTLE, TAX_TRAIN, JUBILEE }

    struct HeistSnapshot {
        uint8 atk;
        uint8 def;
        uint8 stealth;
        uint16 critBps;
        uint16 goldBonusBps;
        uint16 economicRewardBps;
        bool initialFatigue;
    }

    struct CombatSnapshot {
        uint8 atk;
        uint8 def;
        uint8 stealth;
        uint16 critBps;
        uint16 goldBonusBps;
        uint16 economicRewardBps;
        bool initialFatigue;
        uint8 morale;
    }

    struct RewardBundle {
        uint256 gold;
        uint256 yew;
        uint256 iron;
        uint256 baskets;
        uint256 elixirs;
        uint256 gildedBows;
        uint256 yewLongbows;
        uint256 quarterstaffs;
        uint256 poacherDaggers;
    }

    struct EventConfig {
        bool exists;
        EventKind kind;
        uint32 eventYear;
        uint64 startTime;
        uint64 endTime;
        uint32 cap;
    }

    struct CraftRecipe {
        bool isValid;
        SupplyMode mode;
        uint256 cap;
        uint256 goldCost;
        uint256 yewCost;
        uint256 ironCost;
    }
}
```'''

new_types_decl = '''### 0. Canonical Shared Types Library (HoodQuestTypes.sol - HQ-SNAP-001):
To guarantee complete Solidity type closure and eliminate struct divergence across contracts, all shared enums and structs are declared at file-level in `HoodQuestTypes.sol` and imported explicitly:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

enum SupplyMode { UNCAPPED, MAX_LIFETIME, MAX_CIRCULATING, SPLIT }
enum MintSource { DROP, EVENT }
enum EventKind { CASTLE, TAX_TRAIN, JUBILEE, SOLSTICE }
enum ActionKind { CASTLE, TAX_TRAIN, JUBILEE }

struct HeistSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
}

struct CombatSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
    uint8 morale;
}

struct RewardBundle {
    uint256 gold;
    uint256 yew;
    uint256 iron;
    uint256 baskets;
    uint256 elixirs;
    uint256 gildedBows;
    uint256 yewLongbows;
    uint256 quarterstaffs;
    uint256 poacherDaggers;
}

struct EventConfig {
    bool exists;
    EventKind kind;
    uint32 eventYear;
    uint64 startTime;
    uint64 endTime;
    uint32 cap;
}

struct CraftRecipe {
    bool isValid;
    SupplyMode mode;
    uint256 cap;
    uint256 goldCost;
    uint256 yewCost;
    uint256 ironCost;
}
```'''

assert old_types_decl in code, "old_types_decl not found"
code = code.replace(old_types_decl, new_types_decl, 1)

# ==============================================================================
# 4. Section 2: Core Constructor Timelock/Guardian Wiring, expectedPetDeposit, activitySustainedUntil
# ==============================================================================
old_core_constructor = '''    constructor(
        uint256 mintPriceWei_,
        address proceedsRecipient_,
        uint256 genesisTime_
    ) {
        require(proceedsRecipient_ != address(0), "Invalid recipient");
        require(genesisTime_ <= block.timestamp, "Genesis in future");
        MINT_PRICE_WEI = mintPriceWei_;
        PROCEEDS_RECIPIENT = proceedsRecipient_;
        GENESIS_TIME = genesisTime_;
    }'''

new_core_constructor = '''    address public immutable timelock;
    address public guardian;
    IHoodQuestCompanions public companionContract;
    address public bazaarContract;

    constructor(
        uint256 mintPriceWei_,
        address proceedsRecipient_,
        uint256 genesisTime_,
        address timelock_,
        address guardian_
    ) {
        require(proceedsRecipient_ != address(0), "Invalid recipient");
        require(genesisTime_ <= block.timestamp, "Genesis in future");
        require(timelock_ != address(0), "Invalid timelock");
        require(guardian_ != address(0), "Invalid guardian");
        MINT_PRICE_WEI = mintPriceWei_;
        PROCEEDS_RECIPIENT = proceedsRecipient_;
        GENESIS_TIME = genesisTime_;
        timelock = timelock_;
        guardian = guardian_;
    }

    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
        _;
    }
    modifier onlyGuardian() {
        require(msg.sender == guardian, "Not guardian");
        _;
    }
    modifier onlyBazaar() {
        require(msg.sender == bazaarContract, "Not bazaar");
        _;
    }

    function setGuardian(address guardian_) external onlyTimelock {
        require(guardian_ != address(0), "Invalid guardian");
        guardian = guardian_;
        emit GuardianUpdated(guardian_);
    }

    function setBazaarContract(address bazaar_) external onlyTimelock {
        require(bazaar_ != address(0), "Invalid bazaar");
        bazaarContract = bazaar_;
    }

    function setCompanionContract(address companions_) external onlyTimelock {
        require(companions_ != address(0), "Invalid companions");
        companionContract = IHoodQuestCompanions(companions_);
    }

    function pauseEconomicActions(bool paused) external {
        require(msg.sender == guardian || msg.sender == timelock, "Not guardian or timelock");
        economicActionsPaused = paused;
        emit EconomicActionsPaused(paused);
    }'''

assert old_core_constructor in code, "old_core_constructor not found"
code = code.replace(old_core_constructor, new_core_constructor, 1)

# Replace Receiver support in Core to include expectedPetDeposit check (Item 7)
old_receiver_hook = '''    function onERC721Received(address, address, uint256, bytes calldata) external pure override returns (bytes4) {
        return this.onERC721Received.selector;
    }'''

new_receiver_hook = '''    mapping(uint256 => address) public expectedPetDeposit;

    function onERC721Received(address, address from, uint256 petId, bytes calldata) external override returns (bytes4) {
        if (msg.sender == address(companionContract)) {
            require(expectedPetDeposit[petId] == from, "Unsolicited companion deposit");
        } else {
            revert("Direct ERC721 deposits not supported");
        }
        return this.onERC721Received.selector;
    }'''

assert old_receiver_hook in code, "old_receiver_hook not found"
code = code.replace(old_receiver_hook, new_receiver_hook, 1)

# In Core: Add activitySustainedUntil, update canList() removing pendingHeistRewardCount
old_core_state = '''    mapping(uint256 => uint32) public pendingGameplayCount;
    mapping(uint256 => uint32) public pendingEventEntitlementCount;
    mapping(uint256 => uint32) public pendingHeistRewardCount;
    mapping(uint256 => uint32) public activeSolsticeCommitmentCount;
    mapping(uint256 => bool) public hasPendingNormalHeist;
    mapping(uint256 => bool) public isHeroFatigued;
    mapping(uint256 => bool) public bazaarEscrowed;
    mapping(uint256 => uint256) public goldCarry; // Token-bound fractional gold accumulator (base 100_000_000)'''

new_core_state = '''    mapping(uint256 => uint32) public pendingGameplayCount;
    mapping(uint256 => uint32) public pendingEventEntitlementCount;
    mapping(uint256 => uint32) public activeSolsticeCommitmentCount;
    mapping(uint256 => bool) public hasPendingNormalHeist;
    mapping(uint256 => bool) public isHeroFatigued;
    mapping(uint256 => bool) public bazaarEscrowed;
    mapping(uint256 => uint256) public goldCarry; // Token-bound fractional gold accumulator (base 100_000_000)
    mapping(uint256 => uint64) public activitySustainedUntil; // Token-bound 7-day active gameplay sustenance

    function refreshActivitySustained(uint256 hoodId) external onlyActiveEngine {
        activitySustainedUntil[hoodId] = uint64(block.timestamp + 7 days);
        emit ActivitySustainedRefreshed(hoodId, activitySustainedUntil[hoodId]);
    }'''

assert old_core_state in code, "old_core_state not found"
code = code.replace(old_core_state, new_core_state, 1)

# Remove pendingHeistReward increments/decrements in Core
old_heist_rewards_core = '''    function incrementPendingHeistReward(uint256 hoodId) external onlyResolverEngine {
        pendingHeistRewardCount[hoodId]++;
    }
    function decrementPendingHeistReward(uint256 hoodId) external onlySettlementEngine {
        require(pendingHeistRewardCount[hoodId] > 0, "Heist reward underflow");
        pendingHeistRewardCount[hoodId]--;
    }'''

assert old_heist_rewards_core in code, "old_heist_rewards_core not found"
code = code.replace(old_heist_rewards_core + "\n\n", "")

# Update canList in Core
old_canlist = '''    function canList(uint256 hoodId) public view returns (bool allowed, uint256 reasonFlags) {
        if (pendingGameplayCount[hoodId] > 0) reasonFlags |= 1;
        if (pendingUnequipCount[hoodId] > 0) reasonFlags |= 2;
        if (pendingDebondMaturesAt[hoodId] > 0) reasonFlags |= 4;
        if (activeSolsticeCommitmentCount[hoodId] > 0) reasonFlags |= 8;
        if (pendingEventEntitlementCount[hoodId] > 0) reasonFlags |= 16;
        if (pendingHeistRewardCount[hoodId] > 0) reasonFlags |= 32;
        if (bazaarEscrowed[hoodId]) reasonFlags |= 64;
        allowed = (reasonFlags == 0);
    }'''

new_canlist = '''    function canList(uint256 hoodId) public view returns (bool allowed, uint256 reasonFlags) {
        if (pendingGameplayCount[hoodId] > 0) reasonFlags |= 1;
        if (pendingUnequipCount[hoodId] > 0) reasonFlags |= 2;
        if (pendingDebondMaturesAt[hoodId] > 0) reasonFlags |= 4;
        if (activeSolsticeCommitmentCount[hoodId] > 0) reasonFlags |= 8;
        if (pendingEventEntitlementCount[hoodId] > 0) reasonFlags |= 16;
        if (bazaarEscrowed[hoodId]) reasonFlags |= 32;
        allowed = (reasonFlags == 0);
    }'''

assert old_canlist in code, "old_canlist not found"
code = code.replace(old_canlist, new_canlist, 1)

# Remove extra setEngineRoles in Core (Item 9)
old_extra_set_engine = '''    address public timelock;
    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
        _;
    }

    function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyTimelock {
        activeEngine[engine] = active;
        resolverEngine[engine] = resolver;
        settlementEngine[engine] = settlement;
        emit EngineRolesChanged(engine, active, resolver, settlement);
    }'''

assert old_extra_set_engine in code, "old_extra_set_engine not found"
code = code.replace(old_extra_set_engine, '''    function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyTimelock {
        activeEngine[engine] = active;
        resolverEngine[engine] = resolver;
        settlementEngine[engine] = settlement;
        emit EngineRolesChanged(engine, active, resolver, settlement);
    }''', 1)

# ==============================================================================
# 5. Section 2: HoodQuestWorldState Timelock & eventParticipantCount
# ==============================================================================
old_ws_events = '''        // Event Configurations & Finalization Lock
        mapping(uint256 => EventConfig) public events;
        mapping(uint256 => bool) public eventFinalized;'''

new_ws_events = '''        // Event Configurations & Finalization Lock
        mapping(uint256 => EventConfig) public events;
        mapping(uint256 => bool) public eventFinalized;
        mapping(uint256 => uint32) public eventParticipantCount; // Distinct positive contributors for liability closing'''

assert old_ws_events in code, "old_ws_events not found"
code = code.replace(old_ws_events, new_ws_events, 1)

old_ws_add_contrib = '''            firstPositive = (hoodContribution[eventId][hoodId] == 0 && points > 0);
            hoodContribution[eventId][hoodId] += points;
            totalContribution[eventId] += points;
            newCumulative = hoodContribution[eventId][hoodId];'''

new_ws_add_contrib = '''            firstPositive = (hoodContribution[eventId][hoodId] == 0 && points > 0);
            if (firstPositive) {
                eventParticipantCount[eventId]++;
            }
            hoodContribution[eventId][hoodId] += points;
            totalContribution[eventId] += points;
            newCumulative = hoodContribution[eventId][hoodId];'''

assert old_ws_add_contrib in code, "old_ws_add_contrib not found"
code = code.replace(old_ws_add_contrib, new_ws_add_contrib, 1)

# ==============================================================================
# 6. Section 2: HoodQuestTreasures Constructor Wiring, Modifiers, settleHeistRewardBundle
# ==============================================================================
old_treas_top = '''- **`HoodQuestTreasures.sol` (ERC-1155Supply Accounting Authority):**
  - Inherits OpenZeppelin `ERC1155Supply` for authoritative tracking of `totalSupply(id)`.
  - **Explicit Three-Tier Engine Permissions (HQ-TREAS-004):**
    ```solidity
    mapping(address => bool) public activeRaidEngine;    // May request heists, consume stamina, create events
    mapping(address => bool) public resolverApproved;     // May resolve existing requests & reserve drops/trophies
    mapping(address => bool) public settlementApproved;   // May settle existing reward claims & event liabilities

    address public timelock;
    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
        _;
    }

    function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyTimelock {
        activeRaidEngine[engine] = active;
        resolverApproved[engine] = resolver;
        settlementApproved[engine] = settlement;
        emit EngineRolesChanged(engine, active, resolver, settlement);
    }
    ```'''

new_treas_top = '''- **`HoodQuestTreasures.sol` (ERC-1155Supply Accounting Authority):**
  - Inherits OpenZeppelin `ERC1155Supply` for authoritative tracking of `totalSupply(id)`.
  - **Explicit Three-Tier Engine Permissions & Deployment Wiring (HQ-TREAS-004):**
    ```solidity
    address public immutable timelock;
    IHoodQuest public immutable hoodContract;
    IHoodQuestCompanions public companionContract;
    address public bazaarContract;

    mapping(address => bool) public activeRaidEngine;    // May request heists, consume stamina, create events
    mapping(address => bool) public resolverApproved;     // May resolve existing requests & reserve drops/trophies
    mapping(address => bool) public settlementApproved;   // May settle existing reward claims & event liabilities

    constructor(address timelock_, address hoodContract_) {
        require(timelock_ != address(0), "Invalid timelock");
        require(hoodContract_ != address(0), "Invalid hood contract");
        timelock = timelock_;
        hoodContract = IHoodQuest(hoodContract_);
    }

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
    ```'''

assert old_treas_top in code, "old_treas_top not found"
code = code.replace(old_treas_top, new_treas_top, 1)

# Standardize reserveItem modifier in Treasury (Item 5)
old_reserve_item = 'function reserveItem(\n        uint256 itemId,\n        MintSource source,\n        uint256 requestedAmount\n    ) external onlyResolver returns (uint256 reservedAmount) {'
new_reserve_item = 'function reserveItem(\n        uint256 itemId,\n        MintSource source,\n        uint256 requestedAmount\n    ) external onlyResolverApproved returns (uint256 reservedAmount) {'
assert old_reserve_item in code, "old_reserve_item not found"
code = code.replace(old_reserve_item, new_reserve_item, 1)

# Add settleHeistRewardBundle in Treasury (Item 2)
old_mint_expansion = '''    function mintExpansionItem(address to, uint256 itemId, uint256 amount) external nonReentrant {
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
    }'''

new_mint_expansion = '''    function mintExpansionItem(address to, uint256 itemId, uint256 amount) external nonReentrant {
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

    function settleHeistRewardBundle(address recipient, RewardBundle calldata bundle) external onlyResolverApproved nonReentrant {
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
    }'''

assert old_mint_expansion in code, "old_mint_expansion not found"
code = code.replace(old_mint_expansion, new_mint_expansion, 1)

# ==============================================================================
# 7. Section 3: Heist Engine Direct Settlement & Activity Sustenance
# ==============================================================================
old_heist_flow_diagram = '''```mermaid
flowchart LR
    A["00:00 UTC Reset<br>5 Base Heists (Core-Bound)"] --> B["Carriage Ambush<br>(Snapshot + Delayed L2 Entropy)"]
    B -->|"Base Roll: 1-3 Gold"| C["🪙 Royal Gold Sovereigns<br>(Fixed-point carry accumulator)"]
    B -->|"25% Quest Drop"| D1["🪵 Sherwood Yew (Soulbound)"]
    B -->|"20% Quest Drop"| D2["⚔️ Nottingham Iron (Soulbound)"]
    B -->|"Calibrated Drops"| D3["Baskets (0.5%), Elixirs (0.8%), Bow (0.0000125%)"]
    
    C & D1 & D2 -->|"Camp Blacksmith"| E["Forge Finished Weapons & Gear<br>(750 Gilded Bows / 250 Drop Slots)"]
    C -->|"Pantry Sink: 14 Gold"| F["Feast Basket Rations<br>(+7 Days Sustenance; Max 56d)"]
    C -->|"Rescue Post: 20-40 Gold"| G["Mother Meg Pet Adoption<br>(Hound, Falcon, Owl)"]
    
    E & F & G -->|"100% Gold Burned"| K["OpenZeppelin _burn()<br>25% to Rebate Reserve • 75% Permanent Deflation"]
```'''

new_heist_flow_diagram = '''```mermaid
flowchart LR
    A["00:00 UTC Reset<br>5 Base Heists (Core-Bound)"] --> B["Carriage Ambush<br>(Snapshot + Delayed L2 Entropy)"]
    B -->|"Permissionless Resolution"| R["Atomic Settlement to Recipient<br>(Zero Unclaimed Reward Storage)"]
    R -->|"Base Roll: 1-3 Gold"| C["🪙 Royal Gold Sovereigns<br>(Token-Bound Carry Accumulator)"]
    R -->|"25% Quest Drop"| D1["🪵 Sherwood Yew (Soulbound)"]
    R -->|"20% Quest Drop"| D2["⚔️ Nottingham Iron (Soulbound)"]
    R -->|"Calibrated Drops"| D3["Baskets (0.5%), Elixirs (0.8%), Bow (0.0000125%)"]
    
    B -->|"Active Adventuring"| S["activitySustainedUntil = now + 7 days<br>(Sustains Hero without Food)"]
    
    C & D1 & D2 -->|"Camp Blacksmith"| E["Forge Finished Weapons & Gear<br>(750 Gilded Bows / 250 Drop Slots)"]
    C -->|"Pantry Sink: 14 Gold"| F["Feast Basket Rations<br>(Passive Inactivity Protection)"]
    C -->|"Rescue Post: 20-40 Gold"| G["Mother Meg Pet Adoption<br>(Hound, Falcon, Owl)"]
    
    E & F & G -->|"100% Gold Burned"| K["OpenZeppelin _burn()<br>25% to Rebate Reserve • 75% Permanent Deflation"]
```'''

assert old_heist_flow_diagram in code, "old_heist_flow_diagram not found"
code = code.replace(old_heist_flow_diagram, new_heist_flow_diagram, 1)

# Update HeistRequest to include rewardRecipient, remove unclaimedHeistRewards mapping
old_heist_req_struct = '''struct HeistRequest {
    uint256 hoodId;
    uint256 targetBlock;
    uint8 count;          // 1 to 5
    uint8 baseCount;      // Rolls i < baseCount are BASE rolls
    uint8 bonusCount;     // Rolls i >= baseCount are BONUS rolls
    uint32 monthEpochAtRequest;
    bytes32 heroSeed;
    HeistSnapshot snapshot;
}

mapping(uint256 => RewardBundle) public unclaimedHeistRewards;
mapping(uint256 => HeistRequest) public heistRequests;'''

new_heist_req_struct = '''struct HeistRequest {
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

mapping(uint256 => HeistRequest) public heistRequests;'''

assert old_heist_req_struct in code, "old_heist_req_struct not found"
code = code.replace(old_heist_req_struct, new_heist_req_struct, 1)

# Update requestHeistBatch to accept rewardRecipient and refresh activitySustainedUntil
old_req_heist_func = '''function requestHeistBatch(uint256 hoodId, uint8 count) external returns (uint256 requestId) {
    require(hoodContract.activeEngine(address(this)), "Engine not active");
    require(count >= 1 && count <= 5, "Count must be 1..5");
    require(msg.sender == hoodContract.ownerOf(hoodId) || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
    require(!hoodContract.economicActionsPaused(), "Economic actions paused");
    require(!hoodContract.bazaarEscrowed(hoodId), "Hero is listed in Bazaar");
    require(!hoodContract.hasPendingNormalHeist(hoodId), "Pending heist batch already exists");
    
    bytes32 seed = hoodContract.heroSeed(hoodId);
    require(seed != bytes32(0), "Hero seed not finalized");
    
    (uint8 baseConsumed, uint8 bonusConsumed) = hoodContract.consumeStaminaBatch(hoodId, count);
    
    HeistSnapshot memory snap = hoodContract.captureHeistSnapshot(hoodId);
    
    requestId = ++nonce;
    uint256 target = ArbSys(address(0x64)).arbBlockNumber() + 2;
    
    heistRequests[requestId] = HeistRequest({
        hoodId: hoodId,
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
    emit HeistBatchRequested(requestId, hoodId, count, target);
}'''

new_req_heist_func = '''function requestHeistBatch(uint256 hoodId, uint8 count, address rewardRecipient) external returns (uint256 requestId) {
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
    
    // Active gameplay sustains hero upkeep for 7 days (Item 1)
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
}'''

assert old_req_heist_func in code, "old_req_heist_func not found"
code = code.replace(old_req_heist_func, new_req_heist_func, 1)

# Update resolveHeist to atomically settle rewards directly to recipient and eliminate unclaimedHeistRewards
old_resolve_end = '''    hoodContract.setFatigue(req.hoodId, fatigueActive);
    _accrueRewardBundle(req.hoodId, bundle);
    
    // Engine obligation decremented AFTER reservations in _accrueRewardBundle to preserve reservation authority
    pendingRequestsByEngine[address(this)]--;
}'''

new_resolve_end = '''    hoodContract.setFatigue(req.hoodId, fatigueActive);
    
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

    // 2. Atomic settlement directly to snapshotted recipient (Zero Unclaimed Storage - Item 2)
    treasuresContract.settleHeistRewardBundle(req.rewardRecipient, bundle);
    
    pendingRequestsByEngine[address(this)]--;
}'''

assert old_resolve_end in code, "old_resolve_end not found"
code = code.replace(old_resolve_end, new_resolve_end, 1)

# Remove _accrueRewardBundle and claimHeistRewards functions
old_claim_heist_rewards_block = '''function _accrueRewardBundle(uint256 hoodId, RewardBundle memory bundle) internal {
    RewardBundle storage existing = unclaimedHeistRewards[hoodId];
    bool previouslyZero = (
        existing.gold == 0 && existing.yew == 0 && existing.iron == 0 &&
        existing.baskets == 0 && existing.elixirs == 0 &&
        existing.gildedBows == 0 && existing.yewLongbows == 0 &&
        existing.quarterstaffs == 0 && existing.poacherDaggers == 0
    );
    
    if (bundle.elixirs > 0) {
        uint256 res = treasuresContract.reserveItem(GREENWOOD_ELIXIR, MintSource.DROP, bundle.elixirs);
        existing.elixirs += res;
    }
    if (bundle.gildedBows > 0) {
        uint256 res = treasuresContract.reserveItem(GILDED_BOW, MintSource.DROP, bundle.gildedBows);
        existing.gildedBows += res;
    }
    if (bundle.yewLongbows > 0) {
        uint256 res = treasuresContract.reserveItem(YEW_LONGBOW, MintSource.DROP, bundle.yewLongbows);
        existing.yewLongbows += res;
    }
    if (bundle.quarterstaffs > 0) {
        uint256 res = treasuresContract.reserveItem(QUARTERSTAFF, MintSource.DROP, bundle.quarterstaffs);
        existing.quarterstaffs += res;
    }
    if (bundle.poacherDaggers > 0) {
        uint256 res = treasuresContract.reserveItem(POACHER_DAGGERS, MintSource.DROP, bundle.poacherDaggers);
        existing.poacherDaggers += res;
    }
    
    existing.gold += bundle.gold;
    existing.yew += bundle.yew;
    existing.iron += bundle.iron;
    existing.baskets += bundle.baskets;
    
    if (previouslyZero) {
        hoodContract.incrementPendingHeistReward(hoodId);
        outstandingRewardClaimsByEngine[address(this)]++;
    }
}

function claimHeistRewards(uint256 hoodId, address recipient) external nonReentrant {
    require(recipient != address(0), "Invalid recipient");
    address owner = hoodContract.ownerOf(hoodId);
    if (msg.sender != owner) {
        require(hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(recipient == owner, "Delegates can only claim to Hood owner");
    }
    
    RewardBundle memory rewards = unclaimedHeistRewards[hoodId];
    require(
        rewards.gold > 0 || rewards.yew > 0 || rewards.iron > 0 ||
        rewards.baskets > 0 || rewards.elixirs > 0 ||
        rewards.gildedBows > 0 || rewards.yewLongbows > 0 ||
        rewards.quarterstaffs > 0 || rewards.poacherDaggers > 0,
        "No rewards to claim"
    );
    
    delete unclaimedHeistRewards[hoodId];
    hoodContract.decrementPendingHeistReward(hoodId);
    outstandingRewardClaimsByEngine[address(this)]--;
    
    treasuresContract.settleHeistRewardBundle(recipient, rewards);
    emit HeistRewardsClaimed(hoodId, recipient, rewards);
}'''

assert old_claim_heist_rewards_block in code, "old_claim_heist_rewards_block not found"
code = code.replace(old_claim_heist_rewards_block, "// Atomic settlement occurs directly during resolveHeist() via treasuresContract.settleHeistRewardBundle.", 1)

# ==============================================================================
# 8. Section 4: Golden Arrow Delayed-Unequip Exploit Closure (Item 8) & expectedPetDeposit (Item 7)
# ==============================================================================
old_armory_unequip = '''function initiateUnequip(uint256 hoodId, uint8 slot) external {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId), "Owner only");
    require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
    require(slot <= 4, "Invalid slot");
    require(equippedSlot[hoodId][slot] != 0, "Slot is empty");
    require(unequipMaturesAt[hoodId][slot] == 0, "Unequip already pending");
    
    if (slot == 4) {
        require(block.timestamp >= cornucopiaBoundAt[hoodId] + 7 days, "7-day Cornucopia lock active");
    }
    
    unequipMaturesAt[hoodId][slot] = uint64(block.timestamp + 24 hours);
    pendingUnequipCount[hoodId]++;
    emit UnequipInitiated(hoodId, slot, unequipMaturesAt[hoodId][slot]);
}

function finalizeUnequip(uint256 hoodId, uint8 slot) external nonReentrant {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId), "Owner only");
    require(unequipMaturesAt[hoodId][slot] > 0, "Unequip not initiated");
    require(block.timestamp >= unequipMaturesAt[hoodId][slot], "24-hour maturation period not reached");
    
    uint32 itemId = equippedSlot[hoodId][slot];
    equippedSlot[hoodId][slot] = 0;
    unequipMaturesAt[hoodId][slot] = 0;
    pendingUnequipCount[hoodId]--;
    
    boundCount[itemId]--;
    treasuresContract.safeTransferFrom(address(this), msg.sender, itemId, 1, "");
    _updateLoadoutHash(hoodId);
    emit ItemUnequipped(hoodId, slot, itemId);
}'''

new_armory_unequip = '''function initiateUnequip(uint256 hoodId, uint8 slot) external {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId), "Owner only");
    require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");
    require(slot <= 4, "Invalid slot");
    require(equippedSlot[hoodId][slot] != 0, "Slot is empty");
    require(unequipMaturesAt[hoodId][slot] == 0, "Unequip already pending");
    
    // Golden Arrow Dependency Protection: Cannot initiate Bow removal while Arrow is equipped
    if (slot == 0) {
        require(equippedSlot[hoodId][2] != GOLDEN_ARROW, "Cannot unequip Bow while Golden Arrow equipped");
    }
    if (slot == 4) {
        require(block.timestamp >= cornucopiaBoundAt[hoodId] + 7 days, "7-day Cornucopia lock active");
    }
    
    unequipMaturesAt[hoodId][slot] = uint64(block.timestamp + 24 hours);
    pendingUnequipCount[hoodId]++;
    emit UnequipInitiated(hoodId, slot, unequipMaturesAt[hoodId][slot]);
}

function finalizeUnequip(uint256 hoodId, uint8 slot) external nonReentrant {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId), "Owner only");
    require(unequipMaturesAt[hoodId][slot] > 0, "Unequip not initiated");
    require(block.timestamp >= unequipMaturesAt[hoodId][slot], "24-hour maturation period not reached");
    
    // Re-check Golden Arrow dependency at maturation
    if (slot == 0) {
        require(equippedSlot[hoodId][2] != GOLDEN_ARROW, "Cannot finalize Bow removal while Golden Arrow equipped");
    }

    uint32 itemId = equippedSlot[hoodId][slot];
    equippedSlot[hoodId][slot] = 0;
    unequipMaturesAt[hoodId][slot] = 0;
    pendingUnequipCount[hoodId]--;
    
    boundCount[itemId]--;
    treasuresContract.safeTransferFrom(address(this), msg.sender, itemId, 1, "");
    _updateLoadoutHash(hoodId);
    emit ItemUnequipped(hoodId, slot, itemId);
}'''

assert old_armory_unequip in code, "old_armory_unequip not found"
code = code.replace(old_armory_unequip, new_armory_unequip, 1)

# Check equipItem for Golden Arrow: require Bow equipped AND no pending unequip on Bow
old_equip_arrow = '''    if (itemId == GOLDEN_ARROW) {
        require(equippedSlot[hoodId][0] == GILDED_BOW || equippedSlot[hoodId][0] == YEW_LONGBOW, "Arrow requires equipped bow");
    }'''

new_equip_arrow = '''    if (itemId == GOLDEN_ARROW) {
        require(equippedSlot[hoodId][0] == GILDED_BOW || equippedSlot[hoodId][0] == YEW_LONGBOW, "Arrow requires equipped bow");
        require(unequipMaturesAt[hoodId][0] == 0, "Cannot equip Arrow while Bow unequip pending");
    }'''

assert old_equip_arrow in code, "old_equip_arrow not found"
code = code.replace(old_equip_arrow, new_equip_arrow, 1)

# In initiatePetBond: record expectedPetDeposit
old_pet_bond = '''function initiatePetBond(uint256 hoodId, uint256 petId) external nonReentrant {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId), "Not Hood owner");
    require(companionContract.ownerOf(petId) == msg.sender, "Not pet owner");
    require(hoodBoundPet[hoodId] == 0, "Hood already has bonded pet");
    require(petBoundToHood[petId] == 0, "Pet already bonded");
    
    companionContract.transferFrom(msg.sender, address(this), petId);'''

new_pet_bond = '''function initiatePetBond(uint256 hoodId, uint256 petId) external nonReentrant {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId), "Not Hood owner");
    require(companionContract.ownerOf(petId) == msg.sender, "Not pet owner");
    require(hoodBoundPet[hoodId] == 0, "Hood already has bonded pet");
    require(petBoundToHood[petId] == 0, "Pet already bonded");
    
    expectedPetDeposit[petId] = msg.sender;
    companionContract.transferFrom(msg.sender, address(this), petId);
    delete expectedPetDeposit[petId];'''

assert old_pet_bond in code, "old_pet_bond not found"
code = code.replace(old_pet_bond, new_pet_bond, 1)

# ==============================================================================
# 9. Section 7: Upkeep & Devotion (Item 1: Active gameplay substitutes for food)
# ==============================================================================
old_sec7_slumber = '''function protectedUntil(uint256 id) public view returns (uint64) {
    uint64 careProtect = lastCareTimestamp[id] + 3 days;

    if (equippedSlot[id][4] == FRIARS_CORNUCOPIA) {
        // Cornucopia prevents starvation but does NOT replace care.
        return careProtect;
    }

    uint64 rationProtect = rationsUntil[id];
    return careProtect > rationProtect ? careProtect : rationProtect;
}'''

new_sec7_slumber = '''function protectedUntil(uint256 id) public view returns (uint64) {
    uint64 careProtect = lastCareTimestamp[id] + 3 days;

    if (equippedSlot[id][4] == FRIARS_CORNUCOPIA) {
        // Cornucopia prevents starvation but does NOT replace care. Active adventuring provides wake protection:
        uint64 actProtect = activitySustainedUntil[id];
        return careProtect > actProtect ? careProtect : actProtect;
    }

    uint64 actProtect = activitySustainedUntil[id];
    uint64 rationProtect = rationsUntil[id];
    uint64 maxSustain = actProtect > rationProtect ? actProtect : rationProtect;
    return careProtect > maxSustain ? careProtect : maxSustain;
}'''

assert old_sec7_slumber in code, "old_sec7_slumber not found"
code = code.replace(old_sec7_slumber, new_sec7_slumber, 1)

old_sec7_reward_bps = '''function effectiveEconomicRewardBps(uint256 hoodId) public view returns (uint256) {
    bool hasCornucopia = (equippedSlot[hoodId][4] == FRIARS_CORNUCOPIA);
    bool isFed = hasCornucopia || (block.timestamp <= rationsUntil[hoodId]);
    
    // Starvation penalty clamp: 50% yield (5,000 bps) vs Fed (10,000 bps)
    // Devotion bonus applies strictly to goldBonusBps, never universal loot chances
    return isFed ? 10000 : 5000;
}'''

new_sec7_reward_bps = '''function effectiveEconomicRewardBps(uint256 hoodId) public view returns (uint256) {
    bool hasCornucopia = (equippedSlot[hoodId][4] == FRIARS_CORNUCOPIA);
    bool activityFed = (block.timestamp <= activitySustainedUntil[hoodId]);
    bool rationFed = (block.timestamp <= rationsUntil[hoodId]);
    
    // Active adventuring substitutes for food upkeep (Item 1).
    // Starvation penalty clamp: 50% yield (5,000 bps) vs Fed (10,000 bps)
    return (hasCornucopia || activityFed || rationFed) ? 10000 : 5000;
}'''

assert old_sec7_reward_bps in code, "old_sec7_reward_bps not found"
code = code.replace(old_sec7_reward_bps, new_sec7_reward_bps, 1)

# ==============================================================================
# 10. Section 9: World Events, Event Liabilities (Item 9), and V1 -> V2 Migration Protocol (Item 10)
# ==============================================================================
# In requestActionEvent: refresh activitySustainedUntil
old_action_req_body = '''    require(block.timestamp >= cfg.startTime && block.timestamp <= cfg.endTime - 1 hours, "Action cutoff reached");
    
    _consumeEventAttempt(hoodId, eventId, kind);'''

new_action_req_body = '''    require(block.timestamp >= cfg.startTime && block.timestamp <= cfg.endTime - 1 hours, "Action cutoff reached");
    
    _consumeEventAttempt(hoodId, eventId, kind);
    
    // Active adventuring sustains hero upkeep for 7 days (Item 1)
    hoodContract.refreshActivitySustained(hoodId);'''

assert old_action_req_body in code, "old_action_req_body not found"
code = code.replace(old_action_req_body, new_action_req_body, 1)

# In commitSolsticeManeuver: refresh activitySustainedUntil
old_solstice_commit_body = '''    require(maneuverIndex < 5, "All 5 maneuvers completed");
    
    target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);'''

new_solstice_commit_body = '''    require(maneuverIndex < 5, "All 5 maneuvers completed");
    
    // Active adventuring sustains hero upkeep for 7 days (Item 1)
    hoodContract.refreshActivitySustained(hoodId);
    
    target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);'''

assert old_solstice_commit_body in code, "old_solstice_commit_body not found"
code = code.replace(old_solstice_commit_body, new_solstice_commit_body, 1)

# Event Liability Closure with eventParticipantsOutstanding (Item 9)
old_event_records = '''mapping(uint256 => EventRecord) public eventRecords;
mapping(uint256 => mapping(uint256 => bool)) public eventClaimed;
mapping(uint256 => mapping(uint256 => mapping(uint256 => bool))) public eventTrophyEntitlement;
mapping(uint256 => uint256) public eventTrophiesOutstanding;
mapping(uint256 => bool) public eventGoldSettled;
mapping(uint256 => bool) public eventLiabilityOpen;'''

new_event_records = '''mapping(uint256 => EventRecord) public eventRecords;
mapping(uint256 => mapping(uint256 => bool)) public eventClaimed;
mapping(uint256 => mapping(uint256 => mapping(uint256 => bool))) public eventTrophyEntitlement;
mapping(uint256 => uint256) public eventTrophiesOutstanding;
mapping(uint256 => uint32) public eventParticipantsOutstanding; // Outstanding participant entitlements
mapping(uint256 => bool) public eventGoldSettled;
mapping(uint256 => bool) public eventLiabilityOpen;'''

assert old_event_records in code, "old_event_records not found"
code = code.replace(old_event_records, new_event_records, 1)

# In finalizeEvent: set eventParticipantsOutstanding
old_fin_budget = '''        e.finalBudget = treasuresContract.reserveEventBudget(eventId, cfg.cap);
        eventLiabilityOpen[eventId] = true;
        outstandingEventLiabilitiesByEngine[address(this)]++;
        _reserveEventTrophies(eventId, cfg);
    }
    
    e.finalized = true;'''

new_fin_budget = '''        e.finalBudget = treasuresContract.reserveEventBudget(eventId, cfg.cap);
        eventLiabilityOpen[eventId] = true;
        outstandingEventLiabilitiesByEngine[address(this)]++;
        eventParticipantsOutstanding[eventId] = worldStateContract.eventParticipantCount(eventId);
        _reserveEventTrophies(eventId, cfg);
    }
    
    e.finalized = true;'''

assert old_fin_budget in code, "old_fin_budget not found"
code = code.replace(old_fin_budget, new_fin_budget, 1)

# In claimEventReward: decrement eventParticipantsOutstanding
old_claim_reward = '''    eventClaimed[eventId][hoodId] = true;
    hoodContract.decrementPendingEventEntitlement(hoodId);'''

new_claim_reward = '''    eventClaimed[eventId][hoodId] = true;
    hoodContract.decrementPendingEventEntitlement(hoodId);
    eventParticipantsOutstanding[eventId]--;'''

assert old_claim_reward in code, "old_claim_reward not found"
code = code.replace(old_claim_reward, new_claim_reward, 1)

# In expireHoodEventParticipation: decrement eventParticipantsOutstanding
old_expire_claim = '''    eventClaimed[eventId][hoodId] = true;
    hoodContract.decrementPendingEventEntitlement(hoodId);
    emit HoodEventParticipationExpired(eventId, hoodId);'''

new_expire_claim = '''    eventClaimed[eventId][hoodId] = true;
    hoodContract.decrementPendingEventEntitlement(hoodId);
    eventParticipantsOutstanding[eventId]--;
    _tryCloseEventLiability(eventId);
    emit HoodEventParticipationExpired(eventId, hoodId);'''

assert old_expire_claim in code, "old_expire_claim not found"
code = code.replace(old_expire_claim, new_expire_claim, 1)

# In _tryCloseEventLiability: include eventParticipantsOutstanding == 0
old_try_close = '''function _tryCloseEventLiability(uint256 eventId) internal {
    if (eventGoldSettled[eventId] && eventTrophiesOutstanding[eventId] == 0 && eventLiabilityOpen[eventId]) {
        eventLiabilityOpen[eventId] = false;
        outstandingEventLiabilitiesByEngine[address(this)]--;
        emit EventLiabilityClosed(eventId);
    }
}'''

new_try_close = '''function _tryCloseEventLiability(uint256 eventId) internal {
    if (eventGoldSettled[eventId] && 
        eventTrophiesOutstanding[eventId] == 0 && 
        eventParticipantsOutstanding[eventId] == 0 && 
        eventLiabilityOpen[eventId]) {
        eventLiabilityOpen[eventId] = false;
        outstandingEventLiabilitiesByEngine[address(this)]--;
        emit EventLiabilityClosed(eventId);
    }
}'''

assert old_try_close in code, "old_try_close not found"
code = code.replace(old_try_close, new_try_close, 1)

# ==============================================================================
# 11. Section 12 & 13: Invariants & Normative Registry updates
# ==============================================================================
old_inv5 = '''### INV-5: Starvation Economic Multiplier Clamp
- When `rationsUntil[tokenId] < block.timestamp` and not equipped with Cornucopia, `effectiveEconomicRewardBps(tokenId) == 5000` (50% yield clamp).'''

new_inv5 = '''### INV-5: Sustenance & Starvation Economic Clamp
- Active adventuring (`activitySustainedUntil[tokenId] >= block.timestamp`), passive rations (`rationsUntil[tokenId] >= block.timestamp`), or equipped Cornucopia grant full 100% economic yield (`10,000` bps).
- When neither actively adventuring, equipped with Cornucopia, nor passively rationed, `effectiveEconomicRewardBps(tokenId) == 5000` (50% yield clamp).'''

assert old_inv5 in code, "old_inv5 not found"
code = code.replace(old_inv5, new_inv5, 1)

old_inv8 = '''### INV-8: Armory Vault Custody Integrity
- For all equippable items `itemId`, `treasuresContract.balanceOf(HoodQuestVault, itemId) == boundCount[itemId]`.'''

new_inv8 = '''### INV-8: Armory Vault Custody Integrity & Arrow Dependency
- For all equippable items `itemId`, `treasuresContract.balanceOf(HoodQuestVault, itemId) == boundCount[itemId]`.
- Golden Arrow equipped strictly implies a valid Bow equipped and zero pending unequip on the Bow slot (`Golden Arrow equipped => valid Bow equipped => no pending Bow removal`).'''

assert old_inv8 in code, "old_inv8 not found"
code = code.replace(old_inv8, new_inv8, 1)

old_inv13_14 = '''### INV-13: Delegate Asset Non-Redirection & Inventory Spending
- `claimHeistRewards` called by a delegate transfers rewards strictly to `ownerOf(hoodId)`.
- Delegates calling `feed` or `useElixir` burn items strictly from their own inventory.

### INV-14: Scarce-Reward Reservation Solvency
- `treasuresContract.reservedUnclaimed(itemId) >= sum(unclaimedHeistRewards[hoodId].item)`.'''

new_inv13_14 = '''### INV-13: Delegate Asset Non-Redirection & Recipient Safety
- In `requestHeistBatch`, delegates can strictly designate `ownerOf(hoodId)` as `rewardRecipient`.
- Delegates calling `feed` or `useElixir` burn items strictly from their own inventory.

### INV-14: Permissionless Atomic Heist Settlement Solvency
- Normal-heist rewards settle atomically during permissionless `resolveHeist()` directly to `rewardRecipient`.
- Zero unclaimed normal-heist reward state exists; event rewards follow pro-rata pull claims bounded by 90-day deadlines.'''

assert old_inv13_14 in code, "old_inv13_14 not found"
code = code.replace(old_inv13_14, new_inv13_14, 1)

# Write updated generator
with open('/home/arson/rhnftproject/generate_final_blueprint.py', 'w') as f:
    f.write(code)

print("Successfully updated generate_final_blueprint.py with all strict closure items!")
