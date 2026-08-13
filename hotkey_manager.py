import sys
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class HotkeyManager(QObject):
    toggle_overlay_signal = pyqtSignal()
    toggle_click_through_signal = pyqtSignal()
    panic_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.hotkeys_registered = []
        self.shortcuts = []
        self.use_global_hotkeys = False
        self.keyboard_module = None

        try:
            import keyboard
            self.keyboard_module = keyboard
            self.use_global_hotkeys = True
            print("Глобальные хоткеи активированы")
        except ImportError:
            print("Библиотека keyboard не установлена. Установите: pip install keyboard")
        except Exception as e:
            print(f"Ошибка инициализации keyboard: {e}")

        if parent:
            self.toggle_overlay_signal.connect(parent.toggle_overlay)
            self.toggle_click_through_signal.connect(parent.toggle_click_through)
            self.panic_signal.connect(parent.panic_close)

    def register_hotkeys(self, hotkeys_dict):
        self.unregister_all()

        actions = {
            "toggle_overlay": self.toggle_overlay_signal.emit,
            "toggle_click_through": self.toggle_click_through_signal.emit,
            "panic_close": self.panic_signal.emit
        }

        if self.use_global_hotkeys and self.keyboard_module:
            for action, hotkey in hotkeys_dict.items():
                if hotkey and action in actions:
                    try:
                        kb_hotkey = self.convert_to_keyboard_format(hotkey)
                        if kb_hotkey:
                            self.keyboard_module.add_hotkey(kb_hotkey, actions[action], suppress=False)
                            self.hotkeys_registered.append(kb_hotkey)
                            print(f"Зарегистрирован глобальный хоткей: {kb_hotkey}")
                    except Exception as e:
                        print(f"Ошибка регистрации {hotkey}: {e}")

        for action, hotkey in hotkeys_dict.items():
            if hotkey and action in actions:
                try:
                    shortcut = QShortcut(QKeySequence(hotkey), self.parent)
                    shortcut.activated.connect(actions[action])
                    self.shortcuts.append(shortcut)
                    print(f"Зарегистрирован локальный хоткей: {hotkey}")
                except Exception as e:
                    print(f"Ошибка регистрации локального {hotkey}: {e}")

    def unregister_all(self):
        if self.use_global_hotkeys and self.keyboard_module:
            for hotkey in self.hotkeys_registered:
                try:
                    self.keyboard_module.remove_hotkey(hotkey)
                except:
                    pass
        self.hotkeys_registered.clear()

        for shortcut in self.shortcuts:
            try:
                shortcut.setEnabled(False)
                shortcut.deleteLater()
            except:
                pass
        self.shortcuts.clear()

    def convert_to_keyboard_format(self, hotkey):
        if not hotkey:
            return None
        
        hotkey = hotkey.lower().strip()
        
        special_keys = {
            'ctrl': 'ctrl',
            'control': 'ctrl',
            'alt': 'alt',
            'shift': 'shift',
            'meta': 'windows',
            'win': 'windows',
            'space': 'space',
            'return': 'enter',
            'enter': 'enter',
            'tab': 'tab',
            'backspace': 'backspace',
            'delete': 'delete',
            'insert': 'insert',
            'home': 'home',
            'end': 'end',
            'pageup': 'page up',
            'pagedown': 'page down',
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right',
            'escape': 'esc',
            'esc': 'esc',
            'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
            'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
            'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
            'num0': '0', 'num1': '1', 'num2': '2', 'num3': '3',
            'num4': '4', 'num5': '5', 'num6': '6', 'num7': '7',
            'num8': '8', 'num9': '9',
            'num*': '*', 'num+': '+', 'num-': '-', 'num/': '/',
            'numdel': 'delete',
        }
        
        parts = hotkey.split('+')
        kb_parts = []
        for part in parts:
            part = part.strip()
            if part in special_keys:
                kb_parts.append(special_keys[part])
            elif len(part) == 1:
                kb_parts.append(part)
            else:
                kb_parts.append(part)
        
        return '+'.join(kb_parts)