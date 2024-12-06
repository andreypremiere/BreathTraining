from typing import Any
import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage

from editing_video.color_tracker import ColorTracker
from editing_video.point_manager import PointManager
from editing_video.video_manager import VideoManager



class VideoProcessingThread(QThread):
    belly_coordinate = pyqtSignal(tuple)
    breast_coordinate = pyqtSignal(tuple)
    frame_ready = pyqtSignal(np.ndarray)
    send_data = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.running = True
        self.stop_flag = False
        self.point_manager = PointManager()
        # self.video_manager = VideoManager(self.point_manager, 'editing_video/val.mp4')
        self.video_manager = VideoManager(self.point_manager)

        # Подключаем сигнал к слоту
        self.belly_coordinate.connect(self.set_belly_coordinate)

    @pyqtSlot(tuple)
    def set_belly_coordinate(self, coordinate):
        """Слот для обработки координат живота"""
        print(f"Получены данные в потоке: {coordinate}")
        self.video_manager.point_manager.points.append(coordinate)

    @pyqtSlot(tuple)
    def set_breast_coordinate(self, coordinate):
        """Слот для обработки координат груди"""
        print(f"Получены данные в потоке: {coordinate}")
        self.video_manager.point_manager.points.append(coordinate)

    def run(self):
        # Этот метод будет выполняться в отдельном потоке
        # while self.running:
            # print('Поток выполняется')
            # print(self.belly_coordinate_data)
            # self.msleep(1000)
        print("Запуск программы...")

        # frame - кадр (массив), success - успешно ли выполнено чтение
        # video_manager.capture - объект класса cv2.VideoCapture, который захватывает видеопоток.
        success, frame = self.video_manager.capture.read()

        k = 0

        while success and not self.stop_flag:
            success, frame = self.video_manager.capture.read()  # получить следующий кадр
            if not success:
                break

            # Обработка выбора точек
            # если в списке точек меньше двух точек
            if len(self.video_manager.point_manager.points) < 2:
                # если точек нет, то переводим point_manager self.selected_mode = "belly"
                if len(self.video_manager.point_manager.points) == 0:
                    self.video_manager.point_manager.point_belly()
                    # print("Выберите точку для живота")
                # если точка есть, то переводим point_manager self.selected_mode = "breast"
                elif len(self.video_manager.point_manager.points) == 1:
                    self.video_manager.point_manager.point_breast()
                    # print("Выберите точку для груди")
            # в противном случае None (после назначения всех точек)
            else:
                self.video_manager.point_manager.selected_mode = None

            # Создаем трекеры для новых точек
            # если точек больше чем 0, и их меньше, чем трекерах
            if len(self.video_manager.point_manager.points) > 0:
                if len(self.video_manager.trackers) < len(self.video_manager.point_manager.points):
                    for (x, y) in self.video_manager.point_manager.points[len(self.video_manager.trackers):]:
                        self.video_manager.trackers.append(ColorTracker(x, y))
                        print(x, y)
                        print('Точка добавлена')

            k += 1

            # if k == 100:
            #     self.video_manager.point_manager.points.append((20, 47))
            #
            # if k == 200:
            #     self.video_manager.point_manager.points.append((50, 87))
            # if len(self.video_manager.trackers) == 2:
            try:
                frame = self.video_manager.process_frame(frame)
                self.video_manager.data = self.video_manager.update_dataframe(self.video_manager.data,
                                                                              self.video_manager.trackers)
            except Exception as e:
                print(e)

            # cv2.namedWindow("My Camera")
            # cv2.imshow("My Camera", frame)
            self.send_frame(frame)

    def send_frame(self, frame):
        # qt_image = None
        # try:
            # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # h, w, ch = rgb_image.shape
            # print(h, w, ch)
            # qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
            # print(qt_image)
        # except Exception as e:
        #     print('Ошибка преобразование кадра в qlabel')

        self.frame_ready.emit(frame)

    def stop(self):
        """Останавливаем поток"""
        self.stop_flag = True

        try:
            # Получаем данные
            data = self.video_manager.get_dataframe()
            print(data)

            # Преобразуем time_st в UNIX timestamp
            # data['time_st'] = data['time_st'].astype('datetime64[ns]').view('int64') // 10 ** 9

            # Сохраняем DataFrame в CSV до преобразования в массив
            data.to_csv("output.csv", index=False)

            # Преобразуем в numpy
            array_data = data.to_numpy()
            self.send_data.emit(array_data)

        except Exception as e:
            print(f"Ошибка во время выполнения программы: {e}")
        finally:
            self.video_manager.end()
            print("Работа программы завершена.")

        self.quit()
        self.wait()
