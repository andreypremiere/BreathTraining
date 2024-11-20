import sys
import cv2
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                            QGridLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QPixmap, QImage, QFont
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        #Это вариант result_test.py - тест.  главный из них result_test.py
        
        
        
        # Configuración de la ventana principal
        self.setWindowTitle("Interfaz Médica")
        self.setStyleSheet("background-color: #e0f7ff;")
        self.setFixedSize(800, 600)
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Sección de información del paciente
        info_layout = QVBoxLayout()
        self.name_label = QLabel("Иванов Иван Иванович")
        self.name_label.setFont(QFont("Arial", 16))
        self.birth_label = QLabel("Дата рождения: 12.09.2000    Возраст: 2000")
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.birth_label)
        
        # Sección de imagen con OpenCV
        self.image_label = QLabel()
        self.load_image("/path/to/your/image.jpg")  # Cambia a la ruta de tu imagen
        self.image_label.setFixedSize(500, 250)
        
        # Temporizador
        self.timer_label = QLabel("Таймер")
        self.timer_label.setFont(QFont("Arial", 14))
        self.time_display = QLabel("09 : 21")
        self.time_display.setFont(QFont("Arial", 16))
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Configurar el temporizador en cuenta regresiva
        self.timer = QTimer(self)
        self.time_left = QTime(0, 9, 21)
        self.timer.timeout.connect(self.update_timer)
        
        # Botón para terminar el procedimiento
        self.finish_button = QPushButton("Завершить процедуру")
        self.finish_button.clicked.connect(self.finish_procedure)
        
        # Layout para el control
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.timer_label)
        control_layout.addWidget(self.time_display)
        control_layout.addWidget(self.finish_button)
        
        # Sección de estadísticas
        stats_label = QLabel("Статистика")
        stats_label.setFont(QFont("Arial", 14))
        stats_layout = QVBoxLayout()
        stats_layout.addWidget(stats_label)
        
        # Añadir etiquetas de estadísticas
        self.chest_label = QLabel("Метка груди: 367622")
        self.abdomen_label = QLabel("Метка живота: 367622")
        self.extra_data_label_1 = QLabel("И еще что-то: да")
        self.extra_data_label_2 = QLabel("Еще какие-то данные: да")
        
        stats_layout.addWidget(self.chest_label)
        stats_layout.addWidget(self.abdomen_label)
        stats_layout.addWidget(self.extra_data_label_1)
        stats_layout.addWidget(self.extra_data_label_2)
        
        # Plano cartesiano para gráficas (no implementado)
        self.chart_label = QLabel()
        self.chart_label.setFixedSize(500, 200)
        self.chart_label.setFrameShape(QFrame.Shape.Box)
        
        # Añadir layouts al layout principal
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.chart_label)
        
        # Layouts secundarios en un grid
        grid_layout = QGridLayout()
        grid_layout.addLayout(control_layout, 0, 1)
        grid_layout.addLayout(stats_layout, 1, 1)
        
        main_layout.addLayout(grid_layout)
        
        self.setLayout(main_layout)
        
        # Iniciar el temporizador
        self.timer.start(1000)
        
    def load_image(self, image_path):
        # Cargar imagen con OpenCV
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        self.time_display.setText(self.time_left.toString("mm : ss"))
        if self.time_left == QTime(0, 0, 0):
            self.timer.stop()
        
    def finish_procedure(self):
        self.timer.stop()
        self.time_display.setText("00 : 00")
        print("Procedimiento terminado.")

# Configuración de la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
