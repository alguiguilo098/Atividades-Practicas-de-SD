# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

#Description: Displays an "Uploading..." message while an image or file is being sent to the server. 
# The process is handled on the client side using a dedicated class that manages 
# file selection, upload, and user feedback.

class BarUpload:
    """
    A class to handle the upload of a file with a progress bar.
    """
    def __init__(self,sizefile:list[bytes],partofimg:int):
        self.sizefile:list[bytes]=sizefile # list of bytes images 
        self.partofimg:int=partofimg # packet of image and file
        self.download:int=0 # percentage dowload
        self.bar=[] # bar progress
    def show_progress(self):
        """Display the current upload progress."""
        if self.download<=100:
            print(f"{self.download}"+"% "+"[",end="")
            self.__printbarpercentage("=",int(self.download)) 
            self.__printbarpercentage("-",int(100-self.download))
            print("".join(self.bar),end="")
            print("]")
            self.bar.clear() # clear bar
        else:
            # mensage upload
            self.__finish_upload()

    def __printbarpercentage(self,icon:str,size:int=5):
        for i in range(size):
            if i%5==0 and i!=0:
                self.bar.append(icon)
    def upload(self,sizebytedowliad:bytes):
        if self.download<=100:
            self.sizefile.append(sizebytedowliad)
            tam=len(self.sizefile) # qtd of packet img
            self.download=int((tam/self.partofimg)*100) # percentage
        else:
            #show mensage uploads
            self.__finish_upload()

    def __finish_upload(self):
        # mensage finish sucess upload
        print("Upload finished")

    def cancel_upload(self):
        # mensge cancel upload
        print("ERROR: Upload cancelled")


