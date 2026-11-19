from datetime import date

from src.controllers.fila_controller import CRITERIOS_PADRAO, ranquear_fila

HOJE = date(2026, 11, 6)
REGRAS = {"*": {"unidade": "*", "criterios": CRITERIOS_PADRAO, "espera_limite_dias": 60, "versao": 1}}


def item(prontuario, solicitacao, data, exame="USG AXILA", codigo="USAX", unidade="UDI: ULTRASSONOGRAFIA"):
    return {
        "prontuario": prontuario, "nome": f"PACIENTE {prontuario}", "codigo_solicitacao": solicitacao,
        "data_solicitacao": f"{data}T08:00:00", "unidade": unidade, "codigo_exame": codigo,
        "nome_exame": exame, "solicitante": "",
    }


def ordem(resultado):
    return [g["prontuario"] for g in resultado["grupos"]]


def test_lista_de_prioridade_vem_antes_da_espera():
    itens = [item("1", "10", "2026-08-01"), item("2", "20", "2026-10-30")]
    prioritarios = [{"prontuario": "2", "area": "Nefrologia", "motivo": "Hemodiálise", "unidade": None}]
    r = ranquear_fila(itens, {}, prioritarios, REGRAS, [], HOJE)
    assert ordem(r) == ["2", "1"]
    assert r["grupos"][0]["motivo"]["tipo"] == "LISTA"
    assert r["grupos"][1]["motivo"]["tipo"] == "ESPERA"


def test_sem_criterio_atendido_vale_ordem_de_chegada():
    itens = [item("1", "10", "2026-10-20"), item("2", "20", "2026-10-10")]
    r = ranquear_fila(itens, {}, [], REGRAS, [], HOJE)
    assert ordem(r) == ["2", "1"]
    assert all(g["motivo"]["tipo"] == "CHEGADA" for g in r["grupos"])


def test_agendado_sai_da_fila_e_em_contato_permanece():
    itens = [item("1", "10", "2026-08-01"), item("2", "20", "2026-08-02")]
    status = {("10", "USAX"): {"status": "AGENDADO"}, ("20", "USAX"): {"status": "EM_CONTATO"}}
    r = ranquear_fila(itens, status, [], REGRAS, [], HOJE)
    assert ordem(r) == ["2"]
    assert r["grupos"][0]["itens"][0]["status"] == "EM_CONTATO"


def test_paciente_agrupa_exames_e_detecta_combinacao():
    itens = [
        item("1", "10", "2026-09-01", "BIÓPSIA ORIENTADA POR ECOGRAFIA - MAMA", "USBI4"),
        item("1", "11", "2026-09-01", "ANATOMOPATOLÓGICO - MAMA", "MBIOP"),
    ]
    combinacoes = [{"exame_a": "BIÓPSIA ORIENTADA POR ECOGRAFIA - MAMA", "exame_b": "ANATOMOPATOLÓGICO - MAMA",
                    "tipo": "ORDEM", "orientacao": "Biópsia primeiro."}]
    r = ranquear_fila(itens, {}, [], REGRAS, combinacoes, HOJE)
    assert r["resumo"]["pacientes"] == 1
    assert len(r["grupos"][0]["itens"]) == 2
    assert r["grupos"][0]["alertas"][0]["tipo"] == "ORDEM"


def test_mesma_entrada_gera_mesma_ordem():
    itens = [item(str(n), str(100 + n), f"2026-09-{1 + n % 20:02d}") for n in range(30)]
    assert ordem(ranquear_fila(itens, {}, [], REGRAS, [], HOJE)) == ordem(ranquear_fila(list(reversed(itens)), {}, [], REGRAS, [], HOJE))


def test_filtro_por_unidade_mantem_outros_exames_visiveis():
    itens = [
        item("1", "10", "2026-09-01"),
        item("1", "11", "2026-09-01", "DENSITOMETRIA ÓSSEA", "RXDOS", "UDI: DENSITOMETRIA ÓSSEA"),
    ]
    r = ranquear_fila(itens, {}, [], REGRAS, [], HOJE, unidade="UDI: DENSITOMETRIA ÓSSEA")
    grupo = r["grupos"][0]
    assert [i["na_unidade"] for i in grupo["itens"]] == [True, False]
    assert r["resumo"]["exames"] == 1


def test_api_fila_exige_autenticacao(client):
    assert client.get("/api/fila").status_code == 401


def test_api_fila_retorna_grupos(client):
    token = client.post("/api/login", data={"username": "admin", "password": "admin"}).json()["access_token"]
    resposta = client.get("/api/fila", headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["resumo"]["pacientes"] == len(corpo["grupos"])
    assert all(g["motivo"]["rotulo"] for g in corpo["grupos"])
