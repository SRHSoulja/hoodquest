import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Insert Backdrop Props Box before presets-box
s_target = text.find('<!-- Quick Preset Showcase (10 Outlaw Roster) -->')
assert s_target != -1, "presets box comment not found!"

backdrop_ui = """    <!-- Sherwood Camp Backdrop & Props Simulation -->
    <div class="presets-box" style="margin-bottom: 4px; border-color: rgba(132, 204, 76, 0.4);">
      <div class="presets-title">
        <span>🌲 Sherwood Camp Backdrop & Props:</span>
        <span style="font-size:11px; color:#88b04b;">Toggle items in camp scene</span>
      </div>
      <div class="preset-chips" id="backdropChips">
        <div class="chip active" data-prop="target" id="chipPropTarget">🎯 Target</div>
        <div class="chip active" data-prop="campfire" id="chipPropCampfire">🔥 Hearth</div>
        <div class="chip active" data-prop="armoryRack" id="chipPropArmory">🛡️ Armory Rack</div>
        <div class="chip active" data-prop="alchemyBench" id="chipPropAlchemy">🧪 Alchemy Table</div>
        <div class="chip" data-prop="treasureHoard" id="chipPropTreasure">💰 Gold Chest</div>
        <div class="chip" data-prop="meadCask" id="chipPropMead">🍺 Mead Cask</div>
        <div class="chip" data-prop="feastBasket" id="chipPropBasket">🧺 Feast Basket</div>
        <div class="chip active" data-prop="campShelter" id="chipPropShelter">⛺ Shelter</div>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; padding-top:6px; border-top:1px solid #162914; font-size:11px;">
        <span id="charTraitInfo" style="color:#bbf766;">🎭 Traits: Lincoln Green Bycocket • Auburn Hair • Fair Rose Skin</span>
        <button class="pill-btn" id="btnInspectItemArt" style="background:#2a401f; color:#ffd700; border:1px solid #ffd700; cursor:pointer;">🔍 Inspect Item NFT Art</button>
      </div>
    </div>

    <!-- Quick Preset Showcase (10 Outlaw Roster) -->"""

text = text.replace('<!-- Quick Preset Showcase (10 Outlaw Roster) -->', backdrop_ui, 1)

# 2. Add Modal HTML at the bottom of the body
modal_html = """  <!-- Item Art Inspector Modal -->
  <div id="itemArtModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; backdrop-filter:blur(8px); align-items:center; justify-content:center; padding:16px;">
    <div style="background:#131c11; border:2px solid #ffd700; border-radius:14px; max-width:440px; width:100%; padding:20px; box-shadow:0 20px 50px rgba(0,0,0,0.9); position:relative;">
      <button id="btnCloseItemModal" style="position:absolute; top:12px; right:14px; background:none; border:none; color:#9cb894; font-size:20px; cursor:pointer;">✕</button>
      <h2 id="itemModalTitle" style="color:#ffd700; font-size:18px; margin-bottom:4px; display:flex; align-items:center; gap:8px;">🧪 Greenwood Elixir of Vigor</h2>
      <p id="itemModalType" style="color:#88b04b; font-size:12px; margin-bottom:12px;">ERC-1155 Loot • Token ID #5 • Consumable Alchemical Draft</p>
      
      <div style="width:100%; aspect-ratio:1.2; background:#0a1009; border-radius:10px; border:1px solid #2d4522; margin-bottom:14px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
        <canvas id="itemArtCanvas" width="360" height="300" style="width:100%; height:100%;"></canvas>
      </div>

      <div id="itemModalDesc" style="color:#d1e0ca; font-size:12px; line-height:1.5; background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; border-left:3px solid #ffd700; margin-bottom:14px;">
        Brewed by Mother Meg in the deepest hollow of the Greenwood using moonlit belladonna, wild elderberry juice, and ancient spring water. Restores vitality and protects against winter sloth.
      </div>

      <div style="display:flex; gap:6px; flex-wrap:wrap;">
        <button class="pill-btn item-sel-btn active" data-item="elixir">🧪 Elixir</button>
        <button class="pill-btn item-sel-btn" data-item="bow">🏹 Gilded Bow</button>
        <button class="pill-btn item-sel-btn" data-item="arrow">✨ Gold Arrow</button>
        <button class="pill-btn item-sel-btn" data-item="cask">🍺 Mead Cask</button>
        <button class="pill-btn item-sel-btn" data-item="gold">💰 Sovereign</button>
        <button class="pill-btn item-sel-btn" data-item="stiletto">🗡️ Stilettos</button>
      </div>
    </div>
  </div>
"""

s_end_body = text.rfind('</body>')
text = text[:s_end_body] + modal_html + text[s_end_body:]

