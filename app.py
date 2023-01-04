# save this as app.py
import os
import matplotlib.pyplot as plt
import mysql.connector
from flask import Flask, render_template, request
import matplotlib
from dotenv import load_dotenv

load_dotenv()
matplotlib.use('Agg')

host = os.environ['host']
user = os.environ['user']
password = os.environ['password']

app = Flask(__name__)


mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database="databasebd"
)


@app.route("/")
def Index():
    mycursor = mydb.cursor()
    if request.args.get("search"):
        search = "%{}%".format(request.args["search"])
        sql = f"SELECT Nome, ID_CRE, ID_Bairro FROM databasebd.bairro WHERE LOWER(Nome) LIKE LOWER('{search}')"
    else:
        sql = "SELECT Nome, ID_CRE, ID_Bairro FROM databasebd.bairro"
    mycursor.execute(sql)
    bairros = mycursor.fetchall()
    mycursor.close()
    return render_template("index.html", bairros=bairros, search=request.args.get("search"))


@app.route("/sobre")
def Sobre():
    return render_template("sobre.html")


@app.route("/bairro/<id>")
def Bairro(id):
    mycursor = mydb.cursor()
    mycursor.execute(
        f"SELECT Nome, ID_CRE FROM databasebd.bairro WHERE ID_Bairro = {id}")
    bairro = mycursor.fetchall()[0]
    # ============================================================================

    mycursor.execute(
        f"SELECT Intervalo, Taxa FROM (analfabetismo NATURAL JOIN faixa_etaria) NATURAL JOIN bairro WHERE ID_Bairro={id} ORDER BY Intervalo DESC")
    results1 = mycursor.fetchall()
    eixoX = [results1[0][0], results1[1][0], results1[2]
             [0], results1[3][0], results1[4][0], results1[5][0]]
    eixoY = [results1[0][1], results1[1][1], results1[2]
             [1], results1[3][1], results1[4][1], results1[5][1]]
    plot(eixoX, eixoY, "Intervalo",
         "Porcentagem", f"Analfabetismo em {bairro[0]}", bairro[0]+'_analfabetismo.png')
    # ============================================================================
    mycursor.execute(
        f"SELECT Extrema_Pobreza, Pobreza, Baixa_Renda, Acima_Meio_SM FROM bairro WHERE ID_Bairro={id}")
    results2 = mycursor.fetchall()
    eixoX = ["Extrema Pobreza", "Pobreza", "Baixa Renda", "Acima de meio S.M."]
    eixoY = [results2[0][0], results2[0][1], results2[0][2], results2[0][3]]
    plot(eixoX, eixoY, "", "Nº de famílias",
         f"Renda e Bolsa Família em {bairro[0]}", bairro[0]+'_renda.png')
    mycursor.close()
    return render_template("bairro.html", bairro=bairro,)


def plot(eixoX, eixoY, labelX, labelY, title, bairro):
    plt.bar(eixoX, eixoY, color='blue', width=0.8)
    plt.xlabel(labelX)
    plt.xticks(rotation=90)
    plt.ylabel(labelY)
    plt.title(title)
    plt.savefig(f"./static/{bairro}", bbox_inches="tight")
    plt.close("all")
