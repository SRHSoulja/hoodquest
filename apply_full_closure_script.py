import re

with open('/home/arson/rhnftproject/generate_rc3_blueprint.py', 'r') as f:
    content = f.read()

# 1. Update Title and Release in Section 0
content = content.replace(
    '# HoodQuest (HQ): Production System Specification (Protocol Frozen V1.0-RC3)',
    '# HoodQuest (HQ): Production System Specification (Protocol Frozen V1.0)'
)
content = content.replace(
    '- **Specification Release:** **Protocol Frozen V1.0-RC3 (Specification Closure Release)**',
    '- **Specification Release:** **Protocol Frozen V1.0 (Specification Final Closure)**'
)

# 2. Add HoodQuestTypes.sol to Section 2 right under ### Contract Responsibilities:
types_block = r"""### 0. Canonical Shared Types Library (HoodQuestTypes.sol - HQ-SNAP-001):
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
```

"""
content = content.replace(
    '### Contract Responsibilities:\n\n- **`HoodQuest.sol`',
    types_block + '### Contract Responsibilities:\n\n- **`HoodQuest.sol`'
)

# 3. Update HoodQuest.sol engine roles, goldCarry, and lifecycle helpers
old_core_gating = r"""    mapping(uint256 => uint32) public pendingGameplayCount;
    mapping(uint256 => uint32) public pendingEventEntitlementCount;
    mapping(uint256 => uint32) public pendingHeistRewardCount;
    mapping(uint256 => uint32) public activeSolsticeCommitmentCount;
    mapping(uint256 => bool) public bazaarEscrowed;

    function setBazaarEscrowed(uint256 hoodId, bool escrowed) external onlyBazaar {
        bazaarEscrowed[hoodId] = escrowed;
    }

    function incrementPendingGameplay(uint256 hoodId, uint32 count) external onlyAuthorizedEngine {
        pendingGameplayCount[hoodId] += count;
    }
    function decrementPendingGameplay(uint256 hoodId, uint32 count) external onlyAuthorizedEngine {
        require(pendingGameplayCount[hoodId] >= count, "Gameplay counter underflow");
        pendingGameplayCount[hoodId] -= count;
    }

    function incrementPendingEventEntitlement(uint256 hoodId) external onlyAuthorizedEngine {
        pendingEventEntitlementCount[hoodId]++;
    }
    function decrementPendingEventEntitlement(uint256 hoodId) external onlyAuthorizedEngine {
        require(pendingEventEntitlementCount[hoodId] > 0, "Event entitlement underflow");
        pendingEventEntitlementCount[hoodId]--;
    }

    function incrementPendingHeistReward(uint256 hoodId) external onlyAuthorizedEngine {
        pendingHeistRewardCount[hoodId]++;
    }
    function decrementPendingHeistReward(uint256 hoodId) external onlyAuthorizedEngine {
        require(pendingHeistRewardCount[hoodId] > 0, "Heist reward underflow");
        pendingHeistRewardCount[hoodId]--;
    }"""

new_core_gating = r"""    // Three-Tier Engine Lifecycle Permissions (HQ-CORE-004)
    mapping(address => bool) public activeEngine;       // May consume stamina, create requests, increment gameplay
    mapping(address => bool) public resolverEngine;     // May resolve heists/actions, set fatigue, create entitlements
    mapping(address => bool) public settlementEngine;   // May clear entitlements after claim/expiry

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

    mapping(uint256 => uint32) public pendingGameplayCount;
    mapping(uint256 => uint32) public pendingEventEntitlementCount;
    mapping(uint256 => uint32) public pendingHeistRewardCount;
    mapping(uint256 => uint32) public activeSolsticeCommitmentCount;
    mapping(uint256 => bool) public hasPendingNormalHeist;
    mapping(uint256 => bool) public isHeroFatigued;
    mapping(uint256 => bool) public bazaarEscrowed;
    mapping(uint256 => uint256) public goldCarry; // Token-bound fractional gold accumulator (base 100_000_000)

    function setBazaarEscrowed(uint256 hoodId, bool escrowed) external onlyBazaar {
        bazaarEscrowed[hoodId] = escrowed;
    }

    function currentMonthEpoch() public view returns (uint32) {
        if (block.timestamp < GENESIS_TIME) return 0;
        return uint32((block.timestamp - GENESIS_TIME) / 30 days);
    }

    function setPendingNormalHeist(uint256 hoodId, bool pending) external {
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

    function incrementPendingHeistReward(uint256 hoodId) external onlyResolverEngine {
        pendingHeistRewardCount[hoodId]++;
    }
    function decrementPendingHeistReward(uint256 hoodId) external onlySettlementEngine {
        require(pendingHeistRewardCount[hoodId] > 0, "Heist reward underflow");
        pendingHeistRewardCount[hoodId]--;
    }

    function incrementSolsticeCommitment(uint256 hoodId) external onlyActiveEngine {
        activeSolsticeCommitmentCount[hoodId]++;
    }
    function decrementSolsticeCommitment(uint256 hoodId) external onlyResolverEngine {
        require(activeSolsticeCommitmentCount[hoodId] > 0, "Solstice commitment underflow");
        activeSolsticeCommitmentCount[hoodId]--;
    }"""

