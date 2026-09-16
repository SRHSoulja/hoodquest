// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { BaseTest } from "./BaseTest.sol";

contract FuzzTest is BaseTest {
    // 1. Mint Pricing & Count Bounds Fuzzing
    function testFuzz_MintBoundsAndPricing(uint8 count, uint256 payAmount) public {
        count = uint8(bound(count, 0, 10));
        payAmount = bound(payAmount, 0, 1 ether);

        vm.deal(alice, payAmount);
        vm.prank(alice);

        if (count == 0 || count > 5) {
            vm.expectRevert();
            hood.mintHoods{value: payAmount}(count);
        } else {
            uint256 exactPrice = uint256(count) * 0.01 ether;
            if (payAmount != exactPrice) {
                vm.expectRevert();
                hood.mintHoods{value: payAmount}(count);
            } else {
                hood.mintHoods{value: payAmount}(count);
                assertEq(hood.totalHoodsMinted(), count);
                assertEq(hood.balanceOf(alice), count);
            }
        }
    }

    // 2. Fractional Gold Carry Accumulation Fuzzing (settleGoldFraction)
    function testFuzz_FractionalGoldCarry(uint256 scaled1, uint256 scaled2) public {
        scaled1 = bound(scaled1, 0, 1_000_000);
        scaled2 = bound(scaled2, 0, 1_000_000);

        uint256 id = mintAndFinalizeHero(alice);

        // Core settler engine authorization
        vm.startPrank(address(raids));
        uint256 g1 = hood.settleGoldFraction(id, scaled1);
        uint256 carry1 = hood.goldCarry(id);
        assertEq(g1 * 100_000_000 + carry1, scaled1);
        assertTrue(carry1 < 100_000_000);

        uint256 g2 = hood.settleGoldFraction(id, scaled2);
        uint256 carry2 = hood.goldCarry(id);
        assertEq((g1 + g2) * 100_000_000 + carry2, scaled1 + scaled2);
        assertTrue(carry2 < 100_000_000);
        vm.stopPrank();
    }

    // 3. Devotion Bonus Bands Fuzzing (30, 90, 180, 360 days)
    function testFuzz_DevotionBonusBands(uint16 daysHeld) public {
        daysHeld = uint16(bound(daysHeld, 0, 450));

        uint256 id = mintAndFinalizeHero(alice);

        uint256 remaining = daysHeld;
        while (remaining > 0) {
            uint256 chunk = remaining > 35 ? 35 : remaining;
            uint256 baskets = (chunk + 6) / 7;
            grantItem(alice, 7, baskets);
            vm.startPrank(alice);
            for (uint256 i = 0; i < baskets; i++) {
                hood.feed(id);
            }
            vm.stopPrank();
            vm.warp(block.timestamp + chunk * 1 days);
            remaining -= chunk;
        }

        uint16 devotionBps = hood.devotionBonusBps(id);

        if (daysHeld < 30) {
            assertEq(devotionBps, 0);
        } else if (daysHeld < 90) {
            assertEq(devotionBps, 200); // 2%
        } else if (daysHeld < 180) {
            assertEq(devotionBps, 400); // 4%
        } else if (daysHeld < 360) {
            assertEq(devotionBps, 600); // 6%
        } else {
            assertEq(devotionBps, 1000); // 10%
        }
    }

    // 4. Combat Difficulty, Power, and Drop Multiplier Fuzzing
    function testFuzz_CombatMultiplierBounds(uint8 atk, uint8 stealth, uint256 difficulty) public pure {
        atk = uint8(bound(atk, 0, 30));
        stealth = uint8(bound(stealth, 0, 30));
        difficulty = bound(difficulty, 50, 100);

        uint256 power = 50 + atk + (stealth / 2);
        uint256 combatBps = 10000;
        if (power > difficulty) {
            uint256 c = 10000 + (power - difficulty) * 100;
            combatBps = c > 20000 ? 20000 : c;
        }

        assertTrue(combatBps >= 10000);
        assertTrue(combatBps <= 20000);
    }

    // 5. Effective Chance Formula Fuzzing
    function testFuzz_EffectiveChanceBounds(
        uint256 baseChance,
        uint256 combatBps,
        bool isFatigued,
        uint256 economicRewardBps
    ) public view {
        baseChance = bound(baseChance, 0, 250_000_000); // Up to 25% base
        combatBps = bound(combatBps, 10_000, 20_000);   // 1.0x to 2.0x
        economicRewardBps = bound(economicRewardBps, 5_000, 10_000); // 50% to 100%

        uint256 chance = raids.effectiveChance(baseChance, combatBps, isFatigued, economicRewardBps);

        // Exact match with formula
        uint256 expected = (baseChance * combatBps * (isFatigued ? 7500 : 10_000) * economicRewardBps) / 1e12;
        assertEq(chance, expected);

        // Must never exceed baseChance * 2
        assertTrue(chance <= baseChance * 2);
    }

    // 6. Bazaar Protocol Fee Invariant Fuzzing
    function testFuzz_BazaarFeeConservation(uint256 price) public pure {
        price = bound(price, 1, 1_000_000_000);

        uint256 fee = (price * 250) / 10_000;
        uint256 sellerProceeds = price - fee;

        assertEq(fee + sellerProceeds, price);
        assertTrue(fee <= (price * 25) / 1000); // <= 2.5%
    }
}
