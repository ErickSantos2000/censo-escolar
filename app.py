from flask import Flask, request
from helpers.database import get_conn, close_conn
from schema.InstituicaoEnsinoSchema import  InstituicaoEnsinoSchema
from mapper.InstituicaoEnsinoMapper import InstituicaoEnsinoMapper
from marshmallow import ValidationError

# instancia o app flask
app = Flask(__name__)

# registra o teardown
app.teardown_appcontext(close_conn)
instituicoes_schema = InstituicaoEnsinoSchema()
instituicaoEnsinoMapper = InstituicaoEnsinoMapper()

@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200


@app.get("/instituicoesensino")
def getAllInstituicoes():
    listaIntuicoesEnsino = []

    # abre a conexão com o banco de dados
    conn = get_conn()

    # cria um um cursor, obj responsavel por executar comandos SQL e navegar pelos resultados
    cursor = conn.cursor()

    # executa a DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino')

    # fetchall pega todos os registros retornados pelo banco e os armazena na variavel dataset
    dataset = cursor.fetchall()

    # percorre cada linha da tupla retornada pelo dataset
    for row in dataset:
        instituicaoEnsino = instituicaoEnsinoMapper.to_entity(row)

        listaIntuicoesEnsino.append(instituicaoEnsino)

    # converte e monta a lista de resposta com todas as inttuições de ensino do banco
    insituicoesEnsinoReponse = instituicoes_schema.dump(listaIntuicoesEnsino, many=True)

    return insituicoesEnsinoReponse, 200

@app.get("/instituicoesensino/<int:id>")
def getByIdIntituicoes(id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM tb_instituicao_ensino WHERE id = ?', (id,))

    row = cursor.fetchone()

    if row is None:
        return "intituição não encontrada", 404

    instituicaoEnsino = instituicaoEnsinoMapper.to_entity(row)

    insituicaoEnsinoReponse = instituicoes_schema.dump(instituicaoEnsino)

    return insituicaoEnsinoReponse, 200

@app.post("/instituicoesensino")
def postInstituicoes():
    # Entrada do dado em Json.
    # Validação.
    try:
        # valida os dados
        data = instituicoes_schema.load(request.get_json())

        conn = get_conn()
        cursor = conn.cursor()

        # insere os dados
        (cursor.execute
         ('''
            INSERT INTO tb_instituicao_ensino 
            (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, 
             nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            RETURNING *
        ''', (
            data.get("no_entidade"), data.get("co_entidade"), data.get("no_uf"),
            data.get("sg_uf"), data.get("co_uf"), data.get("no_municipio"),
            data.get("co_municipio"), data.get("nu_ano_censo"), data.get("qt_mat_bas"),
            data.get("qt_mat_inf"), data.get("qt_mat_fund"), data.get("qt_mat_med"),
            data.get("qt_mat_prof"), data.get("qt_mat_eja"), data.get("qt_mat_esp")
        )))

        row = cursor.fetchone()

        instituicaoEnsino = instituicaoEnsinoMapper.to_entity(row)

        insituicaoEnsinoReponse = instituicoes_schema.dump(instituicaoEnsino)

        conn.commit()
    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

    # Retorno.
    # Dado de entrada com identificador.
    return insituicaoEnsinoReponse, 201


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    try:
        data = instituicoes_schema.load(request.get_json())

        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tb_instituicao_ensino 
            SET no_entidade = ?, co_entidade = ?, no_uf = ?, sg_uf = ?, co_uf = ?, 
                no_municipio = ?, co_municipio = ?, nu_ano_censo = ?, qt_mat_bas = ?, 
                qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?, qt_mat_prof = ?, 
                qt_mat_eja = ?, qt_mat_esp = ?
            WHERE id = ?
            RETURNING *
        ''', (
            data.get("no_entidade"), data.get("co_entidade"), data.get("no_uf"),
            data.get("sg_uf"), data.get("co_uf"), data.get("no_municipio"),
            data.get("co_municipio"), data.get("nu_ano_censo"), data.get("qt_mat_bas"),
            data.get("qt_mat_inf"), data.get("qt_mat_fund"), data.get("qt_mat_med"),
            data.get("qt_mat_prof"), data.get("qt_mat_eja"), data.get("qt_mat_esp"),
            id
        ))

        row = cursor.fetchone()

        if row is None:
            return {"erro": "Instituição não encontrada"}, 404

        instituicaoEnsino = instituicaoEnsinoMapper.to_entity(row)

        instituicoesEnsinoResponse = instituicoes_schema.dump(instituicaoEnsino)

        conn.commit()

    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

    return instituicoesEnsinoResponse, 200


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tb_instituicao_ensino SET ativo = 0 
        WHERE id = ? AND ativo = 1 RETURNING no_entidade, ativo ''', (id,))

    row = cursor.fetchone()

    if row is None:
        return {"erro": "Instituição não encontrada"}, 404

    nome = row[0]
    ativo = row[1]

    conn.commit()

    return {"sucesso": True, "no_entidade": nome, "ativo": ativo}, 200


def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()