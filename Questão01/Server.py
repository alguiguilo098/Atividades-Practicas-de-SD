from User import *
import sys
import hashlib
from SocketServerOwn import ServerSocket
import os 

if __name__=="__main__":

    pathfilesys="../FileSystem/"

    db.connect()
    db.create_tables([User])

    user=None
    
    print("Initializing Server...")

    socketserver=ServerSocket('localhost', int(sys.argv[1]),int(sys.argv[2]))
    (conn,host)=socketserver.accept()

    print("Server started")

    while True:
        data=conn.recv(1024).decode().split(" ")
        if data[0]=="EXIT":
            conn.send(f"User {data[1]} disconnected".encode())
        if data[0]=="CONNECT":
            pass
        elif data[0]=="CREATEUSER":
            passsha256=hashlib.sha256(data[1].encode()).hexdigest()
            user=User(name=data[1],password=passsha256)
            user.save()
            conn.send("User created")
        