content = content.replace(old_core_gating, new_core_gating)

# 4. Replace WorldState in Section 2 with complete executable implementation
old_worldstate_block = r"""- **`HoodQuestWorldState.sol` (Persistent Canonical World Registry - HQ-EVT-002):**
  - Canonical interface and storage for persistent world progress across Raid engine replacements:
    ```solidity
    interface IHoodQuestWorldState {
        function recordMonthlyActiveHood(uint256 hoodId, uint32 targetMonthEpoch) external;
        function getMonthlyActiveHoodCount(uint32 mEpoch) external view returns (uint32);
        function createEvent(uint256 eventId, EventConfig calldata cfg) external;
        function getEvent(uint256 eventId) external view returns (EventConfig memory);
        function addContribution(uint256 eventId, uint256 hoodId, uint256 points) external;
        function addCastleBreach(uint256 eventId, uint256 points, uint256 target) external returns (bool breached);
        function updateJubileeTop5(uint256 eventId, uint256 hoodId, uint256 newScore) external;
        function addSolsticeRenown(uint256 eventId, uint256 hoodId, uint256 points) external;
        function getTaxTrainThreshold() external view returns (uint256);
        function setTaxTrainThreshold(uint256 newThreshold) external;
        function getBossCooldown() external view returns (uint64);
        function setBossCooldown(uint64 cooldownEndsAt) external;
        function isTaxTrainActive() external view returns (bool);
        function setTaxTrainActive(bool active, uint256 eventId) external;
    }
    ```
  - **Three-Tier Engine Lifecycle Permissions and Contract Storage Layout (HQ-WORLD-001):**
    ```solidity
    contract HoodQuestWorldState is IHoodQuestWorldState {
        address public owner;
        
        // Three-tier lifecycle engine permissions
        mapping(address => bool) public activeEngine;       // May create events, initiate Tax Trains, mutate active calendar
        mapping(address => bool) public resolverEngine;     // May record contributions/census/breaches for its own events
        mapping(address => bool) public settlementEngine;   // May read records and close liabilities

        // Canonical Persistent Census & World Progress across Raid Engine Upgrades
        mapping(uint32 => mapping(uint256 => bool)) public hasParticipatedInMonth;
        mapping(uint32 => uint32) public monthlyActiveHoods;
        mapping(uint256 => EventConfig) public events;
        mapping(uint256 => mapping(uint256 => uint256)) public hoodContribution;
        mapping(uint256 => uint256) public totalContribution;
        mapping(uint256 => bool) public eventFinalized;
        mapping(uint256 => mapping(uint256 => uint256)) public solsticeRenown;
        
        uint256 public taxTrainThreshold;
        uint64 public bossCooldown;
        bool public taxTrainActive;
        uint256 public activeTaxTrainEventId;

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
    }
    ```"""

