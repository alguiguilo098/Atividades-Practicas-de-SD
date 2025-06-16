import pika
import json
import os
import time
from collections import defaultdict
import re
# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 16-06-2025 
# Last modified: 16-06-2025

# Description: Classificador de tweets por tópicos usando RabbitMQ.
# Este script consome tweets de uma fila RabbitMQ, classifica-os em tópicos específicos
#  com base em palavras-chaves

# Palavras-chave por tópico
topicos = {
    "futebol": ["futebol", "jogador", "time","clássico","técnico",
                 "gol", "zagueiro", "goleiro","golaço","Brasileirão...",
                 "prorrogação", "bandeirinha", "penalti"],
    "volei": ["pivô", "saque", "corte","bloqueio", 
                 "jogador", "vôlei", "time","pedreira",
                 "líbero", "meio-de-rede", "rede"],
}

# Função de classificação por contagem de palavras-chave
def classificar_topico_contagem(texto, topicos_palavras_chave):
    contagem = defaultdict(int)
    
    # Tokenização simples, removendo pontuação e convertendo para minúsculas
    palavras_texto = re.findall(r'\b\w+\b', texto.lower())

    for topico, palavras_chave in topicos_palavras_chave.items():
        for palavra in palavras_chave:
            contagem[topico] += palavras_texto.count(palavra.lower())
    
    if not contagem:
        return None

    # Retorna o tópico com maior contagem
    topico_mais_relevante = max(contagem, key=contagem.get)
    
    # Caso todas as contagens sejam 0
    if contagem[topico_mais_relevante] == 0:
        return None

    return topico_mais_relevante


# Callback para cada mensagem recebida
def callback(channel, method, properties, body):
    tweet = json.loads(body)
    
    tp = classificar_topico_contagem(tweet['mensagem'], topicos)
    print(f'Recebido:\n {tweet['mensagem']}\n Tópico: {tp}')
    tweet["topico"]=tp
    if tp:
        publish_to_topic(channel, tweet, tp)

    channel.basic_ack(delivery_tag=method.delivery_tag)

# Publica o tweet classificado no tópico correspondente
def publish_to_topic(channel, tweet, topico):
    channel.basic_publish(
        exchange='topicos',
        routing_key=topico,
        body=json.dumps(tweet)
    )
    print(f"Tweet: {tweet['id']} classificado como {topico}")

# Função principal
def main():

    print(f'Host: {os.getenv('RABBITMQ_HOST','guest')}')
    print(f'Port: {os.getenv('RABBITMQ_PORT', '5672')}')

    parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', '5672')),
        connection_attempts=5,
        retry_delay=20
    )

    for tentativa in range(5):
        try:
            connection = pika.BlockingConnection(parameters)
            print(f'Conexão com RabbitMQ concluída, tentativas:{tentativa}')
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f'Tentativa {tentativa+1}/5: {str(e)}')
            time.sleep(20)

    channel = connection.channel()

    #Fila de consumo
    channel.queue_declare(queue="tweets", durable=True)
    channel.basic_consume(
        queue='tweets',
        on_message_callback=callback,
        auto_ack=False
    )

    # Filas de tópicos
    channel.exchange_declare(
        exchange='topicos',
        exchange_type='topic',
        durable=True
    )
    for key in topicos.keys():
        channel.queue_declare(queue=str(key), durable=True)

        channel.queue_bind(
            exchange='topicos',
            queue=str(key),
            routing_key=str(key)
        )


    print('Classificador aguardando mensagens...')
    channel.start_consuming()

# Executa o programa
if __name__ == "__main__":
    main()
