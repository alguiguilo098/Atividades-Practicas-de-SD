
class BarUpload:
    """
    A class to handle the upload of a file with a progress bar.
    """
    def __init__(self,sizefile:list[bytes],partofimg:int):
        self.sizefile:list[bytes]=sizefile
        self.partofimg:int=partofimg
        self.download:int=0
        self.bar=[]
    def show_progress(self):
        """Display the current upload progress."""
        if self.download<=100:
            print(f"{self.download}"+"% "+"[",end="")
            self.__printbarpercentage("=",int(self.download))
            self.__printbarpercentage("-",int(100-self.download))
            print("".join(self.bar),end="")
            print("]",end="")
            print()
            self.bar.clear()
        else:
            self.__finish_upload()

    def __printbarpercentage(self,icon:str,size:int=5):
        for i in range(size):
            if i%5==0 and i!=0:
                self.bar.append(icon)
    def upload(self,sizebytedowliad:bytes):
        if self.download<=100:
            self.sizefile.append(sizebytedowliad)
            tam=len(self.sizefile)
            self.download=int((tam/self.partofimg)*100)
        else:
            self.__finish_upload()
    def __finish_upload(self):
        print("Upload finished")
    def cancel_upload(self):
        print("ERROR: Upload cancelled")


if __name__== "__main__":
    bar=BarUpload([],3)
    bar.show_progress()
    bar.upload(bytes(1024))
    bar.show_progress()
    bar.upload(bytes(1024))
    bar.show_progress()
    bar.upload(bytes(1024))
    bar.show_progress()
    bar.upload(bytes(1024))
    bar.show_progress()