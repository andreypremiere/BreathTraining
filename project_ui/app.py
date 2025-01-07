import sys

from PyQt6.QtWidgets import (
    QApplication
)

from login_form.login import Login


class WindowManager:
    def __init__(self):
        self.current_window = None

    def show_window(self, window, **kwargs):
        print(self.current_window)
        if self.current_window:
            print('Текущее окно:', window)
            if self.current_window.isVisible():
                self.current_window.close()
        self.current_window = window(manager=self, **kwargs)
        self.current_window.show()
        print('Показано окно:', self.current_window)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    manager = WindowManager()
    manager.show_window(Login)  # Окно входа

    sys.exit(app.exec())
