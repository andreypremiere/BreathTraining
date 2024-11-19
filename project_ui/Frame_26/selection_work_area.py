import sys
import cv2
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Detalles del Paciente con Cámara en Tiempo Real")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #E0F7FA;")

        # principal layout
        layout_principal = QVBoxLayout(self)

        # ---------- Patient Information ----------
        info_paciente = QLabel("Иванов Иван Иванович\nДата рождения: 12.09.2000    Возраст: 2000")
        info_paciente.setStyleSheet("""
            background-color: #D4F1F4;
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            """)
        info_paciente.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---------- Highlight button ----------
        boton_resaltar = QPushButton("Выделите область первой метки")
        boton_resaltar.setStyleSheet("""
            background-color: #FFAB91;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        """)

        # Layout for button and icon
        layout_boton = QHBoxLayout()
        layout_boton.addWidget(boton_resaltar)
        layout_boton.addStretch()

        # Camera Video (OpenCV) 
        self.label_video = QLabel(self)
        self.label_video.setStyleSheet("border: 2px solid #ccc;")
        self.label_video.setFixedSize(800, 450)

        # Add widgets to the main layout
        layout_principal.addWidget(info_paciente)
        layout_principal.addLayout(layout_boton)
        layout_principal.addWidget(self.label_video)

        # Configuring the camera using OpenCV
        self.cap = cv2.VideoCapture(0)  # Uses the default camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Refresh every 30ms (approx. 33fps)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame from BGR (OpenCV) to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to QImage format
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format.Format_RGB888)

            # Display the frame in the QLabel
            self.label_video.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        # When closing the window, release the camera
        self.cap.release()

# Execution of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
