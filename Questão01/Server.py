
from Utils import *
import threading

def LogicService(port:int):
    pathfilesys="./FileSystemServer/"
    configDB()
    conn = configSocketClient(port)
    user=None
    while True:
        data=conn.recv(1024).decode()
        if data!="PWD":
            print("Não pwd")
            data=data.split(" ")

        print(f"Received data: {data}")
        if data[0]=="EXIT":
            print(f"User {data[1]} disconnected")
            sys.exit(0)
        elif data[0]=="CONNECT":
            user=connect(conn, data)
        elif data[0]=="CREATEUSER":
            create_user(conn, data)
        elif data[0]=="CHDIR" and user!=None:
            pathfilesys=change_directory(conn, data, pathfilesys)
            print(pathfilesys)
        elif data[0]=="GETFILE" and user!=None:
            print("entrou no getfile")
            handle_getfiles(conn, pathfilesys)
        elif data[0]=="GETDIR"and user!=None:
            print("entrou no getdir")
            handle_getdirs(conn,pathfilesys)
        elif data=="PWD"and user!=None:
            pwd=pathfilesys[18::]
            conn.send(f"Current path:{pwd}".encode())
        else:
            print("Invalid command")


if __name__=="__main__":
    threads=[]
    pos=2
    for i in range(int(sys.argv[1])):
        threads.append(threading.Thread(target=LogicService,args=(int(sys.argv[pos]),)))
        pos+=1

    for th in threads:
        th.start()

    for th in threads:
        th.join()
