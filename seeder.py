import csv
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="databasebd"
)

mycursor = mydb.cursor()

# Lê CSV e insere CREs
with open('./tables/CRE.csv', 'r', newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Número de Escolas"] == 'null' and row["Número de Matriculas"] == 'null':
            insert = f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES (null,null)"
        else:
            cre = (int(row["Número de Matriculas"]),
                   int(row["Número de Escolas"]))
            insert = f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES {(cre)}"
        mycursor.execute(insert)
        print(
            f"INSERT INTO databasebd.cre (Numero_de_Matriculas, Numero_de_Escolas) VALUES {(cre)}")
        mydb.commit()
# Lê CSV de bairros
with open('./tables/Bairro.csv', 'r', newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Cria as faixas etárias

    for field in reader.fieldnames[2:]:
        intervalo = (field)
        mycursor.execute((
            f"INSERT INTO databasebd.faixa_etaria (Intervalo) VALUES ('{(intervalo)}')"))
        print(
            f"INSERT INTO databasebd.faixa_etaria (Intervalo) VALUES ('{(intervalo)}')")

    # Cria bairros e insere relacionamento em Analfabetismo
    for row in reader:
        bairro = (row["Nome"], int(row["ID_CRE"]))
        mycursor.execute(
            f"INSERT INTO databasebd.bairro (Nome, ID_CRE) VALUES {(bairro)}")
        print(
            f"INSERT INTO databasebd.bairro (Nome, ID_CRE) VALUES {(bairro)}")
        id_bairro = mycursor.lastrowid

        mycursor.execute(
            "SELECT ID_Faixa_Etaria, Intervalo FROM databasebd.faixa_etaria")
        for faixa_etaria in mycursor.fetchall():
            analfabetismo = (
                id_bairro, faixa_etaria[0], float(row[faixa_etaria[1]]))
            mycursor.execute(
                f"INSERT INTO databasebd.analfabetismo (ID_Bairro, ID_Faixa_Etaria, Taxa) VALUES {(analfabetismo)}")

# Lê CSV e insere escolas
with open('./tables/Escolas.csv', 'r', newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        escola = (row["Nome"], row["Endereço"], row["Bairro"])
        mycursor.execute(
            f"SELECT ID_BAIRRO FROM databasebd.bairro WHERE Nome like '{escola[2]}'")
        results = mycursor.fetchall()
        if results == []:
            escola = (row["Nome"], row["Endereço"])
            mycursor.execute(
                f"INSERT INTO databasebd.escola (Nome, Endereco) VALUES {escola}")
        else:
            bairro_id = results[0][0]
            escola = (bairro_id, row["Nome"], row["Endereço"])
            mycursor.execute(
                f"INSERT INTO databasebd.escola (ID_Bairro, Nome, Endereco) VALUES {escola}")

    mydb.commit()
