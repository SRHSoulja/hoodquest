// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Script } from "forge-std/Script.sol";
import { console2 } from "forge-std/console2.sol";
import { SSTORE2 } from "../src/utils/SSTORE2.sol";
import { HoodQuestCartridge } from "../src/HoodQuestCartridge.sol";

contract DeployFullCartridge is Script {
    function run() external returns (address cartridgeAddress, address[] memory chunks) {
        string memory json = vm.readFile("cache/cartridge_build.json");

        bytes32 contentHash = vm.parseJsonBytes32(json, ".contentHash");
        bytes32 compressedHash = vm.parseJsonBytes32(json, ".compressedHash");
        uint32 uncompressedSize = uint32(vm.parseJsonUint(json, ".uncompressedSize"));
        uint32 compressedSize = uint32(vm.parseJsonUint(json, ".compressedSize"));
        bytes[] memory chunkData = vm.parseJsonBytesArray(json, ".chunks");

        console2.log("=== Deploying Full On-Chain Game Cartridge ===");
        console2.log("Chain ID:", block.chainid);
        console2.log("Chunks to store:", chunkData.length);
        console2.log("Total uncompressed size:", uncompressedSize);
        console2.log("Total compressed size:", compressedSize);

        vm.startBroadcast();

        address[] memory chunkAddrs = new address[](chunkData.length);
        for (uint256 i = 0; i < chunkData.length; i++) {
            chunkAddrs[i] = SSTORE2.write(chunkData[i]);
            console2.log("  SSTORE2 Chunk Contract", i + 1, "at:", chunkAddrs[i]);
        }

        HoodQuestCartridge cartridge = new HoodQuestCartridge(
            chunkAddrs,
            contentHash,
            compressedHash,
            uncompressedSize,
            compressedSize
        );

        vm.stopBroadcast();

        cartridgeAddress = address(cartridge);
        chunks = cartridge.getChunkAddresses();

        console2.log("--------------------------------------------------");
        console2.log("HoodQuestCartridge deployed at:", cartridgeAddress);
        for (uint256 i = 0; i < chunks.length; i++) {
            console2.log("  SSTORE2 Chunk Contract", i + 1, "at:", chunks[i]);
        }
        console2.log("Content Hash:", vm.toString(contentHash));
        console2.log("Compressed Hash:", vm.toString(compressedHash));
        console2.log("--------------------------------------------------");
    }
}
