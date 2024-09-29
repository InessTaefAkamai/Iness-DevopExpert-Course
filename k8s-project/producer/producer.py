import pika
import os
import time

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'my-rabbitmq')
username = os.getenv('RABBITMQ_USERNAME')
password = os.getenv('RABBITMQ_PASSWORD')

try:
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)

    while True:
        message = 'Hello World!'
        channel.basic_publish(exchange='', routing_key='hello', body=message,
                              properties=pika.BasicProperties(delivery_mode=2))  # Make message persistent
        print(f"Sent: {message}")
        time.sleep(20)

except pika.exceptions.AMQPConnectionError as e:
    print(f"Connection error: {e}")
except KeyboardInterrupt:
    print("Producer stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()
