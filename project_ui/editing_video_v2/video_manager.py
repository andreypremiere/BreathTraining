from datetime import datetime
import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from color_tracker import ColorTracker
from point_manager import PointManager


class VideoManager:
    """Управление видеопотоком и обработка кадров."""

    def __init__(self, video_source: str, point_manager: PointManager):
        """
        Инициализация VideoManager.

        :param video_source: Путь к видеофайлу.
        :param point_manager: Экземпляр PointManager для управления точками.
        """
        self.point_manager = point_manager
        self.capture = self._initialize_video(video_source)
        self.trackers = {'belly': None, 'breast': None}  # Хранение трекеров
        self.points = {'belly': None, 'breast': None}    # Хранение координат
        self.data = pd.DataFrame(columns=["time_st", "mark_belly", "mark_breast"])
        self.recording_paused = True  # Флаг остановки записи

    def _initialize_video(self, video_source: str) -> cv2.VideoCapture:
        """
        Инициализация источника видео.

        :param video_source: Путь к видеофайлу.
        :return: Объект cv2.VideoCapture.
        """
        capture = cv2.VideoCapture(video_source)
        if not capture.isOpened():
            raise ValueError("Ошибка: не удалось открыть видео!")
        cv2.namedWindow("My Camera")
        cv2.setMouseCallback("My Camera", self.on_mouse)
        return capture

    def on_mouse(self, event: int, x: int, y: int, flags: int, param) -> None:
        """
        Обработчик мыши для выбора точек и добавления их в VideoManager.

        :param event: Тип события мыши.
        :param x: Координата X.
        :param y: Координата Y.
        :param flags: Дополнительные параметры.
        :param param: Пользовательский параметр.
        :return: None
        """
        if event == cv2.EVENT_LBUTTONUP:
            if self.point_manager.selected_mode in self.points and self.points[self.point_manager.selected_mode] is None:
                self.points[self.point_manager.selected_mode] = (x, y)
                self.trackers[self.point_manager.selected_mode] = ColorTracker(x, y)
                print(f"Добавлена новая точка '{self.point_manager.selected_mode}': ({x}, {y})")
                self.point_manager.selected_mode = None

    # def main_loop(self) -> None:
    #     """
    #     Главный цикл обработки видео.
    #
    #     :return: None
    #     """
    #     success, frame = self.capture.read()
    #     while success and cv2.waitKey(1) == -1:
    #         success, frame = self.capture.read()
    #         if not success:
    #             break
    #
    #         if self.points['belly'] is None:
    #             self.point_manager.point_belly()
    #         elif self.points['breast'] is None:
    #             self.point_manager.point_breast()
    #         else:
    #             self.point_manager.selected_mode = None
    #
    #         if self.point_manager.selected_mode is not None:
    #             print(f"Кликните на объект для выбора точки: {self.point_manager.selected_mode}")
    #
    #         # Создание трекеров при наличии точек
    #         for key in self.points:
    #             if self.points[key] is not None and self.trackers[key] is None:
    #                 self.trackers[key] = ColorTracker(*self.points[key])
    #
    #         frame = self._process_frame(frame)
    #
    #         if not self.recording_paused:
    #             self.data = self._update_dataframe(self.data, self.trackers)
    #
    #         #print(f"Текущий словарь точек: {self.points}")
    #         #print(f"Текущий DataFrame:\n{self.data}")
    #
    #         cv2.imshow("My Camera", frame)

    def start_recording_dataframe(self) -> None:
        """
        Начать запись данных в DataFrame.
        """
        if self.recording_paused:
            self.recording_paused = False
            print("Флаг на запись данных в DataFrame.")

    def stop_recording_dataframe(self) -> None:
        """
        Остановить запись данных в DataFrame.
        """
        if not self.recording_paused:
            self.recording_paused = True
            print("Флаг на остановку записи данных в DataFrame.")


    def get_dataframe(self) -> pd.DataFrame:
        """
        Возвращает временной ряд отслеживания двух точек.

        :return: DataFrame с временными рядами.
        """
        return self.data

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Обработка текущего кадра.

        :param frame: Текущий кадр видео.
        :return: Обработанный кадр.
        """
        self.recording_paused = False
        for key, tracker in self.trackers.items():
            if tracker is not None:
                frame = tracker.update_image(frame)
                if tracker.lost:
                    print(f"Объект '{key}' потерян. Запись приостановлена.")
                    self.trackers[key] = None
                    self.points[key] = None
                    self.point_manager.selected_mode = key  # Устанавливаем режим выбора точки
                    self.recording_paused = True
                else:
                    self.points[key] = (tracker.x, tracker.y)

            else:
                self.recording_paused = True
        return frame

    def update_dataframe(self, data: pd.DataFrame, trackers: list) -> pd.DataFrame:
        """
        Обновление DataFrame с координатами точек.

        :param data: DataFrame с текущими данными.
        :param trackers: Список трекеров.
        :return: Обновленный DataFrame.
        """
        current_time = datetime.now()
        y_points = {key: (tracker.y if tracker and not tracker.lost else None) for key, tracker in trackers.items()}
        new_row = {"time_st": current_time, "mark_belly": y_points['belly'], "mark_breast": y_points['breast']}

        if any(value is None for value in y_points.values()):
            #print("Данные не добавлены: одна или более точек потеряны")
            return data
        #print(f"Добавление строки в DataFrame: {new_row}")
        return pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    def create_graph(self, dataframe: pd.DataFrame) -> None:
        """
        Построение и сохранение графика на основе данных.

        :param dataframe: DataFrame с данными.
        :return: None
        """
        if dataframe is None:
            print("Нет данных для построения графика.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(dataframe['time_st'], dataframe['mark_belly'], color='red', label='Sticker 1')
        plt.plot(dataframe['time_st'], dataframe['mark_breast'], color='blue', label='Sticker 2')
        plt.title('Object Tracking')
        plt.xlabel('Time (s)')
        plt.ylabel('Coordinate Y')
        plt.grid()
        plt.legend()
        plt.savefig('tracking_graph.png')
        plt.show()

    def end(self) -> None:
        """
        Завершение работы с видеопотоком.

        :return: None
        """
        self.capture.release()
        cv2.destroyAllWindows()
