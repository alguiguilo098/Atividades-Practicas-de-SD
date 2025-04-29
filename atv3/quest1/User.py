# Name: Guilherme Almeida Lopes
# Name: Hugo Okumura

# Create: 24-04-2025 
# Last modified: 27-04-2025

# Description: This is the User code  defined in the database
from peewee import * 

db= SqliteDatabase('users.db')

# Define the User model
class User(Model):

    # Define the fields for the User model
    name = CharField(max_length=50, unique=True)
    password = CharField(max_length=64)

    # Define the fields for the User model
    class Meta:
        database= db
        db_table ="users"
