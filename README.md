## Celery lab with Flask
This repo is fully based on this one:
https://github.com/DmitriiDenisov/celery_lab

Basically it adds small API using Flask which is stored in celery_lab/web/app.py 

### Reminder for RabbitMQ
https://github.com/DmitriiDenisov/rabbitmq_lab

## Launch Flask app:
1. Run celery_lab/web/app.py
2. Make POST/GET requests (via Postman for example):
Examples:
http://127.0.0.1:5001/email_and_sms
http://127.0.0.1:5001/stupid-task
http://127.0.0.1:5001/home

## Remote broker / Remote worker:
Change in config.py file: 

``` celery_broker_url = 'amqp://{user}:{password}@{ip}' ```

For example:
``` celery_broker_url = 'amqp://one_user:12345@35.202.136.165' ```

## Launch worker on your Machine:
Just an example how to launch worker:

```celery worker --concurrency 3 -A celery_lab.celery_settings -Q SMS,email```

--concurrency - number of concurrent processes, default: 4

-A - entry point. In the example above it is ~/celery_lab/celery_settings.py

-Q - list queues you want to listen to. For example, -Q SMS,email or -Q SMS,email,hard_task


## Know IP in local network (MacOS)
Sotlight -> Network Utility либо в terminal выполнить `ifconfig` и найти параметр en0: inet 


## If Remote broker does not work:
In case of error: [Errno 61] Connection refused. That means that you are trying to connect to local Rabbit
It is known issue, proof: https://superuser.com/questions/464311/open-port-5672-tcp-for-access-to-rabbitmq-on-mac

1) Print 'hostname' in terminal. For example you will see 'MacBook-Air-2.local'
2) ``` nano /usr/local/etc/rabbitmq/rabbitmq-env.conf ```
3) Edit:

```NODE_IP_ADDRESS=0.0.0.0```
```NODENAME=rabbit@MacBook-Air-2```
4) Save it: - Ctrl-O, Enter, Ctrl-x, Enter
5) ```brew services restart rabbitmq```
6) Add new user in RabbitMQ and do not forget to set permissions for it in web-inteface
7) Launch worker via ```celery worker ...```