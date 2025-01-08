import sys
import time

import cv2
import pandas as pd
from PyQt6.QtCore import Qt, QSize, QTimer, QPoint, QPointF
from PyQt6.QtGui import QIcon, QFont, QColor, QMouseEvent
from PyQt6.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel, QVBoxLayout, QFrame, QPushButton, \
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea, QMessageBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

from editing_video_v2.color_tracker import ColorTracker
from editing_video_v2.point_manager import PointManager
from editing_video_v2.video_manager import VideoManager
from work_windows.panel_choosing_marks import PanelChoosingMarks
from work_windows.real_time_graph import RealTimeGraph
from work_windows.requests_work_window import create_procedure
from work_windows.timer_frame import CountdownTimer
from work_windows.video_label import VideoLabel


class WorkWindow(QWidget):
    def __init__(self, manager, jwt_provider, patient):
        super().__init__()
        self.manager = manager
        self.jwt_provider = jwt_provider
        self.patient = patient
        self.managing_marks = None
        self.widget_graph = None
        self.timer_dataframe = None
        self.video_manager = None
        self.width_video_label = 480
        self.height_video_label = 360
        self.capture = None
        self.timer_video = None
        self.point_manager = PointManager()
        self.video_manager = VideoManager(self.point_manager)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""background-color: #E5FBFF;""")
        self.setWindowTitle('Процедура')
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
        self.button_back.clicked.connect(self.go_to_back_window)

        # главные слои
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_frame = QFrame(parent=self)
        self.main_layout = QVBoxLayout(main_frame)
        self.main_layout.setSpacing(14)
        main_frame.setMaximumWidth(900)
        main_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # main_frame.setStyleSheet('background-color: red;')

        # информация о пациенте
        patient_data_frame = QFrame(main_frame)
        patient_data_frame.setGraphicsEffect(self.frame_shadow(patient_data_frame))
        patient_data_layout = QVBoxLayout(patient_data_frame)
        patient_data_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        patient_data_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        patient_data_frame.setStyleSheet("""
            background-color: #F0FDFF;
            border-radius: 14px;
        """)
        patient_data_layout.setContentsMargins(20, 20, 20, 20)

        name_patient_label = QLabel(f"{self.patient['lastname']} {self.patient['name']} "
                                    f"{self.patient['surname'] if self.patient['surname'] else ''}",
                                    patient_data_frame)
        name_patient_label.setFont(QFont("Arial", 14, 600))

        date_label = QLabel(f"{self.patient['birthdate'] if self.patient['birthdate'] else 'Дата рождения отсутствует'}",
                            parent=patient_data_frame)
        date_label.setFont(QFont("Arial", 12, 400))

        patient_data_layout.addWidget(name_patient_label, alignment=Qt.AlignmentFlag.AlignLeft)
        patient_data_layout.addWidget(date_label, alignment=Qt.AlignmentFlag.AlignLeft)
        patient_data_frame.setLayout(patient_data_layout)

        # управление процедурой
        self.managing_procedure_frame = QFrame(main_frame)
        self.managing_procedure_layout = QHBoxLayout(self.managing_procedure_frame)
        self.managing_procedure_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.video_label = VideoLabel(parent=self)
        # self.video_label = QLabel()
        self.video_label.setGraphicsEffect(self.frame_shadow(self.video_label))
        # self.video_label.setStyleSheet('background-color: red;')
        self.video_label.setFixedSize(self.width_video_label, self.height_video_label)

        self.managing_procedure_layout.addWidget(self.video_label)

        # Блок управления процедурой
        right_block = QFrame(parent=main_frame)
        right_block.setStyleSheet("""
            background-color: #F0FDFF;
            border-radius: 14px;
        """)
        right_block.setGraphicsEffect(self.frame_shadow(right_block))
        right_block.setFixedHeight(360)
        right_block_layout = QVBoxLayout(right_block)
        right_block_layout.setSpacing(8)
        right_block_layout.setContentsMargins(12, 12, 12, 12)
        right_block_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        right_block.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        managing_label = QLabel('Управление', right_block)
        managing_label.setFont(QFont('Arial', 16, 600))

        calibration_button_frame = QFrame(right_block)
        calibration_button_layout = QVBoxLayout(calibration_button_frame)
        calibration_button_layout.setSpacing(4)
        calibration_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        calibration_button_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.calibration_button = QPushButton('Калибровка камеры', parent=calibration_button_frame)
        self.calibration_button.setFont(QFont('Arial', 11, 400))
        self.calibration_button.setSizePolicy(QSizePolicy.Policy.Preferred,
                                              QSizePolicy.Policy.Preferred)
        self.calibration_button.setStyleSheet("""
            QPushButton {
                background-color: #ADE8F4;
                border-style: none;
                border-radius: 6px;  /* Круглая кнопка */
                padding: 4px 10px;   
            }
            QPushButton:pressed {
                background-color: #009AB9;
            }
        """)
        self.calibration_button.setGraphicsEffect(self.frame_shadow(self.calibration_button, opacity=32))
        self.calibration_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.calibration_button.clicked.connect(self.perform_calibration)

        self.calibration_finish_label = QLabel('Выполните калибровку камеры', calibration_button_frame)
        self.calibration_finish_label.setFont(QFont('Arial', 8, 400))

        calibration_button_layout.addWidget(self.calibration_button)
        calibration_button_layout.addWidget(self.calibration_finish_label)
        calibration_button_frame.setLayout(calibration_button_layout)

        right_block_layout.addWidget(managing_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        # right_block_layout.addSpacing(10)
        right_block_layout.addWidget(calibration_button_frame, alignment=Qt.AlignmentFlag.AlignHCenter)
        right_block.setLayout(right_block_layout)
        self.managing_procedure_layout.addWidget(right_block)

        # блок выбора меток
        choosing_mark_frame = QFrame(right_block)
        choosing_mark_frame.setMinimumWidth(240)
        choosing_mark_layout = QVBoxLayout(choosing_mark_frame)
        choosing_mark_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        choosing_mark_layout.setSpacing(6)
        # choosing_mark_frame.setStyleSheet('background-color: red;')

        self.choose_mark_button = QPushButton('Выбрать метки', choosing_mark_frame)
        self.choose_mark_button.setFont(QFont('Arial', 11, 400))
        self.choose_mark_button.setSizePolicy(QSizePolicy.Policy.Preferred,
                                              QSizePolicy.Policy.Preferred)
        self.choose_mark_button.setStyleSheet("""
                    QPushButton {
                        background-color: #ADE8F4;
                        border-style: none;
                        border-radius: 6px;  /* Круглая кнопка */
                        padding: 4px 10px;   
                    }
                    QPushButton:pressed {
                        background-color: #009AB9;
                    }
                """)
        self.choose_mark_button.setGraphicsEffect(self.frame_shadow(self.choose_mark_button, opacity=32))
        self.choose_mark_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.choose_mark_button.clicked.connect(self.choose_marks_button)

        # компоновщики координат меток
        coordinates_vertical_layout = QVBoxLayout(choosing_mark_frame)
        coordinates_vertical_layout.setSpacing(2)

        coordinate_breast_layout = QHBoxLayout(choosing_mark_frame)
        coordinate_belly_layout = QHBoxLayout(choosing_mark_frame)

        mark_breast_label = QLabel('Метка груди:', choosing_mark_frame)
        mark_belly_label = QLabel('Метка живота:', choosing_mark_frame)
        self.value_breast_label = QLabel('Не выбрана', choosing_mark_frame)
        self.value_belly_label = QLabel('Не выбрана', choosing_mark_frame)

        coordinate_breast_layout.addWidget(mark_breast_label)
        coordinate_breast_layout.addStretch()
        coordinate_breast_layout.addWidget(self.value_breast_label)

        coordinate_belly_layout.addWidget(mark_belly_label)
        coordinate_belly_layout.addStretch()
        coordinate_belly_layout.addWidget(self.value_belly_label)

        coordinates_vertical_layout.addLayout(coordinate_breast_layout)
        coordinates_vertical_layout.addLayout(coordinate_belly_layout)

        choosing_mark_layout.addWidget(self.choose_mark_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        choosing_mark_layout.addLayout(coordinates_vertical_layout)
        choosing_mark_frame.setLayout(choosing_mark_layout)
        right_block_layout.addWidget(choosing_mark_frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        # таймер
        countdown_timer = CountdownTimer(parent=self,
                                         video_manager=self.video_manager,
                                         start_callback=self.start_graph,
                                         stop_callback=self.stop_graph)
        right_block_layout.addWidget(countdown_timer, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Инструкция
        self.scroll_instruction = QScrollArea(main_frame)
        self.scroll_instruction.setStyleSheet("""
            QScrollArea {
                border-style: none;
                border-radius: 14px;
                background-color: #F0FDFF;
            }
            QScrollArea > QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin-top: 14px; /* Отступ сверху */
                margin-bottom: 14px; /* Отступ снизу */
            }
            QScrollBar::handle:vertical {
                background: #ADE8F4;
                border-radius: 5px;
            }
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
                height: 0px; /* Убираем стрелочки */
                width: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: transparent;
                height: 10px;
                margin-top: 14px; /* Отступ сверху */
                margin-bottom: 14px; /* Отступ снизу */
            }
            QScrollBar::handle:horizontal {
                background: #ADE8F4;
                border-radius: 5px;
            }
            QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {
                width: 0px; /* Убираем стрелочки */
                height: 0px;
            }
        """)
        self.scroll_instruction.setGraphicsEffect(self.frame_shadow(self.scroll_instruction))
        self.scroll_instruction.setMinimumHeight(80)
        self.scroll_instruction.setWidgetResizable(True)

        instruction_frame = QFrame(self.scroll_instruction)
        instruction_frame.setStyleSheet("""
            background-color: transparent; /* Прозрачный фон для фрейма */
        """)
        instruction_layout = QVBoxLayout(patient_data_frame)
        instruction_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        instruction_layout.setContentsMargins(16, 16, 16, 16)
        instruction_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        patient_data_layout.setContentsMargins(20, 20, 20, 20)

        html_text = """
        <p style="margin: 0 0 10px 0;">Это первый абзац текста.</p>
        <p style="margin: 0 0 10px 0;">Это второй абзац текста с таким же отступом.</p>
        <p style="margin: 0 0 20px 0;">Это третий абзац текста с увеличенным отступом снизу. Это третий абзац текста с увеличенным отступом снизу.Это третий абзац текста с увеличенным отступом снизу.Это третий абзац текста с увеличенным отступом снизу.</p>
        <p style="margin: 0 0 10px 0;">Это первый абзац текста.</p>
        <p style="margin: 0 0 10px 0;">Это второй абзац текста с таким же отступом.</p>
        <p style="margin: 0 0 20px 0;">Это третий абзац текста с увеличенным отступом снизу.</p>
        <p style="margin: 0 0 10px 0;">Это первый абзац текста.</p>
        <p style="margin: 0 0 10px 0;">Это второй абзац текста с таким же отступом.</p>
        <p style="margin: 0 0 20px 0;">Это третий абзац текста с увеличенным отступом снизу.</p>
        """

        instruction_head_label = QLabel(parent=instruction_frame,
                                        text="Инструкция")
        instruction_head_label.setFont(QFont('Arial', 16, 600))

        instruction_label = QLabel(parent=instruction_frame,
                                   text=html_text)
        instruction_label.setFont(QFont('Arial', 11, 400))

        instruction_label.setWordWrap(True)

        instruction_layout.addWidget(instruction_head_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        instruction_layout.addWidget(instruction_label)
        instruction_frame.setLayout(instruction_layout)

        self.scroll_instruction.setWidget(instruction_frame)

        # добавление всех элементов
        self.main_layout.addWidget(patient_data_frame)
        self.managing_procedure_frame.setLayout(self.managing_procedure_layout)
        self.main_layout.addWidget(self.managing_procedure_frame)
        self.main_layout.addWidget(self.scroll_instruction)

        main_frame.setLayout(self.main_layout)
        layout.addWidget(main_frame, alignment=Qt.AlignmentFlag.AlignTop)
        self.button_back.raise_()

        # таймер для видео
        self.capture = cv2.VideoCapture(0)  # Укажите путь к вашему видео
        self.video_label.video_manager = self.video_manager

        self.timer_video = QTimer(self)
        self.timer_dataframe = QTimer(self)
        self.timer_video.timeout.connect(self.update_frame)
        self.timer_dataframe.timeout.connect(self.update_dataframe)
        self.timer_video.start(25)

    def perform_calibration(self):
        self.calibration_button.setEnabled(False)
        self.calibration_finish_label.setText('Калибровка камеры выполнена')

    def choose_marks_button(self):
        self.scroll_instruction.setVisible(False)
        self.managing_procedure_frame.setVisible(False)
        self.width_video_label = 640
        self.height_video_label = 480
        self.video_label.setFixedSize(self.width_video_label, self.height_video_label)
        # self.scroll_instruction.hide()
        self.managing_marks = PanelChoosingMarks(video_manager=self.video_manager,
                                                 callback_button_back=self.restore_interface)
        self.video_label.panel_choosing_marks = self.managing_marks
        self.main_layout.addWidget(self.managing_marks, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.video_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # QTimer.singleShot(8000, self.restore_interface)

    def reset_marks(self):
        self.video_manager.points['belly'] = None
        self.video_manager.trackers['belly'] = None
        self.video_manager.points['breast'] = None
        self.video_manager.trackers['breast'] = None
        self.widget_graph = None
        self.current_seconds = 0
        self.current_index = 0

    def restore_interface(self):
        # Возвращаем элементы в исходное состояние
        self.scroll_instruction.setVisible(True)
        self.managing_procedure_frame.setVisible(True)

        self.video_label.setFixedSize(480, 360)  # Исходный размер видео
        self.width_video_label = 480
        self.height_video_label = 360
        if self.managing_marks:
            self.main_layout.removeWidget(self.managing_marks)
            self.managing_marks.setParent(None)  # Отсоединяем от родителя
            self.managing_marks = None
        self.video_label.panel_choosing_marks = None
        self.main_layout.removeWidget(self.video_label)
        self.managing_procedure_layout.insertWidget(0, self.video_label)

    def start_graph(self):
        # self.main_layout.removeWidget(self.scroll_instruction)
        self.scroll_instruction.hide()

        if not self.widget_graph:
            self.widget_graph = RealTimeGraph(data=self.video_manager.data)

        if self.is_widget_in_layout(self.main_layout, self.widget_graph):
            self.widget_graph.show()
        else:
            self.main_layout.addWidget(self.widget_graph, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.timer_dataframe.start(200)

    def is_widget_in_layout(self, layout, widget):
        for i in range(layout.count()):  # Перебираем все элементы в лэйауте
            item = layout.itemAt(i)
            if item.widget() is widget:  # Сравниваем виджет с целевым
                return True
        return False

    def update_dataframe(self):
        if self.video_manager.recording:
            self.video_manager.update_dataframe()
            self.widget_graph.update_graph()
            print('запись')

    def stop_graph(self):
        # self.main_layout.addWidget(self.scroll_instruction)
        self.timer_dataframe.stop()
        # self.main_layout.removeWidget(self.widget_graph)
        self.widget_graph.hide()
        self.scroll_instruction.show()

    def update_frame(self):
        if not self.capture.isOpened():
            # print("Камера не открыта!")
            return

        ret, frame = self.capture.read()
        if not ret:
            # print("Не удалось получить кадр.")
            self.timer_video.stop()
            return

        # print(f"Размер кадра: {frame.shape}")

        height, width, channels = frame.shape
        self.video_label.actual_coordinates = (width, height)

        # Создание трекеров при наличии точек
        for key in self.video_manager.points:
            if self.video_manager.points[key] is not None and self.video_manager.trackers[key] is None:
                self.video_manager.trackers[key] = ColorTracker(*self.video_manager.points[key])

        belly = self.video_manager.points.get("belly")
        breast = self.video_manager.points.get("breast")

        if isinstance(belly, (list, tuple)):
            # print(f'belly y: {belly[1]}')
            self.value_belly_label.setText(str(belly[1]))
        else:
            self.value_belly_label.setText('Не установлена')

        if isinstance(breast, (list, tuple)):
            # print(f'breast y: {breast[1]}')
            self.value_breast_label.setText(str(breast[1]))
        else:
            self.value_breast_label.setText('Не установлена')

        frame = self.video_manager.process_frame(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.resize_frame_to_label(frame)
        # print(f"Размер кадра после масштабирования: {frame.shape}")

        height, width, channel = frame.shape
        qimg = QImage(frame.data, width, height, channel * width, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.video_label.setPixmap(pixmap)
        # print("Кадр успешно отображён.")

    # Используется в timer_frame
    def save_procedure_data(self):
        create_procedure(self.patient['patient_id'], self.jwt_provider.get_id_from_token(), self.video_manager.data)
        # print(self.video_manager.data)

    def resize_frame_to_label(self, frame):
        """Масштабирует кадр под размер QLabel."""
        resized_image = cv2.resize(frame, (self.width_video_label, self.height_video_label),
                                   interpolation=cv2.INTER_AREA)
        # return cv2.flip(resized_image, 1)
        return resized_image

    def frame_shadow(self, parent, radius=20, opacity=64):
        shadow = QGraphicsDropShadowEffect(parent=parent)
        shadow.setBlurRadius(radius)  # Радиус размытия тени
        shadow.setColor(QColor(0, 0, 0, opacity))  # Чёрная тень с прозрачностью
        shadow.setOffset(0, 0)
        return shadow

    def go_to_back_window(self):
        if self.video_manager.recording:
            return
        from patient_window.patient_window import PatientWindow
        self.manager.show_window(PatientWindow, patient=self.patient, jwt_provider=self.jwt_provider)

    def closeEvent(self, event):
        if self.capture and self.capture.isOpened():
            self.capture.release()
        event.accept()

# app = QApplication(sys.argv)
# window = WorkWindow()
# window.show()
# sys.exit(app.exec())
