import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGraphicsScene, QGraphicsView
from work_window.video_processing_thread import VideoProcessingThread


class WorkWindow(QWidget):
    def __init__(self, jwt_provider):
        super().__init__()
        self.video_thread = None
        self.label_count = None
        self.jwt_provider = jwt_provider
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Процедура')
        self.setGeometry(0, 0, 1400, 900)

        # Главный макет
        main_layout = QVBoxLayout()

        # Макет для информации о пациенте
        patient_layout = QVBoxLayout()
        name_patient = QLabel('Иванов Иван Иванович')
        birthday_patient = QLabel('22.08.2002')
        patient_layout.addWidget(name_patient)
        patient_layout.addWidget(birthday_patient)

        main_layout.addLayout(patient_layout)

        # Макет для проведения сессии
        submain_layout = QHBoxLayout()
        graph_and_video_layout = QVBoxLayout()

        # Метка для отображения счетчика
        self.label_count = QLabel("Счетчик: 0")
        graph_and_video_layout.addWidget(self.label_count)

        submain_layout.addLayout(graph_and_video_layout)
        main_layout.addLayout(submain_layout)

        self.setLayout(main_layout)

        self.start_count()

    def start_count(self):
        # Создаем поток и запускаем его
        self.video_thread = VideoProcessingThread()
        self.video_thread.count_updated.connect(self.update_counter)  # Подключаем сигнал
        self.video_thread.start()


    def update_counter(self, count):
        """Обновляем метку с новым значением счетчика"""
        self.label_count.setText(f"Счетчик: {count}")

    def closeEvent(self, event):
        """Останавливаем поток при закрытии окна"""
        self.video_thread.terminate()
        self.video_thread.wait()
        event.accept()





