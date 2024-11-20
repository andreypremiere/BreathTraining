from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QGridLayout)
from PyQt6.QtGui import QFont


class Registration(QWidget):
    """
    Класс для окна регистрации.

    Этот класс представляет окно для регистрации нового пользователя, включая поля для ввода
    электронной почты, пароля и подтверждения пароля. Также добавлены кнопки для регистрации и
    возврата к окну входа.
    """

    def __init__(self, jwt_provider, switch_window_callback):
        """
        Инициализация окна регистрации.

        Создает интерфейс с полями для ввода электронной почты, пароля и подтверждения пароля.
        Сохраняет переданный объект для работы с JWT токенами и функцию для переключения на окно входа.

        :param jwt_provider: Объект для работы с JWT токенами.
        :param switch_window_callback: Функция для переключения на окно входа.
        """
        super().__init__()
        self.confirm_password_input = None  # Поле для подтверждения пароля
        self.email_input = None  # Поле для ввода электронной почты
        self.password_input = None  # Поле для ввода пароля
        self.switch_window = switch_window_callback  # Колбек для переключения на окно входа
        self.jwt_provider = jwt_provider  # Объект для работы с JWT
        self.init_ui()  # Инициализация пользовательского интерфейса

    def init_ui(self):
        """
        Настройка пользовательского интерфейса окна регистрации.

        Создает заголовок, сетку для полей ввода электронной почты, пароля и подтверждения пароля,
        а также кнопки для регистрации и возврата к окну входа.
        """
        layout = QVBoxLayout(self)  # Главный вертикальный макет

        # Заголовок
        header_label = QLabel("Регистрация", self)
        header_label.setFont(QFont("Arial", 16))  # Установка шрифта для заголовка
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрирование заголовка
        layout.addWidget(header_label)

        # Сетка для полей ввода
        form_layout = QGridLayout()  # Сетка для размещения полей ввода

        # Метка и поле для ввода электронной почты
        email_label = QLabel("Элек. почта:", self)
        email_label.setFont(QFont("Arial", 10))  # Установка шрифта для метки
        self.email_input = QLineEdit(self)  # Поле для ввода электронной почты
        form_layout.addWidget(email_label, 0, 0)
        form_layout.addWidget(self.email_input, 0, 1)

        # Метка и поле для ввода пароля
        password_label = QLabel("Пароль:", self)
        password_label.setFont(QFont("Arial", 10))  # Установка шрифта для метки
        self.password_input = QLineEdit(self)  # Поле для ввода пароля
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Прячем пароль
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        # Метка и поле для подтверждения пароля
        confirm_password_label = QLabel("Подтверждение пароля:", self)
        confirm_password_label.setFont(QFont("Arial", 10))
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(confirm_password_label, 2, 0)
        form_layout.addWidget(self.confirm_password_input, 2, 1)

        layout.addLayout(form_layout)

        # Кнопка регистрации
        register_button = QPushButton("Зарегистрироваться", self)
        layout.addWidget(register_button)

        # Кнопка для возврата к окну входа
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.switch_window)
        layout.addWidget(back_button)
