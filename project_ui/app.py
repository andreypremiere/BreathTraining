from PyQt6.QtWidgets import QApplication, QVBoxLayout, QStackedWidget, QWidget
from JWT_Provider.jwt_provider import JWTProvider
from login_form.login import Login
import sys
from register_form.registration import Registration


class MainWindow(QWidget):
    """Главный класс приложения, который управляет переключением между окнами с использованием QStackedWidget.

    Этот класс предоставляет основной интерфейс приложения, который позволяет пользователю переключаться
    между окнами для входа и регистрации. Он также использует JWTProvider для работы с JWT токеном.
    """

    def __init__(self, jwt):
        """
        Инициализация главного окна приложения.

        Метод инициализирует окно и вызывает метод для настройки пользовательского интерфейса.

        :param jwt: Объект для работы с JWT токенами.
        """
        super().__init__()
        self.registration_window = None  # Ссылка на окно регистрации
        self.login_window = None  # Ссылка на окно входа
        self.stacked_widget = None  # QStackedWidget для управления окнами
        self.jwt_provider = jwt  # Провайдер для работы с JWT
        self.init_ui(self.jwt_provider)  # Инициализация UI с использованием jwt

    def init_ui(self, jwt):
        """Настройка пользовательского интерфейса приложения.

        Создает окно с двумя вкладками: одно для входа, другое для регистрации. Для этих окон используется
        QStackedWidget для переключения между ними. Также создается макет с вертикальным расположением элементов.
        """
        self.setGeometry(725, 300, 400, 300)
        self.setWindowTitle("Тренажер дыхания")

        # Создаем QStackedWidget, который будет содержать различные окна
        self.stacked_widget = QStackedWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        # Создаем окна для входа и регистрации
        self.login_window = Login(jwt, self.switch_to_registration)
        self.registration_window = Registration(jwt, self.switch_to_login)

        # Добавляем окна в QStackedWidget
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.registration_window)

        # Устанавливаем начальное окно (окно входа)
        self.stacked_widget.setCurrentWidget(self.login_window)

    def switch_to_registration(self):
        """Переключает отображение окна регистрации.
        """
        self.stacked_widget.setCurrentWidget(self.registration_window)

    def switch_to_login(self):
        """Переключает отображение окна входа.
        """
        self.stacked_widget.setCurrentWidget(self.login_window)


if __name__ == "__main__":
    # Основной цикл приложения
    app = QApplication(sys.argv)
    window = None
    jwt_provider = JWTProvider()  # Создаем провайдер для работы с JWT

    # Проверяем наличие сохраненного токена
    if jwt_provider.load_token() is None:
        window = MainWindow(jwt_provider)

    window.show()
    sys.exit(app.exec())
