import pika
import os
import json
import time
import threading
# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: Assinantes de mensagens de tópicos específicos do RabbitMQ.
# Este script consome mensagens de tópicos específicos do RabbitMQ e imprime as notificações recebidas.
class AdptarorRabbitMQ:
    """Adaptador para consumir mensagens de um tópico específico do RabbitMQ"""
    def __init__(self, topico):
        self.notify = []
        self.topico = topico

    def callback(self, ch, method, properties, body):
        """
        Callback para processar mensagens recebidas do RabbitMQ
        """
        tweet = json.loads(body)
        self.notify.append(tweet["mensagem"])
        print(f"[x] Nova mensagem recebida: {tweet['mensagem']}")
        if len(self.notify)==5:
            ch.stop_consuming()

    def run(self):
        """
            Iniciar a conexão com o RabbitMQ e consumir mensagens do tópico específico
        """
        parametros = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
            connection_attempts=5,
            retry_delay=5
        )

        connection = None
        for tentativa in range(5):
            try:
                # Tenta conectar ao RabbitMQ
                connection = pika.BlockingConnection(parametros)
                print(f"Conectou com o broker. Tentativa: {tentativa + 1}")
                break
            except pika.exceptions.AMQPConnectionError as e:
                # Se falhar, espera e tenta novamente
                print(f'Tentativa {tentativa + 1}/5: {str(e)}')
                time.sleep(5)

        if not connection:
            # Se não conseguir conectar, encerra o processo
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
        # Declara a fila de consumo
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )

        print(f"[*] Aguardando mensagens no tópico '{self.topico}'. Pressione Ctrl+C para sair.")
        # Inicia o consumo de mensagens
        channel.start_consuming()

def print_noify(notify, thread_id):
    print(f"Assinante {thread_id} rebeceived messages:")
    for mensagem  in notify:
        print(f"Assinante {thread_id} - Mensagem: {mensagem}")
    
def main():
    # Configurações do AdptadorRabbitMQ
    adaptador_futebol = AdptarorRabbitMQ("futebol")
    adaptador_volei = AdptarorRabbitMQ("volei")
    try:
        # consumir mensagens 
        adaptador_futebol.run()
        adaptador_volei.run()

        # conseguir variaveis de ambientes do docker container
        threads_futebol= os.getenv("THREADS_FUTEBOL", 2)
        threads_volei = os.getenv("THREADS_VOLEI",2)
        threads_ambos=  os.getenv("THREADS_AMBOS", 2)

        threads=[]
        for  i in range(int(threads_futebol)):
            # Criar e iniciar threads para imprimir notificações de volei
            t1=threading.Thread(target=print_noify, args=(adaptador_futebol.notify.copy(), i))
            threads.append(t1)
            t1.start()
        
        for i in range(int(threads_volei)):
            # Criar e iniciar threads para imprimir notificações de volei
            t2=threading.Thread(target=print_noify, args=(adaptador_volei.notify.copy(),int(threads_futebol)+i))
            threads.append(t2)
            t2.start()
        

        for i in range(int(threads_ambos)):
            # Criar e iniciar threads para imprimir notificações de ambos os espotes
            t3=threading.Thread(target=print_noify, args=(adaptador_volei.notify.copy()+adaptador_futebol.notify.copy(),int(threads_futebol)+int(threads_volei)+i))
            threads.append(t3)
            t3.start()
        for t in threads:
            # Aguardar a conclusão de todas as threads
            t.join()
        
    except KeyboardInterrupt:
        print('Encerrando')


if __name__ == "__main__":
    main()
