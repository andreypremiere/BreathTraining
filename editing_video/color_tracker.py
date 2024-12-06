import cv2
import numpy as np

class ColorTracker:
    """Трекер для отслеживания точек на изображении."""

    def __init__(self, x: int, y: int, max_area_change: float = 1):
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

    def update_image(self, frame: np.ndarray) -> np.ndarray:
        """
        Обновление позиции трекера на текущем кадре.

        :param frame: Текущий кадр видео.
        :return: Обновленный кадр.
        """
        self.edges = self.get_edges(frame)

        # Маска для ограничения области поиска
        search_radius = 100
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        if self.x is not None and self.y is not None:
            cv2.circle(mask, (self.x, self.y), search_radius, 255, -1)
        masked_edges = cv2.bitwise_and(self.edges, self.edges, mask=mask)

        # Поиск контуров
        contours, _ = cv2.findContours(masked_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print("Контуры не найдены. Объект потерян.")
            self.lost = True
            self.x, self.y = None, None
            return frame

        # Поиск ближайшего контура
        dists = [cv2.pointPolygonTest(cnt, (self.x, self.y), True) for cnt in contours]
        max_index = np.argmax(dists)
        selected_contour = contours[max_index]

        # Проверка площади
        current_area = cv2.contourArea(selected_contour)
        if current_area < 200:
            print("Объект слишком мал. Игнорируем.")
            return frame

        if self.initial_area is None:
            self.initial_area = current_area
            print("Установлена начальная площадь объекта.")
        else:
            relative_change = abs(current_area - self.initial_area) / self.initial_area
            if relative_change > self.max_area_change:
                print(f"Изменение площади слишком велико ({relative_change:.2f}). Объект потерян.")
                self.lost = True
                self.x, self.y = None, None
                return frame

        # Проверка формы
        bbox = cv2.boundingRect(selected_contour)
        aspect_ratio = bbox[2] / bbox[3] if bbox[3] != 0 else 0
        if aspect_ratio < 0.5 or aspect_ratio > 2:
            print("Контур слишком деформирован. Игнорируем.")
            return frame

        # Проверка на смещение
        if self.x is not None and self.y is not None:
            distance = np.sqrt((self.x - (bbox[0] + bbox[2] // 2)) ** 2 +
                               (self.y - (bbox[1] + bbox[3] // 2)) ** 2)
            if distance > search_radius:
                print("Объект сместился слишком далеко. Потерян.")
                self.lost = True
                self.x, self.y = None, None
                return frame

        # Обновление координат
        self.x = bbox[0] + bbox[2] // 2
        self.y = bbox[1] + bbox[3] // 2

        # Отрисовка контура и точки
        frame = cv2.drawContours(frame, [selected_contour], -1, (0, 255, 0), 2)
        frame = cv2.circle(frame, (self.x, self.y), 10, (0, 0, 255), -1)

        return frame

    @staticmethod
    def get_edges(frame: np.ndarray) -> np.ndarray:
        """
        Получение границ с помощью Canny.

        :param frame: Текущий кадр видео.
        :return: Границы кадра.
        """

        return cv2.Canny(frame, 150, 200)