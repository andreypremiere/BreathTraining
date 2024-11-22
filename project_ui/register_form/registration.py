from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QGridLayout)
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

    def __init__(self, jwt_provider, switch_window_callback):
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

        name_label = QLabel("Имя:", self)
        name_label.setFont(QFont("Arial", 10))  # Установка шрифта для метки
        self.name_input = QLineEdit(self)  # Поле для ввода имени
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)

        # Метка и поле для ввода фамилии
        lastname_label = QLabel("Фамилия:", self)  # Исправлено с "Элек. почта" на "Фамилия"
        lastname_label.setFont(QFont("Arial", 10))  # Установка шрифта для метки
        self.lastname_input = QLineEdit(self)  # Поле для ввода фамилии
        form_layout.addWidget(lastname_label, 1, 0)  # Индекс строки изменен на 1
        form_layout.addWidget(self.lastname_input, 1, 1)  # Индекс строки изменен на 1

        # Метка и поле для ввода электронной почты
        email_label = QLabel("Элек. почта:", self)
        email_label.setFont(QFont("Arial", 10))  # Установка шрифта для метки
        self.email_input = QLineEdit(self)  # Поле для ввода электронной почты
        form_layout.addWidget(email_label, 2, 0)  # Индекс строки изменен на 2
        form_layout.addWidget(self.email_input, 2, 1)  # Индекс строки изменен на 2

        # Метка и поле для ввода пароля
        password_label = QLabel("Пароль:", self)
        password_label.setFont(QFont("Arial", 10))  # Установка шрифта для метки
        self.password_input = QLineEdit(self)  # Поле для ввода пароля
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Прячем пароль
        form_layout.addWidget(password_label, 3, 0)  # Индекс строки изменен на 3
        form_layout.addWidget(self.password_input, 3, 1)  # Индекс строки изменен на 3

        # Метка и поле для подтверждения пароля
        confirm_password_label = QLabel("Подтверждение пароля:", self)
        confirm_password_label.setFont(QFont("Arial", 10))
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(confirm_password_label, 4, 0)  # Индекс строки изменен на 4
        form_layout.addWidget(self.confirm_password_input, 4, 1)  # Индекс строки изменен на 4

        layout.addLayout(form_layout)

        # Кнопка регистрации
        register_button = QPushButton("Зарегистрироваться", self)
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)

        # Кнопка для возврата к окну входа
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.switch_window)
        layout.addWidget(back_button)

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
            self.switch_window()  # Переключаем на другое окно
        else:
            print(result['error'])

