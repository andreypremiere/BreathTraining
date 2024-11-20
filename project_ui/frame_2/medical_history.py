import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame,
    QGridLayout, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration of the main window
        self.setWindowTitle("Detalles del Paciente")
        self.setGeometry(100, 100, 800, 500)  # Position and size of the window
        self.setStyleSheet("background-color: #E0F7FA;")  # Window background color

        # Horizontal main layout
        layout_principal = QHBoxLayout(self)

        # --------- Central Panel ---------
        panel_central = QVBoxLayout()

        # Patient information (top)
        info_paciente = QFrame()
        info_paciente.setStyleSheet("background-color: #B2EBF2; border-radius: 10px; padding: 15px;")
        layout_info = QVBoxLayout(info_paciente)
        
        #Only text example
        label_nombre = QLabel("Иванов Иван Иванович")
        label_nombre.setStyleSheet("font-size: 18px; font-weight: bold;")
        label_fecha = QLabel("Дата рождения: 12.09.2000    Возраст: 2000")
        label_diagnostico = QLabel(
            "Диагноз: Очень длинное описание диагноза, которое бывает очень длинным и предлинным, что может не поместиться во многие блоки"
        )
        label_diagnostico.setWordWrap(True)

        layout_info.addWidget(label_nombre)
        layout_info.addWidget(label_fecha)
        layout_info.addWidget(label_diagnostico)

        panel_central.addWidget(info_paciente)

        # Botom "Начать процедуру"
        boton_procedimiento = QPushButton("Начать процедуру")
        boton_procedimiento.setStyleSheet("""
            QPushButton {
                background-color: #00ACC1;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #00838F;
            }
        """)
        boton_procedimiento.setFixedHeight(50)
        panel_central.addWidget(boton_procedimiento)

        # Box with buttons "Электронная карта"
        frame_carta = QFrame()
        frame_carta.setStyleSheet("background-color: #E0F2F1; border-radius: 10px; padding: 10px;")
        layout_carta = QHBoxLayout(frame_carta)
        
        
        #button dowload
        boton_descargar = QPushButton("Скачать")
        boton_cargar = QPushButton("Загрузить") #button charge 
        for boton in (boton_descargar, boton_cargar):
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #B2EBF2;
                    color: black;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #80DEEA;
                }
            """)
            boton.setFixedWidth(100)
        
        layout_carta.addWidget(boton_descargar)
        layout_carta.addWidget(boton_cargar)
        panel_central.addWidget(frame_carta)

        # Add central panel to the main layout
        layout_principal.addLayout(panel_central)

        # --------- Lower Left Panel (Procedure History) ---------
        panel_historia = QVBoxLayout()
        panel_historia.setAlignment(Qt.AlignmentFlag.AlignTop)

        frame_historia = QFrame()
        frame_historia.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; padding: 10px;")
        layout_historia = QVBoxLayout(frame_historia)
        
        label_historia = QLabel("История процедур")
        label_historia.setStyleSheet("font-size: 16px; font-weight: bold; padding-bottom: 10px;")
        layout_historia.addWidget(label_historia)

        # List of procedures
        lista_historia = QListWidget()
        lista_historia.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #B2EBF2;
            }
        """)
        #example list 
        procedimientos = [
            "8  Дата: 29.09.2000   Продолжительность: 29.09.2000",
            "7  Дата: 29.09.2000   Продолжительность: 29.09.2000",
            "6  Дата: 29.09.2000   Продолжительность: 29.09.2000",
            "5  Дата: 29.09.2000   Продолжительность: 29.09.2000",
        ]
        for proc in procedimientos:
            item = QListWidgetItem(proc)
            lista_historia.addItem(item)

        layout_historia.addWidget(lista_historia)
        panel_historia.addWidget(frame_historia)

        # Add story panel to the main layout
        layout_principal.addLayout(panel_historia)

        # Right Panel (Statistics and icon buttons) 
        panel_derecho = QVBoxLayout()
        panel_derecho.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Statistics Table
        frame_estadisticas = QFrame()
        frame_estadisticas.setStyleSheet("background-color: #E0F2F1; border-radius: 10px; padding: 10px;")
        layout_estadisticas = QVBoxLayout(frame_estadisticas)

        label_estadisticas = QLabel("Статистика")
        label_estadisticas.setStyleSheet("font-size: 16px; font-weight: bold;")
        label_datos = QLabel("Разные данные: да\nЕще не придумал что: да\nПотом заполню: да")
        label_datos.setWordWrap(True)
        
        layout_estadisticas.addWidget(label_estadisticas)
        layout_estadisticas.addWidget(label_datos)
        panel_derecho.addWidget(frame_estadisticas)

        # Add spacer
        espaciador = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        panel_derecho.addItem(espaciador)

        # Add the right panel to the main layout
        layout_principal.addLayout(panel_derecho)


# Crear la aplicación PyQt6
app = QApplication(sys.argv)

# Crear una ventana
ventana = MainWindow()
ventana.show()

# Ejecutar la aplicación
sys.exit(app.exec())
