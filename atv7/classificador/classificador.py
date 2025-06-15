import pika
import json
import os
import time
from collections import defaultdict

# Palavras-chave por tópico
topicos = {
    "futebol": ["futebol", "jogador", "time",
                 "gol", "zagueiro", "goleiro",
                 "prorrogação", "bandeirinha", "penalti"],
    "voleibol": ["pivô", "saque", "corte", 
                 "jogador", "vôlei", "time",
                 "líbero", "meio-de-rede", "rede"],
}

# Função de classificação por contagem de palavras-chave
def classificar_topico_contagem(texto, topicos_palavras_chave):
    contagem = defaultdict(int)
    palavras_texto = texto.lower().split()
    
    for topico, palavras_chave in topicos_palavras_chave.items():
        for palavra in palavras_chave:
            if palavra.lower() in palavras_texto:
                contagem[topico] += 1
    
    return max(contagem, key=contagem.get) if contagem else None

# Callback para cada mensagem recebida
def callback(channel, method, properties, body):
    tweet = json.loads(body)
    print(f'Recebido:\n {tweet}')
    
    tp = classificar_topico_contagem(tweet['mensagem'], topicos)

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
    credenciais = pika.PlainCredentials(
        os.getenv('RABBITMQ_HOST','guest'),
        os.getenv('RABBITMQ_PASS','guest')
    )
    print(f'Host: {os.getenv('RABBITMQ_HOST','guest')}')
    print(f'Port: {os.getenv('RABBITMQ_PORT', '5672')}')



    parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', '5672')),
        credentials=credenciais,
        connection_attempts=5,
        retry_delay=20
    )

    for tentativa in range(5):
        try:
            connection = pika.BlockingConnection(parameters)
            print(f'Conexão com RabbitMQ concluída, tentativas:{tentativa}')
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f'Tentativa {tentativa+1}/5: str({e})')
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
    # print(topicos.keys())
