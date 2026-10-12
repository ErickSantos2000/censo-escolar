

class InstituicaoEnsino():
    def __init__(
        self,
        no_entidade,
        co_entidade,
        no_uf,
        sg_uf,
        co_uf,
        no_municipio,
        co_municipio,
        nu_ano_censo,
        qt_mat_bas,
        qt_mat_inf,
        qt_mat_fund,
        qt_mat_med,
        qt_mat_prof,
        qt_mat_eja,
        qt_mat_esp,
        id=None,
        created = None,
        ativo = 1
    ):
        self.id = id
        self.no_entidade = no_entidade
        self.co_entidade = co_entidade
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.co_uf = co_uf
        self.no_municipio = no_municipio
        self.co_municipio = co_municipio
        self.nu_ano_censo = nu_ano_censo
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_med = qt_mat_med
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp
        self.created = created
        self.ativo = ativo

    def toDict(self):
        return {"no_entidade": self.no_entidade, "co_entidade": self.co_entidade, "qt_mat_bas": self.qt_mat_bas}



