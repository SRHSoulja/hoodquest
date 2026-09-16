// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { BaseTest } from "../BaseTest.sol";
import { Handler } from "./Handler.sol";

contract InvariantsTestStateful is BaseTest {
    Handler public handler;

    function setUp() public override {
        super.setUp();
        handler = new Handler(hood, treasures, bazaar, raids, mockArbSys);
        targetContract(address(handler));
    }

    // INV-1: Hood Token Supply & ID Invariant
    function invariant_INV1_TokenSupplyBounds() public view {
        uint256 total = hood.totalHoodsMinted();
        assertLe(total, 10_000);
    }

    // INV-2: Mythic Grail Lifetime Mint Ceilings (Golden Arrow #4 <= 25, Cornucopia #9 <= 25)
    function invariant_INV2_GrailLifetimeMintCeilings() public view {
        assertLe(treasures.lifetimeMinted(4) + treasures.reservedUnclaimed(4) + treasures.forfeitedGrails(4), 25);
        assertLe(treasures.lifetimeMinted(9) + treasures.reservedUnclaimed(9) + treasures.forfeitedGrails(9), 25);
    }

    // INV-7: Bounded Expansion Emission Ceiling (<= 25,000 Gold/day)
    function invariant_INV7_ExpansionEmissionCeiling() public view {
        assertLe(treasures.totalAllocatedDailyCap(), 25_000);
    }

    // INV-8 & INV-15: Armory Vault Custody Integrity & Aggregate Custody
    function invariant_INV8_INV15_ArmoryVaultCustody() public view {
        assertEq(treasures.balanceOf(address(hood), 13), hood.boundCount(13));
        assertEq(treasures.balanceOf(address(hood), 4), hood.boundCount(4));
    }

    // INV-9: Global Rebate Reserve Solvency (25% rebate, 75% permanent deflation)
    function invariant_INV9_RebateReserveSolvency() public view {
        assertEq(
            treasures.cumulativeRebateCredits(),
            treasures.freeRebateReserve() + treasures.outstandingEventGold() + treasures.cumulativeEventGoldMinted()
        );
    }

    // INV-17: Bazaar Escrow Solvency & Liability Coverage
    function invariant_INV17_BazaarEscrowSolvency() public view {
        assertGe(treasures.balanceOf(address(bazaar), 1), handler.totalProceedsEscrowed());
    }

    // INV-18: Gilded Bow Split Cap Invariant (750 craft, 250 drop, 1000 total)
    function invariant_INV18_GildedBowCaps() public view {
        assertLe(treasures.forgedGildedBows(), 750);
        assertLe(treasures.droppedGildedBows() + treasures.dropReservedGildedBows(), 250);
        assertLe(treasures.lifetimeMinted(3), 1000);
    }
}
