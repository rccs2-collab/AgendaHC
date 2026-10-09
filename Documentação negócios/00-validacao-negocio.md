# AgendaHC — Documento de Validação e Especificação de Negócio

> **Padrão Oficial SETISD / HC-UFPE (HU Brasil) — Fase 0 (Alinhamento de Negócio)**  
> **Público-alvo:** Central de Marcação de Exames, áreas solicitantes e
Equipe de TI.  
> **Objetivo:** Descrever o processo em linguagem de negócio, para
validação e tomada de decisão antes de qualquer codificação.

---

## 1. Identificação do Projeto e Contexto Institucional

| Campo | Descrição |
| :--- | :--- |
| **Nome do Sistema** | AgendaHC |
| **Área Solicitante / Cliente** | Central de Marcação de Exames do HC-UFPE |
| **Instância Superior Competente** | Tatiane |
| **Líder Técnico (SETISD)** | Tiago Ferrão |
| **Objetivo Estratégico HU Brasil** | Qualificar o acesso do paciente aos serviços de apoio diagnóstico |

---

## 2. O Problema que Queremos Resolver

Hoje o pedido de agendamento de exames chega por um formulário do Google, vira uma
planilha e precisa ser conferido e redigitado manualmente no AGHU pela Central de Marcação.
Esse vai e volta entre planilha e AGHU gera retrabalho e erros constantes, principalmente no
número de solicitação, que é obrigatório para marcar o exame e que muitos pacientes
preenchem errado, às vezes colocando o número de celular no lugar.
Isso não pode continuar porque cada pedido com erro precisa ser investigado ou devolvido, o
que consome o tempo da equipe e atrasa o atendimento. Além disso, a fila hoje segue apenas
a ordem de chegada na planilha, sem critério formal de prioridade. Isso dificulta atender
primeiro quem precisa, como os pacientes de hemodiálise, e também levar em conta a data de
retorno do paciente ao médico ou a distância entre a cidade onde ele mora e o hospital. A
gestão também não tem uma visão clara de quantos pedidos estão pendentes, por exame, nem
de quanto tempo o paciente espera.

---

## 3. Como o Processo Funciona Hoje (A Rotina Atual)

O pedido de exame é feito pelo médico no AGHU durante a consulta, e o paciente sai com um
ticket impresso que traz o número da solicitação. Esse ticket é gerado exclusivamente pelo
AGHU e não pode ser alterado. Com ele em mãos, o paciente preenche um formulário do
Google informando o exame, a data de retorno ao profissional que pediu o exame, seu nome, o
número do prontuário, a idade, o município onde mora, o número da solicitação e um telefone
ou WhatsApp para receber a resposta. O formulário mostra uma foto do ticket indicando qual
número digitar, mas os erros continuam frequentes.
As respostas caem numa planilha no Google Drive. A Central de Marcação abre cada pedido,
copia o número da solicitação e o pesquisa no AGHU, que mostra o paciente, a especialidade
de origem e a consulta vinculada. Se o número estiver errado, o AGHU informa que a
solicitação não foi encontrada e o pedido fica travado. Se estiver certo, a equipe escolhe uma
vaga, marca o exame no AGHU, avisa o paciente pelo WhatsApp e pinta a linha da planilha de
verde. Os pedidos ainda não tratados ficam em branco.
As vagas costumam ser abertas a cada dois meses, mas podem ser liberadas a qualquer
momento, por exemplo quando chegam novos médicos a uma unidade. Para evitar uma fila
impossível de atender, os exames sem vaga ficam sinalizados no formulário, e o paciente é
orientado a procurar também a unidade básica de saúde, já que parte das vagas do hospital é
repassada mensalmente ao estado. As prioridades são tratadas de forma informal: a equipe de
nefrologia envia uma lista dos pacientes de hemodiálise que precisam fazer ultrassom das vias
urinárias com mais urgência, e cada exame tem particularidades que a equipe conhece de
memória.

