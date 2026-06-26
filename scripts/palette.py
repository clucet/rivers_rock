#!/usr/bin/env python3
"""Central palette and design tokens for all Rivers Rock proposals."""

import os
from dataclasses import dataclass, field
from reportlab.lib.colors import HexColor


def _hex(h):
    return HexColor(h)


def _pil(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


@dataclass(frozen=True)
class Config:
    name: str
    colors: dict
    fonts: dict
    tokens: dict
    flags: dict

    def rl(self, name):
        return _hex(self.colors[name][0])

    def pil(self, name):
        return _pil(self.colors[name][0])

    def font_path(self, name, fallback=None):
        return self.fonts.get(name, fallback)

    def token(self, name, default=None):
        return self.tokens.get(name, default)

    def flag(self, name, default=False):
        return self.flags.get(name, default)

    def get(self, name, fallback=None):
        """Get a color value by name with fallback. Supports aliases."""
        if name in self.colors:
            return self.colors[name][0]
        return fallback

    def rl_safe(self, name, fallback="#FFFFFF"):
        h = self.get(name, fallback)
        return _hex(h)

    def pil_safe(self, name, fallback="#FFFFFF"):
        h = self.get(name, fallback)
        return _pil(h)


def _colors(c1):
    return {k: (v, _pil(v)) for k, v in c1.items()}


# ── Configuration originale (BASE) ──
BASE = Config(
    name="Originale",
    colors=_colors({
        "bleu_seine":    "#1A3A5C",
        "vert_eau":      "#4A9B8E",
        "accent":        "#E85D3A",
        "vert_repere":   "#2D8A6E",
        "gris_acier":    "#8C9196",
        "blanc_casse":   "#F5F5F0",
        "blanc":         "#FFFFFF",
        # Aliases for compatibility
        "teal_profond":  "#1A3A5C",
        "terracotta":    "#E85D3A",
        "or_vieilli":    "#FFFFFF",
    }),
    fonts={
        "hero":      "BebasNeue",
        "logo":      "BebasNeue",
        "body":      "Montserrat",
        "badge":     "Montserrat",
        "song":      "Montserrat",
        "accent":    "Montserrat",
    },
    tokens={
        "card_w":    250, "card_h":    74,   "card_r":    6,
        "badge_r":   12,  "badge_y":   15,
        "shadow_off":3,   "shadow_alpha":0.15,
        "border_alpha":0.35,
        "gradient_steps":120,
        "wave_rows": 3,   "wave_opacity":0.07,
        "grain_intensity":0.0,
        "logo_scale":2.2,
        "footer_tracking":3,
        "setlist_font_size":28,
        "card_double_border":False,
        "badge_shape":"circle",
        "wave_style":"sine",
        "gradient_style":"linear",
    },
    flags={
        "use_grain": False,
        "use_halftone": False,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 1 : Fluid Wave (refonte identitaire) ──
FLUID_WAVE = Config(
    name="Fluid Wave",
    colors=_colors({
        "vert_profond":  "#1A4A3A",
        "vert_eau":      "#4A9B8E",
        "ambre":         "#D4A843",
        "accent":        "#E85D3A",
        "vert_repere":   "#2D8A6E",
        "gris_acier":    "#8C9196",
        "blanc_casse":   "#F5F5F0",
        "blanc":         "#FFFFFF",
        # Aliases for generator compatibility
        "bleu_seine":    "#1A4A3A",
        "teal_profond":  "#1A4A3A",
        "terracotta":    "#E85D3A",
        "or_vieilli":    "#D4A843",
    }),
    fonts={
        "hero":      "PlayfairDisplay",
        "logo":      "BebasNeue",
        "body":      "Nunito",
        "badge":     "Nunito",
        "song":      "Nunito",
        "accent":    "Nunito",
    },
    tokens={
        "card_w":    250, "card_h":    74,   "card_r":    14,
        "badge_r":   12,  "badge_y":   15,
        "shadow_off":4,   "shadow_alpha":0.10,
        "border_alpha":0.25,
        "gradient_steps":120,
        "wave_rows": 4,   "wave_opacity":0.04,
        "grain_intensity":0.03,
        "logo_scale":1.8,
        "footer_tracking":3,
        "setlist_font_size":26,
        "card_double_border":False,
        "badge_shape":"droplet",
        "wave_style":"bezier",
        "gradient_style":"radial",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": True,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 2 : Rock Brut (refonte identitaire) ──
ROCK_BRUT = Config(
    name="Rock Brut",
    colors=_colors({
        "noir":          "#0A0A0A",
        "accent":        "#FF3B00",
        "blanc":         "#FFFFFF",
        "vert_accent":   "#4A9B8E",
        "gris_fonce":    "#222222",
        "gris_acier":    "#8C9196",
        # Aliases for generator compatibility
        "bleu_seine":    "#0A0A0A",
        "bleu":          "#0A0A0A",
        "vert_eau":      "#4A9B8E",
        "teal_profond":  "#222222",
        "terracotta":    "#FF3B00",
        "or_vieilli":    "#FFFFFF",
        "vert_repere":   "#222222",
        "blanc_casse":   "#222222",
    }),
    fonts={
        "hero":      "Anton",
        "logo":      "Anton",
        "body":      "InterTight",
        "badge":     "InterTight",
        "song":      "InterTight",
        "data":      "JetBrainsMono",
    },
    tokens={
        "card_w":    250, "card_h":    74,   "card_r":    0,
        "badge_r":   14,  "badge_y":   15,
        "shadow_off":0,   "shadow_alpha":0.0,
        "border_alpha":1.0,
        "gradient_steps":0,
        "wave_rows": 0,   "wave_opacity":0.0,
        "grain_intensity":0.10,
        "logo_scale":2.4,
        "footer_tracking":4,
        "setlist_font_size":28,
        "card_double_border":False,
        "badge_shape":"pictogram",
        "wave_style":"chevron",
        "gradient_style":"flat",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 3 : Scène & Vintage (retenue) ──
SCENE_VINTAGE = Config(
    name="Scène & Vintage",
    colors=_colors({
        "bleu_seine":    "#1A3A5C",
        "teal_profond":  "#1A5C5C",
        "vert_eau":      "#4A9B8E",
        "accent":        "#E85D3A",
        "terracotta":    "#C96D4D",
        "or_vieilli":    "#D4B84C",
        "vert_repere":   "#2D8A6E",
        "gris_acier":    "#8C9196",
        "blanc_casse":   "#F5F5F0",
        "blanc":         "#FFFFFF",
    }),
    fonts={
        "hero":      "Anton",
        "logo":      "BebasNeue",
        "body":      "Montserrat",
        "badge":     "Montserrat",
        "song":      "Montserrat",
        "accent":    "SpaceMono",
    },
    tokens={
        "card_w":    250, "card_h":    74,   "card_r":    6,
        "badge_r":   12,  "badge_y":   15,
        "shadow_off":4,   "shadow_alpha":0.20,
        "border_alpha":0.50,
        "gradient_steps":120,
        "wave_rows": 3,   "wave_opacity":0.06,
        "grain_intensity":0.05,
        "logo_scale":2.2,
        "footer_tracking":3,
        "setlist_font_size":28,
        "card_double_border":True,
        "badge_shape":"circle",
        "wave_style":"sine",
        "gradient_style":"linear",
    },
    flags={
        "use_grain": True,
        "use_halftone": True,
        "use_flare": True,
        "use_or_wave": True,
        "use_duotone": True,
        "use_glow": True,
        "use_timbre": True,
    },
)

# ── Proposition 5 : Ponts & Lumière ──
PONTS_LUMIERE = Config(
    name="Ponts & Lumière",
    colors=_colors({
        "nuit":          "#0D1B2A",
        "acier":         "#415A77",
        "lumiere":       "#FFB703",
        "seine":         "#1B263B",
        "brouillard":    "#E0E1DD",
        "blanc":         "#FFFFFF",
        # Aliases for generator compatibility
        "bleu_seine":    "#0D1B2A",
        "vert_eau":      "#415A77",
        "accent":        "#FFB703",
        "teal_profond":  "#1B263B",
        "terracotta":    "#FFB703",
        "or_vieilli":    "#E0E1DD",
        "vert_repere":   "#1B263B",
        "blanc_casse":   "#E0E1DD",
        "gris_acier":    "#415A77",
    }),
    fonts={
        "hero":      "Teko",
        "logo":      "Teko",
        "body":      "Raleway",
        "badge":     "Raleway",
        "song":      "Raleway",
        "data":      "DMMono",
    },
    tokens={
        "card_w":    250, "card_h":    74,   "card_r":    4,
        "badge_r":   12,  "badge_y":   15,
        "shadow_off":3,   "shadow_alpha":0.25,
        "border_alpha":0.40,
        "gradient_steps":120,
        "wave_rows": 3,   "wave_opacity":0.04,
        "grain_intensity":0.04,
        "logo_scale":2.0,
        "footer_tracking":4,
        "setlist_font_size":26,
        "card_double_border":False,
        "badge_shape":"circle",
        "wave_style":"catenary",
        "gradient_style":"linear",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": True,
        "use_or_wave": True,
        "use_duotone": False,
        "use_glow": True,
        "use_timbre": False,
    },
)

# ── Proposition 6 : Neon Nights ──
NEON_NIGHTS = Config(
    name="Neon Nights",
    colors=_colors({
        "nuit_profonde": "#0F0B1A",
        "rose_neon":     "#FF2D95",
        "cyan":          "#00F5FF",
        "violet_fonce":  "#1A0B2E",
        "blanc_bleute":  "#E8E0F0",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#0F0B1A",
        "vert_eau":      "#1A0B2E",
        "accent":        "#FF2D95",
        "teal_profond":  "#1A0B2E",
        "terracotta":    "#FF2D95",
        "or_vieilli":    "#00F5FF",
        "vert_repere":   "#1A0B2E",
        "blanc_casse":   "#E8E0F0",
        "gris_acier":    "#1A0B2E",
    }),
    fonts={
        "hero":      "Orbitron",
        "logo":      "Orbitron",
        "body":      "Rajdhani",
        "badge":     "Rajdhani",
        "song":      "Rajdhani",
        "data":      "JetBrainsMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 2,
        "badge_r": 13, "badge_y": 15,
        "shadow_off": 4, "shadow_alpha": 0.30,
        "border_alpha": 0.50,
        "gradient_steps": 120,
        "wave_rows": 3, "wave_opacity": 0.05,
        "grain_intensity": 0.03,
        "logo_scale": 2.0,
        "footer_tracking": 5,
        "setlist_font_size": 24,
        "badge_shape": "hexagon",
        "wave_style": "zigzag",
        "gradient_style": "radial",
    },
    flags={
        "use_grain": True,
        "use_halftone": True,
        "use_flare": True,
        "use_or_wave": False,
        "use_duotone": True,
        "use_glow": True,
        "use_timbre": False,
    },
)

# ── Proposition 6 : Sable & Bronze ──
SABLE_BRONZE = Config(
    name="Sable & Bronze",
    colors=_colors({
        "sable":         "#D4A373",
        "terre_cuite":   "#CC6B49",
        "bronze":        "#B5835A",
        "vert_palmier":  "#2D6A4F",
        "creme":         "#FEFAE0",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#2D6A4F",
        "vert_eau":      "#D4A373",
        "accent":        "#CC6B49",
        "teal_profond":  "#B5835A",
        "terracotta":    "#CC6B49",
        "or_vieilli":    "#B5835A",
        "vert_repere":   "#B5835A",
        "blanc_casse":   "#FEFAE0",
        "gris_acier":    "#D4A373",
        "noir":          "#2D6A4F",
    }),
    fonts={
        "hero":      "Cinzel",
        "logo":      "Cinzel",
        "body":      "Lato",
        "badge":     "Lato",
        "song":      "Lato",
        "quote":     "Cormorant",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 8,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 3, "shadow_alpha": 0.12,
        "border_alpha": 0.35,
        "gradient_steps": 120,
        "wave_rows": 2, "wave_opacity": 0.04,
        "grain_intensity": 0.05,
        "logo_scale": 2.0,
        "footer_tracking": 3,
        "setlist_font_size": 24,
        "badge_shape": "circle",
        "wave_style": "geometric",
        "gradient_style": "linear",
    },
    flags={
        "use_grain": True,
        "use_halftone": True,
        "use_flare": True,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Helper : résolution de police dans logoutils ──
FONT_MAP = {
    "BebasNeue":       "BebasNeue-Regular.ttf",
    "Anton":           "Anton-Regular.ttf",
    "Montserrat":      "Montserrat-VariableFont_wght.ttf",
    "SpaceMono":       "SpaceMono-Regular.ttf",
    "PlayfairDisplay": "PlayfairDisplay[wght].ttf",
    "Nunito":          "Nunito[wght].ttf",
    "InterTight":      "InterTight[wght].ttf",
    "JetBrainsMono":   "JetBrainsMono[wght].ttf",
    "Teko":            "Teko[wght].ttf",
    "Raleway":         "Raleway[wght].ttf",
    "DMMono":          "DMMono-Regular.ttf",
    "Orbitron":        "Orbitron[wght].ttf",
    "Rajdhani":        "Rajdhani-Regular.ttf",
    "Cinzel":          "Cinzel[wght].ttf",
    "Lato":            "Lato-Regular.ttf",
    "Cormorant": "Cormorant-VariableFont_wght.ttf",
    "Inter":           "Inter[opsz,wght].ttf",
    "RubikGlitch":     "RubikGlitch-Regular.ttf",
    "SyneMono":        "SyneMono-Regular.ttf",
    "Karla":           "Karla[wght].ttf",
    "Bangers":         "Bangers-Regular.ttf",
    "CinzelDecorative":"CinzelDecorative-Regular.ttf",
    "Oswald":          "Oswald-VariableFont_wght.ttf",
    "SourceSans3":     "SourceSans3-VariableFont_wght.ttf",
    "DMSans":          "DMSans-VariableFont_opsz,wght.ttf",
}


def font_filename(role, cfg=BASE):
    name = cfg.fonts.get(role, "Montserrat")
    return FONT_MAP.get(name, "Montserrat-VariableFont_wght.ttf")


# ── Active config (runtime switchable) ──
ACTIVE = NEON_NIGHTS

def set_active(name):
    """Switch ACTIVE config by name. Names: originale, fluid-wave, rock-brut, scene-vintage."""
    global ACTIVE
    mapping = {
        "originale":    BASE,
        "fluid-wave":   FLUID_WAVE,
        "rock-brut":    ROCK_BRUT,
        "scene-vintage": SCENE_VINTAGE,
        "ponts-lumiere": PONTS_LUMIERE,
        "neon-nights":   NEON_NIGHTS,    "nordik":        NORDIK,
    "grunge":        GRUNGE,
    "jazz-club":     JAZZ_CLUB,
        "sable-bronze":  SABLE_BRONZE,
    "bitume":        BITUME,
    "cordes-voix":   CORDES_VOIX,
    "heritage":      HERITAGE,
    "rubicon":       RUBICON,
    "minuit":        MINUIT,
    }
    ACTIVE = mapping.get(name, SCENE_VINTAGE)
    return ACTIVE


CONFIG_NAMES = {
    "originale":    "00-originale",
    "fluid-wave":   "01-fluid-wave",
    "rock-brut":    "02-rock-brut",
    "scene-vintage": "03-scene-vintage",
    "ponts-lumiere": "04-ponts-lumiere",
    "neon-nights":   "05-neon-nights",
    "nordik":        "07-nordik",
    "grunge":        "08-grunge",
    "jazz-club":     "09-jazz-club",
    "sable-bronze":  "06-sable-bronze",
    "bitume":        "10-bitume",
    "cordes-voix":   "11-cordes-voix",
    "heritage":      "12-heritage",
    "rubicon":       "13-rubicon",
    "minuit":        "14-minuit",
}


def proposition_dir(name):
    """Return the proposition assets directory for a config name."""
    return os.path.join(os.path.dirname(__file__), "..", "propositions", CONFIG_NAMES.get(name, "03-scene-vintage"), "assets")

# ── Proposition 7 : Nordik ──
NORDIK = Config(
    name="Nordik",
    colors=_colors({
        "blanc_pur":     "#FAFAFA",
        "gris_nuage":    "#E8E8E4",
        "gris_ardoise":  "#4A4A4A",
        "noir_doux":     "#2B2B2B",
        "accent_lin":    "#B8B5A8",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#FAFAFA",
        "vert_eau":      "#E8E8E4",
        "accent":        "#B8B5A8",
        "teal_profond":  "#E8E8E4",
        "terracotta":    "#B8B5A8",
        "or_vieilli":    "#4A4A4A",
        "vert_repere":   "#E8E8E4",
        "blanc_casse":   "#F5F0EB",
        "gris_acier":    "#8C9196",
    }),
    fonts={
        "hero":      "Inter",
        "logo":      "Inter",
        "body":      "Inter",
        "badge":     "Inter",
        "song":      "Inter",
        "data":      "Inter",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 2,
        "badge_r": 10, "badge_y": 15,
        "shadow_off": 2, "shadow_alpha": 0.05,
        "border_alpha": 0.15,
        "gradient_steps": 0,
        "wave_rows": 0, "wave_opacity": 0.0,
        "grain_intensity": 0.0,
        "logo_scale": 1.8,
        "footer_tracking": 8,
        "setlist_font_size": 22,
        "badge_shape": "circle",
        "wave_style": "none",
        "gradient_style": "flat",
    },
    flags={
        "use_grain": False,
        "use_halftone": False,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 8 : Grunge ──
GRUNGE = Config(
    name="Grunge",
    colors=_colors({
        "papier":        "#F5EADD",
        "toner":         "#1A1A1A",
        "marqueur":      "#FF3366",
        "correcteur":    "#FFFFFF",
        "agrafes":       "#8C9196",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#F5EADD",
        "vert_eau":      "#F5EADD",
        "accent":        "#FF3366",
        "teal_profond":  "#F5EADD",
        "terracotta":    "#FF3366",
        "or_vieilli":    "#8C9196",
        "vert_repere":   "#1A1A1A",
        "blanc_casse":   "#F5EADD",
        "gris_acier":    "#8C9196",
    }),
    fonts={
        "hero":      "RubikGlitch",
        "logo":      "RubikGlitch",
        "body":      "SpaceMono",
        "badge":     "SyneMono",
        "song":      "SpaceMono",
        "data":      "SyneMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 0,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 0, "shadow_alpha": 0.0,
        "border_alpha": 1.0,
        "gradient_steps": 0,
        "wave_rows": 0, "wave_opacity": 0.0,
        "grain_intensity": 0.15,
        "logo_scale": 2.0,
        "footer_tracking": 3,
        "setlist_font_size": 24,
        "badge_shape": "square",
        "wave_style": "none",
        "gradient_style": "flat",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 9 : Jazz Club ──
JAZZ_CLUB = Config(
    name="Jazz Club",
    colors=_colors({
        "nuit":          "#0A0A0A",
        "or_bruni":      "#C9A86C",
        "cuivre":        "#B87333",
        "rouge_velours": "#8B1A1A",
        "blanc_ivoire":  "#F5F0E8",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#0A0A0A",
        "vert_eau":      "#0A0A0A",
        "accent":        "#C9A86C",
        "teal_profond":  "#0A0A0A",
        "terracotta":    "#C9A86C",
        "or_vieilli":    "#C9A86C",
        "vert_repere":   "#8B1A1A",
        "blanc_casse":   "#F5F0E8",
        "gris_acier":    "#8B1A1A",
    }),
    fonts={
        "hero":      "PlayfairDisplay",
        "logo":      "PlayfairDisplay",
        "body":      "Karla",
        "badge":     "Karla",
        "song":      "Karla",
        "data":      "DMMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 6,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 3, "shadow_alpha": 0.20,
        "border_alpha": 0.35,
        "gradient_steps": 120,
        "wave_rows": 2, "wave_opacity": 0.04,
        "grain_intensity": 0.08,
        "logo_scale": 2.0,
        "footer_tracking": 6,
        "setlist_font_size": 24,
        "badge_shape": "circle",
        "wave_style": "sine",
        "gradient_style": "radial",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": True,
        "use_or_wave": True,
        "use_duotone": False,
        "use_glow": True,
        "use_timbre": True,
    },
)

# ── Proposition 10 : Bitume (Street Art / Urbain) ──
BITUME = Config(
    name="Bitume",
    colors=_colors({
        "bitume":        "#2C2C2C",
        "beton":         "#8C8C8C",
        "fluo":          "#F4D03F",
        "brique":        "#A93226",
        "craie":         "#FDFEFE",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#2C2C2C",
        "vert_eau":      "#8C8C8C",
        "accent":        "#F4D03F",
        "terracotta":    "#A93226",
        "or_vieilli":    "#FDFEFE",
        "teal_profond":  "#2C2C2C",
        "vert_repere":   "#8C8C8C",
        "blanc_casse":   "#FDFEFE",
        "gris_acier":    "#8C8C8C",
    }),
    fonts={
        "hero":      "Bangers",
        "logo":      "Bangers",
        "body":      "SpaceMono",
        "badge":     "SpaceMono",
        "song":      "SpaceMono",
        "data":      "SyneMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 0,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 0, "shadow_alpha": 0.0,
        "border_alpha": 1.0,
        "gradient_steps": 0,
        "wave_rows": 0, "wave_opacity": 0.0,
        "grain_intensity": 0.15,
        "logo_scale": 2.0,
        "footer_tracking": 4,
        "setlist_font_size": 24,
        "badge_shape": "square",
        "wave_style": "none",
        "gradient_style": "flat",
    },
    flags={
        "use_grain": True,
        "use_halftone": True,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 11 : Cordes & Voix (Acoustique / Intimiste) ──
CORDES_VOIX = Config(
    name="Cordes & Voix",
    colors=_colors({
        "creme":         "#FFF8F0",
        "acajou":        "#6D4C41",
        "ambre_doux":    "#FFB74D",
        "foret":         "#2E7D32",
        "noir_doux":     "#37474F",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#FFF8F0",
        "vert_eau":      "#37474F",
        "accent":        "#FFB74D",
        "terracotta":    "#2E7D32",
        "or_vieilli":    "#6D4C41",
        "teal_profond":  "#37474F",
        "vert_repere":   "#2E7D32",
        "blanc_casse":   "#FFF8F0",
        "gris_acier":    "#6D4C41",
    }),
    fonts={
        "hero":      "PlayfairDisplay",
        "logo":      "BebasNeue",
        "body":      "Lato",
        "badge":     "Lato",
        "song":      "Cormorant",
        "quote":     "Cormorant",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 10,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 3, "shadow_alpha": 0.08,
        "border_alpha": 0.20,
        "gradient_steps": 120,
        "wave_rows": 2, "wave_opacity": 0.03,
        "grain_intensity": 0.02,
        "logo_scale": 1.8,
        "footer_tracking": 3,
        "setlist_font_size": 24,
        "badge_shape": "circle",
        "wave_style": "sine",
        "gradient_style": "linear",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": False,
        "use_or_wave": False,
        "use_duotone": False,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 12 : Héritage (Patrimoine normand) ──
HERITAGE = Config(
    name="Héritage",
    colors=_colors({
        "vitrail":       "#1A237E",
        "or_feuille":    "#D4AF37",
        "colombage":     "#4E342E",
        "pierre":        "#BDBDBD",
        "parchemin":     "#FFF8E1",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#1A237E",
        "vert_eau":      "#BDBDBD",
        "accent":        "#D4AF37",
        "terracotta":    "#4E342E",
        "or_vieilli":    "#D4AF37",
        "teal_profond":  "#4E342E",
        "vert_repere":   "#BDBDBD",
        "blanc_casse":   "#FFF8E1",
        "gris_acier":    "#BDBDBD",
    }),
    fonts={
        "hero":      "CinzelDecorative",
        "logo":      "Cinzel",
        "body":      "Lora",
        "badge":     "Cormorant",
        "song":      "Lora",
        "data":      "DMMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 2,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 3, "shadow_alpha": 0.15,
        "border_alpha": 0.30,
        "gradient_steps": 120,
        "wave_rows": 2, "wave_opacity": 0.04,
        "grain_intensity": 0.04,
        "logo_scale": 2.0,
        "footer_tracking": 4,
        "setlist_font_size": 24,
        "badge_shape": "hexagon",
        "wave_style": "catenary",
        "gradient_style": "linear",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": True,
        "use_or_wave": True,
        "use_duotone": False,
        "use_glow": True,
        "use_timbre": True,
    },
)

# ── Proposition 13 : Rubicon (Americana / Road Trip) ──
RUBICON = Config(
    name="Rubicon",
    colors=_colors({
        "route":         "#E65100",
        "ciel":          "#1976D2",
        "poussiere":     "#D7CCC8",
        "pin":           "#33691E",
        "creme":         "#FFF8E1",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#1976D2",
        "vert_eau":      "#33691E",
        "accent":        "#E65100",
        "terracotta":    "#D7CCC8",
        "or_vieilli":    "#FFF8E1",
        "teal_profond":  "#33691E",
        "vert_repere":   "#1976D2",
        "blanc_casse":   "#FFF8E1",
        "gris_acier":    "#D7CCC8",
    }),
    fonts={
        "hero":      "Oswald",
        "logo":      "Anton",
        "body":      "SourceSans3",
        "badge":     "SourceSans3",
        "song":      "Oswald",
        "data":      "JetBrainsMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 4,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 3, "shadow_alpha": 0.12,
        "border_alpha": 0.25,
        "gradient_steps": 120,
        "wave_rows": 3, "wave_opacity": 0.04,
        "grain_intensity": 0.06,
        "logo_scale": 2.0,
        "footer_tracking": 4,
        "setlist_font_size": 26,
        "badge_shape": "circle",
        "wave_style": "geometric",
        "gradient_style": "linear",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": True,
        "use_or_wave": False,
        "use_duotone": True,
        "use_glow": False,
        "use_timbre": False,
    },
)

# ── Proposition 14 : Minuit (French Touch / Élégance) ──
MINUIT = Config(
    name="Minuit",
    colors=_colors({
        "velours":       "#0D0D0D",
        "bordeaux":      "#6A1B4D",
        "or_bruni":      "#C9A87C",
        "ivoire":        "#F5F0E8",
        "perle":         "#9E9E9E",
        "blanc":         "#FFFFFF",
        # Aliases
        "bleu_seine":    "#0D0D0D",
        "vert_eau":      "#6A1B4D",
        "accent":        "#C9A87C",
        "terracotta":    "#9E9E9E",
        "or_vieilli":    "#C9A87C",
        "teal_profond":  "#0D0D0D",
        "vert_repere":   "#9E9E9E",
        "blanc_casse":   "#F5F0E8",
        "gris_acier":    "#9E9E9E",
    }),
    fonts={
        "hero":      "PlayfairDisplay",
        "logo":      "PlayfairDisplay",
        "body":      "Karla",
        "badge":     "Karla",
        "song":      "DMSans",
        "data":      "DMMono",
    },
    tokens={
        "card_w": 250, "card_h": 74, "card_r": 8,
        "badge_r": 12, "badge_y": 15,
        "shadow_off": 4, "shadow_alpha": 0.20,
        "border_alpha": 0.35,
        "gradient_steps": 120,
        "wave_rows": 2, "wave_opacity": 0.04,
        "grain_intensity": 0.06,
        "logo_scale": 2.0,
        "footer_tracking": 5,
        "setlist_font_size": 24,
        "badge_shape": "circle",
        "wave_style": "sine",
        "gradient_style": "radial",
    },
    flags={
        "use_grain": True,
        "use_halftone": False,
        "use_flare": True,
        "use_or_wave": True,
        "use_duotone": False,
        "use_glow": True,
        "use_timbre": True,
    },
)


# ── WCAG contrast checking utilities ──

def relative_luminance(hex_color):
    """Calculate relative luminance per WCAG 2.1 definition."""
    h = hex_color.lstrip("#")
    r, g, b = tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(c1, c2):
    """Calculate contrast ratio between two hex colors (WCAG 2.1)."""
    l1 = relative_luminance(c1)
    l2 = relative_luminance(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_wcag_aa(cfg, threshold_small=4.5, threshold_large=3.0):
    """Check all color pairs in a config against WCAG AA thresholds.
    Returns list of (name1, name2, ratio, passed_small, passed_large)."""
    results = []
    items = [(n, v[0]) for n, v in cfg.colors.items() if not n.startswith("_")]
    for i, (n1, h1) in enumerate(items):
        for n2, h2 in items[i+1:]:
            ratio = contrast_ratio(h1, h2)
            results.append((n1, n2, ratio, ratio >= threshold_small, ratio >= threshold_large))
    return results


def print_wcag_report(cfg):
    """Print a formatted WCAG contrast report for a config."""
    print(f"\n=== WCAG AA Report: {cfg.name} ===")
    print(f"{'Color 1':<20} {'Color 2':<20} {'Ratio':>6} {'Small':>6} {'Large':>6}")
    print("-" * 58)
    for n1, n2, ratio, passed_small, passed_large in check_wcag_aa(cfg):
        small = "✅" if passed_small else "❌"
        large = "✅" if passed_large else "❌"
        print(f"{n1:<20} {n2:<20} {ratio:>5.2f}:1 {small:>6} {large:>6}")
    print()
