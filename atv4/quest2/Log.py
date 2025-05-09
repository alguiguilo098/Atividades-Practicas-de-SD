import logging
import os
class Log:
    def __init__(self,path,level):
        with open(path,mode="+a"):
            print("Criando arquivo de log ...")
        
        logging.basicConfig(filename=path,level=level,
        format='%(asctime)s - %(levelname)s - %(message)s')

    def writeInfo(self,msg:str):
        logging.info(msg)

    def writeError(self,msg:str):
        logging.error(msg)

if __name__=="__main__":
    log=Log('./Client/Log/calvocliente.log',level=logging.INFO)
    log.writeInfo("calvo123")
    log.writeError("calvomorreusemcabelo")