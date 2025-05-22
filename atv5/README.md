# Mflix Software

O **Mflix Software** é um sistema distribuído composto por um servidor TCP escrito em **Python** e um cliente desenvolvido em **Java**. Juntos, eles realizam operações CRUD sobre um banco de dados de filmes utilizando o **MongoDB**.
A comunicação entre cliente e servidor é feita de forma eficiente por meio do **Protocol Buffers (Protobuf)**, garantindo velocidade, portabilidade e baixo consumo de rede.

## Objetivo

O objetivo deste projeto é utilizar o **Protocol Buffers** como meio de comunicação entre cliente e servidor por meio de **sockets TCP**. Por ser um protocolo binário, o Protobuf permite uma comunicação mais eficiente e rápida no transporte de dados.
Além disso, ele facilita o desenvolvimento paralelo das funcionalidades do cliente e do servidor, promovendo maior modularidade e produtividade durante a implementação do sistema.

## Configuração do Ambiente

### Pré-requisitos

- Python 3.x
- Java JDK 11 ou superior
- MongoDB
- `protoc(Protocol Buffers Compiler)
- pip (Python Package Installer)


### Configuração Do Servidor (Python)

    1. Clone o repositório:
   ```bash
   git clone https://github.com/alguiguilo098/Atividades-Practicas-de-SD.git
   cd atv5/

   2. Instale o protobuf com o seguinte commando:

   ```bash
   sudo apt install protobuf

   3. Acesse o diretório que possui o codigo do servidor e crie um ambiente virtual:
   ```bash
    cd ./proto_py/
    virtualenv .
    
    4. Posteriormente acesse o ambiente virtual e baixe as dependências
    ```bash
    source ./bin/activete
    pip install -r requeriments.txt

    5. Configure o Atlas no Mongo DB
        
        5.1 Crie uma conta em https://www.mongodb.com/cloud/atlas.

        5.2 Crie um banco de dados e coleção

        5.3 Escolha para versão em python

        5.4 escolha o modelos movies e nomeie como mflix

        5.5 copie a URL no codigo do servidor na 4 linha

        
Copie a string de conexão

Em "Connect" > "Connect your application", copie a URL
    6. Faça deploy do servidor
    ```bash
    python server.py

### Configuração Do Cliente (Java)

    1. Acesse o diretório no qual possui o codigo em java: 
    ```bash
    cd ./proto_java

    2. compile o protobuf:
    ```bash
    mvn compile 

    3.execute o cliente 