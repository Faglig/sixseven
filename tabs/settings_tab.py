from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt5.QtGui import QColor, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QSpinBox, QPushButton,
    QComboBox, QKeySequenceEdit, QFrame, QGridLayout, QScrollArea,
    QGraphicsOpacityEffect, QInputDialog
)
from color_dialog import ColorPickerDialog
import os
import webbrowser


class SingleKeySequenceEdit(QKeySequenceEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_key_string = ""
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        native_scancode = event.nativeScanCode()
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return
        keys = []
        if modifiers & Qt.ControlModifier:
            keys.append("Ctrl")
        if modifiers & Qt.AltModifier:
            keys.append("Alt")
        if modifiers & Qt.ShiftModifier:
            keys.append("Shift")
        key_str = self.key_to_string(key, native_scancode)
        if key_str:
            keys.append(key_str)
        if keys:
            self.custom_key_string = "+".join(keys)
            self.setKeySequence(QKeySequence(self.custom_key_string))
            self.editingFinished.emit()
            self.clearFocus()
        event.accept()
    
    def get_custom_key_string(self):
        return self.custom_key_string

    def set_custom_key_string(self, value):
        self.custom_key_string = value
        self.setKeySequence(QKeySequence(value))

    def key_to_string(self, key, native_scancode=0):
        key_map = {
            Qt.Key_F1: "F1", Qt.Key_F2: "F2", Qt.Key_F3: "F3",
            Qt.Key_F4: "F4", Qt.Key_F5: "F5", Qt.Key_F6: "F6",
            Qt.Key_F7: "F7", Qt.Key_F8: "F8", Qt.Key_F9: "F9",
            Qt.Key_F10: "F10", Qt.Key_F11: "F11", Qt.Key_F12: "F12",
            Qt.Key_Space: "Space", Qt.Key_Return: "Return",
            Qt.Key_Enter: "Enter", Qt.Key_Tab: "Tab",
            Qt.Key_Delete: "Delete", Qt.Key_Home: "Home",
            Qt.Key_End: "End", Qt.Key_PageUp: "PageUp",
            Qt.Key_PageDown: "PageDown", Qt.Key_Up: "Up",
            Qt.Key_Down: "Down", Qt.Key_Left: "Left",
            Qt.Key_Right: "Right", Qt.Key_Escape: "Escape",
        }
        if key in key_map:
            return key_map[key]
        if 0x41 <= key <= 0x5A:
            return chr(key).lower()
        if 0x30 <= key <= 0x39:
            return chr(key)
        return None


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        theme_group = QFrame()
        theme_group.setObjectName("settingsGroup")
        theme_layout = QVBoxLayout(theme_group)
        theme_layout.setContentsMargins(10, 10, 10, 10)
        theme_layout.setSpacing(6)
        
        theme_title = QLabel("🎨 ТЕМЫ")
        theme_title.setObjectName("groupLabel")
        theme_title.setAlignment(Qt.AlignCenter)
        theme_title.setFixedHeight(28)
        theme_layout.addWidget(theme_title)

        builtin_layout = QHBoxLayout()
        builtin_layout.setSpacing(4)
        self.theme_buttons = {}
        for theme_name in ["Светлая", "Темная", "Красная", "Синяя", "Зеленая"]:
            btn = QPushButton(theme_name)
            btn.setCheckable(True)
            btn.setObjectName("themeButton")
            full_name = f"Тема {theme_name}"
            btn.clicked.connect(lambda checked, t=full_name: self.apply_builtin_theme(t))
            builtin_layout.addWidget(btn)
            self.theme_buttons[full_name] = btn
        theme_layout.addLayout(builtin_layout)

        custom_layout = QHBoxLayout()
        custom_layout.setSpacing(4)
        self.custom_theme_buttons = {}
        for i in range(1, 6):
            slot_name = f"Слот {i}"
            btn = QPushButton(slot_name)
            btn.setCheckable(True)
            btn.setObjectName("themeButton")
            btn.clicked.connect(lambda checked, s=slot_name: self.apply_custom_theme_slot(s))
            custom_layout.addWidget(btn)
            self.custom_theme_buttons[slot_name] = btn
        theme_layout.addLayout(custom_layout)

        theme_actions = QHBoxLayout()
        theme_actions.setSpacing(4)
        save_btn = QPushButton("💾")
        save_btn.setObjectName("themeButton")
        save_btn.setToolTip("Сохранить в слот")
        save_btn.clicked.connect(self.save_current_theme_to_slot)
        theme_actions.addWidget(save_btn)
        
        clear_btn = QPushButton("🗑")
        clear_btn.setObjectName("themeButton")
        clear_btn.setToolTip("Очистить слот")
        clear_btn.clicked.connect(self.clear_theme_slot)
        theme_actions.addWidget(clear_btn)
        theme_layout.addLayout(theme_actions)
        layout.addWidget(theme_group)

        size_group = QFrame()
        size_group.setObjectName("settingsGroup")
        size_layout = QGridLayout(size_group)
        size_layout.setContentsMargins(10, 10, 10, 10)
        size_layout.setVerticalSpacing(4)
        size_layout.setHorizontalSpacing(6)
        
        size_title = QLabel("🪟 ОКНО")
        size_title.setObjectName("groupLabel")
        size_title.setAlignment(Qt.AlignCenter)
        size_title.setFixedHeight(28)
        size_layout.addWidget(size_title, 0, 0, 1, 3)
        
        size_layout.addWidget(QLabel("Ширина:"), 1, 0)
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(400, 1920)
        self.width_slider.setValue(self.parent.config.window_width)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(400, 1920)
        self.width_spin.setValue(self.parent.config.window_width)
        self.width_slider.valueChanged.connect(self.width_spin.setValue)
        self.width_spin.valueChanged.connect(self.width_slider.setValue)
        self.width_spin.valueChanged.connect(self.change_window_size)
        size_layout.addWidget(self.width_slider, 1, 1)
        size_layout.addWidget(self.width_spin, 1, 2)

        size_layout.addWidget(QLabel("Высота:"), 2, 0)
        self.height_slider = QSlider(Qt.Horizontal)
        self.height_slider.setRange(300, 1080)
        self.height_slider.setValue(self.parent.config.window_height)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(300, 1080)
        self.height_spin.setValue(self.parent.config.window_height)
        self.height_slider.valueChanged.connect(self.height_spin.setValue)
        self.height_spin.valueChanged.connect(self.height_slider.setValue)
        self.height_spin.valueChanged.connect(self.change_window_size)
        size_layout.addWidget(self.height_slider, 2, 1)
        size_layout.addWidget(self.height_spin, 2, 2)

        size_layout.addWidget(QLabel("Прозрачность:"), 3, 0)
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(self.parent.config.window_opacity * 100))
        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(0, 100)
        self.opacity_spin.setValue(int(self.parent.config.window_opacity * 100))
        self.opacity_slider.valueChanged.connect(self.opacity_spin.setValue)
        self.opacity_spin.valueChanged.connect(self.opacity_slider.setValue)
        self.opacity_spin.valueChanged.connect(self.change_opacity)
        size_layout.addWidget(self.opacity_slider, 3, 1)
        size_layout.addWidget(self.opacity_spin, 3, 2)
        layout.addWidget(size_group)

        hotkey_group = QFrame()
        hotkey_group.setObjectName("settingsGroup")
        hotkey_layout = QGridLayout(hotkey_group)
        hotkey_layout.setContentsMargins(10, 10, 10, 10)
        hotkey_layout.setVerticalSpacing(4)
        hotkey_layout.setHorizontalSpacing(6)
        
        hotkey_title = QLabel("⌨ ГОРЯЧИЕ КЛАВИШИ")
        hotkey_title.setObjectName("groupLabel")
        hotkey_title.setAlignment(Qt.AlignCenter)
        hotkey_title.setFixedHeight(28)
        hotkey_layout.addWidget(hotkey_title, 0, 0, 1, 2)
        
        hotkey_layout.addWidget(QLabel("Показать/скрыть:"), 1, 0)
        self.toggle_hotkey_edit = SingleKeySequenceEdit()
        self.toggle_hotkey_edit.set_custom_key_string(self.parent.config.hotkeys["toggle_overlay"])
        self.toggle_hotkey_edit.editingFinished.connect(self.update_hotkeys)
        hotkey_layout.addWidget(self.toggle_hotkey_edit, 1, 1)

        hotkey_layout.addWidget(QLabel("Click-Through:"), 2, 0)
        self.click_through_hotkey_edit = SingleKeySequenceEdit()
        self.click_through_hotkey_edit.set_custom_key_string(self.parent.config.hotkeys["toggle_click_through"])
        self.click_through_hotkey_edit.editingFinished.connect(self.update_hotkeys)
        hotkey_layout.addWidget(self.click_through_hotkey_edit, 2, 1)

        hotkey_layout.addWidget(QLabel("Panic:"), 3, 0)
        self.panic_hotkey_edit = SingleKeySequenceEdit()
        self.panic_hotkey_edit.set_custom_key_string(self.parent.config.hotkeys["panic_close"])
        self.panic_hotkey_edit.editingFinished.connect(self.update_hotkeys)
        hotkey_layout.addWidget(self.panic_hotkey_edit, 3, 1)
        layout.addWidget(hotkey_group)

        colors_group = QFrame()
        colors_group.setObjectName("settingsGroup")
        colors_layout = QVBoxLayout(colors_group)
        colors_layout.setContentsMargins(10, 10, 10, 10)
        colors_layout.setSpacing(4)
        
        colors_title = QLabel("🎨 ЦВЕТА")
        colors_title.setObjectName("groupLabel")
        colors_title.setAlignment(Qt.AlignCenter)
        colors_title.setFixedHeight(28)
        colors_layout.addWidget(colors_title)
        
        self.color_buttons = {}
        self.animation_mode_combos = {}
        color_options = [
            ("background", "Фон"), ("surface", "Поверхности"),
            ("border", "Границы"), ("text", "Текст"),
            ("text_secondary", "Втор. текст"), ("accent", "Акцент"),
            ("hover", "Наведение"), ("pressed", "Нажатие"),
            ("titlebar", "Заголовок"), ("sidebar", "Сайдбар"),
            ("scrollbar_background", "Скролл фон"), ("scrollbar_handle", "Скролл ручка")
        ]
        
        for key, label in color_options:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(6)
            
            label_widget = QLabel(label + ":")
            label_widget.setFixedWidth(100)
            row_layout.addWidget(label_widget)
            
            btn = QPushButton()
            btn.setFixedSize(30, 20)
            btn.setStyleSheet(f"background-color: {self.parent.config.config['colors'][key]}; border-radius: 10px;")
            btn.clicked.connect(lambda checked, k=key: self.choose_color(k))
            row_layout.addWidget(btn)
            self.color_buttons[key] = btn
            
            combo = QComboBox()
            combo.addItem("Нет", "none")
            combo.addItem("Радуга", "rainbow")
            combo.addItem("Градиент", "gradient")
            current_mode = self.parent.config.config["animation_modes"].get(key, "none")
            combo.setCurrentIndex(combo.findData(current_mode) if combo.findData(current_mode) != -1 else 0)
            combo.currentIndexChanged.connect(lambda idx, k=key, cb=combo: self.change_animation_mode(k, cb.currentData()))
            row_layout.addWidget(combo, 1)
            self.animation_mode_combos[key] = combo
            
            colors_layout.addWidget(row_widget)
        
        layout.addWidget(colors_group)

        actions_group = QFrame()
        actions_group.setObjectName("settingsGroup")
        actions_layout = QHBoxLayout(actions_group)
        actions_layout.setContentsMargins(10, 10, 10, 10)
        actions_layout.setSpacing(6)
        
        self.reset_btn = QPushButton("🔄 Сброс")
        self.reset_btn.setObjectName("themeButton")
        self.reset_btn.clicked.connect(self.reset_settings)
        
        self.reload_btn = QPushButton("📥 Обновить")
        self.reload_btn.setObjectName("themeButton")
        self.reload_btn.clicked.connect(self.parent.reload_data)
        
        actions_layout.addWidget(self.reset_btn)
        actions_layout.addWidget(self.reload_btn)
        layout.addWidget(actions_group)

        contacts_group = QFrame()
        contacts_group.setObjectName("settingsGroup")
        contacts_layout = QVBoxLayout(contacts_group)
        contacts_layout.setContentsMargins(15, 15, 15, 15)
        contacts_layout.setSpacing(8)
        
        contacts_title = QLabel("📞 КОНТАКТЫ")
        contacts_title.setObjectName("groupLabel")
        contacts_title.setAlignment(Qt.AlignCenter)
        contacts_title.setFixedHeight(28)
        contacts_layout.addWidget(contacts_title)
        
        discord_label = QLabel("Дискорд: Скоро")
        discord_label.setStyleSheet("color: #F9FAFB; font-size: 12px;")
        contacts_layout.addWidget(discord_label)
        
        tg_label = QLabel('<a href="https://t.me/sixseven_project" style="color: #F9FAFB; text-decoration: none; font-size: 12px;">Телеграм: t.me/sixseven_project</a>')
        tg_label.setOpenExternalLinks(True)
        contacts_layout.addWidget(tg_label)
        
        github_label = QLabel('<a href="https://github.com/Faglig" style="color: #F9FAFB; text-decoration: none; font-size: 12px;">Гитхаб: github.com/Faglig</a>')
        github_label.setOpenExternalLinks(True)
        contacts_layout.addWidget(github_label)
        
        profile_widget = QWidget()
        profile_layout = QHBoxLayout(profile_widget)
        profile_layout.setContentsMargins(0, 8, 0, 0)
        profile_layout.setSpacing(10)
        
        self.contact_image_label = QLabel()
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "contact_image.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.contact_image_label.setPixmap(pixmap)
        self.contact_image_label.setFixedSize(60, 60)
        self.contact_image_label.setScaledContents(True)
        self.contact_image_label.setAlignment(Qt.AlignCenter)
        self.contact_image_label.setCursor(Qt.PointingHandCursor)
        self.contact_image_label.mousePressEvent = self.open_contact_link
        profile_layout.addWidget(self.contact_image_label)
        
        profile_text_layout = QVBoxLayout()
        profile_text_layout.setSpacing(2)
        
        self.contact_link = "https://rt.pornhub.com/model/sweetie-fox"
        
        nickname = QLabel(f'<a href="{self.contact_link}" style="color: #F9FAFB; text-decoration: none; font-size: 14px; font-weight: bold;">Sweetie Fox</a>')
        nickname.setOpenExternalLinks(True)
        nickname.setCursor(Qt.PointingHandCursor)
        profile_text_layout.addWidget(nickname)
        
        role = QLabel("Вдохновитель проекта")
        role.setStyleSheet("color: #D1D5DB; font-size: 11px;")
        profile_text_layout.addWidget(role)
        
        profile_layout.addLayout(profile_text_layout)
        profile_layout.addStretch()
        
        contacts_layout.addWidget(profile_widget)
        
        layout.addWidget(contacts_group)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.update_theme_buttons()

    def apply_builtin_theme(self, theme_name):
        if self.parent.config.apply_theme(theme_name):
            self.parent.update_stylesheet()
            self.update_ui_from_config()

    def apply_custom_theme_slot(self, slot_name):
        if self.parent.config.apply_custom_theme(slot_name):
            self.parent.update_stylesheet()
            self.update_ui_from_config()

    def save_current_theme_to_slot(self):
        slot_name, ok = QInputDialog.getItem(self, "Сохранение", "Слот:", ["Слот 1", "Слот 2", "Слот 3", "Слот 4", "Слот 5"], 0, False)
        if ok:
            self.parent.config.save_current_as_theme(slot_name)
            self.update_theme_buttons()

    def clear_theme_slot(self):
        slot_name, ok = QInputDialog.getItem(self, "Очистка", "Слот:", ["Слот 1", "Слот 2", "Слот 3", "Слот 4", "Слот 5"], 0, False)
        if ok:
            self.parent.config.config["custom_themes"][slot_name] = None
            self.parent.config.save()

    def update_theme_buttons(self):
        current = self.parent.config.config.get("current_theme", "")
        for name, btn in self.theme_buttons.items():
            btn.setChecked(name == current)
        for name, btn in self.custom_theme_buttons.items():
            btn.setChecked(name == current)

    def change_window_size(self):
        self.parent.config.window_width = self.width_spin.value()
        self.parent.config.window_height = self.height_spin.value()
        self.parent.resize(self.parent.config.window_width, self.parent.config.window_height)

    def change_opacity(self):
        self.parent.config.window_opacity = self.opacity_spin.value() / 100.0
        self.parent.setWindowOpacity(self.parent.config.window_opacity)

    def update_hotkeys(self):
        hotkeys = {
            "toggle_overlay": self.toggle_hotkey_edit.get_custom_key_string(),
            "toggle_click_through": self.click_through_hotkey_edit.get_custom_key_string(),
            "panic_close": self.panic_hotkey_edit.get_custom_key_string()
        }
        self.parent.config.hotkeys = hotkeys
        self.parent.config.save()
        self.parent.setup_hotkeys()

    def choose_color(self, key):
        dialog = ColorPickerDialog(self, self.parent.config.config["colors"][key], "Выбор цвета")
        if dialog.exec_() == ColorPickerDialog.Accepted:
            color = dialog.get_color()
            self.parent.config.config["colors"][key] = color.name()
            self.color_buttons[key].setStyleSheet(f"background-color: {color.name()}; border-radius: 10px;")
            self.parent.update_stylesheet()

    def change_animation_mode(self, key, mode):
        self.parent.config.config["animation_modes"][key] = mode
        self.parent.restart_animation_timer()
        self.parent.update_stylesheet()

    def reset_settings(self):
        self.parent.config.reset()
        self.parent.apply_settings()
        self.parent.setup_hotkeys()
        self.update_ui_from_config()

    def update_ui_from_config(self):
        self.width_slider.setValue(self.parent.config.window_width)
        self.height_slider.setValue(self.parent.config.window_height)
        self.opacity_slider.setValue(int(self.parent.config.window_opacity * 100))
        self.opacity_spin.setValue(int(self.parent.config.window_opacity * 100))
        self.toggle_hotkey_edit.set_custom_key_string(self.parent.config.hotkeys["toggle_overlay"])
        self.click_through_hotkey_edit.set_custom_key_string(self.parent.config.hotkeys["toggle_click_through"])
        self.panic_hotkey_edit.set_custom_key_string(self.parent.config.hotkeys["panic_close"])
        for key, btn in self.color_buttons.items():
            btn.setStyleSheet(f"background-color: {self.parent.config.config['colors'][key]}; border-radius: 10px;")
        for key, combo in self.animation_mode_combos.items():
            mode = self.parent.config.config["animation_modes"].get(key, "none")
            idx = combo.findData(mode)
            if idx >= 0:
                combo.setCurrentIndex(idx)
        self.update_theme_buttons()

    def open_contact_link(self, event):
        webbrowser.open(self.contact_link)

    def show_update_available(self, version):
        pass