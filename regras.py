from datetime import datetime

LIMITE_CAIXA_VAZIA = 10.0
LIMITE_CONSUMO_ALTO = 12.0
LIMITE_VAZAMENTO = 0.5
HORAS_MADRUGADA = (0, 1, 2, 3, 4)
INTERVALO_NIVEL = (0.0, 100.0)
INTERVALO_VAZAO = (0.0, 30.0)
INTERVALO_HORA = (0, 23)
TARIFA_PADRAO = 0.0

ESTADOS = {
    "NORMAL": {
        "texto": "Normal",
        "orientacao": "Tudo certo com a caixa d'água.",
    },
    "CONSUMO_ALTO": {
        "texto": "Consumo alto",
        "orientacao": "Muita água saindo agora. Confira se há torneiras abertas.",
    },
    "POSSIVEL_VAZAMENTO": {
        "texto": "Possível vazamento",
        "orientacao": "Há água saindo de madrugada. Verifique torneiras, descargas e canos.",
    },
    "CAIXA_VAZIA": {
        "texto": "Caixa vazia",
        "orientacao": "A caixa está quase sem água. Verifique o abastecimento.",
    },
}


def classificar_estado(nivel: float, vazao: float, hora: int) -> str:
    if nivel < LIMITE_CAIXA_VAZIA:
        return "CAIXA_VAZIA"
    elif hora in HORAS_MADRUGADA and vazao > LIMITE_VAZAMENTO:
        return "POSSIVEL_VAZAMENTO"
    elif vazao > LIMITE_CONSUMO_ALTO:
        return "CONSUMO_ALTO"
    else:
        return "NORMAL"


def chave_leitura(leitura: dict) -> tuple:
    return (leitura["data_hora"], leitura["id"])


def calcular_consumo(leituras: list) -> float:
    consumo = 0.0
    ordenadas = sorted(leituras, key=chave_leitura)
    for anterior, atual in zip(ordenadas, ordenadas[1:]):
        inicio = datetime.fromisoformat(anterior["data_hora"])
        fim = datetime.fromisoformat(atual["data_hora"])
        minutos = (fim - inicio).total_seconds() / 60
        consumo += ((anterior["vazao"] + atual["vazao"]) / 2) * minutos
    return consumo
