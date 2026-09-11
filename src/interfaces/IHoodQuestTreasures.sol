// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { IERC1155 } from "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import { MintSource, RewardBundle } from "../HoodQuestTypes.sol";

interface IHoodQuestTreasures is IERC1155 {
    function burnAdoptionGold(address from, uint256 amount) external;
    function mintForageMaterial(address to, uint256 itemId, uint256 amount) external;
    function burnElixir(address from, uint256 amount) external;
    function burnRationBasket(address from, uint256 amount) external;
    function settleBazaarPayment(address buyer, address seller, uint256 price, uint256 fee) external returns (uint256 sellerProceeds);
    function settleHeistRewardBundle(address recipient, RewardBundle calldata bundle) external;
    function reserveItem(uint256 itemId, MintSource source, uint256 requestedAmount) external returns (uint256 reservedAmount);
    function reserveEventTrophy(uint256 eventId, uint256 itemId, uint256 amount) external;
    function settleEventTrophy(uint256 eventId, address recipient, uint256 itemId, uint256 amount) external;
    function forfeitEventTrophy(uint256 eventId, uint256 itemId, uint256 amount) external;
    function reserveEventBudget(uint256 eventId, uint256 cap) external returns (uint256 budget);
    function mintReservedEventGold(address recipient, uint256 eventId, uint256 amount) external;
    function refundEventBudget(uint256 eventId, uint256 amount) external;
    function mintReservedTrophy(uint256 eventId, address recipient, uint256 itemId) external;
    function forfeitReservedTrophy(uint256 eventId, uint256 itemId) external;
    function cumulativeGoldBurned() external view returns (uint256);
    function rewardExpansionGold(address recipient, uint256 amount) external;
}
