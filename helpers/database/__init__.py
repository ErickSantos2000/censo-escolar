import sqlite3

# define uma constante e guarda o nome do arquivo que representa o banco de dados em um variavel global
DATABASE = 'censoescolar.db'

# define uma função que encaspula a logica de conexão
def get_connection():
    conn = sqlite3.connect(DATABASE)
    # retorna o obj de conexão
    return conn