import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt
import pyqtgraph as pg


class StaticGraph(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMaximumWidth(900)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setMaximumHeight(500)

        self.data = data or {'timestamps': [], 'belly': [], 'breast': []}  # Убедимся, что есть данные
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса графика"""
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground("w")
        self.plot_widget.setYRange(0, 480)
        self.plot_widget.setTitle("Данные процедуры")
        self.plot_widget.addLegend()
        self.plot_widget.setLabel("left", "Значение")
        self.plot_widget.setLabel("bottom", "Время")

        self.plot_widget.setMouseEnabled(x=True, y=False)


        # Линии на графике
        self.line1 = self.plot_widget.plot(
            pen=pg.mkPen(color="b", width=2), name="belly"
        )
        self.line2 = self.plot_widget.plot(
            pen=pg.mkPen(color="r", width=2), name="breast"
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Отрисовка графика сразу после инициализации
        self.plot_data()

    def plot_data(self):
        """Отображение данных на графике"""

        def parse_timestamp(t):
            return t.strftime("%H:%M:%S")

        try:
            # Преобразуем временные метки в строковый формат
            r_values = [parse_timestamp(t) for t in self.data['timestamps']]
            x_values = list(range(len(self.data['timestamps'])))
        except ValueError as e:
            print(f"Ошибка преобразования временной метки: {e}")
            return

        # Обновляем данные графика
        y1_values = self.data['belly']
        y2_values = self.data['breast']
        self.line1.setData(x_values, y1_values)
        self.line2.setData(x_values, y2_values)

        # Настройка меток оси X
        self.plot_widget.getAxis('bottom').setTicks([list(zip(x_values, r_values))])

        # Автоматическая настройка диапазона
        min_y = min(min(y1_values), min(y2_values))  # Минимальное значение
        max_y = max(max(y1_values), max(y2_values))  # Максимальное значение

        self.plot_widget.setXRange(0, len(x_values) - 1, padding=0)
        self.plot_widget.setYRange(min_y, max_y, padding=0.1)


# class MainWindow(QWidget):
#     def __init__(self, data):
#         super().__init__()
#         self.data = data
#         self.init_ui()
#
#     def init_ui(self):
#         # self.setWindowTitle("График с данными")
#         main_layout = QVBoxLayout(self)
#
#         # Добавляем фрейм с графиком
#         self.graph_frame = StaticGraph(self, self.data)
#         main_layout.addWidget(self.graph_frame, alignment=Qt.AlignmentFlag.AlignHCenter)
#
#         self.setLayout(main_layout)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     # Пример данных
#     import datetime
#     import random
#
#     timestamps = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(30)]
#     belly_data = [random.randint(200, 400) for _ in range(30)]
#     breast_data = [random.randint(150, 350) for _ in range(30)]
#     data = {'timestamps': timestamps, 'belly': belly_data, 'breast': breast_data}
#
#     window = MainWindow(data)
#     window.show()
#     sys.exit(app.exec())
