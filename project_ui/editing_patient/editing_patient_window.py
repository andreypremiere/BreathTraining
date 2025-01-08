import datetime
import sys

from PyQt6.QtCore import Qt, QPointF, QDate
from PyQt6.QtGui import QColor, QFont, QCursor
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFrame, QSizePolicy, QGraphicsDropShadowEffect, QLabel, \
    QLineEdit, QHBoxLayout, QDateEdit, QAbstractSpinBox, QComboBox, QTextEdit, QPushButton

from editing_patient.date_services import date_to_qdate, qdate_to_date
from editing_patient.requests_editing_patient import create_new_patient


def generate_item(place_holder, max_width, patient=None, key=None):
    frame_item = QFrame()
    frame_item.setStyleSheet('padding: 0px;'
                             'border-radius: 0px;')
    frame_item.setMaximumWidth(max_width)
    frame_layout = QVBoxLayout(frame_item)
    frame_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    frame_item.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    label = QLabel(place_holder, frame_item)
    label.setContentsMargins(8, 0, 0, 0)
    label.setFont(QFont('Arial', 12, 400))
    frame_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
    input_field = QLineEdit(frame_item)
    input_field.setFont(QFont('Arial', 11, 400))
    if key == 'number_phone':
        input_field.setInputMask("+7 (999) 999-99-99;_")  # Маска для формата номера

    if patient is not None:
        input_field.setText(patient[key])
    input_field.setStyleSheet("""
        QLineEdit {
            background-color: #FFFFFF;
            border: none;           
            border-radius: 8px;     
            padding: 6px 10px;        
        }
    """)
    input_field.setGraphicsEffect(QGraphicsDropShadowEffect(parent=input_field, blurRadius=10, color=QColor(0, 0, 0, 16),
                                  offset=QPointF(0, 0)))
    # input_field.setMaximumWidth(max_width)
    input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    if patient:
        input_field.setText(patient[key])
    frame_layout.addWidget(input_field)
    return {'frame': frame_item, 'input_field': input_field}


