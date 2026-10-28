# Especificação de Requisitos — AgendaHC

> **Escopo:** sistema **interno** da Central de Marcação de Exames do HC-UFPE. O AgendaHC lê as solicitações de exame do AGHU (somente leitura) e monta uma **fila priorizada por exame** para o marcador.

## 1\. Requisitos Funcionais (RF)

| ID | Título | Descrição | Prioridade | Origem |
| :---- | :---- | :---- | :---: | :---- |
| RF001 | Login institucional | A equipe acessa com o usuário e a senha institucionais (AD/LDAP Ebserh). Conta desativada no AD perde o acesso. | Essencial | RN-08 |
| RF003 | Leitura das solicitações do AGHU | Carregar as solicitações de exame pendentes (código da solicitação, prontuário, exame, especialidade, unidade, data, status do item) dos exames atendidos pela Central. | Essencial | RN-02 |
| RF004 | Fila por exame | Listar as solicitações pendentes de cada exame na ordem de prioridade, com filtros por exame, unidade, especialidade e período. | Essencial | RN-03 |
| RF005 | Cálculo da prioridade | Ordenar a fila aplicando as regras do exame. Sem regra cadastrada, vale a ordem de chegada (data da solicitação). | Essencial | RN-03, RN-04 |
| RF006 | Motivo da posição | Cada item da fila mostra por que está naquela posição (ex.: "Hemodiálise", "Retorno em 20 dias", "Ordem de chegada"). | Essencial | RN-03 |
| RF010 | Registro do tratamento | O marcador registra o resultado de cada pedido: agendado (data e unidade executora), sem contato, cancelado ou pendente, com observação. Substitui a "linha verde" da planilha. | Essencial | RN-07 |
| RF013 | Disponibilidade de vagas | O gestor indica, por exame, se há vagas abertas. A fila mostra essa situação. O comportamento sem vaga depende da decisão D3. | Importante | RN-05 |
| RF014 | Retorno e município na prioridade | Usar a data de retorno ao médico e o município do paciente como critérios, quando esses dados estiverem disponíveis (D2, D5). | Importante | RN-04 |
| RF015 | Solicitações duplicadas | Sinalizar quando o mesmo prontuário tem mais de uma solicitação pendente para o mesmo exame. | Importante | — |
| RF016 | Importação do formulário atual | Importar a planilha de respostas, casar cada resposta com o AGHU pelo nº da solicitação e prontuário, sinalizar divergências e aproveitar retorno, município e telefone. | Importante | RN-01 |
| RF017 | Painel de gestão | Por exame: pedidos na fila, espera média (solicitação → agendamento), agendados após a data de retorno e se os prioritários são atendidos antes. Apenas consulta. | Desejável | Seção 8 do 00 |
| RF020 | Orientações de preparo | Texto de preparo por exame (jejum, medicação) para o marcador repassar ao paciente. | Desejável | Fluxo da Central |

### Legenda de Níveis de Prioridade:

- **Essencial (Alta):** Funcionalidade indispensável para o funcionamento básico da aplicação. Sem ela, o sistema não pode ir para produção (ex: autenticação, cadastros base).  
- **Importante (Média):** Funcionalidade que agrega valor significativo ao negócio e melhora o fluxo de trabalho, mas cuja ausência temporária não impede a operação mínima (ex: relatórios, filtros avançados).  
- **Desejável (Baixa):** Funcionalidade complementar, melhoria estética ou recurso secundário que pode ser implementado em sprints futuras (ex: temas visuais, atalhos de teclado).

## 2\. Requisitos Não Funcionais (RNF)

