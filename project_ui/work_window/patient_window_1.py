import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation

class PatientWindow(QWidget):
    def __init__(self, switch_window_callback=None):
        super().__init__()
        self.switch_window = switch_window_callback
        self.init_ui()

    def init_ui(self):
        # Ventana principal
        self.setWindowTitle("PATIENT DATA")
        self.setGeometry(100, 100, 1100, 700)
        self.setStyleSheet("background-color: #CAF0F8;")

        # Layout principal
        self.layout_principal_patients = QHBoxLayout(self)

        # Panel principal
        panel_data_patients = QVBoxLayout()
        panel_data_patients.setContentsMargins(180, 0, 180, 50)

        # Lista de pacientes
        label_lista = QLabel("Пациенты", self)
        label_lista.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        panel_data_patients.addWidget(label_lista)

        lista_usuarios = QListWidget(self)
        lista_usuarios.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #00796B;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #B2EBF2;
            }
        """)
        usuarios = [
            ("Попов Ярослав Сергеевич", "Дата рождения: 22.08.2002"),
            ("Иванов Иван Иванович", "Дата рождения: 15.03.1980"),
        ]
        for nombre, fecha in usuarios:
            item = QListWidgetItem(f"{nombre}\n{fecha}")
            lista_usuarios.addItem(item)
        panel_data_patients.addWidget(lista_usuarios)

        button_and_labels_layout = QHBoxLayout()


        # Botón "Начать процедуру"
        self.boton_start_process = QPushButton("Начать процедуру", self)
        self.boton_start_process.setStyleSheet(
            "padding: 30px 75px; font-size:16px; background-color: #0077B6; color: white;"
        )
        button_and_labels_layout.addWidget(self.boton_start_process)
        
        #agg spaced
        button_and_labels_layout.addStretch(1)
        
        # Elementos "Электронная карта" y "Статистика"
        label_electronic_cart = QLabel("Электронная карта", self)
        label_electronic_cart.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        button_and_labels_layout.addWidget(label_electronic_cart)

        label_stadistica = QLabel("Статистика", self)
        label_stadistica.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        button_and_labels_layout.addWidget(label_stadistica)
        
        # Añadir el layout con los botones y etiquetas al panel principal
        panel_data_patients.addLayout(button_and_labels_layout)
        
        # Historial médico
        label_historial = QLabel("История процедур", self)
        label_historial.setStyleSheet("font-size: 16px; font-weight: bold; padding: 1px;")
        panel_data_patients.addWidget(label_historial, alignment=Qt.AlignmentFlag.AlignLeft)

        historial_example = QListWidget(self)
        historial_example.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #00796B;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #B2EBF2;
            }
        """)
        historial_usuarios = [
            ("Процедура 1", "Дата: 22.08.2022"),
            ("Процедура 2", "Дата: 15.09.2022"),
            ("Процедура 3", "Дата: 10.10.2022"),
        ]
        for procedimiento, fecha in historial_usuarios:
            item = QListWidgetItem(f"{procedimiento}\n{fecha}")
            historial_example.addItem(item)
        panel_data_patients.addWidget(historial_example, alignment=Qt.AlignmentFlag.AlignLeft)

        # Añadir el panel al layout principal
        self.layout_principal_patients.addLayout(panel_data_patients)
        
        # --------- botones ----------
        wrapper_right = QVBoxLayout()
        wrapper_right.setContentsMargins(10, 0, 10, 0)  # Margen en los laterales derecho

        
        # Espaciado para centrar los botones verticalmente
        spacer = QVBoxLayout()
        spacer.addStretch(1)  # Añadir espacio flexible para empujar los botones hacia el centro
        wrapper_right.addLayout(spacer)

        # Botones (en la mitad de la parte derecha)
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)

        # Botón de usuario
        self.boton_usuario = QPushButton(self)
        self.boton_usuario.setStyleSheet("padding: 13px; font-size: 16px; background-color: #f2fffe; color: white;")
        self.boton_usuario.setIcon(QIcon("Icons/icon_user.svg"))
        button_layout.addWidget(self.boton_usuario)
        
        # Botón lista
        self.boton_panel_lista = QPushButton(self)
        self.boton_panel_lista.setStyleSheet("padding: 13px; font-size: 16px; background-color: #f2fffe; color: white;")
        self.boton_panel_lista.clicked.connect(self.toggle_panel_derecho)
        self.boton_panel_lista.setIcon(QIcon("Icons/icon_list_users.svg"))
        button_layout.addWidget(self.boton_panel_lista)

        # Botón de casa
        self.boton_home = QPushButton(self)
        self.boton_home.setStyleSheet("padding: 13px; font-size: 16px; background-color: #f2fffe; color: white;")
        self.boton_home.setIcon(QIcon("Icons\icon_home.svg"))
        button_layout.addWidget(self.boton_home)
        
        # Botón agregar paciente
        self.boton_add_pascient = QPushButton(self)
        self.boton_add_pascient.setStyleSheet("padding: 13px; font-size: 16px; background-color: #f2fffe; color: white;")
        self.boton_add_pascient.setIcon(QIcon("Icons/icon_add_user.svg"))
        button_layout.addWidget(self.boton_add_pascient)

        # Añadir los botones a la derecha en el layout
        wrapper_right.addLayout(button_layout)

        # Más espaciado para asegurar que los botones se mantengan centrados
        spacer2 = QVBoxLayout()
        spacer2.addStretch(1)  # Añadir espacio flexible después de los botones
        wrapper_right.addLayout(spacer2)

        # Añadir el wrapper_right al layout principal
        self.layout_principal_patients.addLayout(wrapper_right)

        # Panel deslizante (oculto inicialmente)
        self.panel_derecho = QFrame(self)
        self.panel_derecho.setGeometry(self.width(), 0, 300, self.height())  # Fuera de la vista inicial
        self.panel_derecho.setStyleSheet("background-color: #f2fffe; border-left: 2px solid #00796B;")

        layout_panel = QVBoxLayout(self.panel_derecho)
        label_titulo = QLabel("Список недавних посещений", self.panel_derecho)
        label_titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout_panel.addWidget(label_titulo)

        boton_cerrar = QPushButton("Close list", self.panel_derecho)
        boton_cerrar.clicked.connect(self.toggle_panel_derecho)
        layout_panel.addWidget(boton_cerrar)
        layout_panel.addStretch()

        self.panel_visible = False

    def toggle_panel_derecho(self):
        if self.panel_visible:
            animacion = QPropertyAnimation(self.panel_derecho, b"geometry")
            animacion.setDuration(300)
            animacion.setStartValue(QRect(self.width() - 300, 0, 300, self.height()))
            animacion.setEndValue(QRect(self.width(), 0, 300, self.height()))
            animacion.start()
        else:
            animacion = QPropertyAnimation(self.panel_derecho, b"geometry")
            animacion.setDuration(300)
            animacion.setStartValue(QRect(self.width(), 0, 300, self.height()))
            animacion.setEndValue(QRect(self.width() - 300, 0, 300, self.height()))
            animacion.start()
        self.panel_visible = not self.panel_visible

    def handle_search(self, query):
        print(f"Buscando: {query}")

app = QApplication(sys.argv)
ventana = PatientWindow()
ventana.show()
sys.exit(app.exec())
