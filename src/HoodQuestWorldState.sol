// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { EventConfig } from "./HoodQuestTypes.sol";
import { IHoodQuestWorldState } from "./interfaces/IHoodQuestWorldState.sol";

contract HoodQuestWorldState is IHoodQuestWorldState {
    address public immutable timelock;
    
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
    mapping(uint256 => uint32) public override eventParticipantCount; // Distinct positive contributors for liability closing

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

    event EngineRolesChanged(address indexed engine, bool active, bool resolver, bool settlement);
    event EventResolverAllowanceChanged(uint256 indexed eventId, address indexed resolver, bool allowed);

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

    constructor(address timelock_) {
        require(timelock_ != address(0), "Invalid timelock");
        timelock = timelock_;
        taxTrainThreshold = 100_000; // Baseline initial burn threshold
    }

    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
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
        if (firstPositive) {
            eventParticipantCount[eventId]++;
        }
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

    function _isBetterJubileeScore(uint256 newScore, uint256 newHoodId, uint256 existingScore, uint256 existingHoodId) internal pure returns (bool) {
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
