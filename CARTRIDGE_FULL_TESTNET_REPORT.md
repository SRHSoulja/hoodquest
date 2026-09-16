# HoodQuest Full On-Chain Cartridge: Testnet Deployment & Verification Report

**Target Network:** Robinhood Chain Testnet (Chain ID: `46630`)  
**Latest Deployment Date:** September 14, 2026 (Run `1789411728208`)  
**Status:** FULL GAME LIVE & CONFIRMED ON-CHAIN (V2 Incremental Release)

---

## 1. Milestone Overview

The full interactive HoodQuest game engine (822 KB of game logic, archery physics, Nottingham Castle vault heists, Mother Meg's Animal Sanctuary, retro title screen, inventory, sound synthesizer, and dynamic camp diorama) has been compressed, chunked into 10 SSTORE2 bytecode contracts, and deployed to **Robinhood Chain Testnet**.

When the NFT is viewed in **Blockscout** or any Web3 marketplace, the browser:
1. Receives the on-chain loader inside `animation_url` with embedded sandboxed iframe storage polyfills (`localStorage` and `sessionStorage`).
2. Reads the 10 bytecode chunks directly from Robinhood Chain Testnet via standard `eth_getCode` with 3x retry resilience.
3. Concatenates the 223 KB compressed payload and inflates it using the browser's native `DecompressionStream('deflate')`.
4. Executes and mounts the complete 822 KB game engine inside the sandbox iframe with **zero external web servers**.

---

## 2. Latest V2 On-Chain Contracts & Transactions (Chain ID `46630`)

| Contract / Asset | Address | Explorer Link |
| :--- | :--- | :--- |
| **Main Cartridge Contract (V2 Latest)** | `0x14b7f29a9f67133b8837e6fa76ec0b071a6f18a9` | [`View Contract`](https://explorer.testnet.chain.robinhood.com/address/0x14b7f29a9f67133b8837e6fa76ec0b071a6f18a9) |
| **SSTORE2 Chunk 1 (24,575 B)** | `0xD7AB9Cb0B311612549b52b0F5F85184e4339aAF7` | [`View Chunk 1`](https://explorer.testnet.chain.robinhood.com/address/0xD7AB9Cb0B311612549b52b0F5F85184e4339aAF7) |
| **SSTORE2 Chunk 2 (24,575 B)** | `0x49A23e2DC995F584814eB537680ea69D4dED8De1` | [`View Chunk 2`](https://explorer.testnet.chain.robinhood.com/address/0x49A23e2DC995F584814eB537680ea69D4dED8De1) |
| **SSTORE2 Chunk 3 (24,575 B)** | `0x71dB0D5259c141b658B764B545B61812F3F3f7bB` | [`View Chunk 3`](https://explorer.testnet.chain.robinhood.com/address/0x71dB0D5259c141b658B764B545B61812F3F3f7bB) |
| **SSTORE2 Chunk 4 (24,575 B)** | `0xC0E26C055b55C4e2D865E296A9F0d138e82C0326` | [`View Chunk 4`](https://explorer.testnet.chain.robinhood.com/address/0xC0E26C055b55C4e2D865E296A9F0d138e82C0326) |
| **SSTORE2 Chunk 5 (24,575 B)** | `0xB88972FD5e1a86a807227CE56800cb27ecF69909` | [`View Chunk 5`](https://explorer.testnet.chain.robinhood.com/address/0xB88972FD5e1a86a807227CE56800cb27ecF69909) |
| **SSTORE2 Chunk 6 (24,575 B)** | `0x9d5CCd1eEF60E4CB0e875CdDbDAe697d786ccd21` | [`View Chunk 6`](https://explorer.testnet.chain.robinhood.com/address/0x9d5CCd1eEF60E4CB0e875CdDbDAe697d786ccd21) |
| **SSTORE2 Chunk 7 (24,575 B)** | `0xfa3e585c557B2e646586A66d29A340194B5deBA3` | [`View Chunk 7`](https://explorer.testnet.chain.robinhood.com/address/0xfa3e585c557B2e646586A66d29A340194B5deBA3) |
| **SSTORE2 Chunk 8 (24,575 B)** | `0xc3de7917dd6ccf91735b58c1a57f4c10e28be772` | [`View Chunk 8`](https://explorer.testnet.chain.robinhood.com/address/0xc3de7917dd6ccf91735b58c1a57f4c10e28be772) |
| **SSTORE2 Chunk 9 (24,575 B)** | `0x4c7a4524da56e2d4df3216fd35dfb243a4dc1d2b` | [`View Chunk 9`](https://explorer.testnet.chain.robinhood.com/address/0x4c7a4524da56e2d4df3216fd35dfb243a4dc1d2b) |
| **SSTORE2 Chunk 10 (2,138 B)** | `0x77a617f762e181a5d8a8d2aefaf296f5bd02478a` | [`View Chunk 10`](https://explorer.testnet.chain.robinhood.com/address/0x77a617f762e181a5d8a8d2aefaf296f5bd02478a) |

---

## 3. Payload & Gas Efficiency

- **Uncompressed Game Size:** `822,470` bytes (HTML, CSS, Archery & Heist Logic, Audio Synthesizer, Sanctuary, Retro Title Screen, Camp Diorama).
- **Compressed Bytecode Size:** `223,313` bytes (Deflate compressed, 72.8% reduction).
- **Chunk Count:** Exactly 10 SSTORE2 chunk contracts (all <= 24,575 bytes, strict EIP-170 compliance).
- **Native Decompression:** 0 external JS libraries; decompressed via browser C++ engine in ~20ms.

---

## 4. Live Blockscout Explorer Links

* 🎮 **Token #1 Live Interactive NFT (V2 Latest):**  
  [https://explorer.testnet.chain.robinhood.com/token/0x14b7f29a9f67133b8837e6fa76ec0b071a6f18a9/instance/1](https://explorer.testnet.chain.robinhood.com/token/0x14b7f29a9f67133b8837e6fa76ec0b071a6f18a9/instance/1)

* 📜 **V2 Cartridge Contract:**  
  [https://explorer.testnet.chain.robinhood.com/address/0x14b7f29a9f67133b8837e6fa76ec0b071a6f18a9](https://explorer.testnet.chain.robinhood.com/address/0x14b7f29a9f67133b8837e6fa76ec0b071a6f18a9)

---

## 5. Historical V1 Deployment (September 13, 2026)

- **V1 Contract Address:** `0x2E0F06fDe0551E784252eF1d303FbE68008a803d` (4-chunk initial release, 368 KB).
