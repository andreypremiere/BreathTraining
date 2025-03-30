import sys
from datetime import datetime

from PyQt6.QtCore import QPointF, Qt, QSize
from PyQt6.QtGui import QFont, QCursor, QColor, QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QGraphicsDropShadowEffect, QHBoxLayout, QFrame, QVBoxLayout, \
    QSizePolicy, QLabel, QApplication

from watching_procedure.requests_watching_procedure import get_procedure_by_proc_id
from watching_procedure.static_graph import StaticGraph


class WatchingProcedureWindow(QWidget):
    def __init__(self, manager=None, jwt_provider=None, patient=None, procedure=None):
        super().__init__()
        self.manager = manager
        self.jwt_provider = jwt_provider
        self.patient = patient
        self.procedure = procedure
        self.procedure_data = self.get_data_of_procedure()

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""background-color: #E5FBFF;""")
        self.setWindowTitle('Страница клиента')
        self.setGeometry(50, 30, 1400, 780)

        self.button_back = QPushButton("Назад", self)
        self.button_back.setFont(QFont("Arial", 14, 400))
        self.button_back.setStyleSheet("""
                                    QPushButton {
                                        background-color: #FFFFFF;
                                        border-radius: 8px;
                                        padding: 6px 10px;
                                    }
                                    QPushButton:pressed {
                                        background-color: #ADE8F4;
                                    }
                                """)
        self.button_back.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=self.button_back, blurRadius=20, color=QColor(0, 0, 0, 32),
                                      offset=QPointF(0, 0)))
        self.button_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_back.adjustSize()
        self.button_back.move(20, 20)
        self.button_back.clicked.connect(self.go_to_patient_window)

        # главный горизонтальный layout
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)


        main_frame = QFrame(self)
        main_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        main_frame.setMinimumWidth(600)
        main_frame.setMaximumWidth(900)
        # вертикальный лейаут
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_v_layout.setSpacing(25)

        # первый фрейм
        frame_information = QFrame(self)
        frame_information.setStyleSheet("""
                    background-color: #F0FDFF;
                    border-radius: 14px;
                """)
        frame_information.setMinimumWidth(500)
        frame_information.setMaximumWidth(900)
        frame_information.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=frame_information, blurRadius=20, color=QColor(0, 0, 0, 64),
                                      offset=QPointF(0, 0))
        )

        frame_information.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        label_name = QLabel(
            f"{self.patient['lastname']} {self.patient['name']} "
            f"{self.patient['surname'] if self.patient['surname'] else ''}",
            parent=frame_information)
        # label_name = QLabel(
        #     f"fsfsfsf "
        #     f"dfsfsdfdsfds",
        #     parent=frame_information)
        font = QFont("Arial", 14)
        font.setWeight(600)
        label_name.setFont(font)
        label_name.setMinimumWidth(360)
        label_date = QLabel(
            f"{self.patient['birthdate'] if self.patient['birthdate'] else 'Дата рождения отсутствует'}",
            parent=frame_information)
        # label_date = QLabel(
        #     f"fssdfsdfsdfsfsf",
        #     parent=frame_information)
        font = QFont("Arial", 12)
        font.setWeight(400)
        label_date.setFont(font)
        label_date.setMinimumWidth(360)
        label_desc = QLabel(
            f"Диагноз: {self.patient['diagnosis'] if self.patient['diagnosis'] else 'Диагноз отсутствует'}",
            parent=frame_information)
        # label_desc = QLabel(
        #     f"Диагноз: jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj jjjjjjjjjjjj jjjjjjj j    jjjjjjjj    jjjjjjjjjjj ",
        #     parent=frame_information)
        font = QFont("Arial", 10)
        font.setWeight(400)
        label_desc.setFont(font)
        label_desc.setMinimumWidth(360)
        label_desc.setWordWrap(True)
        label_desc.setMaximumWidth(400)

        information_patient_layout = QHBoxLayout(frame_information)
        information_patient_layout.setContentsMargins(20, 20, 20, 20)

        information_v_layout = QVBoxLayout(frame_information)
        information_v_layout.setSpacing(16)
        information_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        information_v_layout.addWidget(label_name)
        information_v_layout.addWidget(label_date)
        information_v_layout.addWidget(label_desc)

        button_edit_patient = QPushButton('', parent=frame_information)
        button_edit_patient.setFixedSize(54, 54)
        button_edit_patient.setStyleSheet("""
                               QPushButton {
                                   background-color: #FFFFFF;
                                   border-style: none;
                                   border-radius: 6px;  /* Круглая кнопка */
                               }
                               QPushButton:pressed {
                                   background-color: #009AB9;
                               }
                           """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)  # Радиус размытия
        shadow.setColor(QColor(0, 0, 0, 32))  # Полупрозрачная чёрная тень
        shadow.setOffset(0, 0)  # Смещение тени

        button_edit_patient.setGraphicsEffect(shadow)

        icon = QIcon('icons/edit_patient.svg')  # Загружаем иконку из файла
        button_edit_patient.setIcon(icon)
        button_edit_patient.setIconSize(button_edit_patient.size() - QSize(10, 10))
        button_edit_patient.setCursor(Qt.CursorShape.PointingHandCursor)


        information_patient_layout.addLayout(information_v_layout)
        information_patient_layout.addStretch()
        information_patient_layout.addWidget(button_edit_patient)
        frame_information.setLayout(information_patient_layout)

        # Фрейм графика
        self.widget_graph = StaticGraph(data=self.procedure_data, parent=self)

        main_v_layout.addWidget(frame_information, alignment=Qt.AlignmentFlag.AlignTop)
        main_v_layout.addWidget(self.widget_graph, alignment=Qt.AlignmentFlag.AlignTop)
        main_frame.setLayout(main_v_layout)

        main_layout.addWidget(main_frame)

        self.button_back.raise_()

    def go_to_patient_window(self):
        from patient_window.patient_window import PatientWindow
        self.manager.show_window(PatientWindow, patient=self.patient, jwt_provider=self.jwt_provider)

    def get_data_of_procedure(self):
        get_procedure_by_proc_id(self.procedure['procedure_id'])
        result = get_procedure_by_proc_id(self.procedure['procedure_id'])
        if len(result) > 0:
            try:
                result['timestamps'] = [datetime.fromisoformat(i) for i in result['timestamps']]
                result['created_at'] = datetime.fromisoformat(result['created_at'])

            except Exception as e:
                print(f'Ошибка преобразования: {e}')
        return result


# app = QApplication(sys.argv)
# window = WatchingProcedureWindow()
# window.show()
# sys.exit(app.exec())