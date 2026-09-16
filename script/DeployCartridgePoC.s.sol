// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Script } from "forge-std/Script.sol";
import { console2 } from "forge-std/console2.sol";
import { HoodQuestCartridgePoC } from "../src/HoodQuestCartridgePoC.sol";

contract DeployCartridgePoC is Script {
    function run() external returns (address cartridgeAddress, address pointerAddress) {
        // Read uncompressed prototype cartridge HTML
        string memory html = vm.readFile("prototype/cartridge_poc.html");
        bytes memory htmlBytes = bytes(html);

        console2.log("Deploying Cartridge PoC to Chain ID:", block.chainid);
        console2.log("Raw HTML size:", htmlBytes.length, "bytes");

        vm.startBroadcast();

        HoodQuestCartridgePoC cartridge = new HoodQuestCartridgePoC(htmlBytes);

        vm.stopBroadcast();

        cartridgeAddress = address(cartridge);
        pointerAddress = cartridge.cartridgeChunk();

        console2.log("--------------------------------------------------");
        console2.log("HoodQuestCartridgePoC deployed at:", cartridgeAddress);
        console2.log("SSTORE2 Cartridge Pointer at:", pointerAddress);
        console2.log("Expected Content Hash:", vm.toString(cartridge.contentHash()));
        console2.log("Raw Size Reported:", cartridge.payloadSize());
        console2.log("--------------------------------------------------");
    }
}
