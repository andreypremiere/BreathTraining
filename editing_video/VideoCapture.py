import cv2
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import sys
import threading


def list_available_cameras():
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


# Функция создания графика в реальном времени
def create_real_time_graph():
    plt.ion()  # Включаем интерактивный режим
    fig, ax = plt.subplots(figsize=(10, 5))

    line1, = ax.plot([], [], color='red', label='Sticker 1')
    line2, = ax.plot([], [], color='blue', label='Sticker 2')

    ax.set_xlim(0, 10)  # Диапазон по оси X
    ax.set_ylim(0, 700)  # Диапазон по оси Y (измените по вашим данным)
    ax.set_title('Real-time Object Tracking')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Coordinate Y')
    ax.grid(True)
    ax.legend()

    return fig, ax, line1, line2


# Функция обновления графика
def update_graph(fig, ax, line1, line2, x_data, y1_data, y2_data):
    line1.set_xdata(x_data)
    line1.set_ydata(y1_data)
    line2.set_xdata(x_data)
    line2.set_ydata(y2_data)

    ax.set_xlim(max(0, x_data[-1] - 100), x_data[-1])  # Поддержка "скроллинга" по X
    fig.canvas.draw()
    fig.canvas.flush_events()


def save_data(data_time, name_csv_file):
    if not data_time:
        print("Нет данных для сохранения.")
        return

    df = pd.DataFrame(data_time, columns=['Time', 'Y1', 'Y2'])
    df.to_csv(name_csv_file, index=False)
    return df


def create_graph(df):
    if df is None:
        print("Нет данных для построения графика.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['Y1'], color='red', label='Sticker 1')
    plt.plot(df['Time'], df['Y2'], color='blue', label='Sticker 2')
    plt.title('Object Tracking')
    plt.xlabel('Time (s)')
    plt.ylabel('Coordinate Y')
    plt.grid()
    plt.legend()
    plt.savefig('tracking_graph.png')
    plt.show()


def open_videostream():
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
    cap = cv2.VideoCapture(videofile)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео!")
        return None
    return cap


def select_sticker(frame):
    # Функция для выделения эталонного изображения стикера
    roi = cv2.selectROI("Select Sticker", frame, fromCenter=False, showCrosshair=True)
    sticker = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    return sticker, roi


def init_kalman():
    # Инициализация фильтра Калмана
    kalman = cv2.KalmanFilter(4, 2)
    kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0]], np.float32)
    kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                        [0, 1, 0, 1],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], np.float32)
    kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.01
    kalman.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.1  # Увеличение ковариации измерений
    return kalman


def apply_kalman_filter(kalman, x, y, smoothed_x, smoothed_y):
    """Применяет фильтр Калмана для сглаживания координат."""
    return kalman_predict_and_correct(kalman, x, y, smoothed_x, smoothed_y)


def kalman_predict_and_correct(kalman, x, y, smoothed_x, smoothed_y, alpha=0.1):
    # Коррекция: обновляем фильтр на основании текущего измерения
    measured = np.array([[np.float32(x)], [np.float32(y)]])
    kalman.correct(measured)

    # Прогнозирование нового положения
    predicted = kalman.predict()

    # Извлекаем значения как скаляры
    predicted_x = int(predicted[0][0])  # Преобразуем в целое число
    predicted_y = int(predicted[1][0])  # Преобразуем в целое число

    # Дополнительное экспоненциальное сглаживание поверх фильтра Калмана
    smoothed_x = int(alpha * smoothed_x + (1 - alpha) * predicted_x)
    smoothed_y = int(alpha * smoothed_y + (1 - alpha) * predicted_y)

    return smoothed_x, smoothed_y


def extract_roi(frame, roi):
    """Извлекает область интереса (ROI) из кадра."""
    x, y, w, h = roi
    return frame[int(y):int(y + h), int(x):int(x + w)]


def detect_keypoints_and_descriptors(roi_frame, akaze):
    """Обнаруживает ключевые точки и дескрипторы в заданной области интереса."""
    kp, des = akaze.detectAndCompute(roi_frame, None)
    return kp, des


def match_descriptors(des_template, des_frame, bf, threshold=5):
    """Сравнивает дескрипторы и возвращает совпадающие ключевые точки, если найдено достаточно совпадений."""
    if des_frame is None or des_template is None:
        return None

    matches = bf.match(des_template, des_frame)
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > threshold:
        return matches[:20]  # Ограничиваем до 20 лучших совпадений
    return None