new_worldstate_block = r"""- **`HoodQuestWorldState.sol` (Persistent Canonical World Registry - HQ-EVT-002, HQ-WORLD-001):**
  - Canonical interface and storage for persistent world progress across Raid engine replacements:
    ```solidity
    interface IHoodQuestWorldState {
        function recordMonthlyActiveHood(uint256 hoodId, uint32 targetMonthEpoch) external;
        function getMonthlyActiveHoodCount(uint32 mEpoch) external view returns (uint32);
        function createEvent(uint256 eventId, EventConfig calldata cfg) external;
        function getEvent(uint256 eventId) external view returns (EventConfig memory);
        function isEventFinalized(uint256 eventId) external view returns (bool);
        function markEventFinalized(uint256 eventId) external;
        function addContribution(uint256 eventId, uint256 hoodId, uint256 points) external returns (bool firstPositive, uint256 newCumulative);
        function getHoodContribution(uint256 eventId, uint256 hoodId) external view returns (uint256);
        function getTotalContribution(uint256 eventId) external view returns (uint256);
        function addCastleBreach(uint256 eventId, uint256 points, uint256 target) external returns (bool breached);
        function isCastleBreached(uint256 eventId) external view returns (bool);
        function updateJubileeTop5(uint256 eventId, uint256 hoodId, uint256 newCumulativeScore) external;
        function getJubileeTopHood(uint256 eventId, uint256 rankIndex) external view returns (uint256 hoodId, uint256 score);
        function addSolsticeRenown(uint256 eventId, uint256 hoodId, uint256 points) external;
        function getSolsticeLeaderHood(uint256 eventId) external view returns (uint256 leaderHoodId, uint256 leaderRenown);
        function getTaxTrainThreshold() external view returns (uint256);
        function setTaxTrainThreshold(uint256 newThreshold) external;
        function getBossCooldown() external view returns (uint64);
        function setBossCooldown(uint64 cooldownEndsAt) external;
        function isTaxTrainActive() external view returns (bool);
        function setTaxTrainActive(bool active, uint256 eventId) external;
    }

    contract HoodQuestWorldState is IHoodQuestWorldState {
        address public owner;
        
        // Three-tier lifecycle engine permissions
        mapping(address => bool) public activeEngine;       // May create events, initiate Tax Trains, mutate active calendar
        mapping(address => bool) public resolverEngine;     // May record contributions/census/breaches for its own events
        mapping(address => bool) public settlementEngine;   // May read records and close liabilities

        // Event Provenance Architecture (Cross-Upgrade Isolation)
        mapping(uint256 => address) public eventCreator;
        mapping(uint256 => mapping(address => bool)) public eventResolverAllowed;

        // Persistent Census (O(1) storage per Hood across 25+ years)
        mapping(uint256 => uint32) public lastActiveMonthPlusOne;
        mapping(uint32 => uint32) public monthlyActiveHoodCount;

        // Event Configurations & Finalization Lock
        mapping(uint256 => EventConfig) public events;
        mapping(uint256 => bool) public eventFinalized;

        // Canonical Contributions
        mapping(uint256 => mapping(uint256 => uint256)) public hoodContribution;
        mapping(uint256 => uint256) public totalContribution;

        // Castle State
        mapping(uint256 => uint256) public castleProgress;
        mapping(uint256 => bool) public castleBreached;

        // Jubilee State (Top 5 Leaderboard)
        struct JubileeEntry {
            uint256 hoodId;
            uint256 score;
        }
        mapping(uint256 => JubileeEntry[5]) public jubileeTop5;

        // Solstice State
        mapping(uint256 => mapping(uint256 => uint256)) public solsticeRenown;
        mapping(uint256 => uint256) public solsticeLeaderHood;
        mapping(uint256 => uint256) public solsticeLeaderRenown;

        // Tax Train State
        uint256 public taxTrainThreshold;
        uint64 public bossCooldown;
        bool public taxTrainActive;
        uint256 public activeTaxTrainEventId;

        modifier onlyOwner() {
            require(msg.sender == owner, "Not owner");
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
        modifier onlyEventResolver(uint256 eventId) {
            require(resolverEngine[msg.sender] && eventResolverAllowed[eventId][msg.sender], "Not allowed resolver for event");
            _;
        }
        modifier onlySettlementEngine() {
            require(settlementEngine[msg.sender], "Not settlement engine");
            _;
        }

        constructor() {
            owner = msg.sender;
            taxTrainThreshold = 100_000; // Baseline initial burn threshold
        }

        function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyOwner {
            activeEngine[engine] = active;
            resolverEngine[engine] = resolver;
            settlementEngine[engine] = settlement;
        }

        function setEventResolverAllowed(uint256 eventId, address resolver, bool allowed) external onlyOwner {
            eventResolverAllowed[eventId][resolver] = allowed;
        }

        // Census (O(1) storage per Hood)
        function recordMonthlyActiveHood(uint256 hoodId, uint32 targetMonthEpoch) external onlyResolverEngine {
            uint32 stored = lastActiveMonthPlusOne[hoodId];
            if (stored != targetMonthEpoch + 1) {
                lastActiveMonthPlusOne[hoodId] = targetMonthEpoch + 1;
                monthlyActiveHoodCount[targetMonthEpoch] += 1;
            }
        }

        function getMonthlyActiveHoodCount(uint32 mEpoch) external view returns (uint32) {
            return monthlyActiveHoodCount[mEpoch];
        }

        // Event Management & Finalization Lock
        function createEvent(uint256 eventId, EventConfig calldata cfg) external onlyActiveEngine {
            require(!events[eventId].exists, "Event already exists");
            events[eventId] = cfg;
            eventCreator[eventId] = msg.sender;
            eventResolverAllowed[eventId][msg.sender] = true;
        }

        function getEvent(uint256 eventId) external view returns (EventConfig memory) {
            return events[eventId];
        }

        function markEventFinalized(uint256 eventId) external onlyEventResolver(eventId) {
            require(!eventFinalized[eventId], "Event already finalized");
            eventFinalized[eventId] = true;
        }

        function isEventFinalized(uint256 eventId) external view returns (bool) {
            return eventFinalized[eventId];
        }

        // Contributions & Entitlement Tracking
        function addContribution(uint256 eventId, uint256 hoodId, uint256 points)
            external
            onlyEventResolver(eventId)
            returns (bool firstPositive, uint256 newCumulative)
        {
            require(events[eventId].exists, "Event does not exist");
            require(!eventFinalized[eventId], "Event finalized");

            firstPositive = (hoodContribution[eventId][hoodId] == 0 && points > 0);
            hoodContribution[eventId][hoodId] += points;
            totalContribution[eventId] += points;
            newCumulative = hoodContribution[eventId][hoodId];
        }

        function getHoodContribution(uint256 eventId, uint256 hoodId) external view returns (uint256) {
            return hoodContribution[eventId][hoodId];
        }

        function getTotalContribution(uint256 eventId) external view returns (uint256) {
            return totalContribution[eventId];
        }

        // Castle State
        function addCastleBreach(uint256 eventId, uint256 points, uint256 target) external onlyEventResolver(eventId) returns (bool breached) {
            castleProgress[eventId] += points;
            if (castleProgress[eventId] >= target) {
                castleBreached[eventId] = true;
            }
            return castleBreached[eventId];
        }

        function isCastleBreached(uint256 eventId) external view returns (bool) {
            return castleBreached[eventId];
        }

        // Jubilee Leaderboard (Cumulative Score Top 5)
        function updateJubileeTop5(uint256 eventId, uint256 hoodId, uint256 newCumulativeScore) external onlyEventResolver(eventId) {
            JubileeEntry[5] storage top = jubileeTop5[eventId];
            for (uint256 i = 0; i < 5; i++) {
                if (top[i].hoodId == hoodId) {
                    top[i].score = newCumulativeScore;
                    _sortJubileeTop5(top);
                    return;
                }
            }
            if (newCumulativeScore > top[4].score) {
                top[4] = JubileeEntry({hoodId: hoodId, score: newCumulativeScore});
                _sortJubileeTop5(top);
            }
        }

        function _sortJubileeTop5(JubileeEntry[5] storage top) internal {
            for (uint256 i = 0; i < 4; i++) {
                for (uint256 j = 0; j < 4 - i; j++) {
                    if (top[j].score < top[j + 1].score) {
                        JubileeEntry memory temp = top[j];
                        top[j] = top[j + 1];
                        top[j + 1] = temp;
                    }
                }
            }
        }

        function getJubileeTopHood(uint256 eventId, uint256 rankIndex) external view returns (uint256 hoodId, uint256 score) {
            require(rankIndex < 5, "Rank index must be 0..4");
            return (jubileeTop5[eventId][rankIndex].hoodId, jubileeTop5[eventId][rankIndex].score);
        }

        // Solstice Renown & Leaderboard
        function addSolsticeRenown(uint256 eventId, uint256 hoodId, uint256 points) external onlyEventResolver(eventId) {
            solsticeRenown[eventId][hoodId] += points;
            uint256 current = solsticeRenown[eventId][hoodId];
            if (current > solsticeLeaderRenown[eventId]) {
                solsticeLeaderRenown[eventId] = current;
                solsticeLeaderHood[eventId] = hoodId;
            }
        }

        function getSolsticeLeaderHood(uint256 eventId) external view returns (uint256 leaderHoodId, uint256 leaderRenown) {
            return (solsticeLeaderHood[eventId], solsticeLeaderRenown[eventId]);
        }

        // Tax Train State
        function getTaxTrainThreshold() external view returns (uint256) {
            return taxTrainThreshold;
        }
        function setTaxTrainThreshold(uint256 newThreshold) external onlyActiveEngine {
            taxTrainThreshold = newThreshold;
        }
        function getBossCooldown() external view returns (uint64) {
            return bossCooldown;
        }
        function setBossCooldown(uint64 cooldownEndsAt) external onlyActiveEngine {
            bossCooldown = cooldownEndsAt;
        }
        function isTaxTrainActive() external view returns (bool) {
            return taxTrainActive;
        }
        function setTaxTrainActive(bool active, uint256 eventId) external onlyActiveEngine {
            taxTrainActive = active;
            activeTaxTrainEventId = active ? eventId : 0;
        }
    }
    ```"""

