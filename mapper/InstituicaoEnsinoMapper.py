from models.InstituicaoEnsino import InstituicaoEnsino

class InstituicaoEnsinoMapper:
    def __init__(self):
        self
    def to_entity(self, row):
        # mapeia a row do banco pra InstituicaoEnsino
        instituicao = InstituicaoEnsino(
            # atribui cada coluna do banco aos parametros do construtor
            id=row["id"],
            no_entidade=row["no_entidade"],
            co_entidade=row["co_entidade"],
            no_uf=row["no_uf"],
            sg_uf=row["sg_uf"],
            co_uf=row["co_uf"],
            no_municipio=row["no_municipio"],
            co_municipio=row["co_municipio"],
            nu_ano_censo=row["nu_ano_censo"],
            qt_mat_bas=row["qt_mat_bas"],
            qt_mat_inf=row["qt_mat_inf"],
            qt_mat_fund=row["qt_mat_fund"],
            qt_mat_med=row["qt_mat_med"],
            qt_mat_prof=row["qt_mat_prof"],
            qt_mat_eja=row["qt_mat_eja"],
            qt_mat_esp=row["qt_mat_esp"],
            created=row["created"],
            ativo=row["ativo"]
        )

        return instituicao