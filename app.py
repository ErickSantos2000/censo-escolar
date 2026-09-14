from flask import Flask, request
from models.instituicaoensino import InstituicaoEnsino
from helpers.file.json import read


def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


app = Flask(__name__)


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200

# /instituicoesensino?co_inep=123456


@app.get("/instituicoesensino")
def getAllInstituicoes():
    insituicoesEnsino = listar()
    print("Entrou na requisição")
    coEntidade = request.args.get("co_entidade")
    print(f'Valor do co_entidade do request: {coEntidade}')
    print(f'Itens da lista de instituições:{len(insituicoesEnsino)}')
    if coEntidade is not None:
        insituicoesEnsinoReponse = [
            insituicaoEnsino.toDict() for insituicaoEnsino in insituicoesEnsino if insituicaoEnsino.co_entidade == coEntidade]
    else:
        insituicoesEnsinoReponse = [
            insituicaoEnsino.toDict() for insituicaoEnsino in insituicoesEnsino]

    return insituicoesEnsinoReponse, 200


@app.get("/instituicoesensino/<int:id>")
def getByIdInstituicoes(id):
    return {"id": "1", "co_inep": "123456"}, 200


@app.post("/instituicoesensino")
def postInstituicoes():
    data = request.get_json()
    coInep = data.get("co_inep")
    return {"id": 1, "co_inep": coInep}, 201


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes():
    pass


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes():
    pass


def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()