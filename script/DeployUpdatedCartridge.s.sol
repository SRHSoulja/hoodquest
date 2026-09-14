// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Script } from "forge-std/Script.sol";
import { console2 } from "forge-std/console2.sol";
import { SSTORE2 } from "../src/utils/SSTORE2.sol";
import { HoodQuestCartridge } from "../src/HoodQuestCartridge.sol";

contract DeployUpdatedCartridge is Script {
    function run() external returns (address cartridgeAddress, address[] memory chunks) {
        string memory json = vm.readFile("cache/cartridge_build.json");

        bytes32 contentHash = vm.parseJsonBytes32(json, ".contentHash");
        bytes32 compressedHash = vm.parseJsonBytes32(json, ".compressedHash");
        uint32 uncompressedSize = uint32(vm.parseJsonUint(json, ".uncompressedSize"));
        uint32 compressedSize = uint32(vm.parseJsonUint(json, ".compressedSize"));
        bytes[] memory chunkData = vm.parseJsonBytesArray(json, ".chunks");

        console2.log("=== Deploying Incremental On-Chain Cartridge Update ===");
        console2.log("Chain ID:", block.chainid);
        console2.log("Total chunks required:", chunkData.length);
        console2.log("Total uncompressed size:", uncompressedSize);
        console2.log("Total compressed size:", compressedSize);

        // Chunks 1-7 are already verified on-chain
        address[] memory chunkAddrs = new address[](chunkData.length);
        chunkAddrs[0] = 0xD7AB9Cb0B311612549b52b0F5F85184e4339aAF7;
        chunkAddrs[1] = 0x49A23e2DC995F584814eB537680ea69D4dED8De1;
        chunkAddrs[2] = 0x71dB0D5259c141b658B764B545B61812F3F3f7bB;
        chunkAddrs[3] = 0xC0E26C055b55C4e2D865E296A9F0d138e82C0326;
        chunkAddrs[4] = 0xB88972FD5e1a86a807227CE56800cb27ecF69909;
        chunkAddrs[5] = 0x9d5CCd1eEF60E4CB0e875CdDbDAe697d786ccd21;
        chunkAddrs[6] = 0xfa3e585c557B2e646586A66d29A340194B5deBA3;

        for (uint256 i = 0; i < 7; i++) {
            console2.log("  Reusing verified on-chain Chunk", i + 1, "at:", chunkAddrs[i]);
        }

        vm.startBroadcast();

        for (uint256 i = 7; i < chunkData.length; i++) {
            chunkAddrs[i] = SSTORE2.write(chunkData[i]);
            console2.log("  Deployed updated Chunk", i + 1, "at:", chunkAddrs[i]);
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
        console2.log("New HoodQuestCartridge deployed at:", cartridgeAddress);
        console2.log("Content Hash:", vm.toString(contentHash));
        console2.log("Compressed Hash:", vm.toString(compressedHash));
        console2.log("--------------------------------------------------");
    }
}
