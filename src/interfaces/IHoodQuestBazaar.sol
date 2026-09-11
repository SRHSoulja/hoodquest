// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IHoodQuestBazaar {
    function expectedDeposit(uint256 tokenId) external view returns (address);
    function bazaarProceedsEscrow(address seller) external view returns (uint256);
    function withdrawBazaarProceeds() external;
    function withdrawBazaarProceeds(address recipient) external;
}
