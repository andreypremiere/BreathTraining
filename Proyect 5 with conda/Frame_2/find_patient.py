import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration of the main window
        self.setWindowTitle("Interfaz de Búsqueda")
        self.setGeometry(100, 100, 800, 500)  # Window position and size
        self.setStyleSheet("background-color: #E0F7FA;")  # Window background color

        # Create the main layout
        layout_principal = QHBoxLayout(self)

        # --------- Left Panel (List of Users) ----------
        panel_izquierdo = QVBoxLayout()
        panel_izquierdo.setContentsMargins(20, 20, 20, 20)

        #  Title of the user list
        label_lista = QLabel("Список найденных пользователей")
        label_lista.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        panel_izquierdo.addWidget(label_lista)

        # Users list
        lista_usuarios = QListWidget()
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

        # Add items in the list
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

        # Add the left panel to the main layout
        layout_principal.addLayout(panel_izquierdo)

        # --------- Right Panel (Search Box) ----------
        panel_derecho = QVBoxLayout()
        panel_derecho.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a text input box to search for users
        layout_busqueda = QVBoxLayout()
        cuadro_busqueda = QFrame()
        cuadro_busqueda.setStyleSheet("background-color: #B2EBF2; border-radius: 10px; padding: 20px;")
        layout_cuadro = QVBoxLayout(cuadro_busqueda)

        # Label “Enter name”.
        etiqueta_busqueda = QLabel("Введите ФИО пользователя")
        layout_cuadro.addWidget(etiqueta_busqueda)

        # Text field
        campo_texto = QLineEdit()
        campo_texto.setPlaceholderText("Попов Яр")
        campo_texto.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #00838F;
                border-radius: 5px;
            }
        """)
        layout_cuadro.addWidget(campo_texto)

        # Search button
        boton_buscar = QPushButton("Найти")
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
        layout_cuadro.addWidget(boton_buscar)

        layout_busqueda.addWidget(cuadro_busqueda)
        panel_derecho.addLayout(layout_busqueda)

        # Add the right panel to the main layout
        layout_principal.addLayout(panel_derecho)

        # --------- Button Panel with Icons (Right) ----------
        panel_botones = QVBoxLayout()
        panel_botones.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_botones.setContentsMargins(10, 20, 20, 20)

        # Buttons with icons (user and list icon) . ADD img ICONS
        icono_usuario = QPushButton()
        icono_usuario.setIcon(QIcon("user_icon.png"))  #  'user_icon.png' it's a example 
        icono_usuario.setIconSize(icono_usuario.sizeHint())
        icono_usuario.setFixedSize(40, 40)
        icono_usuario.setStyleSheet("border: none; background-color: transparent;")

        icono_lista = QPushButton()
        icono_lista.setIcon(QIcon("list_icon.png")) #  'user_icon.png' it's a example
        icono_lista.setIconSize(icono_lista.sizeHint())
        icono_lista.setFixedSize(40, 40)
        icono_lista.setStyleSheet("border: none; background-color: transparent;")

        panel_botones.addWidget(icono_usuario)
        panel_botones.addWidget(icono_lista)

        # Add button panel to the main layout
        layout_principal.addLayout(panel_botones)


# Create the PyQt6 application
app = QApplication(sys.argv)

# Create a window
ventana = MainWindow()
ventana.show()

# Running the application
sys.exit(app.exec())
