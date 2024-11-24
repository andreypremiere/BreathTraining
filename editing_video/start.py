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

    data = None

    try:
        video_manager.main_loop()
        data = video_manager.get_dataframe()
    except Exception as e:
        print(f"Ошибка во время выполнения программы: {e}")
    finally:
        video_manager.end()
        print("Работа программы завершена.")

    data.to_csv("output.csv", index=False)
    # video_manager.create_graph(data)


if __name__ == "__main__":
    video_path = "val.mp4"
    start_program()