---

## 4. O Que a Nova Solução Deve Entregar (Resultado Esperado)

A proposta é substituir a planilha, e as trocas informais que giram em torno dela, por um
sistema interno do hospital que funcione ao lado do AGHU. Nele, cada pedido é conferido com
os dados oficiais do AGHU antes de chegar à fila, e a Central de Marcação passa a trabalhar
com uma fila organizada por exame e por prioridade, e não mais com uma planilha lida linha
por linha.
Os ganhos imediatos esperados são o fim dos pedidos com solicitação inválida chegando à
equipe, menos tempo gasto em conferência manual, uma fila que respeita as regras de cada
exame e uma visão clara, para a gestão, da demanda e das pendências.

---

## 5. Como Será o Trabalho no Novo Sistema (O Novo Fluxo)

O pedido do paciente chega ao sistema com o número da solicitação e os mesmos dados que
hoje são pedidos no formulário. O canal por onde esse pedido entra ainda precisa ser decidido
(ver Seção 9). O sistema confere a solicitação com o AGHU assim que o pedido chega. Se ela
existir e corresponder ao paciente, o pedido entra na fila do exame correspondente. Se não, o
pedido é barrado e o motivo fica registrado, para que o paciente seja orientado a corrigir.
A Central de Marcação abre a fila já organizada, com os pedidos válidos e as prioridades
aplicadas. Nessa ordenação entram a lista de pacientes prioritários, a data de retorno ao
médico e a distância entre o município do paciente e o hospital. A equipe continua fazendo a
marcação final no AGHU, que segue sendo o sistema oficial, e registra no novo sistema que o
pedido foi agendado. Esse registro substitui a linha pintada de verde na planilha. A gestão
acompanha em um painel quantos pedidos existem por exame, quantos já foram atendidos e
há quanto tempo cada um espera.

---

## 6. Quem Participa do Processo (Atores: Como Faz Hoje vs. Como Fará no Sistema)

O **paciente** hoje preenche um formulário sem nenhuma conferência. No novo sistema, seu
pedido será validado antes de entrar na fila, e ele será avisado do resultado. Ele não terá
acesso a informações de outros pacientes nem à fila completa. Se o paciente vai interagir
diretamente com o sistema ou continuar usando outro canal ainda está em aberto.

A **Central de Marcação** hoje alterna entre a planilha, o AGHU e o WhatsApp e corrige erros
manualmente. No novo sistema, trabalhará a partir de uma fila já validada e organizada,
marcando no AGHU e registrando o resultado. Ela não altera as regras de prioridade por conta
própria.

As **áreas que definem prioridades**, como a nefrologia, hoje enviam listas avulsas. No novo
sistema, suas regras e listas passam a ser aplicadas de forma padronizada na fila. Elas não
fazem agendamentos.

A **gestão** hoje não tem visão consolidada da demanda. No novo sistema, acompanhará
indicadores em um painel, apenas para consulta, sem editar pedidos.

---

## 7. Regras de Negócio Inegociáveis (RNs)

