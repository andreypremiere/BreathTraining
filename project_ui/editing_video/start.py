import cv2

from editing_video.color_tracker import ColorTracker
from editing_video.point_manager import PointManager
from editing_video.video_manager import VideoManager


def start_program(video_path: str = 0) -> None:
    """
    Запуск программы.

    :param video_path: Путь к видеофайлу.
    :return: None
    """
    print("Запуск программы...")
    point_manager = PointManager()
    video_manager = VideoManager(point_manager, video_path)

    data = None

    # frame - кадр (массив), success - успешно ли выполнено чтение
    # video_manager.capture - объект класса cv2.VideoCapture, который захватывает видеопоток.
    success, frame = video_manager.capture.read()

    k = 0

    while success and cv2.waitKey(1) == -1:
        success, frame = video_manager.capture.read()  # получить следующий кадр
        if not success:
            break

        # Обработка выбора точек
        # если в списке точек меньше двух точек
        if len(video_manager.point_manager.points) < 2:
            # если точек нет, то переводим point_manager self.selected_mode = "belly"
            if len(video_manager.point_manager.points) == 0:
                video_manager.point_manager.point_belly()
                print("Выберите точку для живота")
            # если точка есть, то переводим point_manager self.selected_mode = "breast"
            elif len(video_manager.point_manager.points) == 1:
                video_manager.point_manager.point_breast()
                print("Выберите точку для груди")
        # в противном случае None (после назначения всех точек)
        else:
            video_manager.point_manager.selected_mode = None

        # Создаем трекеры для новых точек
        # если точек больше чем 0, и их меньше, чем трекерах
        if len(video_manager.point_manager.points) > 0:
            if len(video_manager.trackers) < len(video_manager.point_manager.points):
                for (x, y) in video_manager.point_manager.points[len(video_manager.trackers):]:
                    video_manager.trackers.append(ColorTracker(x, y))
                    print(x, y)
                    print('Точка добавлена')

        k += 1

        # if k == 470:
        #     video_manager.point_manager.points.append((20, 47))
        #
        # if k == 560:
        #     video_manager.point_manager.points.append((50, 87))

        frame = video_manager.process_frame(frame)
        video_manager.data = video_manager.update_dataframe(video_manager.data, video_manager.trackers)
        # здесь будет ендпоинт возврата кадра
        cv2.imshow("My Camera", frame)

    try:
        # video_manager.main_loop()
        data = video_manager.get_dataframe()
    except Exception as e:
        print(f"Ошибка во время выполнения программы: {e}")
    finally:
        video_manager.end()
        print("Работа программы завершена.")

    data.to_csv("output.csv", index=False)

start_program()