from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame


class ClickableFrame(QFrame):
    def __init__(self, patient, callback, parent=None, add_to_recent=None):
        super().__init__(parent)
        self.patient = patient
        self.callback = callback
        self.add_to_recent = add_to_recent

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.add_to_recent(self.patient['patient_id'])
            self.callback(self.patient)


class ClickableProcedure(QFrame):
    def __init__(self, procedure, callback, parent=None):
        super().__init__(parent)
        self.procedure = procedure
        self.callback = callback

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback(self.procedure)

