import json
import os
import time
import pika
import sys
def load_json(file_path):
    """
    Load a JSON file and return its content.

    :param file_path: Path to the JSON file.
    :return: Content of the JSON file as a list of dictionaries
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from file {file_path}: {e}")
    return data

def createqueue(queue_name):
    print("Host:", os.getenv('RABBITMQ_HOST'))
    print("Port:", os.getenv('RABBITMQ_PORT'))

    host = os.getenv('RABBITMQ_HOST', 'localhost')  # valor padrão
    port = int(os.getenv('RABBITMQ_PORT', '5672'))

    connection_params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    print(f"Queue '{queue_name}' criada em {host}:{port}")
    return channel, connection


def publish_message(channel, queue_name, data):
    """
    Publish messages to a RabbitMQ queue.

    :param channel: RabbitMQ channel to use for publishing
    :param queue_name: Name of the queue to publish to
    :param data: List of tweet dictionaries to publish
    """
    for i in data:
        message = json.dumps(i)
        print(f"Publishing message: {message}")
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message
        )
        print(f"Message published to queue '{queue_name}'")

def main():
    channel, connection = createqueue("tweets")
    json_data = load_json('tweets.json')
    publish_message(channel, "tweets", json_data)
    connection.close()
    channel.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
