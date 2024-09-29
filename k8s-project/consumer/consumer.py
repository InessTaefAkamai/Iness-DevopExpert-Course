import pika
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'my-rabbitmq')
username = os.getenv('RABBITMQ_USERNAME')
password = os.getenv('RABBITMQ_PASSWORD')

try:
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)

    def callback(ch, method, properties, body):
        print("Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()
