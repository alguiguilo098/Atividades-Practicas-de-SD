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