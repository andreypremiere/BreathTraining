import cv2


class PointManager:
    """Управление выбранными точками и режимами."""

    def __init__(self):
        """
                Инициализация PointManager.
                """
        self.selected_mode = None  # Режим работы ("belly" или "breast")
        self.points = []
        print('Класс PointManager инициализирован')


    def on_mouse(self, event: int, x: int, y: int, flags: int, param) -> None:
        """
        Обработчик мыши для выбора точек.
        :param event: Тип события мыши.
        :param x: Координата X.
        :param y: Координата Y.
        :param flags: Дополнительные параметры.
        :param param: Пользовательский параметр.
        :return: None
        """
        if event == cv2.EVENT_LBUTTONUP and self.selected_mode is not None:
            self.points.append((x, y))
            self.selected_mode = None

    def point_belly(self) -> None:
        """Установить режим выбора точки для живота.

        :return: None
        """
        self.selected_mode = "belly"

    def point_breast(self) -> None:
        """
        Установить режим выбора точки для груди.

        :return: None
        """
        self.selected_mode = "breast"