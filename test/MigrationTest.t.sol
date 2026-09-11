// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { BaseTest } from "./BaseTest.sol";
import { HoodQuestRaids } from "../src/HoodQuestRaids.sol";
import { ActionKind, EventConfig, EventKind } from "../src/HoodQuestTypes.sol";

contract MigrationTest is BaseTest {
    HoodQuestRaids public raidsV2;

    function test_EightStep_Engine_Migration_Protocol() public {
        // Alice mints a hero
        uint256 id = mintAndFinalizeHero(alice);

        // V1 starts a normal heist and event action
        vm.prank(alice);
        uint256 heistReqV1 = raids.requestHeistBatch(id, 2, alice);
        assertEq(raids.pendingRequestsByEngine(address(raids)), 1);

        // Advance to Castle event window (Day 28 of Month 1)
        vm.warp(genesisTime + 27 days + 1 hours);
        vm.prank(alice);
        hood.dailyCare(id);
        raids.syncWorldEvents();
        uint256 castleEventId = 1_000_000;

        // --- STEP 1: Deploy & Authorize V2 Full Roles ---
        raidsV2 = new HoodQuestRaids(address(hood), address(treasures), address(worldState));
        hood.setEngineRoles(address(raidsV2), true, true, true);
        treasures.setEngineRoles(address(raidsV2), true, true, true);
        worldState.setEngineRoles(address(raidsV2), true, true, true);

        // --- STEP 2: Transfer Unfinished Event Permissions to V2 ---
        worldState.setEventResolverAllowed(castleEventId, address(raidsV2), true);

        // --- STEP 3: Revoke V1 Active Role Only ---
        hood.setEngineRoles(address(raids), false, true, true);
        treasures.setEngineRoles(address(raids), false, true, true);
        worldState.setEngineRoles(address(raids), false, true, true);

        // V1 can no longer accept new requests
        vm.prank(alice);
        vm.expectRevert("Engine not active");
        raids.requestHeistBatch(id, 1, alice);

        // --- STEP 4: V1 Resolves In-Flight Requests ---
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raids.resolveHeist(heistReqV1);
        assertEq(raids.pendingRequestsByEngine(address(raids)), 0);

        // --- STEP 5: V2 Handles New Gameplay & Finalization ---
        // V2 can process new requests
        // Wait 1 day for daily reset
        vm.warp(block.timestamp + 1 days + 1);
        vm.prank(alice);
        uint256 heistReqV2 = raidsV2.requestHeistBatch(id, 1, alice);
        assertEq(raidsV2.pendingRequestsByEngine(address(raidsV2)), 1);

        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        raidsV2.resolveHeist(heistReqV2);
        assertEq(raidsV2.pendingRequestsByEngine(address(raidsV2)), 0);

        // --- STEP 6: Revoke V1 Resolver Role (pendingRequestsByEngine == 0) ---
        hood.setEngineRoles(address(raids), false, false, true);
        treasures.setEngineRoles(address(raids), false, false, true);
        worldState.setEngineRoles(address(raids), false, false, true);

        // --- STEP 7: Retain V1 Settlement Authority while liabilities exist ---
        // Since V1 has 0 liabilities outstanding:
        assertEq(raids.outstandingEventLiabilitiesByEngine(address(raids)), 0);

        // --- STEP 8: Final V1 Deregistration ---
        hood.setEngineRoles(address(raids), false, false, false);
        treasures.setEngineRoles(address(raids), false, false, false);
        worldState.setEngineRoles(address(raids), false, false, false);

        assertFalse(hood.activeEngine(address(raids)));
        assertFalse(hood.resolverEngine(address(raids)));
        assertFalse(hood.settlementEngine(address(raids)));

        // V2 continues fully operational
        assertTrue(hood.activeEngine(address(raidsV2)));
        assertTrue(hood.resolverEngine(address(raidsV2)));
        assertTrue(hood.settlementEngine(address(raidsV2)));
    }
}
