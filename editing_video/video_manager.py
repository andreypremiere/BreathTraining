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
        self.trackers = []
        self.data = pd.DataFrame(columns=["time_st", "mark_belly", "mark_breast"])

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
        cv2.setMouseCallback("My Camera", self.point_manager.on_mouse)
        return capture

    def main_loop(self) -> None:
        """
        Главный цикл обработки видео.

        :return: None
        """
        success, frame = self.capture.read()
        while success and cv2.waitKey(1) == -1:
            success, frame = self.capture.read()
            if not success:
                break

            # Обработка выбора точек
            if len(self.point_manager.points) < 2:
                if len(self.point_manager.points) == 0:
                    self.point_manager.point_belly()
                elif len(self.point_manager.points) == 1:
                    self.point_manager.point_breast()
            else:
                self.point_manager.selected_mode = None

            # Создаем трекеры для новых точек
            if len(self.point_manager.points) > 0:
                if len(self.trackers) < len(self.point_manager.points):
                    for (x, y) in self.point_manager.points[len(self.trackers):]:
                        self.trackers.append(ColorTracker(x, y))

            frame = self._process_frame(frame)
            self.data = self._update_dataframe(self.data, self.trackers)
            cv2.imshow("My Camera", frame)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Возвращает временной ряд отслеживания двух точек.

        :return: DataFrame с временными рядами.
        """
        return self.data

    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Обработка текущего кадра.

        :param frame: Текущий кадр видео.
        :return: Обработанный кадр.
        """
        for tracker in self.trackers:
            frame = tracker.update_image(frame)
        return frame

    def _update_dataframe(self, data: pd.DataFrame, trackers: list) -> pd.DataFrame:
        """
        Обновление DataFrame с координатами точек.

        :param data: DataFrame с текущими данными.
        :param trackers: Список трекеров.
        :return: Обновленный DataFrame.
        """
        current_time = datetime.now()
        y_points = [tracker.y for tracker in trackers]
        y_point1 = y_points[0] if len(y_points) > 0 else None
        y_point2 = y_points[1] if len(y_points) > 1 else None
        new_row = {"time_st": current_time, "mark_belly": y_point1, "mark_breast": y_point2}
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