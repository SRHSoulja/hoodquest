import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix .chip selector for presets
old_chip_sel = """  // Presets & Random Mint
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      e.target.classList.add('active');
      setSeed(parseInt(e.target.dataset.seed, 10));
    });
  });"""

new_chip_sel = """  // Presets & Random Mint
  document.querySelectorAll('.preset-chips .chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const seed = parseInt(chip.getAttribute('data-seed'), 10);
      if (!isNaN(seed)) setSeed(seed);
    });
  });"""

assert old_chip_sel in text, "old_chip_sel not found!"
text = text.replace(old_chip_sel, new_chip_sel)
print("Fixed preset chips selector!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
