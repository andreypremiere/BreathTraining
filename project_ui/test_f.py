from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Абсолютное позиционирование кнопки")
        self.setGeometry(100, 100, 400, 300)

        # Кнопка внутри слоя
        self.button_back = QPushButton("Назад", self)
        self.button_back.setFont(QFont("Arial", 14, 400))
        self.button_back.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border-radius: 8px;
                padding: 6px 10px;
            }
            QPushButton:pressed {
                background-color: #ADE8F4;
            }
        """)
        self.button_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_back.adjustSize()
        self.button_back.move(20, 20)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
