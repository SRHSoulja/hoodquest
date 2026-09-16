// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Test } from "forge-std/Test.sol";
import { Base64 } from "@openzeppelin/contracts/utils/Base64.sol";
import { HoodQuestCartridgePoC } from "../src/HoodQuestCartridgePoC.sol";
import { SSTORE2 } from "../src/utils/SSTORE2.sol";

contract HoodQuestCartridgePoCTest is Test {
    HoodQuestCartridgePoC public poc;
    bytes public sampleHtml;

    function setUp() public {
        sampleHtml = bytes(vm.readFile("prototype/cartridge_poc.html"));
        poc = new HoodQuestCartridgePoC(sampleHtml);
    }

    function test_CartridgeDeploymentAndHashes() public view {
        bytes32 expectedHash = keccak256(sampleHtml);
        assertEq(poc.contentHash(), expectedHash, "Content hash mismatch");
        assertEq(poc.payloadSize(), sampleHtml.length, "Payload size mismatch");
        assertTrue(poc.cartridgeChunk() != address(0), "Chunk address cannot be 0");
    }

    function test_GetRawCartridgeParity() public view {
        bytes memory raw = poc.getRawCartridge();
        assertEq(keccak256(raw), keccak256(sampleHtml), "Raw cartridge hash mismatch");
        assertEq(raw.length, sampleHtml.length, "Raw cartridge length mismatch");
    }

    function test_TokenUriStructureAndAnimationUrl() public view {
        string memory uri = poc.tokenURI(1);
        assertTrue(bytes(uri).length > 0, "Token URI should not be empty");

        // Prefix check for data:application/json;base64,
        bytes memory uriBytes = bytes(uri);
        bytes memory expectedPrefix = bytes("data:application/json;base64,");
        for (uint256 i = 0; i < expectedPrefix.length; i++) {
            assertEq(uriBytes[i], expectedPrefix[i], "Metadata URI prefix mismatch");
        }
    }

    function test_GasMeasurementReport() public {
        uint256 gasStart = gasleft();
        poc.tokenURI(1);
        uint256 gasUsed = gasStart - gasleft();

        emit log_named_uint("Estimated tokenURI(1) execution gas", gasUsed);
        emit log_named_uint("Raw HTML payload size (bytes)", sampleHtml.length);
        emit log_named_address("SSTORE2 Chunk Contract Address", poc.cartridgeChunk());
    }
}
