from peewee import * 

db= SqliteDatabase('users.db')

class User(Model):

    name = CharField()
    password = CharField()

    class Meta:
        database= db
        db_table ="users"
