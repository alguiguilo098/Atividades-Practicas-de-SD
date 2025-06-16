
# Serviço de Notificação de Tweets

Este projeto implementa um sistema de coleta, processamento, classificação e notificação de **tweets**, utilizando serviços de mensageria como **RabbitMQ**. O sistema é composto por módulos de **coletor**, **classificador** e **assinantes**, e utiliza **Docker Compose** para orquestração.

### Funcionalidades

* Coleta de tweets (arquivo `.json` ou fonte externa).
* Envio dos tweets para uma fila de mensagens.
* Classificação dos tweets por palavras-chave em tópicos como "futebol", "vôlei", etc.
* Notificação automática para assinantes com base nos tópicos desejados.

---

## Como executar

Certifique-se de que você tenha o **Docker** e o **Docker Compose** instalados em sua máquina.

### 1. Iniciar os serviços(No dirtório raiz do projeto)

Execute no terminal:

```bash
docker compose up -d
```

Esse comando irá:

* Criar e subir os containers definidos no `docker-compose.yml`.
* Inicializar os módulos de coletor classificador, fila (RabbitMQ), e assinantes.

### 2. Parar os serviços

Para desligar e remover os containers:

```bash
docker compose down
```

Isso encerrará todos os containers e liberará os recursos utilizados.

---

## 🛠️ Estrutura do Projeto

```
.
├── coletor/
│   └── coletor.py
├── classificador/
│   └── classificador.py
├── assinante/
│   └── assinante.py
├── docker-compose.yml
├── requisitos.txt
└── README.md
```

## 📌 Requisitos

* Docker
* Docker Compose