class EditingPatient(QWidget):
    def __init__(self, manager=None, jwt_provider=None, patient=None):
        super().__init__()

        self.manager = manager
        self.jwt_provider = jwt_provider
        self.patient = patient
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""background-color: #E5FBFF;""")
        self.setWindowTitle('Страница пациента')
        self.setGeometry(50, 30, 1400, 780)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.main_frame = QFrame(self)
        self.main_frame.setStyleSheet("""
            background-color: #F0FDFF;
            border-radius: 20px;
        """)
        self.main_frame.setMaximumWidth(900)
        self.main_frame.setMinimumWidth(600)
        self.main_frame.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=self.main_frame, blurRadius=20, color=QColor(0, 0, 0, 64),
                                      offset=QPointF(0, 0)))
        self.main_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.frame_layout = QVBoxLayout(self.main_frame)
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Первая строка
        self.first_row = QHBoxLayout(self.main_frame)
        self.first_row.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.last_name_field = generate_item('Фамилия', 300, patient=self.patient, key='lastname')
        self.name_field = generate_item('Имя', 300, patient=self.patient, key='name')
        self.surname = generate_item('Отчество', 300, patient=self.patient, key='surname')

        self.first_row.addWidget(self.last_name_field['frame'])
        self.first_row.addWidget(self.name_field['frame'])
        self.first_row.addWidget(self.surname['frame'])

        self.frame_layout.addLayout(self.first_row)

        # Вторая строка
        self.second_row = QHBoxLayout(self.main_frame)
        self.second_row.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.email = generate_item('Электронная почта', 400,  patient=self.patient, key='email')
        self.number_phone = generate_item('Номер телефона', 400, patient=self.patient, key='number_phone')
        # print(self.number_phone['input_field'].text() == '+7 () --')

        self.second_row.addWidget(self.email['frame'])
        self.second_row.addWidget(self.number_phone['frame'])

        self.frame_layout.addLayout(self.second_row)

        # Третья строка
        self.third_row = QHBoxLayout(self.main_frame)
        self.third_row.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # Фрейм даты
        self.frame_date = QFrame()
        self.frame_date.setStyleSheet('padding: 0px;'
                                 'border-radius: 0px;')
        # self.frame_date.setMaximumWidth(max_width)
        date_layout = QVBoxLayout(self.frame_date)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.frame_date.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        label_date = QLabel('Дата рождения', self.frame_date)
        label_date.setContentsMargins(8, 0, 0, 0)
        label_date.setFont(QFont('Arial', 12, 400))
        date_layout.addWidget(label_date, alignment=Qt.AlignmentFlag.AlignLeft)
        self.date_edit = QDateEdit()
        self.date_edit.setFont(QFont('Arial', 12, 400))
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setDate(date_to_qdate(self.patient['birthdate']) if self.patient is not None else QDate(1792, 9, 14))
        # print(qdate_to_date(self.date_edit.date()) == datetime.date(1792, 9, 14))
        self.date_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)  # Убираем стрелочки
        self.date_edit.setStyleSheet("""
                    QDateEdit {
                        background-color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 6px 10px;
                    }
        """)
        self.date_edit.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=self.date_edit, blurRadius=10, color=QColor(0, 0, 0, 16),
                                      offset=QPointF(0, 0)))
        date_layout.addWidget(self.date_edit, alignment=Qt.AlignmentFlag.AlignLeft)
        self.frame_date.setLayout(date_layout)

        self.third_row.addWidget(self.frame_date, alignment=Qt.AlignmentFlag.AlignLeft)

        # фрейм выбора пола
        self.frame_male = QFrame()
        self.frame_male.setStyleSheet('padding: 0px;'
                                      'border-radius: 0px;')
        # self.frame_date.setMaximumWidth(max_width)
        male_layout = QVBoxLayout(self.frame_male)
        male_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.frame_male.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        label_male = QLabel('Пол', self.frame_male)
        label_male.setContentsMargins(8, 0, 0, 0)
        label_male.setFont(QFont('Arial', 12, 400))
        male_layout.addWidget(label_male, alignment=Qt.AlignmentFlag.AlignLeft)
        self.dropdown = QComboBox()
        self.dropdown.setFont(QFont('Arial', 12, 400))
        self.dropdown.setStyleSheet("""
                    QComboBox {
                        background-color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 6px 10px;
                    }
                """)
        self.dropdown.addItems(["Не установлен", "Мужской", "Женский"])  # Добавляем элементы в список
        if self.patient is not None:
            if self.patient['gender'] == 'male':
                self.dropdown.setCurrentIndex(1)
            else:
                self.dropdown.setCurrentIndex(2)

        self.dropdown.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=self.dropdown, blurRadius=10, color=QColor(0, 0, 0, 16),
                                      offset=QPointF(0, 0)))
        male_layout.addWidget(self.dropdown, alignment=Qt.AlignmentFlag.AlignLeft)
        self.frame_male.setLayout(male_layout)

        self.third_row.addWidget(self.frame_male, alignment=Qt.AlignmentFlag.AlignLeft)

        self.frame_layout.addLayout(self.third_row)

        # Конец третьей строки

        # Диагноз
        fourth_row = QHBoxLayout(self.main_frame)
        fourth_row.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.frame_diagnosis = QFrame()
        self.frame_diagnosis.setStyleSheet('padding: 0px;'
                                      'border-radius: 0px;')
        # self.frame_date.setMaximumWidth(max_width)
        diagnosis_layout = QVBoxLayout(self.frame_diagnosis)
        diagnosis_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.frame_diagnosis.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        label_diagnosis = QLabel('Диагноз', self.frame_male)
        label_diagnosis.setContentsMargins(8, 0, 0, 0)
        label_diagnosis.setFont(QFont('Arial', 12, 400))
        diagnosis_layout.addWidget(label_diagnosis, alignment=Qt.AlignmentFlag.AlignLeft)

        self.text_edit = QTextEdit()
        if self.patient is not None:
            self.text_edit.setText(self.patient["diagnosis"])
        self.text_edit.setFont(QFont('Arial', 12, 400))
        self.text_edit.setMaximumHeight(160)
        # self.text_edit.setText("Введите текст...")  # Установка начального текста
        self.text_edit.setStyleSheet("""
                    QTextEdit {
                        background-color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 6px 10px;
                    }
                """)
        self.text_edit.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=self.dropdown, blurRadius=10, color=QColor(0, 0, 0, 16),
                                      offset=QPointF(0, 0)))
        diagnosis_layout.addWidget(self.text_edit)

        self.frame_diagnosis.setLayout(diagnosis_layout)
        fourth_row.addWidget(self.frame_diagnosis, alignment=Qt.AlignmentFlag.AlignTop)

        self.frame_layout.addLayout(fourth_row)

        # Кнопки
        buttons_layout = QHBoxLayout(self.main_frame)
        buttons_layout.setContentsMargins(8, 0, 0, 10)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Кнопка назад
        self.button_back = QPushButton("Отмена", self)
        self.button_back.setFont(QFont("Arial", 14, 400))
        self.button_back.setStyleSheet("""
                                    QPushButton {
                                        background-color: none;
                                        border-radius: 8px;
                                        padding: 4px 8px;
                                        border: 1px solid #3A3A3A;  /* Указываем тип рамки (solid) */
                                    }
                                    QPushButton:pressed {
                                        background-color: #0096C7;
                                    }
                                """)
        self.button_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_back.clicked.connect(self.go_to_back)
        self.button_back.adjustSize()
        buttons_layout.addWidget(self.button_back)

        # Кнопка сохранить
        # Кнопка назад
        self.button_save = QPushButton("Сохранить", self)
        self.button_save.setFont(QFont("Arial", 14, 400))
        self.button_save.setStyleSheet("""
                                            QPushButton {
                                                background-color: #ADE8F4;
                                                border-radius: 8px;
                                                padding: 6px 10px;
                                                border: none; 
                                            }
                                            QPushButton:pressed {
                                                background-color: #0096C7;
                                            }
                                        """)
        self.button_save.setGraphicsEffect(
            QGraphicsDropShadowEffect(parent=self.dropdown, blurRadius=10, color=QColor(0, 0, 0, 16),
                                      offset=QPointF(0, 0)))
        self.button_save.clicked.connect(self.collect_and_send_data)
        self.button_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_save.adjustSize()

        buttons_layout.addWidget(self.button_save)

        self.frame_layout.addLayout(buttons_layout)

        self.main_frame.setLayout(self.frame_layout)
        self.main_layout.addWidget(self.main_frame)
        self.setLayout(self.main_layout)

    def collect_and_send_data(self):
        patient = {}
        patient['lastname'] = self.last_name_field['input_field'].text()
        patient['name'] = self.name_field['input_field'].text()
        patient['surname'] = self.surname['input_field'].text()
        patient['email'] = self.email['input_field'].text()
        number_phone = self.number_phone['input_field'].text()
        if number_phone != '+7 () --':
            patient['number_phone'] = number_phone
        birthdate = self.date_edit.date()
        if birthdate != datetime.date(1792, 9, 14):
            patient['birthdate'] = qdate_to_date(birthdate).isoformat()
        gender = self.dropdown.currentText()
        if gender == 'Мужской':
            patient['gender'] = 'male'
        elif gender == 'Женский':
            patient['gender'] = 'female'
        patient['diagnosis'] = self.text_edit.toPlainText() if self.text_edit.toPlainText() != '' or ' ' else None
        patient['is_active'] = True

        patient_id = create_new_patient(patient)

        if patient_id is not None:
            from login_form.login import Login
            from search_patient.search_window import SearchPatient
            self.manager.show_window(SearchPatient, jwt_provider=self.jwt_provider, login=Login)

        # if patient_id is not None:
        #     patient['patient_id'] = patient_id
        #
        #     from patient_window.patient_window import PatientWindow
        #     self.manager.show_window(PatientWindow, patient=patient, jwt_provider=self.jwt_provider)

    def go_to_back(self):
        from login_form.login import Login
        from search_patient.search_window import SearchPatient
        self.manager.show_window(SearchPatient, jwt_provider=self.jwt_provider, login=Login)


#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ventana = EditingPatient()
#     ventana.show()
#     sys.exit(app.exec())