from flask import Flask, jsonify, request, abort
from celery_lab.functions import function_gener, sum_of_list
from celery_lab.tasks import generate_and_sum_of_lists, redis_db, stupid_func, _try_another_func, hard_func, send_email, \
    send_SMS
from marshmallow import Schema, fields, ValidationError


# Штука, чтобы принимать аргументы через Postman:
# Чтобы послать аргументы через Postman надо выбрать Body->raw и в формате Json:
# {
# 	"n": 5000,
# 	"m": 8000
# }

# Celery начинается, когда делается вызов apply_async(). Она принимает параметр queue - название очереди
# Если queue не подается, то принимается дефолт 'celery'. Если такой очереди нет => создается
# Если queue подается название очереди, которой нет, то она создается
# В общем случае в качестве queue подается название очереди, которое объявлялось в файле celery.py
class TaskParamsSchema(Schema):
    n = fields.Int()
    m = fields.Int()
    k = fields.Int()
app = Flask(__name__)


# Просто принт Hello world, без Celery
@app.route('/home', methods=['GET'])
def hello_world():
    return jsonify({'Hello, World!': 0})


# Запуск без Celery (просто вызов функции)
@app.route('/launch-task', methods=['POST'])
def launch_task():
    whole_list = function_gener(10000, 1500)
    sum_ = sum_of_list(whole_list)
    return jsonify({'sumOfLists': int(sum_)})


# Заупск с Celery (результат записывается в redis)
@app.route('/launch-task-async', methods=['POST'])
def launch_task_async():
    try:
        params = TaskParamsSchema(strict=True).loads(request.data).data
    except ValidationError:
        return abort(400)
    sum_ = generate_and_sum_of_lists.apply_async((params['n'], params['m']))  # celery начинается, когда заходим внутрь
    return jsonify({'sumOfLists': sum_.id})


# Возвращает результат Task по id'нику, который выдает функция launch_task_assync
@app.route('/tasks/<uuid:task_id>/result', methods=['GET'])
def get_result(task_id):
    res = redis_db.get(str(task_id))
    return jsonify({'res': res})


# Возвращает все текущие ключи в Redis
@app.route('/get-all-keys', methods=['GET'])
def get_keys():
    res = redis_db.keys()
    return jsonify({'res': res})


@app.route('/stupid-task', methods=['GET'])
def stupid():
    stupid_func.apply_async(queue='feed_tasks') # подаем название очереди, которой не было. Она создастся
    return jsonify({'res': True})


@app.route('/try-another-func', methods=['GET'])
def try_another_func():
    _try_another_func.apply_async() # если не указывать queue, то будет по дефолта подаваться в очередь celery
    return jsonify({'res': True})


@app.route('/three_ques', methods=['GET'])
def three():
    try:
        params = TaskParamsSchema(strict=True).loads(request.data).data
    except ValidationError:
        return abort(400)

    send_SMS.apply_async(queue='SMS')
    send_email.apply_async(queue='email')
    hard_func.apply_async((params['n'], params['m'], 2), queue='hard_task') # можно запускать по очереди несколько очередей
    hard_func.apply_async((params['n'], params['m'], params['k']), queue='SMS')
    return jsonify({'res': True})


@app.route('/SMS', methods=['GET'])
def SMS():
    from datetime import date
    d = date(2005, 7, 14)
    send_SMS.apply_async((1, 2, d), queue='SMS') # пример, как можно передавать константы внутрь функции
    return jsonify({'res': True})


@app.route('/email', methods=['GET'])
def email():
    send_email.apply_async(queue='email')
    return jsonify({'res': True})


@app.route('/email_and_sms', methods=['POST'])
def email_and_sms():
    send_email.apply_async(queue='email')
    send_SMS.apply_async((1, 2, 3), queue='SMS')
    return jsonify({'res': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # host позволяет дать глобальный доступ для устройств в сети. Адрес в общем виде: http://<ip_addess>:5000. http://172.20.10.2:5000/
