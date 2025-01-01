import sys

from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpinBox, QSizePolicy, QGraphicsDropShadowEffect,
    QApplication, QMainWindow
)
from PyQt6.QtCore import QTimer, Qt, QSize


class PanelChoosingMarks(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMaximumWidth(900)
        self.setStyleSheet("""
            background-color: #F0FDFF;
            border-radius: 14px;
        """)
        self.setContentsMargins(14, 4, 14, 4)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)


        # Заголовки
        self.titles_layout = QVBoxLayout(self)
        self.titles_layout.setSpacing(0)
        # self.titles_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.operation_label = QLabel('Выберите метку живота', self)
        self.operation_label.setFont(QFont('Arial', 14, 500))
        self.error_label = QLabel('Ошибка', self)
        self.error_label.setFont(QFont('Arial', 8, 400))
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        self.titles_layout.addWidget(self.operation_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.titles_layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Горизонтальный layout. Панель кнопок и координат. Смена координат.
        self.panel_managing = QHBoxLayout(self)
        self.panel_managing.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.left_layout_part = self.generate_panel_part('Координата живота: ', 'Сбросить координату')
        self.right_layout_part = self.generate_panel_part('Координата груди: ', 'Сбросить координату')

        self.change_button = QPushButton(self)
        self.change_button.setFixedSize(32, 32)
        self.change_button.setIcon(QIcon("../icons/transfer-data.png"))  # Устанавливаем картинку
        self.change_button.setIconSize(QSize(24, 24))
        self.change_button.setText("")
        self.change_button.setStyleSheet("""
                    QPushButton {
                        background-color: #ADE8F4;
                        border-style: none;
                        border-radius: 4px;  /* Круглая кнопка */
                        padding: 4px;
                    }
                    QPushButton:pressed {
                        background-color: #009AB9;
                    }
                """)
        self.change_button.clicked.connect(self.change_mark)

        self.panel_managing.addLayout(self.left_layout_part)
        self.panel_managing.addWidget(self.change_button)
        self.panel_managing.addLayout(self.right_layout_part)


        # Добавление всех лэйаутов
        self.main_layout.addLayout(self.titles_layout)
        self.main_layout.addLayout(self.panel_managing)
        self.setLayout(self.main_layout)



    def generate_panel_part(self, text_title, text_button):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        coordinates_layout = QHBoxLayout(self)
        coordinates_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        coordinates_layout.setSpacing(0)

        label = QLabel(text_title, self)
        label.setFont(QFont('Arial', 10, 400))

        coordinate = QLabel('892898', self)
        coordinate.setFont(QFont('Arial', 10, 400))

        coordinates_layout.addWidget(label)
        coordinates_layout.addWidget(coordinate)

        button = QPushButton(text_button, self)
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        button.setStyleSheet("""
            QPushButton {
                background-color: #ADE8F4;
                border-style: none;
                border-radius: 6px;  /* Круглая кнопка */
                padding: 4px 10px;
            }
            QPushButton:pressed {
                background-color: #009AB9;
            }
        """)

        layout.addLayout(coordinates_layout)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)

        return layout

    def change_mark(self):
        if self.operation_label.text() == 'Выберите метку живота':
            self.operation_label.setText('Выберите метку груди')
        else:
            self.operation_label.setText('Выберите метку живота')


# def main():
#     app = QApplication(sys.argv)
#
#     # Создаем главное окно для тестирования
#     window = QMainWindow()
#     window.setWindowTitle("Тестирование фрейма")
#     window.setGeometry(100, 100, 900, 400)
#
#     # Создаем центральный виджет
#     central_widget = QFrame()
#     central_layout = QVBoxLayout(central_widget)
#
#     # Создаем экземпляр тестируемого фрейма
#     test_frame = PanelChoosingMarks()
#     central_layout.addWidget(test_frame, alignment=Qt.AlignmentFlag.AlignTop)
#
#     # Устанавливаем центральный виджет в главное окно
#     window.setCentralWidget(central_widget)
#     window.show()
#
#     sys.exit(app.exec())
#
#
# if __name__ == "__main__":
#     main()