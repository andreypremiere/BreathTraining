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
        self.visible_points = 10  # Количество точек, которые должны быть видны
        self.auto_scroll = True  # Флаг автоматического скроллинга
        self.current_index = 0  # Индекс для данных

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

        # Преобразуем временные метки в миллисекунды
        def parse_timestamp_to_ms(timestamp):
            """Преобразует строку формата HH:MM:SS:MMM в миллисекунды"""
            h, m, s, ms = map(int, timestamp.split(":"))
            return (h * 3600 + m * 60 + s) * 1000 + ms

        try:
            # Преобразуем все временные метки в миллисекунды
            x_values = [parse_timestamp_to_ms(t) for t in self.data['timestamp']]
        except ValueError as e:
            print(f"Ошибка преобразования временной метки: {e}")
            return

        # Обновляем данные графика
        y1_values = self.data['belly']
        y2_values = self.data['breast']
        self.line1.setData(x_values, y1_values)
        self.line2.setData(x_values, y2_values)

        # Настройка меток оси X
        self.plot_widget.getAxis('bottom').setTicks([list(zip(x_values, self.data['timestamp']))])

        # Установка диапазона X
        if len(x_values) > self.visible_points:
            self.plot_widget.setXRange(x_values[-self.visible_points], x_values[-1], padding=0)

        # Установка диапазона Y
        min_y = min(min(y1_values), min(y2_values))  # Минимальное значение из обоих графиков
        max_y = max(max(y1_values), max(y2_values))  # Максимальное значение из обоих графиков

        self.plot_widget.setYRange(min_y, max_y, padding=0.1)  # Добавляем небольшой отступ

        self.current_index += 1


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("График с данными")

        # Основной макет
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # self.setFixedSize(1200, 600)

        # Добавляем фрейм с графиком
        self.graph_frame = RealTimeGraph(self)
        main_layout.addWidget(self.graph_frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Кнопки для управления
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Начать")
        self.stop_button = QPushButton("Остановить")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        # Привязка кнопок
        self.start_button.clicked.connect(self.start_graph)
        self.stop_button.clicked.connect(self.stop_graph)

        self.setLayout(main_layout)

    def start_graph(self):
        """Запускает обновление графика"""
        self.graph_frame.timer = QTimer()
        self.graph_frame.timer.timeout.connect(self.graph_frame.update_graph)
        self.graph_frame.timer.start(1000)  # Обновление графика каждую секунду

    def stop_graph(self):
        """Останавливает обновление графика"""
        self.graph_frame.timer.stop()


if __name__ == "__main__":

    # Запуск приложения
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
