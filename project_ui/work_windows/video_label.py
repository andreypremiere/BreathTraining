from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel

from editing_video_v2.color_tracker import ColorTracker


class VideoLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.panel_choosing_marks = None
        self.video_manager = None
        self.actual_coordinates = None
        self.label_widget = None

    def mousePressEvent(self, event: QMouseEvent):
        label_x = event.position().x()
        label_y = event.position().y()

        print(f"Координаты клика на лейбле: x={label_x}, y={label_y}")

        # Вычисление относительных координат (для изображения)
        relative_x = label_x / self.width()
        relative_y = label_y / self.height()

        x = int(relative_x * self.actual_coordinates[0])
        y = int(relative_y * self.actual_coordinates[1])
        print(f'Точки для настоящего кадра: x:{x}, y: {y}')

        # print(self.video_manager.point_manager.selected_mode)

        if self.panel_choosing_marks is not None:
            if self.video_manager.point_manager.selected_mode in self.video_manager.points \
                    and self.video_manager.points[self.video_manager.point_manager.selected_mode] is None:
                self.video_manager.points[self.video_manager.point_manager.selected_mode] = (x, y)
                self.video_manager.trackers[self.video_manager.point_manager.selected_mode] = ColorTracker(x, y)
                print(f"Добавлена новая точка '{self.video_manager.point_manager.selected_mode}': (x: {x}, y: {y})")
                self.panel_choosing_marks.change_mark()

        # print(f"Относительные координаты на изображении: x={relative_x:.2f}, y={relative_y:.2f}")

        super().mousePressEvent(event)