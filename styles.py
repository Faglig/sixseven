

from PyQt5.QtGui import QColor

def get_stylesheet(colors, translucent=True):
    background = colors.get("background", "#111827")
    surface = colors.get("surface", "#1F2937")
    border = colors.get("border", "#2A2A2A")  # Тёмно-серый для границ
    text = colors.get("text", "#F9FAFB")
    text_secondary = colors.get("text_secondary", "#D1D5DB")
    accent = colors.get("accent", "#9333EA")
    hover = colors.get("hover", "#4B5563")
    pressed = colors.get("pressed", "#374151")
    titlebar = colors.get("titlebar", "#1F2937")
    sidebar = colors.get("sidebar", "#111827")
    scrollbar_background = colors.get("scrollbar_background", "#111827")
    scrollbar_handle = colors.get("scrollbar_handle", "#4B5563")

    return f"""
    * {{
        font-family: 'Segoe UI', 'Arial', sans-serif;
        outline: none;
        color: {text};
        background: transparent;
    }}
    QMainWindow {{
        background: transparent;
    }}
    QWidget#centralWidget {{
        background: {background};
        border-radius: 15px;
        border: 1px solid {border};
    }}
    QWidget#titleBar {{
        background: {titlebar};
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
        border-bottom: 1px solid {border};
    }}
    QFrame#sidebar {{
        background: {sidebar};
        border-bottom-left-radius: 15px;
        border-right: 1px solid {border};
    }}
    QPushButton#navButton {{
        background: transparent;
        color: {text_secondary};
        border: 1px solid transparent;
        border-radius: 10px;
        font-size: 11px;
        padding: 8px;
        text-align: left;
        font-weight: 500;
    }}
    QPushButton#navButton:hover {{
        background: {surface};
        color: {text};
        border-color: {border};
    }}
    QPushButton#navButton:checked {{
        background: {accent};
        color: white;
        border-color: {accent};
        font-weight: bold;
    }}
    QPushButton#titleButton {{
        background: transparent;
        color: {text_secondary};
        border: 1px solid transparent;
        border-radius: 10px;
        font-size: 14px;
        min-width: 28px;
        min-height: 28px;
    }}
    QPushButton#titleButton:hover {{
        background: {surface};
        color: {text};
        border-color: {border};
    }}
    QPushButton {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background: {hover};
        border-color: {accent};
    }}
    QPushButton:pressed {{
        background: {pressed};
    }}
    QPushButton#themeButton {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 8px;
        font-size: 10px;
    }}
    QPushButton#themeButton:hover {{
        border-color: {accent};
    }}
    QPushButton#themeButton:checked {{
        background: {accent};
        color: white;
        border-color: {accent};
    }}
    QPushButton#formatButton {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 4px 8px;
        font-size: 12px;
        min-width: 28px;
    }}
    QPushButton#formatButton:hover {{
        border-color: {accent};
    }}
    QPushButton#formatButton:checked {{
        background: {accent};
        color: white;
        border-color: {accent};
    }}
    QLineEdit {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 12px;
    }}
    QLineEdit:focus {{
        border: 1px solid {accent};
    }}
    QTextEdit, QTextBrowser {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 8px;
        font-size: 12px;
    }}
    QListWidget {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 4px;
    }}
    QListWidget::item {{
        padding: 6px 8px;
        border-radius: 8px;
        margin: 1px;
        border: 1px solid transparent;
    }}
    QListWidget::item:selected {{
        background: {accent};
        color: white;
        border-color: {accent};
    }}
    QListWidget::item:hover {{
        background: {hover};
        border-color: {border};
    }}
    QComboBox {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 8px;
        font-size: 12px;
    }}
    QComboBox:focus {{
        border: 1px solid {accent};
    }}
    QComboBox QAbstractItemView {{
        background: {surface};
        color: {text};
        selection-background-color: {accent};
        border: 1px solid {border};
        border-radius: 10px;
    }}
    QSpinBox {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 8px;
        font-size: 12px;
    }}
    QSpinBox:focus {{
        border: 1px solid {accent};
    }}
    QSpinBox::up-button, QSpinBox::down-button {{
        width: 16px;
        background: {hover};
        border: none;
        border-radius: 5px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background: {accent};
    }}
    QSpinBox::up-arrow, QSpinBox::down-arrow {{
        width: 0;
        height: 0;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
    }}
    QSpinBox::up-arrow {{
        border-bottom: 4px solid {text};
    }}
    QSpinBox::down-arrow {{
        border-top: 4px solid {text};
    }}
    QKeySequenceEdit {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 8px;
        font-size: 12px;
    }}
    QKeySequenceEdit:focus {{
        border: 1px solid {accent};
    }}
    QScrollArea {{
        background: transparent;
        border: none;
    }}
    QFrame {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 10px;
    }}
    QFrame#settingsGroup {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 10px;
    }}
    QFrame#featureCard {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 10px;
    }}
    QFrame#featureCard:hover {{
        border-color: {accent};
    }}
    QLabel {{
        background: transparent;
        color: {text};
        font-size: 12px;
    }}
    QLabel#groupLabel {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 6px 10px;
        font-weight: bold;
        font-size: 12px;
    }}
    QScrollBar:vertical {{
        background: {scrollbar_background};
        width: 8px;
        border-radius: 4px;
        border: none;
    }}
    QScrollBar::handle:vertical {{
        background: {scrollbar_handle};
        border-radius: 4px;
        min-height: 20px;
        border: none;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {accent};
    }}
    QScrollBar:horizontal {{
        background: {scrollbar_background};
        height: 8px;
        border-radius: 4px;
        border: none;
    }}
    QScrollBar::handle:horizontal {{
        background: {scrollbar_handle};
        border-radius: 4px;
        min-width: 20px;
        border: none;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {accent};
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 5px;
        border: 1px solid {border};
        background: {surface};
    }}
    QCheckBox::indicator:checked {{
        background: {accent};
        border-color: {accent};
    }}
    QSlider::groove:horizontal {{
        height: 4px;
        background: {border};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        width: 14px;
        height: 14px;
        margin: -5px 0;
        background: {accent};
        border-radius: 7px;
        border: 1px solid {border};
    }}
    QMenu {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 4px;
    }}
    QMenu::item {{
        padding: 5px 15px;
        border-radius: 8px;
    }}
    QMenu::item:selected {{
        background: {accent};
    }}
    QToolTip {{
        background: {surface};
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
    }}
    QDialog {{
        background: {background};
        border: 1px solid {border};
        border-radius: 10px;
    }}
    """