import cv2

capture = cv2.VideoCapture(0)  # Использование веб-камеры
if not capture.isOpened():
    print("Камера не открыта!")
    exit()

while True:
    ret, frame = capture.read()
    if not ret:
        print("Не удалось получить кадр!")
        break

    cv2.imshow("Видео", frame)

    # Нажмите "q" для выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
