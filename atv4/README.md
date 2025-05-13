#Atividade 02 – Sockets UDP

Trabalho desenvolvido para a disciplina Sistemas Distribuídos, ministrada pelo professor Rodrigo Campiolo. 
O objetivo principal é aplicar conceitos de comunicação em rede utilizando o protocolo UDP (User Datagram Protocol), 
explorando suas características de velocidade e ausência de conexão.

## Configuração do Ambiente 

Para instalar o Python, acesse python.org/downloads, baixe a versão recomendada para seu sistema (Windows, macOS ou Linux) e, no Windows, 
marque a opção "Add Python to PATH" antes de instalar.Após a instalação, abra o terminal e digite python --version para confirmar que está
tudo certo — deve aparecer algo como Python 3.10.0 ou superior.

## Problemas Propostos

### Chat P2P (Peer-to-Peer):

Os alunos devem desenvolver um sistema de chat onde os clientes se comunicam diretamente, enviando mensagens entre si. 
Cada mensagem tem um formato específico, contendo o tipo da mensagem, apelido do remetente e o conteúdo. 
Os tipos de mensagem incluem texto comum, emojis, URLs e um modo especial chamado ECHO para indicar que o usuário está ativo.


### Sistema de envio de arquivos via UDP:

O segundo exercício propõe um sistema onde um cliente envia arquivos para um servidor usando o protocolo UDP. 
O arquivo é dividido em partes de até 1024 bytes. O servidor deve validar a integridade do arquivo com um checksum (SHA-1) no final e, 
se estiver tudo certo, salvar o arquivo. Também há  log de transferências, barra de progresso.


## Executando Sistema de envio de arquivos via UDP

1. Acesse o diretório que contém os códigos do cliente e do servidor do sistema de arquivos utilizando o seguinte comando no terminal:

```bash
cd quest2/
```

2. Em seguida, execute o servidor utilizando o comando abaixo, substituindo `<ip>` e `<port>` pelo endereço IP e pela porta desejados:

```bash
python Server.py <ip>:<port>
```

3. Em seguida, excute o Cliente utilizando o seguinte comando abaixo:

```bash
    python Cliente.py
``` 

### Operações do Sistema de Arquivos via UDP
O cliente implementa as seguintes operações principais:

1. **Configurar IP e porta do servidor**
   Permite definir os parâmetros de conexão com o servidor remoto.

2. **Enviar arquivos ao servidor**
   Transfere arquivos do cliente para o servidor utilizando o protocolo UDP.

3. **Listar arquivos locais**
   Exibe os arquivos disponíveis no diretório local do cliente.

4. **Encerrar o cliente**
   Finaliza a aplicação e encerra a conexão com o servidor.

    **OBS**: Digite o numero da operação
    
## Execução do chat P2P UDP

### peer.py
Programa que implementa um peer individual. Para adicionar mais peers abram outros terminais e execute o comando a baixo e siga as instruções que o progama pedir

**Como excutar:**
```bash
python3 peer.py
```

##Bibliotecas Utilizadas
- socket
- struct
- emoji
- threading


=======
