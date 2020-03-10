# text_recognition_container

Данный проект представляет из себя контейнер, который позволяет с помощью OpenCV, tesseract и Apache-Tika извлекать текстовую информацию из картинок, pdf-файлов, текстовых форматов(таких как dox, docx), презентаций(ppt, pptx).

## Instruction

Создание образа происходит с помощью следующей команды:

build -t our_image:version /path/to/directory/with/Dockerfile (.)

Где, our_image - ваше название для образа, version - указание версии,
/path/to/directory/with_Dockerfile - путь к директории с Dockerfile.
В данном случае указываем "." - текущая директория.

Действия, происходящие при создании контейнера описаны в Dockerfile.

----------------------------------------------------------------------------------------------------------------

Запуск контейнера из образа:

docker run -d -p 5000:5000 our_image

-d - Запускает контейнер в фоновом режиме.
-p - осуществляется проброс портов. При указании ip виртуальной машины и 5000 порта происходит
обращение к контейнеру. P.S. При необходимости смены порта, необходимо изменить две строки в Dockerfile:
	1. EXPOSE 5000 => номер порта заменить на свой
	2. ENTRYPOINT ["gunicorn", "-t", "604800","-b", "0.0.0.0:5000", "app:app"] => порт 5000 заменить на свой.

----------------------------------------------------------------------------------------------------------------

Интерфейс контейнера написан на Flask, используется сервер gunicorn.

Интерфейс позволяет посылать POST-запросы с файлом, который необходимо распознать.
Это можно осуществить из браузера, либо с помощью консольных команд:
curl -F "file=@/Path/to/file/test.txt" -F "press=OK" http://ip-VM:5000 - запрос.
wget http://ip-VM/path/to/file/result.txt - скачивание файла.

В ответ на запрос возвращается json со статусом запроса, ссылкой для скачивание 
файла с выделенными конфиденциальными словами и
результатом обработки исходного файла в виде строки.

{“id”:200, "file”:”http://...”, “result”:{“classification”:”some text”, “attribute_classification”:”some text"}}

----------------------------------------------------------------------------------------------------------------

Подключение сторонних модулей к серверу внутри контейнера.

Свой модуль необходимо подключать в модуль app.py - функция upload_file.

Файлы, которые передаются с запросом лежат в директории /tmp_upload.
Имя и полнуй путь до полученного файла можно получить с помощью join(app.config['UPLOAD_FOLDER'], filename).

Файлы, генерируемые в процессе работы вашего модуля необходимо положить в директорию /result. Они должны иметь
имя полученного файла с постфиксом "_out".

Если ваша функция возвращает строку, ее можно записать в переменную string_answer.


## FAQ Docker.

1. Что необходимо установить, чтобы воспользоваться Docker?
-docker-machine
-docker		(На некоторых ОС могут поставляться вместе)
-Драйвер виртуальной машины, например virtualbox.

2. Как создать виртуальную машину?
```docker-machine create --driver=virtualbox Name_of_machine```

3. Как импортировать виртуальное окружение машины?
```docker-machine env Name_of_machine```
После ввода команды, вы должны получить следующий вывод:

```
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.104:2376"
export DOCKER_CERT_PATH="/Users/test_user/.docker/machine/machines/Char"
export DOCKER_MACHINE_NAME="Name_of_machine"
# Run this command to configure your shell:
# eval $(docker-machine env Name_of_machine)
```
Вам необходимо скопировать и ввести в терминал данную строку ```eval $(docker-machine env Name_of_machine)```

