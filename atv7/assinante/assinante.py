import pika
import os
import json
import time


class AdptarorRabbitMQ:
    def __init__(self, topico):
        self.notify = []
        self.topico = topico

    def callback(self, ch, method, properties, body):
        tweet = json.loads(body)
        self.notify.append(tweet["mensagem"])
        print(f"[x] Nova mensagem recebida: {tweet['mensagem']}")
        if len(self.notify)==6:
            ch.stop_consuming()

    def run(self):
        parametros = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
            connection_attempts=5,
            retry_delay=5
        )

        connection = None
        for tentativa in range(5):
            try:
                connection = pika.BlockingConnection(parametros)
                print(f"Conectou com o broker. Tentativa: {tentativa + 1}")
                break
            except pika.exceptions.AMQPConnectionError as e:
                print(f'Tentativa {tentativa + 1}/5: {str(e)}')
                time.sleep(5)

        if not connection:
            print("Não foi possível conectar ao RabbitMQ.")
            return

        channel = connection.channel()

        # Usando tópico em vez de fanout
        channel.exchange_declare(
            exchange='topicos',
            exchange_type='topic',
            durable=True
        )

        result = channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue

        # Vincula com chave de roteamento
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
        print(f"[*] Aguardando mensagens no tópico '{self.topico}'. Pressione Ctrl+C para sair.")
        channel.start_consuming()


def main():
    topico = "futebol"  # escolha um tópico válido
    adaptador_volei = AdptarorRabbitMQ("volei")
    try:
        adaptador_volei.run()

    except KeyboardInterrupt:
        print(adaptador_volei.notify)
        print('Encerrando')


if __name__ == "__main__":
    main()
