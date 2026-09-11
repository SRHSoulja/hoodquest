with open('/home/arson/rhnftproject/generate_final_blueprint.py', 'r') as f:
    code = f.read()

# 1. Remove duplicate Solstice functions in Core
old_dup_solstice = '''    function incrementSolsticeCommitment(uint256 hoodId) external onlyAuthorizedEngine {
        activeSolsticeCommitmentCount[hoodId]++;
    }
    function decrementSolsticeCommitment(uint256 hoodId) external onlyAuthorizedEngine {
        require(activeSolsticeCommitmentCount[hoodId] > 0, "Solstice commitment underflow");
        activeSolsticeCommitmentCount[hoodId]--;
    }'''

assert old_dup_solstice in code, "old_dup_solstice not found"
code = code.replace(old_dup_solstice + "\n\n", "")

# 2. Remove redeclared structs in Section 3 and Section 9
old_s3_structs = '''struct HeistSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
}

struct HeistRequest {
    uint256 hoodId;
    uint256 targetBlock;
    uint8 count;          // 1 to 5
    uint8 baseCount;      // Rolls i < baseCount are BASE rolls
    uint8 bonusCount;     // Rolls i >= baseCount are BONUS rolls
    uint32 monthEpochAtRequest;
    bytes32 heroSeed;
    HeistSnapshot snapshot;
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
}'''

new_s3_structs = '''// All canonical shared structs (HeistSnapshot, RewardBundle, etc.) are imported from HoodQuestTypes.sol
using HoodQuestTypes for *;

struct HeistRequest {
    uint256 hoodId;
    uint256 targetBlock;
    uint8 count;          // 1 to 5
    uint8 baseCount;      // Rolls i < baseCount are BASE rolls
    uint8 bonusCount;     // Rolls i >= baseCount are BONUS rolls
    uint32 monthEpochAtRequest;
    bytes32 heroSeed;
    HeistSnapshot snapshot;
}'''

assert old_s3_structs in code, "old_s3_structs not found"
code = code.replace(old_s3_structs, new_s3_structs)

old_s9_types = '''enum EventKind { CASTLE, TAX_TRAIN, JUBILEE, SOLSTICE }
enum ActionKind { CASTLE, TAX_TRAIN, JUBILEE }

struct EventConfig {
    bool exists;
    EventKind kind;
    uint32 eventYear;
    uint64 startTime;
    uint64 endTime;
    uint32 cap;
}'''

new_s9_types = '''// All canonical shared enums and structs (EventKind, ActionKind, EventConfig) are imported from HoodQuestTypes.sol
using HoodQuestTypes for *;'''

assert old_s9_types in code, "old_s9_types not found"
code = code.replace(old_s9_types, new_s9_types)

# 3. CombatSnapshot morale field in captureCombatSnapshot and Morale Castle scoring in _computeEventPoints
old_capture_combat = '''function captureCombatSnapshot(uint256 hoodId) external view returns (CombatSnapshot memory) {
    HeistSnapshot memory h = this.captureHeistSnapshot(hoodId);
    return CombatSnapshot({
        atk: h.atk,
        def: h.def,
        stealth: h.stealth,
        critBps: h.critBps,
        goldBonusBps: h.goldBonusBps,
        economicRewardBps: h.economicRewardBps,
        initialFatigue: h.initialFatigue
    });
}'''

new_capture_combat = '''function captureCombatSnapshot(uint256 hoodId) external view returns (CombatSnapshot memory) {
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
}'''

assert old_capture_combat in code, "old_capture_combat not found"
code = code.replace(old_capture_combat, new_capture_combat)

old_compute_castle = '''        if (roll + statBonus >= 45) {
            points = 25 + (uint256(entropy >> 16) % 15); // 25..39 points
        } else {
            points = 0;
        }'''

new_compute_castle = '''        // Morale (+10 from Silver Rallying Horn Castle Infiltration Aura) adds directly to the breach check
        uint256 effectiveRoll = roll + statBonus + req.snapshot.morale;
        if (effectiveRoll >= 45) {
            points = 25 + (uint256(entropy >> 16) % 15); // 25..39 points
        } else {
            points = 0;
        }'''

