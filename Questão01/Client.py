import hashlib
import sys
from SocketCliente  import SocketClient

if __name__=="__main__":
    print("Initializing Client...")
    socketclient=SocketClient()
    socketclient.connect('localhost', int(sys.argv[1]))
    socket=socketclient.socket
    print("Connected to server")
    path:str="/"
    while True:
        print(f"$[{path}]:",end="")
        command=input().split(" ")
        if command[0]=="EXIT":
            break
        elif command[0]=="CONNECT":
            pass
        elif command[0]=="CREATEUSER":
            print("Username:",end="")
            username=input()
            print("Password:",end="")
            password=input()
            passha256=hashlib.sha256(password.encode()).hexdigest()
            socket.send(f"CREATEUSER {username} {passha256}".encode())