| ID | Categoria | Descrição |
| :---- | :---- | :---- |
| RNF001 | Integração AGHU | Acesso **somente leitura**: usuário de banco sem permissão de escrita e consultas em SQL puro. Nenhuma gravação no AGHU. |
| RNF002 | Desacoplamento de dados | Padrão Provider: trocar a fonte entre CSV anonimizado (desenvolvimento) e PostgreSQL/AGHU (produção) por configuração, sem alterar as regras de negócio. |
| RNF003 | Autenticação | Tokens JWT, refresh token em cookie HttpOnly e renovação transparente da sessão (interceptor Axios). |
| RNF005 | Segurança HTTP | Security headers do framework (`Cache-Control: no-store`, `X-Frame-Options: DENY`). |
| RNF006 | LGPD | Apenas os dados necessários para identificar o pedido. Dados do paciente visíveis só para perfis autorizados. |
| RNF007 | Auditoria | Trilha append-only em `audit_logs` (categorias SEGURANÇA, NEGÓCIO\_CLÍNICO, CONFIGURAÇÃO) com usuário, ação, dados antes/depois, IP e data/hora UTC. |
| RNF008 | Sem exclusão física | Registros do banco local usam exclusão lógica (soft delete). |
| RNF010 | Explicabilidade | Mesmas solicitações \+ mesma versão das regras \= mesma ordem na fila. A versão da regra aplicada fica registrada. |
| RNF011 | Atualidade dos dados | A tela mostra a data/hora da última leitura do AGHU. A periodicidade é configurável (D6). |
| RNF012 | Desempenho | Fila de até 1.000 solicitações carregada em até 2 s na rede do HC (meta a validar). |
| RNF013 | Monitoramento | Rota `/api/health` para o Zabbix do HC. |
| RNF015 | Qualidade | Testes automatizados (`uv run pytest`) para regras de prioridade e rotas. `audit_framework.py` com 100% de conformidade. |
| RNF016 | Plataforma | Framework SETISD: Vue 3 \+ FastAPI (Python 3.12+). ORM apenas no banco local; implantação em VM do HC via systemd ou Podman/Docker. |

## 3\. Fora do Escopo

- Qualquer tela, formulário ou canal para o paciente.  
- Gravação no AGHU: solicitação, marcação, cancelamento e ticket continuam exclusivamente no AGHU.  
- Pacientes da regulação do SUS ou da Secretaria Estadual de Saúde (RN-09).  
- Envio automático de mensagens (WhatsApp) ao paciente.  
- Gestão de grades e agendas dos médicos (permanece no AGHU).

## 4\. Decisões Pendentes que Afetam Requisitos

| \# | Decisão | Requisitos afetados |
| :---: | :---- | :---- |
| D1 | Quais são as regras de prioridade de cada exame? | RF005, RF007, RF008 |
| D2 | Qual a antecedência mínima por município? | RF014 |
| D3 | Exame sem vaga bloqueia o pedido ou gera lista de espera? | RF013 |
| D5 | O extrato do AGHU pode incluir data de retorno, município e telefone? | RF014, RF016 |
| D6 | Com que frequência os dados do AGHU devem ser atualizados? | RF003, RNF011 |

## 5\. Detalhamento SDD (CARE)

### \[CARE-RF001\] Login institucional

* **Context (Contexto)**: Provedor AD/LDAP configurado no `.env` (provedor mock em desenvolvimento).  
* **Action (Ação)**: Usar o fluxo de autenticação do framework (AD \+ RBAC local) na rota `/api/login`.  
* **Result (Resultado)**: Credencial válida e usuário ativo no RBAC geram sessão (JWT \+ refresh em cookie HttpOnly). Falha retorna 401; usuário sem perfil retorna 403\.  
* **Evaluation (Avaliação)**: `uv run pytest tests/test_auth.py` cobre sucesso, senha inválida, usuário inativo e usuário sem perfil.

### \[CARE-RF002\] Perfis de acesso

* **Context (Contexto)**: Perfis `ADMINISTRADOR`, `GESTOR_CENTRAL`, `MARCADOR` e `AREA_SOLICITANTE` cadastrados em `data/app.db`.  
* **Action (Ação)**: Proteger cada rota com a dependência de perfil correspondente.  
* **Result (Resultado)**: Marcador trata pedidos; gestor edita regras, vagas e vê o painel; área solicitante mantém apenas a própria lista de prioritários.  
* **Evaluation (Avaliação)**: Teste de matriz perfil × rota: toda combinação não permitida retorna 403\.

### \[CARE-RF003\] Leitura das solicitações do AGHU

* **Context (Contexto)**: Consulta `Script-Solicitacao.sql` fornecida pela TI e CSV anonimizado `vw_solicitacao` com as mesmas colunas.  
* **Action (Ação)**: Criar `SolicitacaoProvider` com implementações CSV e PostgreSQL, selecionadas por configuração.  
* **Result (Resultado)**: As duas implementações retornam a mesma lista de solicitações pendentes; nada é gravado no AGHU.  
* **Evaluation (Avaliação)**: Teste carrega o CSV de exemplo e confere quantidade, campos obrigatórios e tipos. Revisão confirma que não há `INSERT/UPDATE/DELETE` em `src/providers/sql/`.

### \[CARE-RF004\] Fila por exame

* **Context (Contexto)**: RF003 e RF005 implementados.  
* **Action (Ação)**: Criar `GET /api/fila?exame=&unidade=&especialidade=&periodo=` e a tela de fila.  
* **Result (Resultado)**: Lista ordenada pela prioridade com posição, paciente, prontuário, exame, motivo e status.  
* **Evaluation (Avaliação)**: Teste confere ordem e filtros sobre o CSV de exemplo; RNF012 medido com 1.000 solicitações.

