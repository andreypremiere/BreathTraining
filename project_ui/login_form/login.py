import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QGridLayout,
                             QVBoxLayout)
from PyQt6.QtGui import QFont
from login_form.reguests_login import login_doctor


class Login(QWidget):
    """
    Класс для окна входа.

    Этот класс представляет окно входа пользователя в приложение, включая поля для ввода
    электронной почты и пароля, а также кнопки для входа и регистрации.
    При успешной авторизации токен сохраняется, и происходит переход на другое окно.
    """

    def __init__(self, jwt_provider, switch_to_register, switch_to_work_window):
        """
        Инициализация окна входа.

        Создает интерфейс с полями для ввода, кнопками и функционалом для переключения
        на окно регистрации. Также сохраняет переданный объект для работы с JWT токенами.

        :param jwt_provider: Объект для работы с JWT токенами.
        :param switch_to_register: Функция для переключения на окно регистрации.
        """
        super().__init__()
        self.switch_to_register = switch_to_register  # Колбек для переключения на окно регистрации
        self.jwt_provider = jwt_provider  # Объект для работы с JWT
        self.switch_to_work_window = switch_to_work_window
        self.init_ui()

    def init_ui(self):
        """
        Настройка пользовательского интерфейса окна входа.

        Создает заголовок, сетку для полей ввода электронной почты и пароля, а также кнопки
        для входа и регистрации. Добавляет чекбокс для показа пароля и настраивает макет.
        """
        layout = QVBoxLayout(self)  # Главный вертикальный макет

        # Заголовок
        header_label = QLabel("Вход", self)
        header_label.setFont(QFont("Arial", 16))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        # Сетка для полей ввода
        form_layout = QGridLayout()

        # Метка и поле для ввода электронной почты
        email_label = QLabel("Элек. почта:", self)
        email_label.setFont(QFont("Arial", 10))
        self.email_input = QLineEdit(self)
        form_layout.addWidget(email_label, 0, 0)
        form_layout.addWidget(self.email_input, 0, 1)

        # Метка и поле для ввода пароля
        password_label = QLabel("Пароль:", self)
        password_label.setFont(QFont("Arial", 10))
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        layout.addLayout(form_layout)  # Добавление сетки в основной макет

        # Чекбокс для отображения пароля
        self.show_password_checkbox = QCheckBox("См. пароль", self)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        # Кнопка входа
        login_button = QPushButton("Войти", self)
        layout.addWidget(login_button)
        login_button.clicked.connect(lambda: self.handle_login(self.email_input.text(), self.password_input.text()))

        # Кнопка регистрации
        register_button = QPushButton("Зарегистрироваться", self)
        register_button.clicked.connect(self.switch_to_register)
        layout.addWidget(register_button)

    def toggle_password_visibility(self):
        """
        Показывать или скрывать пароль.

        Метод переключает режим отображения пароля в поле ввода пароля.
        Если чекбокс "См. пароль" выбран, пароль отображается в открытом виде,
        иначе - скрывается.
        """
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_login(self, email, password):
        """
        Обработка входа пользователя.

        Отправляет запрос на сервер для аутентификации пользователя, используя введенные
        электронную почту и пароль. Если вход успешен, сохраняет токен и переключает окно.

        :param email: Электронная почта пользователя.
        :param password: Пароль пользователя.
        """
        result = login_doctor(email, password)
        if result['error'] is None:
            print(f'Login successful: {result["body"]}')
            self.jwt_provider._token = result['body']
            self.switch_to_work_window()  # Переключаем на другое окно
        else:
            print(result['error'])
