import datetime, time
import cv2
import numpy as np
import pandas as pd


clicked = False
points = []  # Список для хранения координат двух точек


def list_available_cameras():
    """
    Проверяет доступность подключенных камер и возвращает список индексов доступных камер.
    """
    available_cameras = []
    index = 0

    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        else:
            available_cameras.append(index)
            cap.release()
        index += 1
    return available_cameras


def open_videostream():
    """
    Определяет доступные камеры и открывает видеопоток с выбранной пользователем камеры.
    """
    list_cameras = list_available_cameras()

    if len(list_cameras) == 0:
        print("Нет доступных камер")
        return

    if len(list_cameras) == 1:
        cap = cv2.VideoCapture(list_cameras[0])
    else:
        print("Доступные камеры (по индексу): ")
        for cam in list_cameras:
            print(f"Камера {cam}")

        while True:
            try:
                choice_camera = int(input("Введите индекс камеры для выбора: "))
                if choice_camera in list_cameras:
                    cap = cv2.VideoCapture(choice_camera)
                    break
                else:
                    print("Нет такого индекса/камеры. Пожалуйста, выберите из доступных.")
            except ValueError:
                print("Пожалуйста, введите корректный номер.")

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру.")
        return
    return cap


def open_videofile(videofile):
    """
    Открывает видеофайл. Возвращает объект видеозахвата или None при неудаче.
    """
    cap = cv2.VideoCapture(videofile)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео!")
        return None
    return cap


def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        if len(points) < 2:
            points.append((x, y))
            clicked = True
        else:
            print("Достигнуто максимальное количество точек (2).")


# Путь к видеофайлу
path = "val.mp4"
cameraCapture = cv2.VideoCapture(path)

if not cameraCapture.isOpened():
    print("Cannot open camera")

cv2.namedWindow("My Camera")
cv2.setMouseCallback("My Camera", onMouse)

success, frame = cameraCapture.read()

data = pd.DataFrame(columns=["time", "y_point1", "y_point2"])
start_time = time.time()

class ColorTracker:
    def __init__(self, x, y, max_area_change=0.3):
        self.x = x
        self.y = y
        self.edges = None
        self.lost = False  # Флаг для определения потери точки
        self.initial_area = None  # Начальная площадь контура
        self.max_area_change = max_area_change  # Допустимое изменение площади

    def update_image(self, frame):
        self.edges = self.get_edges(frame)
        contours, _ = cv2.findContours(self.edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        dists = []

        for contour in contours:
            dist = cv2.pointPolygonTest(contour, (self.x, self.y), True)
            dists.append(dist)
        dists = np.array(dists)

        if len(dists) > 0 and np.max(dists) > 0:  # Проверяем, что есть контуры рядом с точкой
            needed_contour = np.argmax(dists)
            bbox = cv2.boundingRect(contours[needed_contour])
            self.x = bbox[0] + bbox[2] // 2
            self.y = bbox[1] + bbox[3] // 2

            frame = cv2.drawContours(frame, [contours[needed_contour]], -1, (0, 255, 0), 2)
            frame = cv2.circle(frame, (self.x, self.y), 10, (0, 0, 255), -1)
        return frame

    def get_edges(self, frame):
        return cv2.Canny(frame, 200, 200)


trackers = []

while success and cv2.waitKey(1) == -1:
    success, frame = cameraCapture.read()
    if not success:
        break

    # Создаем трекеры для каждой точки при первом клике
    if clicked and len(points) > 0:
        if len(trackers) < len(points):
            for (x, y) in points[len(trackers):]:
                trackers.append(ColorTracker(x, y))

        # Обновляем и отображаем точки в одном окне
        for tracker in trackers:
            frame = tracker.update_image(frame)

    # Показ изображения с точками и контурами
    cv2.imshow("My Camera", frame)

cv2.destroyAllWindows()