assert old_compute_castle in code, "old_compute_castle not found"
code = code.replace(old_compute_castle, new_compute_castle)

# 4. Pending-heist getter naming: hasPendingNormalHeist in requestHeistBatch
old_has_pending = 'require(!hoodContract.pendingNormalHeist(hoodId), "Pending heist batch already exists");'
new_has_pending = 'require(!hoodContract.hasPendingNormalHeist(hoodId), "Pending heist batch already exists");'
assert old_has_pending in code, "old_has_pending not found"
code = code.replace(old_has_pending, new_has_pending)

# 5. currentMonthEpoch calculation in Core & Raid call
old_epoch_calc = '''    function currentMonthEpoch() public view returns (uint32) {
        if (block.timestamp < GENESIS_TIME) return 0;
        return uint32((block.timestamp - GENESIS_TIME) / 30 days);
    }'''

new_epoch_calc = '''    function currentMonthEpoch() public view returns (uint32) {
        if (block.timestamp < GENESIS_TIME) return 0;
        uint256 elapsed = block.timestamp - GENESIS_TIME;
        uint32 yearIndex = uint32(elapsed / 365 days);
        uint256 day = (elapsed % 365 days) / 1 days;
        uint32 monthInYear = uint32(day < 360 ? day / 30 : 11);

        return yearIndex * 12 + monthInYear;
    }'''

assert old_epoch_calc in code, "old_epoch_calc not found"
code = code.replace(old_epoch_calc, new_epoch_calc)

old_raid_epoch = 'monthEpochAtRequest: currentMonthEpoch(),'
new_raid_epoch = 'monthEpochAtRequest: hoodContract.currentMonthEpoch(),'
assert old_raid_epoch in code, "old_raid_epoch not found"
code = code.replace(old_raid_epoch, new_raid_epoch)

# 6. Fallback Gold in _resolveFallbackRoll
old_fallback_carry = '''function _resolveFallbackRoll(
    uint256 hoodId,
    HeistSnapshot memory snap,
    RewardBundle memory bundle
) internal {
    // Runs through exact same fractional accumulator pipeline without forcing arbitrary 1 Gold
    uint256 scaled = 1 * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps) + goldCarry[hoodId];
    uint256 wholeGold = scaled / 100_000_000;
    goldCarry[hoodId] = scaled % 100_000_000;
    bundle.gold += wholeGold;
}'''

new_fallback_carry = '''function _resolveFallbackRoll(
    uint256 hoodId,
    HeistSnapshot memory snap,
    RewardBundle memory bundle
) internal {
    // Settles through Core-owned fractional accumulator
    uint256 scaled = 1 * (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps);
    bundle.gold += hoodContract.settleGoldFraction(hoodId, scaled);
}'''

assert old_fallback_carry in code, "old_fallback_carry not found"
code = code.replace(old_fallback_carry, new_fallback_carry)

# 7. consumeStaminaBatch modifier in Core
old_stamina_mod = 'function consumeStaminaBatch(uint256 hoodId, uint8 count) external onlyRaidEngine returns (uint8 baseConsumed, uint8 bonusConsumed) {'
new_stamina_mod = 'function consumeStaminaBatch(uint256 hoodId, uint8 count) external onlyActiveEngine returns (uint8 baseConsumed, uint8 bonusConsumed) {'
assert old_stamina_mod in code, "old_stamina_mod not found"
code = code.replace(old_stamina_mod, new_stamina_mod)

