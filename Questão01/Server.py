from User import *
import os 

if __name__=="__main__":
    db.create_tables([User])

    uncle_bob = User(name='Bob', password="1234")
    uncle_bob.save() 