import sys
import os
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QSystemTrayIcon, QMenu, QAction
)

from styles import get_stylesheet
from config_manager import ConfigManager
from network_worker import DownloadWorker
from tabs.laws_tab import LawsTab
from tabs.features_tab import FeaturesTab
from tabs.calculator_tab import CalculatorTab
from tabs.notes_tab import NotesTab
from tabs.chatbot_tab import ChatbotTab
from tabs.settings_tab import SettingsTab
from hotkey_manager import HotkeyManager
from version_checker import VersionChecker


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(36)
        self.setObjectName("titleBar")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(4)

        self.logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedSize(24, 24)
        layout.addWidget(self.logo_label)

        self.title_label = QLabel("SixSeven Project")
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.minimize_btn = QPushButton("—")
        self.maximize_btn = QPushButton("□")
        self.close_btn = QPushButton("✕")
        for btn in (self.minimize_btn, self.maximize_btn, self.close_btn):
            btn.setFixedSize(28, 28)
            btn.setObjectName("titleButton")
            layout.addWidget(btn)

        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.parent.close)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.moving = True
            self.parent.offset = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.parent.moving:
            self.parent.move(event.globalPos() - self.parent.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.parent.moving = False
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.moving = False
        self.offset = None
        self.config = ConfigManager()
        self.hotkey_manager = HotkeyManager(self)

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.setInterval(50)

        self.rainbow_hue = 0
        self.gradient_phase = 0.0
        self.animated_colors = {}

        self.click_through_enabled = False
        self.fade_animation = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("SixSeven Project")

        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.app_icon = QIcon(icon_path)
        else:
            self.app_icon = self.style().standardIcon(self.style().SP_ComputerIcon)
        self.setWindowIcon(self.app_icon)

        if sys.platform == "win32":
            try:
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SixSevenProject.Overlay.1.0")
            except:
                pass

        self.resize(self.config.window_width, self.config.window_height)

        outer_widget = QWidget()
        outer_layout = QVBoxLayout(outer_widget)
        outer_layout.setContentsMargins(2, 2, 2, 2)
        outer_layout.setSpacing(0)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        central_layout.addWidget(self.title_bar)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(90)
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(4, 8, 4, 8)
        sidebar_layout.setSpacing(2)

        self.nav_buttons = []
        self.pages = QStackedWidget()

        self.create_nav_button("Законы", 0)
        self.create_nav_button("Фичи", 1)
        self.create_nav_button("Калькулятор", 2)
        self.create_nav_button("Заметки", 3)
        self.create_nav_button("Чат-бот", 4)

        sidebar_layout.addStretch()

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setCheckable(True)
        self.settings_btn.setAutoExclusive(True)
        self.settings_btn.setFixedSize(80, 36)
        self.settings_btn.setObjectName("navButton")
        self.settings_btn.setToolTip("Настройки")
        self.settings_btn.clicked.connect(lambda checked: self.switch_page(5))
        sidebar_layout.addWidget(self.settings_btn)
        self.nav_buttons.append(self.settings_btn)

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages, 1)
        central_layout.addWidget(content_widget)

        outer_layout.addWidget(central_widget)
        self.setCentralWidget(outer_widget)

        self.laws_tab = LawsTab(self)
        self.features_tab = FeaturesTab(self)
        self.calculator_tab = CalculatorTab()
        self.notes_tab = NotesTab()
        self.chatbot_tab = ChatbotTab()
        self.settings_tab = SettingsTab(self)

        self.pages.addWidget(self.laws_tab)
        self.pages.addWidget(self.features_tab)
        self.pages.addWidget(self.calculator_tab)
        self.pages.addWidget(self.notes_tab)
        self.pages.addWidget(self.chatbot_tab)
        self.pages.addWidget(self.settings_tab)

        self.setMinimumSize(300, 200)
        self.pages.setMinimumSize(300, 200)
        for tab in [self.laws_tab, self.features_tab, self.calculator_tab, self.notes_tab, self.chatbot_tab, self.settings_tab]:
            tab.setMinimumHeight(100)
            tab.setMinimumWidth(300)

        self.setup_tray_icon()
        self.load_data()
        self.apply_settings()
        self.setup_hotkeys()
        self.check_for_updates()
        self.update_stylesheet()
        self.show_with_animation()

    def create_nav_button(self, text, index):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setFixedSize(80, 30)
        btn.setObjectName("navButton")
        btn.clicked.connect(lambda checked, idx=index: self.switch_page(idx))
        self.sidebar.layout().addWidget(btn)
        self.nav_buttons.append(btn)
        if index == 0:
            btn.setChecked(True)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        if index == 5:
            self.settings_btn.setChecked(True)
        else:
            for btn in self.nav_buttons:
                if btn is not self.settings_btn:
                    btn.setChecked(False)

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.app_icon)
        self.tray_icon.setToolTip("SixSeven Project")
        tray_menu = QMenu()
        self.tray_show_action = QAction("Показать/Скрыть", self)
        self.tray_show_action.triggered.connect(self.toggle_overlay)
        self.tray_click_through_action = QAction("Click-through режим", self)
        self.tray_click_through_action.setCheckable(True)
        self.tray_click_through_action.triggered.connect(self.toggle_click_through)
        self.tray_exit_action = QAction("Выход", self)
        self.tray_exit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(self.tray_show_action)
        tray_menu.addAction(self.tray_click_through_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.tray_exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_overlay()

    def toggle_overlay(self):
        if self.isVisible():
            self.hide_with_animation()
        else:
            self.show_with_animation()

    def show_with_animation(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity", self)
        self.fade_animation.setDuration(250)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(self.config.window_opacity)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.start(QAbstractAnimation.DeleteWhenStopped)

    def hide_with_animation(self):
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity", self)
        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(self.windowOpacity())
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start(QAbstractAnimation.DeleteWhenStopped)

    def toggle_click_through(self):
        self.click_through_enabled = not self.click_through_enabled
        if self.click_through_enabled:
            self.setWindowFlag(Qt.WindowTransparentForInput, True)
        else:
            self.setWindowFlag(Qt.WindowTransparentForInput, False)
        self.tray_click_through_action.setChecked(self.click_through_enabled)
        self.show()
        self.raise_()

    def panic_close(self):
        self.hotkey_manager.unregister_all()
        self.config.window_width = self.width()
        self.config.window_height = self.height()
        self.config.save()
        self.tray_icon.hide()
        QApplication.quit()

    def quit_application(self):
        self.hotkey_manager.unregister_all()
        self.config.window_width = self.width()
        self.config.window_height = self.height()
        self.config.save()
        self.hide_with_animation()
        QTimer.singleShot(250, QApplication.quit)

    def load_data(self):
        self.laws_worker = DownloadWorker("https://raw.githubusercontent.com/Faglig/sixseven/main/laws.json")
        self.laws_worker.data_loaded.connect(self.laws_tab.set_data)
        self.laws_worker.error.connect(lambda msg: print(f"Ошибка загрузки законов: {msg}"))
        self.laws_worker.start()
        self.features_worker = DownloadWorker("https://raw.githubusercontent.com/Faglig/sixseven/main/features.json")
        self.features_worker.data_loaded.connect(self.features_tab.set_data)
        self.features_worker.error.connect(lambda msg: print(f"Ошибка загрузки фич: {msg}"))
        self.features_worker.start()

    def reload_data(self):
        if hasattr(self, 'laws_worker') and self.laws_worker.isRunning():
            self.laws_worker.terminate()
        if hasattr(self, 'features_worker') and self.features_worker.isRunning():
            self.features_worker.terminate()
        self.load_data()

    def apply_settings(self):
        self.resize(self.config.window_width, self.config.window_height)
        self.setWindowOpacity(self.config.window_opacity)
        self.update_stylesheet()
        self.restart_animation_timer()

    def update_stylesheet(self):
        colors = self.config.config["colors"].copy()
        for key, mode in self.config.config["animation_modes"].items():
            if mode != "none" and key in self.animated_colors:
                colors[key] = self.animated_colors[key]
        if self.config.rainbow_enabled and self.config.config["animation_modes"].get("accent") == "none":
            colors["accent"] = self.animated_colors.get("accent", colors["accent"])
        translucent = self.config.window_opacity < 0.99
        self.setStyleSheet(get_stylesheet(colors, translucent=translucent))

    def restart_animation_timer(self):
        any_animation = False
        for mode in self.config.config["animation_modes"].values():
            if mode != "none":
                any_animation = True
                break
        if self.config.rainbow_enabled and self.config.config["animation_modes"].get("accent") == "none":
            any_animation = True
        if any_animation:
            if not self.animation_timer.isActive():
                self.update_animation()
                self.animation_timer.start()
        else:
            self.animation_timer.stop()
            self.animated_colors.clear()

    def update_animation(self):
        import math
        self.rainbow_hue = (self.rainbow_hue + 1) % 360
        self.gradient_phase = (math.sin(self.rainbow_hue * 0.02 * self.config.config["gradient_speed"]) + 1) / 2
        c1 = QColor(self.config.config["gradient_color1"])
        c2 = QColor(self.config.config["gradient_color2"])
        for key, mode in self.config.config["animation_modes"].items():
            if mode == "rainbow":
                offset = list(self.config.config["animation_modes"].keys()).index(key) * 30
                self.animated_colors[key] = QColor.fromHsv((self.rainbow_hue + offset) % 360, 255, 255).name()
            elif mode == "gradient":
                r = int(c1.red() + (c2.red() - c1.red()) * self.gradient_phase)
                g = int(c1.green() + (c2.green() - c1.green()) * self.gradient_phase)
                b = int(c1.blue() + (c2.blue() - c1.blue()) * self.gradient_phase)
                self.animated_colors[key] = QColor(r, g, b).name()
        if self.config.rainbow_enabled and self.config.config["animation_modes"].get("accent") == "none":
            self.animated_colors["accent"] = QColor.fromHsv(self.rainbow_hue, 255, 255).name()
        self.update_stylesheet()

    def setup_hotkeys(self):
        self.hotkey_manager.register_hotkeys(self.config.hotkeys)

    def check_for_updates(self):
        self.version_checker = VersionChecker()
        self.version_checker.update_available.connect(self.settings_tab.show_update_available)
        self.version_checker.start()

    def hideEvent(self, event):
        if self.animation_timer.isActive():
            self.animation_timer.setInterval(1000)
        super().hideEvent(event)

    def showEvent(self, event):
        if self.animation_timer.isActive():
            self.animation_timer.setInterval(50)
        super().showEvent(event)

    def closeEvent(self, event):
        self.hotkey_manager.unregister_all()
        self.config.window_width = self.width()
        self.config.window_height = self.height()
        self.config.save()
        self.tray_icon.hide()
        if self.windowOpacity() < 0.1:
            event.accept()
        else:
            event.ignore()
            self.fade_animation = QPropertyAnimation(self, b"windowOpacity", self)
            self.fade_animation.setDuration(200)
            self.fade_animation.setStartValue(self.windowOpacity())
            self.fade_animation.setEndValue(0.0)
            self.fade_animation.setEasingCurve(QEasingCurve.InCubic)
            self.fade_animation.finished.connect(self.close)
            self.fade_animation.start(QAbstractAnimation.DeleteWhenStopped)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())