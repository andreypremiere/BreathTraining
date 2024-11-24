import cv2
import numpy as np


class ColorTracker:
    """Трекер для отслеживания точек на изображении."""

    def __init__(self, x: int, y: int, max_area_change: float = 0.6):
        """
        Инициализация ColorTracker.

        :param x: Координата X.
        :param y: Координата Y.
        :param initial_area: Изначальное значение площади
        :param max_area_change: Максимально допустимое изменение площади.
        """
        self.x = x
        self.y = y
        self.edges = None
        self.lost = False
        self.initial_area = None
        self.max_area_change = max_area_change
        print('Класс ColorTracker инициализирован')


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
            needed_contour = contours[np.argmax(dists)]
            area = cv2.contourArea(needed_contour)

            if self.initial_area is None:
                self.initial_area = area

            area_change = abs(area - self.initial_area) / self.initial_area
            if area_change > self.max_area_change:
                self.lost = True
                self.x, self.y = None, None
                return frame

            bbox = cv2.boundingRect(needed_contour)
            self.x = bbox[0] + bbox[2] // 2
            self.y = bbox[1] + bbox[3] // 2
            self.initial_area = area

            frame = cv2.drawContours(frame, [needed_contour], -1, (0, 255, 0), 2)
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