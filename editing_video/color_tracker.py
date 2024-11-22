import cv2
import numpy as np


class ColorTracker:
    """Трекер для отслеживания точек на изображении."""

    def __init__(self, x: int, y: int, max_area_change: float = 0.3):
        """
        Инициализация ColorTracker.

        :param x: Координата X.
        :param y: Координата Y.
        :param max_area_change: Максимально допустимое изменение площади.
        """
        self.x = x
        self.y = y
        self.edges = None
        self.lost = False
        self.initial_area = None
        self.max_area_change = max_area_change

    def update_image(self, frame: np.ndarray) -> np.ndarray:
        """
        Обновление позиции трекера на текущем кадре.

        :param frame: Текущий кадр видео.
        :return: Обновленный кадр.
        """
        self.edges = self.get_edges(frame)
        contours, _ = cv2.findContours(self.edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        dists = []

        for contour in contours:
            dist = cv2.pointPolygonTest(contour, (self.x, self.y), True)
            dists.append(dist)
        dists = np.array(dists)

        if len(dists) > 0 and np.max(dists) > 0:
            needed_contour = np.argmax(dists)
            bbox = cv2.boundingRect(contours[needed_contour])
            self.x = bbox[0] + bbox[2] // 2
            self.y = bbox[1] + bbox[3] // 2

            frame = cv2.drawContours(frame, [contours[needed_contour]], -1, (0, 255, 0), 2)
            frame = cv2.circle(frame, (self.x, self.y), 10, (0, 0, 255), -1)
            self.lost = False
        else:
            self.x, self.y = None, None
            self.lost = True
        return frame

    @staticmethod
    def get_edges(frame: np.ndarray) -> np.ndarray:
        """
        Получение границ с помощью Canny.

        :param frame: Текущий кадр видео.
        :return: Границы кадра.
        """
        return cv2.Canny(frame, 200, 200)
