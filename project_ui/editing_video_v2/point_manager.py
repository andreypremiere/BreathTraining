import cv2


class PointManager:
    """Управление выбранными точками и режимами."""

    def __init__(self):
        """
        Инициализация PointManager.
        """
        self.selected_mode = None  # Режим работы ("belly" или "breast")

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