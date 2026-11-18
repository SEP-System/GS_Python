from dados import ARQUIVO_CAIXAS, ARQUIVO_CONFIGURACOES, ARQUIVO_LEITURAS, buscar_por_id, carregar_sistema, gerar_id, salvar_dados
from regras import ESTADOS, INTERVALO_HORA, INTERVALO_NIVEL, INTERVALO_VAZAO, classificar_estado
from relatorios import exibir_alertas, exibir_historico, exibir_relatorio, formatar_reais, leituras_da_caixa
from validacao import ler_codigo_equipamento, ler_data, ler_decimal, ler_inteiro, ler_sim_nao, ler_texto, pausar


def listar_caixas(caixas: list) -> None:
    if not caixas:
        print("Nenhuma caixa cadastrada ainda.")
        return
    for caixa in caixas:
        print(f"\nID: {caixa['id']} | Nome: {caixa['nome']}")
        print(f"Endereço: {caixa['endereco']}")
        print(f"Capacidade: {caixa['capacidade']:.2f} L | Responsável: {caixa['responsavel']}")
        print(f"Código do equipamento: {caixa['device_id']}")


def escolher_caixa(caixas: list) -> dict | None:
    listar_caixas(caixas)
    if not caixas:
        return None
    maior_id = max([caixa["id"] for caixa in caixas])
    while True:
        identificador = ler_inteiro("ID da caixa (0 para voltar): ", 0, maior_id)
        if identificador == 0:
            return None
        caixa = buscar_por_id(caixas, identificador)
        if caixa is not None:
            return caixa
        print("Não existe uma caixa com esse ID. Escolha um dos IDs listados.")


def ler_campos_caixa() -> dict:
    return {
        "nome": ler_texto("Nome da caixa: "),
        "endereco": ler_texto("Endereço: "),
        "capacidade": ler_decimal("Capacidade em litros: ", 0, permitir_minimo=False),
        "responsavel": ler_texto("Responsável: "),
    }


def cadastrar_caixa(caixas: list, leituras: list) -> None:
    caixa: dict = {"id": gerar_id(caixas, leituras)}
    caixa.update(ler_campos_caixa())
    caixa["device_id"] = ler_codigo_equipamento(caixas)
    if salvar_dados(ARQUIVO_CAIXAS, caixas + [caixa]):
        caixas.append(caixa)
        print(f"Caixa cadastrada com sucesso. ID: {caixa['id']}.")


def editar_caixa(caixas: list) -> None:
    caixa = escolher_caixa(caixas)
    if caixa is None:
        return
    print("Informe os novos valores dos quatro campos.")
    atualizada = caixa.copy()
    atualizada.update(ler_campos_caixa())
    novas_caixas = [atualizada if item["id"] == caixa["id"] else item for item in caixas]
    if salvar_dados(ARQUIVO_CAIXAS, novas_caixas):
        caixa.update(atualizada)
        print("Caixa atualizada com sucesso.")


def excluir_caixa(caixas: list, leituras: list) -> None:
    caixa = escolher_caixa(caixas)
    if caixa is None:
        return
    if not ler_sim_nao(f"Confirma a exclusão da caixa {caixa['nome']}?"):
        print("Exclusão cancelada.")
        return
    apagar_leituras = ler_sim_nao("Deseja apagar também as leituras dessa caixa?")
    novas_caixas = [item for item in caixas if item["id"] != caixa["id"]]
    if apagar_leituras:
        novas_leituras = [leitura for leitura in leituras if leitura["caixa_id"] != caixa["id"]]
        if not salvar_dados(ARQUIVO_LEITURAS, novas_leituras):
            return
    else:
        novas_leituras = leituras[:]
    if not salvar_dados(ARQUIVO_CAIXAS, novas_caixas):
        if apagar_leituras and not salvar_dados(ARQUIVO_LEITURAS, leituras):
            leituras[:] = novas_leituras
            print("A caixa foi mantida, mas suas leituras já foram removidas do arquivo.")
        return
    caixas[:] = novas_caixas
    leituras[:] = novas_leituras
    if apagar_leituras:
        print("Caixa e suas leituras excluídas com sucesso.")
    else:
        print("Caixa excluída. Leituras preservadas; seus alertas continuam disponíveis.")


