// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import { Strings } from "@openzeppelin/contracts/utils/Strings.sol";
import { Base64 } from "@openzeppelin/contracts/utils/Base64.sol";
import { SSTORE2 } from "./utils/SSTORE2.sol";

contract HoodQuestCartridgePoC is ERC721 {
    using Strings for uint256;

    address public immutable cartridgeChunk;
    bytes32 public immutable contentHash;
    uint32 public immutable payloadSize;

    constructor(bytes memory payload) ERC721("HoodQuest Cartridge PoC", "HOODPOC") {
        require(payload.length > 0, "Empty payload");
        require(payload.length <= 24575, "Payload exceeds single chunk cap");

        contentHash = keccak256(payload);
        payloadSize = uint32(payload.length);
        cartridgeChunk = SSTORE2.write(payload);

        _mint(msg.sender, 1);
    }

    function getRawCartridge() external view returns (bytes memory) {
        bytes memory raw = SSTORE2.read(cartridgeChunk);
        require(keccak256(raw) == contentHash, "Cartridge integrity failure");
        return raw;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);

        bytes memory raw = SSTORE2.read(cartridgeChunk);
        require(keccak256(raw) == contentHash, "Cartridge integrity failure");

        string memory animationUrl = string(abi.encodePacked(
            "data:text/html;base64,",
            Base64.encode(raw)
        ));

        string memory svg = string(abi.encodePacked(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" width="100%" height="100%">',
            '<rect width="320" height="320" rx="16" fill="#09140b"/>',
            '<rect x="10" y="10" width="300" height="300" rx="12" fill="none" stroke="#284c22" stroke-width="2"/>',
            '<circle cx="160" cy="130" r="50" fill="#2f6932" stroke="#ffd700" stroke-width="2"/>',
            '<text x="160" y="210" text-anchor="middle" fill="#ffd700" font-family="sans-serif" font-size="16" font-weight="bold">HoodQuest Cartridge PoC</text>',
            '<text x="160" y="235" text-anchor="middle" fill="#94a3b8" font-family="sans-serif" font-size="12">Robinhood Chain Testnet</text>',
            '<text x="160" y="260" text-anchor="middle" fill="#88b04b" font-family="monospace" font-size="11">Token #', tokenId.toString(), '</text>',
            '</svg>'
        ));

        string memory imageUri = string(abi.encodePacked(
            "data:image/svg+xml;base64,",
            Base64.encode(bytes(svg))
        ));

        string memory json = string(abi.encodePacked(
            '{"name":"HoodQuest Cartridge PoC #', tokenId.toString(), '",',
            '"description":"Self-contained on-chain playable cartridge proof for Robinhood Chain Testnet.",',
            '"image":"', imageUri, '",',
            '"animation_url":"', animationUrl, '",',
            '"attributes":[',
            '{"trait_type":"Storage Engine","value":"SSTORE2"},',
            '{"trait_type":"Payload Bytes","value":', uint256(payloadSize).toString(), '},',
            '{"trait_type":"Content Hash","value":"', Strings.toHexString(uint256(contentHash)), '"}',
            ']}'
        ));

        return string(abi.encodePacked(
            "data:application/json;base64,",
            Base64.encode(bytes(json))
        ));
    }
}