# 8. Trophy leaderboard getters tuple destructuring
old_trophy_destruct = '''    if (cfg.kind == EventKind.SOLSTICE && cfg.eventYear <= 20) {
        uint256 leader = worldStateContract.getSolsticeLeaderHood(eventId);
        if (leader != 0) {
            treasuresContract.reserveEventTrophy(eventId, GOLDEN_ARROW, 1);
            eventTrophyEntitlement[eventId][leader][GOLDEN_ARROW] = true;
            eventTrophiesOutstanding[eventId]++;
        }
    } else if (cfg.kind == EventKind.JUBILEE) {
        uint256 champion = worldStateContract.getJubileeTopHood(eventId, 0);
        if (champion != 0) {
            treasuresContract.reserveEventTrophy(eventId, GOLDEN_ARROW, 1);
            eventTrophyEntitlement[eventId][champion][GOLDEN_ARROW] = true;
            eventTrophiesOutstanding[eventId]++;
        }
        for (uint8 i = 0; i < 5; i++) {
            uint256 hood = worldStateContract.getJubileeTopHood(eventId, i);
            if (hood != 0) {
                treasuresContract.reserveEventTrophy(eventId, FRIARS_CORNUCOPIA, 1);
                eventTrophyEntitlement[eventId][hood][FRIARS_CORNUCOPIA] = true;
                eventTrophiesOutstanding[eventId]++;
            }
        }
    }'''

new_trophy_destruct = '''    if (cfg.kind == EventKind.SOLSTICE && cfg.eventYear <= 20) {
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
    }'''

assert old_trophy_destruct in code, "old_trophy_destruct not found"
code = code.replace(old_trophy_destruct, new_trophy_destruct)

# 9. Governance: WorldState, Core, and Treasury Timelock Authority
old_ws_const = '''        constructor() {
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
        }'''

new_ws_const = '''        constructor(address timelock_) {
            require(timelock_ != address(0), "Invalid timelock");
            owner = timelock_;
            taxTrainThreshold = 100_000; // Baseline initial burn threshold
        }

        modifier onlyTimelock() {
            require(msg.sender == owner, "Not timelock");
            _;
        }

        function setEngineRoles(address engine, bool active, bool resolver, bool settlement) external onlyTimelock {
            activeEngine[engine] = active;
            resolverEngine[engine] = resolver;
            settlementEngine[engine] = settlement;
            emit EngineRolesChanged(engine, active, resolver, settlement);
        }

        function setEventResolverAllowed(uint256 eventId, address resolver, bool allowed) external onlyTimelock {
            eventResolverAllowed[eventId][resolver] = allowed;
            emit EventResolverAllowanceChanged(eventId, resolver, allowed);
        }'''

assert old_ws_const in code, "old_ws_const not found"
code = code.replace(old_ws_const, new_ws_const)

# Core setEngineRoles
old_core_mod = '''    modifier onlySettlementEngine() {
        require(settlementEngine[msg.sender], "Not settlement engine");
        _;
    }'''

new_core_mod = '''    modifier onlySettlementEngine() {
        require(settlementEngine[msg.sender], "Not settlement engine");
        _;
    }

    address public timelock;
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

assert old_core_mod in code, "old_core_mod not found"
code = code.replace(old_core_mod, new_core_mod)

# Treasury setEngineRoles
old_treas_mod = '''    mapping(address => bool) public activeRaidEngine;    // May request heists, consume stamina, create events
    mapping(address => bool) public resolverApproved;     // May resolve existing requests & reserve drops/trophies
    mapping(address => bool) public settlementApproved;   // May settle existing reward claims & event liabilities'''

new_treas_mod = '''    mapping(address => bool) public activeRaidEngine;    // May request heists, consume stamina, create events
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
    }'''

assert old_treas_mod in code, "old_treas_mod not found"
code = code.replace(old_treas_mod, new_treas_mod)

# 10. Expansion economic pause guard
old_treas_pause = 'require(!economicActionsPaused, "Economic actions paused");'
new_treas_pause = 'require(!hoodContract.economicActionsPaused(), "Economic actions paused");'
assert old_treas_pause in code, "old_treas_pause not found"
code = code.replace(old_treas_pause, new_treas_pause)

old_sec10_pause = 'require(!economicActionsPaused, "Economic actions paused");'
# Check in rewardExpansionGold
old_reward_gold = '''function rewardExpansionGold(address to, uint256 amount) external nonReentrant {
    require(isModuleAuthorized[msg.sender], "Unauthorized module");
    require(to != address(0), "Invalid recipient");'''

