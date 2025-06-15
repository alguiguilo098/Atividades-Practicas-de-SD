import pika
import os
import json
import threading
import time
import random

import pika.exceptions


class AssinanteThread(threading.Thread):
    def __init__(self, topico, assinante):
        threading.Thread.__init__(self)
        self.topico = topico
        self.assinante = assinante

    def callback(self, ch, method, properties, body):
        tweet = json.loads(body)
        print(f"Assinante {self.assinante} Recebeu:\n {self.topico}:{tweet['mensagem']}")

    def run(self):
        print(f'Assinante {self.assinante} inscrito no tópico {self.topico}')

        parametros = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
            connection_attempts=5,
            retry_delay=20
        )
        for tentativa in range(5):
            try:
                connetion = pika.BlockingConnection(parametros)
                print(f"Assinante {self.assinante}: conectou com o broker. tentativas: {tentativa}")
            except pika.exceptions.AMQPConnectionError as e:
                print(f'Tentativa {tentativa+10}/5: str{str(e)}')
                time.sleep(20)

        channel = connetion.channel()

        channel.exchange_declare(
            exchange='topicos',
            exchange_type='topic',
            durable=True
        )

        result = channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue

        channel.queue_bind(
            exchange='topicos',
            queue=self.queue_name,
            routing_key=self.topico
        )
        
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
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
        print(i)
        thread = AssinanteThread(topicos[random.randint(0,n_top-1)],i)
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