import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer, QTime


class ProcedureWindow(QWidget):
    def __init__(self, switch_window_callback=None):
        super().__init__()
        self.switch_window = switch_window_callback
        self.init_ui()

    def init_ui(self):
        # Ventana principal
        self.setWindowTitle("PATIENT DATA")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #CAF0F8;")

        # Layout principal
        self.layout_principal_procedure = QHBoxLayout(self)

        # Info del Paciente (Ejemplo)
        info_paciente = QLabel("Иванов Иван Иванович\nДата рождения: 12.09.2000    Возраст: 2000")
        info_paciente.setStyleSheet("""
            background-color: #D4F1F4;
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            """)
        info_paciente.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_principal_procedure.addWidget(info_paciente)

        # Panel de video (OpenCV)
        self.label_video = QLabel(self)
        self.label_video.setStyleSheet("border: 2px solid #ccc;")
        self.label_video.setFixedSize(640, 480)
        self.layout_principal_procedure.addWidget(self.label_video)

        # Panel derecho (Controles)
        layout_panel_control = QVBoxLayout()

        control_label = QLabel("Управление")
        control_label.setStyleSheet("font-size: 16px; padding: 5px;")
        control_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_panel_control.addWidget(control_label)

        # Botón de calibración
        self.boton_calibracion = QPushButton("Калибровка камеры")
        self.boton_calibracion.setStyleSheet("""
            background-color: #B0BEC5;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        """)
        layout_panel_control.addWidget(self.boton_calibracion)

        # Botón para seleccionar metas
        self.boton_metas = QPushButton("Выбрать метки")
        self.boton_metas.setStyleSheet("""
            background-color: #B0BEC5;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        """)
        layout_panel_control.addWidget(self.boton_metas)

        # Botón para comenzar la sesión
        self.start_button = QPushButton("Начать процедуру")
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setStyleSheet("""
            background-color: #B3E5FC;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        """)
        layout_panel_control.addWidget(self.start_button)

        # Etiqueta del temporizador
        self.time_display = QLabel("10:00")
        self.time_display.setStyleSheet("font-size: 24px; color: black;")
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_panel_control.addWidget(self.time_display)

        # Añadir el panel de control al layout principal
        self.layout_principal_procedure.addLayout(layout_panel_control)

        # Configuración del temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Tiempo de ejemplo (10 minutos)
        self.remaining_time = QTime(0, 0, 5) #change its 5 seconds

        # Configuración de captura de video con OpenCV
        self.capture = cv2.VideoCapture(0)  # 0 para la cámara por defecto
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_video)
        self.video_timer.start(30)  # Actualizar cada 30 ms (~33 fps)

    def start_timer(self):
        """Iniciar el temporizador al presionar el botón"""
        self.timer.start(1000)

    def update_timer(self):
        """Actualiza la pantalla del temporizador cada segundo."""
        if self.remaining_time > QTime(0, 0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.time_display.setText(self.remaining_time.toString("mm:ss"))
        else:
            self.timer.stop()
            self.time_display.setText("00:00")
            self.time_display.setStyleSheet("font-size: 24px; color: red;")
            print("¡Tiempo finalizado!")  # Acción al finalizar el temporizador

    def update_video(self):
        """Captura y muestra frames del video en tiempo real."""
        ret, frame = self.capture.read()
        if ret:
            # Convertir frame de BGR (OpenCV) a RGB (Qt)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            q_image = QImage(frame.data, width, height, step, QImage.Format.Format_RGB888)
            # Mostrar frame en el QLabel
            self.label_video.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        """Cierra la cámara cuando se cierra la ventana."""
        self.capture.release()
        super().closeEvent(event)


app = QApplication(sys.argv)
ventana = ProcedureWindow()
ventana.show()
sys.exit(app.exec())
