from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, \
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea
from PyQt6.QtGui import QIcon

from additional_widget.clickable_frame import ClickableFrame
from editing_patient.editing_patient_window import EditingPatient
from search_patient.parse_full_name import parse_fullname
from search_patient.recent_patients import RecentPatients
from search_patient.requests_serch_window import get_patients_by_name, get_patients_by_ids
from patient_window.patient_window import PatientWindow


class SearchPatient(QWidget):
    def __init__(self, manager, jwt_provider=None, login=None, switch_window_callback=None):
        super().__init__()

        self.manager = manager
        self.button1 = None
        self.left_panel_layout = None
        # self.patients_of_doctor = get_patients_of_doctor(jwt_provider.get_id_from_token())
        self.recent_patient_manager = RecentPatients()
        self.recent_patients = get_patients_by_ids(self.recent_patient_manager.get_all_ids())
        self.switch_window = switch_window_callback
        self.input_lastname_patient = None
        self.button_search_patient = None
        self.login = login
        self.jwt_provider = jwt_provider
        self.init_ui()
        # self.show()

    def init_ui(self):
        self.setStyleSheet("""background-color: #E5FBFF;""")
        self.setWindowTitle('Поиск клиента')
        self.setGeometry(50, 30, 1400, 780)

        # Главный горизонтальный макет
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Левая панель
        self.left_panel = QFrame(self)
        self.left_panel.hide()

        self.left_panel.setStyleSheet("""
            background-color: #F1FDFF;
            border: none;
            border-radius: 15px;
        """)
        self.left_panel.setMinimumWidth(300)  # Ширина панели
        self.left_panel.setMaximumWidth(360)  # Ширина панели

        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setSpacing(20)  # Отступы между элементами
        self.left_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        shadow_effect_1 = QGraphicsDropShadowEffect()
        shadow_effect_1.setBlurRadius(20)
        shadow_effect_1.setOffset(0, 0)
        shadow_effect_1.setColor(QColor(0, 0, 0, 64))
        self.left_panel.setGraphicsEffect(shadow_effect_1)

        # Элементы левой панели
        menu_label = QLabel("Найденные пациенты", self)
        menu_label.setStyleSheet("""
            color: black;/* Синяя рамка толщиной 2px */
        """)
        menu_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        menu_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)  # Фиксируем высоту

        self.left_panel_layout.addSpacing(10)
        self.left_panel_layout.addWidget(menu_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.button2 = QPushButton("Скрыть", self)
        self.button2.setStyleSheet("""
            QPushButton {
                background-color: #009AB9;
                color: white;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #007A94;
            }
        """)
        self.button2.clicked.connect(self.hide_panel)


        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Внутренний виджет, который будет содержать панель
        container_widget = QFrame()
        self.notes_finded_panel = QVBoxLayout(container_widget)
        self.notes_finded_panel.setSpacing(4)
        self.notes_finded_panel.setAlignment(Qt.AlignmentFlag.AlignTop)



        # Устанавливаем контейнер в прокручиваемую область
        scroll_area.setWidget(container_widget)

        self.left_panel_layout.addWidget(scroll_area)

        # spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # self.left_panel_layout.addItem(spacer)  # Добавляем распорку перед кнопкой

        self.left_panel_layout.addWidget(self.button2)





        # ---------------------------------------------------------------------------------------------

        # Центральная часть (основной контент)
        central_widget = QFrame(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Фрейм с формой
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setStyleSheet("""
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #D5F8FF, stop: 1 #9BE6FF);
                    border: none;           
                    border-radius: 15px; 
                """)
        frame.setMaximumSize(300, 140)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(30)
        shadow_effect.setOffset(0, 0)
        shadow_effect.setColor(QColor(0, 0, 0, 64))
        frame.setGraphicsEffect(shadow_effect)

        # Заголовок
        title = QLabel("Введите ФИО пациента", self)
        font = QFont("Arial", 12)
        font.setWeight(600)
        title.setFont(font)
        title.setStyleSheet("background-color: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поле ввода
        self.input_lastname_patient = QLineEdit(self)
        # self.input_lastname_patient.setPlaceholderText("ФИО")
        self.input_lastname_patient.setFont(QFont("Arial", 10))
        self.input_lastname_patient.setStyleSheet("background-color: #FBFBFB;"
                                                  "border-radius: 6px;"
                                                  "border-style: none;")
        self.input_lastname_patient.setMinimumSize(200, 28)

        # Кнопка
        self.button_search_patient = QPushButton("Найти", self)
        self.button_search_patient.setStyleSheet("""
                    QPushButton {
                        background-color: #00B4D8;
                        border-radius: 6px;
                        border-style: none;
                    }
                    QPushButton:pressed {
                        background-color: #009AB9;
                    }
                """)
        self.button_search_patient.setFixedSize(50, 28)
        self.button_search_patient.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_search_patient.clicked.connect(self.handle_search_patients)

        # Добавление элементов во фрейм
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(14)
        frame_layout.addWidget(title)
        frame_layout.addWidget(self.input_lastname_patient)
        frame_layout.addWidget(self.button_search_patient, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Добавление фрейма в центральный макет
        central_layout.addWidget(frame)

        # ---------------------------------------------------------------------------------------------

        # Панель кнопок

        button_panel = QVBoxLayout()
        button_panel.setSpacing(10)
        button_panel.setContentsMargins(10, 10, 20, 10)  # Устанавливаем отступы: слева, сверху, справа, снизу
        button_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icons = ['icons/person.svg', 'icons/latest_list.svg', 'icons/add_patient.svg', 'icons/exit.svg']

        for i in range(len(icons)):  # Добавляем три кнопки
            button = QPushButton('', self)
            button.setFixedSize(48, 48)
            button.setStyleSheet("""
                           QPushButton {
                               background-color: #FFFFFF;
                               border-style: none;
                               border-radius: 6px;  /* Круглая кнопка */
                           }
                           QPushButton:pressed {
                               background-color: #009AB9;
                           }
                       """)

            # Устанавливаем иконку
            icon = QIcon(icons[i])  # Загружаем иконку из файла
            button.setIcon(icon)
            button.setIconSize(button.size() - QSize(5, 5))  # Размер иконки равен размеру кнопки

            # Добавляем кнопку в панель
            button_panel.addWidget(button)

        button_panel.itemAt(1).widget().clicked.connect(self.hide_panel_right)
        button_panel.itemAt(2).widget().clicked.connect(self.go_to_new_patient)
        button_panel.itemAt(3).widget().clicked.connect(self.handle_exit)

        button_panel.itemAt(0).widget().setToolTip("Мой профиль")
        button_panel.itemAt(1).widget().setToolTip("Список недавних пациентов")
        button_panel.itemAt(2).widget().setToolTip("Добавить пациента")
        button_panel.itemAt(3).widget().setToolTip("Выход")


        # ---------------------------------------------------------------------------------------------

        self.right_panel = QFrame(self)
        self.right_panel.setStyleSheet("""
            background-color: #F1FDFF;
            border: none;
            border-radius: 15px;
        """)
        self.right_panel.setMinimumWidth(300)  # Ширина панели
        self.right_panel.setMaximumWidth(360)
        self.right_panel.hide()

        # Главный макет правой панели
        right_panel_layout = QVBoxLayout(self.right_panel)
        right_panel_layout.setSpacing(20)
        right_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        # Тень для правой панели
        shadow_effect_2 = QGraphicsDropShadowEffect()
        shadow_effect_2.setBlurRadius(20)
        shadow_effect_2.setOffset(0, 0)
        shadow_effect_2.setColor(QColor(0, 0, 0, 64))
        self.right_panel.setGraphicsEffect(shadow_effect_2)

        # Заголовок "Информация"
        right_menu_label = QLabel("Недавние пациенты", self)
        right_menu_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        right_menu_label.setStyleSheet("color: black;")
        right_panel_layout.addSpacing(10)

        right_panel_layout.addWidget(right_menu_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Прокручиваемая область
        scroll_area_right = QScrollArea(self)
        scroll_area_right.setWidgetResizable(True)

        # Внутренний виджет для прокрутки
        container_widget_right = QFrame()
        self.info_panel = QVBoxLayout(container_widget_right)
        self.info_panel.setSpacing(4)
        self.info_panel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.add_recent_patients()

        # Устанавливаем контейнер в прокручиваемую область
        scroll_area_right.setWidget(container_widget_right)

        # Добавляем прокручиваемую область в правую панель
        right_panel_layout.addWidget(scroll_area_right)

        # Кнопка "Скрыть" для правой панели
        self.right_button1 = QPushButton("Скрыть", self)
        self.right_button1.setStyleSheet("""
            QPushButton {
                background-color: #009AB9;
                color: white;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #007A94;
            }
        """)
        self.right_button1.clicked.connect(self.hide_panel_right)
        right_panel_layout.addWidget(self.right_button1)

        # Добавляем панели и центральный виджет в главный макет
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(central_widget)
        main_layout.addLayout(button_panel)
        main_layout.addWidget(self.right_panel)

    def hide_panel(self):
        if self.left_panel.isVisible():
            self.left_panel.hide()

    def hide_panel_right(self):
        if self.right_panel.isVisible():
            self.right_panel.hide()
        else:
            self.right_panel.show()

    def handle_search_patients(self):
        data = parse_fullname(self.input_lastname_patient.text())

        result = get_patients_by_name(data)

        if result is None:
            return

        self.add_finded_patients(result)

        if not self.left_panel.isVisible():
            # self.left_panel.hide()
            # self.button2.setText("Показать")
            self.left_panel.show()

    def add_finded_patients(self, data):
        self.clear_layout(self.notes_finded_panel)

        # Генерация множества кнопок
        for i in data:
            item_frame = ClickableFrame(i, self.switch_to_patient_card, self, self.recent_patient_manager.add_user_id)
            item_frame.setStyleSheet("""
                                QFrame {
                                    background-color: none;
                                    border: 1px solid #CCCCCC;
                                    border-radius: 6px;
                                    box-shadow: 
                                }
                            """)
            item_frame.setFixedHeight(70)  # Высота каждого элемента
            item_frame.setContentsMargins(4, 4, 4, 4)

            # Компоновщик для содержимого
            item_layout = QVBoxLayout(item_frame)
            item_layout.setSpacing(2)
            # item_layout.setContentsMargins(10, 5, 10, 5)  # Внутренние отступы

            # ФИО
            name_label = QLabel(f"{i['lastname']} {i['name']} {i['surname'] if i['surname'] else ''}", self)
            name_label.setStyleSheet("font-size: 14px; font-weight: bold; "
                                     "color: #333333;"
                                     "border-style: none;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            # name_label.setWordWrap(True)  # Перенос слов

            # Год рождения
            birth_year_label = QLabel(f"{i['birthdate'] if i['birthdate'] else 'Дата не установлена'}", self)
            birth_year_label.setStyleSheet("font-size: 12px; color: #666666;"
                                           "border-style: none;")
            birth_year_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # Добавляем виджеты в компоновщик
            item_layout.addWidget(name_label)
            item_layout.addWidget(birth_year_label)

            # Добавляем объект в панель
            self.notes_finded_panel.addWidget(item_frame)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)  # Получаем первый элемент из лейаута
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Удаляем виджет корректно
            else:
                self.clear_layout(item.layout())
            #

    def add_recent_patients(self):
        self.clear_layout(self.info_panel)
        for i in self.recent_patients:
            # Карточка
            item_frame = ClickableFrame(i, self.switch_to_patient_card, self, self.recent_patient_manager.add_user_id)
            item_frame.setStyleSheet("""
                        QFrame {
                            background-color: none;
                            border: 1px solid #CCCCCC;
                            border-radius: 6px;
                        }
                    """)
            item_frame.setFixedHeight(70)  # Высота карточки
            item_frame.setContentsMargins(4, 4, 4, 4)

            # Макет для содержимого карточки
            item_layout = QVBoxLayout(item_frame)
            item_layout.setSpacing(2)

            # Название элемента
            title_label = QLabel(f"{i['lastname']} {i['name']} {i['surname'] if i['surname'] else ''}", self)
            title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333; border-style: none;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            # Подробности элемента
            detail_label = QLabel(f"{i['birthdate'] if i['birthdate'] else 'Дата не установлена'}", self)
            detail_label.setStyleSheet("font-size: 12px; color: #666666; border-style: none;")
            detail_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # Добавляем виджеты в карточку
            item_layout.addWidget(title_label)
            item_layout.addWidget(detail_label)

            # Добавляем карточку в панель
            self.info_panel.addWidget(item_frame)

    def switch_to_patient_card(self, patient):
        self.manager.show_window(PatientWindow, patient=patient, jwt_provider=self.jwt_provider)

    def go_to_new_patient(self):
        self.manager.show_window(EditingPatient, jwt_provider=self.jwt_provider, patient=None)

    def handle_exit(self):
        self.jwt_provider.clear_token()
        self.manager.show_window(self.login)

# app = QApplication(sys.argv)
# ventana = SearchPatient(manager=None, login=None)
# ventana.show()
# sys.exit(app.exec())
