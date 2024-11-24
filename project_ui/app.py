from PyQt6.QtWidgets import QApplication, QVBoxLayout, QStackedWidget, QWidget
from JWT_Provider.jwt_provider import JWTProvider
from login_form.login import Login
import sys
from register_form.registration import Registration
from work_window.work_window import WorkWindow


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
        self.work_window = None
        self.registration_window = None  # Ссылка на окно регистрации
        self.login_window = None  # Ссылка на окно входа
        self.stacked_widget = None  # QStackedWidget для управления окнами
        self.jwt_provider = jwt  # Провайдер для работы с JWT
        self.init_ui()  # Инициализация UI с использованием jwt

    def init_ui(self):
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
        self.login_window = Login(self.jwt_provider, self.switch_to_registration, self.switch_to_work_window)
        self.registration_window = Registration(self.jwt_provider, self.switch_to_login)
        self.work_window = WorkWindow(self.jwt_provider)

        # Добавляем окна в QStackedWidget
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.registration_window)
        self.stacked_widget.addWidget(self.work_window)

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

    def switch_to_work_window(self):
        self.stacked_widget.setCurrentWidget(self.work_window)


if __name__ == "__main__":
    # Основной цикл приложения
    app = QApplication(sys.argv)
    jwt_provider = JWTProvider()  # Создаем провайдер для работы с JWT
    window = MainWindow(jwt_provider)

    # Проверяем наличие сохраненного токена
    # if jwt_provider.load_token() is None:
    #     window = MainWindow(jwt_provider)

    window.show()
    sys.exit(app.exec())
