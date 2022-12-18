import csv
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="databasebd"
)

mycursor = mydb.cursor()

with open('./tables/CRE.csv', 'r', newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        cre = (int(row["Número de Matriculas"]), int(row["Número de Escolas"]))
        mycursor.execute(
            f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES {(cre)}")
        print(
            f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES {(cre)}")

    mydb.commit()
