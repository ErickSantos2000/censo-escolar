from marshmallow import Schema, fields, validate

class InstituicaoEnsinoSchema(Schema):

    id = fields.Int(dump_only=True)

    no_entidade = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    co_entidade = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    no_uf = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    sg_uf = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2)
    )

    co_uf = fields.Int(
        required=True
    )

    no_municipio = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    co_municipio = fields.Int(
        required=True
    )

    nu_ano_censo = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_bas = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_inf = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_fund = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_med = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_prof = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_eja = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_esp = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    ativo = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    created = fields.Str(
        dump_only=True
    )

