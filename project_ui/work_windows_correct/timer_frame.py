from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpinBox, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import QTimer, Qt


class CountdownTimer(QFrame):
    def __init__(self, parent=None):
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
        if self.remaining_time > 0:  # Запускаем только если есть время
            self.timer.start(1000)

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.remaining_time = 0
        self.update_time_label()
        self.hours_spinbox.setValue(0)
        self.minutes_spinbox.setValue(0)
        self.seconds_spinbox.setValue(0)

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_time_label()
        else:
            self.timer.stop()

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