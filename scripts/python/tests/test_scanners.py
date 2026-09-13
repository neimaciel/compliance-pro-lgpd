"""Testes dos scanners Python do compliance-pro-lgpd.

Cobrem o que o CI nunca exercitou até a v1.0.1:
  - CPF e CNPJ com dígito verificador;
  - exclusões relativas ao alvo (um projeto dentro de uma pasta tmp/ era pulado inteiro
    e o scan "passava" com 0 arquivos);
  - detecção de fixture pelo caminho dentro do alvo, não pelo caminho absoluto;
  - cadeia de hash do evidence log, varredura de logs (inclusive .gz) e de schema SQL.

Nenhum CPF/CNPJ válido fica literal no repositório: eles são gerados aqui, porque o
próprio pii-scan roda sobre este repo no CI.
"""
from __future__ import annotations

import gzip
import json

from click.testing import CliRunner

from compliance_pro import audit_log_integrity as ali
from compliance_pro.log_scanner import scan_log
from compliance_pro.patterns import validate_cnpj, validate_cpf
from compliance_pro.pii_scanner import DEFAULT_EXCLUDES, iter_files
from compliance_pro.pii_scanner import cli as pii_cli
from compliance_pro.retention_scanner import covered_by_ropa, parse_schema_sql


def _cpf_valido(base: str = "5299" + "82247") -> str:   # partido: 8+ dígitos seguidos parecem RG
    d = [int(c) for c in base]
    for n in (9, 10):
        s = sum(d[j] * (n + 1 - j) for j in range(n))
        d.append((s * 10) % 11 % 10)
    t = "".join(map(str, d))
    return f"{t[:3]}.{t[3:6]}.{t[6:9]}-{t[9:]}"


def _cnpj_valido(base: str = "1122" + "2333" + "0001") -> str:   # partido: sequências longas parecem RG/título
    d = [int(c) for c in base]
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for w in (w1, [6] + w1):
        r = sum(x * y for x, y in zip(d, w)) % 11
        d.append(0 if r < 2 else 11 - r)
    t = "".join(map(str, d))
    return f"{t[:2]}.{t[2:5]}.{t[5:8]}/{t[8:12]}-{t[12:]}"


def _troca_ultimo_digito(doc: str) -> str:
    return doc[:-1] + str((int(doc[-1]) + 1) % 10)


# --- validadores ---------------------------------------------------------------
def test_cpf_com_digito_certo_e_errado():
    cpf = _cpf_valido()
    assert validate_cpf(cpf)
    assert not validate_cpf(_troca_ultimo_digito(cpf))
    assert not validate_cpf("111.111.111-11")        # dígitos repetidos


def test_cnpj_com_digito_certo_e_errado():
    cnpj = _cnpj_valido()
    assert validate_cnpj(cnpj)
    assert not validate_cnpj(_troca_ultimo_digito(cnpj))


# --- pii-scan -------------------------------------------------------------------
def _projeto(tmp_path):
    # o alvo mora DENTRO de uma pasta chamada tmp: era o caso que zerava o scan
    root = tmp_path / "tmp" / "projeto"
    (root / "src").mkdir(parents=True)
    (root / "src" / "cadastro.py").write_text(f'CPF_CLIENTE = "{_cpf_valido()}"\n', encoding="utf-8")
    (root / "node_modules" / "lib").mkdir(parents=True)
    (root / "node_modules" / "lib" / "x.js").write_text(f'var c = "{_cpf_valido()}";\n', encoding="utf-8")
    (root / "logo.png").write_bytes(b"\x89PNG")
    return root


def test_alvo_dentro_de_pasta_excluida_ainda_e_examinado(tmp_path):
    root = _projeto(tmp_path)
    arquivos = {p.relative_to(root).as_posix() for p in iter_files(root, DEFAULT_EXCLUDES)}
    assert arquivos == {"src/cadastro.py"}          # node_modules e .png ficam de fora


def test_cli_acha_cpf_mascara_no_relatorio_e_falha_no_limite(tmp_path):
    root = _projeto(tmp_path)
    rel = tmp_path / "r.json"
    res = CliRunner().invoke(pii_cli, ["--target", str(root), "--report", str(rel),
                                       "--fail-on", "high", "--quiet"])
    assert res.exit_code == 2
    texto = rel.read_text(encoding="utf-8")
    data = json.loads(texto)
    assert data["files_scanned"] == 1
    cpf = [f for f in data["findings"] if f["pattern"] == "cpf"]
    assert cpf and cpf[0]["validated"] is True
    assert _cpf_valido() not in texto                  # só o valor mascarado vai ao relatório


