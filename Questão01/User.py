from peewee import * 

db= SqliteDatabase('users.db')

class User(Model):

    name = CharField(max_length=50, unique=True)
    password = CharField(max_length=64)

    class Meta:
        database= db
        db_table ="users"
