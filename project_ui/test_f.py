import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, \
    QGraphicsDropShadowEffect, QSizePolicy


class SearchPatient(QWidget):
    def __init__(self, switch_window_callback=None):
        super().__init__()

        self.button1 = None
        self.left_panel_layout = None
        self.switch_window = switch_window_callback
        self.input_lastname_patient = None
        self.button_search_patient = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""background-color: #E5FBFF;""")
        self.setWindowTitle('Поиск клиента')
        self.setGeometry(50, 30, 1400, 780)

        # Главный горизонтальный макет
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        outer_frame = QWidget()
        outer_layout = QVBoxLayout()

        # Внутренний фрейм, растягивающийся по возможной высоте
        inner_frame = QWidget()
        inner_layout = QVBoxLayout()
        label = QLabel("Это внутренний фрейм, растягивающийся по высоте")
        button = QPushButton("Нажми меня")
        inner_layout.addWidget(label)
        inner_layout.addWidget(button)
        inner_frame.setLayout(inner_layout)

        outer_layout.addWidget(inner_frame)
        outer_frame.setLayout(outer_layout)

        main_layout.addWidget(outer_frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SearchPatient()
    ventana.show()
    sys.exit(app.exec())