new_reward_gold = '''function rewardExpansionGold(address to, uint256 amount) external nonReentrant {
    require(isModuleAuthorized[msg.sender], "Unauthorized module");
    require(!hoodContract.economicActionsPaused(), "Economic actions paused");
    require(to != address(0), "Invalid recipient");'''

assert old_reward_gold in code, "old_reward_gold not found"
code = code.replace(old_reward_gold, new_reward_gold)

# 11. Expansion registration rejects SupplyMode.SPLIT
old_reg_exp_s2 = '''        require(id >= 21, "IDs 1..20 reserved for core");
        require(!itemRegistered[id], "Item already registered");
        require(module != address(0), "Invalid module address");'''

new_reg_exp_s2 = '''        require(id >= 21, "IDs 1..20 reserved for core");
        require(!itemRegistered[id], "Item already registered");
        require(mode != SupplyMode.SPLIT, "Expansion SPLIT mode unsupported in V1");
        require(module != address(0), "Invalid module address");'''

assert old_reg_exp_s2 in code, "old_reg_exp_s2 not found"
code = code.replace(old_reg_exp_s2, new_reg_exp_s2)

old_reg_exp_s10 = '''    require(id >= 21, "IDs 1..20 reserved for core");
    require(!itemRegistered[id], "Item already registered");
    require(module != address(0), "Invalid module address");'''

new_reg_exp_s10 = '''    require(id >= 21, "IDs 1..20 reserved for core");
    require(!itemRegistered[id], "Item already registered");
    require(mode != SupplyMode.SPLIT, "Expansion SPLIT mode unsupported in V1");
    require(module != address(0), "Invalid module address");'''

assert old_reg_exp_s10 in code, "old_reg_exp_s10 not found"
code = code.replace(old_reg_exp_s10, new_reg_exp_s10)

# 12. Deterministic Tie-Breaking for Jubilee and Solstice
old_ws_sort = '''        // Jubilee Leaderboard (Cumulative Score Top 5)
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
        }'''

new_ws_sort = '''        function _isBetterJubileeScore(uint256 newScore, uint256 newHoodId, uint256 existingScore, uint256 existingHoodId) internal pure returns (bool) {
            if (existingHoodId == 0) return true;
            if (newScore > existingScore) return true;
            if (newScore == existingScore && newHoodId < existingHoodId) return true;
            return false;
        }

        // Jubilee Leaderboard (Cumulative Score Top 5 with Deterministic Tie-Breaking: Higher Score, Lower Hood ID)
        function updateJubileeTop5(uint256 eventId, uint256 hoodId, uint256 newCumulativeScore) external onlyEventResolver(eventId) {
            JubileeEntry[5] storage top = jubileeTop5[eventId];
            for (uint256 i = 0; i < 5; i++) {
                if (top[i].hoodId == hoodId) {
                    top[i].score = newCumulativeScore;
                    _sortJubileeTop5(top);
                    return;
                }
            }
            if (_isBetterJubileeScore(newCumulativeScore, hoodId, top[4].score, top[4].hoodId)) {
                top[4] = JubileeEntry({hoodId: hoodId, score: newCumulativeScore});
                _sortJubileeTop5(top);
            }
        }

        function _sortJubileeTop5(JubileeEntry[5] storage top) internal {
            for (uint256 i = 0; i < 4; i++) {
                for (uint256 j = 0; j < 4 - i; j++) {
                    if (_isBetterJubileeScore(top[j + 1].score, top[j + 1].hoodId, top[j].score, top[j].hoodId)) {
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

        // Solstice Renown & Leaderboard (Higher Renown Wins; Equal Renown -> Lower Hood ID Wins)
        function addSolsticeRenown(uint256 eventId, uint256 hoodId, uint256 points) external onlyEventResolver(eventId) {
            solsticeRenown[eventId][hoodId] += points;
            uint256 current = solsticeRenown[eventId][hoodId];
            uint256 currentLeaderRenown = solsticeLeaderRenown[eventId];
            uint256 currentLeaderHood = solsticeLeaderHood[eventId];

            if (current > currentLeaderRenown || 
               (current == currentLeaderRenown && (currentLeaderHood == 0 || hoodId < currentLeaderHood))) {
                solsticeLeaderRenown[eventId] = current;
                solsticeLeaderHood[eventId] = hoodId;
            }
        }'''

