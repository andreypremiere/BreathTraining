from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QGroupBox, QLineEdit, QGridLayout
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Медицинская карта")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #e0f7fa;")  # Установка цвета фона

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Верхний блок с информацией
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        patient_info = QGroupBox("Информация о пациенте")
        patient_info_layout = QVBoxLayout()
        patient_info.setLayout(patient_info_layout)
        top_layout.addWidget(patient_info)

        name_label = QLabel("Иванов Иван Иванович")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        patient_info_layout.addWidget(name_label)

        dob_label = QLabel("Дата рождения: 12.09.2000    Возраст: 23")
        patient_info_layout.addWidget(dob_label)

        diagnosis_label = QLabel("Диагноз: Очень длинное описание диагноза, "
                                 "которое бывает очень длинным предлинным, что может не помещаться в многие блоки.")
        diagnosis_label.setWordWrap(True)
        patient_info_layout.addWidget(diagnosis_label)

        edit_button = QPushButton("✏️")
        edit_button.setFixedSize(40, 30)
        patient_info_layout.addWidget(edit_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка "Начать процедуру"
        start_button = QPushButton("Начать процедуру")
        start_button.setStyleSheet("font-size: 16px; background-color: #00bcd4; color: white; padding: 10px;")
        start_button.setFixedHeight(50)
        main_layout.addWidget(start_button)

        # Средний блок
        middle_layout = QHBoxLayout()
        main_layout.addLayout(middle_layout)

        # История процедур
        history_box = QGroupBox("История процедур")
        history_layout = QVBoxLayout()
        history_box.setLayout(history_layout)
        middle_layout.addWidget(history_box)

        history_list = QListWidget()
        for i in range(8, 0, -1):
            history_list.addItem(f"{i}. Дата: 29.09.2000\n   Продолжительность: 29.09.2000")
        history_layout.addWidget(history_list)

        # Статистика
        stats_box = QGroupBox("Статистика")
        stats_layout = QVBoxLayout()
        stats_box.setLayout(stats_layout)
        middle_layout.addWidget(stats_box)

        stats_labels = [
            "Разные данные: да",
            "Еще не придумал что: да",
            "Потом заполню: да"
        ]
        for stat in stats_labels:
            stats_layout.addWidget(QLabel(stat))

        # Электронная карта
        card_box = QGroupBox("Электронная карта")
        card_layout = QHBoxLayout()
        card_box.setLayout(card_layout)
        middle_layout.addWidget(card_box)

        download_button = QPushButton("Скачать")
        upload_button = QPushButton("Загрузить")
        card_layout.addWidget(download_button)
        card_layout.addWidget(upload_button)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
