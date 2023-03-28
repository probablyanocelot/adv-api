import pika
import json
import os
import django
# from dotenv import load_dotenv
# load_dotenv('.env')

# MQ_HOST = os.getenv('MQ_HOST')
# MQ_PORT = os.getenv('MQ_PORT')
# MQ_USER = os.getenv('MQ_USER')
# MQ_PASSWD = os.getenv('MQ_PASSWD')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
from products.models import Product


params = pika.URLParameters(
    'amqp://myuser:mypassword@rabbitmq:5672?heartbeat=0&blocked_connection_timeout=0')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
