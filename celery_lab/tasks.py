import time
from datetime import datetime, date

from celery_lab.celery import app
from celery_lab.functions import sum_of_list, function_gener
from redis import StrictRedis

# В реддис (большой словарь) хранятся все результаты
redis_db = StrictRedis(decode_responses=True)


@app.task(bind=True) # bind=True => передавать self внутрь функции
# Здесь, чтобы получить id из self. self - ссылка на объект типа Task.
# Task - это объект
def generate_and_sum_of_lists(self, n: int, m: int):
    print('START! FOR N={}, M={}'.format(n, m))
    whole_list = function_gener(n, m)
    sum_ = sum_of_list(whole_list)
    redis_db.set(str(self.request.id), str(sum_))
    print('DONE!')


@app.task(bind=True)
def stupid_func(self):
    print('Hello world!')


@app.task(bind=True)
def _try_another_func(self):
    print('try_another_func!')


@app.task(bind=True)
def send_SMS(self, n: int, m: int, k: int):
    time.sleep(1)
    print('SMS SENT!')
    print('Values given: {}, {}, {}'.format(n, m, k))
    print('Their types: {}, {}, {}'.format(type(n), type(m), type(k)))


@app.task(bind=True)
def send_email(self):
    time.sleep(2)
    print('EMAIL SENT')


@app.task(bind=True)
def hard_func(self, n: int, m: int, k: int):
    print('START! FOR N={}, M={}'.format(n, m))
    whole_list = function_gener(n, m)
    sum_ = sum_of_list(whole_list)
    redis_db.set(str(self.request.id), str(sum_))
    print('DONE!')