content = content.replace(old_worldstate_block, new_worldstate_block)

# 5. Update HoodQuestTreasures.sol in Section 2 with itemRegistered and mintExpansionItem
old_treasures_expansion = r"""    function _burnGold(address from, uint256 amount) internal {
        _burn(from, 1, amount);
        cumulativeGoldBurned += amount;
        uint256 scaled = amount * 2500 + rebateCarryBps;
        uint256 credit = scaled / 10_000;
        rebateCarryBps = uint16(scaled % 10_000);
        cumulativeRebateCredits += credit;
        freeRebateReserve += credit;
    }"""

new_treasures_expansion = r"""    mapping(uint256 => bool) public itemRegistered;

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
        require(!economicActionsPaused, "Economic actions paused");
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
    }"""

content = content.replace(old_treasures_expansion, new_treasures_expansion)

# 6. Update HoodQuestCompanions.sol in Section 2 with recordBondAge, settleDebondAge, and currentUtcDay
old_adopt_block = r"""        _safeMint(msg.sender, petId);
        emit CompanionAdopted(hoodId, petId, species);
    }"""

new_adopt_block = r"""        _safeMint(msg.sender, petId);
        emit CompanionAdopted(hoodId, petId, species);
    }

    mapping(uint256 => uint64) public hoodEffectiveAgeAtBond;
    mapping(uint256 => uint64) public accumulatedPetActiveSeconds;

    function recordBondAge(uint256 petId, uint64 hoodAge) external onlyHoodQuest {
        hoodEffectiveAgeAtBond[petId] = hoodAge;
    }

    function settleDebondAge(uint256 petId, uint64 hoodAge) external onlyHoodQuest {
        require(hoodEffectiveAgeAtBond[petId] <= hoodAge, "Invalid bond age");
        accumulatedPetActiveSeconds[petId] += (hoodAge - hoodEffectiveAgeAtBond[petId]);
        delete hoodEffectiveAgeAtBond[petId];
    }

    function currentUtcDay() public view returns (uint32) {
        return uint32(block.timestamp / 1 days);
    }"""

