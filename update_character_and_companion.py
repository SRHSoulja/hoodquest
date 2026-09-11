import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_char = text.find('function drawCharacter(c, info) {')
e_char = text.find('// --- Living Pet Companion Rendering (Artisan Vector Illustrated) ---', s_char)
assert s_char != -1 and e_char != -1, "drawCharacter bounds not found!"

new_char = """function drawCharacter(c, info) {
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

    // 6. Locksley Velvet Cloak (Equipped Loot)
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

    // Sleeping / Slumber pose if dormant
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
      // --- ARTISAN FEMALE ANATOMY (Maid Marian & Mother Meg) ---

      // 1. BACK HAIR VOLUME (Drawn behind body for seamless 360 layering!)
      ctx.fillStyle = hairSh;
      ctx.beginPath();
      // Smooth cranial dome connecting behind the neck and over shoulders
      ctx.arc(0, -69, 8.5, -Math.PI * 0.95, -Math.PI * 0.05);
      ctx.quadraticCurveTo(14, -58, 13, -38);
      ctx.quadraticCurveTo(14, -24, 9, -20);
      ctx.lineTo(4, -20);
      ctx.quadraticCurveTo(8, -38, 6, -56);
      ctx.lineTo(-6, -56);
      ctx.quadraticCurveTo(-8, -38, -4, -20);
      ctx.lineTo(-9, -20);
      ctx.quadraticCurveTo(-14, -24, -13, -38);
      ctx.quadraticCurveTo(-14, -58, 0, -69);
      ctx.closePath();
      ctx.fill();

      // 2. Flowing Back Cloak / Capelet
      ctx.fillStyle = c.cloak.sh;
      ctx.beginPath();
      ctx.moveTo(-10, -52);
      ctx.quadraticCurveTo(-18, -25, -16, 2);
      ctx.lineTo(16, 2);
      ctx.quadraticCurveTo(18, -25, 10, -52);
      ctx.closePath();
      ctx.fill();

      // 3. Elegant Pleated Skirt / Gown Hem
      ctx.fillStyle = c.cloak.hex;
      ctx.beginPath();
      ctx.moveTo(-7, -34);
      ctx.quadraticCurveTo(-14, -15, -16, 0);
      ctx.lineTo(16, 0);
      ctx.quadraticCurveTo(14, -15, 7, -34);
      ctx.closePath();
      ctx.fill();

      // Skirt Pleat Shadows
      ctx.strokeStyle = c.cloak.sh;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(-5, -32); ctx.quadraticCurveTo(-7, -15, -9, 0);
      ctx.moveTo(0, -32); ctx.lineTo(0, 0);
      ctx.moveTo(5, -32); ctx.quadraticCurveTo(7, -15, 9, 0);
      ctx.stroke();

      // Delicate Leather Riding Boots
      ctx.fillStyle = '#26170d';
      ctx.beginPath();
      ctx.roundRect(-6, -2, 5, 4, 1);
      ctx.roundRect(1, -2, 5, 4, 1);
      ctx.fill();

      // Gilded Hem Trim (Veterans & Legends)
      if (info.stageNum >= 3) {
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(-16, 0); ctx.lineTo(16, 0); ctx.stroke();
      }

      // 4. Fitted Bodice & Velvet Corset
      ctx.fillStyle = c.cloak.hi;
      ctx.beginPath();
      ctx.moveTo(-9, -52); ctx.lineTo(9, -52); ctx.lineTo(7, -34); ctx.lineTo(-7, -34);
      ctx.closePath();
      ctx.fill();

      // Corset Front Panel with Gold Criss-Cross Lacing
      ctx.fillStyle = '#1e130b';
      ctx.fillRect(-3.5, -50, 7, 16);
      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 0.9;
      ctx.beginPath();
      ctx.moveTo(-3, -48); ctx.lineTo(3, -44);
      ctx.moveTo(3, -48); ctx.lineTo(-3, -44);
      ctx.moveTo(-3, -44); ctx.lineTo(3, -40);
      ctx.moveTo(3, -44); ctx.lineTo(-3, -40);
      ctx.moveTo(-3, -40); ctx.lineTo(3, -36);
      ctx.moveTo(3, -40); ctx.lineTo(-3, -36);
      ctx.stroke();

      // Woven Leather Belt with Brass/Gold Buckle
      ctx.fillStyle = '#2b170c';
      ctx.fillRect(-7.5, -35, 15, 3.5);
      ctx.fillStyle = '#ffd700';
      ctx.fillRect(-2, -36, 4, 5.5);
      ctx.fillStyle = '#1e130b';
      ctx.fillRect(-1, -35, 2, 3.5);

      // 5. Slender Graceful Neck
      ctx.fillStyle = skinSh;
      ctx.fillRect(-2.5, -60, 5, 9);

      // 6. Refined Oval Face (Delicate Contours in active skin tone)
      ctx.fillStyle = skinBase;
      ctx.beginPath();
      ctx.ellipse(0, -68, 6.2, 7.8, 0, 0, Math.PI * 2);
      ctx.fill();

      // 7. Expressive Almond Eyes & Eyelashes
      ctx.fillStyle = '#1e130b';
      ctx.beginPath(); ctx.ellipse(-2.8, -68, 1.3, 1.8, -0.15, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(2.8, -68, 1.3, 1.8, 0.15, 0, Math.PI * 2); ctx.fill();
      // Corneal light gleams
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-3.2, -68.8, 0.7, 0.7);
      ctx.fillRect(2.4, -68.8, 0.7, 0.7);

      // Eyelashes
      ctx.strokeStyle = '#100a06';
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(-4.5, -69.5); ctx.quadraticCurveTo(-2.8, -70.5, -1.2, -69);
      ctx.moveTo(1.2, -69); ctx.quadraticCurveTo(2.8, -70.5, 4.5, -69.5);
      ctx.stroke();

      // Soft Rose Blush on Cheeks
      ctx.fillStyle = skinBlush;
      ctx.beginPath();
      ctx.ellipse(-4.2, -65, 2, 1.2, 0, 0, Math.PI * 2);
      ctx.ellipse(4.2, -65, 2, 1.2, 0, 0, Math.PI * 2);
      ctx.fill();

      // Delicate Tinted Lips
      ctx.fillStyle = skinLip;
      ctx.beginPath();
      ctx.ellipse(0, -62.5, 1.4, 0.8, 0, 0, Math.PI * 2);
      ctx.fill();

      // 8. SEAMLESS FRONT HAIR LOCKS & FLOWING TRESSES (Connects directly to crown!)
      ctx.fillStyle = hairHex;
      // Left Front Tress
      ctx.beginPath();
      ctx.moveTo(0, -75); // Crown center parting
      ctx.quadraticCurveTo(-6.5, -74, -7.5, -66); // Over temple
      ctx.quadraticCurveTo(-11, -50, -9.5, -34);  // Curving over shoulder
      ctx.quadraticCurveTo(-11, -26, -7, -22);    // Front tip
      ctx.lineTo(-4, -22);
      ctx.quadraticCurveTo(-6.5, -34, -5.5, -54); // Inner line along neck
      ctx.quadraticCurveTo(-4, -64, 0, -73);
      ctx.closePath();
      ctx.fill();

      // Right Front Tress
      ctx.beginPath();
      ctx.moveTo(0, -75);
      ctx.quadraticCurveTo(6.5, -74, 7.5, -66);
      ctx.quadraticCurveTo(11, -50, 9.5, -34);
      ctx.quadraticCurveTo(11, -26, 7, -22);
      ctx.lineTo(4, -22);
      ctx.quadraticCurveTo(6.5, -34, 5.5, -54);
      ctx.quadraticCurveTo(4, -64, 0, -73);
      ctx.closePath();
      ctx.fill();

      // Golden wave highlights along front tresses
      ctx.strokeStyle = hairHi;
      ctx.lineWidth = 1.1;
      ctx.beginPath();
      ctx.moveTo(-1, -74); ctx.quadraticCurveTo(-8, -60, -6.5, -24);
      ctx.moveTo(1, -74); ctx.quadraticCurveTo(8, -60, 6.5, -24);
      ctx.stroke();

      ctx.strokeStyle = '#fef08a';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.moveTo(-1, -73); ctx.quadraticCurveTo(-6.5, -52, -5, -26);
      ctx.moveTo(1, -73); ctx.quadraticCurveTo(6.5, -52, 5, -26);
      ctx.stroke();

      if (archId === 'infiltrator') {
        // --- MAID MARIAN SPECIFICS ---
        // Noble velvet hood / skullcap
        ctx.fillStyle = hatHex;
        ctx.beginPath();
        ctx.ellipse(0, -74, 8, 5, 0, Math.PI, 0);
        ctx.fill();

        // Golden Filigree Tiara on Brow
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.arc(0, -72, 7.2, -Math.PI * 0.85, -Math.PI * 0.15);
        ctx.stroke();

        // Teardrop Ruby Gem on Forehead
        ctx.fillStyle = '#e74c3c';
        ctx.beginPath();
        ctx.ellipse(0, -73.5, 1.3, 2, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0.2, -74.5, 0.7, 0.7);

        // Hands & Dual Damascus Stilettos (FIRMLY HELD IN HAND!)
        const handX = isActing ? 22 : 11;
        const handY = isActing ? -54 : -36;

        // Right Arm extending to hand
        ctx.strokeStyle = c.cloak.hi;
        ctx.lineWidth = 3.2;
        ctx.beginPath();
        ctx.moveTo(8, -50);
        ctx.quadraticCurveTo(12, -44, handX, handY);
        ctx.stroke();

        // Stiletto blade
        ctx.strokeStyle = '#cbd5e1';
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        if (isActing) {
          ctx.moveTo(handX - 4, handY + 4);
          ctx.lineTo(handX + 16, handY - 14);
        } else {
          ctx.moveTo(handX, handY);
          ctx.lineTo(handX + 6, handY + 16);
        }
        ctx.stroke();

        // Crossguard & Ruby Pommel
        ctx.fillStyle = '#ffd700';
        ctx.fillRect(handX - 2, handY - 2, 4, 4);

        // Hand fingers clasping the grip
        ctx.fillStyle = skinBase;
        ctx.beginPath();
        ctx.arc(handX, handY, 2.6, 0, Math.PI * 2);
        ctx.fill();

      } else if (archId === 'herbalist') {
        // --- MOTHER MEG SPECIFICS ---
        // Silver braided crown
        ctx.strokeStyle = '#d8dce2';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.arc(0, -73, 7.5, -Math.PI * 0.9, -Math.PI * 0.1);
        ctx.stroke();

        // Garland of ferns & berries
        ctx.fillStyle = '#27ae60';
        ctx.fillRect(-6, -78, 3, 2); ctx.fillRect(4, -78, 3, 2);
        ctx.fillStyle = '#e74c3c';
        ctx.beginPath(); ctx.arc(-2, -77, 1.5, 0, Math.PI * 2); ctx.arc(2, -77, 1.5, 0, Math.PI * 2); ctx.fill();

        // Elderwood staff held in left hand
        ctx.strokeStyle = '#4a2e18';
        ctx.lineWidth = 2.8;
        ctx.beginPath();
        ctx.moveTo(-12, -88); ctx.quadraticCurveTo(-14, -50, -12, 2);
        ctx.stroke();

        // Amber crystal on staff
        ctx.fillStyle = '#f39c12';
        ctx.beginPath(); ctx.ellipse(-12, -90, 3, 5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#fef08a';
        ctx.beginPath(); ctx.ellipse(-12, -90, 1.5, 2.5, 0, 0, Math.PI * 2); ctx.fill();

        // Left Hand gripping staff
        ctx.fillStyle = skinBase;
        ctx.beginPath(); ctx.arc(-12, -48, 2.8, 0, Math.PI * 2); ctx.fill();

        // Right Hand holding Stone Mortar with Bubbling Brew
        ctx.fillStyle = '#475569';
        ctx.beginPath(); ctx.roundRect(8, -48, 13, 11, 2); ctx.fill();
        ctx.fillStyle = '#10b981';
        ctx.beginPath(); ctx.ellipse(14.5, -48, 5.5, 2, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = 'rgba(52, 211, 153, 0.7)';
        ctx.font = '11px sans-serif';
        ctx.fillText('✨', 14, -56);

        // Right Hand holding mortar
        ctx.fillStyle = skinBase;
        ctx.beginPath(); ctx.arc(8, -43, 2.8, 0, Math.PI * 2); ctx.fill();
      }

    } else {
      // --- ARTISAN MALE OUTLAW ANATOMY ---
      const isBroad = (archId === 'brawler');
      const tunicW = isBroad ? 18 : 14.5;

      // 1. Tailored Wool Hosen / Breeches
      ctx.fillStyle = '#1e1610';
      ctx.beginPath();
      ctx.moveTo(-tunicW + 6, -30); ctx.lineTo(-1, -30); ctx.lineTo(-1, -15); ctx.lineTo(-tunicW + 5, -15);
      ctx.closePath(); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(1, -30); ctx.lineTo(tunicW - 6, -30); ctx.lineTo(tunicW - 5, -15); ctx.lineTo(1, -15);
      ctx.closePath(); ctx.fill();

      // 2. High Medieval Leather Riding Boots
      ctx.fillStyle = '#150e09';
      ctx.beginPath();
      ctx.moveTo(-tunicW + 5, -15); ctx.lineTo(-2, -15); ctx.lineTo(-2, 0); ctx.lineTo(-tunicW + 4, 0); ctx.lineTo(-tunicW + 6, -11);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#2a1a10';
      ctx.fillRect(-tunicW + 6, -16, tunicW - 3, 3.5);

      ctx.fillStyle = '#150e09';
      ctx.beginPath();
      ctx.moveTo(2, -15); ctx.lineTo(tunicW - 5, -15); ctx.lineTo(tunicW - 4, 0); ctx.lineTo(2, 0); ctx.lineTo(1, -11);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#2a1a10';
      ctx.fillRect(1, -16, tunicW - 3, 3.5);

      // 3. Layered Outlaw Gambeson / Tunic
      ctx.fillStyle = c.cloak.hex;
      ctx.beginPath();
      ctx.moveTo(-tunicW, -24);
      ctx.quadraticCurveTo(-tunicW + 1.5, -42, -tunicW + 1, -58);
      ctx.lineTo(tunicW - 1, -58);
      ctx.quadraticCurveTo(tunicW - 1.5, -42, tunicW, -24);
      ctx.lineTo(3.5, -24);
      ctx.lineTo(0, -31);
      ctx.lineTo(-3.5, -24);
      ctx.closePath();
      ctx.fill();

      // Seam Highlights
      ctx.strokeStyle = c.cloak.sh;
      ctx.lineWidth = 1.1;
      ctx.beginPath();
      ctx.moveTo(-tunicW + 7, -24); ctx.lineTo(-5, -46);
      ctx.moveTo(tunicW - 7, -24); ctx.lineTo(5, -46);
      ctx.stroke();

      // Adventurer Leather Belt & Buckle
      ctx.fillStyle = '#1c0f07';
      ctx.fillRect(-tunicW + 1, -35, (tunicW - 1) * 2, 4.8);
      ctx.fillStyle = info.stageNum >= 3 ? '#ffd700' : '#d4af37';
      ctx.fillRect(-3.5, -36.5, 7, 7.5);
      ctx.fillStyle = '#120803';
      ctx.fillRect(-2, -35, 4, 4.5);
      // Hanging belt strap
      ctx.fillStyle = '#1c0f07';
      ctx.fillRect(2.2, -35, 3.2, 11);

      // 4. Shaded Neck
      ctx.fillStyle = skinSh;
      ctx.fillRect(-3.5, -60, 7, 8);

      // 5. Sculpted Jawline & Contoured Head
      ctx.fillStyle = skinBase;
      ctx.beginPath();
      if (archId === 'brawler') {
        ctx.moveTo(-8.5, -75); ctx.lineTo(8.5, -75); ctx.lineTo(8.2, -64);
        ctx.quadraticCurveTo(6, -58.5, 0, -58.5); ctx.quadraticCurveTo(-6, -58.5, -8.2, -64);
        ctx.closePath();
      } else if (archId === 'friar') {
        ctx.ellipse(0, -67, 8.2, 8.5, 0, 0, Math.PI * 2);
      } else if (archId === 'scout') {
        ctx.ellipse(0, -68, 6.2, 7.6, 0, 0, Math.PI * 2);
      } else if (archId === 'sheriff') {
        ctx.ellipse(0, -66, 8, 8.2, 0, 0, Math.PI * 2);
      } else {
        ctx.moveTo(-7.2, -75); ctx.lineTo(7.2, -75); ctx.lineTo(6.8, -65);
        ctx.quadraticCurveTo(4.8, -59, 0, -59); ctx.quadraticCurveTo(-4.8, -59, -6.8, -65);
        ctx.closePath();
      }
      ctx.fill();

      // 6. Almond Eyes & Eyebrows
      ctx.fillStyle = '#1c130d';
      if (archId === 'friar') {
        ctx.strokeStyle = '#1c130d';
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        ctx.arc(-3.2, -67.5, 2, -Math.PI * 0.85, -Math.PI * 0.15);
        ctx.arc(3.2, -67.5, 2, -Math.PI * 0.85, -Math.PI * 0.15);
        ctx.stroke();
        ctx.fillStyle = skinBlush;
        ctx.beginPath(); ctx.arc(-4.6, -64, 2.4, 0, Math.PI * 2); ctx.arc(4.6, -64, 2.4, 0, Math.PI * 2); ctx.fill();
      } else if (archId === 'scout') {
        ctx.beginPath(); ctx.ellipse(-2.8, -68, 1.4, 1.8, 0, 0, Math.PI * 2); ctx.ellipse(2.8, -68, 1.4, 1.8, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-3.3, -68.8, 0.8, 0.8); ctx.fillRect(2.3, -68.8, 0.8, 0.8);
        ctx.strokeStyle = hairSh; ctx.lineWidth = 0.9;
        ctx.beginPath(); ctx.moveTo(-4.2, -70.8); ctx.lineTo(-1.6, -70.8); ctx.moveTo(1.6, -70.8); ctx.lineTo(4.2, -70.8); ctx.stroke();
        // Subtle forest freckles
        ctx.fillStyle = 'rgba(160, 82, 45, 0.5)';
        ctx.fillRect(-4, -64.5, 0.8, 0.8); ctx.fillRect(3.5, -64.5, 0.8, 0.8);
      } else {
        ctx.beginPath(); ctx.ellipse(-3, -68, 1.3, 1.6, -0.08, 0, Math.PI * 2); ctx.ellipse(3, -68, 1.3, 1.6, 0.08, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-3.3, -68.7, 0.7, 0.7); ctx.fillRect(2.7, -68.7, 0.7, 0.7);
        ctx.strokeStyle = hairSh; ctx.lineWidth = 1.1;
        ctx.beginPath(); ctx.moveTo(-4.6, -70.5); ctx.lineTo(-1.5, -69.8); ctx.moveTo(1.5, -69.8); ctx.lineTo(4.6, -70.5); ctx.stroke();
      }

      // Nose shadow & lips
      ctx.fillStyle = skinSh;
      ctx.beginPath(); ctx.moveTo(0, -68); ctx.lineTo(-0.8, -64.5); ctx.lineTo(0.8, -64.5); ctx.closePath(); ctx.fill();
      ctx.fillStyle = skinLip; ctx.fillRect(-1.2, -62.2, 2.4, 0.8);

      // --- ARCHETYPE SPECIFICS (GEAR & HAND-HELD WEAPONS) ---
      if (archId === 'archer') {
        // ROBIN HOOD (OR NOTTINGHAM BEGGAR DISGUISE!)
        if (c.isBeggar) {
          // Nottingham Beggar Disguise: Patchwork travel cowl covering face
          ctx.fillStyle = '#5c4d3c';
          ctx.beginPath();
          ctx.ellipse(0, -75, 11, 7, 0, Math.PI, 0);
          ctx.fill();
          // Patched hood edge
          ctx.fillStyle = '#7a6852';
          ctx.fillRect(-4, -78, 4, 3);
          // Wooden Alms Change Cup held in hands!
          ctx.fillStyle = '#6e4726';
          ctx.beginPath(); ctx.roundRect(4, -46, 9, 8, 2); ctx.fill();
          // Clinking silver pence inside
          ctx.fillStyle = '#cbd5e1';
          ctx.beginPath(); ctx.arc(7, -44, 1.5, 0, Math.PI * 2); ctx.arc(10, -43, 1.2, 0, Math.PI * 2); ctx.fill();
          // Hands holding cup
          ctx.fillStyle = skinBase;
          ctx.beginPath(); ctx.arc(3, -42, 2.5, 0, Math.PI * 2); ctx.arc(14, -42, 2.5, 0, Math.PI * 2); ctx.fill();
        } else {
          // Classic Lincoln Green Archer Cowl & Feather
          ctx.fillStyle = hatHex;
          ctx.beginPath();
          ctx.moveTo(-11, -74); ctx.quadraticCurveTo(-9, -82, 0, -87); ctx.quadraticCurveTo(10, -82, 14, -73); ctx.lineTo(-11, -74);
          ctx.closePath(); ctx.fill();
          ctx.strokeStyle = hatSh; ctx.lineWidth = 1.2; ctx.stroke();

          // Pheasant Feather
          ctx.strokeStyle = '#e11d48'; ctx.lineWidth = 2.4;
          ctx.beginPath(); ctx.moveTo(1, -83); ctx.quadraticCurveTo(14, -98, 23, -93); ctx.stroke();
          ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 0.9;
          ctx.beginPath(); ctx.moveTo(1, -83); ctx.quadraticCurveTo(12, -94, 20, -91); ctx.stroke();

          // Van Dyke Goatee
          ctx.fillStyle = beardColor;
          ctx.beginPath();
          ctx.moveTo(-4.5, -63.5); ctx.quadraticCurveTo(0, -62, 4.5, -63.5); ctx.quadraticCurveTo(0, -64.5, -4.5, -63.5); ctx.fill();
          ctx.beginPath(); ctx.moveTo(-2, -61); ctx.lineTo(2, -61); ctx.lineTo(0, -57.5); ctx.closePath(); ctx.fill();

          // Back Quiver
          ctx.fillStyle = '#4a2f1b'; ctx.fillRect(-17, -62, 6.5, 26);
          const hasGoldArrow = !!equippedLoot[4];
          ctx.fillStyle = hasGoldArrow ? '#ffd700' : '#f8fafc';
          ctx.fillRect(-17, -70, 2, 9); ctx.fillRect(-14, -68, 2, 7); ctx.fillRect(-11.5, -71, 2, 10);

          // FIRM HAND-HELD YEOW LONGBOW (NO FLOATING BOWS!)
          const bowHandX = isActing ? 20 : 16;
          const bowHandY = isActing ? -50 : -46;

          // Left Arm extending to grip the bow riser
          ctx.strokeStyle = c.cloak.hi;
          ctx.lineWidth = 3.2;
          ctx.beginPath();
          ctx.moveTo(9, -52); ctx.lineTo(bowHandX, bowHandY); ctx.stroke();

          // Archer Leather Bracer on forearm
          ctx.fillStyle = '#3a2012'; ctx.fillRect(11, -50, 4.5, 6);

          // Longbow Body passing THROUGH the hand
          const hasGildedBow = !!equippedLoot[3];
          ctx.strokeStyle = hasGildedBow ? '#ffd700' : (info.stageNum >= 4 ? '#b8860b' : '#613917');
          ctx.lineWidth = hasGildedBow ? 3.6 : 2.8;
          ctx.beginPath();
          if (isActing) {
            ctx.arc(bowHandX - 3, bowHandY, 24, -Math.PI * 0.44, Math.PI * 0.44);
            ctx.stroke();
            // Bowstring pulled back to cheek
            ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 0.9;
            ctx.beginPath();
            ctx.moveTo(bowHandX - 3 + Math.cos(-Math.PI * 0.44) * 24, bowHandY + Math.sin(-Math.PI * 0.44) * 24);
            ctx.lineTo(2, -50);
            ctx.lineTo(bowHandX - 3 + Math.cos(Math.PI * 0.44) * 24, bowHandY + Math.sin(Math.PI * 0.44) * 24);
            ctx.stroke();
            // Right hand pinching string at cheek
            ctx.fillStyle = skinBase;
            ctx.beginPath(); ctx.arc(2, -50, 2.5, 0, Math.PI * 2); ctx.fill();
          } else {
            ctx.arc(bowHandX, bowHandY, 22, -Math.PI * 0.35, Math.PI * 0.35);
            ctx.stroke();
            ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(bowHandX + Math.cos(-Math.PI * 0.35) * 22, bowHandY + Math.sin(-Math.PI * 0.35) * 22);
            ctx.lineTo(bowHandX + Math.cos(Math.PI * 0.35) * 22, bowHandY + Math.sin(Math.PI * 0.35) * 22);
            ctx.stroke();
          }

          // Hand fingers clasping firmly over the bow riser!
          ctx.fillStyle = skinBase;
          ctx.beginPath();
          ctx.roundRect(bowHandX - 2.5, bowHandY - 3, 5, 6, 1.5);
          ctx.fill();
          ctx.strokeStyle = '#2b170c'; ctx.lineWidth = 0.8;
          ctx.strokeRect(bowHandX - 2.5, bowHandY - 3, 5, 6);
        }

      } else if (archId === 'brawler') {
        // LITTLE JOHN: Giant Frame, Headband, Beard & Heavy Quarterstaff
        ctx.fillStyle = '#2b170c'; ctx.fillRect(-8.5, -74, 17, 3.5);
        ctx.fillStyle = '#94a3b8'; ctx.fillRect(-1, -73.5, 2, 2.5);

        // Thick Cascading Beard
        ctx.fillStyle = beardColor;
        ctx.beginPath();
        ctx.moveTo(-8, -65); ctx.quadraticCurveTo(-11, -54, -7, -40);
        ctx.quadraticCurveTo(0, -32, 7, -40); ctx.quadraticCurveTo(11, -54, 8, -65);
        ctx.closePath(); ctx.fill();

        // Massive Oak Quarterstaff gripped in both hands
        const staffAngle = isActing ? 0.35 : -0.15;
        ctx.strokeStyle = '#5a3418'; ctx.lineWidth = 4.2;
        ctx.beginPath();
        ctx.moveTo(isActing ? -4 : 8, isActing ? -86 : -84);
        ctx.lineTo(isActing ? 22 : 14, 2);
        ctx.stroke();
        // Iron Ferrules
        ctx.fillStyle = '#64748b';
        ctx.fillRect(isActing ? -6 : 6, isActing ? -86 : -84, 5, 4);

        // Hands gripping staff
        ctx.fillStyle = skinBase;
        ctx.beginPath();
        ctx.arc(isActing ? 6 : 10, isActing ? -56 : -52, 3.5, 0, Math.PI * 2);
        ctx.arc(isActing ? 14 : 12, isActing ? -36 : -34, 3.5, 0, Math.PI * 2);
        ctx.fill();

      } else if (archId === 'friar') {
        // FRIAR TUCK (Standard Ale Flagon OR Beggar Disguise Change Cup!)
        if (c.isBeggar) {
          // Beggar Friar Disguise (Patchwork Cowl & Change Cup)
          ctx.fillStyle = '#4a321f';
          ctx.beginPath(); ctx.ellipse(0, -75, 11, 7, 0, Math.PI, 0); ctx.fill();
          // Turned Wooden Change Cup held in hands!
          const cupX = 10, cupY = isActing ? -52 : -44;
          ctx.fillStyle = '#6e4726';
          ctx.beginPath(); ctx.roundRect(cupX - 4, cupY - 4, 11, 9, 2); ctx.fill();
          // Clinking Pence & Shillings inside
          ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(cupX, cupY - 2, 1.8, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#cbd5e1'; ctx.beginPath(); ctx.arc(cupX + 4, cupY - 3, 1.5, 0, Math.PI * 2); ctx.fill();
          // Hands cupping the bowl
          ctx.fillStyle = skinBase;
          ctx.beginPath(); ctx.arc(cupX - 4, cupY, 3, 0, Math.PI * 2); ctx.arc(cupX + 8, cupY, 3, 0, Math.PI * 2); ctx.fill();
        } else {
          // Tonsure Ring
          ctx.fillStyle = beardColor;
          ctx.beginPath(); ctx.arc(0, -74, 9, Math.PI, 0); ctx.stroke();
          ctx.fillStyle = skinBase; ctx.beginPath(); ctx.ellipse(0, -75, 5, 3.5, 0, 0, Math.PI * 2); ctx.fill();

          // Habit Cowl & Knotted Rope Cincture
          ctx.fillStyle = '#4a2e18';
          ctx.beginPath(); ctx.moveTo(-11, -54); ctx.quadraticCurveTo(0, -48, 11, -54); ctx.lineTo(8, -60); ctx.quadraticCurveTo(0, -56, -8, -60); ctx.closePath(); ctx.fill();

          ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2.2;
          ctx.beginPath(); ctx.moveTo(-12, -35); ctx.lineTo(12, -35); ctx.stroke();
          ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.arc(-2, -35, 2, 0, Math.PI * 2); ctx.arc(2, -35, 2, 0, Math.PI * 2); ctx.fill();

          // Frothy Ale Tankard gripped in hand!
          const mugX = isActing ? 12 : 9;
          const mugY = isActing ? -64 : -50;
          ctx.fillStyle = '#6b4323';
          ctx.beginPath(); ctx.roundRect(mugX, mugY, 14, 17, 2); ctx.fill();
          ctx.fillStyle = '#475569';
          ctx.fillRect(mugX, mugY + 3, 14, 2); ctx.fillRect(mugX, mugY + 12, 14, 2);
          ctx.fillStyle = '#fffdf0';
          ctx.beginPath(); ctx.ellipse(mugX + 7, mugY - 1, 8.5, 4.5, 0, 0, Math.PI * 2); ctx.fill();

          // Hand gripping tankard handle
          ctx.fillStyle = skinBase;
          ctx.beginPath(); ctx.arc(mugX + 14, mugY + 8, 3.2, 0, Math.PI * 2); ctx.fill();
        }

      } else if (archId === 'minstrel') {
        // ALAN-A-DALE: Cavalier Beret, Peacock Feather, Rosewood Lute
        ctx.fillStyle = hatHex;
        ctx.beginPath(); ctx.ellipse(1, -76, 13, 6, 0.22, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#0284c7'; ctx.lineWidth = 2.2;
        ctx.beginPath(); ctx.moveTo(3, -77); ctx.quadraticCurveTo(16, -92, 24, -86); ctx.stroke();
        ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.arc(22, -87, 2.5, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(22, -87, 1.2, 0, Math.PI * 2); ctx.fill();

        // Wavy chestnut locks
        ctx.fillStyle = hairHex;
        ctx.beginPath(); ctx.moveTo(-7.5, -74); ctx.quadraticCurveTo(-11, -62, -8, -54); ctx.lineTo(-6, -56); ctx.quadraticCurveTo(-8, -64, -6, -72); ctx.closePath(); ctx.fill();

        // Rosewood Lute played in hands!
        ctx.save();
        ctx.translate(isActing ? 11 : 9, isActing ? -48 : -46);
        ctx.rotate(0.35);
        ctx.fillStyle = '#9a4f21';
        ctx.beginPath(); ctx.ellipse(0, 0, 8.5, 12, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(0, -1, 3, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#261205'; ctx.beginPath(); ctx.arc(0, -1, 1.8, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#3e1d08'; ctx.lineWidth = 3.2;
        ctx.beginPath(); ctx.moveTo(0, -12); ctx.lineTo(0, -28); ctx.stroke();
        // Left hand fretting neck
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(0, -20, 2.5, 0, Math.PI * 2); ctx.fill();
        // Right hand strumming
        ctx.beginPath(); ctx.arc(4, 0, 2.8, 0, Math.PI * 2); ctx.fill();
        ctx.restore();

      } else if (archId === 'duelist') {
        // WILL SCARLET: Feathered Cavalier Hat, Capelet, Rapier Basket Hilt
        ctx.fillStyle = '#991b1b';
        ctx.beginPath(); ctx.ellipse(0, -76, 13, 5.5, -0.15, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(-2, -78); ctx.quadraticCurveTo(12, -94, 20, -88); ctx.stroke();

        ctx.fillStyle = beardColor;
        ctx.beginPath(); ctx.moveTo(-5, -63.5); ctx.quadraticCurveTo(0, -62, 5, -63.5); ctx.quadraticCurveTo(6, -65, 7, -66); ctx.quadraticCurveTo(0, -63.5, -5, -63.5); ctx.fill();

        // Highland Rapier held in hand
        const swHandX = isActing ? 12 : 11;
        const swHandY = isActing ? -46 : -36;
        ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 2.4;
        ctx.beginPath();
        if (isActing) { ctx.moveTo(swHandX, swHandY); ctx.lineTo(34, -68); }
        else { ctx.moveTo(swHandX, swHandY); ctx.lineTo(22, -74); }
        ctx.stroke();

        // Basket Hilt enclosing hand
        ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 1.8;
        ctx.beginPath(); ctx.arc(swHandX, swHandY, 4.5, 0, Math.PI * 2); ctx.stroke();
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(swHandX, swHandY, 2.5, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'scout') {
        // MUCH THE MILLER'S SON: Nimble Forest Scout with Slingshot
        ctx.fillStyle = '#e2e8f0'; // Flour-dusted linen hood
        ctx.beginPath(); ctx.ellipse(0, -75, 10, 6.5, 0, Math.PI, 0); ctx.fill();
        ctx.fillStyle = hairHex; // Tousled hair
        ctx.beginPath(); ctx.moveTo(-6, -73); ctx.lineTo(-8, -67); ctx.lineTo(-4, -70); ctx.closePath(); ctx.fill();
        ctx.beginPath(); ctx.moveTo(6, -73); ctx.lineTo(8, -67); ctx.lineTo(4, -70); ctx.closePath(); ctx.fill();

        // Leather scout bandolier
        ctx.strokeStyle = '#3a2012'; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(-11, -54); ctx.lineTo(10, -32); ctx.stroke();

        // Forked Slingshot gripped in left hand
        const slingX = isActing ? 16 : 14;
        const slingY = isActing ? -52 : -46;
        ctx.strokeStyle = '#6e3e1a'; ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(slingX, slingY + 8); ctx.lineTo(slingX, slingY);
        ctx.lineTo(slingX - 4, slingY - 7);
        ctx.moveTo(slingX, slingY); ctx.lineTo(slingX + 4, slingY - 6);
        ctx.stroke();

        // Left hand holding slingshot handle
        ctx.fillStyle = skinBase;
        ctx.beginPath(); ctx.arc(slingX, slingY + 4, 2.8, 0, Math.PI * 2); ctx.fill();

        // Right hand pulling back acorn ammo
        const pullX = isActing ? 6 : 9;
        const pullY = isActing ? -48 : -40;
        ctx.fillStyle = '#854d0e'; // Acorn
        ctx.beginPath(); ctx.arc(pullX, pullY, 2.8, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = skinBase;
        ctx.beginPath(); ctx.arc(pullX - 1, pullY, 2.2, 0, Math.PI * 2); ctx.fill();

      } else if (archId === 'bounty') {
        // GUY OF GISBORNE: Nasal Helmet, Chainmail Coif & Notched Bastard Sword
        ctx.fillStyle = '#334155';
        ctx.beginPath(); ctx.moveTo(-12, -54); ctx.quadraticCurveTo(0, -49, 12, -54); ctx.lineTo(8, -62); ctx.quadraticCurveTo(0, -58, -8, -62); ctx.closePath(); ctx.fill();
        ctx.fillStyle = '#1e293b';
        ctx.beginPath(); ctx.arc(0, -73, 9, -Math.PI, 0); ctx.lineTo(9, -71); ctx.lineTo(-9, -71); ctx.closePath(); ctx.fill();
        ctx.fillRect(-1.2, -73, 2.4, 6);

        // Blackened sword gripped in gauntlet
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
        // SHERIFF OF NOTTINGHAM: Velvet Cap, Ermine Fur, Tax Purse in Hand
        ctx.fillStyle = '#831843'; ctx.beginPath(); ctx.ellipse(0, -76, 12, 5.5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(4, -76, 2.4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.ellipse(0, -54, 13, 5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#0f172a'; ctx.fillRect(-7, -55, 1.8, 2.5); ctx.fillRect(0, -53, 1.8, 2.5); ctx.fillRect(7, -55, 1.8, 2.5);

        // Heavy velvet tax coin purse clutched in hand
        ctx.fillStyle = '#b45309'; ctx.beginPath(); ctx.ellipse(13, -38, 7, 8, 0.2, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.fillRect(10, -44, 6, 2.5);
        ctx.fillStyle = skinBase; ctx.beginPath(); ctx.arc(10, -42, 3, 0, Math.PI * 2); ctx.fill();
      }
    }

    // Gold Bling (Earned by holding Gold Sovereigns)
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

text = text[:s_char] + new_char + text[e_char:]
print("Updated drawCharacter successfully!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