def menu_caixas(caixas: list, leituras: list) -> None:
    while True:
        print("\nCaixas d'água\n1. Cadastrar\n2. Listar todas\n3. Editar\n4. Excluir\n0. Voltar")
        opcao = ler_inteiro("Escolha uma opção: ", 0, 4)
        match opcao:
            case 1:
                cadastrar_caixa(caixas, leituras)
            case 2:
                listar_caixas(caixas)
            case 3:
                editar_caixa(caixas)
            case 4:
                excluir_caixa(caixas, leituras)
            case 0:
                return
        pausar()


def registrar_leitura(caixas: list, leituras: list) -> None:
    caixa = escolher_caixa(caixas)
    if caixa is None:
        return
    nivel = ler_decimal("Nível da caixa (%): ", INTERVALO_NIVEL[0], INTERVALO_NIVEL[1])
    vazao = ler_decimal("Vazão de saída (L/min): ", INTERVALO_VAZAO[0], INTERVALO_VAZAO[1])
    data = ler_data("Data da leitura")
    hora = ler_inteiro("Hora da leitura (0 a 23): ", INTERVALO_HORA[0], INTERVALO_HORA[1])
    estado = classificar_estado(nivel, vazao, hora)
    leitura = {
        "id": gerar_id(leituras),
        "caixa_id": caixa["id"],
        "data_hora": f"{data}T{hora:02d}:00:00",
        "nivel": nivel,
        "vazao": vazao,
        "hora": hora,
        "estado": estado,
    }
    if salvar_dados(ARQUIVO_LEITURAS, leituras + [leitura]):
        leituras.append(leitura)
        print(f"Leitura registrada. Estado: {ESTADOS[estado]['texto']} ({estado}).")
        print(ESTADOS[estado]["orientacao"])


def consultar_historico(caixas: list, leituras: list) -> None:
    caixa = escolher_caixa(caixas)
    if caixa is not None:
        exibir_historico(caixa, leituras)


def gerar_relatorio(caixas: list, leituras: list, configuracoes: dict) -> None:
    caixa = escolher_caixa(caixas)
    if caixa is None:
        return
    if not leituras_da_caixa(leituras, caixa["id"]):
        print("Nenhuma leitura registrada para esta caixa ainda.")
        return
    print(f"Tarifa salva: {formatar_reais(configuracoes['tarifa'])} por m³.")
    if ler_sim_nao("Deseja usar outra tarifa apenas neste relatório?"):
        tarifa = ler_decimal("Tarifa para este relatório (R$ por m³): ", 0)
    else:
        tarifa = configuracoes["tarifa"]
    exibir_relatorio(caixa, leituras, tarifa)


def menu_configuracoes(configuracoes: dict) -> None:
    while True:
        print("\nConfigurações\n1. Ver tarifa de água\n2. Alterar tarifa de água\n0. Voltar")
        opcao = ler_inteiro("Escolha uma opção: ", 0, 2)
        match opcao:
            case 1:
                print(f"Tarifa de água: {formatar_reais(configuracoes['tarifa'])} por m³")
            case 2:
                tarifa = ler_decimal("Nova tarifa de água (R$ por m³): ", 0)
                if salvar_dados(ARQUIVO_CONFIGURACOES, {"tarifa": tarifa}):
                    configuracoes["tarifa"] = tarifa
                    print("Tarifa atualizada com sucesso.")
            case 0:
                return
        pausar()


def executar() -> None:
    caixas, leituras, configuracoes = carregar_sistema()
    while True:
        print("\nSEP System - Monitoramento de caixas d'água")
        print("1. Caixas d'água\n2. Registrar leitura\n3. Histórico de leituras")
        print("4. Relatório de consumo\n5. Alertas\n6. Configurações\n0. Sair")
        opcao = ler_inteiro("Escolha uma opção: ", 0, 6)
        match opcao:
            case 1:
                menu_caixas(caixas, leituras)
            case 2:
                registrar_leitura(caixas, leituras)
                pausar()
            case 3:
                consultar_historico(caixas, leituras)
                pausar()
            case 4:
                gerar_relatorio(caixas, leituras, configuracoes)
                pausar()
            case 5:
                exibir_alertas(caixas, leituras)
                pausar()
            case 6:
                menu_configuracoes(configuracoes)
            case 0:
                print("SEP System encerrado. Até a próxima.")
                return


if __name__ == "__main__":
    try:
        executar()
    except (EOFError, KeyboardInterrupt):
        print("\nSEP System encerrado. As alterações já salvas foram mantidas.")
