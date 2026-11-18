import json
import os
from datetime import datetime

from regras import ESTADOS, INTERVALO_HORA, INTERVALO_NIVEL, INTERVALO_VAZAO, TARIFA_PADRAO, classificar_estado
from validacao import numero_finito, tem_espaco

PASTA_DADOS = "dados"
ARQUIVO_CAIXAS = "caixas.json"
ARQUIVO_LEITURAS = "leituras.json"
ARQUIVO_CONFIGURACOES = "configuracoes.json"


def numero_valido(valor: object, minimo: float, maximo: float | None = None, permitir_minimo: bool = True) -> bool:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not numero_finito(valor):
        return False
    if valor < minimo or (valor == minimo and not permitir_minimo):
        return False
    return maximo is None or valor <= maximo


def inteiro_positivo(valor: object) -> bool:
    return type(valor) is int and valor > 0


def texto_valido(valor: object) -> bool:
    return isinstance(valor, str) and bool(valor.strip()) and valor.isprintable()


def caixa_valida(caixa: dict, equipamentos: list) -> bool:
    for campo in ("nome", "endereco", "responsavel", "device_id"):
        if not texto_valido(caixa.get(campo)):
            return False
    codigo = caixa["device_id"].lower()
    if tem_espaco(codigo) or codigo in equipamentos:
        return False
    equipamentos.append(codigo)
    return numero_valido(caixa.get("capacidade"), 0, permitir_minimo=False)


def leitura_valida(leitura: dict) -> bool:
    if not inteiro_positivo(leitura.get("caixa_id")):
        return False
    if not numero_valido(leitura.get("nivel"), INTERVALO_NIVEL[0], INTERVALO_NIVEL[1]):
        return False
    if not numero_valido(leitura.get("vazao"), INTERVALO_VAZAO[0], INTERVALO_VAZAO[1]):
        return False
    hora = leitura.get("hora")
    if type(hora) is not int or not INTERVALO_HORA[0] <= hora <= INTERVALO_HORA[1]:
        return False
    if not isinstance(leitura.get("estado"), str) or leitura["estado"] not in ESTADOS:
        return False
    if leitura["estado"] != classificar_estado(leitura["nivel"], leitura["vazao"], hora):
        return False
    try:
        momento = datetime.fromisoformat(leitura.get("data_hora", ""))
    except (ValueError, TypeError):
        return False
    if momento.tzinfo is not None or momento.isoformat(timespec="seconds") != leitura["data_hora"]:
        return False
    return momento.hour == hora


def conteudo_valido(nome_arquivo: str, conteudo: object) -> bool:
    if nome_arquivo == ARQUIVO_CONFIGURACOES:
        return isinstance(conteudo, dict) and numero_valido(conteudo.get("tarifa"), 0)
    if nome_arquivo not in (ARQUIVO_CAIXAS, ARQUIVO_LEITURAS) or not isinstance(conteudo, list):
        return False
    identificadores = []
    equipamentos = []
    for registro in conteudo:
        if not isinstance(registro, dict):
            return False
        identificador = registro.get("id")
        if not inteiro_positivo(identificador) or identificador in identificadores:
            return False
        identificadores.append(identificador)
        if nome_arquivo == ARQUIVO_CAIXAS:
            if not caixa_valida(registro, equipamentos):
                return False
        elif not leitura_valida(registro):
            return False
    return True


def criar_pasta_dados() -> None:
    try:
        os.mkdir(PASTA_DADOS)
    except FileExistsError:
        pass


def salvar_dados(nome_arquivo: str, conteudo: list | dict) -> bool:
    try:
        criar_pasta_dados()
        with open(f"{PASTA_DADOS}/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
            json.dump(conteudo, arquivo, ensure_ascii=False, indent=4, allow_nan=False)
        return True
    except (OSError, ValueError, TypeError, OverflowError):
        print(f"Não foi possível salvar {nome_arquivo}. Confira o espaço e a permissão da pasta dados.")
        return False


def carregar_dados(nome_arquivo: str, padrao: list | dict) -> list | dict:
    try:
        with open(f"{PASTA_DADOS}/{nome_arquivo}", "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
    except FileNotFoundError:
        salvar_dados(nome_arquivo, padrao)
        return padrao
    except (json.JSONDecodeError, UnicodeError):
        print(f"Aviso: {nome_arquivo} está corrompido. Iniciando com os valores padrão.")
        return padrao
    except OSError:
        print(f"Não foi possível ler {nome_arquivo}. Iniciando com os valores padrão.")
        return padrao
    if not conteudo_valido(nome_arquivo, conteudo):
        print(f"Aviso: {nome_arquivo} tem dados inválidos. Iniciando com os valores padrão.")
        return padrao
    return conteudo


def carregar_sistema() -> tuple:
    caixas = carregar_dados(ARQUIVO_CAIXAS, [])
    leituras = carregar_dados(ARQUIVO_LEITURAS, [])
    configuracoes = carregar_dados(ARQUIVO_CONFIGURACOES, {"tarifa": TARIFA_PADRAO})
    return caixas, leituras, configuracoes


def buscar_por_id(registros: list, identificador: int) -> dict | None:
    for registro in registros:
        if registro["id"] == identificador:
            return registro
    return None


def gerar_id(registros: list, leituras: list | None = None) -> int:
    maior_id = max([registro["id"] for registro in registros], default=0)
    if leituras is not None:
        maior_id = max([leitura["caixa_id"] for leitura in leituras] + [maior_id])
    return maior_id + 1
