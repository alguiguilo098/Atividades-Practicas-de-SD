# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: Implements a message logging system to log messages to a file,
# using the logging module to record messages with different severity levels (INFO, ERROR).

import logging 

class Log:
    def __init__(self, path, level=logging.INFO):
        # Isso é feito apenas para garantir que o arquivo exista
        with open(path, mode="a+"):  
            print("Criando arquivo de log ...")
        
        # Configura o sistema de logging para registrar mensagens em arquivo
        logging.basicConfig(
            filename=path,      # Caminho do arquivo de log
            level=level,        # Nível mínimo de severidade a ser registrado (ex: logging.INFO)
            format='%(asctime)s - %(levelname)s - %(message)s'  # Formato das mensagens de log
        )

    def writeInfo(self, msg: str): 
        # Registra uma mensagem com nível INFO no log
        logging.info(msg)

    def writeError(self, msg: str):
        # Registra uma mensagem com nível ERROR no log
        logging.error(msg)
