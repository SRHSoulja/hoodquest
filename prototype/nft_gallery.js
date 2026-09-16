/**
 * HoodQuest (HQ) - Royal Armory & Menagerie Showcase Gallery
 * Interactive on-chain vector art viewer and metadata inspector for all ecosystem NFTs:
 * - 3 Companions (ERC-721: Camp Hound, Hunting Falcon, Barn Owl)
 * - 13 Weapons, Armor, Relics & Materials (ERC-1155)
 */

(() => {
  // SVG Generation Helpers
  const SVG_DEFS = {
    // 🐕 Camp Hound (ERC-721)
    campHound: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
          <radialGradient id="houndBg" cx="50%" cy="50%" r="70%">
            <stop offset="0%" stop-color="#1b2d1c"/>
            <stop offset="60%" stop-color="#0e1a10"/>
            <stop offset="100%" stop-color="#060d07"/>
          </radialGradient>
        </defs>
        <rect width="400" height="400" rx="16" fill="url(#houndBg)"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-opacity="0.7"/>
        <rect x="20" y="20" width="360" height="360" rx="8" fill="none" stroke="#997825" stroke-width="1" stroke-dasharray="6,4"/>
        
        <ellipse cx="200" cy="330" rx="140" ry="38" fill="#1b3d1f"/>
        <ellipse cx="200" cy="328" rx="120" ry="28" fill="#2d5e34"/>

        <!-- Wagging Tail -->
        <path d="M125,270 Q95,240 85,205 Q90,200 96,206 Q110,245 138,272 Z" fill="#6d4327" stroke="#4a2c16" stroke-width="1.5"/>
        
        <!-- Hind Quarters -->
        <ellipse cx="150" cy="275" rx="38" ry="32" transform="rotate(-15 150 275)" fill="#55341e"/>
        <ellipse cx="145" cy="298" rx="16" ry="12" fill="#4a2c16"/>

        <!-- Torso & Tan Chest -->
        <ellipse cx="195" cy="245" rx="42" ry="52" transform="rotate(18 195 245)" fill="#7a4b2c"/>
        <path d="M205,210 Q235,240 230,285 Q210,295 195,280 Q195,230 205,210 Z" fill="#d49b6a"/>

        <!-- Forelegs & Paws -->
        <rect x="212" y="260" width="18" height="60" rx="8" fill="#7a4b2c"/>
        <rect x="232" y="265" width="17" height="55" rx="7" fill="#6d4327"/>
        <ellipse cx="221" cy="320" rx="14" ry="8" fill="#55341e"/>
        <ellipse cx="240" cy="320" rx="13" ry="8" fill="#4a2c16"/>

        <!-- Studded Collar with Brass Sherwood Leaf -->
        <path d="M196,188 L242,202 L238,216 L192,202 Z" fill="#2d1a0d"/>
        <circle cx="204" cy="198" r="2.5" fill="#ffd700"/>
        <circle cx="218" cy="203" r="2.5" fill="#ffd700"/>
        <circle cx="232" cy="208" r="2.5" fill="#ffd700"/>
        <circle cx="220" cy="216" r="6" fill="#ffd700" stroke="#b8860b" stroke-width="1"/>

        <!-- Hound Head & Muzzle -->
        <ellipse cx="225" cy="155" rx="28" ry="26" fill="#7a4b2c"/>
        <path d="M198,145 Q180,180 185,215 Q195,220 202,210 Q205,175 210,150 Z" fill="#4a2914"/>
        <path d="M242,142 Q260,170 255,200 Q248,205 242,198 Q240,170 236,146 Z" fill="#3a2010"/>

        <ellipse cx="246" cy="166" rx="20" ry="15" fill="#55341e"/>
        <ellipse cx="244" cy="174" rx="14" ry="10" fill="#4a2c16"/>
        <path d="M256,158 Q264,158 263,165 Q260,170 255,168 Z" fill="#15100c"/>

        <!-- Loyal Eye -->
        <ellipse cx="230" cy="148" rx="5" ry="4.5" fill="#24140a"/>
        <circle cx="231" cy="147" r="2.5" fill="#d97706"/>
        <circle cx="232" cy="146.5" r="1.2" fill="#0f0905"/>
        <circle cx="232.5" cy="145.8" r="0.8" fill="#ffffff"/>

        <rect x="60" y="32" width="280" height="34" rx="6" fill="#142415" stroke="#d4af37" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="15" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">CAMP HOUND</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#10b981" text-anchor="middle" letter-spacing="1">ERC-721 COMPANION • 400 MAX SUPPLY</text>
      </svg>
    `,

    // 🦅 Hunting Falcon (ERC-721)
    huntingFalcon: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
          <radialGradient id="falconBg" cx="50%" cy="40%" r="75%">
            <stop offset="0%" stop-color="#1e293b"/>
            <stop offset="60%" stop-color="#0f172a"/>
            <stop offset="100%" stop-color="#020617"/>
          </radialGradient>
        </defs>
        <rect width="400" height="400" rx="16" fill="url(#falconBg)"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-opacity="0.6"/>

        <!-- Perch Post -->
        <rect x="188" y="250" width="24" height="130" rx="4" fill="#3e2723"/>
        <rect x="165" y="244" width="70" height="10" rx="5" fill="#5d4037"/>

        <!-- Braided Golden Jesses -->
        <path d="M190,250 Q180,285 175,320" stroke="#f59e0b" stroke-width="2.5" fill="none"/>
        <path d="M210,250 Q218,280 222,315" stroke="#f59e0b" stroke-width="2.5" fill="none"/>

        <!-- Talons Gripping Perch -->
        <ellipse cx="188" cy="248" rx="10" ry="6" fill="#f59e0b"/>
        <ellipse cx="212" cy="248" rx="10" ry="6" fill="#f59e0b"/>

        <!-- Falcon Anatomy -->
        <polygon points="190,265 210,265 204,335 196,335" fill="#1e293b"/>
        <ellipse cx="200" cy="195" rx="30" ry="48" fill="#f8fafc"/>
        <path d="M185,180 Q200,183 215,180 M182,195 Q200,198 218,195 M186,210 Q200,213 214,210 M190,225 Q200,227 210,225" stroke="#475569" stroke-width="2.5" fill="none"/>

        <path d="M172,160 Q150,210 178,280 Q192,270 190,210 Q185,175 172,160 Z" fill="#334155"/>
        <path d="M170,170 Q156,220 182,270" stroke="#64748b" stroke-width="1.8" fill="none"/>

        <!-- Head, Hooked Beak & Eye -->
        <circle cx="218" cy="140" r="22" fill="#1e293b"/>
        <path d="M200,140 Q215,120 236,132 Q230,155 215,160 Z" fill="#0f172a"/>
        <path d="M236,134 Q254,136 248,154 Q238,148 234,146 Z" fill="#f59e0b"/>
        <circle cx="224" cy="136" r="7" fill="#d97706"/>
        <circle cx="225" cy="135.5" r="4" fill="#020617"/>
        <circle cx="226.5" cy="134" r="1.5" fill="#ffffff"/>

        <rect x="60" y="32" width="280" height="34" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="15" font-weight="bold" fill="#e0f2fe" text-anchor="middle" letter-spacing="2">HUNTING FALCON</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle" letter-spacing="1">ERC-721 COMPANION • 250 MAX SUPPLY</text>
      </svg>
    `,

    // 🦉 Barn Owl (ERC-721)
    barnOwl: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
          <radialGradient id="owlBg" cx="50%" cy="45%" r="70%">
            <stop offset="0%" stop-color="#2d1b4e"/>
            <stop offset="50%" stop-color="#19102e"/>
            <stop offset="100%" stop-color="#0a0517"/>
          </radialGradient>
        </defs>
        <rect width="400" height="400" rx="16" fill="url(#owlBg)"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#c084fc" stroke-width="2.5" stroke-opacity="0.6"/>

        <circle cx="200" cy="175" r="110" fill="#fef08a" opacity="0.12"/>
        <circle cx="200" cy="175" r="85" fill="#fef08a" opacity="0.18"/>

        <!-- Mossy Hollow Log -->
        <rect x="110" y="270" width="180" height="45" rx="12" fill="#3e2723"/>
        <ellipse cx="200" cy="270" rx="90" ry="14" fill="#4e342e"/>
        <path d="M130,268 Q150,262 170,268 Q180,260 200,268" stroke="#22c55e" stroke-width="6" stroke-linecap="round" fill="none"/>

        <!-- Feathered Feet -->
        <ellipse cx="178" cy="268" rx="14" ry="8" fill="#f8fafc"/>
        <ellipse cx="222" cy="268" rx="14" ry="8" fill="#f8fafc"/>

        <!-- Body & Wings -->
        <ellipse cx="200" cy="205" rx="44" ry="58" fill="#d97706"/>
        <ellipse cx="200" cy="208" rx="30" ry="46" fill="#fffbeb"/>
        <ellipse cx="158" cy="205" rx="16" ry="50" transform="rotate(8 158 205)" fill="#92400e"/>
        <ellipse cx="242" cy="205" rx="16" ry="50" transform="rotate(-8 242 205)" fill="#92400e"/>

        <!-- Heart Facial Disc -->
        <path d="M200,172 C165,135 155,105 180,95 C195,88 200,105 200,110 C200,105 205,88 220,95 C245,105 235,135 200,172 Z" fill="#b45309"/>
        <path d="M200,168 C168,133 160,107 182,98 C195,93 200,107 200,112 C200,107 205,93 218,98 C240,107 232,133 200,168 Z" fill="#ffffff"/>

        <!-- Dark Eyes with Golden Rings -->
        <circle cx="184" cy="126" r="11" fill="#78350f"/>
        <circle cx="184" cy="126" r="9.5" fill="#0f172a"/>
        <circle cx="182" cy="123" r="2.2" fill="#fbbf24"/>
        <circle cx="216" cy="126" r="11" fill="#78350f"/>
        <circle cx="216" cy="126" r="9.5" fill="#0f172a"/>
        <circle cx="214" cy="123" r="2.2" fill="#fbbf24"/>
        <path d="M198,132 L202,132 L200,146 Z" fill="#fef08a" stroke="#d97706" stroke-width="0.8"/>

        <rect x="60" y="32" width="280" height="34" rx="6" fill="#1e1035" stroke="#c084fc" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="15" font-weight="bold" fill="#f3e8ff" text-anchor="middle" letter-spacing="2">BARN OWL</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#c084fc" text-anchor="middle" letter-spacing="1">ERC-721 COMPANION • 150 MAX SUPPLY</text>
      </svg>
    `,

    // 🏹 Gilded Recurve Bow (ERC-1155 #3)
    gildedBow: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
          <radialGradient id="bowBg" cx="50%" cy="50%" r="75%">
            <stop offset="0%" stop-color="#2a1f11"/>
            <stop offset="60%" stop-color="#140e06"/>
            <stop offset="100%" stop-color="#080502"/>
          </radialGradient>
          <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#fef08a"/>
            <stop offset="40%" stop-color="#eab308"/>
            <stop offset="80%" stop-color="#ca8a04"/>
            <stop offset="100%" stop-color="#854d0e"/>
          </linearGradient>
        </defs>
        <rect width="400" height="400" rx="16" fill="url(#bowBg)"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#eab308" stroke-width="2.5"/>

        <!-- Double Curved Bow Stave -->
        <path d="M120,80 Q100,140 130,200 Q100,260 120,320 Q128,322 134,316 Q112,260 144,200 Q112,140 134,84 Z" fill="url(#goldGrad)" stroke="#713f12" stroke-width="2"/>
        <path d="M126,95 Q110,145 133,200 Q110,255 126,305" stroke="#78350f" stroke-width="3.5" fill="none"/>

        <!-- Antler Nocks & String -->
        <path d="M120,80 L115,70 L125,72 Z" fill="#fef3c7" stroke="#b45309" stroke-width="1.2"/>
        <path d="M120,320 L115,330 L125,328 Z" fill="#fef3c7" stroke="#b45309" stroke-width="1.2"/>
        <line x1="120" y1="74" x2="120" y2="326" stroke="#f8fafc" stroke-width="1.8"/>

        <!-- Velvet Grip & Crossing Arrow -->
        <rect x="132" y="186" width="15" height="28" rx="3" fill="#047857" stroke="#064e3b" stroke-width="1.5"/>
        <line x1="90" y1="200" x2="310" y2="200" stroke="#d97706" stroke-width="3"/>
        <polygon points="310,192 335,200 310,208 316,200" fill="#fde047" stroke="#854d0e" stroke-width="1.5"/>
        <polygon points="90,200 115,190 120,200 115,210" fill="#059669"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#1c1307" stroke="#eab308" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="15" font-weight="bold" fill="#fef08a" text-anchor="middle" letter-spacing="2">GILDED RECURVE BOW</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#eab308" text-anchor="middle" letter-spacing="1">ERC-1155 #3 • +20 ATK & +20% GOLD (1,000 CAP)</text>
      </svg>
    `,

    // ✨ The Golden Arrow (ERC-1155 #4 - Mythic Grail)
    goldenArrow: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
          <radialGradient id="arrowBg" cx="50%" cy="50%" r="75%">
            <stop offset="0%" stop-color="#3b1d11"/>
            <stop offset="50%" stop-color="#1f0e07"/>
            <stop offset="100%" stop-color="#0a0301"/>
          </radialGradient>
        </defs>
        <rect width="400" height="400" rx="16" fill="url(#arrowBg)"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#f59e0b" stroke-width="2.5"/>

        <circle cx="200" cy="200" r="140" fill="#fbbf24" opacity="0.1"/>
        <line x1="70" y1="330" x2="310" y2="90" stroke="#fef08a" stroke-width="5" stroke-linecap="round"/>
        <line x1="72" y1="328" x2="308" y2="92" stroke="#d97706" stroke-width="2"/>

        <polygon points="310,90 350,70 330,110 322,98" fill="#ffffff" stroke="#1d4ed8" stroke-width="1.5"/>
        <polygon points="70,330 60,300 85,305 85,325" fill="#ec4899"/>
        <polygon points="70,330 100,340 95,315 75,315" fill="#8b5cf6"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#2d1205" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">THE GOLDEN ARROW</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ef4444" text-anchor="middle" letter-spacing="1">MYTHIC GRAIL • EXACTLY 25 LIFETIME SUPPLY</text>
      </svg>
    `,

    // 🍇 Friar's Cornucopia (ERC-1155 #9 - Mythic Grail)
    cornucopia: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#1c1108"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#f59e0b" stroke-width="2.5"/>

        <circle cx="200" cy="200" r="120" fill="#fde047" opacity="0.12"/>
        <path d="M120,150 Q160,110 230,130 Q300,160 310,230 Q300,280 230,280 Q160,280 130,210 Z" fill="#92400e" stroke="#78350f" stroke-width="3"/>
        <path d="M120,150 Q80,180 90,220 Q105,250 140,240 Q170,230 180,180 Z" fill="#78350f"/>

        <!-- Harvest Bounty -->
        <circle cx="250" cy="220" r="22" fill="#dc2626"/>
        <circle cx="280" cy="245" r="18" fill="#ef4444"/>
        <circle cx="210" cy="255" r="10" fill="#6b21a8"/>
        <circle cx="225" cy="265" r="10" fill="#7e22ce"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#2d1705" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">FRIAR'S CORNUCOPIA</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ef4444" text-anchor="middle" letter-spacing="1">MYTHIC GRAIL • PERPETUAL FEEDER (25 CAP)</text>
      </svg>
    `,

    // 🪵 Sherwood Yew Log (ERC-1155 #16)
    sherwoodYew: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#0d170c"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-dasharray="8,4"/>

        <circle cx="200" cy="200" r="115" fill="#22c55e" opacity="0.09"/>
        <path d="M120,160 L280,140 L280,250 L120,270 Z" fill="#54331a" stroke="#38200f" stroke-width="3"/>
        <ellipse cx="120" cy="215" rx="30" ry="55" fill="#d97706" stroke="#451a03" stroke-width="3"/>
        <ellipse cx="120" cy="215" rx="20" ry="40" fill="#ea580c"/>
        <ellipse cx="120" cy="215" rx="10" ry="20" fill="#b91c1c"/>

        <path d="M190,195 L200,185 L210,195 M200,185 L200,210" stroke="#86efac" stroke-width="3" stroke-linecap="round" fill="none"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#0d2410" stroke="#22c55e" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#dcfce7" text-anchor="middle" letter-spacing="2">SHERWOOD YEW TIMBER</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#4ade80" text-anchor="middle" letter-spacing="1">ERC-1155 #16 • SOULBOUND CRAFTING TIMBER</text>
      </svg>
    `,

    // ⛏️ Nottingham Iron Ingot (ERC-1155 #17)
    nottinghamIron: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#0f172a"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#94a3b8" stroke-width="2.5" stroke-dasharray="8,4"/>

        <polygon points="100,240 140,160 290,160 250,240" fill="#64748b"/>
        <polygon points="100,240 250,240 230,270 80,270" fill="#334155"/>
        <polygon points="250,240 290,160 270,185 230,270" fill="#1e293b"/>
        <line x1="145" y1="165" x2="285" y2="165" stroke="#f8fafc" stroke-width="2.5" opacity="0.8"/>

        <rect x="175" y="185" width="40" height="32" rx="4" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
        <path d="M185,208 L185,195 L190,195 L190,198 L195,198 L195,195 L200,195 L200,198 L205,198 L205,195 L210,195 L210,208 Z" fill="#cbd5e1"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle" letter-spacing="2">NOTTINGHAM IRON STEEL</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle" letter-spacing="1">ERC-1155 #17 • SOULBOUND CRAFTING STEEL</text>
      </svg>
    `,

    // 🪙 Royal Gold Sovereign (ERC-1155 #1)
    goldSovereign: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
          <radialGradient id="sovereignGrad" cx="35%" cy="35%" r="65%">
            <stop offset="0%" stop-color="#fffbeb"/>
            <stop offset="30%" stop-color="#fef08a"/>
            <stop offset="70%" stop-color="#eab308"/>
            <stop offset="95%" stop-color="#a16207"/>
          </radialGradient>
        </defs>
        <rect width="400" height="400" rx="16" fill="#120c06"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#d97706" stroke-width="2.5"/>

        <circle cx="205" cy="205" r="105" fill="#713f12"/>
        <circle cx="200" cy="200" r="105" fill="url(#sovereignGrad)" stroke="#a16207" stroke-width="4"/>
        <circle cx="200" cy="200" r="92" fill="none" stroke="#713f12" stroke-width="2" stroke-dasharray="4,4"/>

        <!-- Embossed Crest -->
        <polygon points="200,140 230,188 210,188 210,246 190,246 190,188 170,188" fill="#fef08a"/>
        <path d="M175,130 L185,115 L200,125 L215,115 L225,130 Z" fill="#713f12"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#1c1107" stroke="#eab308" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">GOLD SOVEREIGN</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#eab308" text-anchor="middle" letter-spacing="1">ERC-1155 #1 • CANONICAL CORE CURRENCY</text>
      </svg>
    `,

    // 🍺 Vintage Nottingham Mead Cask (ERC-1155 #2)
    meadCask: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#170f09"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#d97706" stroke-width="2.5"/>

        <ellipse cx="200" cy="210" rx="80" ry="95" fill="#78350f" stroke="#451a03" stroke-width="3"/>
        <path d="M125,160 Q200,175 275,160" stroke="#1e293b" stroke-width="8" fill="none"/>
        <path d="M120,210 Q200,225 280,210" stroke="#1e293b" stroke-width="8" fill="none"/>
        <path d="M125,260 Q200,275 275,260" stroke="#1e293b" stroke-width="8" fill="none"/>

        <rect x="190" y="210" width="20" height="12" rx="2" fill="#f59e0b"/>
        <path d="M209,238 Q209,270 215,290" stroke="#fef08a" stroke-width="3" stroke-linecap="round" fill="none"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#1c1107" stroke="#d97706" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">NOTTINGHAM MEAD CASK</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#f59e0b" text-anchor="middle" letter-spacing="1">ERC-1155 #2 • CAMP BANTER & HEARTH HAPPINESS</text>
      </svg>
    `,

    // 🧪 Greenwood Alchemical Elixir (ERC-1155 #5)
    greenwoodElixir: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#08140c"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#10b981" stroke-width="2.5"/>

        <circle cx="200" cy="225" r="95" fill="#10b981" opacity="0.18"/>
        <path d="M185,130 L215,130 L215,165 L260,255 C275,285 255,305 200,305 C145,305 125,285 140,255 L185,165 Z" fill="#064e3b" opacity="0.4" stroke="#6ee7b7" stroke-width="2.5"/>
        <path d="M152,240 C175,235 225,245 248,240 L256,260 C265,282 245,298 200,298 C155,298 135,282 144,260 Z" fill="#10b981"/>
        <circle cx="185" cy="265" r="4" fill="#ffffff" opacity="0.8"/>
        <rect x="187" y="112" width="26" height="20" rx="3" fill="#92400e"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#062e1a" stroke="#10b981" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#d1fae5" text-anchor="middle" letter-spacing="2">GREENWOOD ELIXIR</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#34d399" text-anchor="middle" letter-spacing="1">ERC-1155 #5 • +5 HEISTS / DAY CONSUMABLE</text>
      </svg>
    `,

    // 🧥 Locksley Velvet Cloak (ERC-1155 #6)
    locksleyCloak: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#08170c"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#22c55e" stroke-width="2.5"/>

        <path d="M170,120 Q200,105 230,120 Q285,280 300,320 Q200,340 100,320 Q115,280 170,120 Z" fill="#14532d" stroke="#052e16" stroke-width="3"/>
        <path d="M100,320 Q200,340 300,320" stroke="#f59e0b" stroke-width="5" fill="none"/>
        <circle cx="178" cy="125" r="9" fill="#f59e0b" stroke="#78350f" stroke-width="1.5"/>
        <circle cx="222" cy="125" r="9" fill="#f59e0b" stroke="#78350f" stroke-width="1.5"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#0c2e17" stroke="#22c55e" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#f0fdf4" text-anchor="middle" letter-spacing="2">LOCKSLEY VELVET CLOAK</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#4ade80" text-anchor="middle" letter-spacing="1">ERC-1155 #6 • +20 DEF & STEALTH AMBUSH SHIELD</text>
      </svg>
    `,

    // 🧺 Forest Feast Basket (ERC-1155 #7)
    feastBasket: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#171108"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#d97706" stroke-width="2.5"/>

        <path d="M120,200 L280,200 L260,300 L140,300 Z" fill="#92400e" stroke="#78350f" stroke-width="3"/>
        <path d="M140,200 Q200,110 260,200" stroke="#b45309" stroke-width="6" fill="none"/>
        <ellipse cx="170" cy="185" rx="30" ry="18" fill="#d97706"/>
        <circle cx="200" cy="190" r="14" fill="#dc2626"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#241508" stroke="#d97706" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">FOREST FEAST BASKET</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#f59e0b" text-anchor="middle" letter-spacing="1">ERC-1155 #7 • 7-DAY RATIONS (PREVENTS STARVATION)</text>
      </svg>
    `,

    // 📯 Silver Rallying Horn (ERC-1155 #8)
    rallyHorn: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#0f172a"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#94a3b8" stroke-width="2.5"/>

        <path d="M120,240 Q160,280 240,250 Q280,230 280,160 Q270,160 260,180 Q250,220 220,225 Q160,240 120,210 Z" fill="#cbd5e1" stroke="#475569" stroke-width="2.5"/>
        <ellipse cx="280" cy="160" rx="18" ry="10" fill="#94a3b8" stroke="#334155" stroke-width="2"/>
        <path d="M295,145 Q315,160 295,175" stroke="#f59e0b" stroke-width="2" fill="none"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle" letter-spacing="2">SILVER RALLYING HORN</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle" letter-spacing="1">ERC-1155 #8 • +10 ATK PARTY MORALE AURA</text>
      </svg>
    `,

    // 🪵 Oak Quarterstaff (ERC-1155 #14)
    quarterstaff: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#140f0a"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#78350f" stroke-width="2.5"/>

        <line x1="80" y1="320" x2="320" y2="80" stroke="#78350f" stroke-width="10" stroke-linecap="round"/>
        <line x1="82" y1="318" x2="318" y2="82" stroke="#92400e" stroke-width="4"/>
        <rect x="300" y="82" width="18" height="18" rx="2" transform="rotate(-45 309 91)" fill="#475569" stroke="#0f172a" stroke-width="1.5"/>
        <rect x="82" y="300" width="18" height="18" rx="2" transform="rotate(-45 91 309)" fill="#475569" stroke="#0f172a" stroke-width="1.5"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#241407" stroke="#78350f" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#fef3c7" text-anchor="middle" letter-spacing="2">OAK QUARTERSTAFF</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#d97706" text-anchor="middle" letter-spacing="1">ERC-1155 #14 • +15 DEF & BRAWLER STUN STRIKE</text>
      </svg>
    `,

    // 🗡️ Poacher's Twin Daggers (ERC-1155 #15)
    twinDaggers: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <rect width="400" height="400" rx="16" fill="#0b1117"/>
        <rect x="14" y="14" width="372" height="372" rx="12" fill="none" stroke="#64748b" stroke-width="2.5"/>

        <line x1="110" y1="290" x2="290" y2="110" stroke="#cbd5e1" stroke-width="4.5" stroke-linecap="round"/>
        <line x1="290" y1="290" x2="110" y2="110" stroke="#cbd5e1" stroke-width="4.5" stroke-linecap="round"/>
        <rect x="150" y="245" width="22" height="6" rx="2" transform="rotate(-45 161 248)" fill="#ffd700"/>
        <rect x="230" y="245" width="22" height="6" rx="2" transform="rotate(45 241 248)" fill="#ffd700"/>

        <rect x="50" y="32" width="300" height="34" rx="6" fill="#17222c" stroke="#64748b" stroke-width="1.5"/>
        <text x="200" y="54" font-family="'Cinzel', 'Georgia', serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle" letter-spacing="2">TWIN POACHER'S DAGGERS</text>
        <text x="200" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle" letter-spacing="1">ERC-1155 #15 • +15 STEALTH & DUAL CRITICALS</text>
      </svg>
    `
  };

  // NFT Item Catalog Definition
  const ALL_NFTS = [
    // Companions
    {
      id: 'hound',
      category: 'companions',
      contract: 'ERC-721',
      name: 'The Camp Hound',
      title: 'Forest Tracker',
      rarity: 'Common Companion',
      cap: '400 Max Supply',
      stats: '+15% Yew Wood Drops • +10 DEF',
      icon: '🐕',
      desc: 'Faithful Greenwood bloodhound. Tracks Nottingham tax carts through dense bracken and scents fallen yew boughs.',
      svgKey: 'campHound',
      traits: [
        { trait_type: 'Species', value: 'Bloodhound' },
        { trait_type: 'Role', value: 'Forest Tracker' },
        { trait_type: 'Max Supply', value: '400' },
        { trait_type: 'Perk', value: '+15% Sherwood Yew Drops' },
        { trait_type: 'Stat Boost', value: '+10 DEF' }
      ]
    },
    {
      id: 'falcon',
      category: 'companions',
      contract: 'ERC-721',
      name: 'The Hunting Falcon',
      title: 'Aerial Scout',
      rarity: 'Uncommon Companion',
      cap: '250 Max Supply',
      stats: '+12% Nottingham Iron Drops • +Crit Chance',
      icon: '🦅',
      desc: 'Piercing-eyed peregrine falcon. Circles high above Sherwood canopy to spot armed Nottingham royal weapon transports.',
      svgKey: 'huntingFalcon',
      traits: [
        { trait_type: 'Species', value: 'Peregrine Falcon' },
        { trait_type: 'Role', value: 'Aerial Scout' },
        { trait_type: 'Max Supply', value: '250' },
        { trait_type: 'Perk', value: '+12% Nottingham Iron Drops' },
        { trait_type: 'Stat Boost', value: '+5% Crit Chance' }
      ]
    },
    {
      id: 'owl',
      category: 'companions',
      contract: 'ERC-721',
      name: 'The Barn Owl',
      title: 'Silent Shadow',
      rarity: 'Rare Companion',
      cap: '150 Max Supply',
      stats: '+10% Bonus Gold Looted • +Stealth',
      icon: '🦉',
      desc: 'Heart-faced nocturnal raptor. Glides with utter silence through moonlit branches, guiding outlaws safely past town sentries.',
      svgKey: 'barnOwl',
      traits: [
        { trait_type: 'Species', value: 'Barn Owl' },
        { trait_type: 'Role', value: 'Silent Shadow' },
        { trait_type: 'Max Supply', value: '150' },
        { trait_type: 'Perk', value: '+10% Bonus Gold Looted' },
        { trait_type: 'Stat Boost', value: '+15 Stealth' }
      ]
    },

    // Weapons & Armor
    {
      id: 'item3',
      category: 'weapons',
      contract: 'ERC-1155 #3',
      name: 'Gilded Recurve Bow',
      title: 'Apex Archery Weapon',
      rarity: 'Rare Weapon',
      cap: '1,000 Circulating Cap',
      stats: '+20 ATK • +20% Gold Multiplier',
      icon: '🏹',
      desc: 'Masterwork recurve bow carved from aged Sherwood yew and chased in 24k royal gold filigree. Premier gold-farming weapon.',
      svgKey: 'gildedBow',
      traits: [
        { trait_type: 'Item Type', value: 'Weapon' },
        { trait_type: 'ATK Boost', value: '+20 ATK' },
        { trait_type: 'Gold Perk', value: '+20% Gold Yield' },
        { trait_type: 'Hard Cap', value: '1,000' }
      ]
    },
    {
      id: 'item4',
      category: 'weapons',
      contract: 'ERC-1155 #4',
      name: 'The Golden Arrow',
      title: 'Nottingham Tournament Grail',
      rarity: 'Mythic Grail',
      cap: '25 Lifetime Minted',
      stats: '+25 ATK (Highest Single Item in Game)',
      icon: '✨',
      desc: 'The legendary prize of the Sherwood Archery Tournament. Solid gold shaft with diamond chisel head. Exactly 25 will ever exist.',
      svgKey: 'goldenArrow',
      traits: [
        { trait_type: 'Rarity', value: 'Mythic Grail' },
        { trait_type: 'ATK Boost', value: '+25 ATK' },
        { trait_type: 'Lifetime Cap', value: '25' },
        { trait_type: 'Provenance', value: 'Annual Tournament Prize' }
      ]
    },
    {
      id: 'item14',
      category: 'weapons',
      contract: 'ERC-1155 #14',
      name: 'Oak Quarterstaff',
      title: 'Brawler River Guard',
      rarity: 'Uncommon Weapon',
      cap: '2,500 Circulating Cap',
      stats: '+15 DEF • Road-Block Stun',
      icon: '🪵',
      desc: 'Seven feet of seasoned English oak shod in hammered iron rings. Little John’s weapon of choice for defending woodland crossings.',
      svgKey: 'quarterstaff',
      traits: [
        { trait_type: 'Item Type', value: 'Weapon' },
        { trait_type: 'DEF Boost', value: '+15 DEF' },
        { trait_type: 'Combat Skill', value: 'Log Bridge Stun' },
        { trait_type: 'Hard Cap', value: '2,500' }
      ]
    },
    {
      id: 'item15',
      category: 'weapons',
      contract: 'ERC-1155 #15',
      name: "Poacher's Twin Daggers",
      title: 'Silent Stiletto Pair',
      rarity: 'Uncommon Weapon',
      cap: '1,500 Circulating Cap',
      stats: '+15 STEALTH • Dual Critical Strikes',
      icon: '🗡️',
      desc: 'Matched Damascus stiletto blades with stag antler grips and ruby pommels. Favored by Maid Marian for court infiltration.',
      svgKey: 'twinDaggers',
      traits: [
        { trait_type: 'Item Type', value: 'Weapon' },
        { trait_type: 'Stealth Boost', value: '+15 STEALTH' },
        { trait_type: 'Combat Skill', value: 'Silent Ambush' },
        { trait_type: 'Hard Cap', value: '1,500' }
      ]
    },
    {
      id: 'item6',
      category: 'weapons',
      contract: 'ERC-1155 #6',
      name: 'Locksley Velvet Cloak',
      title: 'Noble Camouflage',
      rarity: 'Rare Armor',
      cap: '750 Circulating Cap',
      stats: '+20 DEF / STEALTH • Ambush Damage Shield',
      icon: '🧥',
      desc: 'Deep green velvet trimmed with gold embroidery and brass oak-leaf clasps. Provides heavy defense against Sheriff ambushes.',
      svgKey: 'locksleyCloak',
      traits: [
        { trait_type: 'Item Type', value: 'Armor' },
        { trait_type: 'DEF Boost', value: '+20 DEF' },
        { trait_type: 'Hard Cap', value: '750' }
      ]
    },

    // Relics & Sustenance
    {
      id: 'item9',
      category: 'relics',
      contract: 'ERC-1155 #9',
      name: "Friar's Cornucopia",
      title: 'Mythic Endless Feeder',
      rarity: 'Mythic Grail',
      cap: '25 Lifetime Minted',
      stats: 'Perpetual Camp Rations • Eliminates Food Sink',
      icon: '🍇',
      desc: 'Woven wicker horn of endless harvest won only in the 5-Year Climax World Boss battles. Keeps hero fed forever without gold cost.',
      svgKey: 'cornucopia',
      traits: [
        { trait_type: 'Rarity', value: 'Mythic Grail' },
        { trait_type: 'Perk', value: 'Infinite Camp Rations' },
        { trait_type: 'Lifetime Cap', value: '25' }
      ]
    },
    {
      id: 'item2',
      category: 'relics',
      contract: 'ERC-1155 #2',
      name: 'Nottingham Mead Cask',
      title: 'Hearth Brew',
      rarity: 'Uncommon Camp Relic',
      cap: '5,000 Circulating Cap',
      stats: 'Camp Happiness • Tavern Banter in SVG',
      icon: '🍺',
      desc: 'Oak cask filled with aged heather honey mead. Unlocks celebratory mug-drinking animations and tavern banter around the campfire.',
      svgKey: 'meadCask',
      traits: [
        { trait_type: 'Item Type', value: 'Camp Decor' },
        { trait_type: 'Aesthetic Perk', value: 'Hearth Banter & Foam' },
        { trait_type: 'Hard Cap', value: '5,000' }
      ]
    },
    {
      id: 'item5',
      category: 'relics',
      contract: 'ERC-1155 #5',
      name: 'Greenwood Alchemical Elixir',
      title: 'Stamina Phial',
      rarity: 'Consumable Elixir',
      cap: '2,500 Circulating Cap',
      stats: '+5 Heists / Day Consumable',
      icon: '🧪',
      desc: 'Bubbling emerald distillation of forest herbs prepared by Mother Meg. Restores +5 heist attempts (limited to 1 per day).',
      svgKey: 'greenwoodElixir',
      traits: [
        { trait_type: 'Item Type', value: 'Consumable' },
        { trait_type: 'Stamina Perk', value: '+5 Daily Heists' },
        { trait_type: 'Daily Limit', value: '1 Drink / Day' }
      ]
    },
    {
      id: 'item7',
      category: 'relics',
      contract: 'ERC-1155 #7',
      name: 'Forest Feast Basket',
      title: 'Camp Provisions',
      rarity: 'Common Sustenance',
      cap: 'Uncapped Supply (Crafted)',
      stats: '7-Day Rations • Prevents 50% Starvation Penalty',
      icon: '🧺',
      desc: 'Willow basket filled with crusty loaves, roasted fowl, and cheeses. Prevents the 50% starvation penalty and ward against cold slumber.',
      svgKey: 'feastBasket',
      traits: [
        { trait_type: 'Item Type', value: 'Sustenance' },
        { trait_type: 'Ration Duration', value: '7 Days' },
        { trait_type: 'Starvation Shield', value: 'Active' }
      ]
    },
    {
      id: 'item8',
      category: 'relics',
      contract: 'ERC-1155 #8',
      name: 'Silver Rallying Horn',
      title: 'Battle Horn',
      rarity: 'Rare Party Gear',
      cap: '500 Circulating Cap',
      stats: '+10 ATK Party Morale Aura',
      icon: '📯',
      desc: 'Engraved silver horn that sounds across the forest, rallying companion outlaws and granting +10 ATK to all party members in raid.',
      svgKey: 'rallyHorn',
      traits: [
        { trait_type: 'Item Type', value: 'Party Gear' },
        { trait_type: 'Party Aura', value: '+10 ATK Morale' },
        { trait_type: 'Hard Cap', value: '500' }
      ]
    },

    // Soulbound Materials & Currency
    {
      id: 'item1',
      category: 'materials',
      contract: 'ERC-1155 #1',
      name: 'Royal Gold Sovereign',
      title: 'Universal Realm Currency',
      rarity: 'Canonical Currency',
      cap: 'Dynamic Disinflationary',
      stats: 'Primary In-Game Currency & Crafting Burn',
      icon: '🪙',
      desc: 'Solid minted royal gold coins looted from the Sheriff’s tax carriages. Burned in smart contracts to craft all equipment.',
      svgKey: 'goldSovereign',
      traits: [
        { trait_type: 'Item Type', value: 'Currency' },
        { trait_type: 'Standard', value: 'OpenZeppelin ERC-1155 Burnable' }
      ]
    },
    {
      id: 'item16',
      category: 'materials',
      contract: 'ERC-1155 #16',
      name: 'Sherwood Yew Timber',
      title: 'Proof-of-Play Timber',
      rarity: 'Soulbound Material',
      cap: 'Non-Transferable (Bound)',
      stats: 'Essential for Bow & Staff Woodcraft',
      icon: '🪵',
      desc: 'Dense, flexible heartwood from ancient Sherwood yew trees. Dropped exclusively from active questing. Cannot be bought or sold.',
      svgKey: 'sherwoodYew',
      traits: [
        { trait_type: 'Item Type', value: 'Soulbound Material' },
        { trait_type: 'Drop Rate', value: '25% on Successful Heist' },
        { trait_type: 'Transferable', value: 'FALSE (Proof of Play)' }
      ]
    },
    {
      id: 'item17',
      category: 'materials',
      contract: 'ERC-1155 #17',
      name: 'Nottingham Iron Steel',
      title: 'Proof-of-Play Steel',
      rarity: 'Soulbound Material',
      cap: 'Non-Transferable (Bound)',
      stats: 'Essential for Blades, Staves & Armor',
      icon: '⛏️',
      desc: 'Cold-forged pig iron stamped with the royal castle seal. Dropped from carriage heists and used to forge stiletto blades and armor.',
      svgKey: 'nottinghamIron',
      traits: [
        { trait_type: 'Item Type', value: 'Soulbound Material' },
        { trait_type: 'Drop Rate', value: '20% on Successful Heist' },
        { trait_type: 'Transferable', value: 'FALSE (Proof of Play)' }
      ]
    }
  ];

  // UI Modal Construction
  function injectGalleryModal() {
    if (document.getElementById('nftGalleryModal')) return;

    const modalHtml = `
      <div id="nftGalleryModal" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(4,9,6,0.92); backdrop-filter:blur(10px); align-items:center; justify-content:center; padding:16px;">
        <div style="background:#0c160e; border:2px solid #2e4726; border-radius:14px; max-width:1050px; width:100%; height:90vh; max-height:860px; display:flex; flex-direction:column; overflow:hidden; box-shadow:0 12px 48px rgba(0,0,0,0.8);">
          
          <!-- Header -->
          <div style="display:flex; align-items:center; justify-content:space-between; padding:16px 24px; border-bottom:1px solid #1e331a; background:#071009;">
            <div style="display:flex; align-items:center; gap:12px;">
              <span style="font-size:24px;">🏛️</span>
              <div>
                <h2 style="font-family:'Cinzel', Georgia, serif; font-size:18px; color:#ffd700; margin:0; letter-spacing:1.5px;">ROYAL ARMORY & MENAGERIE SHOWCASE</h2>
                <div style="font-size:12px; color:#88b04b;">High-Fidelity Standalone On-Chain Vector Artworks & Metadata Invariants</div>
              </div>
            </div>
            <button id="btnCloseGalleryModal" style="background:#1a2b16; border:1px solid #3b5731; color:#fef3c7; font-size:18px; width:36px; height:36px; border-radius:50%; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:0.2s;">✕</button>
          </div>

          <!-- Filter Tabs -->
          <div style="display:flex; gap:10px; padding:12px 24px; border-bottom:1px solid #172814; background:#09140b; overflow-x:auto;">
            <button class="gallery-tab active" data-cat="all" style="padding:7px 14px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer; background:#2e4726; color:#ffd700; border:1px solid #4a733e;">🌟 All Items (16)</button>
            <button class="gallery-tab" data-cat="companions" style="padding:7px 14px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer; background:#122012; color:#a1cf7e; border:1px solid #23361e;">🐾 Companions (ERC-721)</button>
            <button class="gallery-tab" data-cat="weapons" style="padding:7px 14px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer; background:#122012; color:#a1cf7e; border:1px solid #23361e;">🏹 Weapons & Armor</button>
            <button class="gallery-tab" data-cat="relics" style="padding:7px 14px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer; background:#122012; color:#a1cf7e; border:1px solid #23361e;">🏺 Relics & Sustenance</button>
            <button class="gallery-tab" data-cat="materials" style="padding:7px 14px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer; background:#122012; color:#a1cf7e; border:1px solid #23361e;">🪵 Soulbound Materials</button>
          </div>

          <!-- Main Content Area: Left Grid + Right Inspector -->
          <div style="flex:1; display:flex; overflow:hidden;">
            <!-- Left: Card Grid -->
            <div id="galleryCardGrid" style="flex:1.2; padding:18px; overflow-y:auto; display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:14px; border-right:1px solid #172814;">
            </div>

            <!-- Right: Detailed Inspector Panel -->
            <div id="galleryInspector" style="flex:1; padding:20px; overflow-y:auto; background:#071008; display:flex; flex-direction:column; gap:16px;">
            </div>
          </div>
        </div>
      </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = modalHtml;
    document.body.appendChild(div.firstElementChild);

    // Event listeners
    document.getElementById('btnCloseGalleryModal')?.addEventListener('click', () => {
      document.getElementById('nftGalleryModal').style.display = 'none';
    });

    const tabs = document.querySelectorAll('.gallery-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => {
          t.style.background = '#122012';
          t.style.color = '#a1cf7e';
          t.style.borderColor = '#23361e';
        });
        tab.style.background = '#2e4726';
        tab.style.color = '#ffd700';
        tab.style.borderColor = '#4a733e';
        renderGrid(tab.getAttribute('data-cat'));
      });
    });

    renderGrid('all');
    selectNft(ALL_NFTS[0].id);
  }

  function renderGrid(category) {
    const grid = document.getElementById('galleryCardGrid');
    if (!grid) return;

    const filtered = category === 'all' ? ALL_NFTS : ALL_NFTS.filter(n => n.category === category);

    grid.innerHTML = filtered.map(item => `
      <div class="gallery-card" data-id="${item.id}" style="background:#101d12; border:1px solid #23361e; border-radius:10px; padding:10px; cursor:pointer; display:flex; flex-direction:column; gap:8px; transition:0.2s;">
        <div style="aspect-ratio:1/1; border-radius:8px; overflow:hidden; background:#040905; border:1px solid #1c2b18; display:flex; align-items:center; justify-content:center;">
          ${SVG_DEFS[item.svgKey] || `<div style="font-size:42px;">${item.icon}</div>`}
        </div>
        <div>
          <div style="font-size:10px; color:#88b04b; text-transform:uppercase; font-weight:bold;">${item.contract}</div>
          <div style="font-size:13px; font-weight:bold; color:#fef3c7; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${item.name}</div>
          <div style="font-size:11px; color:#ffd700;">${item.rarity}</div>
        </div>
      </div>
    `).join('');

    grid.querySelectorAll('.gallery-card').forEach(card => {
      card.addEventListener('click', () => {
        selectNft(card.getAttribute('data-id'));
      });
    });

    if (filtered.length > 0) {
      selectNft(filtered[0].id);
    }
  }

  function selectNft(id) {
    const item = ALL_NFTS.find(n => n.id === id);
    if (!item) return;

    document.querySelectorAll('.gallery-card').forEach(c => {
      if (c.getAttribute('data-id') === id) {
        c.style.borderColor = '#ffd700';
        c.style.background = '#182b1b';
        c.style.boxShadow = '0 0 12px rgba(255,215,0,0.35)';
      } else {
        c.style.borderColor = '#23361e';
        c.style.background = '#101d12';
        c.style.boxShadow = 'none';
      }
    });

    const inspector = document.getElementById('galleryInspector');
    if (!inspector) return;
    inspector.scrollTop = 0;

    const svgContent = SVG_DEFS[item.svgKey] || `<div style="font-size:80px; text-align:center;">${item.icon}</div>`;

    inspector.innerHTML = `
      <div style="aspect-ratio:1/1; max-width:320px; width:100%; margin:0 auto; border-radius:12px; overflow:hidden; border:2px solid #3b5731; box-shadow:0 8px 30px rgba(0,0,0,0.6); background:#050d06;">
        ${svgContent}
      </div>

      <div style="border-top:1px solid #1e331a; padding-top:14px; display:flex; flex-direction:column; gap:10px;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
          <div>
            <span style="font-size:11px; font-weight:bold; color:#88b04b; background:#122414; padding:2px 8px; border-radius:4px; border:1px solid #233d20;">${item.contract}</span>
            <h3 style="font-family:'Cinzel', Georgia, serif; font-size:19px; color:#ffd700; margin:4px 0 0 0;">${item.name}</h3>
          </div>
          <span style="font-size:12px; font-weight:bold; color:#f59e0b; background:#241606; padding:4px 10px; border-radius:6px; border:1px solid #78350f;">${item.rarity}</span>
        </div>

        <div style="font-size:12px; color:#dcfce7; line-height:1.45; background:#0e1c10; padding:10px 12px; border-radius:8px; border:1px solid #1c3319;">
          ${item.desc}
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:12px;">
          <div style="background:#0b160d; border:1px solid #1d3319; border-radius:6px; padding:8px 10px;">
            <div style="color:#88b04b; font-size:10px; text-transform:uppercase;">Combat / Utility Perk</div>
            <div style="color:#ffd700; font-weight:bold; margin-top:2px;">${item.stats}</div>
          </div>
          <div style="background:#0b160d; border:1px solid #1d3319; border-radius:6px; padding:8px 10px;">
            <div style="color:#88b04b; font-size:10px; text-transform:uppercase;">Statutory Supply Cap</div>
            <div style="color:#f8fafc; font-weight:bold; margin-top:2px;">${item.cap}</div>
          </div>
        </div>

        <div>
          <div style="font-size:11px; color:#88b04b; font-weight:bold; margin-bottom:6px; text-transform:uppercase;">On-Chain OpenSea Traits Preview:</div>
          <div style="display:flex; flex-wrap:wrap; gap:6px;">
            ${item.traits.map(t => `
              <div style="background:#132415; border:1px solid #2b4526; border-radius:6px; padding:4px 8px; font-size:11px;">
                <span style="color:#88b04b; font-size:9px; display:block; text-transform:uppercase;">${t.trait_type}</span>
                <span style="color:#fef3c7; font-weight:bold;">${t.value}</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  window.openNftGallery = function() {
    injectGalleryModal();
    const modal = document.getElementById('nftGalleryModal');
    if (modal) modal.style.display = 'flex';
  };

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#btnOpenNftGallery, .btn-open-nft-gallery').forEach(btn => {
      btn.addEventListener('click', window.openNftGallery);
    });
  });
})();
