from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Выпадающее меню")

        # Создаем QComboBox
        self.dropdown = QComboBox()
        self.dropdown.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
            }
        """)
        self.dropdown.addItems(["Не установлен", "Мужской", "Женский"])  # Добавляем элементы в список
        self.dropdown.setPlaceholderText("Выберите вариант")  # Подсказка до выбора

        # Кнопка для получения выбранного значения
        self.button = QPushButton("Получить выбор")
        self.button.clicked.connect(self.get_selection)

        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.dropdown)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_selection(self):
        """
        Получение выбранного значения из выпадающего списка.
        """
        selected_text = self.dropdown.currentText()  # Текст выбранного элемента
        selected_index = self.dropdown.currentIndex()  # Индекс выбранного элемента
        print(f"Вы выбрали: {selected_text} (индекс: {selected_index})")


# Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
