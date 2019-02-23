from celery import Celery
from kombu import Queue
import config

app = Celery('celery_lab')
app.config_from_object(config, namespace='celery')

# app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('SMS'),
    Queue('email'),
    Queue('hard_task'),
)
# task_default_exchange = 'tasks'
# task_default_exchange_type = 'topic'
# task_default_routing_key = 'task.default'
