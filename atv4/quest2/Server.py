# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 9-05-2025 
# Last modified: 12-04-2025


# Description: This script initializes a UDP server using a custom SocketUDPServer class.
#  It takes an IP and port from the command line in the format IP:PORT, starts the server, 
# and continuously listens for incoming data using the getfile()

from  SocketsUtil.SocketServer import SocketUDPServer # server Socket UDP
import sys # arguments terminal

def UDPsocket(ip:str,port:int):
    serverudp=SocketUDPServer(int(port),ip)
    while True:
        serverudp.getfile() # Upload file of client 

if __name__=="__main__":
    ip,port=sys.argv[1].split(":")
    UDPsocket()
