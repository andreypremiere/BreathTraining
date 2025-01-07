import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor
from PyQt6.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel, QVBoxLayout, QFrame, QPushButton, \
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea

from additional_widget.clickable_frame import ClickableProcedure
from patient_window.requests_patient_window import get_procedures_of_patient
from work_windows.work_window import WorkWindow


class PatientWindow(QWidget):
    def __init__(self, manager, patient, jwt_provider):
        super().__init__()

        self.manager = manager
        self.patient = patient
        self.jwt_provider = jwt_provider
        self.procedures_list = self.get_procedures_of_patient()
        self.button1 = None
        self.left_panel_layout = None
        self.input_lastname_patient = None
        self.button_search_patient = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""background-color: #E5FBFF;""")
        self.setWindowTitle('Страница клиента')
        self.setGeometry(50, 30, 1400, 780)

        # главный горизонтальный layout
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        frame_information.setMinimumWidth(400)
        frame_information.setMaximumWidth(660)
        shadow = QGraphicsDropShadowEffect(parent=frame_information)
        shadow.setBlurRadius(20)  # Радиус размытия тени
        shadow.setColor(QColor(0, 0, 0, 64))  # Чёрная тень с прозрачностью
        shadow.setOffset(0, 0)  # Смещение тени по X и Y

        frame_information.setGraphicsEffect(shadow)
        frame_information.setSizePolicy(
            frame_information.sizePolicy().horizontalPolicy().Expanding,  # Оставляем ширину неизменной
            frame_information.sizePolicy().verticalPolicy().Preferred  # Высота подстраивается
        )

        label_name = QLabel(
            f"{self.patient['lastname']} {self.patient['name']} "
            f"{self.patient['surname'] if self.patient['surname'] else ''}",
            parent=frame_information)
        font = QFont("Arial", 14)
        font.setWeight(600)
        label_name.setFont(font)
        label_name.setMinimumWidth(360)
        label_date = QLabel(f"{self.patient['birthdate'] if self.patient['birthdate'] else 'Дата рождения отсутствует'}",
                            parent=frame_information)
        font = QFont("Arial", 12)
        font.setWeight(400)
        label_date.setFont(font)
        label_date.setMinimumWidth(360)
        label_desc = QLabel(f"{self.patient['diagnosis'] if self.patient['diagnosis'] else 'Диагноз отсутствует'}",
                            parent=frame_information)
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
        button_edit_patient.setCursor(Qt.CursorShape.PointingHandCursor)
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

        information_patient_layout.addLayout(information_v_layout)
        information_patient_layout.addStretch()
        information_patient_layout.addWidget(button_edit_patient)

        # frame для нижней панели
        lower_frame = QFrame(self)
        # lower_frame.setContentsMargins(0, 0, 0, 0)
        lower_frame.setStyleSheet("""
                    background-color: none;
                    border-radius: 14px;
                """)
        lower_frame.setMaximumWidth(660)
        shadow = QGraphicsDropShadowEffect(parent=frame_information)
        shadow.setBlurRadius(20)  # Радиус размытия тени
        shadow.setColor(QColor(0, 0, 0, 64))  # Чёрная тень с прозрачностью
        shadow.setOffset(0, 0)  # Смещение тени по X и Y

        lower_frame.setGraphicsEffect(shadow)

        size_policy = lower_frame.sizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        lower_frame.setSizePolicy(size_policy)

        # горизонтальный нижний компановщик
        sub_main_lower_layout = QHBoxLayout(lower_frame)
        sub_main_lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_frame.setLayout(sub_main_lower_layout)

        # левый компоновщик
        left_sub_main_layout = QVBoxLayout(lower_frame)
        left_sub_main_layout.setSpacing(20)
        left_sub_main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        # Кнопка начала записи
        button_start_procedure = QPushButton('Начать процедуру', parent=lower_frame)
        button_start_procedure.setCursor(Qt.CursorShape.PointingHandCursor)
        button_start_procedure.setMinimumWidth(300)
        button_start_procedure.setFixedHeight(100)
        button_start_procedure.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        button_start_procedure.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        button_start_procedure.setStyleSheet("""
                               QPushButton {
                                   background-color: #0096C7;
                                   border-style: none;
                                   border-radius: 18px;  /* Круглая кнопка */
                                   color: #F6F6F6;
                               }
                               QPushButton:pressed {
                                   background-color: #ADE8F4;
                               }
                           """)
        button_start_procedure.clicked.connect(self.switch_to_work_window)

        left_sub_main_layout.addWidget(button_start_procedure)

        # История процедур
        left_sub_lower_frame = QFrame(parent=lower_frame)
        left_sub_lower_frame.setStyleSheet("""
                    background-color: #F0FDFF;
                    border-radius: 14px;
                """)
        size_policy = left_sub_lower_frame.sizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        left_sub_lower_frame.setSizePolicy(size_policy)
        left_sub_lower_layout = QVBoxLayout(left_sub_lower_frame)

        history_label = QLabel('История процедур', parent=left_sub_lower_frame)
        history_label.setFont(QFont("Arial", 12, weight=500))

        # Скролл для записей пациентов
        scroll_area_history = QScrollArea(parent=left_sub_lower_frame)
        scroll_area_history.setStyleSheet("""
            QScrollBar:vertical {
                background: #E5E5E5;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #ADE8F4;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
                background: none;
                border: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        # scroll_area_history.setStyleSheet("background-color: blue;")
        scroll_area_history.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        scroll_area_history.setMinimumHeight(186)

        scroll_area_history.setWidgetResizable(True)
        # scroll_area_history.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container_scroll_history = QFrame(parent=scroll_area_history)
        # container_scroll_history.setStyleSheet("""
        #     background-color: red;
        # """)
        container_scroll_history.setContentsMargins(10, 10, 10, 10)
        container_scroll_history.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        history_layout = QVBoxLayout(container_scroll_history)
        history_layout.setSpacing(4)
        history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Генерация множества кнопок
        for i in range(len(self.procedures_list)):
            item_history = ClickableProcedure(self.procedures_list[i], self.switch_to_watching_procedure,
                                              parent=container_scroll_history)
            item_history.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            item_history.setStyleSheet("""
                        QFrame {
                                background-color: none;
                                border: 1px solid #CCCCCC;
                                border-radius: 6px;
                            }

                        QLabel {
                            border: none;          
                            }
                    """)

            item_history_main_layout = QHBoxLayout(item_history)

            serial_number = QLabel(f'{i+1}', parent=item_history)
            serial_number.setFont(QFont("Arial", 15, weight=500))

            item_history_main_layout.addWidget(serial_number)

            information_item = QVBoxLayout(item_history)

            date_procedure = QLabel(f"Дата: {self.procedures_list[i]['created_at'].strftime('%d.%m.%y %H:%M')}",
                                    parent=item_history)
            date_procedure.setFont(QFont("Arial", 10, weight=400))

            # duration_procedure = QLabel(f'Продолжительность: {i} мин', parent=item_history)
            # duration_procedure.setFont(QFont("Arial", 10, weight=400))

            information_item.addWidget(date_procedure, alignment=Qt.AlignmentFlag.AlignLeft)
            # information_item.addWidget(duration_procedure, alignment=Qt.AlignmentFlag.AlignLeft)

            item_history_main_layout.addLayout(information_item)
            item_history_main_layout.addStretch()

            item_history.setLayout(item_history_main_layout)
            history_layout.addWidget(item_history)


        container_scroll_history.setLayout(history_layout)
        scroll_area_history.setWidget(container_scroll_history)

        # Конец скролла для записей пациентов

        left_sub_lower_layout.addSpacing(10)
        left_sub_lower_layout.addWidget(history_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_sub_lower_layout.addWidget(scroll_area_history)
        left_sub_lower_frame.setLayout(left_sub_lower_layout)
        left_sub_main_layout.addWidget(left_sub_lower_frame)

        # правый компоновщик
        right_sub_main_layout = QVBoxLayout(lower_frame)
        right_sub_main_layout.setSpacing(20)
        right_sub_main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_sub_main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Работа с электронной картой
        elecrtonic_card = QFrame(parent=lower_frame)
        elecrtonic_card.setStyleSheet("""
            background-color: #F0FDFF;
            border-style: none;
            border-radius: 18px; 
        """)
        elecrtonic_card.setMinimumWidth(260)
        elecrtonic_card.setFixedHeight(100)
        elecrtonic_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        elecrtonic_card_h_layout = QHBoxLayout(elecrtonic_card)
        elecrtonic_card.setLayout(elecrtonic_card_h_layout)
        elecrtonic_card_h_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        elecrtonic_card_sub_frame = QFrame(parent=elecrtonic_card)
        elecrtonic_card_v_layout = QVBoxLayout(elecrtonic_card_sub_frame)
        elecrtonic_card_v_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        elecrtonic_card_v_layout.setSpacing(12)
        elecrtonic_card_sub_frame.setLayout(elecrtonic_card_v_layout)
        elecrtonic_card_h_layout.addWidget(elecrtonic_card_sub_frame)

        label_electronic_card = QLabel('Электронная карта', parent=elecrtonic_card_sub_frame)
        label_electronic_card.setFont(QFont("Arial", 12, weight=500))

        # Кнопки загрузки и скачивания
        button_el_card_layout = QHBoxLayout(elecrtonic_card_sub_frame)

        def create_button_for_card(text):
            new_button = QPushButton(text, elecrtonic_card_sub_frame)
            new_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #ADE8F4;
                                    border-radius: 6px;
                                    border-style: none;
                                }
                                QPushButton:pressed {
                                    background-color: #009AB9;
                                }
                            """)
            new_button.setFixedSize(80, 28)
            new_button.setCursor(Qt.CursorShape.PointingHandCursor)

            # new_button.setCursor(Qt.CursorShape.PointingHandCursor)
            return new_button

        # Кнопки загрузки и скачивания
        button_el_card_layout.addWidget(create_button_for_card('Загрузить'))
        button_el_card_layout.addWidget(create_button_for_card('Скачать'))

        elecrtonic_card_v_layout.addWidget(label_electronic_card, alignment=Qt.AlignmentFlag.AlignHCenter)
        elecrtonic_card_v_layout.addLayout(button_el_card_layout)
        right_sub_main_layout.addWidget(elecrtonic_card)
        # Конец работа с электронной картой

        # Статистика
        statistics_frame = QFrame(parent=lower_frame)
        statistics_frame.setStyleSheet("""
                           background-color: #F0FDFF;
                           border-radius: 14px;
                       """)
        size_policy = statistics_frame.sizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        statistics_frame.setSizePolicy(size_policy)

        statistics_layout = QVBoxLayout(statistics_frame)
        statistics_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        statistics_label = QLabel('Статистика', parent=statistics_frame)
        statistics_label.setFont(QFont("Arial", 12, weight=500))

        statistics_layout.addSpacing(10)
        statistics_layout.addWidget(statistics_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Данные статистики
        data_statistics = []

        def create_label_data(text, value):
            frame_stat_item = QFrame(statistics_frame)
            stat_item_layout = QHBoxLayout(frame_stat_item)

            name_stat = QLabel(text, frame_stat_item)
            value_stat = QLabel(str(value), frame_stat_item)

            stat_item_layout.addWidget(name_stat)
            stat_item_layout.addStretch()
            stat_item_layout.addWidget(value_stat)

            return frame_stat_item

        data_statistics.append(create_label_data('Количество процедур', len(self.procedures_list)))
        # data_statistics.append(create_label_data('Max value', 38290))

        items_layout = QVBoxLayout(statistics_frame)
        items_layout.setSpacing(2)
        for i in data_statistics:
            items_layout.addWidget(i)

        statistics_layout.addLayout(items_layout)
        # добавление в главные компановщики

        right_sub_main_layout.addWidget(statistics_frame, alignment=Qt.AlignmentFlag.AlignTop)

        sub_main_lower_layout.addLayout(left_sub_main_layout)
        # sub_main_lower_layout.addStretch()
        sub_main_lower_layout.addLayout(right_sub_main_layout)

        main_v_layout.addWidget(frame_information)
        main_v_layout.addWidget(lower_frame)

        main_layout.addLayout(main_v_layout)

    def get_procedures_of_patient(self):
        result = get_procedures_of_patient(self.patient['patient_id'])

        try:
            sorted_procedures = sorted(result, key=lambda x: x["created_at"], reverse=True)
            return sorted_procedures
        except Exception as e:
            print('Ошибка сортировки списка процедур: ', e)
            return []

    def switch_to_watching_procedure(self, procedure):
        print(procedure)

        # Здесь вызов на окно просмотра процедуры, его нужно сделать
        # self.manager.show_window()

    def switch_to_work_window(self):
        self.manager.show_window(WorkWindow, jwt_provider=self.jwt_provider, patient=self.patient)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ventana = PatientWindow()
#     ventana.show()
#     sys.exit(app.exec())
