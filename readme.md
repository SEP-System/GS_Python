# SEP System

Aplicação de terminal para a disciplina Computational Thinking with Python da FIAP,
Global Solution 2026.2, CitizenTech.

## Problema e solução

Vazamentos e falta de água em casas e condomínios costumam ser percebidos apenas
quando a conta chega ou a torneira seca. O SEP System organiza o monitoramento de
caixas d'água a partir de nível (%) e vazão de saída (L/min), grandezas medidas por
um ESP32 no projeto do grupo.

Esta aplicação permite informar as medições manualmente, classifica os estados e
apresenta orientações, histórico, estimativa de consumo e alertas. A comunicação
automática com o ESP32 não faz parte desta aplicação.

## Como executar

Requer Python 3.10 ou superior por utilizar `match/case`. Não exige instalação de
pacotes. Na pasta do projeto, execute:

```text
python main.py
```

Se o computador utiliza o comando `python3`, execute `python3 main.py`.
A pasta `dados/` e os três arquivos JSON são criados automaticamente ao iniciar,
na pasta em que o terminal está. Por isso, execute o programa sempre de dentro da
pasta do projeto, para que os dados salvos sejam encontrados.

## Funcionalidades

| Opção | Funcionalidade |
| --- | --- |
| 1 | Cadastrar, listar, editar e excluir caixas d'água |
| 2 | Registrar nível, vazão, data e hora; classificar e orientar |
| 3 | Consultar histórico por caixa, do mais recente ao mais antigo, com filtro opcional por estado |
| 4 | Exibir estatísticas, contagens por estado, consumo e custo estimados |
| 5 | Listar todas as leituras de alerta, com suas orientações |
| 6 | Ver e alterar a tarifa de água persistida |
| 0 | Sair |

O cadastro gera um ID e exige nome, endereço, capacidade positiva, responsável e
código de equipamento único, sem espaços. A comparação dos códigos ignora
diferenças entre maiúsculas e minúsculas. A edição mantém ID e código do equipamento.
A exclusão pede confirmação e permite apagar ou preservar as leituras.
Alertas preservados identificam caixas excluídas pelo ID. Os históricos e relatórios
por caixa são acessados pelas caixas ainda cadastradas.

As entradas numéricas aceitam vírgula ou ponto decimal, sem separador de milhar.
O nível deve ficar entre 0 e 100 e a vazão entre 0 e 30. A data usa `AAAA-MM-DD`
e Enter seleciona hoje; a hora é um inteiro de 0 a 23, com minutos e segundos zero.
Datas futuras também são aceitas para simulações. Entradas incorretas repetem a
pergunta, com explicação. O ID zero permite voltar da seleção de caixa.

## Regras dos estados

As condições abaixo são avaliadas nesta ordem; a primeira verdadeira prevalece.
Os limites estão no início de `regras.py`.

| Prioridade | Estado | Condição | Orientação |
| --- | --- | --- | --- |
| 1 | CAIXA_VAZIA | Nível menor que 10% | A caixa está quase sem água. Verifique o abastecimento. |
| 2 | POSSIVEL_VAZAMENTO | Vazão maior que 0,5 L/min nas horas 0, 1, 2, 3 ou 4 | Há água saindo de madrugada. Verifique torneiras, descargas e canos. |
| 3 | CONSUMO_ALTO | Vazão maior que 12 L/min | Muita água saindo agora. Confira se há torneiras abertas. |
| 4 | NORMAL | Demais situações | Tudo certo com a caixa d'água. |

Nível igual a 10% não caracteriza caixa vazia; vazões iguais a 0,5 e a 12 não
ultrapassam os limites correspondentes. A classificação usa a hora da leitura,
independentemente da hora em que o programa é executado.

## Consumo e tarifa

O relatório mostra quantidade de leituras, média e mínimo de nível, média e máximo
de vazão e contagem de cada estado. As médias são aritméticas das medições.
O consumo ordena as leituras por data e hora e aplica a regra do trapézio:

```text
consumo em litros = soma de ((vazão anterior + vazão atual) / 2) x minutos decorridos
custo em reais = (consumo em litros / 1000) x tarifa por m³
```