def calculate_new_position(matches, kp_frame, roi, frame_shape):
    """Рассчитывает новое положение ROI на основе совпадающих точек."""
    if matches is None:
        return roi

    matched_kp_frame = np.array([kp_frame[m.trainIdx].pt for m in matches], dtype=np.float32)
    new_center = np.mean(matched_kp_frame, axis=0)

    x, y, w, h = roi
    new_x = int(new_center[0]) + x - w // 2
    new_y = int(new_center[1]) + y - h // 2

    # Ограничиваем координаты в пределах кадра
    new_x = max(0, min(new_x, frame_shape[1] - w))
    new_y = max(0, min(new_y, frame_shape[0] - h))

    return new_x, new_y, w, h


def draw_rectangle(frame, roi, color):
    """Рисует прямоугольник вокруг области интереса."""
    x, y, w, h = roi
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def track_sticker(sticker_roi, des_template, smoothed_x, smoothed_y, color_rectangle, kalman, gray_frame, frame, akaze,
                  bf):
    """Основная функция трекинга стикера."""
    roi_frame = extract_roi(gray_frame, sticker_roi)
    kp_frame, des_frame = detect_keypoints_and_descriptors(roi_frame, akaze)
    matches = match_descriptors(des_template, des_frame, bf)

    if matches:
        sticker_roi = calculate_new_position(matches, kp_frame, sticker_roi, frame.shape)
        smoothed_x, smoothed_y = apply_kalman_filter(kalman, sticker_roi[0], sticker_roi[1], smoothed_x, smoothed_y)
        draw_rectangle(frame, (smoothed_x, smoothed_y, sticker_roi[2], sticker_roi[3]), color_rectangle)

    return sticker_roi, smoothed_x, smoothed_y


def main_video_capture_helper(cap, realtime_graph=False):
    akaze = cv2.AKAZE_create()
    kalman1 = init_kalman()
    kalman2 = init_kalman()
    data = []

    if cap is None:
        sys.exit("Завершение программы: видеофайл не найден или не удалось открыть.")

    ret, frame = cap.read()
    if ret:
        sticker1, sticker1_roi = select_sticker(frame)
        sticker2, sticker2_roi = select_sticker(frame)
        sticker1_gray = cv2.cvtColor(sticker1, cv2.COLOR_BGR2GRAY)
        sticker2_gray = cv2.cvtColor(sticker2, cv2.COLOR_BGR2GRAY)
        kp_template1, des_template1 = akaze.detectAndCompute(sticker1_gray, None)
        kp_template2, des_template2 = akaze.detectAndCompute(sticker2_gray, None)
        smoothed_x1, smoothed_y1 = sticker1_roi[0], sticker1_roi[1]
        smoothed_x2, smoothed_y2 = sticker2_roi[0], sticker2_roi[1]
    else:
        print("Не удалось захватить первый кадр")
        return

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    start_time = time.time()

    if realtime_graph:
        fig, ax, line1, line2 = create_real_time_graph()
        x_data, y1_data, y2_data = [], [], []
        last_graph_update_time = start_time  # Время последнего обновления графика

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sticker1_roi, smoothed_x1, smoothed_y1 = track_sticker(sticker1_roi, des_template1, smoothed_x1, smoothed_y1,
                                                               (0, 255, 0), kalman1, gray_frame, frame, akaze, bf)
        sticker2_roi, smoothed_x2, smoothed_y2 = track_sticker(sticker2_roi, des_template2, smoothed_x2, smoothed_y2,
                                                               (0, 255, 255), kalman2, gray_frame, frame, akaze, bf)
        current_time = time.time() - start_time
        data.append((current_time, smoothed_y1, smoothed_y2))

        if realtime_graph:
            # Добавляем новые данные для графика
            x_data.append(current_time)
            y1_data.append(smoothed_y1)
            y2_data.append(smoothed_y2)

            # Обновляем график раз в секунду
            if current_time - (last_graph_update_time - start_time) >= 1:
                update_graph(fig, ax, line1, line2, x_data, y1_data, y2_data)
                last_graph_update_time = current_time  # Обновляем время последнего обновления графика

        cv2.imshow('Sticker Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Сохраняем данные в CSV и выводим финальный график
    df = save_data(data, "tracking_data.csv")
    create_graph(df)


def main_video_capture(cap):
    main_video_capture_helper(cap, realtime_graph=False)


def main_video_capture_with_realtimegraph(cap):
    main_video_capture_helper(cap, realtime_graph=True)


if __name__ == "__main__":
    videofile = "val.mp4"
    cap = open_videofile(videofile)
    main_video_capture_with_realtimegraph(cap)
