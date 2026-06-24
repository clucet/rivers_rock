#!/usr/bin/env python3
"""Central palette and design tokens for all Rivers Rock proposals."""

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
        "or_vieilli":    "#C9A84C",
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
}


def font_filename(role, cfg=BASE):
    name = cfg.fonts.get(role, "Montserrat")
    return FONT_MAP.get(name, "Montserrat-VariableFont_wght.ttf")


# ── Active config (runtime switchable) ──
ACTIVE = SCENE_VINTAGE

def set_active(name):
    """Switch ACTIVE config by name. Names: originale, fluid-wave, rock-brut, scene-vintage."""
    global ACTIVE
    mapping = {
        "originale":    BASE,
        "fluid-wave":   FLUID_WAVE,
        "rock-brut":    ROCK_BRUT,
        "scene-vintage": SCENE_VINTAGE,
        "ponts-lumiere": PONTS_LUMIERE,
    }
    ACTIVE = mapping.get(name, SCENE_VINTAGE)
    return ACTIVE


CONFIG_NAMES = {
    "originale":    "00-originale",
    "fluid-wave":   "01-fluid-wave",
    "rock-brut":    "02-rock-brut",
    "scene-vintage": "03-scene-vintage",
    "ponts-lumiere": "04-ponts-lumiere",
}


def proposition_dir(name):
    """Return the proposition assets directory for a config name."""
    return os.path.join(os.path.dirname(__file__), "..", "propositions", CONFIG_NAMES.get(name, "03-scene-vintage"), "assets")
