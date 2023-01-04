import os
from faker import Faker
import mysql.connector
import random
from dotenv import load_dotenv

load_dotenv()

host = os.environ['host']
user = os.environ['user']
password = os.environ['password']

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database="databasebd"
)

mycursor = mydb.cursor()

fake = Faker()
Faker.seed(0)

faixa_etaria = ["7 a 14 anos", "10 a 14 anos", "15 a 17 anos",
                "18 a 24 anos", "15 anos ou mais", "25 anos ou mais"]

for h in faixa_etaria:
    mycursor.execute(

        "INSERT INTO databasebd.faixa_etaria (Intervalo) VALUES ('" + h + "')"
    )
    print("INSERT INTO databasebd.faixa_etaria (Intervalo) VALUES (" + h + ")")

mycursor.execute(
    "SELECT ID_Faixa_Etaria FROM databasebd.faixa_etaria")
faixa_etaria = mycursor.fetchall()

for i in range(5):
    cre = (random.randint(1, 100), random.randint(1, 100))
    mycursor.execute(

        f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES {(cre)}")
    print(
        f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES {(cre)}")
    cre_id = mycursor.lastrowid

    for j in range(8):
        bairro = (fake.city(), cre_id)
        mycursor.execute(

            f"INSERT INTO databasebd.bairro (Nome, ID_CRE) VALUES {(bairro)}")
        print(
            f"INSERT INTO databasebd.bairro (Nome, ID_CRE) VALUES {(bairro)}")
        bairro_id = mycursor.lastrowid

        for k in faixa_etaria:
            analfabetismo = (bairro_id, k[0], random.randint(0, 100)/100)
            mycursor.execute(
                f"INSERT INTO databasebd.analfabetismo (ID_Bairro, ID_Faixa_Etaria, Taxa) VALUES {(analfabetismo)}")
            print(
                f"INSERT INTO databasebd.analfabetismo (ID_Bairro, ID_Faixa_Etaria, Taxa) VALUES {(analfabetismo)}")
        for l in range(10):
            escola = (bairro_id, fake.name(), fake.address())
            mycursor.execute(

                f"INSERT INTO databasebd.escola(ID_Bairro, Nome, Endereco) VALUES {(escola)}")
            print(
                f"INSERT INTO databasebd.escola(ID_Bairro, Nome, Endereco) VALUES {(escola)}")

mydb.commit()
mycursor.close()
