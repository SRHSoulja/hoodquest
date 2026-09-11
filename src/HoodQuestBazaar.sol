// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { IERC721Receiver } from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import { IERC1155Receiver } from "@openzeppelin/contracts/token/ERC1155/IERC1155Receiver.sol";
import { IERC165 } from "@openzeppelin/contracts/utils/introspection/IERC165.sol";
import { ReentrancyGuard } from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import { BazaarTransferMode } from "./HoodQuestTypes.sol";
import { IHoodQuestBazaar } from "./interfaces/IHoodQuestBazaar.sol";
import { IHoodQuest } from "./interfaces/IHoodQuest.sol";
import { IHoodQuestTreasures } from "./interfaces/IHoodQuestTreasures.sol";

contract HoodQuestBazaar is ReentrancyGuard, IERC721Receiver, IERC1155Receiver, IHoodQuestBazaar {
    IHoodQuest public immutable hoodContract;
    IHoodQuestTreasures public immutable treasuresContract;

    struct Listing {
        address seller;
        uint256 price;
        bytes32 loadoutHash;
    }

    mapping(uint256 => Listing) public listings;
    mapping(address => uint256) public override bazaarProceedsEscrow;
    uint256[] public activeListingTokenIds;
    mapping(uint256 => uint256) public activeListingIndexPlusOne; // 0 = not listed
    mapping(uint256 => address) public override expectedDeposit;

    event HeroListed(uint256 indexed hoodId, address indexed seller, uint256 price, bytes32 loadoutHash);
    event ListingCancelled(uint256 indexed hoodId, address indexed seller);
    event HeroSold(uint256 indexed hoodId, address indexed seller, address indexed buyer, uint256 price, uint256 fee);
    event ProceedsWithdrawn(address indexed seller, address indexed recipient, uint256 amount);

    constructor(address hoodContract_, address treasuresContract_) {
        require(hoodContract_ != address(0), "Invalid hood contract");
        require(treasuresContract_ != address(0), "Invalid treasures contract");
        hoodContract = IHoodQuest(hoodContract_);
        treasuresContract = IHoodQuestTreasures(treasuresContract_);
    }

    function listHero(uint256 hoodId, uint256 price) external nonReentrant {
        require(price >= 40, "Minimum price 40 Gold"); // Enforces integer 2.5% protocol fee >= 1 Gold
        require(hoodContract.ownerOf(hoodId) == msg.sender, "Not owner");
        (bool allowed, ) = hoodContract.canList(hoodId);
        require(allowed, "Pre-sale check failed");
        
        bytes32 lHash = hoodContract.getLoadoutHash(hoodId);
        listings[hoodId] = Listing({
            seller: msg.sender,
            price: price,
            loadoutHash: lHash
        });
        
        activeListingTokenIds.push(hoodId);
        activeListingIndexPlusOne[hoodId] = activeListingTokenIds.length;
        
        hoodContract.setBazaarEscrowed(hoodId, true);
        
        expectedDeposit[hoodId] = msg.sender;
        hoodContract.safeTransferFrom(msg.sender, address(this), hoodId);
        delete expectedDeposit[hoodId];
        
        emit HeroListed(hoodId, msg.sender, price, lHash);
    }

    function cancelListing(uint256 hoodId) external nonReentrant {
        Listing memory l = listings[hoodId];
        require(l.seller == msg.sender, "Not seller");
        
        delete listings[hoodId];
        _removeActiveListing(hoodId);
        
        hoodContract.setBazaarEscrowed(hoodId, false);
        
        hoodContract.setBazaarTransferMode(BazaarTransferMode.CANCEL_WITHDRAWAL);
        hoodContract.safeTransferFrom(address(this), msg.sender, hoodId);
        hoodContract.setBazaarTransferMode(BazaarTransferMode.NONE);
        
        emit ListingCancelled(hoodId, msg.sender);
    }

    function buyListing(uint256 hoodId) external nonReentrant {
        Listing memory l = listings[hoodId];
        require(l.price > 0, "Not listed");
        require(msg.sender != l.seller, "Cannot buy own listing");
        
        bytes32 currentHash = hoodContract.getLoadoutHash(hoodId);
        require(currentHash == l.loadoutHash, "Loadout modified while listed");
        
        delete listings[hoodId];
        _removeActiveListing(hoodId);
        
        hoodContract.setBazaarEscrowed(hoodId, false);
        
        uint256 fee = (l.price * 250) / 10_000; // 2.5% protocol fee
        uint256 sellerProceeds = treasuresContract.settleBazaarPayment(msg.sender, l.seller, l.price, fee);
        bazaarProceedsEscrow[l.seller] += sellerProceeds;
        
        hoodContract.setBazaarTransferMode(BazaarTransferMode.SALE_PURCHASE);
        hoodContract.safeTransferFrom(address(this), msg.sender, hoodId);
        hoodContract.setBazaarTransferMode(BazaarTransferMode.NONE);
        
        emit HeroSold(hoodId, l.seller, msg.sender, l.price, fee);
    }

    function withdrawBazaarProceeds(address recipient) external nonReentrant {
        require(recipient != address(0), "Invalid recipient");
        uint256 amount = bazaarProceedsEscrow[msg.sender];
        require(amount > 0, "No proceeds");
        
        bazaarProceedsEscrow[msg.sender] = 0;
        treasuresContract.safeTransferFrom(address(this), recipient, 1, amount, "");
        emit ProceedsWithdrawn(msg.sender, recipient, amount);
    }

    function withdrawBazaarProceeds() external nonReentrant {
        uint256 amount = bazaarProceedsEscrow[msg.sender];
        require(amount > 0, "No proceeds");
        
        bazaarProceedsEscrow[msg.sender] = 0;
        treasuresContract.safeTransferFrom(address(this), msg.sender, 1, amount, "");
        emit ProceedsWithdrawn(msg.sender, msg.sender, amount);
    }

    function _removeActiveListing(uint256 hoodId) internal {
        uint256 indexPlusOne = activeListingIndexPlusOne[hoodId];
        require(indexPlusOne > 0, "Not in active listings");
        uint256 index = indexPlusOne - 1;
        uint256 lastIndex = activeListingTokenIds.length - 1;
        
        if (index != lastIndex) {
            uint256 lastTokenId = activeListingTokenIds[lastIndex];
            activeListingTokenIds[index] = lastTokenId;
            activeListingIndexPlusOne[lastTokenId] = index + 1;
        }
        
        activeListingTokenIds.pop();
        delete activeListingIndexPlusOne[hoodId];
    }

    function getActiveListings(uint256 offset, uint256 limit) external view returns (uint256[] memory tokenIds, Listing[] memory details) {
        require(limit > 0 && limit <= 100, "Limit 1..100");
        uint256 total = activeListingTokenIds.length;
        if (offset >= total) return (new uint256[](0), new Listing[](0));
        
        uint256 end = offset + limit;
        if (end > total) end = total;
        uint256 count = end - offset;
        
        tokenIds = new uint256[](count);
        details = new Listing[](count);
        for (uint256 i = 0; i < count; i++) {
            uint256 id = activeListingTokenIds[offset + i];
            tokenIds[i] = id;
            details[i] = listings[id];
        }
    }

    function onERC721Received(address, address, uint256, bytes calldata) external pure override returns (bytes4) {
        return this.onERC721Received.selector;
    }

    function onERC1155Received(address, address, uint256, uint256, bytes calldata) external pure override returns (bytes4) {
        return this.onERC1155Received.selector;
    }

    function onERC1155BatchReceived(address, address, uint256[] calldata, uint256[] calldata, bytes calldata) external pure override returns (bytes4) {
        return this.onERC1155BatchReceived.selector;
    }

    function supportsInterface(bytes4 interfaceId) external pure override returns (bool) {
        return interfaceId == type(IERC721Receiver).interfaceId ||
               interfaceId == type(IERC1155Receiver).interfaceId ||
               interfaceId == type(IERC165).interfaceId;
    }
}
