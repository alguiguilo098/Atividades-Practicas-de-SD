import pika
import os
import json
import threading
import time
import random

import pika.exceptions


class AssinanteThread(threading.Thread):
    def __init__(self, topico):
        threading.Thread.__init__(self)
        self.topico = topico

    def run(self):
        credenciais = pika.PlainCredentials(
            os.getenv('RABBITMQ_USER','guest'),
            os.getenv('RABBITMQ_PASS', 'guest')
        )
        parametros = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
            credentials=credenciais,
            connection_attempts=5,
            retry_delay=20
        )
        for i in range(5):
            try:
                connetion = pika.BlockingConnection(parametros)
            except pika.exceptions.AMQPConnectionError as e:
                time.sleep(20)
        channel = connetion.channel()

        channel.exchange_declare(
            exchange='topicos',
            exchange_type='topic',
            durable=True
        )

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(
            exchange='topicos',
            queue=queue_name,
            routing_key=self.topico
        )

        def callback(ch, method, properties, body):
            tweet = queue_name
            print(f"{self.topico} {tweet['text']}")
        
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        channel.start_consuming()


def main():
    topicos = os.getenv('TOPICOS', '').split(',')
    thread_count = int(os.getenv('THREAD_COUNT','1'))
    n_top = len(topicos)

    print(topicos)
    print(thread_count)
    threads = []
    for i in range(thread_count):
        thread = AssinanteThread(topicos[random.randint(0,n_top-1)])
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('encerrando')




if __name__ == "__main__":
    main()