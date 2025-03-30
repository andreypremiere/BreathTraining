from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QVBoxLayout)
from PyQt6.QtGui import QFont

from JWT_Provider.jwt_provider import JWTProvider
from login_form.reguests_login import login_doctor
from register_form.registration import Registration
from search_patient.search_window import SearchPatient


class Login(QWidget):
    """
    Класс для окна входа.

    Этот класс представляет окно входа пользователя в приложение, включая поля для ввода
    электронной почты и пароля, а также кнопки для входа и регистрации.
    При успешной авторизации токен сохраняется, и происходит переход на другое окно.
    """

    def __init__(self, jwt_provider=None, manager=None, switch_to_register=0, switch_to_work_window=0):
        """
        Инициализация окна входа.

        Создает интерфейс с полями для ввода, кнопками и функционалом для переключения
        на окно регистрации. Также сохраняет переданный объект для работы с JWT токенами.

        :param jwt_provider: Объект для работы с JWT токенами.
        :param switch_to_register: Функция для переключения на окно регистрации.
        """
        super().__init__()
        # self.switch_to_register = switch_to_register  # Колбек для переключения на окно регистрации
        self.show_password_checkbox = None
        self.password_input = None
        self.email_input = None
        self.jwt_provider = jwt_provider if jwt_provider else JWTProvider()
        self.manager = manager
        # self.init_ui()
        if self.check_token():
            QTimer.singleShot(0, self.switch_to_work_window)
        self.init_ui()

    def init_ui(self):
        """
        Настройка пользовательского интерфейса окна входа.

        Создает заголовок, сетку для полей ввода электронной почты и пароля, а также кнопки
        для входа и регистрации. Добавляет чекбокс для показа пароля и настраивает макет.
        """
        self.setWindowTitle('Вход')
        self.setObjectName("LoginWindow")
        self.setStyleSheet("""
                    QWidget#LoginWindow {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #D5F8FF, stop: 1 #9BE6FF);
                    }
                """)

        layout = QVBoxLayout(self)  # Главный вертикальный макет
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        header_label = QLabel("Вход", self)
        header_label.setFont(QFont("Arial", 16))
        header_label.setStyleSheet("background-color: none;"
                                   "margin: 20px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрирование заголовка
        layout.addWidget(header_label)

        # Сетка для полей ввода
        form_layout = QVBoxLayout(self)

        # Метка и поле для ввода электронной почты
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")  # Устанавливаем плейсхолдер
        self.email_input.setFont(QFont("Arial", 10))  # Устанавливаем шрифт
        self.email_input.setStyleSheet("background-color: #FBFBFB;"
                                       "border-radius: 6px;"
                                       "border-style: none;")
        self.email_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.email_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Метка и поле для ввода пароля
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setFont(QFont("Arial", 10))
        self.password_input.setStyleSheet("background-color: #FBFBFB;"
                                          "border-radius: 6px;"
                                          "border-style: none;")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedSize(300, 28)  # ширина 200 пикселей, высота 30 пикселей
        form_layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(form_layout)

        # Чекбокс для отображения пароля
        self.show_password_checkbox = QCheckBox("См. пароль", self)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Кнопка входа
        layout.addSpacing(10)
        login_button = QPushButton("Войти", self)
        login_button.setStyleSheet("background-color: #00B4D8;"
                                   "border-radius: 6px;"
                                   "border-style: none;")
        login_button.setStyleSheet("""
                    QPushButton {
                        background-color: #00B4D8;
                        border-radius: 6px;
                        border-style: none;
                    }
                    QPushButton:pressed {
                        background-color: #009AB9;  /* Цвет при нажатии */
                    }
                """)
        login_button.setFixedSize(200, 28)
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.clicked.connect(lambda: self.handle_login(self.email_input.text(), self.password_input.text()))
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(10)

        register_button = QLabel('Нет аккаунта? <a style="color: black; '
                                 'text-decoration: underline;" '
                                 'href="#">Зарегистрироваться</a>',
                                 self)
        register_button.setStyleSheet("background-color: none;")
        register_button.setFont(QFont("Arial", 10))
        register_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_button.setOpenExternalLinks(False)
        register_button.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        register_button.linkActivated.connect(self.switch_to_register)
        layout.addWidget(register_button)

    def switch_to_register(self):
        self.manager.show_window(Registration, login=type(self))

    def switch_to_work_window(self):
        self.manager.show_window(SearchPatient, jwt_provider=self.jwt_provider, login=type(self))

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
            self.jwt_provider.save_token()
            self.switch_to_work_window()  # Переключаем на другое окно
        else:
            print(result['error'])

    def check_token(self):
        self.jwt_provider.load_token()
        if self.jwt_provider.is_token_valid():
            return True
        return False




# app = QApplication(sys.argv)
# ventana = Login()
# ventana.show()
# sys.exit(app.exec())
