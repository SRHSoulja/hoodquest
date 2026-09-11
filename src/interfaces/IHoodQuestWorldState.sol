// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { EventConfig } from "../HoodQuestTypes.sol";

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
    function eventParticipantCount(uint256 eventId) external view returns (uint32);
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
    function setEventResolverAllowed(uint256 eventId, address resolver, bool allowed) external;
}
