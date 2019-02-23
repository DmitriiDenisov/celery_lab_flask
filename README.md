## Чтобы установить Rabbit-MQ:
```brew services start rabbitmq```
Ссылка на RabbitMQ:

http://127.0.0.1:15672/#/queues, что эквивалентно http://localhost:15672/#/queues. То есть 127.0.0.1 = localhost; Пароль: guest

## Как запустить воркер на текущей машине:
1. Создать venv в папке с проектом, сделать pip install requirements.txt
2. В консольке сначала cd в папку с проектом, затем: source venv/bin/activate (активируем терминал в venv)
3. Далее запуск Worker'a:
celery worker --concurrency 2 -A celery_lab -Q lab.generate_and_sum_of_lists
--concurrency - число дочерних процессов в Воркере, дефолт: 4
-A - название проекта
-Q - перечисляем названия очередей. Например, -Q SMS,email. Или -Q SMS,email,hard_task

## Как делать запросы (добавлять в очередь элементы):
Примеры запросов (для Postman):
    http://127.0.0.1:5000/email_and_sms
    http://127.0.0.1:5000/stupid-task
    http://127.0.0.1:5000/home
    Здесь 127.0.0.1 = localhost, 5000 - порт Фласка, home - метод, который прописывается в app.py

## Для воркеров на разных машинах:
1) Прописываем в run: host='0.0.0.0'. Это позволит делать глобальные обращения (=в сети)
2) Проверяем, что работает. Для этого зайти в настройки сети Settings -> Network. Там взять IP соединения. Например, 192.168.0.102
3) Далее проверяем, вбиваем в браузере http://192.168.0.102:5000/. (Это обращение глобальное к фласку, он находится на 5000 порте). Должно быть "The requested URL was not found on the server."
4) В RabbitMQ создаем нового юзера, например, логин:worker; пароль:worker
5) На новой машине в config.py:
celery_brocker_url = 'amqp://worker:worker@<ip_address_где_крутится_Rabbit>' # worker - worker это логин и пароль. Например,
celery_broker_url = 'amqp://worker:worker@192.168.0.102'
6) Запускаем через терминал (терминал можно в Pycharm) 'celery worker --concurrency 2 -A celery_lab -Q email' #тут email - название очереди
Прим.1: если выдается ошибка:[Errno 61] Connection refused. Это означает, что он пытается подцепиться к Локальному (!) Rabbit
Прим.2: нужно заставить его коннектиться к глобальному
7) Набрать команду 'hostname' в треминале. Выведется что-то в роде: 'MacBook-Air-2.local'. Надо взять 'MacBook-Air-2'
8) 'nano /usr/local/etc/rabbitmq/rabbitmq-env.conf'
9) Правим - NODE_IP_ADDRESS=0.0.0.0
NODENAME=rabbit@MacBook-Air-2
10) Чтобы сохранить - Ctrl-O, Enter, Ctrl-x, Enter
11) brew services restart rabbitmq
12) Заново заводим юзера worker (через интерфейс Rabbit MQ), жмем set permissions
13) повторить пункт 6)


## Чтобы ставить таски (добавлять в очередь), можно использовать браузер/postman любого компьютера в сети.
    По порту 5000 находится Фласк. Таким образом, запросы строятся по типу:
    http://<IP>:5000/<название_метода>, например
    http://172.20.10.2:5000/email

К одной очереди можно подключить несколько разных машин.