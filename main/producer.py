import pika, json

params = pika.URLParameters(
    'amqp://myuser:mypassword@rabbitmq:5672?heartbeat=0&blocked_connection_timeout=0')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
