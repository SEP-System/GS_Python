from datetime import datetime

from dados import buscar_por_id
from regras import ESTADOS, calcular_consumo, chave_leitura
from validacao import ler_inteiro


def formatar_reais(valor: float) -> str:
    return f"R$ {valor:.2f}".replace(".", ",")


def leituras_da_caixa(leituras: list, caixa_id: int) -> list:
    return [leitura for leitura in leituras if leitura["caixa_id"] == caixa_id]


def exibir_tabela(leituras: list) -> None:
    print(f"{'ID':>5} | {'Data e hora':16} | {'Nível (%)':>10} | {'Vazão (L/min)':>14} | Estado")
    print("-" * 92)
    for leitura in sorted(leituras, key=chave_leitura, reverse=True):
        momento = datetime.fromisoformat(leitura["data_hora"]).strftime("%d/%m/%Y %H:%M")
        texto_estado = ESTADOS[leitura["estado"]]["texto"]
        print(f"{leitura['id']:>5} | {momento:16} | {leitura['nivel']:>10.2f} | {leitura['vazao']:>14.2f} | {texto_estado}")


def escolher_filtro_estado() -> str | None:
    print("\nFiltro de estado")
    print("0. Todos os estados\n1. Normal\n2. Consumo alto\n3. Possível vazamento\n4. Caixa vazia")
    opcao = ler_inteiro("Escolha o filtro: ", 0, 4)
    match opcao:
        case 1:
            return "NORMAL"
        case 2:
            return "CONSUMO_ALTO"
        case 3:
            return "POSSIVEL_VAZAMENTO"
        case 4:
            return "CAIXA_VAZIA"
        case _:
            return None


def exibir_historico(caixa: dict, leituras: list) -> None:
    selecionadas = leituras_da_caixa(leituras, caixa["id"])
    if not selecionadas:
        print("Nenhuma leitura registrada para esta caixa ainda.")
        return
    estado = escolher_filtro_estado()
    filtradas = [leitura for leitura in selecionadas if estado is None or leitura["estado"] == estado]
    print(f"\nHistórico de {caixa['nome']}")
    if filtradas:
        exibir_tabela(filtradas)
    else:
        print("Nenhuma leitura encontrada com esse estado.")


def exibir_relatorio(caixa: dict, leituras: list, tarifa: float) -> None:
    selecionadas = leituras_da_caixa(leituras, caixa["id"])
    if not selecionadas:
        print("Nenhuma leitura registrada para esta caixa ainda.")
        return
    quantidade = len(selecionadas)
    niveis = [leitura["nivel"] for leitura in selecionadas]
    vazoes = [leitura["vazao"] for leitura in selecionadas]
    contagens = dict.fromkeys(ESTADOS, 0)
    for leitura in selecionadas:
        contagens[leitura["estado"]] += 1
    consumo = calcular_consumo(selecionadas)
    custo = (consumo / 1000) * tarifa
    print(f"\nRelatório de consumo: {caixa['nome']}")
    print(f"Quantidade de leituras: {quantidade}")
    print(f"Nível médio: {sum(niveis) / quantidade:.2f}%")
    print(f"Menor nível: {min(niveis):.2f}%")
    print(f"Vazão média: {sum(vazoes) / quantidade:.2f} L/min")
    print(f"Vazão máxima: {max(vazoes):.2f} L/min")
    for estado, dados_estado in ESTADOS.items():
        print(f"{dados_estado['texto']} ({estado}): {contagens[estado]}")
    print(f"Consumo estimado entre as leituras: {consumo:.2f} L")
    print(f"Tarifa utilizada: {formatar_reais(tarifa)} por m³")
    print(f"Custo estimado: {formatar_reais(custo)}")
    if quantidade < 2:
        print("São necessárias duas leituras para estimar o consumo; por enquanto, o total é zero.")
    print("A estimativa considera a variação da vazão entre medições; intervalos longos reduzem a precisão.")
    print("Leituras no mesmo instante não acrescentam tempo ao cálculo.")


def exibir_alertas(caixas: list, leituras: list) -> None:
    alertas = [leitura for leitura in leituras if leitura["estado"] != "NORMAL"]
    if not alertas:
        print("Nenhum alerta registrado. Tudo certo por aqui.")
        return
    for leitura in sorted(alertas, key=chave_leitura, reverse=True):
        caixa = buscar_por_id(caixas, leitura["caixa_id"])
        if caixa is None:
            nome_caixa = f"Caixa excluída ou indisponível (ID {leitura['caixa_id']})"
        else:
            nome_caixa = caixa["nome"]
        print(f"\nCaixa: {nome_caixa}")
        exibir_tabela([leitura])
        print(ESTADOS[leitura["estado"]]["orientacao"])
    print(f"\nTotal de alertas registrados: {len(alertas)}")
