import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_char = text.find('function drawCharacter(c, info) {')
e_char = text.find('// --- Living Pet Companion Rendering (Artisan Vector Illustrated) ---', s_char)
assert s_char != -1 and e_char != -1, "drawCharacter bounds not found!"

pristine_artisan_draw_character = """function drawCharacter(c, info) {
    const x = 150;
    const y = 370;
    const isDormant = info.isDormant;
    const isActing = charAnim.actionTimer > 0;
    if (isActing) charAnim.actionTimer--;
    const archId = (c.archetype && c.archetype.id) || 'archer';

    ctx.save();
    ctx.translate(x, y);

    // Ground shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.35)';
    ctx.beginPath();
    ctx.ellipse(0, 0, 22, 7, 0, 0, Math.PI * 2);
    ctx.fill();

    // Locksley Velvet Cloak (Equipped Loot)
    if (equippedLoot[6] && !isDormant) {
      ctx.fillStyle = '#1b4d24';
      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(-14, -54);
      ctx.quadraticCurveTo(-24, -20, -22, 0);
      ctx.lineTo(-6, 0);
      ctx.quadraticCurveTo(-12, -22, -6, -54);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }

    // Slumber pose if dormant
    if (isDormant) {
      ctx.fillStyle = c.cloak.hex;
      ctx.beginPath();
      ctx.arc(0, -12, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#ffd0a6';
      ctx.fillRect(-6, -24, 12, 10);
      ctx.fillStyle = '#402a1d';
      ctx.font = '12px sans-serif';
      ctx.fillText('💤', 12, -30);
      ctx.restore();
      return;
    }

    const hasSilver = info.years >= 10;
    const hairHex = hasSilver ? '#a6adb5' : (c.hair ? c.hair.hex : '#7a3215');
    const hairHi = hasSilver ? '#d1d7de' : (c.hair ? c.hair.hi : '#d97736');
    const hairSh = hasSilver ? '#6b727a' : (c.hair ? c.hair.sh : '#4a1b0b');
    const beardColor = hasSilver ? '#a6adb5' : hairHex;

    const isFemale = (archId === 'infiltrator' || archId === 'herbalist');
    const skinBase = c.skin ? c.skin.base : (isFemale ? '#fde8d4' : '#f5c69b');
    const skinSh = c.skin ? c.skin.sh : (isFemale ? '#ecc195' : '#e0ab7d');
    const skinBlush = c.skin ? c.skin.blush : 'rgba(235, 87, 87, 0.35)';
    const skinLip = c.skin ? c.skin.lip : '#d96565';

    const hatHex = c.hatColor ? c.hatColor.hex : c.cloak.hex;
    const hatHi = c.hatColor ? c.hatColor.hi : c.cloak.hi;
    const hatSh = c.hatColor ? c.hatColor.sh : c.cloak.sh;

    if (isFemale) {
      // ==========================================
      // --- ARTISAN FEMALE (MAID MARIAN & MEG) ---
      // ==========================================

      // 1. Back Hair Volume (Behind torso)
      ctx.fillStyle = hairSh;
      ctx.beginPath();
      ctx.arc(0, -68, 8.5, -Math.PI * 0.95, -Math.PI * 0.05);
      ctx.quadraticCurveTo(14, -56, 13, -36);
      ctx.quadraticCurveTo(14, -22, 9, -18);
      ctx.lineTo(4, -18);
      ctx.quadraticCurveTo(8, -36, 6, -54);
      ctx.lineTo(-6, -54);
      ctx.quadraticCurveTo(-8, -36, -4, -18);
      ctx.lineTo(-9, -18);
      ctx.quadraticCurveTo(-14, -22, -13, -36);
      ctx.quadraticCurveTo(-14, -56, 0, -68);
      ctx.closePath();
      ctx.fill();

      // 2. Flowing Back Cloak
      ctx.fillStyle = c.cloak.sh;
      ctx.beginPath();
      ctx.moveTo(-10, -52); ctx.quadraticCurveTo(-18, -25, -16, 2); ctx.lineTo(16, 2); ctx.quadraticCurveTo(18, -25, 10, -52);
      ctx.closePath(); ctx.fill();

      // 3. Pleated Skirt / Gown Hem
      ctx.fillStyle = c.cloak.hex;
      ctx.beginPath();
      ctx.moveTo(-7, -34); ctx.quadraticCurveTo(-14, -15, -16, 0); ctx.lineTo(16, 0); ctx.quadraticCurveTo(14, -15, 7, -34);
      ctx.closePath(); ctx.fill();

      ctx.strokeStyle = c.cloak.sh; ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(-5, -32); ctx.quadraticCurveTo(-7, -15, -9, 0);
      ctx.moveTo(0, -32); ctx.lineTo(0, 0);
      ctx.moveTo(5, -32); ctx.quadraticCurveTo(7, -15, 9, 0);
      ctx.stroke();

      ctx.fillStyle = '#26170d';
      ctx.beginPath(); ctx.roundRect(-6, -2, 5, 4, 1); ctx.roundRect(1, -2, 5, 4, 1); ctx.fill();

      if (info.stageNum >= 3) {
        ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(-16, 0); ctx.lineTo(16, 0); ctx.stroke();
      }

      // 4. Fitted Bodice & Corset Lacing
      ctx.fillStyle = c.cloak.hi;
      ctx.beginPath();
      ctx.moveTo(-9, -52); ctx.lineTo(9, -52); ctx.lineTo(7, -34); ctx.lineTo(-7, -34);
      ctx.closePath(); ctx.fill();

      ctx.fillStyle = '#1e130b'; ctx.fillRect(-3.5, -50, 7, 16);
      ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 0.9;
      ctx.beginPath();
      ctx.moveTo(-3, -48); ctx.lineTo(3, -44); ctx.moveTo(3, -48); ctx.lineTo(-3, -44);
      ctx.moveTo(-3, -44); ctx.lineTo(3, -40); ctx.moveTo(3, -44); ctx.lineTo(-3, -40);
      ctx.moveTo(-3, -40); ctx.lineTo(3, -36); ctx.moveTo(3, -40); ctx.lineTo(-3, -36);
      ctx.stroke();

      ctx.fillStyle = '#2b170c'; ctx.fillRect(-7.5, -35, 15, 3.5);
      ctx.fillStyle = '#ffd700'; ctx.fillRect(-2, -36, 4, 5.5);

      // 5. Slender Graceful Neck
      ctx.fillStyle = skinSh; ctx.fillRect(-2.5, -60, 5, 9);

      // 6. Sculpted Oval Face
      ctx.fillStyle = skinBase;
      ctx.beginPath(); ctx.ellipse(0, -68, 6.2, 7.8, 0, 0, Math.PI * 2); ctx.fill();

      // 7. Expressive Almond Eyes & Lips
      ctx.fillStyle = '#1e130b';
      ctx.beginPath(); ctx.ellipse(-2.8, -68, 1.3, 1.8, -0.15, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(2.8, -68, 1.3, 1.8, 0.15, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#ffffff'; ctx.fillRect(-3.2, -68.8, 0.7, 0.7); ctx.fillRect(2.4, -68.8, 0.7, 0.7);

      ctx.strokeStyle = '#100a06'; ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(-4.5, -69.5); ctx.quadraticCurveTo(-2.8, -70.5, -1.2, -69);
      ctx.moveTo(1.2, -69); ctx.quadraticCurveTo(2.8, -70.5, 4.5, -69.5);
      ctx.stroke();

      ctx.fillStyle = skinBlush;
      ctx.beginPath(); ctx.ellipse(-4.2, -65, 2, 1.2, 0, 0, Math.PI * 2); ctx.ellipse(4.2, -65, 2, 1.2, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = skinLip;
      ctx.beginPath(); ctx.ellipse(0, -62.5, 1.4, 0.8, 0, 0, Math.PI * 2); ctx.fill();

      // 8. Seamless Front Hair Locks
      ctx.fillStyle = hairHex;
      ctx.beginPath();
      ctx.moveTo(0, -75);
      ctx.quadraticCurveTo(-6.5, -74, -7.5, -66);
      ctx.quadraticCurveTo(-11, -50, -9.5, -34);
      ctx.quadraticCurveTo(-11, -26, -7, -22);
      ctx.lineTo(-4, -22);
      ctx.quadraticCurveTo(-6.5, -34, -5.5, -54);
      ctx.quadraticCurveTo(-4, -64, 0, -73);
      ctx.closePath(); ctx.fill();

      ctx.beginPath();
      ctx.moveTo(0, -75);
      ctx.quadraticCurveTo(6.5, -74, 7.5, -66);
      ctx.quadraticCurveTo(11, -50, 9.5, -34);
      ctx.quadraticCurveTo(11, -26, 7, -22);
      ctx.lineTo(4, -22);
      ctx.quadraticCurveTo(6.5, -34, 5.5, -54);
      ctx.quadraticCurveTo(4, -64, 0, -73);
      ctx.closePath(); ctx.fill();

      ctx.strokeStyle = hairHi; ctx.lineWidth = 1.1;
      ctx.beginPath();
      ctx.moveTo(-1, -74); ctx.quadraticCurveTo(-8, -60, -6.5, -24);
      ctx.moveTo(1, -74); ctx.quadraticCurveTo(8, -60, 6.5, -24);
      ctx.stroke();

      if (archId === 'infiltrator') {
        // Tiara & Stiletto
        ctx.fillStyle = hatHex;
        ctx.beginPath(); ctx.ellipse(0, -74, 8, 5, 0, Math.PI, 0); ctx.fill();
        ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.arc(0, -72, 7.2, -Math.PI * 0.85, -Math.PI * 0.15); ctx.stroke();
        ctx.fillStyle = '#e74c3c';
        ctx.beginPath(); ctx.ellipse(0, -73.5, 1.3, 2, 0, 0, Math.PI * 2); ctx.fill();

        const handX = isActing ? 22 : 11;
        const handY = isActing ? -54 : -36;
        ctx.strokeStyle = c.cloak.hi; ctx.lineWidth = 3.2;
        ctx.beginPath(); ctx.moveTo(8, -50); ctx.quadraticCurveTo(12, -44, handX, handY); ctx.stroke();

        ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 2.0;
        ctx.beginPath();
        if (isActing) { ctx.moveTo(handX - 4, handY + 4); ctx.lineTo(handX + 16, handY - 14); }
        else { ctx.moveTo(handX, handY); ctx.lineTo(handX + 6, handY + 16); }
        ctx.stroke();
        ctx.fillStyle = '#ffd700'; ctx.fillRect(handX - 2, handY - 2, 4, 4);
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(handX, handY, 2.6, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'herbalist') {
        // Mother Meg
        ctx.strokeStyle = '#d8dce2'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.arc(0, -73, 7.5, -Math.PI * 0.9, -Math.PI * 0.1); ctx.stroke();
        ctx.fillStyle = '#27ae60'; ctx.fillRect(-6, -78, 3, 2); ctx.fillRect(4, -78, 3, 2);

        ctx.strokeStyle = '#4a2e18'; ctx.lineWidth = 2.8;
        ctx.beginPath(); ctx.moveTo(-12, -88); ctx.quadraticCurveTo(-14, -50, -12, 2); ctx.stroke();
        ctx.fillStyle = '#f39c12'; ctx.beginPath(); ctx.ellipse(-12, -90, 3, 5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(-12, -48, 2.8, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.roundRect(8, -48, 13, 11, 2); ctx.fill();
        ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.ellipse(14.5, -48, 5.5, 2, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(8, -43, 2.8, 0, Math.PI * 2); ctx.fill();
      }

    } else {
      // =========================================================================
      // --- ARTISAN MALE OUTLAW ANATOMY (SCULPTED NATURAL DELTOIDS & WAIST) ---
      // =========================================================================
      const isBroad = (archId === 'brawler');
      const isMonk = (archId === 'friar');
      const tunicW = isBroad ? 18 : (isMonk ? 16 : 14);

      // 1. Wool Hosen & Sculpted Ranger Riding Boots
      ctx.fillStyle = '#1a130e';
      ctx.beginPath();
      ctx.moveTo(-tunicW + 5, -28); ctx.lineTo(-1, -28); ctx.lineTo(-1, -14); ctx.lineTo(-tunicW + 4, -14);
      ctx.closePath(); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(1, -28); ctx.lineTo(tunicW - 5, -28); ctx.lineTo(tunicW - 4, -14); ctx.lineTo(1, -14);
      ctx.closePath(); ctx.fill();

      // Turned Leather Boots with Cuffs & Metal Buckles
      ctx.fillStyle = '#140d09';
      ctx.beginPath();
      ctx.moveTo(-tunicW + 4, -14); ctx.lineTo(-1.5, -14); ctx.lineTo(-1.5, 0); ctx.lineTo(-tunicW + 3, 0);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#26170e'; ctx.fillRect(-tunicW + 4, -15.5, tunicW - 4, 3);

      ctx.fillStyle = '#140d09';
      ctx.beginPath();
      ctx.moveTo(1.5, -14); ctx.lineTo(tunicW - 4, -14); ctx.lineTo(tunicW - 3, 0); ctx.lineTo(1.5, 0);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#26170e'; ctx.fillRect(1.5, -15.5, tunicW - 4, 3);

      // 2. Sculpted Natural Torso & Sloping Shoulders (NO FLAT RIGID HORIZONTAL SHELVES!)
      const robeColor = isMonk ? '#4a2e18' : c.cloak.hex;
      ctx.fillStyle = robeColor;
      ctx.beginPath();
      ctx.moveTo(-tunicW, -24); // Flared left hem
      ctx.quadraticCurveTo(-tunicW + 1, -38, -tunicW + 2, -48); // Waist to armpit
      ctx.quadraticCurveTo(-tunicW + 2, -54, -4, -58); // Sloping left shoulder to neck base!
      ctx.lineTo(4, -58); // Neck base
      ctx.quadraticCurveTo(tunicW - 2, -54, tunicW - 2, -48); // Sloping right shoulder!
      ctx.quadraticCurveTo(tunicW - 1, -38, tunicW, -24); // Right waist to hem
      ctx.lineTo(3.5, -24);
      ctx.lineTo(0, -30); // Center split
      ctx.lineTo(-3.5, -24);
      ctx.closePath();
      ctx.fill();

      // Fabric fold shading
      ctx.strokeStyle = isMonk ? '#331e0f' : c.cloak.sh;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(-tunicW + 5, -24); ctx.lineTo(-4, -46);
      ctx.moveTo(tunicW - 5, -24); ctx.lineTo(4, -46);
      ctx.stroke();

      // 3. Belt
      if (isMonk) {
        ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2.2;
        ctx.beginPath(); ctx.moveTo(-tunicW + 2, -34); ctx.lineTo(tunicW - 2, -34); ctx.stroke();
        ctx.fillStyle = '#f8fafc';
        [-4, 0, 4].forEach(kx => { ctx.beginPath(); ctx.arc(kx, -34, 2, 0, Math.PI*2); ctx.fill(); });
        ctx.beginPath(); ctx.moveTo(4, -34); ctx.lineTo(6, -20); ctx.stroke();
      } else {
        ctx.fillStyle = '#1c0f07'; ctx.fillRect(-tunicW + 2, -35, (tunicW - 2) * 2, 4.5);
        ctx.fillStyle = info.stageNum >= 3 ? '#ffd700' : '#d4af37';
        ctx.fillRect(-3, -36, 6, 6.5);
        ctx.fillStyle = '#120803'; ctx.fillRect(-1.5, -34.5, 3, 3.5);
        ctx.fillStyle = '#1c0f07'; ctx.fillRect(2, -35, 2.8, 10);
      }

      // 4. Shaded Neck with Sternocleidomastoid lines
      ctx.fillStyle = skinSh;
      const neckW = isBroad ? 8.5 : (isMonk ? 8 : 6.8);
      ctx.fillRect(-neckW/2, -61, neckW, 9);

      // 5. Cranial Dome & Jaw Sculpting (Smooth 3D head geometry!)
      ctx.fillStyle = skinBase;
      ctx.beginPath();
      if (archId === 'brawler') {
        // Little John: Strong rugged warrior jaw & head
        ctx.arc(0, -68, 8.8, -Math.PI, 0); // Skull dome
        ctx.lineTo(8.5, -64);
        ctx.quadraticCurveTo(6, -58.5, 0, -58.5);
        ctx.quadraticCurveTo(-6, -58.5, -8.5, -64);
        ctx.closePath();
      } else if (archId === 'friar') {
        // Friar Tuck: Plump rounded smiling jowls & double chin
        ctx.ellipse(0, -66.5, 8.5, 8.8, 0, 0, Math.PI * 2);
      } else if (archId === 'scout') {
        // Much the Miller: Youthful, agile ranger jaw
        ctx.arc(0, -68, 6.8, -Math.PI, 0);
        ctx.lineTo(6.5, -65);
        ctx.quadraticCurveTo(4.5, -59, 0, -59);
        ctx.quadraticCurveTo(-4.5, -59, -6.5, -65);
        ctx.closePath();
      } else if (archId === 'sheriff') {
        ctx.ellipse(0, -66, 8, 8.2, 0, 0, Math.PI * 2);
      } else {
        // Robin Hood, Alan-a-Dale, Will Scarlet, Guy: Chiseled masculine skull
        ctx.arc(0, -68.5, 7.5, -Math.PI, 0);
        ctx.lineTo(7.2, -65);
        ctx.quadraticCurveTo(5, -59, 0, -59);
        ctx.quadraticCurveTo(-5, -59, -7.2, -65);
        ctx.closePath();
      }
      ctx.fill();

      // 6. Facial Features
      ctx.fillStyle = '#1c130d';
      if (archId === 'friar') {
        // Laughing crinkled squint eyes
        ctx.strokeStyle = '#1c130d'; ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.arc(-3.4, -67.5, 2.2, -Math.PI * 0.85, -Math.PI * 0.15);
        ctx.arc(3.4, -67.5, 2.2, -Math.PI * 0.85, -Math.PI * 0.15);
        ctx.stroke();
        // Cheeks
        ctx.fillStyle = skinBlush;
        ctx.beginPath(); ctx.arc(-4.6, -63.5, 2.4, 0, Math.PI * 2); ctx.arc(4.6, -63.5, 2.4, 0, Math.PI * 2); ctx.fill();
        // Warm laughing mouth
        ctx.strokeStyle = '#1c130d'; ctx.lineWidth = 1.1;
        ctx.beginPath(); ctx.arc(0, -62.5, 3.2, 0.2, Math.PI - 0.2); ctx.stroke();
      } else if (archId === 'scout') {
        // Much: Bright hazel almond eyes & freckles
        ctx.beginPath(); ctx.ellipse(-2.8, -68, 1.4, 1.8, 0, 0, Math.PI * 2); ctx.ellipse(2.8, -68, 1.4, 1.8, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-3.3, -68.8, 0.8, 0.8); ctx.fillRect(2.3, -68.8, 0.8, 0.8);
        ctx.strokeStyle = hairSh; ctx.lineWidth = 0.9;
        ctx.beginPath(); ctx.moveTo(-4.2, -70.8); ctx.lineTo(-1.6, -70.8); ctx.moveTo(1.6, -70.8); ctx.lineTo(4.2, -70.8); ctx.stroke();
        ctx.fillStyle = 'rgba(160, 82, 45, 0.5)';
        ctx.fillRect(-4, -64.5, 0.8, 0.8); ctx.fillRect(3.5, -64.5, 0.8, 0.8);
        ctx.fillStyle = skinLip; ctx.fillRect(-1.2, -62.2, 2.4, 0.8);
      } else {
        ctx.beginPath(); ctx.ellipse(-3, -68, 1.3, 1.6, -0.08, 0, Math.PI * 2); ctx.ellipse(3, -68, 1.3, 1.6, 0.08, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-3.3, -68.7, 0.7, 0.7); ctx.fillRect(2.7, -68.7, 0.7, 0.7);
        ctx.strokeStyle = hairSh; ctx.lineWidth = (archId === 'brawler') ? 1.6 : 1.1;
        ctx.beginPath(); ctx.moveTo(-4.6, -70.5); ctx.lineTo(-1.5, -69.8); ctx.moveTo(1.5, -69.8); ctx.lineTo(4.6, -70.5); ctx.stroke();
        ctx.fillStyle = skinSh;
        ctx.beginPath(); ctx.moveTo(0, -68); ctx.lineTo(-0.8, -64.5); ctx.lineTo(0.8, -64.5); ctx.closePath(); ctx.fill();
        ctx.fillStyle = skinLip; ctx.fillRect(-1.2, -62.2, 2.4, 0.8);
      }

      // ==========================================
      // --- ARCHETYPE ARTISAN HAIR & EQUIPMENT ---
      // ==========================================

      if (archId === 'friar') {
        // --- FRIAR TUCK (SCULPTED TONSURE RING & TANKARD) ---
        // 1. Shaved Pale Scalp Crown
        ctx.fillStyle = skinBase;
        ctx.beginPath(); ctx.ellipse(0, -73, 5.8, 3.8, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.beginPath(); ctx.ellipse(1.5, -74, 2.8, 1.5, 0.2, 0, Math.PI * 2); ctx.fill();

        // 2. Curled Tonsure Ring (Wrapping snugly around ears and nape!)
        ctx.fillStyle = hairSh;
        // Left Ear & Temple Fluff
        ctx.beginPath();
        ctx.moveTo(-5.5, -73.5); ctx.quadraticCurveTo(-9.2, -72, -9.6, -66);
        ctx.quadraticCurveTo(-10.2, -60, -7.5, -59); ctx.lineTo(-5.2, -61);
        ctx.quadraticCurveTo(-8.2, -65, -5.5, -73.5); ctx.closePath(); ctx.fill();

        // Right Ear & Temple Fluff
        ctx.beginPath();
        ctx.moveTo(5.5, -73.5); ctx.quadraticCurveTo(9.2, -72, 9.6, -66);
        ctx.quadraticCurveTo(10.2, -60, 7.5, -59); ctx.lineTo(5.2, -61);
        ctx.quadraticCurveTo(8.2, -65, 5.5, -73.5); ctx.closePath(); ctx.fill();

        // Nape Hair Ring
        ctx.fillStyle = hairHex;
        ctx.beginPath();
        ctx.arc(0, -72, 8.8, -Math.PI * 0.96, -Math.PI * 0.04);
        ctx.lineTo(8.5, -66); ctx.quadraticCurveTo(0, -70, -8.5, -66); ctx.closePath(); ctx.fill();

        // Curled strand tufts
        ctx.fillStyle = hairHex;
        ctx.beginPath();
        ctx.arc(-8.5, -66, 2.5, 0, Math.PI * 2); ctx.arc(-7.5, -61, 2.2, 0, Math.PI * 2);
        ctx.arc(8.5, -66, 2.5, 0, Math.PI * 2); ctx.arc(7.5, -61, 2.2, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = hairHi; ctx.lineWidth = 1.1;
        ctx.beginPath();
        ctx.arc(-8.5, -66, 2.5, -Math.PI * 0.5, Math.PI * 0.5);
        ctx.arc(8.5, -66, 2.5, Math.PI * 0.5, -Math.PI * 0.5);
        ctx.stroke();

        // 3. Monastic Habit Cowl Hood
        ctx.fillStyle = '#3a2110';
        ctx.beginPath();
        ctx.moveTo(-11, -54); ctx.quadraticCurveTo(0, -47, 11, -54);
        ctx.lineTo(8, -61); ctx.quadraticCurveTo(0, -56, -8, -61);
        ctx.closePath(); ctx.fill();

        // 4. Carved Wooden Ale Tankard in Hand
        const mugX = isActing ? 12 : 9;
        const mugY = isActing ? -64 : -50;
        ctx.fillStyle = '#6b4323';
        ctx.beginPath(); ctx.roundRect(mugX, mugY, 14, 17, 2); ctx.fill();
        ctx.fillStyle = '#475569';
        ctx.fillRect(mugX, mugY + 3, 14, 2); ctx.fillRect(mugX, mugY + 12, 14, 2);
        ctx.strokeStyle = '#4a2a12'; ctx.lineWidth = 2.2; ctx.strokeRect(mugX + 13, mugY + 4, 4, 9);
        ctx.fillStyle = '#fffdf0';
        ctx.beginPath(); ctx.ellipse(mugX + 7, mugY - 1, 8.5, 4.5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = skinBase;
        ctx.beginPath(); ctx.arc(mugX + 14, mugY + 8, 3.2, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'brawler') {
        // --- LITTLE JOHN (SCULPTED WARRIOR BEARD & QUARTERSTAFF) ---
        // Headband & Spilling Hair
        ctx.fillStyle = hairHex;
        ctx.beginPath(); ctx.arc(0, -74, 9, -Math.PI, 0); ctx.fill();
        ctx.fillStyle = '#2b170c'; ctx.fillRect(-8.5, -74, 17, 3.5);
        ctx.fillStyle = '#94a3b8'; ctx.fillRect(-1, -73.5, 2, 2.5);

        // Hand-Sculpted Cascading Beard
        ctx.fillStyle = beardColor;
        ctx.beginPath();
        ctx.moveTo(-8.2, -65);
        ctx.quadraticCurveTo(-12, -54, -9, -38);
        ctx.quadraticCurveTo(-4, -28, 0, -28);
        ctx.quadraticCurveTo(4, -28, 9, -38);
        ctx.quadraticCurveTo(12, -54, 8.2, -65);
        ctx.closePath(); ctx.fill();

        // Beard wave highlights
        ctx.strokeStyle = hairHi; ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(-5, -60); ctx.quadraticCurveTo(-7, -45, -3, -32);
        ctx.moveTo(0, -60); ctx.lineTo(0, -30);
        ctx.moveTo(5, -60); ctx.quadraticCurveTo(7, -45, 3, -32);
        ctx.stroke();

        // Massive Oak Quarterstaff gripped in both hands
        ctx.strokeStyle = '#5a3418'; ctx.lineWidth = 4.2;
        ctx.beginPath();
        ctx.moveTo(isActing ? -4 : 8, isActing ? -86 : -84); ctx.lineTo(isActing ? 22 : 14, 2); ctx.stroke();
        ctx.fillStyle = '#64748b'; ctx.fillRect(isActing ? -6 : 6, isActing ? -86 : -84, 5, 4);

        ctx.fillStyle = skinBase;
        ctx.beginPath();
        ctx.arc(isActing ? 6 : 10, isActing ? -56 : -52, 3.5, 0, Math.PI * 2);
        ctx.arc(isActing ? 14 : 12, isActing ? -36 : -34, 3.5, 0, Math.PI * 2);
        ctx.fill();

      } else if (archId === 'archer') {
        // --- ROBIN HOOD (AUTHENTIC BYCOCKET & HAND-HELD LONGBOW) ---
        // Hair peeking from beneath hat
        ctx.fillStyle = hairHex;
        ctx.beginPath(); ctx.arc(-7.5, -67, 2.5, 0, Math.PI * 2); ctx.arc(7.5, -67, 2.5, 0, Math.PI * 2); ctx.fill();

        // Authentic Turned-Brim Bycocket Hunting Hat
        ctx.fillStyle = hatHex;
        ctx.beginPath();
        ctx.moveTo(-10, -72);
        ctx.quadraticCurveTo(-11, -82, -2, -87);
        ctx.quadraticCurveTo(8, -84, 14, -72);
        ctx.lineTo(-10, -72);
        ctx.closePath(); ctx.fill();
        ctx.strokeStyle = hatSh; ctx.lineWidth = 1.3; ctx.stroke();

        // Turned-up back brim
        ctx.fillStyle = hatHi;
        ctx.beginPath();
        ctx.moveTo(-10, -72); ctx.quadraticCurveTo(0, -74, 12, -71); ctx.lineTo(11, -69); ctx.quadraticCurveTo(0, -72, -9, -69);
        ctx.closePath(); ctx.fill();

        // Sweeping Curved Pheasant Feather
        ctx.strokeStyle = '#e11d48'; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(0, -84); ctx.quadraticCurveTo(14, -98, 23, -93); ctx.stroke();
        ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 0.9;
        ctx.beginPath(); ctx.moveTo(0, -84); ctx.quadraticCurveTo(12, -94, 20, -91); ctx.stroke();

        // Van Dyke Beard & Moustache
        ctx.fillStyle = beardColor;
        ctx.beginPath();
        ctx.moveTo(-4.5, -63.5); ctx.quadraticCurveTo(0, -62, 4.5, -63.5); ctx.quadraticCurveTo(0, -64.5, -4.5, -63.5); ctx.fill();
        ctx.beginPath(); ctx.moveTo(-2, -61); ctx.lineTo(2, -61); ctx.lineTo(0, -57.5); ctx.closePath(); ctx.fill();

        // Quiver on Back
        ctx.fillStyle = '#4a2f1b'; ctx.fillRect(-17, -62, 6.5, 26);
        const hasGoldArrow = !!equippedLoot[4];
        ctx.fillStyle = hasGoldArrow ? '#ffd700' : '#f8fafc';
        ctx.fillRect(-17, -70, 2, 9); ctx.fillRect(-14, -68, 2, 7); ctx.fillRect(-11.5, -71, 2, 10);

        // Hand-held Longbow
        const bowHandX = isActing ? 20 : 16;
        const bowHandY = isActing ? -50 : -46;
        ctx.strokeStyle = c.cloak.hi; ctx.lineWidth = 3.2;
        ctx.beginPath(); ctx.moveTo(9, -52); ctx.lineTo(bowHandX, bowHandY); ctx.stroke();
        ctx.fillStyle = '#3a2012'; ctx.fillRect(11, -50, 4.5, 6);

        const hasGildedBow = !!equippedLoot[3];
        ctx.strokeStyle = hasGildedBow ? '#ffd700' : (info.stageNum >= 4 ? '#b8860b' : '#613917');
        ctx.lineWidth = hasGildedBow ? 3.6 : 2.8;
        ctx.beginPath();
        if (isActing) {
          ctx.arc(bowHandX - 3, bowHandY, 24, -Math.PI * 0.44, Math.PI * 0.44);
          ctx.stroke();
          ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 0.9;
          ctx.beginPath();
          ctx.moveTo(bowHandX - 3 + Math.cos(-Math.PI * 0.44) * 24, bowHandY + Math.sin(-Math.PI * 0.44) * 24);
          ctx.lineTo(2, -50);
          ctx.lineTo(bowHandX - 3 + Math.cos(Math.PI * 0.44) * 24, bowHandY + Math.sin(Math.PI * 0.44) * 24);
          ctx.stroke();
          ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(2, -50, 2.5, 0, Math.PI * 2); ctx.fill();
        } else {
          ctx.arc(bowHandX, bowHandY, 22, -Math.PI * 0.35, Math.PI * 0.35);
          ctx.stroke();
          ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 0.8;
          ctx.beginPath();
          ctx.moveTo(bowHandX + Math.cos(-Math.PI * 0.35) * 22, bowHandY + Math.sin(-Math.PI * 0.35) * 22);
          ctx.lineTo(bowHandX + Math.cos(Math.PI * 0.35) * 22, bowHandY + Math.sin(Math.PI * 0.35) * 22);
          ctx.stroke();
        }
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.roundRect(bowHandX - 2.5, bowHandY - 3, 5, 6, 1.5); ctx.fill();

      } else if (archId === 'minstrel') {
        // --- ALAN-A-DALE (WAVY HAIR & LUTE) ---
        ctx.fillStyle = hatHex;
        ctx.beginPath(); ctx.ellipse(1, -76, 13, 6, 0.22, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#0284c7'; ctx.lineWidth = 2.2;
        ctx.beginPath(); ctx.moveTo(3, -77); ctx.quadraticCurveTo(16, -92, 24, -86); ctx.stroke();
        ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.arc(22, -87, 2.5, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = hairHex;
        ctx.beginPath(); ctx.moveTo(-7.5, -74); ctx.quadraticCurveTo(-11, -62, -8, -54); ctx.lineTo(-6, -56); ctx.quadraticCurveTo(-8, -64, -6, -72); ctx.closePath(); ctx.fill();

        ctx.save();
        ctx.translate(isActing ? 11 : 9, isActing ? -48 : -46);
        ctx.rotate(0.35);
        ctx.fillStyle = '#9a4f21';
        ctx.beginPath(); ctx.ellipse(0, 0, 8.5, 12, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(0, -1, 3, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#3e1d08'; ctx.lineWidth = 3.2;
        ctx.beginPath(); ctx.moveTo(0, -12); ctx.lineTo(0, -28); ctx.stroke();
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(0, -20, 2.5, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(4, 0, 2.8, 0, Math.PI * 2); ctx.fill();
        ctx.restore();

      } else if (archId === 'duelist') {
        // --- WILL SCARLET (CRIMSON DUELIST) ---
        ctx.fillStyle = '#991b1b';
        ctx.beginPath(); ctx.ellipse(0, -76, 13, 5.5, -0.15, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(-2, -78); ctx.quadraticCurveTo(12, -94, 20, -88); ctx.stroke();

        ctx.fillStyle = beardColor;
        ctx.beginPath(); ctx.moveTo(-5, -63.5); ctx.quadraticCurveTo(0, -62, 5, -63.5); ctx.quadraticCurveTo(6, -65, 7, -66); ctx.quadraticCurveTo(0, -63.5, -5, -63.5); ctx.fill();

        const swHandX = isActing ? 12 : 11;
        const swHandY = isActing ? -46 : -36;
        ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 2.4;
        ctx.beginPath();
        if (isActing) { ctx.moveTo(swHandX, swHandY); ctx.lineTo(34, -68); }
        else { ctx.moveTo(swHandX, swHandY); ctx.lineTo(22, -74); }
        ctx.stroke();
        ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 1.8;
        ctx.beginPath(); ctx.arc(swHandX, swHandY, 4.5, 0, Math.PI * 2); ctx.stroke();
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(swHandX, swHandY, 2.5, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'scout') {
        // --- MUCH THE MILLER'S SON (HANDSOME RANGER & SLINGSHOT) ---
        // Tousled hair framing face
        ctx.fillStyle = hairHex;
        ctx.beginPath(); ctx.arc(0, -74, 7.5, -Math.PI, 0); ctx.fill();
        ctx.beginPath(); ctx.moveTo(-6, -73); ctx.lineTo(-8, -67); ctx.lineTo(-4, -70); ctx.closePath(); ctx.fill();
        ctx.beginPath(); ctx.moveTo(6, -73); ctx.lineTo(8, -67); ctx.lineTo(4, -70); ctx.closePath(); ctx.fill();

        // Rolled Undyed Linen Hood (Draped back naturally!)
        ctx.fillStyle = '#e2e8f0';
        ctx.beginPath();
        ctx.moveTo(-8.5, -73); ctx.quadraticCurveTo(0, -78, 8.5, -73);
        ctx.quadraticCurveTo(10, -66, 7.5, -60);
        ctx.quadraticCurveTo(0, -63, -7.5, -60);
        ctx.closePath(); ctx.stroke();
        ctx.fillStyle = '#d1d5db';
        ctx.beginPath();
        ctx.moveTo(-8, -60); ctx.lineTo(-11, -52); ctx.lineTo(-6, -52); ctx.closePath(); ctx.fill();

        ctx.strokeStyle = '#3a2012'; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(-11, -54); ctx.lineTo(10, -32); ctx.stroke();

        const slingX = isActing ? 16 : 14;
        const slingY = isActing ? -52 : -46;
        ctx.strokeStyle = '#6e3e1a'; ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(slingX, slingY + 8); ctx.lineTo(slingX, slingY);
        ctx.lineTo(slingX - 4, slingY - 7);
        ctx.moveTo(slingX, slingY); ctx.lineTo(slingX + 4, slingY - 6);
        ctx.stroke();

        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(slingX, slingY + 4, 2.8, 0, Math.PI * 2); ctx.fill();
        const pullX = isActing ? 6 : 9;
        const pullY = isActing ? -48 : -40;
        ctx.fillStyle = '#854d0e'; ctx.beginPath(); ctx.arc(pullX, pullY, 2.8, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(pullX - 1, pullY, 2.2, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'bounty') {
        // --- GUY OF GISBORNE (STEEL HELMET & BASTARD SWORD) ---
        ctx.fillStyle = '#334155';
        ctx.beginPath(); ctx.moveTo(-12, -54); ctx.quadraticCurveTo(0, -49, 12, -54); ctx.lineTo(8, -62); ctx.quadraticCurveTo(0, -58, -8, -62); ctx.closePath(); ctx.fill();
        ctx.fillStyle = '#1e293b';
        ctx.beginPath(); ctx.arc(0, -73, 9, -Math.PI, 0); ctx.lineTo(9, -71); ctx.lineTo(-9, -71); ctx.closePath(); ctx.fill();
        ctx.fillRect(-1.2, -73, 2.4, 6);

        const swX = isActing ? 13 : 14;
        const swY = isActing ? -36 : -32;
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 3.2;
        ctx.beginPath();
        if (isActing) { ctx.moveTo(swX, swY); ctx.lineTo(16, -82); }
        else { ctx.moveTo(swX, swY); ctx.lineTo(14, -76); }
        ctx.stroke();
        ctx.fillStyle = '#0f172a'; ctx.fillRect(swX - 6, swY, 12, 2.8);
        ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(swX, swY, 3.2, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'sheriff') {
        // --- SHERIFF OF NOTTINGHAM (PURSUER) ---
        ctx.fillStyle = '#831843'; ctx.beginPath(); ctx.ellipse(0, -76, 12, 5.5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(4, -76, 2.4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.ellipse(0, -54, 13, 5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#0f172a'; ctx.fillRect(-7, -55, 1.8, 2.5); ctx.fillRect(0, -53, 1.8, 2.5); ctx.fillRect(7, -55, 1.8, 2.5);

        ctx.fillStyle = '#b45309'; ctx.beginPath(); ctx.ellipse(13, -38, 7, 8, 0.2, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.fillRect(10, -44, 6, 2.5);
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(10, -42, 3, 0, Math.PI * 2); ctx.fill();
      }
    }

    // Gold Bling
    const charGold = walletLootBalances[1] || 0;
    if (charGold >= 50 && equippedLoot[1]) {
      ctx.fillStyle = '#ffd700';
      ctx.beginPath(); ctx.moveTo(-10, -76); ctx.lineTo(-6, -86); ctx.lineTo(0, -80); ctx.lineTo(6, -86); ctx.lineTo(10, -76); ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#e74c3c'; ctx.beginPath(); ctx.arc(0, -79, 1.8, 0, Math.PI * 2); ctx.fill();
    } else if (charGold >= 10 && equippedLoot[1]) {
      const broochY = isFemale ? -53 : -48;
      ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(0, broochY, isFemale ? 2.2 : 3.2, 0, Math.PI * 2); ctx.fill();
      if (isFemale) { ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.arc(0, broochY, 1.0, 0, Math.PI * 2); ctx.fill(); }
    }

    // Legendary Golden Spirit Aura at Stage 5
    if (info.stageNum === 5) {
      const aura = ctx.createRadialGradient(0, -42, 8, 0, -42, 54);
      aura.addColorStop(0, 'rgba(187, 247, 102, 0.28)');
      aura.addColorStop(0.65, 'rgba(187, 247, 102, 0.09)');
      aura.addColorStop(1, 'rgba(187, 247, 102, 0)');
      ctx.fillStyle = aura;
      ctx.beginPath(); ctx.arc(0, -42, 54, 0, Math.PI * 2); ctx.fill();
    }

    ctx.restore();
  }

  """

text = text[:s_char] + pristine_artisan_draw_character + text[e_char:]
print("Applied true artisan vector engine to simulator.html!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
