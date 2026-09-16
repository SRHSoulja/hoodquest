// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Test } from "forge-std/Test.sol";
import { IERC1155 } from "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import { IHoodQuest } from "../src/interfaces/IHoodQuest.sol";
import { IHoodQuestTreasures } from "../src/interfaces/IHoodQuestTreasures.sol";
import { HoodQuestRaids } from "../src/HoodQuestRaids.sol";

interface IRaidsInspect {
    function getBreachTarget(uint32 year) external view returns (uint256);
    function castleManeuversUsed(uint256 year, uint256 hoodId) external view returns (uint8);
}

interface ITreasuresInspect {
    function craftRecipes(uint256 itemId) external view returns (bool, uint8, uint256, uint256, uint256, uint256);
}

contract AbiVerificationTest is Test {
    function test_VerifiedFunctionSelectors() public pure {
        // HoodQuest
        assertEq(bytes4(keccak256("effectiveBiologicalAge(uint256)")), IHoodQuest.effectiveBiologicalAge.selector);
        assertEq(bytes4(keccak256("isSlumbering(uint256)")), IHoodQuest.isSlumbering.selector);
        assertEq(bytes4(keccak256("heroArchetype(uint256)")), IHoodQuest.heroArchetype.selector);
        assertEq(bytes4(keccak256("heroSeed(uint256)")), IHoodQuest.heroSeed.selector);
        assertEq(bytes4(keccak256("equippedSlot(uint256,uint8)")), IHoodQuest.equippedSlot.selector);
        assertEq(bytes4(keccak256("hoodBoundPet(uint256)")), IHoodQuest.hoodBoundPet.selector);

        // HoodQuestTreasures
        assertEq(bytes4(keccak256("balanceOf(address,uint256)")), IERC1155.balanceOf.selector);
        assertEq(bytes4(keccak256("craftRecipes(uint256)")), ITreasuresInspect.craftRecipes.selector);

        // HoodQuestRaids
        assertEq(bytes4(keccak256("getBreachTarget(uint32)")), IRaidsInspect.getBreachTarget.selector);
        assertEq(bytes4(keccak256("castleManeuversUsed(uint256,uint256)")), IRaidsInspect.castleManeuversUsed.selector);
    }
}