content = content.replace(old_adopt_block, new_adopt_block)

# 7. Section 3 Updates: Remove goldCarry from Raids, call hoodContract.settleGoldFraction, and activeEngine check
content = content.replace(
    'mapping(uint256 => HeistRequest) public heistRequests;\nmapping(uint256 => uint256) public goldCarry; // Token-bound fractional gold accumulator',
    'mapping(uint256 => HeistRequest) public heistRequests;'
)

old_req_heist_top = r"""function requestHeistBatch(uint256 hoodId, uint8 count) external returns (uint256 requestId) {
    require(count >= 1 && count <= 5, "Count must be 1..5");"""

new_req_heist_top = r"""function requestHeistBatch(uint256 hoodId, uint8 count) external returns (uint256 requestId) {
    require(hoodContract.activeEngine(address(this)), "Engine not active");
    require(count >= 1 && count <= 5, "Count must be 1..5");"""

content = content.replace(old_req_heist_top, new_req_heist_top)

# Update _resolveSequentialRoll and _resolveFallbackRoll to use hoodContract.settleGoldFraction
old_gold_roll = r"""    // 4. Fixed-Point Gold Carry Accumulator (HQ-ECO-001)
    bytes32 goldEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GOLD"));
    uint256 baseGold = 1 + (uint256(goldEntropy) % 3); // 1, 2, or 3 Gold
    uint256 scaled = baseGold * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps) + goldCarry[hoodId];
    uint256 wholeGold = scaled / 100_000_000;
    goldCarry[hoodId] = scaled % 100_000_000;
    bundle.gold += wholeGold;"""

new_gold_roll = r"""    // 4. Token-Bound Gold Carry Settled in Core (HQ-ECO-001)
    bytes32 goldEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GOLD"));
    uint256 baseGold = 1 + (uint256(goldEntropy) % 3); // 1, 2, or 3 Gold
    uint256 scaled = baseGold * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps);
    uint256 wholeGold = hoodContract.settleGoldFraction(hoodId, scaled);
    bundle.gold += wholeGold;"""

content = content.replace(old_gold_roll, new_gold_roll)

old_fallback_roll = r"""function _resolveFallbackRoll(
    uint256 hoodId,
    HeistSnapshot memory snap,
    RewardBundle memory bundle
) internal {
    uint256 scaled = 1 * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps) + goldCarry[hoodId];
    uint256 wholeGold = scaled / 100_000_000;
    goldCarry[hoodId] = scaled % 100_000_000;
    bundle.gold += wholeGold;
}"""

new_fallback_roll = r"""function _resolveFallbackRoll(
    uint256 hoodId,
    HeistSnapshot memory snap,
    RewardBundle memory bundle
) internal {
    uint256 scaled = 1 * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps);
    uint256 wholeGold = hoodContract.settleGoldFraction(hoodId, scaled);
    bundle.gold += wholeGold;
}"""

content = content.replace(old_fallback_roll, new_fallback_roll)

# 8. Section 6 Updates: companion rank immutable lookup logic
old_comp_table = r"""| Species (ID Range) | Rank 1 (0 XP) | Rank 2 (300 XP) | Rank 3 (900 XP) | Rank 4 (1,800 XP) | Rank 5 (3,650 XP Apex) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Camp Hound (#1–4,000)** | +0 DEF | +2 DEF | +4 DEF | +6 DEF | **+10 DEF** (Max Statutory Bonus) |
| **Hunting Falcon (#4,001–7,000)**| +0% Crit | +1.6% (160 bps) | +3.2% (320 bps) | +4.8% (480 bps) | **+8.0% (800 bps Crit Apex)** |
| **Barn Owl (#7,001–10,000)** | +0% Gold, +0 Ste | +2% Gold, +1 Ste | +4% Gold, +2 Ste | +6% Gold, +3 Ste | **+10% Gold (1,000 bps) & +5 Stealth** |"""

new_comp_table = r"""| Species (ID Range) | Rank 1 (0 XP) | Rank 2 (300 XP) | Rank 3 (900 XP) | Rank 4 (1,800 XP) | Rank 5 (3,650 XP Apex) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Camp Hound (#1–4,000)** | +0 DEF | +2 DEF | +4 DEF | +6 DEF | **+10 DEF** (Max Statutory Bonus) |
| **Hunting Falcon (#4,001–7,000)**| +0% Crit | +1.6% (160 bps) | +3.2% (320 bps) | +4.8% (480 bps) | **+8.0% (800 bps Crit Apex)** |
| **Barn Owl (#7,001–10,000)** | +0% Gold, +0 Ste | +2% Gold, +1 Ste | +4% Gold, +2 Ste | +6% Gold, +3 Ste | **+10% Gold (1,000 bps) & +5 Stealth** |

*Immutable Lookup Arrays (indexed by `rank - 1`):*
- **Hound DEF:** `[0, 2, 4, 6, 10]`
- **Falcon Crit:** `[0, 160, 320, 480, 800]` (in basis points)
- **Owl Gold Bonus:** `[0, 200, 400, 600, 1000]` (in basis points)
- **Owl Stealth:** `[0, 1, 2, 3, 5]`"""

