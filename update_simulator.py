import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Trait Palettes and Backdrop State
old_palettes = """  const CLOAK_PALETTES = [
    { name: 'Lincoln Green', hex: '#2f6932', hi: '#489f4d', sh: '#1c421e' },
    { name: 'Autumn Russet', hex: '#944b25', hi: '#c76633', sh: '#592911' },
    { name: 'Midnight Charcoal', hex: '#293545', hi: '#425570', sh: '#161e29' },
    { name: 'Sherwood Moss', hex: '#44662d', hi: '#699943', sh: '#253d16' },
    { name: 'Crimson Scarlet', hex: '#8a2323', hi: '#bd3333', sh: '#521414' },
    { name: 'Royal Velvet', hex: '#5b264e', hi: '#8c3b77', sh: '#33122b' }
  ];"""

new_palettes = """  const CLOAK_PALETTES = [
    { name: 'Lincoln Green', hex: '#2f6932', hi: '#489f4d', sh: '#1c421e' },
    { name: 'Autumn Russet', hex: '#944b25', hi: '#c76633', sh: '#592911' },
    { name: 'Midnight Charcoal', hex: '#293545', hi: '#425570', sh: '#161e29' },
    { name: 'Sherwood Moss', hex: '#44662d', hi: '#699943', sh: '#253d16' },
    { name: 'Crimson Scarlet', hex: '#8a2323', hi: '#bd3333', sh: '#521414' },
    { name: 'Royal Velvet', hex: '#5b264e', hi: '#8c3b77', sh: '#33122b' }
  ];

  const HAIR_COLORS = [
    { name: 'Auburn', hex: '#7a3215', hi: '#d97736', sh: '#4a1b0b' },
    { name: 'Chestnut Brown', hex: '#4a2f1b', hi: '#82522c', sh: '#2b1a0e' },
    { name: 'Raven Black', hex: '#1e1b18', hi: '#3d3835', sh: '#0d0c0a' },
    { name: 'Golden Flaxen', hex: '#b5893e', hi: '#e0b25e', sh: '#73541f' },
    { name: 'Forest Copper', hex: '#963c1a', hi: '#c95828', sh: '#5c220c' },
    { name: 'Silver Gray', hex: '#8a949e', hi: '#c2cbd4', sh: '#525c66' }
  ];

  const SKIN_TONES = [
    { name: 'Fair Rose', base: '#fde8d4', sh: '#ecc195', blush: 'rgba(235, 87, 87, 0.35)', lip: '#d96565' },
    { name: 'Warm Peach', base: '#fbd3b6', sh: '#dfa87e', blush: 'rgba(220, 80, 80, 0.32)', lip: '#c95b5b' },
    { name: 'Olive Tan', base: '#e4b48b', sh: '#be895b', blush: 'rgba(195, 75, 75, 0.30)', lip: '#b75353' },
    { name: 'Weathered Bronze', base: '#c78c58', sh: '#996538', blush: 'rgba(175, 65, 65, 0.28)', lip: '#a64d4d' },
    { name: 'Deep Umber', base: '#8d5538', sh: '#663820', blush: 'rgba(140, 50, 50, 0.25)', lip: '#7a3838' }
  ];

  const HAT_PALETTES = [
    { name: 'Lincoln Green', hex: '#2f6932', hi: '#489f4d', sh: '#1c421e' },
    { name: 'Royal Burgundy', hex: '#831843', hi: '#be185d', sh: '#500724' },
    { name: 'Midnight Charcoal', hex: '#1e293b', hi: '#334155', sh: '#0f172a' },
    { name: 'Autumn Russet', hex: '#944b25', hi: '#c76633', sh: '#592911' },
    { name: 'Tawny Gold', hex: '#b45309', hi: '#d97706', sh: '#78350f' }
  ];

  const backdropProps = {
    target: true,
    campfire: true,
    armoryRack: true,
    alchemyBench: true,
    treasureHoard: false,
    meadCask: false,
    feastBasket: false,
    campShelter: true
  };"""

assert old_palettes in content, "old_palettes not found!"
content = content.replace(old_palettes, new_palettes)
print("Replaced palettes successfully!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
