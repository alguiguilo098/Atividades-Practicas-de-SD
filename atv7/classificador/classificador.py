import pika
import json
import os
from collections import defaultdict

topicos = {
    "futebol": ["futebol", "jogador", "time", "gol","zagueiro","goleiro","prorrogação","bandeirinha","penalti"],
    "voleibol": ["pivô", "saque", "corte", "jogador","vôlei","time","líbero","meio-de-rede","rede"],
}


def classificar_topico_contagem(texto, topicos_palavras_chave):
    contagem = defaultdict(int)
    palavras_texto = texto.lower().split()
    
    for topico, palavras_chave in topicos_palavras_chave.items():
        for palavra in palavras_chave:
            if palavra.lower() in palavras_texto:
                contagem[topico] += 1
    
    return max(contagem, key=contagem.get) if contagem else None


def callback(channel, method, properties, body):
    tweet = json.loads(body)
    print(f'Recebido:\n {tweet}')
    tp = classificar_topico_contagem(tweet['text'], topicos)

    if tp == None:
        pass
    else:
        publish_to_topic(channel, tweet, tp)
    
    channel.basic_ack(delivery_tag=method.delivery_tag)

def publish_to_topic(channel, tweet, topico):
    channel.basic_publish(
        exchange='amq.topic',
        routing_key=topico,
        body=json.dumps(tweet)
    )
    print(f'Tweet: {tweet['id']} classificado como {topico}')


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'))
    )
    channel = connection.channel()

    channel.queue_declare(queue="tweets", durable=True)

    channel.basic_consume(
        queue='tweets',
        on_message_callback=callback,
        auto_ack=False
    )

    print('Classificador aguardando mensagens...')
    channel.start_consuming()


if __name__ == '__main__':
    main()


