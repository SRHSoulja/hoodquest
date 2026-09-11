// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IRenderer {
    function tokenURI(uint256 tokenId) external view returns (string memory);
}
