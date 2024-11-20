import sys
import cv2
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpacerItem, QSizePolicy
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration of the main window
        self.setWindowTitle("Examen del Paciente")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #E0F7FA;")

        # Layout principal
        layout_principal = QVBoxLayout(self)

        # ---------- Información del Paciente ----------
        info_paciente = QLabel("Иванов Иван Иванович\nДата рождения: 12.09.2000    Возраст: 2000")
        info_paciente.setStyleSheet("""
            background-color: #D4F1F4;
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            """)
        info_paciente.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---------- Video de la Cámara (OpenCV) ----------
        self.label_video = QLabel(self)
        self.label_video.setStyleSheet("border: 2px solid #ccc;")
        self.label_video.setFixedSize(640, 480)

        # ---------- Panel de Control a la Derecha ----------
        layout_panel_control = QVBoxLayout()
        control_label = QLabel("Управление")
        control_label.setStyleSheet("font-size: 16px; padding: 5px;")

        # Botón de Calibración
        self.boton_calibracion = QPushButton("Калибровка камеры")
        self.boton_calibracion.setStyleSheet("""
            background-color: #B0BEC5;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        """)

        # Texto "Калибровка завершена"
        self.label_calibracion = QLabel("Калибровка завершена")
        self.label_calibracion.setStyleSheet("font-size: 12px; color: gray;")

        # Botón para Seleccionar Metas
        self.boton_metas = QPushButton("Выбрать метки")
        self.boton_metas.setStyleSheet("""
            background-color: #B0BEC5;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        """)

        # Campos para las Metas
        self.label_meta1 = QLabel("Метка груди:")
        self.input_meta1 = QLineEdit(self)
        self.input_meta1.setText("367622")  # Estos son placeholders para integrarse con otro sistema.

        self.label_meta2 = QLabel("Метка живота:")
        self.input_meta2 = QLineEdit(self)
        self.input_meta2.setText("367622")

        # Temporizador
        self.timer_label = QLabel("Таймер")
        self.time_display = QLabel("10 : 00")
        self.time_display.setStyleSheet("font-size: 24px; color: black;")
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón para Comenzar la Sesión
        self.boton_inicio = QPushButton("Начать процедуру")
        self.boton_inicio.setStyleSheet("""
            background-color: #B3E5FC;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        """)

        # Add to Control Panel Layout
        layout_panel_control.addWidget(control_label)
        layout_panel_control.addWidget(self.boton_calibracion)
        layout_panel_control.addWidget(self.label_calibracion)
        layout_panel_control.addWidget(self.boton_metas)
        layout_panel_control.addWidget(self.label_meta1)
        layout_panel_control.addWidget(self.input_meta1)
        layout_panel_control.addWidget(self.label_meta2)
        layout_panel_control.addWidget(self.input_meta2)
        layout_panel_control.addWidget(self.timer_label)
        layout_panel_control.addWidget(self.time_display)
        layout_panel_control.addWidget(self.boton_inicio)
        layout_panel_control.addStretch()

        # ---------- Instructions on the Bottom ----------
        instrucciones = QLabel("""
        1. Здесь будет подробная инструкция по настройке камеры;
        2. И все, что нужно, чтобы начать сессию.
        3. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """)
        instrucciones.setStyleSheet("""
            background-color: #FFFFFF;
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
            """)
        instrucciones.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ---------- Main Distribution: Video on the left and Control Panel on the right ----------
        layout_central = QHBoxLayout()
        layout_central.addWidget(self.label_video)
        layout_central.addLayout(layout_panel_control)

        # Add all to Main Layout
        layout_principal.addWidget(info_paciente)
        layout_principal.addLayout(layout_central)
        layout_principal.addWidget(instrucciones)

        # Configuring the camera using OpenCV
        self.cap = cv2.VideoCapture(0)  # Uses the default camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Refresh every 30ms (approx. 33fps)

        # Temporizador
        self.time_left = QTime(0, 10, 0)  # Inicia en 10 minutos
        self.timer.timeout.connect(self.update_timer)

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

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        self.time_display.setText(self.time_left.toString("mm : ss"))

        if self.time_left == QTime(0, 0, 0):
            self.timer.stop()

    def closeEvent(self, event):
        # When closing the window, release the camera
        self.cap.release()

# Ejecución de la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
