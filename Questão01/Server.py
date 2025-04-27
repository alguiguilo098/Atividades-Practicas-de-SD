
from Utils import *
import threading
def LogicService():
    pathfilesys="./FileSystemServer/"
    configDB()
    conn = configSocketClient()
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
            pass
        elif data[0]=="GETDIR"and user!=None:
            pass
        elif data=="PWD"and user!=None:
            pwd=pathfilesys[18::]
            conn.send(f"Current path:{pwd}".encode())

# if __name__=="__main__":
#     threads=[]
#     for i in range(int(sys.argv[2])):
#         threads.append(threading.Thread(target=LogicService))
#         threads[i].start()
#     for i in range(int(sys.argv[2])):
#         threads[i].join()

if __name__=="__main__":
    LogicService()