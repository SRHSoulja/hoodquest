// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { IERC721Enumerable } from "@openzeppelin/contracts/token/ERC721/extensions/IERC721Enumerable.sol";

interface IHoodQuestCompanions is IERC721Enumerable {
    function species(uint256 petId) external view returns (uint8);
    function petSpecies(uint256 petId) external view returns (uint8);
    function petSeed(uint256 petId) external view returns (bytes32);
    function petXp(uint256 petId) external view returns (uint256);
    function bondRank(uint256 petId) external view returns (uint8);
    function effectivePetAge(uint256 petId) external view returns (uint256);
    function recordBondAge(uint256 petId, uint64 hoodAge) external;
    function settleDebondAge(uint256 petId, uint64 hoodAge) external;
    function pendingForageYew(uint256 hoodId) external view returns (uint256);
    function pendingForageIron(uint256 hoodId) external view returns (uint256);
    function soloForage(uint256 petId) external;
    function claimForage(uint256 hoodId, address recipient) external;
    function adoptGenesisPet(uint256 hoodId, uint8 petSpeciesChoice) external returns (uint256 petId);
}
