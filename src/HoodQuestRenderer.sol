// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Strings } from "@openzeppelin/contracts/utils/Strings.sol";
import { Base64 } from "@openzeppelin/contracts/utils/Base64.sol";
import { IRenderer } from "./interfaces/IRenderer.sol";
import { IHoodQuest } from "./interfaces/IHoodQuest.sol";

contract HoodQuestRenderer is IRenderer {
    using Strings for uint256;

    IHoodQuest public immutable hoodContract;

    constructor(address _hood) {
        require(_hood != address(0), "Invalid Hood address");
        hoodContract = IHoodQuest(_hood);
    }

    function _archetypeName(uint8 archetype) internal pure returns (string memory) {
        if (archetype == 0) return "Robin Hood";
        if (archetype == 1) return "Maid Marian";
        if (archetype == 2) return "Little John";
        if (archetype == 3) return "Friar Tuck";
        return "Much the Miller's Son";
    }

    function _archetypeColor(uint8 archetype) internal pure returns (string memory) {
        if (archetype == 0) return "#2d5a27"; // Forest Green
        if (archetype == 1) return "#2b4c7e"; // Sapphire/Teal
        if (archetype == 2) return "#5c3a21"; // Oak Brown
        if (archetype == 3) return "#735c32"; // Burlap Brown
        return "#4a5d4e";                     // Muted Sage
    }

    function tokenURI(uint256 tokenId) external view override returns (string memory) {
        uint8 archetype = hoodContract.heroArchetype(tokenId);
        uint256 age = hoodContract.effectiveBiologicalAge(tokenId);
        bool slumbering = hoodContract.isSlumbering(tokenId);
        bytes32 seed = hoodContract.heroSeed(tokenId);
        string memory aName = _archetypeName(archetype);
        string memory aColor = _archetypeColor(archetype);

        string memory svg = string(abi.encodePacked(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">',
            '<defs><radialGradient id="bg" cx="50%" cy="50%" r="70%"><stop offset="0%" stop-color="#1a2f1c"/><stop offset="100%" stop-color="#081009"/></radialGradient></defs>',
            '<rect width="400" height="400" rx="16" fill="url(#bg)"/>',
            '<rect x="12" y="12" width="376" height="376" rx="12" fill="none" stroke="#d4af37" stroke-width="2" stroke-opacity="0.8"/>',
            '<circle cx="200" cy="170" r="75" fill="', aColor, '" stroke="#d4af37" stroke-width="3"/>',
            '<text x="200" y="290" text-anchor="middle" fill="#d4af37" font-family="sans-serif" font-size="20" font-weight="bold">', aName, '</text>',
            '<text x="200" y="320" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="14">Age ', age.toString(), ' - ', slumbering ? 'Slumbering' : 'Awake', '</text>',
            '<text x="200" y="350" text-anchor="middle" fill="#888888" font-family="sans-serif" font-size="12">Hood #', tokenId.toString(), '</text>',
            '</svg>'
        ));

        string memory imageUri = string(abi.encodePacked(
            "data:image/svg+xml;base64,",
            Base64.encode(bytes(svg))
        ));

        string memory json = string(abi.encodePacked(
            '{"name": "', aName, ' #', tokenId.toString(), '",',
            '"description": "HoodQuest Outlaw of Sherwood Forest.",',
            '"image": "', imageUri, '",',
            '"attributes": [',
            '{"trait_type": "Archetype", "value": "', aName, '"},',
            '{"trait_type": "Biological Age", "value": ', age.toString(), '},',
            '{"trait_type": "State", "value": "', slumbering ? 'Slumbering' : 'Awake', '"},',
            '{"trait_type": "Seed", "value": "', Strings.toHexString(uint256(seed)), '"}',
            ']}'
        ));

        return string(abi.encodePacked(
            "data:application/json;base64,",
            Base64.encode(bytes(json))
        ));
    }
}
