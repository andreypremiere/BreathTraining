import sys
import cv2
import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QWidget):
    def __init__(self):  # Cambiado a __init__
        super().__init__()

        # Window configuration
        self.setWindowTitle("Cámara y Datos en Tiempo Real")
        self.setGeometry(100, 100, 1000, 800)
        layout = QVBoxLayout()

        # Real-time camera
        self.camera_label = QLabel(self)
        layout.addWidget(self.camera_label)

        # Statistics container
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("Estadísticas: actualizando...")
        stats_layout.addWidget(self.stats_label)

        # Real-time graphic
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        stats_layout.addWidget(self.canvas)

        # Add statistics and graphics to the main layout
        layout.addLayout(stats_layout)

        # Control buttons
        self.start_button = QPushButton("Iniciar Procedimiento", self)
        self.start_button.clicked.connect(self.start_camera)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Terminar Procedimiento", self)
        self.stop_button.clicked.connect(self.stop_camera)
        layout.addWidget(self.stop_button)

        # Timer to update camera and graphics
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Initialize video capture (camera)
        self.cap = cv2.VideoCapture(0)  # ID 0 for the default camera
        self.setLayout(layout)

    def start_camera(self):
        # Check if the camera is opened correctly
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return
        self.timer.start(30)  # Update every 30 ms

    def stop_camera(self):
        self.timer.stop()
        self.cap.release()
        cv2.destroyAllWindows()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert OpenCV image (BGR) to Qt (RGB)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            # Show image in QLabel
            self.camera_label.setPixmap(pixmap)

            # Update graph with simulated data
            self.update_graph()

    def update_graph(self):
        # Generate sample random data (replace with real data)
        t = np.linspace(0, 10, 100)
        y = np.sin(t + np.random.random())

        # Clean the figure and plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(t, y, label="Datos en tiempo real")
        ax.set_title("Gráfico de Señal en Tiempo Real")
        self.canvas.draw()

# Iniciar aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
