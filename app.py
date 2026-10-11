from flask import Flask, request

from models.InstituicaoEnsino import InstituicaoEnsino
from helpers.file.json import read
from helpers.database import get_conn, close_conn
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

# instancia o app flask
app = Flask(__name__)

# registra o teardown
app.teardown_appcontext(close_conn)


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200


@app.get("/instituicoesensino")
def getAllInstituicoes():
    insituicoesEnsinoReponse = []

    # abre a conexão com o banco de dados
    conn = get_conn()

    # cria um um cursor, obj responsavel por executar comandos SQL e navegar pelos resultados
    cursor = conn.cursor()

    # executa a DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino')

    # fetchall pega todos os registros retornados pelo banco e os armazena na variavel dataset
    dataset = cursor.fetchall()

    # passa por cada linha retornada pela consulta do banco de dados
    for row in dataset:
        # extrai os valores das colunas do select (no caso todas) usando os indices da tabela
        no_entidade = row[1]
        co_entidade = row[2]
        no_uf = row[3]
        sg_uf = row[4]
        co_uf = row[5]
        no_municipio = row[6]
        co_municipio = row[7]
        nu_ano_censo = row[8]
        qt_mat_bas = row[9]
        qt_mat_inf = row[10]
        qt_mat_fund = row[11]
        qt_mat_med = row[12]
        qt_mat_prof = row[13]
        qt_mat_eja = row[14]
        qt_mat_esp = row[15]

        # cria o objeto passando todos os argumentos
        instituicaoEnsino = InstituicaoEnsino(
            no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio,
            co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf,
            qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp
        )

        # retorna todas as intituiçoes do ensino em formato de dicionario
        insituicoesEnsinoReponse.append(instituicaoEnsino.toDict())

    return insituicoesEnsinoReponse, 200

@app.get("/intiuicoesensino/<int:id>")
def getByIdIntituicoes(id):
    pass

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