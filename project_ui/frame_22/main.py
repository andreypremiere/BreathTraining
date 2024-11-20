import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLCDNumber, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana de Información del Paciente con Cámara en Tiempo Real")
        self.setGeometry(200, 200, 900, 500)
        self.setStyleSheet("background-color:#caf0f8;")

        # Create main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # principal Layout 
        main_layout = QVBoxLayout(central_widget)

        # Create the header with name and details
        header_layout = QVBoxLayout()
        name_label = QLabel("Иванов Иван Иванович")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        birthdate_label = QLabel("Дата рождения: 12.09.2000  Возраст: 2000")

        header_layout.addWidget(name_label)
        header_layout.addWidget(birthdate_label)

        # Add header to the main layout
        main_layout.addLayout(header_layout)

        # Layout for image and controls
        middle_layout = QHBoxLayout()

        # Real-time camera (video stream)
        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(350, 250)  # Establecer tamaño fijo para el video

        # Layout of controls
        control_layout = QVBoxLayout()

        # Camera calibration button
        calibrate_button = QPushButton("Калибровка камеры")
        
        # Button to select metadata
        select_tags_button = QPushButton("Выбрать метки")

        # Timer (placeholder)
        timer_label = QLabel("Таймер")
        timer_display = QLCDNumber()
        timer_display.display("10:00")
        
        # Button to start the procedure
        start_button = QPushButton("Начать процедуру")

        # Adding widgets to the control layout
        control_layout.addWidget(calibrate_button)
        control_layout.addWidget(select_tags_button)
        control_layout.addWidget(timer_label)
        control_layout.addWidget(timer_display)
        control_layout.addWidget(start_button)

        # Add spaces for clean design
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        control_layout.addItem(spacer)

        # Add camera and controls to the media layout
        middle_layout.addWidget(self.camera_label)
        middle_layout.addLayout(control_layout)

        # Add middle layout to the main layout
        main_layout.addLayout(middle_layout)

        # Layout of instructions
        instructions_layout = QVBoxLayout()
        instructions_label = QLabel("Инструкция")
        instructions_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        instructions_text = QLabel(
            "1. Здесь будет подробная инструкция по настройке камеры;\n"
            "2. И все, что нужно, чтобы начать сессию.\n"
            "3. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
            "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation."
        )

        instructions_layout.addWidget(instructions_label)
        instructions_layout.addWidget(instructions_text)

        # Add instruction layout to the main layout
        main_layout.addLayout(instructions_layout)

        # Camera configuration (OpenCV)
        self.cap = cv2.VideoCapture(0)  # Open camera (use the correct index if you have more than one camera)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Image refresh every 30 ms (approximately 30 fps)

    def update_frame(self):
        ret, frame = self.cap.read()  # Read the camera chart
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert color from BGR to RGB for PyQt
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.camera_label.setPixmap(pixmap.scaled(350, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.cap.release()  # Release the camera when closing the window
        event.accept()


# Start the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
