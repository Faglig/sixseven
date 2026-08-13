from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChatbotTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        title = QLabel("🤖 ЧАТ-БОТ")
        title.setObjectName("groupLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(30)
        title.setMinimumWidth(150)
        layout.addWidget(title)
        
        label = QLabel("В разработке")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("groupLabel")
        label.setFixedHeight(40)
        layout.addWidget(label)
        
        layout.addStretch()