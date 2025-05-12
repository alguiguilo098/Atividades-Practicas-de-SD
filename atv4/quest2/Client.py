from UserInter.Menu import ClientMenu
import time
if __name__=="__main__":
    print("Inicializando cliente...") 
    time.sleep(1)
    print("Configurando Menu...") 
    path_abs="./Client/Images/"
    time.sleep(1)
    menu=ClientMenu(pathmenu=path_abs) # create menu 
    try:
        menu.run() # run interface 
    except Exception as e:
        print(e) #  show error
        
