// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract MockArbSys {
    uint256 public blockNumber = 1000;
    mapping(uint256 => bytes32) public blockHashes;

    function setBlockNumber(uint256 _blockNumber) external {
        blockNumber = _blockNumber;
    }

    function setBlockHash(uint256 _blockNumber, bytes32 _hash) external {
        blockHashes[_blockNumber] = _hash;
    }

    function arbBlockNumber() external view returns (uint256) {
        return blockNumber;
    }

    function arbBlockHash(uint256 blockNum) external view returns (bytes32) {
        bytes32 h = blockHashes[blockNum];
        if (h == bytes32(0)) {
            return keccak256(abi.encodePacked("mock_block_hash", blockNum));
        }
        return h;
    }
}
