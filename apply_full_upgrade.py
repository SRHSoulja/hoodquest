import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update generateCharacter
old_gen = """  function generateCharacter(seed) {
    const rng = xorshift(seed * 27361 + 817);
    const archIdx = (seed - 1) % ARCHETYPES.length;
    const arch = ARCHETYPES[archIdx >= 0 ? archIdx : 0];
    const name = arch.names[Math.floor(rng() * arch.names.length)];
    const cloak = CLOAK_PALETTES[Math.floor(rng() * CLOAK_PALETTES.length)];
    const compIdx = Math.floor(rng() * (COMPANIONS.length - 1)); // 0 to 3, Stag is earned
    const companion = COMPANIONS[compIdx];

    return {
      seed,
      archetype: arch,
      name,
      cloak,
      companion,
      rng
    };
  }"""

new_gen = """  function generateCharacter(seed) {
    const rng = xorshift(seed * 27361 + 817);
    const archIdx = (seed - 1) % ARCHETYPES.length;
    const arch = ARCHETYPES[archIdx >= 0 ? archIdx : 0];
    const name = arch.names[Math.floor(rng() * arch.names.length)];
    const cloak = CLOAK_PALETTES[Math.floor(rng() * CLOAK_PALETTES.length)];
    const skin = SKIN_TONES[Math.floor(rng() * SKIN_TONES.length)];
    const hair = HAIR_COLORS[Math.floor(rng() * HAIR_COLORS.length)];
    const hatColor = HAT_PALETTES[Math.floor(rng() * HAT_PALETTES.length)];
    const compIdx = Math.floor(rng() * COMPANIONS.length);
    const companion = COMPANIONS[compIdx];

    // Folklore Paper-Doll Variants: Beggar disguise & Change Cup!
    const isBeggar = (arch.id === 'friar' || arch.id === 'archer') && ((seed % 3) === 0);

    return {
      seed,
      archetype: arch,
      name,
      cloak,
      skin,
      hair,
      hatColor,
      isBeggar,
      companion,
      rng
    };
  }"""

assert old_gen in text, "old_gen not found!"
text = text.replace(old_gen, new_gen)
print("Updated generateCharacter successfully!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
