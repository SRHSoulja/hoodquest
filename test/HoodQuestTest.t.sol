// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { BaseTest } from "./BaseTest.sol";
import { ActionKind, EventKind, EventConfig } from "../src/HoodQuestTypes.sol";

contract HoodQuestTest is BaseTest {
    function test_MintHero_BoundsAndState() public {
        vm.prank(alice);
        hood.mintHoods{value: MINT_PRICE}(1);
        uint256 id1 = 1;
        assertEq(id1, 1);
        assertEq(hood.ownerOf(id1), alice);
        assertFalse(hood.isSlumbering(id1));
        assertEq(hood.effectiveBiologicalAge(id1), 0);

        // Advance ArbSys block and finalize seed
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        hood.finalizeHeroSeed(id1);

        assertTrue(hood.heroArchetype(id1) < 5);
        assertFalse(hood.heroSeed(id1) == bytes32(0));

        // Proceeds withdrawable
        hood.withdrawMintProceeds();
        assertEq(proceedsRecipient.balance, MINT_PRICE);

        // Cannot mint with insufficient funds
        vm.prank(alice);
        vm.expectRevert();
        hood.mintHoods{value: MINT_PRICE - 1}(1);
    }

    function test_DailyCareAndRations() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Advance 1 day to perform daily care
        vm.warp(block.timestamp + 1 days);
        vm.prank(alice);
        hood.dailyCare(id);

        // Rations give 7 days per basket
        grantItem(alice, 7, 2); // 2 Feast Baskets (#7)
        assertEq(treasures.balanceOf(alice, 7), 2);

        // Alice feeds hero
        vm.prank(alice);
        hood.feed(id);
        assertEq(treasures.balanceOf(alice, 7), 1);
        assertTrue(hood.rationsUntil(id) >= block.timestamp + 7 days - 1);

        // Slumber test: warp past protection/rations without care
        vm.warp(hood.protectedUntil(id) + 1);
        assertTrue(hood.isSlumbering(id));

        // Cannot feed while slumbering (INV-6)
        vm.prank(alice);
        vm.expectRevert();
        hood.feed(id);

        // Wake up with daily care
        vm.prank(alice);
        hood.dailyCare(id);
        assertFalse(hood.isSlumbering(id));

        // Now can feed
        vm.prank(alice);
        hood.feed(id);
        assertEq(treasures.balanceOf(alice, 7), 0);
    }

    function test_SlumberFreezesBiologicalAge_Mathematically() public {
        uint256 id = mintAndFinalizeHero(alice);
        // Mint grants 7 days starter rations (protected until t0 + 7 days)
        uint64 t0 = uint64(block.timestamp);

        // 1. Advance 4 days while awake
        vm.warp(t0 + 4 days);
        assertFalse(hood.isSlumbering(id));
        assertEq(hood.effectiveBiologicalAge(id), 4 days);

        // 2. Warp past day 7 (rations expire at day 7). Warp to day 37 (30 days of slumber)
        vm.warp(t0 + 37 days);
        assertTrue(hood.isSlumbering(id));
        // Hero was awake for exactly 7 days before rations expired.
        // During the 30 days of sleep (from day 7 to day 37), age must remain FROZEN at 7 days!
        assertEq(hood.effectiveBiologicalAge(id), 7 days);

        // 3. Let another 100 days pass in sleep (total 137 days since mint)
        vm.warp(t0 + 137 days);
        assertTrue(hood.isSlumbering(id));
        // Age is STILL frozen at 7 days!
        assertEq(hood.effectiveBiologicalAge(id), 7 days);

        // 4. Wake up with daily care on day 137
        vm.prank(alice);
        hood.dailyCare(id);
        assertFalse(hood.isSlumbering(id));
        // Immediate age at wake-up is still 7 days
        assertEq(hood.effectiveBiologicalAge(id), 7 days);

        // 5. Hero stays awake for 3 more days under daily care protection
        vm.warp(t0 + 140 days);
        assertFalse(hood.isSlumbering(id));
        // Age is now 7 days + 3 days = 10 days!
        assertEq(hood.effectiveBiologicalAge(id), 10 days);
    }

    function test_Equipment_And_GoldenArrowLock() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Give alice Bow (#13) and Golden Arrow (#4) and Cloak (#6)
        grantItem(alice, 13, 1); // Yew Longbow (slot 0)
        grantItem(alice, 6, 1);  // Velvet Cloak (slot 1)
        grantItem(alice, 4, 1);  // Golden Arrow (slot 2)

        // Set approval for Core vault
        vm.startPrank(alice);
        treasures.setApprovalForAll(address(hood), true);

        // Cannot equip Golden Arrow without Bow (INV-8)
        vm.expectRevert();
        hood.equipItem(id, 2, 4);

        // Equip Bow first
        hood.equipItem(id, 0, 13);
        assertEq(hood.equippedSlot(id, 0), 13);
        assertEq(treasures.balanceOf(address(hood), 13), 1);

        // Now equip Golden Arrow
        hood.equipItem(id, 2, 4);
        assertEq(hood.equippedSlot(id, 2), 4);

        // Cannot unequip Bow while Golden Arrow is equipped
        vm.expectRevert();
        hood.initiateUnequip(id, 0);

        // Initiate unequip of Golden Arrow
        hood.initiateUnequip(id, 2);

        // Cannot finalize unequip immediately (24h lock)
        vm.expectRevert();
        hood.finalizeUnequip(id, 2);

        // Warp 24 hours
        vm.warp(block.timestamp + 24 hours + 1);
        hood.finalizeUnequip(id, 2);
        assertEq(hood.equippedSlot(id, 2), 0);
        assertEq(treasures.balanceOf(alice, 4), 1);

        // Now can initiate unequip of Bow
        hood.initiateUnequip(id, 0);
        vm.warp(block.timestamp + 24 hours + 1);
        hood.finalizeUnequip(id, 0);
        assertEq(hood.equippedSlot(id, 0), 0);
        assertEq(treasures.balanceOf(alice, 13), 1);
        vm.stopPrank();
    }

    function test_Companions_Adoption_Bonding_Debonding() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Give Alice Gold for pet adoption fee (20 Gold)
        grantItem(alice, 1, 100);

        // Adopt Genesis Hound (species 0)
        vm.prank(alice);
        uint256 petId = companions.adoptGenesisPet(id, 0);
        assertEq(petId, 1);
        assertEq(companions.ownerOf(petId), alice);
        assertEq(companions.species(petId), 0);

        // Cannot adopt second genesis pet for same Hood (INV-3)
        vm.prank(alice);
        vm.expectRevert("Genesis pet already adopted for this Hood");
        companions.adoptGenesisPet(id, 0);

        // Alice bonds pet to Hood
        vm.startPrank(alice);
        companions.approve(address(hood), petId);
        hood.bondPet(id, petId);
        assertEq(hood.hoodBoundPet(id), petId);
        assertEq(hood.petBoundToHood(petId), id);
        assertEq(companions.ownerOf(petId), address(hood));

        // Cannot initiate debond during 12h initial lock
        vm.expectRevert();
        hood.initiateDebond(id);

        // Warp 12 hours
        vm.warp(block.timestamp + 12 hours + 1);
        hood.initiateDebond(id);

        // Cannot finalize debond before 12h timer matures
        vm.expectRevert();
        hood.finalizeDebond(id);

        // Warp 12 hours
        vm.warp(block.timestamp + 12 hours + 1);
        hood.finalizeDebond(id);
        assertEq(hood.hoodBoundPet(id), 0);
        assertEq(companions.ownerOf(petId), alice);
        vm.stopPrank();
    }

    function test_Bazaar_Listing_And_Purchase() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Alice lists Hood for 100 Gold (min 40 Gold)
        vm.startPrank(alice);
        hood.approve(address(bazaar), id);
        bazaar.listHero(id, 100);
        assertTrue(hood.bazaarEscrowed(id));
        assertEq(hood.ownerOf(id), address(bazaar));
        vm.stopPrank();

        // Bob buys Hood
        treasures.setModuleAuthorization(address(this), 25000, true);
        treasures.rewardExpansionGold(bob, 100);
        assertEq(treasures.balanceOf(bob, 1), 100);

        vm.startPrank(bob);
        treasures.setApprovalForAll(address(bazaar), true);
        bazaar.buyListing(id);
        assertEq(hood.ownerOf(id), bob);
        assertFalse(hood.bazaarEscrowed(id));
        vm.stopPrank();

        // Check proceeds escrow for Alice: 100 - 2.5% fee (2 Gold) = 98 Gold
        assertEq(bazaar.bazaarProceedsEscrow(alice), 98);

        // Alice withdraws proceeds
        vm.prank(alice);
        bazaar.withdrawBazaarProceeds(alice);
        assertEq(bazaar.bazaarProceedsEscrow(alice), 0);
        assertEq(treasures.balanceOf(alice, 1), 98);
    }

    function test_Heist_FullLifecycle_And_Fallback() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Request 5 heists
        vm.prank(alice);
        uint256 reqId = raids.requestHeistBatch(id, 5, alice);
        assertTrue(hood.hasPendingNormalHeist(id));
        assertEq(raids.pendingRequestsByEngine(address(raids)), 1);

        // Cannot request another heist batch while one is pending (INV-12)
        vm.prank(alice);
        vm.expectRevert("Pending heist batch already exists");
        raids.requestHeistBatch(id, 1, alice);

        // Target block not reached yet
        vm.expectRevert("Target block not reached");
        raids.resolveHeist(reqId);

        // Advance ArbSys mock block by 3 blocks (> targetBlock)
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);

        // Resolve heist
        raids.resolveHeist(reqId);
        assertFalse(hood.hasPendingNormalHeist(id));
        assertEq(raids.pendingRequestsByEngine(address(raids)), 0);

        // Active adventuring sustained upkeep for 7 days
        assertTrue(hood.activitySustainedUntil(id) >= block.timestamp + 7 days - 1);

        // Now test fallback roll when request is older than 256 blocks (INV-10)
        // Advance day to reset stamina
        vm.warp(block.timestamp + 1 days + 1);
        vm.prank(alice);
        uint256 reqId2 = raids.requestHeistBatch(id, 5, alice);

        // Advance ArbSys block by 300 blocks
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 300);

        // Resolves cleanly via fallback with zero reversions
        raids.resolveHeist(reqId2);
        assertFalse(hood.hasPendingNormalHeist(id));
    }

    function test_WorldEvent_CastleAndFinalization() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Advance to Day 28 of Month 1
        vm.warp(genesisTime + 27 days + 1 hours);
        raids.syncWorldEvents();

        uint256 castleId = 1_000_000;
        assertTrue(worldState.getEvent(castleId).exists);

        // Wake up hero after time skip
        vm.prank(alice);
        hood.dailyCare(id);

        // Alice requests Castle maneuver
        vm.prank(alice);
        uint256 reqId = raids.requestActionEvent(id, castleId, ActionKind.CASTLE, 0);

        // Advance ArbSys block
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);

        // Resolve action
        raids.resolveActionEvent(reqId);

        // Advance past event endTime + 2 hours grace period
        EventConfig memory cfg = worldState.getEvent(castleId);
        vm.warp(cfg.endTime + 2 hours + 1);

        // Authorize Raids engine in WorldState event resolver
        worldState.setEventResolverAllowed(castleId, address(raids), true);

        // Finalize event
        raids.finalizeEvent(castleId);
        (,,,, bool isFin) = raids.eventRecords(castleId);
        assertTrue(isFin);
    }

    function test_Solstice_5Maneuver_CommitReveal() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Warp to Day 359 (Solstice start)
        vm.warp(genesisTime + 358 days + 1 hours);
        raids.syncWorldEvents();

        uint256 solsticeId = 2_000_001; // Year 1
        assertTrue(worldState.getEvent(solsticeId).exists);

        // Wake up hero after time skip
        vm.prank(alice);
        hood.dailyCare(id);

        // Authorize Raids resolver
        worldState.setEventResolverAllowed(solsticeId, address(raids), true);

        // Execute maneuver 0
        bytes32 secret0 = bytes32(uint256(777));
        bytes32 secretHash0 = keccak256(abi.encode(secret0, id, 1, 0, address(raids), block.chainid));

        vm.prank(alice);
        raids.commitSolsticeManeuver(solsticeId, id, secretHash0, 0);

        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);

        // Reveal maneuver 0
        vm.prank(alice);
        raids.revealSolsticeManeuver(solsticeId, id, secret0);

        assertEq(raids.currentSolsticeManeuver(solsticeId, id), 1);
        assertTrue(worldState.solsticeRenown(solsticeId, id) >= 50);
    }

    function test_Renderer_ReturnsValidTokenURI() public {
        uint256 id = mintAndFinalizeHero(alice);

        string memory uri = hood.tokenURI(id);
        assertTrue(bytes(uri).length > 0);
    }

    function test_BatchEquip_And_Cancellations() public {
        uint256 id = mintAndFinalizeHero(alice);

        grantItem(alice, 13, 1); // Bow (slot 0)
        grantItem(alice, 6, 1);  // Velvet Cloak (slot 1)
        grantItem(alice, 4, 1);  // Golden Arrow (slot 2)

        vm.startPrank(alice);
        treasures.setApprovalForAll(address(hood), true);

        // Single-transaction batch equip
        uint8[] memory slots = new uint8[](3);
        slots[0] = 0; slots[1] = 1; slots[2] = 2;
        uint32[] memory items = new uint32[](3);
        items[0] = 13; items[1] = 6; items[2] = 4;

        hood.equipBatch(id, slots, items);

        assertEq(hood.equippedSlot(id, 0), 13);
        assertEq(hood.equippedSlot(id, 1), 6);
        assertEq(hood.equippedSlot(id, 2), 4);
        assertEq(hood.boundCount(13), 1);
        assertEq(hood.boundCount(6), 1);
        assertEq(hood.boundCount(4), 1);

        // Test unequip cancellation: initiate unequip of cloak
        hood.initiateUnequip(id, 1);
        assertEq(hood.pendingUnequipCount(id), 1);
        (bool allowed, uint256 reasonFlags) = hood.canList(id);
        assertFalse(allowed);
        assertEq(reasonFlags, 2);

        // Cancel unequip: player retains item equipped, removes lock
        hood.cancelUnequip(id, 1);
        assertEq(hood.pendingUnequipCount(id), 0);
        assertEq(hood.equippedSlot(id, 1), 6);
        (allowed, reasonFlags) = hood.canList(id);
        assertTrue(allowed);
        assertEq(reasonFlags, 0);

        vm.stopPrank();
    }

    function test_Cat_Adoption_And_Perks() public {
        uint256 id = mintAndFinalizeHero(alice);

        // Grant Alice 25 Gold Sovereigns for Cat adoption
        grantItem(alice, 1, 25);

        // Adopt Sherwood Cat (speciesChoice = 3)
        vm.prank(alice);
        uint256 catId = companions.adoptGenesisPet(id, 3);

        assertTrue(catId >= 7501 && catId <= 10000);
        assertEq(companions.species(catId), 3);
        assertEq(companions.petSpecies(catId), 3);
        assertEq(companions.ownerOf(catId), alice);
        assertEq(treasures.balanceOf(alice, 1), 0); // 25 gold burned

        // Bond Cat to Hood
        vm.startPrank(alice);
        companions.approve(address(hood), catId);
        hood.bondPet(id, catId);
        assertEq(hood.hoodBoundPet(id), catId);

        // Cancel debond test
        vm.warp(block.timestamp + 12 hours + 1);
        hood.initiateDebond(id);
        (bool allowed, uint256 flags) = hood.canList(id);
        assertFalse(allowed);
        assertEq(flags, 4);

        hood.cancelDebond(id);
        (allowed, flags) = hood.canList(id);
        assertTrue(allowed);
        assertEq(flags, 0);
        assertEq(hood.hoodBoundPet(id), catId);
        vm.stopPrank();
    }
}
