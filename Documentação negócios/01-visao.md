# Documento de Visão - Sistema de Agendamento de Exames

## 1. Problema e Oportunidade
**O Problema**: o agendamento de exames no HC-UFPE depende de um fluxo manual entre um
formulário do Google, uma planilha no Drive e o AGHU. A Central de Marcação redigita cada
pedido no AGHU, e boa parte deles chega com o número de solicitação errado, o que impede a
marcação e gera retrabalho.

**Impacto**: a equipe gasta tempo conferindo e corrigindo pedidos em vez de agendar. Pacientes
esperam mais do que o necessário. A fila segue apenas a ordem de chegada, o que dificulta
respeitar prioridades clínicas como a da hemodiálise, e a gestão não tem visão consolidada da
demanda por exame.

**Solução Proposta**: um sistema web que recebe o pedido do paciente e confere na hora,
contra os dados do AGHU, se a solicitação existe e pertence a ele. Os pedidos válidos entram
numa fila organizada por exame e por prioridade, que a Central de Marcação usa para fazer a
marcação no AGHU. O sistema apenas lê o AGHU e guarda seus próprios dados, como fila,
status e histórico, em uma base local.

## 2. Partes Interessadas (Stakeholders)
Os usuários finais são os pacientes, que fazem o pedido, e a equipe da Central de Marcação,
que trata a fila e agenda no AGHU. As áreas que definem prioridades, como a nefrologia,
participam indicando quem deve ser atendido primeiro. A gestão da Central e as chefias
acompanham os indicadores. A equipe de TI do hospital responde pelo acesso aos dados do
AGHU e pela sustentação do sistema. A Ebserh, como mantenedora do AGHU, é uma parte
interessada indireta, já que o sistema depende da estrutura de dados definida por ela.

## 3. Escopo do Produto
Estão dentro do escopo o pedido de agendamento pelo paciente com validação imediata da
solicitação, a fila por exame com regras de prioridade configuráveis, o controle de exames com
e sem vagas abertas, o registro do resultado de cada pedido pela Central e um painel de
acompanhamento para a gestão.
Estão fora do escopo qualquer gravação ou alteração no AGHU, que continua sendo o único
lugar onde a marcação é efetivada e o comprovante do paciente é emitido. Também ficam fora
a integração com a central de regulação do SUS e com a Secretaria Estadual de Saúde, já que
o projeto se restringe ao hospital. A leitura dos dados do AGHU será feita por consulta ao
banco ou por arquivo espelhado disponibilizado pela TI, e o sistema deve isolar esse acesso
em um único ponto, para que ele possa ser trocado no futuro por uma integração oficial sem
refazer o restante.

## 4. Metas e Objetivos de Negócio
A principal meta é eliminar os pedidos que chegam à Central com número de solicitação
inválido, já que a validação passa a acontecer antes do envio. Espera-se também reduzir o
tempo entre o pedido do paciente e o agendamento e o tempo gasto pela equipe em
conferência manual. Por fim, o objetivo é garantir que os pedidos prioritários sejam atendidos
antes dos demais e dar à gestão uma visão contínua da demanda de cada exame. Os valores
de referência de cada meta dependem de um levantamento da situação atual, a ser feito com a
Central de Marcação antes do início do desenvolvimento.
