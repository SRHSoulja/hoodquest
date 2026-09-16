// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Test } from "forge-std/Test.sol";
import { console2 } from "forge-std/console2.sol";
import { SSTORE2 } from "../src/utils/SSTORE2.sol";
import { HoodQuestCartridge } from "../src/HoodQuestCartridge.sol";

contract HoodQuestCartridgeTest is Test {
    HoodQuestCartridge public cartridge;
    bytes[] internal chunks;
    bytes32 public expectedContentHash;
    bytes32 public expectedCompHash;
    uint32 public expectedUncompressedSize;
    uint32 public expectedCompressedSize;

    function setUp() public {
        uint256 totalLen = 92649;
        uint256 chunkSize = 24575;
        uint256 count = (totalLen + chunkSize - 1) / chunkSize;

        for (uint256 i = 0; i < count; i++) {
            uint256 thisLen = (i == count - 1) ? (totalLen - i * chunkSize) : chunkSize;
            bytes memory chunk = new bytes(thisLen);
            for (uint256 j = 0; j < thisLen; j++) {
                chunk[j] = bytes1(uint8((j * 17 + i * 3) % 256));
            }
            chunks.push(chunk);
        }

        expectedContentHash = keccak256("Full Uncompressed HoodQuest HTML");
        expectedCompHash = keccak256("Compressed Bytes");
        expectedUncompressedSize = 366508;
        expectedCompressedSize = uint32(totalLen);

        address[] memory chunkAddrs = new address[](chunks.length);
        for (uint256 i = 0; i < chunks.length; i++) {
            chunkAddrs[i] = SSTORE2.write(chunks[i]);
        }

        cartridge = new HoodQuestCartridge(
            chunkAddrs,
            expectedContentHash,
            expectedCompHash,
            expectedUncompressedSize,
            expectedCompressedSize
        );
    }

    function test_MultiChunkDeployment() public view {
        assertEq(cartridge.chunkCount(), 4, "Should have 4 chunks");
        assertEq(cartridge.uncompressedSize(), expectedUncompressedSize);
        assertEq(cartridge.compressedSize(), expectedCompressedSize);
        assertEq(cartridge.cartridgeChunks(0).code.length, 24575 + 1); // payload + STOP byte
    }

    function test_TokenURIGasAndStructure() public view {
        uint256 gasBefore = gasleft();
        string memory uri = cartridge.tokenURI(1);
        uint256 gasUsed = gasBefore - gasleft();

        console2.log("Production tokenURI(1) execution gas:", gasUsed);
        console2.log("Total tokenURI character length:", bytes(uri).length);
        assertTrue(gasUsed < 500000, "tokenURI execution gas should be very low and fast");
        assertTrue(bytes(uri).length > 2000, "URI should be properly formatted");
    }
}
