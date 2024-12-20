from PyQt6.QtWidgets import QMessageBox


def show_error_message(parent, error_message):
    """
    Отображение всплывающего окна с ошибкой.

    :param parent: Родительский объект, чтобы окно отображалось поверх него.
    :param error_message: Сообщение об ошибке, которое нужно показать пользователю.
    """
    error_box = QMessageBox(parent)
    # error_box.setIcon(QMessageBox.Icon.Critical)
    error_box.setWindowTitle("Ошибка")
    error_box.setInformativeText(error_message)  # Дополнительная информация об ошибке
    error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_box.exec()
