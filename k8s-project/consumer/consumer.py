import pika
import os
from prometheus_client import start_http_server, Counter

# Environment variables for RabbitMQ connection
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'my-rabbitmq')
username = os.getenv('RABBITMQ_USERNAME')
password = os.getenv('RABBITMQ_PASSWORD')

# Prometheus metric to count messages
message_counter = Counter('consumer_messages_count', 'Total number of consumed messages')

def callback(ch, method, properties, body):
    # Increment the counter each time a message is received
    message_counter.inc()
    print("Received %r" % body)

try:
    # Start HTTP server for Prometheus metrics
    start_http_server(9422)

    # Set up RabbitMQ connection and channel
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)

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
