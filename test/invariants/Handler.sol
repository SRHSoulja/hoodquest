// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Test } from "forge-std/Test.sol";
import { HoodQuest } from "../../src/HoodQuest.sol";
import { HoodQuestTreasures } from "../../src/HoodQuestTreasures.sol";
import { HoodQuestBazaar } from "../../src/HoodQuestBazaar.sol";
import { HoodQuestRaids } from "../../src/HoodQuestRaids.sol";
import { MockArbSys } from "../mocks/MockArbSys.sol";

contract Handler is Test {
    HoodQuest public hood;
    HoodQuestTreasures public treasures;
    HoodQuestBazaar public bazaar;
    HoodQuestRaids public raids;
    MockArbSys public mockArbSys;

    address[] public actors;
    address internal currentActor;
    uint256[] public mintedHoods;
    uint256[] public pendingHeists;

    uint256 public totalProceedsEscrowed;

    modifier useActor(uint256 actorIndex) {
        currentActor = actors[actorIndex % actors.length];
        vm.startPrank(currentActor);
        _;
        vm.stopPrank();
    }

    constructor(
        HoodQuest _hood,
        HoodQuestTreasures _treasures,
        HoodQuestBazaar _bazaar,
        HoodQuestRaids _raids,
        MockArbSys _mockArbSys
    ) {
        hood = _hood;
        treasures = _treasures;
        bazaar = _bazaar;
        raids = _raids;
        mockArbSys = _mockArbSys;

        actors.push(address(0xA11CE));
        actors.push(address(0xB0B));
        actors.push(address(0xCC));
    }

    function mintHero(uint256 actorIndex, uint8 count) external useActor(actorIndex) {
        count = uint8(bound(count, 1, 5));
        if (hood.totalHoodsMinted() + count > 10_000) return;

        uint256 cost = uint256(count) * hood.MINT_PRICE_WEI();
        vm.deal(currentActor, cost);
        hood.mintHoods{value: cost}(count);

        uint256 total = hood.totalHoodsMinted();
        mockArbSys.setBlockNumber(mockArbSys.arbBlockNumber() + 3);
        for (uint256 i = total - count + 1; i <= total; i++) {
            hood.finalizeHeroSeed(i);
            mintedHoods.push(i);
        }
    }

    function equipBow(uint256 hoodIndex) external {
        if (mintedHoods.length == 0) return;
        uint256 hoodId = mintedHoods[hoodIndex % mintedHoods.length];
        address owner = hood.ownerOf(hoodId);
        if (hood.isSlumbering(hoodId) || hood.bazaarEscrowed(hoodId)) return;

        dealERC1155(address(treasures), owner, 13, 1);
        vm.startPrank(owner);
        treasures.setApprovalForAll(address(hood), true);
        if (hood.equippedSlot(hoodId, 0) == 0) {
            try hood.equipItem(hoodId, 0, 13) {} catch {}
        }
        vm.stopPrank();
    }

    function requestHeist(uint256 hoodIndex, uint8 count) external {
        if (mintedHoods.length == 0) return;
        uint256 hoodId = mintedHoods[hoodIndex % mintedHoods.length];
        address owner = hood.ownerOf(hoodId);
        if (hood.isSlumbering(hoodId) || hood.bazaarEscrowed(hoodId) || hood.hasPendingNormalHeist(hoodId)) return;

        count = uint8(bound(count, 1, 3));
        vm.startPrank(owner);
        try raids.requestHeistBatch(hoodId, count, owner) returns (uint256 reqId) {
            pendingHeists.push(reqId);
        } catch {}
        vm.stopPrank();
    }

    function resolvePendingHeist(uint256 heistIndex) external {
        if (pendingHeists.length == 0) return;
        uint256 reqId = pendingHeists[heistIndex % pendingHeists.length];
        (,,uint256 target,,,,,,) = raids.heistRequests(reqId);
        if (target == 0) return;

        mockArbSys.setBlockNumber(target + 1);
        try raids.resolveHeist(reqId) {} catch {}
    }

    function listHeroOnBazaar(uint256 hoodIndex, uint256 price) external {
        if (mintedHoods.length == 0) return;
        uint256 hoodId = mintedHoods[hoodIndex % mintedHoods.length];
        address owner = hood.ownerOf(hoodId);
        if (hood.isSlumbering(hoodId) || hood.bazaarEscrowed(hoodId)) return;
        if (hood.pendingGameplayCount(hoodId) > 0) return;

        price = bound(price, 40, 1000);
        vm.startPrank(owner);
        hood.approve(address(bazaar), hoodId);
        try bazaar.listHero(hoodId, price) {} catch {}
        vm.stopPrank();
    }

    function buyHeroOnBazaar(uint256 hoodIndex, uint256 buyerIndex) external {
        if (mintedHoods.length == 0) return;
        uint256 hoodId = mintedHoods[hoodIndex % mintedHoods.length];
        if (!hood.bazaarEscrowed(hoodId)) return;

        (, uint256 price, ) = bazaar.listings(hoodId);
        if (price == 0) return;

        address buyer = actors[buyerIndex % actors.length];
        dealERC1155(address(treasures), buyer, 1, price);

        vm.startPrank(buyer);
        treasures.setApprovalForAll(address(bazaar), true);
        try bazaar.buyListing(hoodId) {
            uint256 fee = (price * 250) / 10_000;
            totalProceedsEscrowed += (price - fee);
        } catch {}
        vm.stopPrank();
    }

    function claimBazaarProceeds(uint256 actorIndex) external useActor(actorIndex) {
        uint256 claimable = bazaar.bazaarProceedsEscrow(currentActor);
        if (claimable > 0) {
            try bazaar.withdrawBazaarProceeds() {
                totalProceedsEscrowed -= claimable;
            } catch {}
        }
    }
}
