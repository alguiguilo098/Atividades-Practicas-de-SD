# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura
from  SocketsUtil.SocketServer import SocketUDPServer
import sys
if __name__=="__main__":
    ip,port=sys.argv[1].split(":")
    serverudp=SocketUDPServer(int(port),ip)
    serverudp.getfile()
