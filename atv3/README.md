## Descrição da Atividade 1 – Programação com Sockets TCP

    Disciplina: Sistemas Distribuídos
    Professor: Rodrigo Campiolo

## Objetivo
    Esta atividade tem como objetivo desenvolver a habilidade de programação em redes utilizando Sockets 
    TCP, com foco na criação de servidores multiclientes, comunicação baseada em comandos e 
    manipulação de arquivos e diretórios de forma remota. A atividade é dividida em duas partes:
    
## Configuração Do ambiente
    
    1. Primeiramente clone o repositório:

    ```bash
        git clone "<URL>"
    ```
    
    2. Instalar o python na sua máquina usando o comando:

    ```bash
        sudo dnf install python3 python3virtualenv
    ```

    ou

    ```bash
        sudo apt install python3 python3virtualenv
    ```

    3. Posteriomente  crie um ambiente virtual com o seguinte comando:

    ```bash
        virtualenv .venv
    ```

    3. Posteriomente  ative o ambiente virtual:

    ```bash
        source .venv/bin/activete
    ```
    
    4. Posteriomente  ative o ambiente virtual:

    ```bash
        source .venv/bin/activete
    ```
# FileServer.py

<ol>
<li> Como executar

> python3 FileServer.py 
</ol>

# FileClients.py

<ol>
<li> Como executar

> python3 FileClients.py
</li>
</ol>

## Exemplo de uso

    1. Executar FileServer.py
    2. Em um outro terminal executar FileClient.py
    3. No diretório criado automaticamente pelo FileClient crie um arquivo de teste
    4. no terminal executando FileClient digite:
        -> 1 nomedoarquivo.tipodoarquivo
        ou
        -> ADDFILE  nomedoarquivo.tipodoarquivo
    5. Veja as mensagens de resposta
    6. digite:
        -> 5
        ou
        -> SAIR
        para finalizar o processo do cliente


## Bibliotecas usadas
- os
- socket
- logging
- struct
- peewee