# 3. Add JS event listeners for backdrop chips and item modal
js_code = """
  // --- Backdrop Prop Toggle Logic ---
  document.querySelectorAll('#backdropChips .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const prop = chip.getAttribute('data-prop');
      backdropProps[prop] = !backdropProps[prop];
      if (backdropProps[prop]) {
        chip.classList.add('active');
        showToast(`🌲 Enabled ${chip.innerText.trim()} in camp scene`);
      } else {
        chip.classList.remove('active');
        showToast(`🌲 Hidden ${chip.innerText.trim()} from camp scene`);
      }
    });
  });

  // --- Item Art Inspector Canvas Rendering ---
  function renderItemArt(itemKey) {
    const cvs = document.getElementById('itemArtCanvas');
    if (!cvs) return;
    const ictx = cvs.getContext('2d');
    const iw = cvs.width, ih = cvs.height;
    ictx.clearRect(0, 0, iw, ih);

    // Dark moody greenwood vignette
    const bgGrad = ictx.createRadialGradient(iw/2, ih/2, 20, iw/2, ih/2, iw*0.6);
    bgGrad.addColorStop(0, '#152412');
    bgGrad.addColorStop(1, '#080d06');
    ictx.fillStyle = bgGrad;
    ictx.fillRect(0, 0, iw, ih);

    ictx.save();
    ictx.translate(iw/2, ih/2);

    if (itemKey === 'elixir') {
      document.getElementById('itemModalTitle').innerText = '🧪 Greenwood Elixir of Vigor';
      document.getElementById('itemModalType').innerText = 'ERC-1155 Loot • Token ID #5 • Alchemical Consumable';
      document.getElementById('itemModalDesc').innerText = 'Distilled by Mother Meg beneath ancient hollow oaks. Swirling emerald effervescence grants swift recovery and woodland vigor on Robinhood Chain.';
      
      // Radiant emerald glow
      const aura = ictx.createRadialGradient(0, 0, 5, 0, 0, 80);
      aura.addColorStop(0, 'rgba(16, 185, 129, 0.45)');
      aura.addColorStop(1, 'rgba(16, 185, 129, 0)');
      ictx.fillStyle = aura;
      ictx.beginPath(); ictx.arc(0, 0, 80, 0, Math.PI*2); ictx.fill();

      // Ornate Alchemical Glass Flask
      ictx.fillStyle = 'rgba(230, 255, 245, 0.25)';
      ictx.strokeStyle = '#6ee7b7';
      ictx.lineWidth = 2.5;
      ictx.beginPath();
      ictx.moveTo(-12, -45); ictx.lineTo(12, -45); ictx.lineTo(10, -25);
      ictx.quadraticCurveTo(45, 0, 36, 45);
      ictx.quadraticCurveTo(0, 68, -36, 45);
      ictx.quadraticCurveTo(-45, 0, -10, -25);
      ictx.closePath();
      ictx.fill();
      ictx.stroke();

      // Bubbling Emerald Liquid
      ictx.fillStyle = '#10b981';
      ictx.beginPath();
      ictx.moveTo(-32, 38);
      ictx.quadraticCurveTo(0, 62, 32, 38);
      ictx.quadraticCurveTo(36, 15, 24, 0);
      ictx.quadraticCurveTo(0, -6, -24, 0);
      ictx.quadraticCurveTo(-36, 15, -32, 38);
      ictx.closePath();
      ictx.fill();

      // Rising bubbles
      ictx.fillStyle = '#a7f3d0';
      ictx.beginPath();
      ictx.arc(-10, 25, 4, 0, Math.PI*2);
      ictx.arc(12, 18, 3.5, 0, Math.PI*2);
      ictx.arc(0, 5, 2.5, 0, Math.PI*2);
      ictx.fill();

      // Golden Filigree Collar & Wax Seal
      ictx.fillStyle = '#ffd700';
      ictx.fillRect(-15, -28, 30, 6);
      ictx.fillStyle = '#831843';
      ictx.beginPath(); ictx.arc(0, -25, 7, 0, Math.PI*2); ictx.fill();
      // Crystal Stopper
      ictx.fillStyle = '#9333ea';
      ictx.fillRect(-6, -58, 12, 14);

    } else if (itemKey === 'bow') {
      document.getElementById('itemModalTitle').innerText = '🏹 Gilded Recurve Longbow';
      document.getElementById('itemModalType').innerText = 'ERC-1155 Loot • Token ID #3 • Masterwork Outlaw Weapon';
      document.getElementById('itemModalDesc').innerText = 'Carved from 100-year cured English yew, adorned with 24k gold leaf leaf-inlays and wrapped in supple doe leather. Adds +10 Marksman precision.';

      // Golden aura
      const aura = ictx.createRadialGradient(0, 0, 5, 0, 0, 90);
      aura.addColorStop(0, 'rgba(255, 215, 0, 0.35)');
      aura.addColorStop(1, 'rgba(255, 215, 0, 0)');
      ictx.fillStyle = aura;
      ictx.beginPath(); ictx.arc(0, 0, 90, 0, Math.PI*2); ictx.fill();

      // Recurve Bow Curve
      ictx.strokeStyle = '#ffd700';
      ictx.lineWidth = 6;
      ictx.beginPath();
      ictx.arc(-20, 0, 85, -Math.PI*0.35, Math.PI*0.35);
      ictx.stroke();

      ictx.strokeStyle = '#78350f';
      ictx.lineWidth = 4;
      ictx.beginPath();
      ictx.arc(-20, 0, 85, -Math.PI*0.35, Math.PI*0.35);
      ictx.stroke();

      // Bowstring
      ictx.strokeStyle = '#ffffff';
      ictx.lineWidth = 1.4;
      ictx.beginPath();
      ictx.moveTo(-20 + Math.cos(-Math.PI*0.35)*85, Math.sin(-Math.PI*0.35)*85);
      ictx.lineTo(-20 + Math.cos(Math.PI*0.35)*85, Math.sin(Math.PI*0.35)*85);
      ictx.stroke();

      // Leather grip
      ictx.fillStyle = '#27170e';
      ictx.fillRect(52, -14, 12, 28);
      ictx.fillStyle = '#ffd700';
      ictx.fillRect(54, -14, 2, 28);
      ictx.fillRect(60, -14, 2, 28);

    } else if (itemKey === 'arrow') {
      document.getElementById('itemModalTitle').innerText = '✨ Mythic Golden Arrow of Nottingham';
      document.getElementById('itemModalType').innerText = 'ERC-1155 Loot • Token ID #4 • Legendary Tournament Prize';
      document.getElementById('itemModalDesc').innerText = 'The eponymous Golden Arrow won by Robin Hood at the Sheriff’s tournament. Forged of solid aurum with enchanted fletching that never wavers.';

      ictx.rotate(-Math.PI / 4);
      // Shaft
      ictx.fillStyle = '#ffd700';
      ictx.fillRect(-90, -2.5, 180, 5);
      // Gilded Broadhead
      ictx.beginPath();
      ictx.moveTo(90, 0); ictx.lineTo(70, -12); ictx.lineTo(75, 0); ictx.lineTo(70, 12);
      ictx.closePath(); ictx.fill();
      // Phoenix Fletching
      ictx.fillStyle = '#ffffff';
      ictx.fillRect(-85, -12, 28, 6);
      ictx.fillRect(-85, 6, 28, 6);
      ictx.fillStyle = '#f59e0b';
      ictx.fillRect(-80, -10, 20, 2);
      ictx.fillRect(-80, 8, 20, 2);

    } else if (itemKey === 'cask') {
      document.getElementById('itemModalTitle').innerText = '🍺 Nottingham Royal Mead Cask';
      document.getElementById('itemModalType').innerText = 'ERC-1155 Loot • Token ID #2 • Sherwood Camp Amenity';
      document.getElementById('itemModalDesc').innerText = 'Heisted directly from the Sheriff’s private cellar. Aged heather-honey mead keeps outlaws warm and merry during cold winter slumbers.';

      // Barrel Body
      ictx.fillStyle = '#78350f';
      ictx.beginPath();
      ictx.ellipse(0, 0, 55, 68, 0, 0, Math.PI*2);
      ictx.fill();
      // Iron hoops
      ictx.strokeStyle = '#334155';
      ictx.lineWidth = 7;
      ictx.beginPath();
      ictx.moveTo(-50, -32); ictx.lineTo(50, -32);
      ictx.moveTo(-54, 0); ictx.lineTo(54, 0);
      ictx.moveTo(-50, 32); ictx.lineTo(50, 32);
      ictx.stroke();
      // Brass Spigot Tap
      ictx.fillStyle = '#ffd700';
      ictx.fillRect(45, 5, 22, 10);
      // Frothing tankard beside cask
      ictx.fillStyle = '#5c381c';
      ictx.fillRect(68, 12, 20, 24);
      ictx.fillStyle = '#ffffff';
      ictx.beginPath(); ictx.ellipse(78, 11, 12, 7, 0, 0, Math.PI*2); ictx.fill();

    } else if (itemKey === 'gold') {
      document.getElementById('itemModalTitle').innerText = '💰 Robinhood Gold Sovereign';
      document.getElementById('itemModalType').innerText = 'ERC-1155 Loot • Token ID #1 • Greenwood Standard Currency';
      document.getElementById('itemModalDesc').innerText = 'Stolen from royal tax carriages and distributed among Sherwood outlaws. Stamped with the Greenwood Oak Leaf and royal crown seal.';

      // Gold coin
      ictx.fillStyle = '#ffd700';
      ictx.beginPath(); ictx.arc(0, 0, 65, 0, Math.PI*2); ictx.fill();
      ictx.strokeStyle = '#b45309';
      ictx.lineWidth = 4;
      ictx.stroke();
      // Inner rim
      ictx.strokeStyle = '#fef08a';
      ictx.lineWidth = 2;
      ictx.beginPath(); ictx.arc(0, 0, 55, 0, Math.PI*2); ictx.stroke();
      // Embossed Oak Leaf
      ictx.fillStyle = '#b45309';
      ictx.beginPath();
      ictx.ellipse(0, 0, 22, 38, 0.2, 0, Math.PI*2);
      ictx.fill();
      ictx.fillStyle = '#ffd700';
      ictx.beginPath();
      ictx.ellipse(0, 0, 16, 32, 0.2, 0, Math.PI*2);
      ictx.fill();

    } else if (itemKey === 'stiletto') {
      document.getElementById('itemModalTitle').innerText = '🗡️ Maid Marian’s Damascus Stilettos';
      document.getElementById('itemModalType').innerText = 'Bespoke Weapon • Dual Folded Starlight Blades';
      document.getElementById('itemModalDesc').innerText = 'Concealed by Lady Marian beneath her royal court sleeves. Balanced to perfection for lightning-fast throws and silent infiltration.';

      // Left Stiletto
      ictx.save();
      ictx.translate(-24, 0);
      ictx.rotate(0.2);
      ictx.fillStyle = '#e2e8f0';
      ictx.beginPath(); ictx.moveTo(0, -65); ictx.lineTo(10, 15); ictx.lineTo(-10, 15); ictx.closePath(); ictx.fill();
      ictx.fillStyle = '#ffd700'; ictx.fillRect(-18, 15, 36, 6);
      ictx.fillStyle = '#3e2717'; ictx.fillRect(-6, 21, 12, 24);
      ictx.fillStyle = '#e74c3c'; ictx.beginPath(); ictx.arc(0, 48, 6, 0, Math.PI*2); ictx.fill();
      ictx.restore();

      // Right Stiletto
      ictx.save();
      ictx.translate(24, 0);
      ictx.rotate(-0.2);
      ictx.fillStyle = '#e2e8f0';
      ictx.beginPath(); ictx.moveTo(0, -65); ictx.lineTo(10, 15); ictx.lineTo(-10, 15); ictx.closePath(); ictx.fill();
      ictx.fillStyle = '#ffd700'; ictx.fillRect(-18, 15, 36, 6);
      ictx.fillStyle = '#3e2717'; ictx.fillRect(-6, 21, 12, 24);
      ictx.fillStyle = '#e74c3c'; ictx.beginPath(); ictx.arc(0, 48, 6, 0, Math.PI*2); ictx.fill();
      ictx.restore();
    }

    ictx.restore();
  }

  // Modal open/close listeners
  const btnInspect = document.getElementById('btnInspectItemArt');
  const itemModal = document.getElementById('itemArtModal');
  const btnCloseModal = document.getElementById('btnCloseItemModal');

  if (btnInspect && itemModal) {
    btnInspect.addEventListener('click', () => {
      itemModal.style.display = 'flex';
      renderItemArt('elixir');
    });
  }
  if (btnCloseModal && itemModal) {
    btnCloseModal.addEventListener('click', () => {
      itemModal.style.display = 'none';
    });
  }
  document.querySelectorAll('.item-sel-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.item-sel-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderItemArt(btn.getAttribute('data-item'));
    });
  });

  // Update Trait Info in HUD
  function updateTraitHUD() {
    const el = document.getElementById('charTraitInfo');
    if (!el || !currentToken) return;
    const skinName = currentToken.skin ? currentToken.skin.name : 'Fair';
    const hairName = currentToken.hair ? currentToken.hair.name : 'Auburn';
    const hatName = currentToken.hatColor ? currentToken.hatColor.name : 'Lincoln Green';
    const varText = currentToken.isBeggar ? ' • 🎭 Beggar Disguise (with Change Cup!)' : '';
    el.innerText = `🎭 Traits: ${hatName} • ${hairName} Hair • ${skinName}${varText}`;
  }

  // Hook into updateHUD
  const prevUpdateHUD = updateHUD;
  updateHUD = function() {
    prevUpdateHUD();
    updateTraitHUD();
  };
"""

# Append JS code before closing script
s_end_script = text.rfind('</script>')
text = text[:s_end_script] + js_code + text[s_end_script:]

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Added UI backdrop props, Item Art Inspector Modal, and trait feedback successfully!")
