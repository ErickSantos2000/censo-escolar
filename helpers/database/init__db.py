import sqlite3

connection = None

try:
    # abre com conexão com banco
    connection = sqlite3.connect('censoescolar.db')

    # abre arquivo de comando para definir estrutura do banco
    with open('scheme.sql') as file:
        # le e executa todos os camandos sql
        connection.executescript(file.read())

    # salva pernamentemente o as alteraçoes
    connection.commit()

except sqlite3.Error as e:
    print(f"O sqlite lançou uma exceção : {str(e)}")
finally:
    if connection is not None:
        connection.close()