import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal


class VideoProcessingThread(QThread):
    # Сигнал, который будет передавать текущее значение счетчика
    count_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.counter = 0  # Счетчик

    def run(self):
        # Этот метод будет выполняться в отдельном потоке
        while True:
            # Обновляем счетчик каждую секунду
            self.counter += 1
            self.count_updated.emit(self.counter)  # Отправляем сигнал с новым значением
            self.msleep(1000)  # Задержка в 1 секунду