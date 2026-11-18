# Nome das ferramentas utilizadas

OpenAI: Codex - GPT6.1 Sol, GPT6 Luna
Anthropic: Claude Code - Opus 5.5, Sonnet 5.5

# Prompts utilizados

  - Faça uma revisão completa do código e me aponte nomes de funções "ruins", funções grandes demais ou qualquer outra coisa duplicada.
  - Revise os textos no terminal e deixei eles de modo mais claro para o usuário.
  - Me fale casos de teste, como entradas inválidas, Json corrompido, campo vaziom nível acima de 100 etc.
  - Estruture o Read Me com base nesse PDF, nele tem todas as informações do projeto, o que ele é e como ele funciona. Coloque no Read Me as informações sobre ele e como executar o projeto.


# Descrição das funcionalidades desenvolvidas:

### 1. Revisão completa do código

O código foi revisado para eliminar repetições, dividir funções grandes e deixar
cada função com uma única responsabilidade, sem alterar o comportamento do programa.

- Funções grandes divididas: a validação dos arquivos JSON (`conteudo_valido`)
  passou a usar `caixa_valida` e `leitura_valida`; o relatório e o histórico do menu
  principal foram para `gerar_relatorio` e `consultar_historico`; o filtro do
  histórico foi para `escolher_filtro_estado`.
- Trechos duplicados reunidos em funções reaproveitadas: `ler_campos_caixa` (perguntas
  do cadastro e da edição), `buscar_por_id` (busca de caixa pelo ID),
  `numero_finito`, `tem_espaco` e `codigo_em_uso` (validações usadas na digitação
  e na leitura dos arquivos) e `formatar_reais` (valores em dinheiro).
- Nomes dos arquivos JSON guardados em constantes (`ARQUIVO_CAIXAS`,
  `ARQUIVO_LEITURAS`, `ARQUIVO_CONFIGURACOES`) e limites de nível, vazão e hora
  reaproveitados de `regras.py`, em vez de números repetidos.
- Laços de soma, mínimo, máximo e filtragem substituídos por `sum`, `min`, `max` e
  listas simples, deixando o relatório e os alertas mais curtos.
- Todas as funções passaram a indicar o tipo dos parâmetros e do retorno, por
  exemplo `def classificar_estado(nivel: float, vazao: float, hora: int) -> str`.
- Recursos não vistos em aula foram trocados: o caminho da pasta de dados ficou
  `"dados"` e a gravação passou a ser feita diretamente no arquivo JSON.

### 2. Revisão dos textos do terminal

As mensagens foram escritas em português simples, sem termos técnicos, para
orientar o usuário em cada etapa.

- Menus numerados, com o nome SEP System no cabeçalho e a opção 0 para voltar ou sair.
- Entradas incorretas não encerram o programa: a pergunta é repetida explicando o
  que é aceito, por exemplo "Digite um número inteiro entre 0 e 4." ou "Use uma
  data existente no formato AAAA-MM-DD.".
- Cada leitura registrada mostra o estado e uma orientação, como "Há água saindo de
  madrugada. Verifique torneiras, descargas e canos.".
- Listas vazias têm mensagens próprias, como "Nenhuma caixa cadastrada ainda." e
  "Nenhum alerta registrado. Tudo certo por aqui.".
- Exclusões pedem confirmação, e cada resultado é seguido de "Pressione Enter para
  continuar".
- Valores em dinheiro aparecem sempre no formato brasileiro, como R$ 10,00.

### 3. Casos de teste

Foi elaborada uma lista de situações para conferir se o programa trata
corretamente entradas erradas e arquivos com problema.

- Entradas inválidas: letras onde se pede número, opções fora do menu, valores
  negativos, data inexistente (2026-02-30) e respostas diferentes de s/n.
- Campos vazios: nome, endereço ou responsável em branco são recusados.
- Limites: nível acima de 100, vazão acima de 30 e hora acima de 23 são recusados;
  nível igual a 10 e vazões iguais a 0,5 e 12 não disparam alerta.
- Prioridade dos estados: nível abaixo de 10 com vazão alta resulta em CAIXA_VAZIA.
- Código do equipamento com espaço ou repetido, inclusive com letras maiúsculas
  diferentes, é recusado.
- JSON corrompido ou com dados incompatíveis: o programa avisa e continua com os
  valores iniciais, sem travar.
- Persistência: os dados continuam disponíveis depois de fechar e abrir o programa.
- Consumo: 2 L/min às 10h e 4 L/min às 11h resultam em 180 litros e, com tarifa de
  R$ 10,00/m³, em R$ 1,80.

### 4. Estruturação do Read Me

O readme.md foi organizado com as informações do projeto e as instruções de uso:
integrantes, problema e solução, como executar, funcionalidades de cada opção do
menu, regras dos estados, cálculo de consumo e tarifa, estrutura dos arquivos,
persistência e recuperação dos dados, e a verificação realizada.


# Explicação de como o grupo verificou, testou e ajustou os resultados gerados

  - Prompt 1 - Foi analisado todas as funções que a IA dividiu, vimos se cada funções fazia seu papel original, alteramos nomes genéricos gerados e colocamos todos os parâmetros e retornos.
  - Prompt 2 - Analisamos se o texto gerado ficou com um entendimento claro para o usuário.
  - Prompt 3 - Vimos todos os casos de testes propostos e testamos um por um.
  - Prompt 4 - Analisamos se IA explicou exatamente cada trecho do PDF original criado por nós, também analisamos os passos de execução do projeto para ser se condizem com a realidade.



# Análise crítica

A IA é muito útil para fazer tarefas demoradas e repetitivas, como escrever documentação, é muito boa também para encontrar erros escondidos no código e criar casos de uso para testes. Tivemos dificuldade na refatoração de funções, pois toda vez que ela fazia isso colocava nomes muito genéricos nas funções, variáveis ou qualquer outra coisa do tipo, ela também tirava os parâmetros e retornos e não colocava de volta. Testamos modelos de duas empresas diferentes e 4 agentes diferentes entre eles e todos eles faziam os mesmos erros. Já com a documentação não tem o que reclamar já que são LLMs (Large Language Models).