content = content.replace(old_comp_table, new_comp_table)

# 9. Section 7 Updates:
# a) protectedUntil with max for normal Hoods, careProtect for Cornucopia
old_protected_until = r"""function protectedUntil(uint256 id) public view returns (uint64) {
    uint64 careProtect = lastCareTimestamp[id] + 3 days;
    bool hasCornucopia = (equippedSlot[id][4] == FRIARS_CORNUCOPIA);
    uint64 rationProtect = hasCornucopia ? type(uint64).max : rationsUntil[id];
    // Cornucopia provides immortal sustenance, but care protection still expires after 3 days
    return careProtect < rationProtect ? careProtect : rationProtect;
}"""

new_protected_until = r"""function protectedUntil(uint256 id) public view returns (uint64) {
    uint64 careProtect = lastCareTimestamp[id] + 3 days;

    if (equippedSlot[id][4] == FRIARS_CORNUCOPIA) {
        // Cornucopia prevents starvation but does NOT replace care.
        return careProtect;
    }

    uint64 rationProtect = rationsUntil[id];
    return careProtect > rationProtect ? careProtect : rationProtect;
}"""

content = content.replace(old_protected_until, new_protected_until)

# b) feed() requires !isSlumbering(hoodId) per INV-6
old_feed = r"""function feed(uint256 hoodId) external {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");"""

new_feed = r"""function feed(uint256 hoodId) external {
    _requireOwned(hoodId);
    require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!isSlumbering(hoodId), "Hero is slumbering");
    require(!bazaarEscrowed[hoodId], "Hero listed in Bazaar");"""

content = content.replace(old_feed, new_feed)

# c) effectiveEconomicRewardBps is hunger-only (10000 fed, 5000 starving)
old_reward_bps = r"""function effectiveEconomicRewardBps(uint256 hoodId) public view returns (uint256) {
    bool hasCornucopia = (equippedSlot[hoodId][4] == FRIARS_CORNUCOPIA);
    bool isFed = hasCornucopia || (block.timestamp <= rationsUntil[hoodId]);
    
    // Starvation penalty clamp: 50% yield (5,000 bps)
    if (!isFed) {
        return 5000;
    }
    
    // Fed yield: 10,000 bps (100%) + Devotion Ladder bonus (up to +10%)
    return 10000 + devotionBonusBps(hoodId);
}"""

new_reward_bps = r"""function effectiveEconomicRewardBps(uint256 hoodId) public view returns (uint256) {
    bool hasCornucopia = (equippedSlot[hoodId][4] == FRIARS_CORNUCOPIA);
    bool isFed = hasCornucopia || (block.timestamp <= rationsUntil[hoodId]);
    
    // Starvation penalty clamp: 50% yield (5,000 bps) vs Fed (10,000 bps)
    // Devotion bonus applies strictly to goldBonusBps, never universal loot chances
    return isFed ? 10000 : 5000;
}"""

content = content.replace(old_reward_bps, new_reward_bps)

# d) effectiveCombatStats & captureHeistSnapshot with rank - 1 lookup and Devotion in goldBonusBps
old_snapshots = r"""    uint256 petId = hoodBoundPet[hoodId];
    if (petId != 0) {
        uint8 sp = companionContract.species(petId);
        uint8 rank = companionContract.bondRank(petId);
        if (sp == 0) def += (rank == 5 ? 10 : rank * 2);
        else if (sp == 2) stealth += rank;
    }
    
    // Clamp to statutory invariants
    if (atk > 45) atk = 45;
    if (def > 30) def = 30;
    if (stealth > 30) stealth = 30;
}

function captureHeistSnapshot(uint256 hoodId) external view returns (HeistSnapshot memory) {
    (uint8 atk, uint8 def, uint8 stealth) = effectiveCombatStats(hoodId);
    uint16 critBps = 0;
    uint16 goldBonusBps = 0;
    
    uint256 petId = hoodBoundPet[hoodId];
    if (petId != 0) {
        uint8 sp = companionContract.species(petId);
        uint8 rank = companionContract.bondRank(petId);
        if (sp == 1) critBps = uint16(rank * 160); // Falcon: up to 800 bps (8%)
        else if (sp == 2) goldBonusBps = uint16(rank * 200); // Owl: up to 1000 bps (10%)
    }
    
    if (equippedSlot[hoodId][0] == GILDED_BOW) {
        goldBonusBps += 2000; // +20%
    }
    if (goldBonusBps > 4000) goldBonusBps = 4000; // Max 40% statutory cap
    
    return HeistSnapshot({
        atk: atk,
        def: def,
        stealth: stealth,
        critBps: critBps,
        goldBonusBps: goldBonusBps,
        economicRewardBps: uint16(effectiveEconomicRewardBps(hoodId)),
        initialFatigue: isHeroFatigued[hoodId]
    });
}"""

