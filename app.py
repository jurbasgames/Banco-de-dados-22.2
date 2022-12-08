# save this as app.py
from flask import Flask
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)

app = Flask(__name__)


@app.route("/")
def Index():
    return "Hello, World!"


mydb.close()
