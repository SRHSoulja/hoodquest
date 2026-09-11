// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { IERC721Enumerable } from "@openzeppelin/contracts/token/ERC721/extensions/IERC721Enumerable.sol";
import { HeistSnapshot, CombatSnapshot, BazaarTransferMode } from "../HoodQuestTypes.sol";

interface IHoodQuest is IERC721Enumerable {
    function heroSeed(uint256 tokenId) external view returns (bytes32);
    function heroArchetype(uint256 tokenId) external view returns (uint8);
    function GENESIS_TIME() external view returns (uint256);
    function currentUtcDay() external view returns (uint32);
    function economicActionsPaused() external view returns (bool);
    function expectedPetDeposit(uint256 tokenId) external view returns (address);
    function petBoundToHood(uint256 petId) external view returns (uint256);
    function hoodBoundPet(uint256 hoodId) external view returns (uint256);
    function bazaarEscrowed(uint256 tokenId) external view returns (bool);
    function equippedSlot(uint256 tokenId, uint8 slot) external view returns (uint32);
    function effectiveBiologicalAge(uint256 tokenId) external view returns (uint256);
    function isSlumbering(uint256 tokenId) external view returns (bool);
    function isGameDelegate(uint256 tokenId, address delegate) external view returns (bool);
    function hasPendingNormalHeist(uint256 tokenId) external view returns (bool);
    function setPendingNormalHeist(uint256 tokenId, bool pending) external;
    function solsticeCommitmentCount(uint256 tokenId) external view returns (uint8);
    function incrementSolsticeCommitment(uint256 tokenId) external;
    function decrementSolsticeCommitment(uint256 tokenId) external;
    function touchActivity(uint256 tokenId) external;
    function consumeStamina(uint256 tokenId, uint8 count) external;
    function captureHeistSnapshot(uint256 tokenId) external view returns (HeistSnapshot memory);
    function captureCombatSnapshot(uint256 tokenId) external view returns (CombatSnapshot memory);
    function setBazaarTransferMode(BazaarTransferMode mode) external;
    function bazaarLock(uint256 tokenId) external;
    function bazaarUnlock(uint256 tokenId) external;
    function canList(uint256 tokenId) external view returns (bool allowed, uint256 reasonFlags);
    function getLoadoutHash(uint256 tokenId) external view returns (bytes32);
    function setBazaarEscrowed(uint256 tokenId, bool escrowed) external;
    function activeEngine(address engine) external view returns (bool);
    function resolverEngine(address engine) external view returns (bool);
    function settlementEngine(address engine) external view returns (bool);
    function currentMonthEpoch() external view returns (uint32);
    function consumeStaminaBatch(uint256 hoodId, uint8 count) external returns (uint8 baseConsumed, uint8 bonusConsumed);
    function refreshActivitySustained(uint256 hoodId) external;
    function incrementPendingGameplay(uint256 hoodId, uint32 count) external;
    function decrementPendingGameplay(uint256 hoodId, uint32 count) external;
    function incrementPendingEventEntitlement(uint256 hoodId) external;
    function decrementPendingEventEntitlement(uint256 hoodId) external;
    function setFatigue(uint256 hoodId, bool fatigued) external;
    function settleGoldFraction(uint256 hoodId, uint256 scaledNumerator) external returns (uint256 wholeGold);
}
