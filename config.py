celery_broker_url = 'amqp://localhost'
# celery_broker_url = 'amqp://dmitry:12345@35.202.136.165'
celery_imports = ['celery_lab.tasks']

# celery_task_routes = {
#     'celery_lab.tasks.generate_and_sum_of_lists': {
#         'queue': 'lab.generate_and_sum_of_lists',
#         'exchange': 'lab.generate_and_sum_of_lists',
#         'exchange_type': 'fanout',
#         'routing_key': 'lab.generate_and_sum_of_lists',
#     },
#     'celery_lab.tasks.stupid_func': {
#         'queue': 'lab.func',
#         'exchange': 'lab.func',
#         'routing_key': 'lab.func',
#     }
# }

# celery_task_routes = {
#     'celery_lab.tasks.generate_and_sum_of_lists': {
#         'queue': 'lab.generate_and_sum_of_lists',
#         'exchange': 'lab.generate_and_sum_of_lists',
#         'routing_key': 'lab.generate_and_sum_of_lists',
#     },
#     'celery_lab.tasks.stupid_func': {
#         'queue': 'lab.generate_and_sum_of_lists',
#         'exchange': 'lab.generate_and_sum_of_lists',
#         'routing_key': 'lab.generate_and_sum_of_lists',
#     }
# }