* **RN-01 (Solicitação válida obrigatória):** nenhum pedido entra na fila sem um número de
solicitação que exista no AGHU e corresponda ao paciente.
* **RN-02 (AGHU como sistema oficial):** o novo sistema apenas consulta o AGHU e nunca grava
nada nele. A solicitação do exame, a marcação final e o ticket do paciente continuam sendo
feitos exclusivamente no AGHU.
* **RN-03 (Prioridade por exame):** cada exame pode ter sua própria regra de prioridade, definida
pela área responsável, como a prioridade dos pacientes de hemodiálise no ultrassom das vias
urinárias. Na ausência de regra, vale a ordem de chegada.
* **RN-04 (Data de retorno e antecedência):** a data de retorno ao médico orienta o
agendamento, para que o exame seja feito antes da próxima consulta. O sistema também não
deve sugerir vagas que o paciente não consiga aproveitar por causa da distância entre seu
município e o hospital. A antecedência mínima exata será definida pela área de negócio.
* **RN-05 (Respeito à disponibilidade de vagas):** exames sem vagas abertas não recebem
novos pedidos, a menos que a gestão decida manter uma lista de espera (ver Seção 9).
* **RN-06 (Dados mínimos do paciente):** o sistema coleta apenas os dados necessários para
identificar o paciente, o pedido e a forma de contato, em conformidade com a LGPD.
* **RN-07 (Histórico preservado):** todo pedido guarda o registro de quando foi feito, quem o
tratou e qual foi o resultado. Esse histórico não pode ser apagado.
* **RN-08 (Acesso institucional):** a equipe interna acessa o sistema com o login institucional do
hospital, para que toda ação fique vinculada ao seu autor.
* **RN-09 (Escopo interno):** a fila tratada pelo sistema é apenas a do hospital. Pacientes
encaminhados pela regulação do SUS ou pela Secretaria Estadual de Saúde ficam fora do
escopo.

---

## 8. Painel de Gestão e Indicadores Estratégicos (KPIs)

O painel deve mostrar, por exame, quantos pedidos estão na fila e há quanto tempo, em média,
os pacientes esperam entre o pedido e o agendamento. Também deve mostrar quantos
pedidos foram barrados por solicitação inválida, o que ajuda a medir o problema atual e a ver
onde a orientação ao paciente precisa melhorar. Deve mostrar ainda quantos exames foram
agendados depois da data de retorno do paciente ao médico, já que esses casos indicam falha
no atendimento. Por fim, deve mostrar quantos pedidos prioritários existem e se estão sendo
atendidos antes dos demais.
---

## 9. Matriz de Pontos de Decisão (Gabinete / Gestão do Negócio)

> *Itens que dependem de confirmação dos gestores do hospital antes da conclusão:*

| # | Ponto a Decidir | Impacto no Processo | Quem deve decidir? | Status / Definição |
| :-: | :--- | :--- | :--- | :--- |
| **1** | O paciente fará o pedido diretamente no novo sistema ou por outro canal, com o sistema sendo usado só pela equipe interna?| Define se haverá tela para o paciente e como a validação da solicitação chega até ele. | TI e Central de Marcação | 🟡 Em definição |
| **2** | Quais dados o paciente informa para confirmar que a solicitação é dele? | Define a segurança da validação e a facilidade de uso. | Central de Marcação e TI | 🟡 Em definição |
| **3** | Qual a regra de prioridade de cada exame e quem é responsável por mantê-la? | Define como a fila é ordenada. | Áreas solicitantes e gestão | 🟡 Em definição |
| **4** | Qual a antecedência mínima de agendamento conforme o município do paciente? | Evita oferecer vagas que o paciente não consegue aproveitar. | Central de Marcação | 🟡 Em definição |
| **5** | Exame sem vaga bloqueia o pedido ou gera lista de espera? | Define se a demanda reprimida passa a ser registrada. | Gestão da Central | 🟡 Em definição |
| **6** | Com que frequência os dados do AGHU precisam ser atualizados no sistema? | Define se a validação usa dados do momento ou de algumas horas atrás. | TI e Central de Marcação | 🟡 Em definição |
| **7** | Como o paciente será avisado de que o exame foi agendado? | Define se o WhatsApp continua como canal e se o sistema precisa apoiar esse contato. | Gestão da Central | 🟡 Em definição |

---
---

# Como este documento se liga aos demais

Este documento é a ponte entre a área de negócio e a equipe de engenharia. Depois de
validado com a Central de Marcação, suas Seções 2 a 4 alimentam o 01-visao.md. As Seções
5 a 7 viram requisitos e casos de uso. A Seção 8 orienta as telas de acompanhamento, e a
Seção 9 define os parâmetros que ainda precisam ser configurados antes da implementação.
