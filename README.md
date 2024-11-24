### Установка необходимых библиотек

1. Скачайте файл environment.yml;

2. Откройте консоль anaconda promt и введите команду:

```
conda env create -f environment.yml
```

Необходимо выполнить команду, находясь в директории, где находится файл или прописать путь к файлу yml.

3. Откройте PyCharm, в project settings > setting > project > python interpreter выберите add interpreter > conda environment > use existing environment и выберите 'server_application'.


### Работа на ветке assembling

Сейчас лучше работать на ветках, производных от assembling. 

Переходите на ветку assembling ```git checkout assembling```

Если такой ветки нет, то ее нужно подтянуть с удаленного репозитория ```git pull origin/assembling```

Проверить доступные удаленные ветки: ```git branch -r```

Находясь на ветке assembling создайте свою ветку, в которой будете работать.

### Краткое описание, что находится в assembling

В папке server_app находится сервер.

В папке project_ui пишется интерфейс.ф

В папке project_ui/editing_video находится трекер меток (такой же, что и просто в папке editing_video, но встроенный в приложение).

При работе, пожалуйста пишите, что вы создали такую-то ветку и отвечаете за нее, если сделали какой-то функционал - напишите, чтобы сразу получить обратную связь.