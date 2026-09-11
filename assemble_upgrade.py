import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace drawCamp to include backdropProps
s_camp = text.find('function drawCamp(info) {')
e_camp = text.find('// --- Character Rendering (10 Archetypes with Aging) ---', s_camp)
assert s_camp != -1 and e_camp != -1, "drawCamp bounds not found!"

new_camp = """function drawCamp(info) {
    const isDormant = info.isDormant;

    // 1. Camp Shelter (Tent / Lodge)
    if (backdropProps.campShelter) {
      if (info.stageNum === 1) {
        ctx.fillStyle = '#6b5839';
        ctx.fillRect(115, 362, 34, 10); // burlap bedroll
      }
      if (info.stageNum >= 2 && info.stageNum < 4) {
        ctx.fillStyle = '#a19379';
        ctx.beginPath();
        ctx.moveTo(110, 370); ctx.lineTo(150, 295); ctx.lineTo(190, 370);
        ctx.closePath(); ctx.fill();
        ctx.fillStyle = '#3d3023';
        ctx.beginPath();
        ctx.moveTo(140, 370); ctx.lineTo(150, 325); ctx.lineTo(160, 370);
        ctx.closePath(); ctx.fill();
      }
      if (info.stageNum >= 4) {
        ctx.fillStyle = '#3a2717';
        ctx.fillRect(100, 275, 95, 75);
        ctx.fillStyle = '#5c4128';
        for (let i = 0; i < 5; i++) {
          ctx.fillRect(100, 280 + i * 14, 95, 2);
        }
        ctx.fillStyle = info.stageNum === 5 ? '#243b1c' : '#4d2e18';
        ctx.beginPath();
        ctx.moveTo(90, 275); ctx.lineTo(147, 230); ctx.lineTo(205, 275);
        ctx.closePath(); ctx.fill();
        ctx.fillStyle = isDormant ? '#222' : '#f5c842';
        ctx.fillRect(122, 292, 16, 18);
        if (info.stageNum === 5) {
          ctx.fillStyle = '#7a1924';
          ctx.fillRect(190, 250, 14, 28);
          ctx.fillStyle = '#ffd700';
          ctx.fillText('🏹', 191, 267);
        }
      }
    }

    // 2. Campfire / Hearth
    if (backdropProps.campfire) {
      const fx = campfire.x, fy = campfire.y;
      if (info.stageNum >= 3) {
        ctx.fillStyle = '#4f5752';
        for (let a = 0; a < Math.PI * 2; a += 0.9) {
          ctx.beginPath();
          ctx.arc(fx + Math.cos(a) * 20, fy + Math.sin(a) * 9, 6, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.strokeStyle = '#1e1e1e';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(fx - 18, fy + 4); ctx.lineTo(fx - 18, fy - 22); ctx.lineTo(fx + 18, fy - 22); ctx.lineTo(fx + 18, fy + 4);
        ctx.stroke();
        ctx.fillStyle = '#111';
        ctx.beginPath(); ctx.arc(fx, fy - 14, 7, 0, Math.PI * 2); ctx.fill();
      } else {
        ctx.fillStyle = '#574838';
        ctx.fillRect(fx - 14, fy + 2, 28, 4);
      }

      if (!isDormant) {
        const glow = ctx.createRadialGradient(fx, fy, 4, fx, fy, 75 * campfire.intensity);
        glow.addColorStop(0, 'rgba(255, 170, 40, 0.55)');
        glow.addColorStop(1, 'rgba(255, 100, 20, 0)');
        ctx.fillStyle = glow;
        ctx.beginPath(); ctx.arc(fx, fy, 75 * campfire.intensity, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ff7b1a';
        ctx.beginPath(); ctx.arc(fx, fy - 2, 8 * campfire.intensity, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd242';
        ctx.beginPath(); ctx.arc(fx, fy - 4, 4 * campfire.intensity, 0, Math.PI * 2); ctx.fill();
      } else {
        ctx.fillStyle = '#3a3a3a';
        ctx.beginPath(); ctx.arc(fx, fy, 8, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#8a5024';
        ctx.fillRect(fx - 6, fy - 2, 12, 4);
      }
    }

    // 3. Armory Weapon Rack
    if (backdropProps.armoryRack) {
      const rx = 208, ry = 372;
      ctx.fillStyle = '#4a2f1b';
      ctx.beginPath();
      ctx.moveTo(rx - 9, ry); ctx.lineTo(rx - 4, ry - 30); ctx.lineTo(rx + 4, ry - 30); ctx.lineTo(rx + 9, ry);
      ctx.closePath(); ctx.fill();
      ctx.fillRect(rx - 13, ry - 19, 26, 3.5);
      ctx.fillRect(rx - 11, ry - 8, 22, 3);
      // Upright Yew Longbow
      ctx.strokeStyle = '#8b5a2b';
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.arc(rx - 4, ry - 15, 17, -Math.PI * 0.42, Math.PI * 0.42);
      ctx.stroke();
      ctx.strokeStyle = '#f8fafc';
      ctx.lineWidth = 0.7;
      ctx.beginPath();
      ctx.moveTo(rx - 4 + Math.cos(-Math.PI * 0.42) * 17, ry - 15 + Math.sin(-Math.PI * 0.42) * 17);
      ctx.lineTo(rx - 4 + Math.cos(Math.PI * 0.42) * 17, ry - 15 + Math.sin(Math.PI * 0.42) * 17);
      ctx.stroke();
      // Shield
      ctx.fillStyle = '#1e3a8a';
      ctx.beginPath();
      ctx.moveTo(rx + 2, ry - 17); ctx.lineTo(rx + 15, ry - 17); ctx.quadraticCurveTo(rx + 15, ry - 4, rx + 8.5, ry); ctx.quadraticCurveTo(rx + 2, ry - 4, rx + 2, ry - 17);
      ctx.closePath(); ctx.fill();
      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 1.1;
      ctx.stroke();
      ctx.fillStyle = '#ffd700';
      ctx.beginPath(); ctx.arc(rx + 8.5, ry - 9, 2.5, 0, Math.PI * 2); ctx.fill();
    }

    // 4. Mother Meg's Alchemy Bench & Glowing Elixirs
    if (backdropProps.alchemyBench || equippedLoot[5]) {
      const ax = 182, ay = 376;
      ctx.fillStyle = '#3e2717';
      ctx.fillRect(ax - 12, ay - 11, 24, 3.5);
      ctx.fillRect(ax - 10, ay - 7.5, 2.8, 9.5);
      ctx.fillRect(ax + 7, ay - 7.5, 2.8, 9.5);
      // Glowing green alchemical flask (Greenwood Elixir)
      ctx.fillStyle = 'rgba(200, 255, 230, 0.7)';
      ctx.beginPath(); ctx.arc(ax - 5, ay - 15, 4.2, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#10b981';
      ctx.beginPath(); ctx.arc(ax - 5, ay - 14, 3.4, 0, Math.PI); ctx.fill();
      // Rising steam
      ctx.fillStyle = 'rgba(52, 211, 153, 0.7)';
      ctx.font = '9px sans-serif';
      ctx.fillText('✨', ax - 8, ay - 21);
      // Stone Mortar
      ctx.fillStyle = '#64748b';
      ctx.beginPath(); ctx.roundRect(ax + 3, ay - 16, 6.5, 5, 1); ctx.fill();
      ctx.fillStyle = '#334155'; ctx.fillRect(ax + 5, ay - 19, 1.8, 4);
      // Violet Nightshade vial
      ctx.fillStyle = '#8b5cf6'; ctx.fillRect(ax - 0.5, ay - 16, 2.4, 4.8);
    }

    // 5. Gold Sovereigns Treasury Hoard
    const goldCount = walletLootBalances[1] || 0;
    if (backdropProps.treasureHoard || (equippedLoot[1] && goldCount > 0)) {
      const cx = 236, cy = 378;
      ctx.fillStyle = '#3a2010';
      ctx.fillRect(cx - 14, cy - 8, 28, 16);
      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 2;
      ctx.strokeRect(cx - 14, cy - 8, 28, 16);
      // Gold corner brackets
      ctx.fillStyle = '#ffd700';
      ctx.fillRect(cx - 14, cy - 8, 5, 4);
      ctx.fillRect(cx + 9, cy - 8, 5, 4);
      ctx.fillRect(cx - 14, cy + 4, 5, 4);
      ctx.fillRect(cx + 9, cy + 4, 5, 4);
      // Open lid
      ctx.fillStyle = '#522c15';
      ctx.beginPath();
      ctx.moveTo(cx - 14, cy - 8); ctx.lineTo(cx - 17, cy - 16); ctx.lineTo(cx + 17, cy - 16); ctx.lineTo(cx + 14, cy - 8);
      ctx.closePath(); ctx.fill();
      ctx.strokeStyle = '#ffd700'; ctx.stroke();
      // Chalice
      ctx.fillStyle = '#ffd700';
      ctx.beginPath();
      ctx.moveTo(cx + 17, cy - 2); ctx.lineTo(cx + 23, cy - 2); ctx.lineTo(cx + 21, cy + 6); ctx.lineTo(cx + 19, cy + 6);
      ctx.closePath(); ctx.fill();
      // Coins & gems
      ctx.fillStyle = '#ffd700';
      [-10, -6, -2, 2, 6, 10].forEach((dx, i) => {
        ctx.beginPath(); ctx.arc(cx + dx, cy - 8 - (i % 3), 2.8, 0, Math.PI * 2); ctx.fill();
      });
      ctx.fillStyle = '#e74c3c';
      ctx.beginPath(); ctx.arc(cx - 1, cy - 6, 2, 0, Math.PI * 2); ctx.fill();
    }

    // 6. Nottingham Mead Cask
    if (backdropProps.meadCask || equippedLoot[2]) {
      const bx = 270, by = 376;
      ctx.fillStyle = '#6d4427';
      ctx.beginPath(); ctx.ellipse(bx, by, 11, 15, 0, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = '#2c3e50'; ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(bx - 10, by - 7); ctx.lineTo(bx + 10, by - 7);
      ctx.moveTo(bx - 11, by + 5); ctx.lineTo(bx + 11, by + 5);
      ctx.stroke();
      ctx.fillStyle = '#f5cd47'; ctx.fillRect(bx - 15, by - 2, 5, 4);
      ctx.fillStyle = '#4a2f1b'; ctx.fillRect(bx - 23, by + 2, 7, 9);
      ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.ellipse(bx - 20, by + 1, 5, 3, 0, 0, Math.PI * 2); ctx.fill();
    }

    // 7. Forest Feast Basket
    if (backdropProps.feastBasket || equippedLoot[7]) {
      const fx2 = 250, fy2 = 383;
      ctx.fillStyle = '#8c5828';
      ctx.beginPath(); ctx.ellipse(fx2, fy2, 10, 6, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#a46d38'; ctx.fillRect(fx2 - 6, fy2 - 4, 12, 3);
      ctx.fillStyle = '#e74c3c';
      ctx.beginPath(); ctx.arc(fx2 - 2, fy2 - 5, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#f39c12';
      ctx.beginPath(); ctx.ellipse(fx2 + 3, fy2 - 4, 4, 2.5, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#8e44ad';
      ctx.beginPath(); ctx.arc(fx2 + 6, fy2 - 2, 2, 0, Math.PI * 2); ctx.fill();
    }
  }

  """

text = text[:s_camp] + new_camp + text[e_camp:]
print("Updated drawCamp successfully!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
