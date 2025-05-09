import logging

class Log:
    def __init__(self,path:str,level):
        logging.basicConfig(filename=path,level=level,format='%(asctime)s - %(levelname)s - %(message)s')
    def writeInfo(self,msg:str):
        logging.info(msg)

    def writeError(self,msg:str):
        logging.error(msg)

if __name__=="__main__":
    log=Log('./Server/Log.log',level=logging.INFO)
    log.writeInfo("calvo 123")
    log.writeError("calvo morreu sem cabelo")