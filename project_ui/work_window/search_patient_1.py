import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation


class SearchPatient(QWidget):
    def __init__(self, switch_window_callback=None):
        super().__init__()

        self.switch_window = switch_window_callback  # Función de cambio de ventana, si es necesario
        self.init_ui()

    def init_ui(self):
        # Configuración de la ventana principal
        self.setWindowTitle("Interfaz de Búsqueda")
        self.setGeometry(100, 100, 1000, 500)  # Posición y tamaño de la ventana
        self.setStyleSheet("background-color: #CAF0F8;")  # Color de fondo

        # Crear el layout principal
        self.layout_principal = QHBoxLayout(self)

        # --------- Panel Izquierdo (Lista de Pacientes) ----------
        panel_izquierdo = QVBoxLayout()
        panel_izquierdo.setContentsMargins(20, 20, 20, 20)

        # Título de la lista de usuarios
        label_lista = QLabel("Список найденных пользователей", self)
        label_lista.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        panel_izquierdo.addWidget(label_lista) #con esta funcion agregamos al panel izquierdo 

        # Lista de pacientes
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

        # Agregar elementos a la lista ejemplo
        usuarios = [
            ("Попов Ярослав Сергеевич", "Дата рождения: 22.08.2002"),
            ("Попов Ярослав Сергеевич", "Дата рождения: 22.08.1999"),
            ("Попов Ярослав Сергеевич", "Дата рождения: 22.08.2002"),
            ("Попов Ярослав Сергеевич", "Дата рождения: 22.08.2002")
        ]
        for nombre, fecha in usuarios:
            item = QListWidgetItem(f"{nombre}\n{fecha}")
            lista_usuarios.addItem(item)

        panel_izquierdo.addWidget(lista_usuarios)
        self.layout_principal.addLayout(panel_izquierdo)

        # --------- Panel Derecho (Caja de Búsqueda) ----------
        panel_derecho = QVBoxLayout()
        panel_derecho.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Crear la caja de búsqueda
        layout_busqueda = QVBoxLayout()
        cuadro_busqueda = QFrame(self)
        cuadro_busqueda.setStyleSheet("background-color: #B2EBF2; border-radius: 10px; padding: 20px;")
        layout_cuadro = QVBoxLayout(cuadro_busqueda)

        # Etiqueta de búsqueda
        etiqueta_busqueda = QLabel("Введите ФИО пользователя", self)
        layout_cuadro.addWidget(etiqueta_busqueda)

        # Campo de texto para ingresar la búsqueda
        campo_texto = QLineEdit(self)
        campo_texto.setPlaceholderText("Попов Яр")
        campo_texto.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #00838F;
                border-radius: 5px;
            }
        """)
        layout_cuadro.addWidget(campo_texto)

        # Botón de búsqueda
        boton_buscar = QPushButton("Найти", self)
        boton_buscar.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00838F;
            }
        """)
        boton_buscar.clicked.connect(lambda: self.handle_search(campo_texto.text()))  # Funcionalidad de búsqueda
        layout_cuadro.addWidget(boton_buscar)

        layout_busqueda.addWidget(cuadro_busqueda)
        panel_derecho.addLayout(layout_busqueda)
        self.layout_principal.addLayout(panel_derecho)

        
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
        self.layout_principal.addLayout(wrapper_right)

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
ventana = SearchPatient()
ventana.show()
sys.exit(app.exec())