new_snapshots = r"""    uint256 petId = hoodBoundPet[hoodId];
    if (petId != 0) {
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
    
    // Clamp to statutory invariants
    if (atk > 45) atk = 45;
    if (def > 30) def = 30;
    if (stealth > 30) stealth = 30;
}

function captureHeistSnapshot(uint256 hoodId) external view returns (HeistSnapshot memory) {
    (uint8 atk, uint8 def, uint8 stealth) = effectiveCombatStats(hoodId);
    uint16 critBps = 0;
    uint16 goldBonusBps = 0;
    
    uint256 petId = hoodBoundPet[hoodId];
    if (petId != 0) {
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
        goldBonusBps += 2000; // +20%
    }
    // Devotion bonus is added directly to Gold bonus (capped at +40% statutory maximum)
    goldBonusBps += devotionBonusBps(hoodId);
    if (goldBonusBps > 4000) goldBonusBps = 4000; // Max 40% statutory cap
    
    return HeistSnapshot({
        atk: atk,
        def: def,
        stealth: stealth,
        critBps: critBps,
        goldBonusBps: goldBonusBps,
        economicRewardBps: uint16(effectiveEconomicRewardBps(hoodId)),
        initialFatigue: isHeroFatigued[hoodId]
    });
}"""

content = content.replace(old_snapshots, new_snapshots)

# 10. Section 9 Updates:
# a) Calendar prose
old_calendar_prose = r"""### 1. Sherwood Astronomical Calendar:
The perpetual Sherwood Calendar runs on an autonomous 365-day astronomical cycle:
- **12 Months × 30 Days (Days 1–360):** Regular gameplay and monthly Castle Infiltrations.
- **5 Intercalary Solstice Days (Days 361–365):** The Grand Solstice Vault Heist tournament.
- **First-Month Handshake:** Day 1 begins at `GENESIS_TIME`, with zero pre-mine or retroactive active-Hood requirements."""

new_calendar_prose = r"""### 1. Sherwood Astronomical Calendar:
The perpetual Sherwood Calendar runs on an autonomous 365-day astronomical cycle:
- **Regular Calendar: Days 1–360 (12 Months × 30 Days):** Regular gameplay and monthly Castle Infiltrations.
- **Intercalary Solstice Days: Days 361–365 (5 Days):** The 5 sacred Solstice intercalary festival days.
- **Solstice Championship Window: Days 359–365 (7 Days):** The annual 7-day competitive Solstice Vault Heist tournament begins two days early at day index 358 and runs through Day 365.
- **First-Month Handshake:** Day 1 begins at `GENESIS_TIME`, with zero pre-mine or retroactive active-Hood requirements."""

content = content.replace(old_calendar_prose, new_calendar_prose)

# b) Active engine check in requestActionEvent and commitSolsticeManeuver
old_action_req_top = r"""    syncWorldEvents();
    EventConfig memory cfg = worldStateContract.getEvent(eventId);"""

new_action_req_top = r"""    require(hoodContract.activeEngine(address(this)), "Engine not active");
    syncWorldEvents();
    EventConfig memory cfg = worldStateContract.getEvent(eventId);"""

content = content.replace(old_action_req_top, new_action_req_top)

old_solstice_commit_top = r"""function commitSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secretHash, uint8 maneuverIndex) external returns (uint64 target) {
    syncWorldEvents();"""

new_solstice_commit_top = r"""function commitSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secretHash, uint8 maneuverIndex) external returns (uint64 target) {
    require(hoodContract.activeEngine(address(this)), "Engine not active");
    syncWorldEvents();"""

content = content.replace(old_solstice_commit_top, new_solstice_commit_top)

# c) resolveActionEvent: addContribution returns (firstPositive, cumulative); updateJubileeTop5 with cumulative
old_action_res = r"""        if (points > 0) {
            worldStateContract.addContribution(req.eventId, req.hoodId, points);
            
            if (req.kind == ActionKind.CASTLE) {
                uint32 mEpoch = uint32(req.eventId - 1_000_000);
                worldStateContract.addCastleBreach(req.eventId, points, getBreachTarget(mEpoch));
            } else if (req.kind == ActionKind.JUBILEE) {
                worldStateContract.updateJubileeTop5(req.eventId, req.hoodId, points);
            }
        }"""

new_action_res = r"""        if (points > 0) {
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
        }"""

content = content.replace(old_action_res, new_action_res)

# d) revealSolsticeManeuver: addContribution returns (firstPositive, ); increment entitlement
old_solstice_reveal = r"""        // Accrues both canonical hoodContribution and solsticeRenown via WorldState
        worldStateContract.addContribution(eventId, hoodId, points);
        worldStateContract.addSolsticeRenown(eventId, hoodId, points);"""

