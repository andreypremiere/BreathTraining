import sys

import cv2
import pandas as pd
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGraphicsScene, QGraphicsView
from work_window.video_processing_thread import VideoProcessingThread


class WorkWindow(QWidget):
    def __init__(self, jwt_provider):
        super().__init__()
        self.main_layout = None
        self.video_label = None
        self.video_thread = VideoProcessingThread()
        self.label_count = None
        self.jwt_provider = jwt_provider
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Процедура')
        self.setGeometry(0, 0, 1400, 900)

        # Главный макет
        self.main_layout = QVBoxLayout()

        # Макет для информации о пациенте
        patient_layout = QVBoxLayout()
        name_patient = QLabel('Иванов Иван Иванович')
        birthday_patient = QLabel('22.08.2002')
        patient_layout.addWidget(name_patient)
        patient_layout.addWidget(birthday_patient)

        button_close = QPushButton("Закрыть окно")
        button_close.clicked.connect(lambda x: print('hello'))
        patient_layout.addWidget(button_close)

        self.main_layout.addLayout(patient_layout)

        # Макет для проведения сессии
        submain_layout = QHBoxLayout()
        graph_and_video_layout = QVBoxLayout()

        # лейбел для видео
        self.video_label = QLabel(self)
        self.video_label.setMaximumWidth(480)
        self.video_label.adjustSize()

        graph_and_video_layout.addWidget(self.video_label)
        submain_layout.addLayout(graph_and_video_layout)

        self.main_layout.addLayout(submain_layout)

        # # Метка для отображения счетчика
        # self.label_count = QLabel("Счетчик: 0")
        # graph_and_video_layout.addWidget(self.label_count)
        #
        # submain_layout.addLayout(graph_and_video_layout)
        # main_layout.addLayout(submain_layout)

        self.setLayout(self.main_layout)
        self.video_thread.start()

        self.video_thread.frame_ready.connect(self.update_frame)
        self.video_thread.send_data.connect(self.get_data)

        # Запускаем поток
        # self.video_thread.start()

    def get_data(self, data):
        # columns = ['time_st', 'mark_belly', 'mark_breast']  # Имена столбцов
        #
        # df = pd.DataFrame(data, columns=columns)
        # df['time_st'] = pd.to_datetime(df['time_st'], unit='s')

        print('Датафрейм принят')
        print(data)

    def update_frame(self, frame):
        """Обновляем QLabel новым кадром"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        # print(h, w, ch)
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
        # print(qt_image)
        pixmap = QPixmap(qt_image)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

        self.image_width = w
        self.image_height = h

    def send_data_to_thread(self, coordinate):
        """Передает данные в поток"""
        self.video_thread.belly_coordinate.emit(coordinate)

    def closeEvent(self, event):
        # Закрытие видеопотока при закрытии окна
        self.video_thread.stop()
        event.accept()

    def mousePressEvent(self, event):
        """Обрабатываем клик мыши только на области с видео и выводим координаты в консоль"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Получаем позицию клика относительно всего окна
            global_pos = event.globalPosition().toPoint()  # Позиция клика в глобальных координатах
            local_pos = self.video_label.mapFromGlobal(global_pos)  # Преобразуем к локальным координатам QLabel

            # Проверяем, находится ли клик в границах QLabel
            if 0 <= local_pos.x() <= self.video_label.width() and 0 <= local_pos.y() <= self.video_label.height():
                # Получаем масштабирование изображения относительно QLabel
                scale_x = self.video_label.width() / self.image_width
                scale_y = self.video_label.height() / self.image_height

                # Преобразуем координаты клика в координаты изображения
                image_x = int(local_pos.x() / scale_x)
                image_y = int(local_pos.y() / scale_y)

                self.send_data_to_thread((image_x, image_y))

                print(f"Координаты на изображении: x={image_x}, y={image_y}")
            else:
                print("Клик вне области видео")

    # def start_count(self):
    #     # Создаем поток и запускаем его
    #     self.video_thread = VideoProcessingThread()
    #     self.video_thread.count_updated.connect(self.update_counter)  # Подключаем сигнал
    #     self.video_thread.start()


    # def update_counter(self, count):
    #     """Обновляем метку с новым значением счетчика"""
    #     self.label_count.setText(f"Счетчик: {count}")
    #
    # def closeEvent(self, event):
    #     """Останавливаем поток при закрытии окна"""
    #     self.video_thread.terminate()
    #     self.video_thread.wait()
    #     event.accept()





