import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QGridLayout, QApplication)
from PyQt6.QtGui import QFont
from register_form.confirm_repeated_password import confirm_password
from register_form.requests_register import register_doctor


class Registration(QWidget):
    """
    Класс для окна регистрации.

    Этот класс представляет окно для регистрации нового пользователя, включая поля для ввода
    электронной почты, пароля и подтверждения пароля. Также добавлены кнопки для регистрации и
    возврата к окну входа.
    """

    def __init__(self, jwt_provider=0, switch_window_callback=0):
        """
        Инициализация окна регистрации.

        Создает интерфейс с полями для ввода электронной почты, пароля и подтверждения пароля.
        Сохраняет переданный объект для работы с JWT токенами и функцию для переключения на окно входа.

        :param jwt_provider: Объект для работы с JWT токенами.
        :param switch_window_callback: Функция для переключения на окно входа.
        """
        super().__init__()
        self.lastname_input = None
        self.name_input = None
        self.confirm_password_input = None  # Поле для подтверждения пароля
        self.email_input = None  # Поле для ввода электронной почты
        self.password_input = None  # Поле для ввода пароля
        # self.switch_window = switch_window_callback  # Колбек для переключения на окно входа
        self.jwt_provider = jwt_provider  # Объект для работы с JWT
        self.init_ui()  # Инициализация пользовательского интерфейса

    def init_ui(self):
        """
        Настройка пользовательского интерфейса окна регистрации.

        Создает заголовок, сетку для полей ввода электронной почты, пароля и подтверждения пароля,
        а также кнопки для регистрации и возврата к окну входа.
        """
        self.setStyleSheet("""
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #D5F8FF, stop: 1 #9BE6FF);
                """)

        layout = QVBoxLayout(self)  # Главный вертикальный макет
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        header_label = QLabel("Регистрация", self)
        header_label.setFont(QFont("Arial", 16))  # Установка шрифта для заголовка
        header_label.setStyleSheet("background-color: none;"
                                   "margin: 20px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрирование заголовка
        layout.addWidget(header_label)

        # Сетка для размещения полей ввода
        form_layout = QVBoxLayout()

        # Поле для ввода имени с плейсхолдером
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Введите имя")  # Устанавливаем плейсхолдер
        self.name_input.setFont(QFont("Arial", 10))  # Устанавливаем шрифт
        self.name_input.setStyleSheet("background-color: #FBFBFB;"
                                      "border-radius: 6px;"
                                      "border-style: none;")
        self.name_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.name_input)  # Объединяем столбцы

        # Поле для ввода фамилии с плейсхолдером
        self.lastname_input = QLineEdit(self)
        self.lastname_input.setPlaceholderText("Введите фамилию")
        self.lastname_input.setFont(QFont("Arial", 10))
        self.lastname_input.setStyleSheet("background-color: #FBFBFB;"
                                          "border-radius: 6px;"
                                          "border-style: none;")
        self.lastname_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.lastname_input)

        # Поле для ввода электронной почты с плейсхолдером
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Введите электронную почту")
        self.email_input.setFont(QFont("Arial", 10))
        self.email_input.setStyleSheet("background-color: #FBFBFB;"
                                       "border-radius: 6px;"
                                       "border-style: none;")
        self.email_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.email_input)

        # Поле для ввода пароля с плейсхолдером
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setFont(QFont("Arial", 10))
        self.password_input.setStyleSheet("background-color: #FBFBFB;"
                                          "border-radius: 6px;"
                                          "border-style: none;")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.password_input)

        # Поле для подтверждения пароля с плейсхолдером
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setFont(QFont("Arial", 10))
        self.confirm_password_input.setStyleSheet("background-color: #FBFBFB;"
                                                  "border-radius: 6px;"
                                                  "border-style: none;")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.confirm_password_input)

        layout.addLayout(form_layout)

        layout.addSpacing(10)
        # Кнопка регистрации
        register_button = QPushButton("Зарегистрироваться", self)
        register_button.setStyleSheet("background-color: #00B4D8;"
                                      "border-radius: 6px;"
                                      "border-style: none;")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #00B4D8;
                border-radius: 6px;
                border-style: none;
            }
            QPushButton:pressed {
                background-color: #009AB9;  /* Цвет при нажатии */
            }
        """)
        register_button.setFixedSize(200, 28)
        register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(10)

        back_label = QLabel('Уже есть аккаунт? <a style="color: black; text-decoration: underline;" href="#">Войти</a>',
                            self)
        back_label.setStyleSheet("background-color: none;")
        back_label.setFont(QFont("Arial", 10))
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setOpenExternalLinks(False)
        back_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        back_label.linkActivated.connect(self.switch_window)
        layout.addWidget(back_label)

        self.adjustSize()

        self.setFixedSize(self.size())

    def handle_register(self):
        name = self.name_input.text()
        password = self.password_input.text()
        lastname = self.lastname_input.text()
        email = self.email_input.text()

        if not confirm_password(password, self.confirm_password_input.text()):
            return None

        if (name or password or lastname or email) is None:
            return None

        result = register_doctor(name, lastname, email, password)

        if result['error'] is None:
            print('Пользователь успешно создан')
            # self.switch_window()  # Переключаем на другое окно
        else:
            print(result['error'])

    def switch_window(self):
        print('switch')


app = QApplication(sys.argv)
ventana = Registration()
ventana.show()
sys.exit(app.exec())
