import cv2

from editing_video_v2.color_tracker import ColorTracker
from point_manager import PointManager
from video_manager import VideoManager


def start_program(video_path: str) -> None:
    """
    Запуск программы.

    :param video_path: Путь к видеофайлу.
    :return: None
    """
    print("Запуск программы...")
    point_manager = PointManager()
    video_manager = VideoManager(video_path, point_manager)
    try:

        success, frame = video_manager.capture.read()
        while success and cv2.waitKey(1) == -1:
            success, frame = video_manager.capture.read()
            if not success:
                break

            if video_manager.points['belly'] is None:
                video_manager.point_manager.point_belly()
            elif video_manager.points['breast'] is None:
                video_manager.point_manager.point_breast()
            else:
                video_manager.point_manager.selected_mode = None

            if video_manager.point_manager.selected_mode is not None:
                print(f"Кликните на объект для выбора точки: {video_manager.point_manager.selected_mode}")

            # Создание трекеров при наличии точек
            for key in video_manager.points:
                if video_manager.points[key] is not None and video_manager.trackers[key] is None:
                    video_manager.trackers[key] = ColorTracker(*video_manager.points[key])

            # print('video_manager.points:', video_manager.points)

            frame = video_manager.process_frame(frame)

            if not video_manager.recording_paused:
                video_manager.data = video_manager.update_dataframe(video_manager.data, video_manager.trackers)

            # print(f"Текущий словарь точек: {self.points}")
            # print(f"Текущий DataFrame:\n{self.data}")

            cv2.imshow("My Camera", frame)

        data = video_manager.get_dataframe()
    except Exception as e:
        print(f"Ошибка во время выполнения программы: {e}")
    finally:
        video_manager.end()
        print("Работа программы завершена.")
    data.to_csv("output.csv", index=False)
    # video_manager.create_graph(data)


if __name__ == "__main__":
    #video_path = "vid2.mp4"
    #video_path = "vid.mp4"
    video_path = 0
    start_program(video_path)
