# Especificação de Requisitos

## 1. Requisitos Funcionais (RF)
| ID | Título | Descrição | Prioridade |
| :--- | :--- | :--- | :---: |
| RF001 | Filtragem de requisições | Filtrar quais requisições são válidas, e quais tem algum erro que impede a alocação da vaga | Importante |
| RF002 | Atribuição de prioridade | Capacidade do sistema de dar uma prioridade para uma requisição | Importante |
| RF003 | Planilha inteligente | Interface principal que mostra as informações obtidas após a filtragem e atribuição, além de funcionalidades de usabilidade para as usuárias | Essencial |

### Legenda de Níveis de Prioridade:
- **Essencial (Alta):** Funcionalidade indispensável para o funcionamento básico da aplicação. Sem ela, o sistema não pode ir para produção (ex: autenticação, cadastros base).
- **Importante (Média):** Funcionalidade que agrega valor significativo ao negócio e melhora o fluxo de trabalho, mas cuja ausência temporária não impede a operação mínima (ex: relatórios, filtros avançados).
- **Desejável (Baixa):** Funcionalidade complementar, melhoria estética ou recurso secundário que pode ser implementado em sprints futuras (ex: temas visuais, atalhos de teclado).

## 2. Requisitos Não Funcionais (RNF)
| ID | Categoria | Descrição |
| :--- | :--- | :--- |
| RNF001 | Chamada do banco de dados | Chamar banco de dados do AGHU para saber quais as requisições válidas e quais as vagas disponíveis por área |
| RNF002 | Obtenção das requisições | Obter as requisições submetidas pelo microsoft forms |
| RNF003 | Listagem de prioridades | Lista de prioridades para cada tipo de exame |

## 3. Detalhamento SDD (CARE)

### [CARE-RNF001]
* **Context (Contexto)**: Fork do SETSID feito
* **Action (Ação)**: Pedir os SELECTS apropriados caso não existam, e descobrir como é feita a chamada, e criação de funções que colocam os resultados em arquivos .csv
* **Result (Resultado)**: API reutilizável para leitura do banco
* **Evaluation (Avaliação)**: 

### [CARE-RNF002]
* **Context (Contexto)**: Conexão com o microsoft forms estabelecida
* **Action (Ação)**: Criar função que crie um arquivo .csv para leitura das requisições
* **Result (Resultado)**: API para acesso das requisições do microsoft forms
* **Evaluation (Avaliação)**: 

### [CARE-RNF003]
* **Context (Contexto)**: Contato com cada uma das funcionárias que fazem a marcação
* **Action (Ação)**: Criar critérios unificados sobre prioridades para: cada tipo de exame, cada tipo de paciente, cada possível local e clínicas solicitantes. Além de como essas clínicas
* **Result (Resultado)**: Uma arquivo de rápido acesso para aplicação das prioridades
* **Evaluation (Avaliação)**: 

### [CARE-RF001]
* **Context (Contexto)**: RNF001 e RNF002 concluidas
* **Action (Ação)**: Criar função que cria dois novos .csv, um com as requisições válidas, e outro com as requisições inválidas
* **Result (Resultado)**: Uma abstração por meio de um arquivo que divide todo o processo de chamada e filtragem da área de aplicação de prioridades
* **Evaluation (Avaliação)**: Os exames de cada .csv pertencem ao local onde deveriam estar, e nenhum exames falhou o processo de classificação (não está em nenhum dos .csv)

### [CARE-RF002]
* **Context (Contexto)**: RF001 e RNF003 concluidas
* **Action (Ação)**: novo .csv que possua as requisições válidas, em ordem de prioridade
* **Result (Resultado)**: Arquivo em formato parecido com a planilha, para interação indireta com o usuário por meio da interface
* **Evaluation (Avaliação)**: 

### [CARE-RF003]
* **Context (Contexto)**: RF002 concluida
* **Action (Ação)**: Criação de uma planilha interativa, que auxilie na tomada de decisão, e que seja facilmente alterável por meio de filtragem (por local por exemplo), e por meio da adição e remoção de prioridades
* **Result (Resultado)**: O produto final. Uma planilha parecida com a utilizada pelas funcionárias, porém com funcionalidades de auxílio à tomada de decisão
* **Evaluation (Avaliação)**: 

