from datetime import datetime, timedelta
import sys
import time
import pandas as pd
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSizePolicy
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg


class RealTimeGraph(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(900)
        self.setMinimumHeight(200)
        self.init_ui()

        # Определяем видимую область
        self.visible_points = 30  # Количество точек, которые должны быть видны
        self.auto_scroll = True  # Флаг автоматического скроллинга

        self.data = data

    def init_ui(self):
        """Инициализация интерфейса графика"""
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground("w")
        self.plot_widget.setYRange(0, 480)
        self.plot_widget.setTitle("Данные процедуры")
        self.plot_widget.addLegend()
        self.plot_widget.setLabel("left", "Значение")
        self.plot_widget.setLabel("bottom", "Время")

        # Включаем панорамирование и масштабирование
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

    # Пример обновления графика
    def update_graph(self):
        """Обновление данных графика"""

        def parse_timestamp(t):
            return t.strftime("%H:%M:%S")

        try:
            # Преобразуем все временные метки в миллисекунды
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

        # Установка диапазона X
        if len(x_values) > self.visible_points:
            self.plot_widget.setXRange(x_values[-self.visible_points], x_values[-1], padding=0)

        # Установка диапазона Y
        min_y = min(min(y1_values), min(y2_values))  # Минимальное значение из обоих графиков
        max_y = max(max(y1_values), max(y2_values))  # Максимальное значение из обоих графиков

        self.plot_widget.setYRange(min_y, max_y, padding=0.1)  # Добавляем небольшой отступ


# if __name__ == "__main__":
#
#     # Запуск приложения
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
