"""
ForkDog Visualizer - Dog Edition
"""

import math
import json
import time
from pathlib import Path
from typing import Dict, List
from src.genetics import DogDNA, TraitCategory, Rarity

class DogVisualizer:
    """Generates generic SVG dog art from DNA"""

    BODY_COLORS = {
        "brown": {"main": "#8B4513", "shadow": "#5D2E0C", "highlight": "#A0522D"},
        "tan": {"main": "#D2B48C", "shadow": "#B8956E", "highlight": "#E8D4B8"},
        "beige": {"main": "#F5F5DC", "shadow": "#D4D4B8", "highlight": "#FFFFF0"},
        "gray": {"main": "#808080", "shadow": "#5A5A5A", "highlight": "#A0A0A0"},
        "golden": {"main": "#FFD700", "shadow": "#B8860B", "highlight": "#FFEC8B"},
        "silver": {"main": "#C0C0C0", "shadow": "#909090", "highlight": "#E8E8E8"},
        "copper": {"main": "#B87333", "shadow": "#8B5A2B", "highlight": "#D4A574"},
        "bronze": {"main": "#CD7F32", "shadow": "#8B5A2B", "highlight": "#DAA06D"},
        "white": {"main": "#FFFFFF", "shadow": "#E0E0E0", "highlight": "#FFFFFF"},
        "black": {"main": "#333333", "shadow": "#000000", "highlight": "#555555"},
        "spotted": {"main": "#FFFFFF", "shadow": "#E0E0E0", "highlight": "#FFFFFF"},
        "rainbow": {"main": "url(#rainbow-body)", "shadow": "#9400D3", "highlight": "#FFD700"},
        "galaxy": {"main": "url(#galaxy-body)", "shadow": "#1A0033", "highlight": "#E6E6FA"},
        "holographic": {"main": "url(#holo-body)", "shadow": "#4B0082", "highlight": "#FFFFFF"},
        "crystal": {"main": "#E0FFFF", "shadow": "#87CEEB", "highlight": "#FFFFFF"},
    }

    BACKGROUNDS = {
        "white": {"type": "solid", "color": "#F8F9FA"},
        "blue_sky": {"type": "gradient", "id": "sky-gradient"},
        "green_grass": {"type": "gradient", "id": "grass-gradient"},
        "sunset": {"type": "gradient", "id": "sunset-gradient"},
        "forest": {"type": "scene", "base": "#1A4D1A", "elements": "trees"},
        "beach": {"type": "scene", "base": "#F0E68C", "elements": "waves"},
        "mountains": {"type": "scene", "base": "#708090", "elements": "peaks"},
        "city": {"type": "scene", "base": "#2C3E50", "elements": "buildings"},
        "space": {"type": "scene", "base": "#0D1B2A", "elements": "stars"},
        "underwater": {"type": "scene", "base": "#006994", "elements": "bubbles"},
        "volcano": {"type": "scene", "base": "#1A0A00", "elements": "lava"},
        "aurora": {"type": "gradient", "id": "aurora-gradient"},
        "multiverse": {"type": "gradient", "id": "multiverse-gradient"},
        "black_hole": {"type": "scene", "base": "#000000", "elements": "vortex"},
        "dimension_rift": {"type": "gradient", "id": "rift-gradient"},
        "heaven": {"type": "gradient", "id": "heaven-gradient"},
    }

    @classmethod
    def generate_svg(cls, dna: DogDNA, width: int = 400, height: int = 400) -> str:
        traits = {
            "body_color": dna.traits[TraitCategory.BODY_COLOR].value,
            "expression": dna.traits[TraitCategory.FACE_EXPRESSION].value,
            "accessory": dna.traits[TraitCategory.ACCESSORY].value,
            "pattern": dna.traits[TraitCategory.PATTERN].value,
            "background": dna.traits[TraitCategory.BACKGROUND].value,
            "special": dna.traits[TraitCategory.SPECIAL].value,
        }
        seed = int(dna.dna_hash[:8], 16) if dna.dna_hash else 12345

        svg_parts = [
            f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
            cls._generate_defs(),
            cls._generate_background(traits["background"], width, height, seed),
            cls._generate_special_back(traits["special"], width, height),
            cls._generate_body(traits["body_color"], traits["pattern"], width, height, seed),
            cls._generate_face(traits["expression"], width, height),
            cls._generate_accessory(traits["accessory"], width, height),
            cls._generate_special_front(traits["special"], width, height, seed),
            cls._generate_badge(dna, width, height),
            "</svg>",
        ]

        print("DEBUG: visualizer.traits =", traits)
        # Save full traits for CI inspection
        try:
            Path("dog_data").mkdir(exist_ok=True)
            fname = Path("dog_data") / f"traits_debug_{int(time.time())}.json"
            fname.write_text(json.dumps(traits, indent=2))
            print(f"DEBUG: traits saved to {fname}")
        except Exception as e:
            print(f"DEBUG: failed to save traits: {e}")

        return "\n".join(svg_parts)

    @classmethod
    def _generate_defs(cls) -> str:
        """Generate SVG definitions"""
        return '''<defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="8" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="rainbow-body" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FF6B6B"/><stop offset="25%" stop-color="#FFE66D"/>
        <stop offset="50%" stop-color="#4ECDC4"/><stop offset="75%" stop-color="#45B7D1"/>
        <stop offset="100%" stop-color="#DDA0DD"/>
    </linearGradient>
    <radialGradient id="galaxy-body" cx="30%" cy="30%">
        <stop offset="0%" stop-color="#E6E6FA"/><stop offset="50%" stop-color="#9370DB"/>
        <stop offset="100%" stop-color="#1A0033"/>
    </radialGradient>
    <linearGradient id="holo-body" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FF00FF"/><stop offset="50%" stop-color="#00FFFF"/>
        <stop offset="100%" stop-color="#FFFF00"/>
    </linearGradient>
    <linearGradient id="sky-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#E0F4FF"/>
    </linearGradient>
    <linearGradient id="grass-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#90EE90"/><stop offset="100%" stop-color="#228B22"/>
    </linearGradient>
    <linearGradient id="sunset-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#FF6B6B"/><stop offset="50%" stop-color="#FFE66D"/>
        <stop offset="100%" stop-color="#4ECDC4"/>
    </linearGradient>
    <linearGradient id="aurora-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0D1B2A"/><stop offset="30%" stop-color="#00FF7F"/>
        <stop offset="70%" stop-color="#FF00FF"/><stop offset="100%" stop-color="#0D1B2A"/>
    </linearGradient>
    <radialGradient id="multiverse-gradient" cx="50%" cy="50%">
        <stop offset="0%" stop-color="#FFD700"/><stop offset="40%" stop-color="#FF00FF"/>
        <stop offset="70%" stop-color="#00FFFF"/><stop offset="100%" stop-color="#000"/>
    </radialGradient>
    <linearGradient id="rift-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#000"/><stop offset="30%" stop-color="#9400D3"/>
        <stop offset="50%" stop-color="#00FFFF"/><stop offset="70%" stop-color="#9400D3"/>
        <stop offset="100%" stop-color="#000"/>
    </linearGradient>
    <linearGradient id="heaven-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#FFF"/><stop offset="50%" stop-color="#FFD700" stop-opacity="0.3"/>
        <stop offset="100%" stop-color="#F0F8FF"/>
    </linearGradient>
    <clipPath id="head-clip"><ellipse cx="200" cy="200" rx="110" ry="115"/></clipPath>
</defs>'''

    @classmethod
    def _generate_background(cls, bg: str, w: int, h: int, seed: int) -> str:
        """Generate background"""
        cfg = cls.BACKGROUNDS.get(bg, cls.BACKGROUNDS["white"])
        parts = []

        if cfg["type"] == "solid":
            parts.append(f'<rect width="{w}" height="{h}" fill="{cfg["color"]}"/>')
        elif cfg["type"] == "gradient":
            parts.append(f'<rect width="{w}" height="{h}" fill="url(#{cfg["id"]})"/>')
        elif cfg["type"] == "scene":
            parts.append(f'<rect width="{w}" height="{h}" fill="{cfg["base"]}"/>')
            parts.append(cls._scene_elements(cfg["elements"], w, h, seed))

        return "\n".join(parts)

    @classmethod
    def _scene_elements(cls, elem: str, w: int, h: int, seed: int) -> str:
        """Generate scene elements"""
        parts = []

        if elem == "stars":
            for i in range(40):
                x, y = (seed * (i+1) * 7) % w, (seed * (i+1) * 13) % h
                r = 1 + i % 2
                parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="white" opacity="{0.4+i%5*0.1}"/>')

        elif elem == "trees":
            for i in range(5):
                x = 40 + i * 80
                th = 50 + (seed * i) % 30
                parts.append(f'<polygon points="{x},{h-20} {x-20},{h-20} {x},{h-20-th}" fill="#0D3D0D" opacity="0.5"/>')
                parts.append(f'<polygon points="{x},{h-20} {x+20},{h-20} {x},{h-20-th}" fill="#1A5C1A" opacity="0.5"/>')

        elif elem == "waves":
            for i in range(3):
                y = h - 50 + i * 15
                parts.append(f'<path d="M0 {y} Q100 {y-12} 200 {y} T400 {y}" fill="#4169E1" opacity="{0.25-i*0.06}"/>')

        elif elem == "peaks":
            parts.append(f'<polygon points="50,{h} 150,{h-140} 250,{h}" fill="#4A5568"/>')
            parts.append(f'<polygon points="180,{h} 280,{h-180} 380,{h}" fill="#2D3748"/>')
            parts.append(f'<polygon points="145,{h-130} 150,{h-140} 155,{h-130}" fill="white"/>')
            parts.append(f'<polygon points="275,{h-170} 280,{h-180} 285,{h-170}" fill="white"/>')

        elif elem == "buildings":
            for i in range(7):
                x, bh = i * 60, 70 + (seed * (i+1)) % 90
                parts.append(f'<rect x="{x}" y="{h-bh}" width="50" height="{bh}" fill="#1A202C"/>')
                for wy in range(10, int(bh)-10, 18):
                    for wx in range(8, 42, 14):
                        if (seed+i+wy+wx) % 3:
                            parts.append(f'<rect x="{x+wx}" y="{h-bh+wy}" width="6" height="8" fill="#FFD700" opacity="0.6"/>')

        elif elem == "bubbles":
            for i in range(15):
                x, y = (seed*(i+1)*17) % w, (seed*(i+1)*23) % h
                r = 4 + i % 8
                parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="white" opacity="0.25"/>')

        elif elem == "lava":
            parts.append(f'<rect x="0" y="{h-60}" width="{w}" height="60" fill="#FF4500" opacity="0.6"/>')
            for i in range(6):
                x = 30 + (seed*i*11) % (w-60)
                parts.append(f'<circle cx="{x}" cy="{h-25}" r="{6+i%4}" fill="#FF6600"/>')

        elif elem == "vortex":
            cx, cy = w//2, h//2
            for i in range(6):
                parts.append(f'<circle cx="{cx}" cy="{cy}" r="{160-i*25}" fill="none" stroke="#4B0082" stroke-width="2" opacity="{0.1+i*0.05}"/>')
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="25" fill="#000"/>')

        return "\n".join(parts)

    @classmethod
    def _generate_body(cls, color: str, pattern: str, w: int, h: int, seed: int) -> str:
        cx, cy = w // 2, h // 2
        c = cls.BODY_COLORS.get(color, cls.BODY_COLORS["brown"])
        parts = []

        # Floppy Ears
        parts.append(f'<ellipse cx="{cx-70}" cy="{cy-40}" rx="30" ry="60" fill="{c["main"]}" transform="rotate(20 {cx-70} {cy-40})" filter="url(#shadow)"/>')
        parts.append(f'<ellipse cx="{cx+70}" cy="{cy-40}" rx="30" ry="60" fill="{c["main"]}" transform="rotate(-20 {cx+70} {cy-40})" filter="url(#shadow)"/>')

        # Head
        parts.append(f'<rect x="{cx-80}" y="{cy-80}" width="160" height="150" rx="40" fill="{c["main"]}" filter="url(#shadow)"/>')

        # Snout area
        parts.append(f'<ellipse cx="{cx}" cy="{cy+20}" rx="50" ry="35" fill="{c["highlight"]}" opacity="0.6"/>')

        return "\n".join(parts)

    @classmethod
    def _pattern(cls, p: str, cx: int, cy: int, seed: int) -> str:
        """Generate pattern overlay"""
        if p == "spots":
            return "".join(f'<circle cx="{cx+((seed*i*7)%180)-90}" cy="{cy+((seed*i*11)%180)-90}" r="12" fill="#000" opacity="0.12"/>' for i in range(10))
        elif p == "stripes":
            return "".join(f'<rect x="{cx-110}" y="{cy-100+i*35}" width="220" height="12" fill="#000" opacity="0.08" transform="rotate(-15 {cx} {cy})"/>' for i in range(6))
        elif p == "stars":
            return "".join(f'<text x="{cx+((seed*i*13)%160)-80}" y="{cy+((seed*i*17)%160)-80}" font-size="18" fill="#FFD700" opacity="0.5">★</text>' for i in range(8))
        elif p == "hearts":
            return "".join(f'<text x="{cx+((seed*i*19)%140)-70}" y="{cy+((seed*i*23)%140)-70}" font-size="16" fill="#FF69B4" opacity="0.4">♥</text>' for i in range(7))
        elif p == "diamonds":
            return "".join(f'<text x="{cx+((seed*i*11)%150)-75}" y="{cy+((seed*i*13)%150)-75}" font-size="18" fill="#00CED1" opacity="0.35">◆</text>' for i in range(8))
        elif p == "swirls":
            return "".join(f'<circle cx="{cx}" cy="{cy}" r="{100-i*25}" fill="none" stroke="#000" stroke-width="2" opacity="0.08" stroke-dasharray="15,10"/>' for i in range(4))
        elif p == "gradient":
            return f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="115" fill="url(#sky-gradient)" opacity="0.25"/>'
        elif p == "nebula":
            return f'<ellipse cx="{cx-25}" cy="{cy-15}" rx="45" ry="35" fill="#FF00FF" opacity="0.12"/><ellipse cx="{cx+30}" cy="{cy+25}" rx="40" ry="30" fill="#00FFFF" opacity="0.12"/>'
        elif p == "lightning":
            return f'<path d="M{cx-15} {cy-70} L{cx+15} {cy-10} L{cx} {cy-10} L{cx+30} {cy+50}" stroke="#FFD700" stroke-width="3" fill="none" opacity="0.5"/>'
        elif p == "flames":
            return f'<ellipse cx="{cx}" cy="{cy+70}" rx="45" ry="25" fill="#FF4500" opacity="0.2"/><ellipse cx="{cx}" cy="{cy+60}" rx="35" ry="20" fill="#FF6600" opacity="0.15"/>'
        elif p in ["fractals", "aurora", "quantum", "cosmic_dust", "void"]:
            return f'<ellipse cx="{cx}" cy="{cy}" rx="100" ry="105" fill="url(#aurora-gradient)" opacity="0.2"/>'
        return ""

    @classmethod
    def _generate_face(cls, expr: str, w: int, h: int) -> str:
        cx, cy = w // 2, h // 2
        parts = []

        # Eyes (Round for dog)
        parts.append(f'<circle cx="{cx-35}" cy="{cy-20}" r="15" fill="#FFF"/>')
        parts.append(f'<circle cx="{cx+35}" cy="{cy-20}" r="15" fill="#FFF"/>')
        parts.append(f'<circle cx="{cx-35}" cy="{cy-20}" r="8" fill="#000"/>')
        parts.append(f'<circle cx="{cx+35}" cy="{cy-20}" r="8" fill="#000"/>')

        # Big nose
        parts.append(f'<ellipse cx="{cx}" cy="{cy+10}" rx="20" ry="15" fill="#000"/>')
        parts.append(f'<ellipse cx="{cx-5}" cy="{cy+5}" rx="5" ry="3" fill="#FFF" opacity="0.5"/>')

        # Tongue out?
        if expr in ["happy", "excited"]:
             parts.append(f'<path d="M{cx-10} {cy+30} Q{cx} {cy+60} {cx+10} {cy+30}" fill="#FF69B4" stroke="#D14785" stroke-width="2"/>')
        else:
            parts.append(f'<path d="M{cx-15} {cy+30} Q{cx} {cy+45} {cx+15} {cy+30}" stroke="#000" stroke-width="3" fill="none"/>')

        return "\n".join(parts)

    @classmethod
    def _generate_accessory(cls, acc: str, w: int, h: int) -> str:
        """Generate accessory"""
        cx, cy = w // 2, h // 2

        accessories = {
            "none": "",
            "simple_hat": f'<rect x="{cx-45}" y="{cy-145}" width="90" height="18" rx="3" fill="#8B0000"/><rect x="{cx-55}" y="{cy-130}" width="110" height="8" fill="#8B0000"/>',
            "bandana": f'<path d="M{cx-90} {cy-80} Q{cx} {cy-110} {cx+90} {cy-80}" stroke="#E74C3C" stroke-width="12" fill="none"/><polygon points="{cx-95},{cy-75} {cx-110},{cy-40} {cx-85},{cy-50}" fill="#E74C3C"/>',
            "bow": f'<ellipse cx="{cx-70}" cy="{cy-70}" rx="20" ry="15" fill="#FF69B4"/><ellipse cx="{cx-70}" cy="{cy-70}" rx="8" ry="8" fill="#FF1493"/><polygon points="{cx-70},{cy-85} {cx-55},{cy-70} {cx-70},{cy-55}" fill="#FF69B4"/>',
            "sunglasses": f'<rect x="{cx-58}" y="{cy-25}" width="38" height="28" rx="4" fill="#000" opacity="0.85"/><rect x="{cx+20}" y="{cy-25}" width="38" height="28" rx="4" fill="#000" opacity="0.85"/><line x1="{cx-20}" y1="{cy-11}" x2="{cx+20}" y2="{cy-11}" stroke="#000" stroke-width="3"/><line x1="{cx-58}" y1="{cy-11}" x2="{cx-80}" y2="{cy-20}" stroke="#000" stroke-width="2"/><line x1="{cx+58}" y1="{cy-11}" x2="{cx+80}" y2="{cy-20}" stroke="#000" stroke-width="2"/>',
            "crown": f'<polygon points="{cx-35},{cy-130} {cx-20},{cy-155} {cx},{cy-135} {cx+20},{cy-155} {cx+35},{cy-130}" fill="#FFD700" stroke="#DAA520" stroke-width="2"/><rect x="{cx-35}" y="{cy-130}" width="70" height="12" fill="#FFD700" stroke="#DAA520" stroke-width="2"/>',
            "headphones": f'<path d="M{cx-75} {cy-30} Q{cx-75} {cy-100} {cx} {cy-110} Q{cx+75} {cy-100} {cx+75} {cy-30}" stroke="#333" stroke-width="8" fill="none"/><rect x="{cx-85}" y="{cy-45}" width="25" height="40" rx="5" fill="#333"/><rect x="{cx+60}" y="{cy-45}" width="25" height="40" rx="5" fill="#333"/>',
            "monocle": f'<circle cx="{cx+38}" cy="{cy-15}" r="22" fill="none" stroke="#DAA520" stroke-width="3"/><line x1="{cx+60}" y1="{cy-15}" x2="{cx+90}" y2="{cy+40}" stroke="#DAA520" stroke-width="2"/>',
            "halo": f'<ellipse cx="{cx}" cy="{cy-150}" rx="55" ry="12" fill="none" stroke="#FFD700" stroke-width="6" opacity="0.85" filter="url(#glow)"/>',
            "horns": f'<path d="M{cx-60} {cy-90} Q{cx-80} {cy-150} {cx-50} {cy-160}" stroke="#8B0000" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M{cx+60} {cy-90} Q{cx+80} {cy-150} {cx+50} {cy-160}" stroke="#8B0000" stroke-width="12" fill="none" stroke-linecap="round"/>',
            "wizard_hat": f'<polygon points="{cx},{cy-190} {cx-55},{cy-115} {cx+55},{cy-115}" fill="#4B0082"/><ellipse cx="{cx}" cy="{cy-115}" rx="65" ry="12" fill="#4B0082"/><text x="{cx}" y="{cy-145}" font-size="20" fill="#FFD700" text-anchor="middle">★</text>',
            "golden_crown": f'<polygon points="{cx-45},{cy-130} {cx-30},{cy-165} {cx-10},{cy-140} {cx+10},{cy-165} {cx+30},{cy-140} {cx+45},{cy-165} {cx+45},{cy-115} {cx-45},{cy-115}" fill="#FFD700" stroke="#B8860B" stroke-width="3"/><circle cx="{cx}" cy="{cy-155}" r="8" fill="#E74C3C"/><circle cx="{cx-25}" cy="{cy-145}" r="5" fill="#3498DB"/><circle cx="{cx+25}" cy="{cy-145}" r="5" fill="#2ECC71"/>',
            "diamond_chain": f'<path d="M{cx-80} {cy+80} Q{cx} {cy+100} {cx+80} {cy+80}" stroke="#C0C0C0" stroke-width="4" fill="none"/><polygon points="{cx},{cy+85} {cx+12},{cy+100} {cx},{cy+115} {cx-12},{cy+100}" fill="#00CED1" stroke="#87CEEB" stroke-width="2"/>',
            "jetpack": f'<rect x="{cx-50}" y="{cy+60}" width="20" height="50" rx="5" fill="#555"/><rect x="{cx+30}" y="{cy+60}" width="20" height="50" rx="5" fill="#555"/><ellipse cx="{cx-40}" cy="{cy+120}" rx="8" ry="15" fill="#FF4500" opacity="0.8"/><ellipse cx="{cx+40}" cy="{cy+120}" rx="8" ry="15" fill="#FF4500" opacity="0.8"/>',
            "wings": f'<path d="M{cx-100} {cy} Q{cx-150} {cy-80} {cx-180} {cy+20} Q{cx-140} {cy+10} {cx-100} {cy+30}" fill="#E6E6FA" opacity="0.8"/><path d="M{cx+100} {cy} Q{cx+150} {cy-80} {cx+180} {cy+20} Q{cx+140} {cy+10} {cx+100} {cy+30}" fill="#E6E6FA" opacity="0.8"/>',
            "laser_eyes": f'<line x1="{cx-38}" y1="{cy-15}" x2="{cx-150}" y2="{cy+50}" stroke="#FF0000" stroke-width="4" opacity="0.7"/><line x1="{cx+38}" y1="{cy-15}" x2="{cx+150}" y2="{cy+50}" stroke="#FF0000" stroke-width="4" opacity="0.7"/>',
        }
        return accessories.get(acc, "")

    @classmethod
    def _generate_special_back(cls, sp: str, w: int, h: int) -> str:
        """Generate special effects behind dog"""
        cx, cy = w // 2, h // 2
        if sp == "aura":
            return f'<circle cx="{cx}" cy="{cy}" r="160" fill="none" stroke="#9400D3" stroke-width="4" opacity="0.3"/><circle cx="{cx}" cy="{cy}" r="175" fill="none" stroke="#4B0082" stroke-width="2" opacity="0.2"/>'
        elif sp == "energy":
            return f'<circle cx="{cx}" cy="{cy}" r="165" fill="none" stroke="#00FFFF" stroke-width="3" opacity="0.25" stroke-dasharray="20,10"/>'
        elif sp in ["transcendent", "godlike", "mythical"]:
            return f'<circle cx="{cx}" cy="{cy}" r="180" fill="url(#multiverse-gradient)" opacity="0.15"/>'
        return ""

    @classmethod
    def _generate_special_front(cls, sp: str, w: int, h: int, seed: int) -> str:
        """Generate special effects in front"""
        cx, cy = w // 2, h // 2
        if sp == "sparkles":
            pos = [(cx-90, cy-90), (cx+90, cy-90), (cx-90, cy+90), (cx+90, cy+90), (cx, cy-130)]
            return "".join(f'<text x="{x}" y="{y}" font-size="24" fill="#FFD700">✦</text>' for x, y in pos)
        elif sp == "glow":
            return f'<circle cx="{cx}" cy="{cy}" r="135" fill="none" stroke="#FFD700" stroke-width="6" opacity="0.25"/>'
        elif sp == "shadow":
            return f'<ellipse cx="{cx}" cy="{cy+140}" rx="100" ry="20" fill="#000" opacity="0.2"/>'
        elif sp == "particles":
            return "".join(f'<circle cx="{cx+((seed*i*13)%200)-100}" cy="{cy+((seed*i*17)%200)-100}" r="3" fill="#FFD700" opacity="0.6"/>' for i in range(12))
        elif sp == "transcendent":
            return f'<circle cx="{cx}" cy="{cy}" r="145" fill="none" stroke="#FFD700" stroke-width="4" opacity="0.4" filter="url(#glow)"/>'
        elif sp == "godlike":
            return f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="#FFF" stroke-width="3" opacity="0.5" filter="url(#glow)"/><text x="{cx}" y="{cy-170}" font-size="36" fill="#FFD700" text-anchor="middle" filter="url(#glow)">♔</text>'
        elif sp == "mythical":
            return f'<circle cx="{cx}" cy="{cy}" r="155" fill="none" stroke="#FF00FF" stroke-width="3" opacity="0.4" filter="url(#glow)"/><circle cx="{cx}" cy="{cy}" r="165" fill="none" stroke="#00FFFF" stroke-width="2" opacity="0.3"/>'
        return ""

    @classmethod
    def _generate_badge(cls, dna: DogDNA, w: int, h: int) -> str:
        """Generate rarity badge"""
        score = dna.get_rarity_score()
        gen = dna.generation

        if score >= 80:
            color, label = "#FFD700", "LEGENDARY"
        elif score >= 60:
            color, label = "#9370DB", "RARE"
        elif score >= 40:
            color, label = "#4ECDC4", "UNCOMMON"
        else:
            color, label = "#A0A0A0", "COMMON"

        return f'''<g transform="translate({w-75}, 15)">
            <rect width="65" height="22" rx="4" fill="{color}" opacity="0.9"/>
            <text x="32" y="15" font-size="8" fill="#FFF" text-anchor="middle" font-family="sans-serif" font-weight="bold">{label}</text>
        </g>
        <g transform="translate(10, 15)">
            <rect width="45" height="22" rx="4" fill="#333" opacity="0.8"/>
            <text x="22" y="15" font-size="9" fill="#FFF" text-anchor="middle" font-family="sans-serif">Gen {gen}</text>
        </g>'''


    @classmethod
    def generate_thumbnail(cls, dna: DogDNA, size: int = 100) -> str:
        return cls.generate_svg(dna, width=size, height=size)

def main():
    pass

if __name__ == "__main__":
    main()
