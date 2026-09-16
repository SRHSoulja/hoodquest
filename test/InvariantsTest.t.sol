// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { BaseTest } from "./BaseTest.sol";
import { ActionKind, EventKind, SupplyMode, MintSource } from "../src/HoodQuestTypes.sol";

contract InvariantsTest is BaseTest {
    // INV-1: Hood Token Supply & ID Invariant
    function test_INV1_SupplyAndIdInvariant() public {
        uint256 id = mintAndFinalizeHero(alice);
        assertTrue(id >= 1 && id <= 10_000);
        assertEq(hood.totalHoodsMinted(), 1);

        // Token 0 does not exist
        vm.expectRevert();
        hood.ownerOf(0);
    }

    // INV-2: Mythic Grail Lifetime Mint Ceilings (Golden Arrow #4 <= 25, Cornucopia #9 <= 25)
    function test_INV2_GrailLifetimeMintCeilings() public view {
        assertEq(treasures.itemLifetimeCap(4), 25);
        assertEq(treasures.itemLifetimeCap(9), 25);
        assertTrue(treasures.lifetimeMinted(4) + treasures.reservedUnclaimed(4) + treasures.forfeitedGrails(4) <= 25);
        assertTrue(treasures.lifetimeMinted(9) + treasures.reservedUnclaimed(9) + treasures.forfeitedGrails(9) <= 25);
    }

    // INV-3: Companion Genesis Parity & Adoption Limit
    function test_INV3_CompanionGenesisParityAndAdoptionLimit() public {
        uint256 id = mintAndFinalizeHero(alice);

        grantItem(alice, 1, 100);
        vm.prank(alice);
        uint256 pet1 = companions.adoptGenesisPet(id, 0); // Hound (1..4000)
        assertTrue(pet1 >= 1 && pet1 <= 4000);
        assertTrue(companions.genesisAdoptionUsed(id));

        vm.prank(alice);
        vm.expectRevert("Genesis pet already adopted for this Hood");
        companions.adoptGenesisPet(id, 0);
    }

    // INV-4: Identity-Bound Temporal Tracking
    function test_INV4_IdentityBoundTemporalTracking() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Alice plays heist
        vm.prank(alice);
        uint256 reqId = raids.requestHeistBatch(id, 3, alice);
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raids.resolveHeist(reqId);

        assertEq(hood.baseHeistsUsed(id), 3);
        uint64 sustainedBefore = hood.activitySustainedUntil(id);
        assertTrue(sustainedBefore > 0);

        // Alice transfers to Bob
        vm.prank(alice);
        hood.transferFrom(alice, bob, id);

        // State remains bound to token ID, not owner
        assertEq(hood.baseHeistsUsed(id), 3);
        assertEq(hood.activitySustainedUntil(id), sustainedBefore);
        assertEq(hood.ownerOf(id), bob);
    }

    // INV-5: Sustenance & Starvation Economic Clamp (10,000 bps vs 5,000 bps)
    function test_INV5_SustenanceAndStarvationEconomicClamp() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Just minted: initial day care sustains, economic reward is 10,000
        assertEq(hood.effectiveEconomicRewardBps(id), 10_000);

        // Warp 8 days with no activity and no food
        vm.warp(block.timestamp + 8 days);

        // Starvation clamp: exactly 5,000 bps
        assertEq(hood.effectiveEconomicRewardBps(id), 5_000);

        // Active adventuring restores 10,000 bps
        // Wake up first
        vm.prank(alice);
        hood.dailyCare(id);
        vm.prank(alice);
        uint256 reqId = raids.requestHeistBatch(id, 1, alice);
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raids.resolveHeist(reqId);

        // Restored to full 10,000 bps
        assertEq(hood.effectiveEconomicRewardBps(id), 10_000);
    }

    // INV-6: Slumbering Action Prohibition
    function test_INV6_SlumberingActionProhibition() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Warp into slumber (8 days)
        vm.warp(block.timestamp + 8 days);
        assertTrue(hood.isSlumbering(id));

        // Heist reverts
        vm.prank(alice);
        vm.expectRevert("Hero is slumbering");
        raids.requestHeistBatch(id, 1, alice);

        // Feed reverts
        vm.prank(alice);
        vm.expectRevert();
        hood.feed(id);
    }

    // INV-7: Bounded Expansion Emission Ceiling (<= 25,000 Gold/day)
    function test_INV7_BoundedExpansionEmissionCeiling() public {
        treasures.setModuleAuthorization(address(this), 25_000, true);
        assertEq(treasures.totalAllocatedDailyCap(), 25_000);

        // Cannot allocate cap exceeding 25,000
        vm.expectRevert("Exceeds 25k daily cap");
        treasures.setModuleAuthorization(bob, 1, true);

        // Mint exactly 25,000
        treasures.rewardExpansionGold(alice, 25_000);
        assertEq(treasures.balanceOf(alice, 1), 25_000);

        // Cannot mint more today
        vm.expectRevert("Exceeds daily module cap");
        treasures.rewardExpansionGold(alice, 1);
    }

    // INV-8: Armory Vault Custody Integrity & Arrow Dependency
    function test_INV8_ArmoryVaultCustodyAndArrowDependency() public {
        uint256 id = mintAndFinalizeHero(alice);

        grantItem(alice, 13, 1); // Bow
        grantItem(alice, 4, 1);  // Golden Arrow

        vm.startPrank(alice);
        treasures.setApprovalForAll(address(hood), true);
        hood.equipItem(id, 0, 13);
        hood.equipItem(id, 2, 4);

        // Invariant: Core vault balance == boundCount
        assertEq(treasures.balanceOf(address(hood), 13), hood.boundCount(13));
        assertEq(treasures.balanceOf(address(hood), 4), hood.boundCount(4));

        // Arrow requires Bow: cannot initiate unequip of Bow while Arrow equipped
        vm.expectRevert();
        hood.initiateUnequip(id, 0);
        vm.stopPrank();
    }

    // INV-9: Global Rebate Reserve Solvency (25% rebate, 75% deflation)
    function test_INV9_GlobalRebateReserveSolvency() public {
        treasures.setModuleAuthorization(address(this), 25000, true);
        treasures.rewardExpansionGold(alice, 100);

        // Alice burns 100 Gold via adoption or craft
        // In Treasures, _burnGold credits 25% to freeRebateReserve
        vm.prank(address(companions));
        treasures.burnAdoptionGold(alice, 100);

        assertEq(treasures.cumulativeGoldBurned(), 100);
        assertEq(treasures.cumulativeRebateCredits(), 25);
        assertEq(
            treasures.cumulativeRebateCredits(),
            treasures.freeRebateReserve() + treasures.outstandingEventGold() + treasures.cumulativeEventGoldMinted()
        );
    }

    // INV-10: Delayed Entropy Terminal State Guarantee (> 256 blocks fallback)
    function test_INV10_DelayedEntropyTerminalStateGuarantee() public {
        uint256 id = mintAndFinalizeHero(alice);

        vm.prank(alice);
        uint256 reqId = raids.requestHeistBatch(id, 5, alice);

        // Fast-forward ArbSys past 256 blocks
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 500);

        // Terminal fallback state resolves cleanly with zero reversions
        raids.resolveHeist(reqId);
        assertFalse(hood.hasPendingNormalHeist(id));
    }

    // INV-11: Mixed Stamina Batch Roll Classification
    function test_INV11_MixedStaminaBatchRollClassification() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Use 4 base heists
        vm.prank(alice);
        uint256 req1 = raids.requestHeistBatch(id, 4, alice);
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raids.resolveHeist(req1);

        // Alice unlocks bonus stamina with Elixir (#5)
        grantItem(alice, 5, 1);
        vm.prank(alice);
        hood.useElixir(id);

        // Now request 3 heists: 1 remaining base, 2 bonus
        vm.prank(alice);
        uint256 req2 = raids.requestHeistBatch(id, 3, alice);

        (,,,uint8 count, uint8 baseCount, uint8 bonusCount,,,) = raids.heistRequests(req2);
        assertEq(count, 3);
        assertEq(baseCount, 1);
        assertEq(bonusCount, 2);

        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raids.resolveHeist(req2);
    }

    // INV-12: Single Pending Heist Batch Invariant
    function test_INV12_SinglePendingHeistBatchInvariant() public {
        uint256 id = mintAndFinalizeHero(alice);

        vm.prank(alice);
        raids.requestHeistBatch(id, 1, alice);

        vm.prank(alice);
        vm.expectRevert("Pending heist batch already exists");
        raids.requestHeistBatch(id, 1, alice);
    }

    // INV-13: Delegate Asset Non-Redirection & Recipient Safety
    function test_INV13_DelegateAssetNonRedirection() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Alice sets Bob as game delegate
        vm.prank(alice);
        hood.setGameDelegate(id, bob, true);

        // Bob cannot direct rewards to himself
        vm.prank(bob);
        vm.expectRevert("Delegates can only direct rewards to Hood owner");
        raids.requestHeistBatch(id, 1, bob);

        // Bob can direct rewards to Alice (owner)
        vm.prank(bob);
        uint256 reqId = raids.requestHeistBatch(id, 1, alice);
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raids.resolveHeist(reqId);
    }

    // INV-14: Permissionless Atomic Heist Settlement Solvency
    function test_INV14_AtomicHeistSettlementSolvency() public {
        uint256 id = mintAndFinalizeHero(alice);

        vm.prank(alice);
        uint256 reqId = raids.requestHeistBatch(id, 5, alice);
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);

        // Anyone (e.g. Charlie) can permissionlessly resolve heist, rewards settle directly to Alice
        vm.prank(charlie);
        raids.resolveHeist(reqId);

        // Request deleted atomically
        (uint256 reqHoodId,,,,,,,,) = raids.heistRequests(reqId);
        assertEq(reqHoodId, 0);
    }

    // INV-15: Aggregate ERC-1155 Vault Custody
    function test_INV15_AggregateVaultCustody() public {
        uint256 id1 = mintAndFinalizeHero(alice);
        uint256 id2 = mintAndFinalizeHero(bob);

        grantItem(alice, 13, 1);
        grantItem(bob, 13, 1);

        vm.prank(alice);
        treasures.setApprovalForAll(address(hood), true);
        vm.prank(alice);
        hood.equipItem(id1, 0, 13);

        vm.prank(bob);
        treasures.setApprovalForAll(address(hood), true);
        vm.prank(bob);
        hood.equipItem(id2, 0, 13);

        // Aggregate vault custody: exactly 2 Bows
        assertEq(treasures.balanceOf(address(hood), 13), 2);
        assertEq(hood.boundCount(13), 2);
    }

    // INV-16: Per-Slot Unequip Request Isolation
    function test_INV16_PerSlotUnequipRequestIsolation() public {
        uint256 id = mintAndFinalizeHero(alice);

        grantItem(alice, 13, 1); // Slot 0
        grantItem(alice, 6, 1);  // Slot 1

        vm.startPrank(alice);
        treasures.setApprovalForAll(address(hood), true);
        hood.equipItem(id, 0, 13);
        hood.equipItem(id, 1, 6);

        // Unequip Slot 0 only
        hood.initiateUnequip(id, 0);

        // Slot 1 remains fully equipped and unaffected
        assertEq(hood.equippedSlot(id, 1), 6);
        (uint64 maturesAt1,) = hood.pendingUnequip(id, 1);
        assertEq(maturesAt1, 0);

        (uint64 maturesAt0,) = hood.pendingUnequip(id, 0);
        assertTrue(maturesAt0 > 0);
        vm.stopPrank();
    }

    // INV-17: Bazaar Escrow Solvency & Liability Coverage
    function test_INV17_BazaarEscrowSolvency() public {
        uint256 id = mintAndFinalizeHero(alice);

        vm.startPrank(alice);
        hood.approve(address(bazaar), id);
        bazaar.listHero(id, 100);
        vm.stopPrank();

        assertEq(hood.balanceOf(address(bazaar)), 1);

        treasures.setModuleAuthorization(address(this), 25000, true);
        treasures.rewardExpansionGold(bob, 100);

        vm.startPrank(bob);
        treasures.setApprovalForAll(address(bazaar), true);
        bazaar.buyListing(id);
        vm.stopPrank();

        // Treasury balance held in Bazaar >= seller proceeds liability
        assertEq(treasures.balanceOf(address(bazaar), 1), 98);
        assertEq(bazaar.bazaarProceedsEscrow(alice), 98);
    }

    // INV-18: Gilded Bow Split Cap Invariant (750 craft, 250 drop, 1000 total)
    function test_INV18_GildedBowSplitCapInvariant() public view {
        assertEq(treasures.itemLifetimeCap(3), 1000);
        assertTrue(treasures.forgedGildedBows() <= 750);
        assertTrue(treasures.droppedGildedBows() + treasures.dropReservedGildedBows() <= 250);
    }
}