Por exemplo, 2 L/min às 10h e 4 L/min às 11h estimam 180 litros. Com tarifa de
R$ 10,00/m³, o custo estimado é R$ 1,80. Uma única leitura resulta em zero litros,
pois não existe intervalo. Leituras simultâneas são aceitas, ordenadas pelo ID em
caso de empate; o intervalo entre elas contribui com zero litros.

O cálculo supõe variação linear da vazão entre as leituras, inclusive quando são
de dias diferentes. Intervalos longos podem reduzir bastante a precisão. O valor
não representa a conta de água completa: não inclui esgoto, faixas de cobrança,
taxas ou cobranças mínimas.

A tarifa inicial é R$ 0,00/m³ e pode ser zero ou positiva. Altere-a em Configurações.
Ao gerar um relatório, é possível informar uma tarifa apenas para aquela consulta,
sem alterar a tarifa salva. Os valores são arredondados somente na exibição.
Os alertas representam registros históricos e não uma afirmação de problema atual.

## Estrutura dos arquivos

```text
gs_python/
    main.py
    dados.py
    validacao.py
    regras.py
    relatorios.py
    readme.md
    prompt.md
    dados/                    (criada na primeira execução)
        caixas.json
        leituras.json
        configuracoes.json
```

| Arquivo | Responsabilidade |
| --- | --- |
| main.py | Menu principal, submenus, cadastro, edição, exclusão e registro de leituras |
| dados.py | Criação, validação, leitura e gravação dos JSON; geração de IDs |
| validacao.py | Entradas de inteiro, decimal, texto, sim/não, data e código do equipamento; pausa |
| regras.py | Constantes, tuplas de limites, dicionário de estados, classificação e cálculo de consumo |
| relatorios.py | Histórico em tabela, filtros, estatísticas e alertas |
| readme.md | Execução, regras, estrutura e relação com os requisitos da disciplina |
| prompt.md | Registro do uso de IA e espaço para a avaliação crítica do grupo |

## Persistência e recuperação

Os dados são salvos logo após cada alteração, gravando diretamente no arquivo JSON.
A pasta `dados/` é criada com `os.mkdir` quando ainda não existe. Se a gravação falhar, o programa avisa e não anuncia sucesso. A exclusão que envolve
dois arquivos tenta restaurar as leituras se a gravação das caixas falhar.
Essa operação não é uma transação de banco de dados: uma interrupção abrupta entre
as duas gravações pode deixar somente uma delas concluída.

Arquivos inexistentes são criados com listas vazias ou tarifa padrão. JSON
corrompido, codificação inválida ou estrutura incompatível gera aviso e inicia
aquele conjunto de dados com os valores padrão, sem encerrar o programa.
O arquivo inválido só é substituído quando ocorrer uma alteração nesse conjunto;
os registros antigos desse arquivo não são recuperados automaticamente.
Erros de permissão também são informados. Verifique o acesso à pasta antes de
continuar se o programa avisar que não conseguiu salvar.

Somente `json`, `os` e `datetime` são importados da biblioteca padrão. O código usa
funções e estruturas básicas, sem classes ou bibliotecas externas.
A entrega não contém dados de teste.


## Verificação realizada pelo assistente

O programa foi executado no terminal com Python 3.15 em cópias temporárias,
separadas da entrega. Um roteiro com 197 entradas percorreu todas as opções do
menu principal, os submenus, os cinco filtros do histórico e entradas inválidas
de texto, números, data, hora, código repetido e confirmação.

Também foram conferidos o reinício com dados salvos, a exclusão com e sem remoção
de leituras, os limites e prioridades dos estados, leituras fora de ordem,
intervalos de duração zero, virada de dia e relatório com apenas uma leitura.
Uma sequência de quatro leituras resultou em 3.015 litros e R$ 30,15 com tarifa
de R$ 10,00/m³, conforme o cálculo manual.

Os três arquivos foram testados com JSON corrompido, estrutura incompatível e
codificação inválida. Os avisos apareceram e o programa continuou funcionando.
Foram simuladas falhas de leitura e de criação da pasta de gravação. A entrega
não inclui a pasta `dados/`: ela e os três arquivos JSON são criados pelo programa
na primeira execução.