new_solstice_reveal = r"""        // Accrues both canonical hoodContribution and solsticeRenown via WorldState
        (bool firstPositive, ) = worldStateContract.addContribution(eventId, hoodId, points);
        if (firstPositive) {
            hoodContract.incrementPendingEventEntitlement(hoodId);
        }
        worldStateContract.addSolsticeRenown(eventId, hoodId, points);"""

content = content.replace(old_solstice_reveal, new_solstice_reveal)

# e) finalizeEvent: markEventFinalized lock in WorldState
old_finalize_event = r"""    e.totalContribution = worldStateContract.getTotalContribution(eventId);
    bool payableEvent = (cfg.kind != EventKind.CASTLE || worldStateContract.isCastleBreached(eventId));
    
    if (e.totalContribution == 0 || !payableEvent) {
        e.finalBudget = 0;
        eventGoldSettled[eventId] = true;
    } else {
        e.finalBudget = treasuresContract.reserveEventBudget(eventId, cfg.cap);
        eventLiabilityOpen[eventId] = true;
        outstandingEventLiabilitiesByEngine[address(this)]++;
        _reserveEventTrophies(eventId, cfg);
    }
    
    e.finalized = true;"""

new_finalize_event = r"""    // WorldState owns the canonical one-time finalization lock across engine upgrades
    worldStateContract.markEventFinalized(eventId);

    e.totalContribution = worldStateContract.getTotalContribution(eventId);
    bool payableEvent = (cfg.kind != EventKind.CASTLE || worldStateContract.isCastleBreached(eventId));
    
    if (e.totalContribution == 0 || !payableEvent) {
        e.finalBudget = 0;
        eventGoldSettled[eventId] = true;
    } else {
        e.finalBudget = treasuresContract.reserveEventBudget(eventId, cfg.cap);
        eventLiabilityOpen[eventId] = true;
        outstandingEventLiabilitiesByEngine[address(this)]++;
        _reserveEventTrophies(eventId, cfg);
    }
    
    e.finalized = true;"""

content = content.replace(old_finalize_event, new_finalize_event)

# f) Restore expireHoodEventParticipation in Section 9
old_claim_trophy_end = r"""    treasuresContract.mintReservedTrophy(eventId, recipient, itemId);
    _tryCloseEventLiability(eventId);
    emit EventTrophyClaimed(eventId, hoodId, recipient, itemId);
}"""

new_claim_trophy_end = r"""    treasuresContract.mintReservedTrophy(eventId, recipient, itemId);
    _tryCloseEventLiability(eventId);
    emit EventTrophyClaimed(eventId, hoodId, recipient, itemId);
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
    emit HoodEventParticipationExpired(eventId, hoodId);
}"""

content = content.replace(old_claim_trophy_end, new_claim_trophy_end)

# 11. Section 10 Updates: registerExpansionItem with itemRegistered check and mintExpansionItem
old_section10_reg = r"""function registerExpansionItem(
    uint256 id,
    address module,
    SupplyMode mode,
    uint256 cap
) external onlyTimelock {
    require(id >= 21, "IDs 1..20 reserved for core");
    require(itemSupplyMode[id] == SupplyMode.UNCAPPED && itemLifetimeCap[id] == 0, "Item already registered");
    require(module != address(0), "Invalid module address");
    
    itemSupplyMode[id] = mode;
    itemLifetimeCap[id] = cap;
    itemAuthorizedModule[id] = module;
    emit ExpansionItemRegistered(id, module, mode, cap);
}"""

new_section10_reg = r"""mapping(uint256 => bool) public itemRegistered;

function registerExpansionItem(
    uint256 id,
    address module,
    SupplyMode mode,
    uint256 cap
) external onlyTimelock {
    require(id >= 21, "IDs 1..20 reserved for core");
    require(!itemRegistered[id], "Item already registered");
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
    require(!economicActionsPaused, "Economic actions paused");
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
}"""

content = content.replace(old_section10_reg, new_section10_reg)

# 12. Section 12 Invariants:
old_inv6 = r"""### INV-6: Slumbering Action Prohibition
- While `isSlumbering(tokenId) == true`, calls to `requestHeistBatch`, `requestActionEvent`, `commitSolsticeManeuver`, `feed`, and `soloForage` strictly revert."""

new_inv6 = r"""### INV-6: Slumbering Action Prohibition
- While `isSlumbering(tokenId) == true`, calls to `requestHeistBatch`, `requestActionEvent`, `commitSolsticeManeuver`, `feed`, and `soloForage` strictly revert.
- `dailyCare()` is the mandatory wake-up prerequisite; feeding can only follow once awake."""

content = content.replace(old_inv6, new_inv6)

# Write to generate_final_blueprint.py
with open('/home/arson/rhnftproject/generate_final_blueprint.py', 'w') as f:
    f.write(content)

print("Successfully wrote generate_final_blueprint.py")
