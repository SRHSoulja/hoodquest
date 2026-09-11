// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Test } from "forge-std/Test.sol";
import { MockArbSys } from "./mocks/MockArbSys.sol";
import { HoodQuest } from "../src/HoodQuest.sol";
import { HoodQuestTreasures } from "../src/HoodQuestTreasures.sol";
import { HoodQuestCompanions } from "../src/HoodQuestCompanions.sol";
import { HoodQuestBazaar } from "../src/HoodQuestBazaar.sol";
import { HoodQuestWorldState } from "../src/HoodQuestWorldState.sol";
import { HoodQuestRaids } from "../src/HoodQuestRaids.sol";
import { HoodQuestRenderer } from "../src/HoodQuestRenderer.sol";
import {
    SupplyMode,
    MintSource,
    EventKind,
    ActionKind,
    HeistSnapshot,
    CombatSnapshot,
    RewardBundle,
    EventConfig,
    CraftRecipe
} from "../src/HoodQuestTypes.sol";

contract BaseTest is Test {
    MockArbSys public mockArbSys;
    HoodQuest public hood;
    HoodQuestTreasures public treasures;
    HoodQuestCompanions public companions;
    HoodQuestBazaar public bazaar;
    HoodQuestWorldState public worldState;
    HoodQuestRaids public raids;
    HoodQuestRenderer public renderer;

    address public timelock;
    address public guardian;
    address public proceedsRecipient;

    address public alice = address(0xA11CE);
    address public bob = address(0xB0B);
    address public charlie = address(0xCC);

    uint256 public constant MINT_PRICE = 0.01 ether;
    uint256 public genesisTime;

    function setUp() public virtual {
        vm.warp(1700000000);
        timelock = address(this);
        guardian = address(0x999);
        proceedsRecipient = address(0x888);
        genesisTime = block.timestamp;

        // Setup ArbSys precompile mock at 0x0000000000000000000000000000000000000064
        MockArbSys impl = new MockArbSys();
        vm.etch(address(0x64), address(impl).code);
        mockArbSys = MockArbSys(address(0x64));
        mockArbSys.setBlockNumber(1000);

        // Deploy Core
        hood = new HoodQuest(
            MINT_PRICE,
            proceedsRecipient,
            genesisTime,
            timelock,
            guardian
        );

        // Deploy Treasures
        treasures = new HoodQuestTreasures(timelock, address(hood));

        // Deploy Companions
        companions = new HoodQuestCompanions(timelock, address(hood), address(treasures));

        // Deploy Bazaar
        bazaar = new HoodQuestBazaar(address(hood), address(treasures));

        // Deploy WorldState
        worldState = new HoodQuestWorldState(timelock);

        // Deploy Raids
        raids = new HoodQuestRaids(address(hood), address(treasures), address(worldState));

        // Deploy Renderer
        renderer = new HoodQuestRenderer(address(hood));

        // Wire Core
        hood.setTreasuresContract(address(treasures));
        hood.setCompanionContract(address(companions));
        hood.setBazaarContract(address(bazaar));
        hood.setRenderer(address(renderer));
        hood.setEngineRoles(address(raids), true, true, true);

        // Wire Treasures
        treasures.setBazaarContract(address(bazaar));
        treasures.setCompanionContract(address(companions));
        treasures.setEngineRoles(address(raids), true, true, true);

        // Wire WorldState
        worldState.setEngineRoles(address(raids), true, true, true);

        // Fund test users
        vm.deal(alice, 100 ether);
        vm.deal(bob, 100 ether);
        vm.deal(charlie, 100 ether);
    }

    function mintAndFinalizeHero(address to) internal returns (uint256 id) {
        vm.prank(to);
        hood.mintHoods{value: MINT_PRICE}(1);
        id = hood.totalHoodsMinted();
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        hood.finalizeHeroSeed(id);
    }

    function grantItem(address to, uint256 itemId, uint256 amount) internal {
        dealERC1155(address(treasures), to, itemId, amount);
    }
}