assert old_ws_sort in code, "old_ws_sort not found"
code = code.replace(old_ws_sort, new_ws_sort)

# 13 & 14. Add Migration Protocol and Monthly Castle Schedule Clarification in Section 9
old_cal_head = '''### 1. Sherwood Astronomical Calendar:
The perpetual Sherwood Calendar runs on an autonomous 365-day astronomical cycle:
- **Regular Calendar: Days 1–360 (12 Months × 30 Days):** Regular gameplay and monthly Castle Infiltrations.
- **Intercalary Solstice Days: Days 361–365 (5 Days):** The 5 sacred Solstice intercalary festival days.
- **Solstice Championship Window: Days 359–365 (7 Days):** The annual 7-day competitive Solstice Vault Heist tournament begins two days early at day index 358 and runs through Day 365.
- **First-Month Handshake:** Day 1 begins at `GENESIS_TIME`, with zero pre-mine or retroactive active-Hood requirements.'''

new_cal_head = '''### 1. Sherwood Astronomical Calendar & Castle Schedule:
The perpetual Sherwood Calendar runs on an autonomous 365-day astronomical cycle:
- **Regular Calendar: Days 1–360 (12 Months × 30 Days):** Regular gameplay and monthly Castle Infiltrations.
- **Monthly Castle Schedule:** Months 1–11 host monthly Castle Infiltrations (scheduled Days 28–30 of each month; day indices 27..29). Month 12 is replaced by the year-end Jubilee (Days 351–357) and the Grand Solstice Championship tournament window (Days 359–365).
- **Intercalary Solstice Days: Days 361–365 (5 Days):** The 5 sacred Solstice intercalary festival days.
- **Solstice Championship Window: Days 359–365 (7 Days):** The annual 7-day competitive Solstice Vault Heist tournament begins two days early at day index 358 and runs through Day 365.
- **First-Month Handshake:** Day 1 begins at `GENESIS_TIME`, with zero pre-mine or retroactive active-Hood requirements.

### 2. Raid Engine Replacement & Event Migration Protocol (HQ-GOV-004):
Before removing active engine status from Raid Engine V1:
1. Timelock sets Raid Engine V2 as `activeEngine` in Core, WorldState, and Treasury (`setEngineRoles(address(V2), true, true, false)`).
2. Timelock calls `worldStateContract.setEventResolverAllowed(eventId, address(V2), true)` for every active or unfinished canonical event.
3. V1 retains `resolverEngine` approval strictly to resolve already-issued requests.
4. V2 owns finalization of unfinished events (`finalizeEvent()`).
5. V1 remains `settlementApproved` only for liabilities it already finalized until all claims reach zero.'''

assert old_cal_head in code, "old_cal_head not found"
code = code.replace(old_cal_head, new_cal_head)

# Also update Section 9 section numbering to follow
code = code.replace('### 2. Event Kinds & Zero-Keeper', '### 3. Event Kinds & Zero-Keeper')
code = code.replace('### 3. Unified Reusable `ActionRequest` Engine', '### 4. Unified Reusable `ActionRequest` Engine')
code = code.replace('### 4. Executable Solstice Championship', '### 5. Executable Solstice Championship')
code = code.replace('### 5. Deterministic Reveal Verification', '### 6. Deterministic Reveal Verification')
code = code.replace('### 6. Event Finalization, Entitlement Verification', '### 7. Event Finalization, Entitlement Verification')

with open('/home/arson/rhnftproject/generate_final_blueprint.py', 'w') as f:
    f.write(code)

print("Successfully applied patch_v1_frozen_closure.py!")
