import sys

from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpinBox, QSizePolicy, QGraphicsDropShadowEffect,
    QApplication, QMainWindow
)
from PyQt6.QtCore import QTimer, Qt, QSize


class PanelChoosingMarks(QFrame):
    def __init__(self, parent=None, video_manager=None,
                 callback_button_back=None):
        self.video_manager = video_manager
        self.callback_button_back = callback_button_back

        super().__init__(parent)

        self.setFixedWidth(640)
        self.setStyleSheet("""
            background-color: #F0FDFF;
            border-radius: 14px;
        """)
        self.setContentsMargins(14, 4, 14, 4)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(12)
        shadow = QGraphicsDropShadowEffect(parent=parent)
        shadow.setBlurRadius(20)  # Радиус размытия тени
        shadow.setColor(QColor(0, 0, 0, 64))  # Чёрная тень с прозрачностью
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)


        # Заголовки
        self.titles_layout = QVBoxLayout(self)
        self.titles_layout.setSpacing(0)
        # self.titles_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.operation_label = QLabel('', self)
        self.set_breast_mode()
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

        self.left_dict_part = self.generate_panel_part('Координата живота: ', 'Сбросить координату')
        self.right_dict_part = self.generate_panel_part('Координата груди: ', 'Сбросить координату')
        self.left_dict_part.get('button').clicked.connect(self.reset_mark_belly)
        self.right_dict_part.get('button').clicked.connect(self.reset_mark_breast)

        # self.change_button = QPushButton(self)
        # self.change_button.setFixedSize(32, 32)
        # self.change_button.setIcon(QIcon("../icons/transfer-data.png"))  # Устанавливаем картинку
        # self.change_button.setIconSize(QSize(24, 24))
        # self.change_button.setText("")
        # self.change_button.setStyleSheet("""
        #             QPushButton {
        #                 background-color: #ADE8F4;
        #                 border-style: none;
        #                 border-radius: 4px;  /* Круглая кнопка */
        #                 padding: 4px;
        #             }
        #             QPushButton:pressed {
        #                 background-color: #009AB9;
        #             }
        #         """)
        # self.change_button.clicked.connect(self.change_mark)

        self.panel_managing.addLayout(self.left_dict_part['layout'])
        # self.panel_managing.addWidget(self.change_button)
        self.panel_managing.addLayout(self.right_dict_part['layout'])

        # Кнопки сохранить и назад
        self.panel_buttons = QHBoxLayout(self)
        self.panel_buttons.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.button_save = QPushButton('Готово', self)
        self.button_save.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.button_save.setStyleSheet("""
                    QPushButton {
                        background-color: #ADE8F4;
                        border-style: none;
                        border-radius: 6px;  /* Круглая кнопка */
                        padding: 4px 10px;
                        font-size: 14px;
                    }
                    QPushButton:pressed {
                        background-color: #009AB9;
                    }
                """)
        self.button_save.clicked.connect(self.callback_button_back)

        # self.button_back = QPushButton('Назад', self)
        # self.button_back.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # self.button_back.setStyleSheet("""
        #                     QPushButton {
        #                         background-color: #ADE8F4;
        #                         border-style: none;
        #                         border-radius: 6px;  /* Круглая кнопка */
        #                         padding: 4px 10px;
        #                         font-size: 14px;
        #                     }
        #                     QPushButton:pressed {
        #                         background-color: #009AB9;
        #                     }
        #                 """)
        # self.button_back.clicked.connect(self.back_and_reset_marks)
        # self.panel_buttons.addWidget(self.button_back)
        self.panel_buttons.addWidget(self.button_save)


        # Добавление всех лэйаутов
        self.main_layout.addLayout(self.titles_layout)
        self.main_layout.addLayout(self.panel_managing)
        self.main_layout.addLayout(self.panel_buttons)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500)  # Обновление каждую секунду

        self.setLayout(self.main_layout)

    def update_labels(self):
        belly = self.video_manager.points.get("belly")
        breast = self.video_manager.points.get("breast")

        if self.left_dict_part.get('coordinate'):
            self.left_dict_part['coordinate'].setText(
                str(belly[1]) if isinstance(belly, (list, tuple)) else 'Не установлена')

        if self.right_dict_part.get('coordinate'):
            self.right_dict_part['coordinate'].setText(
                str(breast[1]) if isinstance(breast, (list, tuple)) else 'Не установлена')

        current_mode = self.video_manager.point_manager.selected_mode

        if not breast:
            self.set_breast_mode()
        elif not belly:
            self.set_belly_mode()
        elif belly and breast:
            self.operation_label.setText("Метки установлены")
            self.video_manager.point_manager.selected_mode = None

    def generate_panel_part(self, text_title, text_button):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        coordinates_layout = QHBoxLayout(self)
        coordinates_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        coordinates_layout.setSpacing(0)

        label = QLabel(text_title, self)
        label.setFont(QFont('Arial', 10, 400))

        coordinate = QLabel('Не установлена', self)
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

        return {
            'layout': layout,
            'coordinate': coordinate,
            'button': button
        }

    def change_mark(self):
        current_mode = self.video_manager.point_manager.selected_mode

        if (not self.video_manager.points.get("breast") and current_mode != "breast") or not self.video_manager.points.get("breast"):
            self.set_breast_mode()

        elif (not self.video_manager.points.get("belly") and current_mode != "belly") or not self.video_manager.points.get("belly"):
            self.set_belly_mode()

        else:
            self.operation_label.setText("Метки установлены")
            self.video_manager.point_manager.selected_mode = None

    def set_breast_mode(self):
        self.operation_label.setText('Выберите метку груди')
        self.video_manager.point_manager.selected_mode = 'breast'


    def set_belly_mode(self):
        self.operation_label.setText('Выберите метку живота')
        self.video_manager.point_manager.selected_mode = 'belly'

    def reset_mark_belly(self):
        self.video_manager.points['belly'] = None
        self.video_manager.trackers['belly'] = None

    def reset_mark_breast(self):
        self.video_manager.points['breast'] = None
        self.video_manager.trackers['breast'] = None
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