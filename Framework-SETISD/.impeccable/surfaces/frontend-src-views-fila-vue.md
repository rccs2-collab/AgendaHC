---
version: 1
slug: "frontend-src-views-fila-vue"
primary_target: "frontend/src/views/Fila.vue"
related_targets: ["frontend/src/views/Painel.vue","frontend/src/views/Regras.vue"]
---

# Surface brief: Fila de marcação (AgendaHC)

Scope: the marcador's working queue, plus its satellites (Painel, Regras) inside the same shell. Mode: Operate.

Audience and task: marcador(a) of the Central de Marcação, desktop, during the shift. Pick the next patient, see every pending exam of that patient and any conflict between them, book in the AGHU, record the outcome here. Secondary: gestão reads Painel and edits Regras.

Content: anonymized AGHU extract (576 items, 415 patients, 49 exams, 8 unidades). Priority lists and incompatibility rules are example data and say so on screen. Return date, município and phone are not in the extract: shown as "sem dado".

Constraints: Framework SETISD shell and tokens evolve, not replace; pt-BR; AGHU read-only; nothing for the patient.

Unresolved: real priority rules per exam, open-slot data, return dates.

## Direction contract

THESIS: A queue of people, not of tickets. Each row is a patient with all their pending exams, ranked by the strongest reason among them, and the reason is printed on the row. Refuses the category default of one flat row per exam with an unexplained priority column.

OWN-WORLD: The framework's warm paper ground and charcoal sidebar, Nunito, teal primary for selection and actions. Reason chips carry the colour: teal-ink "Lista de prioridade", amber ramp for waiting days, neutral for "Ordem de chegada"; vermilion only for exam conflicts. Tabular figures for prontuário and days. Hairline-divided dense rows, no cards inside cards.

STORY: The marcador sees the queue already ordered, understands why the first patient is first, notices the conflict before booking, records the outcome, and the patient leaves the queue.

FIRST VIEWPORT: Sidebar left (AgendaHC, Fila, Painel, Regras, version footer). Top bar: title, AGHU freshness line, search by nome or prontuário. Second column: unidade rail with counts. Main: four-figure summary strip, then the ranked patient table (posição, paciente + prontuário, exames pendentes stacked, espera, motivo chip, conflito flag). Selecting a row opens a right detail panel with per-exam "Registrar tratamento". Primary action lives in that panel.

FORM: Patient-grouped ranked queue with unidade rail and side detail panel, sixth on my ordered list; seed:a2a8243e4d3dc533

SIGNATURE MOVE: the queue re-ranks in place like a departures board: when a priority list or rule changes, rows slide to their new positions keeping identity, and moved rows hold a "subiu N" mark until the next action.

FINISH: unreviewed and undocumented is unfinished; the run ends after the finish review's fixes and DESIGN.md.
