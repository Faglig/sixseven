# file: tabs/features_tab.py

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel, QGridLayout, QGraphicsOpacityEffect
)
import re


class FeaturesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        title = QLabel("✨ ФИЧИ")
        title.setObjectName("groupLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(30)
        title.setFixedWidth(100)
        layout.addWidget(title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        self.grid.setSpacing(8)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll, 1)

        self.data = []

    def set_data(self, data):
        if isinstance(data, str):
            self.data = self.parse_markdown(data)
        elif isinstance(data, list):
            self.data = data
        else:
            self.data = []
        self.refresh_cards()

    def parse_markdown(self, md_text):
        """Парсит Markdown текст в список фич"""
        features = []
        
        parts = re.split(r'^##?\s+', md_text, flags=re.MULTILINE)
        
        if parts and not parts[0].strip():
            parts = parts[1:]
        
        for part in parts:
            if not part.strip():
                continue
            
            lines = part.strip().split('\n')
            title = lines[0].strip()
            
            # Ищем описание (всё что после заголовка)
            description_lines = []
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('- '):
                    description_lines.append(line[2:])
                elif line:
                    description_lines.append(line)
            
            description = '\n'.join(description_lines).strip()
            
            features.append({
                "title": title,
                "description": description
            })
        
        return features

    def refresh_cards(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for i, feature in enumerate(self.data):
            card = QFrame()
            card.setObjectName("featureCard")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(8, 8, 8, 8)
            card_layout.setSpacing(4)
            
            title_label = QLabel(feature.get("title", "Без названия"))
            title_label.setObjectName("groupLabel")
            title_label.setFixedHeight(25)
            
            desc_label = QLabel(feature.get("description", ""))
            desc_label.setWordWrap(True)
            desc_label.setTextFormat(Qt.MarkdownText)
            
            card_layout.addWidget(title_label)
            card_layout.addWidget(desc_label)
            self.grid.addWidget(card, i // 2, i % 2)