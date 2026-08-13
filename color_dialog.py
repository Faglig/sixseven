

import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QLabel, QSlider, QSpinBox, QFrame
)

FAVORITES_FILE = os.path.join(os.path.dirname(__file__), "favorites.json")


class ColorPickerDialog(QDialog):
    def __init__(self, parent=None, initial_color="#FFFFFF", title="Выбор цвета"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setFixedSize(460, 560)
        self.setStyleSheet(self.get_dialog_style())
        self.selected_color = QColor(initial_color)
        self.favorite_colors = self.load_favorites()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.preview_label = QLabel()
        self.preview_label.setFixedHeight(50)
        self.preview_label.setStyleSheet(f"background-color: {self.selected_color.name()}; border: 1px solid #3C3C3C; border-radius: 6px;")
        layout.addWidget(self.preview_label)

        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("HEX:"))
        self.hex_edit = QLineEdit()
        self.hex_edit.setText(self.selected_color.name())
        self.hex_edit.setMaxLength(7)
        self.hex_edit.returnPressed.connect(self.apply_hex)
        hex_layout.addWidget(self.hex_edit)
        layout.addLayout(hex_layout)

        self.r_slider, self.r_spin = self.create_rgb_row("R:", layout)
        self.g_slider, self.g_spin = self.create_rgb_row("G:", layout)
        self.b_slider, self.b_spin = self.create_rgb_row("B:", layout)

        self.r_slider.setValue(self.selected_color.red())
        self.g_slider.setValue(self.selected_color.green())
        self.b_slider.setValue(self.selected_color.blue())

        self.favorites_frame = QFrame()
        self.favorites_layout = QHBoxLayout(self.favorites_frame)
        self.favorites_layout.setContentsMargins(0, 0, 0, 0)
        self.favorites_layout.setSpacing(4)
        layout.addWidget(QLabel("Избранное:"))
        layout.addWidget(self.favorites_frame)
        self.refresh_favorites()

        fav_btn_layout = QHBoxLayout()
        self.add_fav_btn = QPushButton("+ В избранное")
        self.add_fav_btn.clicked.connect(self.add_to_favorites)
        self.remove_fav_btn = QPushButton("− Удалить")
        self.remove_fav_btn.clicked.connect(self.remove_from_favorites)
        fav_btn_layout.addWidget(self.add_fav_btn)
        fav_btn_layout.addWidget(self.remove_fav_btn)
        layout.addLayout(fav_btn_layout)

        color_list = [
            "#FFFFFF", "#C0C0C0", "#808080", "#000000",
            "#FF0000", "#800000", "#FFFF00", "#808000",
            "#00FF00", "#008000", "#00FFFF", "#008080",
            "#0000FF", "#000080", "#FF00FF", "#800080",
            "#9333EA", "#22C55E", "#0078D4", "#FF6B00",
            "#FFD700", "#FF1493", "#8B4513", "#2E8B57"
        ]
        grid = QGridLayout()
        grid.setSpacing(4)
        for i, color_name in enumerate(color_list):
            btn = self.create_color_button(color_name)
            btn.clicked.connect(lambda checked, c=color_name: self.set_color_from_button(c))
            grid.addWidget(btn, i // 6, i % 6)
        layout.addLayout(grid)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.r_slider.valueChanged.connect(self.update_from_rgb)
        self.g_slider.valueChanged.connect(self.update_from_rgb)
        self.b_slider.valueChanged.connect(self.update_from_rgb)
        self.r_spin.valueChanged.connect(self.update_from_spin)
        self.g_spin.valueChanged.connect(self.update_from_spin)
        self.b_spin.valueChanged.connect(self.update_from_spin)

    def create_rgb_row(self, label_text, parent_layout):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 255)
        spin = QSpinBox()
        spin.setRange(0, 255)
        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)
        row.addWidget(slider)
        row.addWidget(spin)
        parent_layout.addLayout(row)
        return slider, spin

    def create_color_button(self, color_name):
        btn = QPushButton()
        btn.setProperty("colorSwatch", True)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet(f"background-color: {color_name};")
        return btn

    def get_dialog_style(self):
        return """
        QDialog {
            background: #1E1E1E;
            border: 1px solid #3C3C3C;
            border-radius: 8px;
        }
        QLabel {
            color: #FFFFFF;
        }
        QLineEdit {
            background: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #3C3C3C;
            border-radius: 4px;
            padding: 4px;
        }
        QPushButton {
            background: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #3C3C3C;
            border-radius: 4px;
            padding: 5px 12px;
        }
        QPushButton:hover {
            background: #3C3C3C;
        }
        QPushButton:pressed {
            background: #2A2A2A;
        }
        QPushButton[colorSwatch="true"] {
            background: transparent;
            border: 1px solid #3C3C3C;
            border-radius: 4px;
            padding: 0;
        }
        QPushButton[colorSwatch="true"]:hover {
            border-color: #FFFFFF;
        }
        QSlider::groove:horizontal {
            height: 4px;
            background: #3C3C3C;
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            width: 14px;
            height: 14px;
            margin: -5px 0;
            background: #9333EA;
            border-radius: 7px;
        }
        QSpinBox {
            background: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #3C3C3C;
            border-radius: 4px;
            padding: 2px;
        }
        """

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
            except:
                pass
        return []

    def save_favorites(self):
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.favorite_colors, f, indent=2, ensure_ascii=False)

    def refresh_favorites(self):
        while self.favorites_layout.count():
            item = self.favorites_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for color_name in self.favorite_colors:
            btn = self.create_color_button(color_name)
            btn.clicked.connect(lambda checked, c=color_name: self.set_color_from_button(c))
            self.favorites_layout.addWidget(btn)
        self.favorites_layout.addStretch()

    def add_to_favorites(self):
        color_name = self.selected_color.name()
        if color_name not in self.favorite_colors:
            self.favorite_colors.append(color_name)
            self.save_favorites()
            self.refresh_favorites()

    def remove_from_favorites(self):
        color_name = self.selected_color.name()
        if color_name in self.favorite_colors:
            self.favorite_colors.remove(color_name)
            self.save_favorites()
            self.refresh_favorites()

    def set_color_from_button(self, color_name):
        self.selected_color = QColor(color_name)
        self.update_controls_from_color()

    def apply_hex(self):
        text = self.hex_edit.text().strip()
        if text.startswith('#'):
            text = text[1:]
        if len(text) == 6:
            color = QColor(f"#{text}")
            if color.isValid():
                self.selected_color = color
                self.update_controls_from_color()
        else:
            self.hex_edit.setText(self.selected_color.name())

    def update_from_rgb(self):
        r = self.r_slider.value()
        g = self.g_slider.value()
        b = self.b_slider.value()
        self.selected_color = QColor(r, g, b)
        self.update_controls_from_color()

    def update_from_spin(self):
        r = self.r_spin.value()
        g = self.g_spin.value()
        b = self.b_spin.value()
        self.selected_color = QColor(r, g, b)
        self.update_controls_from_color()

    def update_controls_from_color(self):
        self.hex_edit.setText(self.selected_color.name())
        self.preview_label.setStyleSheet(f"background-color: {self.selected_color.name()}; border: 1px solid #3C3C3C; border-radius: 6px;")
        self.r_slider.setValue(self.selected_color.red())
        self.g_slider.setValue(self.selected_color.green())
        self.b_slider.setValue(self.selected_color.blue())
        self.r_spin.setValue(self.selected_color.red())
        self.g_spin.setValue(self.selected_color.green())
        self.b_spin.setValue(self.selected_color.blue())

    def get_color(self):
        return self.selected_color