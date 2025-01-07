from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Абсолютное позиционирование кнопки")
        self.setGeometry(100, 100, 400, 300)

        # Кнопка внутри слоя
        self.button = QPushButton("Нажми меня", self)
        self.button.setGeometry(50, 50, 100, 30)  # Устанавливаем позицию (x, y) и размер (width, height)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
