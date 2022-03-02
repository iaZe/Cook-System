import os
import sqlite3
from sqlite3 import Error

banco = sqlite3.connect('database.db')
cursor = banco.cursor()

pastaApp=os.path.dirname(__file__)
nomeBanco=pastaApp+"\\database.db"

def ConexaoBanco():
    con=None
    try:
        con=sqlite3.connect(nomeBanco)
    except Error as ex:
        print(ex)
    return con

def dql(query): #Select
    vcon=ConexaoBanco()
    c=vcon.cursor()
    c.execute(query)
    res=c.fetchall()
    vcon.close()
    return res

def dml(query): #Insert, Update, Delete
    try:
        vcon=ConexaoBanco()
        c=vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
    except Error as ex:
        print(ex)
    