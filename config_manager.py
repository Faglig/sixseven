# file: config_manager.py

import json
import os

class ConfigManager:
    DEFAULT_CONFIG = {
        "window_width": 800,
        "window_height": 600,
        "window_opacity": 1.0,
        "accent_color": "#0078D4",
        "rainbow_enabled": False,
        "font_scale": 1.0,
        "current_theme": "Тема Темная",
        "themes": {
            "Тема Светлая": {
                "background": "#F5F5F5",
                "surface": "#FFFFFF",
                "border": "#D0D0D0",
                "text": "#111111",
                "text_secondary": "#555555",
                "accent": "#0078D4",
                "hover": "#E0E0E0",
                "pressed": "#CCCCCC",
                "titlebar": "#FFFFFF",
                "sidebar": "#F0F0F0",
                "scrollbar_background": "#F5F5F5",
                "scrollbar_handle": "#C0C0C0"
            },
            "Тема Темная": {
                "background": "#111827",
                "surface": "#1F2937",
                "border": "#374151",
                "text": "#F9FAFB",
                "text_secondary": "#D1D5DB",
                "accent": "#9333EA",
                "hover": "#4B5563",
                "pressed": "#374151",
                "titlebar": "#1F2937",
                "sidebar": "#111827",
                "scrollbar_background": "#111827",
                "scrollbar_handle": "#4B5563"
            },
            "Тема Красная": {
                "background": "#1A0A0A",
                "surface": "#2D1515",
                "border": "#4A2020",
                "text": "#FFE5E5",
                "text_secondary": "#FFB3B3",
                "accent": "#FF0000",
                "hover": "#5C2D2D",
                "pressed": "#3D1A1A",
                "titlebar": "#2D1515",
                "sidebar": "#1A0A0A",
                "scrollbar_background": "#1A0A0A",
                "scrollbar_handle": "#5C2D2D"
            },
            "Тема Синяя": {
                "background": "#0A0A1A",
                "surface": "#15152D",
                "border": "#20204A",
                "text": "#E5E5FF",
                "text_secondary": "#B3B3FF",
                "accent": "#0066FF",
                "hover": "#2D2D5C",
                "pressed": "#1A1A3D",
                "titlebar": "#15152D",
                "sidebar": "#0A0A1A",
                "scrollbar_background": "#0A0A1A",
                "scrollbar_handle": "#2D2D5C"
            },
            "Тема Зеленая": {
                "background": "#0A1A0A",
                "surface": "#152D15",
                "border": "#204A20",
                "text": "#E5FFE5",
                "text_secondary": "#B3FFB3",
                "accent": "#00CC00",
                "hover": "#2D5C2D",
                "pressed": "#1A3D1A",
                "titlebar": "#152D15",
                "sidebar": "#0A1A0A",
                "scrollbar_background": "#0A1A0A",
                "scrollbar_handle": "#2D5C2D"
            }
        },
        "custom_themes": {
            "Слот 1": None,
            "Слот 2": None,
            "Слот 3": None,
            "Слот 4": None,
            "Слот 5": None
        },
        "hotkeys": {
            "toggle_overlay": "ctrl+alt+o",
            "toggle_click_through": "ctrl+alt+c",
            "panic_close": "ctrl+alt+p"
        },
        "language": "ru",
        "click_through_enabled": False,
        "colors": {
            "background": "#111827",
            "surface": "#1F2937",
            "border": "#374151",
            "text": "#F9FAFB",
            "text_secondary": "#D1D5DB",
            "accent": "#9333EA",
            "hover": "#4B5563",
            "pressed": "#374151",
            "titlebar": "#1F2937",
            "sidebar": "#111827",
            "scrollbar_background": "#111827",
            "scrollbar_handle": "#4B5563"
        },
        "animation_modes": {
            "background": "none",
            "surface": "none",
            "border": "none",
            "text": "none",
            "text_secondary": "none",
            "accent": "none",
            "hover": "none",
            "pressed": "none",
            "titlebar": "none",
            "sidebar": "none",
            "scrollbar_background": "none",
            "scrollbar_handle": "none"
        },
        "gradient_color1": "#FF0000",
        "gradient_color2": "#0000FF",
        "gradient_speed": 1.0,
        "favorite_colors": []
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = self.DEFAULT_CONFIG.copy()
                merged.update(data)
                if "colors" in data and isinstance(data["colors"], dict):
                    merged["colors"] = {**self.DEFAULT_CONFIG["colors"], **data["colors"]}
                if "animation_modes" in data and isinstance(data["animation_modes"], dict):
                    merged["animation_modes"] = {**self.DEFAULT_CONFIG["animation_modes"], **data["animation_modes"]}
                if "favorite_colors" in data and isinstance(data["favorite_colors"], list):
                    merged["favorite_colors"] = data["favorite_colors"]
                if "themes" in data and isinstance(data["themes"], dict):
                    merged["themes"] = data["themes"]
                if "custom_themes" in data and isinstance(data["custom_themes"], dict):
                    merged["custom_themes"] = data["custom_themes"]
                return merged
            except:
                pass
        return json.loads(json.dumps(self.DEFAULT_CONFIG))

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def reset(self):
        favorite_colors = self.config.get("favorite_colors", [])
        self.config = json.loads(json.dumps(self.DEFAULT_CONFIG))
        self.config["favorite_colors"] = favorite_colors
        self.save()

    def apply_theme(self, theme_name):
        if theme_name in self.config.get("themes", {}):
            self.config["current_theme"] = theme_name
            self.config["colors"] = self.config["themes"][theme_name].copy()
            self.save()
            return True
        return False

    def apply_custom_theme(self, slot_name):
        theme_data = self.config.get("custom_themes", {}).get(slot_name)
        if theme_data:
            self.config["current_theme"] = slot_name
            self.config["colors"] = theme_data.copy()
            self.save()
            return True
        return False

    def save_current_as_theme(self, slot_name):
        if slot_name in self.config.get("custom_themes", {}):
            self.config["custom_themes"][slot_name] = self.config["colors"].copy()
            self.config["current_theme"] = slot_name
            self.save()
            return True
        return False

    @property
    def font_scale(self):
        return self.config.get("font_scale", 1.0)

    @font_scale.setter
    def font_scale(self, value):
        self.config["font_scale"] = value

    @property
    def window_width(self):
        return self.config["window_width"]

    @window_width.setter
    def window_width(self, value):
        self.config["window_width"] = value

    @property
    def window_height(self):
        return self.config["window_height"]

    @window_height.setter
    def window_height(self, value):
        self.config["window_height"] = value

    @property
    def window_opacity(self):
        return self.config["window_opacity"]

    @window_opacity.setter
    def window_opacity(self, value):
        self.config["window_opacity"] = value

    @property
    def accent_color(self):
        return self.config["accent_color"]

    @accent_color.setter
    def accent_color(self, value):
        self.config["accent_color"] = value

    @property
    def rainbow_enabled(self):
        return self.config["rainbow_enabled"]

    @rainbow_enabled.setter
    def rainbow_enabled(self, value):
        self.config["rainbow_enabled"] = value

    @property
    def hotkeys(self):
        return self.config["hotkeys"]

    @hotkeys.setter
    def hotkeys(self, value):
        self.config["hotkeys"] = value

    @property
    def language(self):
        return self.config["language"]

    @language.setter
    def language(self, value):
        self.config["language"] = value

    @property
    def click_through_enabled(self):
        return self.config["click_through_enabled"]

    @click_through_enabled.setter
    def click_through_enabled(self, value):
        self.config["click_through_enabled"] = value

    def get_favorite_colors(self):
        return self.config.get("favorite_colors", [])

    def add_favorite_color(self, color_name):
        if color_name not in self.config.get("favorite_colors", []):
            self.config.setdefault("favorite_colors", []).append(color_name)
            self.save()

    def remove_favorite_color(self, color_name):
        if color_name in self.config.get("favorite_colors", []):
            self.config["favorite_colors"].remove(color_name)
            self.save()