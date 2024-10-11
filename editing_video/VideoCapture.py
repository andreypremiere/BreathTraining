import cv2
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

data = []


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


def save_data(data_time):
    if not data_time:
        print("Нет данных для сохранения.")
        return

    df = pd.DataFrame(data_time, columns=['Time', 'Y'])
    df.to_csv('tracking_data.csv', index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['Y'], color='red')
    plt.title('Object Tracking')
    plt.xlabel('Time (s)')
    plt.ylabel('Coordinate Y')
    plt.grid()
    plt.savefig('tracking_graph.png')
    plt.show()


def video_capture():
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

    ret, frame = cap.read()
    if not ret:
        print("Ошибка: не удалось захватить кадр.")
        cap.release()
        return

    # ROI
    bbox = cv2.selectROI('Выберите область для отслеживания', frame, False)
    cv2.destroyWindow('Выберите область для отслеживания')

    # Инициализация отслеживания
    x, y, w, h = bbox
    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Вычисление границ цвета в выбранной области
    lower_color = np.min(hsv_roi, axis=(0, 1))
    upper_color = np.max(hsv_roi, axis=(0, 1))

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось захватить кадр.")
            break

        frame = cv2.flip(frame, 1)  # Реверс видео

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Контуры на маске
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            center = (x + w // 2, y + h // 2)

            if w > 10 and h > 10:  # Проверка, что размеры прямоугольника достаточно велики
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

            current_time = time.time() - start_time
            data.append((current_time, center[1]))

        cv2.imshow('Frame', frame)
        cv2.imshow('Mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Нажмите 'q' для выхода
            break

    cap.release()
    cv2.destroyAllWindows()
    save_data(data)


if __name__ == "__main__":
    video_capture()
