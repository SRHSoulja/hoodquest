// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Test } from "forge-std/Test.sol";
import { SSTORE2 } from "../src/utils/SSTORE2.sol";

contract SSTORE2Test is Test {
    function externalWrite(bytes memory data) external returns (address) {
        return SSTORE2.write(data);
    }

    function test_0BytePayload() public {
        bytes memory data = new bytes(0);
        address pointer = SSTORE2.write(data);
        assertTrue(pointer != address(0), "Pointer should be non-zero");
        bytes memory readData = SSTORE2.read(pointer);
        assertEq(readData.length, 0, "Read data length should be 0");
    }

    function test_1BytePayload() public {
        bytes memory data = hex"42";
        address pointer = SSTORE2.write(data);
        bytes memory readData = SSTORE2.read(pointer);
        assertEq(readData, data, "Read data should match written data");
    }

    function test_MaxChunkPayload() public {
        // Maximum allowed payload: 24,575 bytes (EIP-170 code size 24,576 minus 1-byte stop prefix)
        uint256 maxLen = 24575;
        bytes memory data = new bytes(maxLen);
        for (uint256 i = 0; i < maxLen; i++) {
            data[i] = bytes1(uint8((i * 31 + 7) % 256));
        }
        address pointer = SSTORE2.write(data);
        bytes memory readData = SSTORE2.read(pointer);
        assertEq(keccak256(readData), keccak256(data), "Max chunk data mismatch");
        assertEq(readData.length, maxLen, "Length mismatch at maxLen");
    }

    function test_MaxPlusOneChunkPayload() public {
        // Exceeding 24,575 bytes causes deployed code size (data + 1 byte STOP) to exceed 24,576.
        // On an EIP-170 compliant EVM, CREATE reverts with DeploymentFailed.
        // In test environments without code_size_limit enforced, verify deployed bytecode exceeds 24,576 bytes.
        uint256 overflowLen = 24576;
        bytes memory data = new bytes(overflowLen);
        try this.externalWrite(data) returns (address pointer) {
            assertGt(pointer.code.length, 24576, "Deployed code size should exceed 24,576");
        } catch (bytes memory reason) {
            assertEq(bytes4(reason), SSTORE2.DeploymentFailed.selector, "Expected DeploymentFailed");
        }
    }

    function test_LeadingStopByte() public {
        bytes memory data = hex"deadbeef";
        address pointer = SSTORE2.write(data);
        bytes memory code = pointer.code;
        // The deployed runtime bytecode should be: 1 byte of 0x00 + data
        assertEq(code.length, data.length + 1, "Deployed code length should be data.length + 1");
        assertEq(uint8(code[0]), 0x00, "First byte of runtime bytecode must be 0x00 (STOP)");
    }

    function test_ByteForByteRoundTrip() public {
        bytes memory data = bytes("HoodQuest: Outlaws of Sherwood Forest Cartridge Payload 2026");
        address pointer = SSTORE2.write(data);
        bytes memory readData = SSTORE2.read(pointer);
        assertEq(string(readData), string(data), "String round trip mismatch");
        assertEq(keccak256(readData), keccak256(data), "Hash round trip mismatch");
    }
}
