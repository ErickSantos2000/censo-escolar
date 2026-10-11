import sqlite3
from flask import g

# define uma constante e guarda o nome do arquivo que representa o banco de dados em um variavel global
DATABASE = 'censoescolar.db'



# define uma função que encaspula a logica de conexão
def get_conn():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    # retorna o obj de conexão
    return g.db

def close_conn(exception):
    # pega o 'db' de dentro do 'g' e o remove, retornando None se não existir
    db = g.pop('db', None)

    if db is not None:
        db.close() # fecha a conexão