def test_cpf_invalido_em_fixture_nao_vira_achado(tmp_path):
    root = tmp_path / "proj"
    (root / "tests").mkdir(parents=True)
    (root / "tests" / "fixture_clientes.py").write_text(
        f'X = "{_troca_ultimo_digito(_cpf_valido())}"\n', encoding="utf-8")
    rel = tmp_path / "r.json"
    CliRunner().invoke(pii_cli, ["--target", str(root), "--report", str(rel), "--quiet"])
    data = json.loads(rel.read_text(encoding="utf-8"))
    assert not [f for f in data["findings"] if f["pattern"] == "cpf"]


def test_arquivo_comum_nao_vira_fixture_por_causa_do_caminho_absoluto(tmp_path):
    # o tmp_path do pytest tem "test_..." no nome: a detecção olhava o caminho absoluto
    root = tmp_path / "proj"
    (root / "src").mkdir(parents=True)
    (root / "src" / "cadastro.py").write_text(
        f'X = "{_troca_ultimo_digito(_cpf_valido())}"\n', encoding="utf-8")
    rel = tmp_path / "r.json"
    CliRunner().invoke(pii_cli, ["--target", str(root), "--report", str(rel), "--quiet"])
    cpf = [f for f in json.loads(rel.read_text(encoding="utf-8"))["findings"] if f["pattern"] == "cpf"]
    assert cpf and cpf[0]["validated"] is False


def test_nenhum_arquivo_examinado_nao_passa_calado(tmp_path):
    vazio = tmp_path / "vazio"
    vazio.mkdir()
    res = CliRunner().invoke(pii_cli, ["--target", str(vazio), "--fail-on", "critical", "--quiet"])
    assert res.exit_code == 3


# --- evidence log ---------------------------------------------------------------
def test_cadeia_de_evidencia_integra_e_adulterada(tmp_path):
    log = tmp_path / "log.jsonl"
    r = CliRunner()
    for ev in ('{"event":"ropa","ts":"2026-09-13T00:00:00Z"}',
               '{"event":"dpia","ts":"2026-09-13T01:00:00Z"}'):
        assert r.invoke(ali.cli, ["append", "--file", str(log), "--event", ev]).exit_code == 0
    assert r.invoke(ali.cli, ["verify", "--file", str(log)]).exit_code == 0

    linhas = log.read_text(encoding="utf-8").splitlines()
    rec = json.loads(linhas[0])
    rec["event"] = "adulterado"
    linhas[0] = json.dumps(rec)
    log.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    assert r.invoke(ali.cli, ["verify", "--file", str(log)]).exit_code == 2


# --- log-scan -------------------------------------------------------------------
def test_log_com_cpf_valido_inclusive_gz(tmp_path):
    linha = f"2026-09-13 login ok cpf={_cpf_valido()}\n"
    plano = tmp_path / "app.log"
    plano.write_text("linha sem dado\n" + linha, encoding="utf-8")
    comp = tmp_path / "app.log.gz"
    with gzip.open(comp, "wt", encoding="utf-8") as f:
        f.write(linha)
    a, b = list(scan_log(plano)), list(scan_log(comp))
    assert [(x.line, x.pattern) for x in a] == [(2, "cpf")]
    assert [(x.line, x.pattern) for x in b] == [(1, "cpf")]


# --- retention-scan -------------------------------------------------------------
def test_schema_marca_coluna_pessoal_e_cobertura_da_ropa():
    sql = ("CREATE TABLE clientes (\n  id INTEGER PRIMARY KEY,\n  nome VARCHAR(120) NOT NULL,\n"
           "  cpf CHAR(11)\n);")
    cols = {c.column: c for c in parse_schema_sql(sql)}
    assert cols["cpf"].is_pii
    assert cols["nome"].nullable is False and cols["cpf"].nullable is True
    ropa = {"atividades": [{"tabela": "clientes"}]}
    assert covered_by_ropa("clientes", "cpf", ropa)
    assert not covered_by_ropa("pedidos", "valor", ropa)
