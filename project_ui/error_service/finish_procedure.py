from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QWidget, QFrame, QSizePolicy, \
    QTextEdit


class DialogProcedure(QDialog):
    def __init__(self, option, save_procedure_callback=None,
                 reset_marks_callback=None, open_choose_marks_window=None,
                 video_manager=None, reset_timer_callback=None,
                 reset_data_callback=None):
        super().__init__()
        self.save_procedure_callback = save_procedure_callback
        self.video_manager = video_manager
        self.open_choose_marks_window = open_choose_marks_window
        self.reset_marks_callback = reset_marks_callback
        self.reset_timer_callback = reset_timer_callback
        self.reset_data = reset_data_callback

        self.setWindowTitle("Информационное окно")
        self.setFixedSize(400, 300)
        self.main_frame = QFrame(self)
        self.layout = QVBoxLayout(self.main_frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.main_frame.setLayout(self.layout)
        self.main_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_frame,
                                   alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setStyleSheet("""
            background-color: #F0FDFF;
        """)
        self.main_frame.setStyleSheet("""
            background-color: none;
        """)

        label = QLabel(self.main_frame)
        label.setFont(QFont("Arial", 12, 600))
        label.setMinimumWidth(300)

        self.layout.addWidget(label)
        self.layout.addSpacing(20)

        if option == 1:
            label.setText('Процедура успешно завершена')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Устанавливаем выравнивание по центру

            button_save = QPushButton('Сохранить процедуру',
                                      self.main_frame)
            button_save.setStyleSheet("""
                        QPushButton {
                            background-color: #ADE8F4;
                            border-style: none;
                            border-radius: 6px;  /* Круглая кнопка */
                            padding: 8px 16px;
                        }
                        QPushButton:pressed {
                            background-color: #009AB9;
                        }
                    """)
            button_save.setFont(QFont("Arial", 12, 600))
            button_save.setCursor(Qt.CursorShape.PointingHandCursor)  # Устанавливаем курсор "указатель"
            button_save.clicked.connect(self.save_procedure)

            button_not_save = QPushButton('Не сохранять процедуру',
                                          self.main_frame)
            button_not_save.setStyleSheet("""
                        QPushButton {
                            background-color: #E0FBFF;
                            border-style: none;
                            border-radius: 6px;  /* Круглая кнопка */
                            padding: 4px 10px;
                        }
                        QPushButton:pressed {
                            background-color: #009AB9;
                        }
                    """)
            button_not_save.setCursor(Qt.CursorShape.PointingHandCursor)  # Устанавливаем курсор "указатель"
            button_not_save.clicked.connect(self.dont_save_and_reset)

            self.layout.addWidget(button_save,
                                  alignment=Qt.AlignmentFlag.AlignHCenter)
            self.layout.addWidget(button_not_save,
                                  alignment=Qt.AlignmentFlag.AlignHCenter)

        elif option == 2:
            label.setWordWrap(True)
            label.setText('Процедура прервана. Пожалуйста, выберите дальнейшее действие')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Устанавливаем выравнивание по центру

            style = """
                    QPushButton {
                        background-color: #E0FBFF;
                        border-style: none;
                        border-radius: 6px;  /* Круглая кнопка */
                        padding: 4px 10px;
                    }
                    QPushButton:pressed {
                        background-color: #009AB9;
                    }
                    """

            button_choose_and_continue = QPushButton('Выбрать метки и продолжить',
                                                     self.main_frame)
            button_choose_and_continue.setStyleSheet(style)
            button_choose_and_continue.setCursor(Qt.CursorShape.PointingHandCursor)
            button_choose_and_continue.setFont(QFont('Arial', 11, 400))
            button_choose_and_continue.clicked.connect(self.choose_and_continue)

            button_save = QPushButton('Сохранить и сбросить',
                                                   self.main_frame)
            button_save.setStyleSheet(style)
            button_save.setCursor(Qt.CursorShape.PointingHandCursor)
            button_save.setFont(QFont('Arial', 11, 400))
            button_save.clicked.connect(self.save_procedure)
            button_save.clicked.connect(self.dont_save_and_reset)

            button_not_save = QPushButton('Не сохранять и сбросить',
                                                   self.main_frame)
            button_not_save.setStyleSheet(style)
            button_not_save.setCursor(Qt.CursorShape.PointingHandCursor)
            button_not_save.setFont(QFont('Arial', 11, 400))
            button_not_save.clicked.connect(self.dont_save_and_reset)


            self.layout.addWidget(button_choose_and_continue,
                                  alignment=Qt.AlignmentFlag.AlignHCenter)
            self.layout.addWidget(button_save,
                                  alignment=Qt.AlignmentFlag.AlignHCenter)
            self.layout.addWidget(button_not_save,
                                  alignment=Qt.AlignmentFlag.AlignHCenter)

    def choose_and_continue(self):
        self.open_choose_marks_window()
        self.close()

    def dont_save_and_reset(self):
        self.reset_marks_callback()
        self.reset_timer_callback()
        self.reset_data()
        self.close()

    def save_procedure(self):
        self.save_procedure_callback()
        self.close()


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Основное окно")
        self.setGeometry(100, 100, 400, 300)

        # layout = QVBoxLayout(self)
        # self.setLayout(layout)
        self.show_dialog()

    def show_dialog(self):
        dialog = DialogProcedure()
        dialog.exec()


if __name__ == "__main__":
    app = QApplication([])
    # window = MyWindow()
    # window.show()
    dialog = DialogProcedure(1)
    dialog.show()
    app.exec()
