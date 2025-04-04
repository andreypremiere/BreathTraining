from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpinBox, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt

from error_service.finish_procedure import DialogProcedure


def show_info_message(text):
    # Создание и настройка информационного окна
    message_box = QMessageBox()
    message_box.setWindowTitle("Информация")
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    # Показ окна
    message_box.exec()


class CountdownTimer(QFrame):
    def __init__(self, parent=None, video_manager=None,
                 start_callback=None, stop_callback=None):
        self.parent_wid = parent
        self.video_manager = video_manager
        self.start_callback = start_callback
        self.stop_callback = stop_callback

        super().__init__(parent)

        # self.setStyleSheet("background-color: none; border-radius: 8px;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.layout = QVBoxLayout(self)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        # Создание интерфейса таймера
        self.timer_frame = QFrame(self)
        self.timer_layout = QHBoxLayout(self.timer_frame)
        self.timer_layout.setSpacing(4)
        self.timer_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.timer_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.timer_layout.setContentsMargins(4, 4, 4, 4)
        self.timer_frame.setStyleSheet("background-color: #FFFFFF;"
                                       "border-radius: 6px;")
        self.timer_frame.setGraphicsEffect(self.frame_shadow(self.timer_frame, opacity=32))

        self.hours_spinbox = QSpinBox(self.timer_frame)
        self.hours_spinbox.setRange(0, 23)
        self.hours_spinbox.setSuffix(" ч.")
        self.hours_spinbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.hours_spinbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.hours_spinbox.setFont(QFont('Arial', 14, 500))
        # self.hours_spinbox.setContentsMargins(0, 0, 0, 0)
        self.hours_spinbox.setStyleSheet("""
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }
        """)

        self.minutes_spinbox = QSpinBox(self.timer_frame)
        self.minutes_spinbox.setRange(0, 59)
        self.minutes_spinbox.setSuffix(" м")
        self.minutes_spinbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.minutes_spinbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.minutes_spinbox.setFont(QFont('Arial', 14, 500))
        self.minutes_spinbox.setStyleSheet("""
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }
        """)

        self.seconds_spinbox = QSpinBox(self.timer_frame)
        self.seconds_spinbox.setRange(0, 59)
        self.seconds_spinbox.setSuffix(" с")
        self.seconds_spinbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.seconds_spinbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.seconds_spinbox.setFont(QFont('Arial', 14, 500))
        self.seconds_spinbox.setStyleSheet("""
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }
        """)

        self.timer_layout.addWidget(self.hours_spinbox)
        self.timer_layout.addWidget(self.minutes_spinbox)
        self.timer_layout.addWidget(self.seconds_spinbox)
        self.layout.addWidget(self.timer_frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Таймерное отображение
        self.time_label = QLabel("00:00:00", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont('Arial', 20, weight=600))
        self.layout.addWidget(self.time_label)

        # Кнопки управления
        self.buttons_layout = QHBoxLayout()
        self.start_button = self.generate_button_timer("Старт", self)
        self.pause_button = self.generate_button_timer("Пауза", self)
        self.reset_button = self.generate_button_timer("Завершить", self)

        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.pause_button)
        self.buttons_layout.addWidget(self.reset_button)
        self.layout.addLayout(self.buttons_layout)

        # Настройка логики
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.remaining_time = 0  # Секунды оставшегося времени

        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)

    def start_timer(self):
        if self.remaining_time == 0:  # Если время не установлено, берём из спинбоксов
            self.remaining_time = (
                    self.hours_spinbox.value() * 3600
                    + self.minutes_spinbox.value() * 60
                    + self.seconds_spinbox.value()
            )

        belly = self.video_manager.points.get("belly")
        breast = self.video_manager.points.get("breast")

        if self.remaining_time > 0 and belly and breast:  # Запускаем только если есть время
            self.video_manager.recording = True
            self.timer.start(1000)
            self.start_callback()
        else:
            show_info_message('Не установлена одна или несколько меток.')

    def pause_timer(self):
        self.timer.stop()
        self.video_manager.recording = False
        self.stop_callback()

    def reset_timer(self):
        self.timer.stop()
        self.video_manager.recording = False
        self.stop_callback()
        message_error = DialogProcedure(1, save_procedure_callback=self.parent_wid.save_procedure_data,
                                        open_choose_marks_window=self.parent_wid.choose_marks_button,
                                        reset_marks_callback=self.parent_wid.reset_marks,
                                        reset_timer_callback=self.clean_timer,
                                        reset_data_callback=self.video_manager.reset_data)
        message_error.exec()
        self.clean_timer()

    def clean_timer(self):
        self.remaining_time = 0
        self.update_time_label()
        self.hours_spinbox.setValue(0)
        self.minutes_spinbox.setValue(0)
        self.seconds_spinbox.setValue(0)

    def update_timer(self):
        belly = self.video_manager.points.get("belly")
        breast = self.video_manager.points.get("breast")

        if not belly or not breast:
            self.pause_timer()
            # self.video_manager.recording = False
            message_error = DialogProcedure(2, save_procedure_callback=self.parent_wid.save_procedure_data,
                                            open_choose_marks_window=self.parent_wid.choose_marks_button,
                                            reset_marks_callback=self.parent_wid.reset_marks,
                                            reset_timer_callback=self.clean_timer,
                                            reset_data_callback=self.video_manager.reset_data
                                            )
            message_error.exec()
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_time_label()
        else:
            self.timer.stop()
            self.video_manager.recording = False
            self.stop_callback()
            message_error = DialogProcedure(1, save_procedure_callback=self.parent_wid.save_procedure_data,
                                            open_choose_marks_window=self.parent_wid.choose_marks_button,
                                            reset_marks_callback=self.parent_wid.reset_marks,
                                            reset_timer_callback=self.clean_timer,
                                            reset_data_callback=self.video_manager.reset_data)
            message_error.exec()

    def update_time_label(self):
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def frame_shadow(self, parent, radius=20, opacity=64):
        shadow = QGraphicsDropShadowEffect(parent=parent)
        shadow.setBlurRadius(radius)  # Радиус размытия тени
        shadow.setColor(QColor(0, 0, 0, opacity))  # Чёрная тень с прозрачностью
        shadow.setOffset(0, 0)
        return shadow

    def generate_button_timer(self, text, parent):
        button = QPushButton(text, parent=parent)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        button.setFont(QFont('Arial', 10, 500))
        button.setStyleSheet("""
            QPushButton {
                background-color: #ADE8F4;
                border-radius: 4px;
                padding: 4px 10px;
            }
            
            QPushButton:pressed {
                        background-color: #009AB9;
            }
        """)
        return button
