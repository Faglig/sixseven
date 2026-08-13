from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QComboBox, QSpinBox,
    QPushButton, QInputDialog, QLabel, QListWidget, QSplitter, QTextEdit, QMessageBox
)
from color_dialog import ColorPickerDialog


class NotesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = {}  # {название: текст}
        self.current_note = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        title = QLabel("📝 ЗАМЕТКИ")
        title.setObjectName("groupLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(28)
        title.setFixedWidth(120)
        layout.addWidget(title)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(4)
        
        self.notes_list = QListWidget()
        self.notes_list.setFixedWidth(150)
        self.notes_list.itemClicked.connect(self.load_note)
        top_layout.addWidget(self.notes_list)
        
        self.new_note_btn = QPushButton("+ Новая")
        self.new_note_btn.setObjectName("formatButton")
        self.new_note_btn.clicked.connect(self.create_note)
        top_layout.addWidget(self.new_note_btn)
        
        self.delete_note_btn = QPushButton("🗑")
        self.delete_note_btn.setObjectName("formatButton")
        self.delete_note_btn.clicked.connect(self.delete_note)
        top_layout.addWidget(self.delete_note_btn)
        
        self.rename_note_btn = QPushButton("✏️")
        self.rename_note_btn.setObjectName("formatButton")
        self.rename_note_btn.clicked.connect(self.rename_note)
        top_layout.addWidget(self.rename_note_btn)
        
        top_layout.addStretch()
        layout.addLayout(top_layout)

        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(4)
        layout.addWidget(toolbar_widget)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Verdana"])
        self.font_combo.currentTextChanged.connect(self.change_font)
        toolbar_layout.addWidget(self.font_combo)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(12)
        self.size_spin.valueChanged.connect(self.change_font_size)
        toolbar_layout.addWidget(self.size_spin)

        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.clicked.connect(self.toggle_bold)
        self.bold_btn.setObjectName("formatButton")
        toolbar_layout.addWidget(self.bold_btn)

        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.clicked.connect(self.toggle_italic)
        self.italic_btn.setObjectName("formatButton")
        toolbar_layout.addWidget(self.italic_btn)

        self.underline_btn = QPushButton("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.clicked.connect(self.toggle_underline)
        self.underline_btn.setObjectName("formatButton")
        toolbar_layout.addWidget(self.underline_btn)

        self.color_btn = QPushButton("🎨")
        self.color_btn.clicked.connect(self.choose_color)
        self.color_btn.setObjectName("formatButton")
        toolbar_layout.addWidget(self.color_btn)

        self.link_btn = QPushButton("🔗")
        self.link_btn.clicked.connect(self.insert_link)
        self.link_btn.setObjectName("formatButton")
        toolbar_layout.addWidget(self.link_btn)

        toolbar_layout.addStretch()
        layout.addLayout(barrel_layout if False else QHBoxLayout())  # placeholder

        self.text_edit = QTextBrowser()
        self.text_edit.setReadOnly(False)
        self.text_edit.setOpenExternalLinks(True)
        self.text_edit.textChanged.connect(self.save_current_note)
        layout.addWidget(self.text_edit, 1)

    def create_note(self):
        name, ok = QInputDialog.getText(self, "Новая заметка", "Название:")
        if ok and name:
            if name not in self.notes:
                self.notes[name] = ""
                self.notes_list.addItem(name)
                self.notes_list.setCurrentRow(self.notes_list.count() - 1)
                self.current_note = name
                self.text_edit.clear()
            else:
                QMessageBox.warning(self, "Ошибка", "Заметка с таким названием уже существует")

    def delete_note(self):
        if self.current_note:
            confirm = QMessageBox.question(self, "Удаление", f"Удалить заметку '{self.current_note}'?")
            if confirm == QMessageBox.Yes:
                del self.notes[self.current_note]
                row = self.notes_list.currentRow()
                self.notes_list.takeItem(row)
                self.current_note = None
                self.text_edit.clear()

    def rename_note(self):
        if self.current_note:
            new_name, ok = QInputDialog.getText(self, "Переименовать", "Новое название:", text=self.current_note)
            if ok and new_name and new_name != self.current_note:
                if new_name not in self.notes:
                    self.notes[new_name] = self.notes.pop(self.current_note)
                    self.current_note = new_name
                    self.notes_list.currentItem().setText(new_name)
                else:
                    QMessageBox.warning(self, "Ошибка", "Заметка с таким названием уже существует")

    def load_note(self, item):
        self.current_note = item.text()
        self.text_edit.setHtml(self.notes.get(self.current_note, ""))

    def save_current_note(self):
        if self.current_note and self.current_note in self.notes:
            self.notes[self.current_note] = self.text_edit.toHtml()

    def change_font(self, font_family):
        current_font = self.text_edit.currentFont()
        current_font.setFamily(font_family)
        self.text_edit.setCurrentFont(current_font)

    def change_font_size(self, size):
        current_font = self.text_edit.currentFont()
        current_font.setPointSize(size)
        self.text_edit.setCurrentFont(current_font)

    def toggle_bold(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontWeight(QFont.Bold if self.bold_btn.isChecked() else QFont.Normal)
        self.text_edit.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self.text_edit.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self.text_edit.mergeCurrentCharFormat(fmt)

    def choose_color(self):
        dialog = ColorPickerDialog(self, "#FFFFFF", "Выбор цвета")
        if dialog.exec_() == ColorPickerDialog.Accepted:
            color = dialog.get_color()
            fmt = self.text_edit.currentCharFormat()
            fmt.setForeground(color)
            self.text_edit.mergeCurrentCharFormat(fmt)

    def insert_link(self):
        url, ok = QInputDialog.getText(self, "Вставить ссылку", "URL:")
        if ok and url:
            cursor = self.text_edit.textCursor()
            if cursor.hasSelection():
                selected_text = cursor.selectedText()
                cursor.insertHtml(f'<a href="{url}">{selected_text}</a>')
            else:
                cursor.insertHtml(f'<a href="{url}">{url}</a>')
            self.text_edit.setTextCursor(cursor)