from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QListWidget, QTextEdit, QSplitter,
    QGraphicsOpacityEffect, QLabel, QHBoxLayout
)

class LawsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(6)
        
        title = QLabel("📜 ЗАКОНЫ")
        title.setObjectName("groupLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedWidth(150)
        title.setFixedHeight(30)
        top_layout.addWidget(title)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Поиск законов...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        top_layout.addWidget(self.search_input, 1)
        
        layout.addLayout(top_layout)

        self.search_results = QListWidget()
        self.search_results.setMaximumHeight(150)
        self.search_results.hide()
        self.search_results.itemClicked.connect(self.on_search_result_clicked)
        layout.addWidget(self.search_results)

        splitter = QSplitter(Qt.Horizontal)
        self.list_widget = QListWidget()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        splitter.addWidget(self.list_widget)
        splitter.addWidget(self.text_area)
        splitter.setSizes([200, 400])
        layout.addWidget(splitter, 1)

        self.list_widget.itemClicked.connect(self.on_item_clicked)

        self.content_effect = QGraphicsOpacityEffect(self)
        splitter.setGraphicsEffect(self.content_effect)
        self.content_effect.setOpacity(0.0)

    def set_data(self, data):
        if isinstance(data, dict):
            data = data.get('laws', data.get('data', []))
        self.data = data if isinstance(data, list) else []
        self.filter_list("")
        anim = QPropertyAnimation(self.content_effect, b"opacity", self)
        anim.setDuration(300)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def filter_list(self, text):
        self.list_widget.clear()
        for item in self.data:
            title = item.get("title", "")
            if text.lower() in title.lower():
                self.list_widget.addItem(title)

    def on_search_text_changed(self, text):
        self.filter_list(text)
        
        self.search_results.clear()
        if text.strip():
            matches = []
            for item in self.data:
                title = item.get("title", "")
                content = item.get("content", "")
                if text.lower() in title.lower():
                    matches.append(f"📜 {title}")
                elif text.lower() in content.lower():
                    idx = content.lower().find(text.lower())
                    start = max(0, idx - 30)
                    end = min(len(content), idx + 30)
                    snippet = content[start:end].replace('\n', ' ')
                    matches.append(f"🔍 {title}: ...{snippet}...")
            
            if matches:
                self.search_results.addItems(matches[:10])
                self.search_results.show()
            else:
                self.search_results.hide()
        else:
            self.search_results.hide()

    def on_search_result_clicked(self, item):
        result_text = item.text()
        search_text = self.search_input.text().strip()
        
        if result_text.startswith("📜 "):
            law_title = result_text[2:]
        elif result_text.startswith("🔍 "):
            law_title = result_text[2:].split(":")[0]
        else:
            law_title = result_text
        
        for law in self.data:
            if law.get("title") == law_title:
                self.display_law(law)
                if search_text:
                    self.highlight_search(search_text)
                for i in range(self.list_widget.count()):
                    if self.list_widget.item(i).text() == law_title:
                        self.list_widget.setCurrentRow(i)
                        break
                self.search_results.hide()
                break

    def on_item_clicked(self, item):
        title = item.text()
        for law in self.data:
            if law.get("title") == title:
                self.display_law(law)
                search_text = self.search_input.text().strip()
                if search_text:
                    self.highlight_search(search_text)

    def display_law(self, law):
        """Отображает закон с HTML-форматированием"""
        title = law.get("title", "")
        content = law.get("content", "")
        color = law.get("color", "#F9FAFB")
        font_size = law.get("font_size", 12)
        font_family = law.get("font_family", "Arial")
        bold = law.get("bold", False)
        italic = law.get("italic", False)
        underline = law.get("underline", False)
        background = law.get("background", "transparent")
        alignment = law.get("alignment", "left")
        
        align_map = {
            "left": "left",
            "center": "center",
            "right": "right",
            "justify": "justify"
        }
        align = align_map.get(alignment, "left")
        
        font_weight = "bold" if bold else "normal"
        font_style = "italic" if italic else "normal"
        text_decoration = "underline" if underline else "none"
        
        html = f"""
        <div style="
            font-family: '{font_family}';
            font-size: {font_size}px;
            color: {color};
            font-weight: {font_weight};
            font-style: {font_style};
            text-decoration: {text_decoration};
            background-color: {background};
            text-align: {align};
            padding: 10px;
            border-radius: 10px;
        ">
            {content}
        </div>
        """
        
        self.text_area.setHtml(html)

    def highlight_search(self, search_text):
        format = QTextCharFormat()
        format.setBackground(QColor("#FFD700"))
        format.setForeground(QColor("#000000"))
        
        document = self.text_area.document()
        first_cursor = document.find(search_text)
        if not first_cursor.isNull():
            cursor = document.find(search_text)
            while not cursor.isNull():
                cursor.mergeCharFormat(format)
                cursor = document.find(search_text, cursor)
            self.text_area.setTextCursor(first_cursor)
            self.text_area.ensureCursorVisible()