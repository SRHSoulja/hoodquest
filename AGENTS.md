# HoodQuest — Agent Boundaries & Repository Ownership

## Ownership Scope

### OWNS:
- HoodQuest smart contracts (`src/HoodQuest*.sol`)
- HoodQuest gameplay mechanics, game loop, renderer, and audio
- HoodQuest chain-resident cartridge payload and build scripts (`build_cartridge.py`, `prototype/`)
- HoodQuest art, companions, items, and assets
- HoodQuest integration adapter with Console Runtime

Console platform changes belong in `../cartridge-console`.

---

## Repository Visibility & Disclosure Policy
- **Visibility**: **PUBLIC**
- **Role**: Open-source on-chain RPG application and reference Cartridge #0001.
- **Boundaries**:
  * Platform contracts, host, and runtime belong in `../cartridge-console`.
  * MARKS/TARGETS (`../marks-targets`) is private / surprise-sensitive; never copy private mechanics or details here.
- **Invariance Guarantee**: HoodQuest cartridge chunks 1–7 must remain 100% bit-for-bit invariant with deployed testnet bytecode.