### \[CARE-RF005\] Cálculo da prioridade

* **Context (Contexto)**: Regras do exame cadastradas (RF007) e lista de prioritários (RF008).  
* **Action (Ação)**: Implementar o cálculo como função pura: recebe as solicitações e a versão das regras e devolve a ordem e o motivo de cada item.  
* **Result (Resultado)**: Proposta inicial de critérios: (1) paciente na lista de prioritários; (2) data de retorno mais próxima; (3) antecedência por município; (4) ordem de chegada como desempate. Exame sem regra usa só a ordem de chegada.  
* **Evaluation (Avaliação)**: Testes unitários com cenários fixos: prioritário à frente, retorno próximo antes de distante, exame sem regra por data, empates estáveis e a mesma entrada gerando sempre a mesma ordem (RNF010).

### \[CARE-RF006\] Motivo da posição

* **Context (Contexto)**: RF005 devolve o critério decisivo de cada item.  
* **Action (Ação)**: Exibir o motivo na fila e no detalhe do pedido.  
* **Result (Resultado)**: Todo item tem um motivo legível, inclusive "Ordem de chegada".  
* **Evaluation (Avaliação)**: Teste garante que nenhum item da fila sai sem motivo.

### \[CARE-RF007\] Regras de prioridade por exame

* **Context (Contexto)**: Perfil `GESTOR_CENTRAL`; decisão D1 registrada.  
* **Action (Ação)**: CRUD de regras por exame (critérios ativos e ordem), gravando nova versão a cada alteração.  
* **Result (Resultado)**: A fila passa a usar a versão nova; as anteriores ficam consultáveis.  
* **Evaluation (Avaliação)**: Teste altera uma regra e confere a nova ordem, a nova versão e o registro em `audit_logs` (CONFIGURAÇÃO).

### \[CARE-RF008\] Lista de pacientes prioritários

* **Context (Contexto)**: Perfil `AREA_SOLICITANTE` vinculado à sua área.  
* **Action (Ação)**: Incluir e remover prontuários com exame, motivo e validade.  
* **Result (Resultado)**: Prontuários válidos sobem na fila do exame; vencidos deixam de valer automaticamente.  
* **Evaluation (Avaliação)**: Teste inclui um prontuário, confere a subida na fila e a volta à posição original após a validade.

### \[CARE-RF009\] Detalhe da solicitação

* **Context (Contexto)**: RF003 implementado.  
* **Action (Ação)**: Criar `GET /api/solicitacoes/{codigo}` e a tela de detalhe.  
* **Result (Resultado)**: Dados do AGHU e histórico local do pedido em uma única tela.  
* **Evaluation (Avaliação)**: Teste confere os campos retornados e o 404 para código inexistente.

### \[CARE-RF010\] Registro do tratamento

* **Context (Contexto)**: Perfil `MARCADOR`; marcação já feita no AGHU.  
* **Action (Ação)**: Criar `POST /api/solicitacoes/{codigo}/tratamento` com status, data agendada, unidade executora e observação.  
* **Result (Resultado)**: Pedido agendado ou cancelado sai da fila; "sem contato" e "pendente" permanecem com o status visível.  
* **Evaluation (Avaliação)**: Testes para cada status; "agendado" sem data é rejeitado; cada registro gera entrada em `audit_logs` (NEGÓCIO\_CLÍNICO).

### \[CARE-RF011\] Histórico do pedido

* **Context (Contexto)**: RF010 e RNF007 implementados.  
* **Action (Ação)**: Montar a linha do tempo do pedido a partir da trilha de auditoria.  
* **Result (Resultado)**: Lista cronológica de ações com usuário e data/hora, sem opção de editar ou excluir.  
* **Evaluation (Avaliação)**: Teste confere que não há rota de alteração ou exclusão de histórico e que a ordem cronológica é respeitada.

### \[CARE-RNF001\] Integração AGHU somente leitura

* **Context (Contexto)**: Credenciais de leitura fornecidas pela TI do HC.  
* **Action (Ação)**: Conectar ao AGHU com usuário sem permissão de escrita; consultas apenas em templates SQL.  
* **Result (Resultado)**: Qualquer tentativa de escrita é recusada pelo próprio banco.  
* **Evaluation (Avaliação)**: `uv run python audit_framework.py` aprovado e verificação de que os templates SQL contêm apenas `SELECT`.