from datetime import datetime


def numero_finito(valor: float) -> bool:
    return valor == valor and valor not in (float("inf"), -float("inf"))


def tem_espaco(texto: str) -> bool:
    for caractere in texto:
        if caractere.isspace():
            return True
    return False


def codigo_em_uso(caixas: list, codigo: str) -> bool:
    for caixa in caixas:
        if caixa["device_id"].lower() == codigo.lower():
            return True
    return False


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um número inteiro entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_decimal(mensagem: str, minimo: float, maximo: float | None = None, permitir_minimo: bool = True) -> float:
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("Entrada inválida. Digite um número; pode usar vírgula ou ponto.")
            continue
        if not numero_finito(valor):
            print("Digite um número decimal finito.")
        elif valor < minimo or (valor == minimo and not permitir_minimo):
            if permitir_minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
            else:
                print(f"Digite um valor maior que {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"Digite um valor menor ou igual a {maximo}.")
        else:
            return valor


def ler_texto(mensagem: str) -> str:
    while True:
        texto = input(mensagem).strip()
        if texto and texto.isprintable():
            return texto
        print("Digite um texto não vazio, sem caracteres de controle.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem + " (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        elif resposta in ("n", "nao", "não"):
            return False
        else:
            print("Resposta inválida. Digite s para sim ou n para não.")


def ler_data(mensagem: str) -> str:
    while True:
        texto = input(mensagem + " (AAAA-MM-DD; Enter para hoje): ").strip()
        if texto == "":
            return datetime.now().date().isoformat()
        try:
            data = datetime.strptime(texto, "%Y-%m-%d")
        except ValueError:
            print("Data inválida. Use uma data existente no formato AAAA-MM-DD.")
            continue
        if texto == data.date().isoformat():
            return texto
        print("Use o formato AAAA-MM-DD, por exemplo 2026-11-17.")


def ler_codigo_equipamento(caixas: list) -> str:
    while True:
        codigo = ler_texto("Código do equipamento (ex.: caixa_g01): ")
        if tem_espaco(codigo):
            print("O código do equipamento não pode conter espaços.")
        elif codigo_em_uso(caixas, codigo):
            print("Esse código de equipamento já pertence a outra caixa.")
        else:
            return codigo


def pausar() -> None:
    input("\nPressione Enter para continuar")
