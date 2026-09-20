from flask import Flask, request

from helpers.database.init__db import connection
from models.InstituicaoEnsino import InstituicaoEnsino
from helpers.file.json import read
from helpers.database import get_connection
import json


def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InstituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"],
        row["no_entidade"],
        row["co_entidade"],
        row["qt_mat_bas"])
        for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


app = Flask(__name__)


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200


# Rota GET mantida intacta conforme solicitado
@app.get("/instituicoesensino")
def getInstituicoes():
    insituicoesEnsinoReponse = []

    # abre a conexão com o banco de dados
    connection = get_connection()

    # cria um um cursor, obj responsavel por executar comandos SQL e navegar pelos resultados
    cursor = connection.cursor()

    # Executar as DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino')

    # fetchall pega todos os registros retornados pelo banco e os armazena na variavel dataset
    dataset = cursor.fetchall()

    # passa por cada linha e imprime o tipo de dado de cada registro no terminal
    for row in dataset:
        print(type(row))
        insituicoesEnsinoReponse.append(row)

    # é preciso fechar a conexão e o cursor
    cursor.close()
    connection.close()

    return insituicoesEnsinoReponse, 200


@app.post("/instituicoesensino")
def postInstituicoes():
    dados = request.get_json()
    if not dados:
        return {"erro": "Dados inválidos"}, 400

    novo_instituicao = InstituicaoEnsino(
        id=dados.get("id"),
        no_entidade=dados.get("no_entidade"),
        co_entidade=dados.get("co_entidade"),
        qt_mat_bas=dados.get("qt_mat_bas")
    )

    dataset = read("instituicoes.json")
    dataset.append(novo_instituicao.toDict())

    with open("instituicoes.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return novo_instituicao.no_entidade, 201


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    dados = request.get_json()
    if not dados:
        return {"erro": "Dados inválidos"}, 400

    dataset = read("instituicoes.json")
    encontrado = False

    for row in dataset:
        if str(row["id"]) == str(id):
            row["id"] = dados.get("id", row["id"])
            row["no_entidade"] = dados.get("no_entidade", row["no_entidade"])
            row["co_entidade"] = dados.get("co_entidade", row["co_entidade"])
            row["qt_mat_bas"] = dados.get("qt_mat_bas", row["qt_mat_bas"])
            encontrado = True
            break

    if not encontrado:
        return {"erro": "Instituição não encontrada"}, 404

    with open("instituicoes.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return  200


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    dataset = read("instituicoes.json")
    novo_dataset = [row for row in dataset if str(row["id"]) != str(id)]

    if len(novo_dataset) == len(dataset):
        return {"erro": "Instituição não encontrada"}, 404

    with open("instituicoes.json", "w", encoding="utf-8") as f:
        json.dump(novo_dataset, f, indent=4, ensure_ascii=False)

    return  200


def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()