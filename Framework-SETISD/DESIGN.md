---
name: AgendaHC
description: Fila de marcação explicável da Central de Marcação do HC-UFPE, sobre o Framework SETISD.
colors:
  acao: "#3d6d6e"
  acao-hover: "#335c5d"
  acao-suave: "#e4eeee"
  lista-ink: "#2c5c5d"
  lista-bg: "#dfecec"
  espera-ink: "#7a5100"
  espera-bg: "#fbefd4"
  chegada-ink: "#5d5851"
  chegada-bg: "#ecebe6"
  separar-ink: "#a33811"
  separar-bg: "#fbe4d9"
  ordem-ink: "#574887"
  ordem-bg: "#ebe7f5"
  agrupar-ink: "#22627a"
  agrupar-bg: "#dff0f6"
  ok-ink: "#2f6b49"
  ok-bg: "#dff1e6"
  paper-bg: "#f4f3ef"
  paper-sidebar: "#33312e"
  paper-active-link: "#4a4743"
  surface: "#ffffff"
  surface-sunken: "#faf9f6"
  ink: "#2b2925"
  ink-muted: "#6b665f"
  line: "#e3e0d8"
  line-strong: "#d3cfc5"
  paper-disabled: "#e0e0e0"
  faixa-30: "#c9d9d9"
  faixa-60: "#e9c46f"
  faixa-90: "#d98a2b"
typography:
  figure-lg:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 800
    fontFeature: "'tnum' 1"
  figure:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 800
    fontFeature: "'tnum' 1"
  headline:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 700
  title:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 800
    lineHeight: 1.375
  section:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 800
  body:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.43
  label:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
  tag:
    fontFamily: "Nunito, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.6875rem"
    fontWeight: 700
rounded:
  sm: "2px"
  default: "4px"
  md: "6px"
  lg: "8px"
  full: "9999px"
spacing:
  cell-x: "8px"
  cell-y: "10px"
  gutter: "24px"
  panel: "20px"
components:
  button-acao:
    backgroundColor: "{colors.acao}"
    textColor: "{colors.surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "6px 12px"
  button-acao-hover:
    backgroundColor: "{colors.acao-hover}"
  button-acao-disabled:
    backgroundColor: "{colors.paper-disabled}"
    textColor: "{colors.ink-muted}"
  button-secundario:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "6px 12px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
  motivo-lista:
    backgroundColor: "{colors.lista-bg}"
    textColor: "{colors.lista-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
  motivo-espera:
    backgroundColor: "{colors.espera-bg}"
    textColor: "{colors.espera-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
  motivo-chegada:
    backgroundColor: "{colors.chegada-bg}"
    textColor: "{colors.chegada-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
  alerta-separar:
    backgroundColor: "{colors.separar-bg}"
    textColor: "{colors.separar-ink}"
    typography: "{typography.tag}"
    rounded: "{rounded.default}"
    padding: "1px 6px"
  status-agendado:
    backgroundColor: "{colors.ok-bg}"
    textColor: "{colors.ok-ink}"
    typography: "{typography.tag}"
    rounded: "{rounded.default}"
    padding: "1px 6px"
  fila-linha:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: "10px 8px"
  fila-linha-selecionada:
    backgroundColor: "{colors.acao-suave}"
  fila-linha-subiu:
    backgroundColor: "{colors.lista-bg}"
  rail-item:
    textColor: "{colors.ink-muted}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 10px"
  rail-item-active:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
  painel-detalhe:
    backgroundColor: "{colors.surface}"
    width: "400px"
    padding: "16px 20px"
  sidebar:
    backgroundColor: "{colors.paper-sidebar}"
    width: "224px"
---

# Design System: AgendaHC

## Overview

**Creative North Star: "The Annotated Queue"**

AgendaHC is a working instrument for a marcador at a desk through a whole shift. It keeps the Framework SETISD shell the hospital already knows: warm paper ground, charcoal sidebar with the version in its footer, Nunito everywhere. The new parts are a deep teal action color and a small set of paired ink-on-tint colors, each tied to exactly one reason or state. Every row is a patient. The reason for the row's position is printed on it as a chip, and the color comes from that reason, not from decoration.

Density is high and flat. Rows are divided by hairlines, and containers are white panels on paper with a 1px ring. Shadows are almost absent. Numbers that people compare (position, prontuário, days, counts) always use tabular figures. Motion has one job, which is to make a re-rank legible: rows slide to their new place and keep their identity.

**Key Characteristics:**
- Framework SETISD shell evolved, not replaced: paper ground, charcoal sidebar, version footer.
- One action color (teal) for buttons, links, focus, caret, selection and the selected row.
- Ink-on-tint pairs as the semantic vocabulary, always with an icon and a text label.
- Hairline-divided dense tables, tabular figures, no cards inside cards.
- In-place re-rank motion with a persistent "subiu N" mark.

## Colors

Warm neutrals carry the structure. Color appears only as a teal action signal and as paired semantic chips.

### Primary
- **Ação Teal** (acao): every primary button, text link, focus outline, input caret and accent, and the refresh control. Hover deepens to acao-hover. The pale tint acao-suave fills the selected queue row and text selection.

### Semantic pairs (ink on tint)
Each pair is used as dark text and icon on a light tint of the same hue. Every pair reaches at least 5.3:1.
- **Lista Teal** (lista-ink / lista-bg): the "Lista de prioridade" reason, the priority count in the summary strip, priority-list area names, and the "subiu N" re-rank mark and row wash.
- **Espera Amber** (espera-ink / espera-bg): the "Espera > N dias" reason, the median-wait figure and the over-60 total in Painel, and day counts in rows or unit cells that exceed the waiting limit.
- **Chegada Stone** (chegada-ink / chegada-bg): the "Ordem de chegada" reason and the Cancelado status. The tint alone, with ink text, backs the criteria pills in the ordering line.
- **Separar Vermilion** (separar-ink / separar-bg): conflict and failure. Used for the "Não no mesmo dia" combination alert, the combination-alert count, the Sem contato status, every error banner and inline error, the error toast, and the hover state of destructive Remover.
- **Ordem Violet** (ordem-ink / ordem-bg): the "Ordem obrigatória" combination alert only.
- **Agrupar Blue** (agrupar-ink / agrupar-bg): the "Agendar junto" combination alert and the Em contato status.
- **OK Green** (ok-ink / ok-bg): the Agendado no AGHU status and the scheduled-date line.

### Wait-band ramp
- **Faixas** (faixa-30, faixa-60, faixa-90, then separar-ink for more than 90 days): the stacked wait-distribution bar and its legend in Painel. These values are inline in the bar component, not theme variables.

### Neutral
- **Paper** (paper-bg): app ground, the unit rail, and the queue's toolbar and sticky header.
- **Charcoal Sidebar** (paper-sidebar), with paper-active-link marking the active nav item.
- **Surface White** (surface): table rows, the detail panel, the top bar and section panels. **Sunken** (surface-sunken) is used for row hover, table heads in Painel/Regras, and the rule list.
- **Ink** (ink, 13:1 on paper) for primary text. **Ink Muted** (ink-muted, at least 5.1:1) for secondary text, column heads and units.
- **Line** (line) for hairlines and rings. **Line Strong** (line-strong) for input borders and the scrollbar thumb.
- **Disabled** (paper-disabled) is the fill for disabled primary buttons.

### Named Rules
**The Reason Owns the Color Rule.** A hue appears only because a reason or state named in text sits next to it. No color is decorative, and no chip or tag ships without its icon and label.

**The Amber Is Waiting Rule.** Amber is the waiting-time color. Summary figures and wait bands use it as a category color. In a row or per-unit cell, a day count turns amber only when it is over the unit rule's limit (or the 60-day Painel threshold), and stays in ink otherwise.

**The Vermilion Is Trouble Rule.** On chips, tags, text and alerts, vermilion means a conflict between exams or a failure that needs action, and never priority or waiting. The one exception is the top step of the wait-band bar. It differs from the direction contract and should not be extended.

**The One Teal Action Rule.** Acao is the only action color. Lista teal is a reason, not a button.

## Typography

**Font:** Nunito (loaded at 400, 600, 700 and 800), falling back to ui-sans-serif and system-ui.

**Character:** One rounded humanist sans used at every level. Hierarchy comes from weight (800 for figures and names, 700 for labels) more than size. The steps are 10 / 11 / 12 / 14 / 16 / 18 / 20 / 30px.

### Hierarchy
- **Figure large** (800, 30px, tabular): Painel totals.
- **Figure** (800, 20px, tabular): the four-figure summary strip above the queue. Each figure takes the color of the reason it counts.
- **Headline** (700, 18px): the page title in the top bar.
- **Title** (800, 16px, 1.375): patient name in the detail panel, the rule name in Regras, and the queue position number.
- **Section** (800, 14px): panel headings in Painel and Regras.
- **Body** (400 to 700, 14px): table cells. Patient names are 700 and exam names 600 when they belong to the current unit.
- **Label** (700, 12px): column heads, detail-panel section heads, form labels and reason chips. Sentence case with normal tracking.
- **Tag** (700, 11px): status tags, combination alerts and the "subiu N" mark. 10–11px is also used for the sidebar footer and help notes.

### Named Rules
**The Tabular Figures Rule.** Positions, prontuários, request codes, dates, day counts and every count use the `tabular` utility (tnum), so columns line up.

**The Sentence Case Rule.** Labels and headings are sentence case pt-BR at normal tracking. The build has no uppercase or letter-spaced labels.

## Layout

The shell is a full-height flex layout. The sidebar is 224px, collapses to 72px icons, and becomes an off-canvas drawer below md. Next to it are a 56px white top bar with the page title and the profile control, then a scrolling main area on paper.

The queue has three columns. On the left is a 240px unit rail (lg and up; below that it becomes a select). The center is the table section. On the right, a 400px detail panel opens only when a row is selected. While the panel is open the queue goes compact: the Combinação column folds into the Motivo cell, summary gaps tighten, and the rail is hidden.

The page gutter is 24px. Panel padding is 20px. Table cells are 8px wide by 10px tall in the queue and 12px tall in Painel. Vertical stacks use 4 to 12px gaps. Painel and Regras cap their content at 1280px. The queue table is fixed-layout with set widths for position, patient, wait, reason and combination, and the exams column takes the remaining space. Long lists render 60 patients, then offer "Mostrar mais 60".

**The Hairline Density Rule.** Rows are separated by 1px line borders, never by gaps or cards. Rows are top-aligned so a patient's stacked exams read as one row.

## Elevation & Depth

The system is flat and tonal. Depth comes from paper versus white surfaces, 1px line borders and 1px rings. The queue's sticky header uses paper at 95% with a small backdrop blur. Only two shadows exist:
- **Rail lift** (`0 1px 2px rgba(43,41,37,0.08)` with a 1px line ring): the active unit in the rail.
- **Toast** (`0 6px 20px -6px rgba(43,41,37,0.35)`): bottom-left toasts, ink background for success and info, vermilion for error, 8px radius, 14px/600 text.

The framework's `shadow-paper` (on its Card component) survives only on the inherited Login and Configurações screens. The Fila, Painel and Regras screens don't use it.

**The Ring, Not Shadow Rule.** Containers are surface white with a 1px line ring. A new shadow needs a state to justify it.

## Shapes

Corners are gently rounded and stay small. Bars use 2px. Status tags, alerts and icon buttons use 4px. Buttons, inputs, rail items and result options use 6px. Section panels and toasts use 8px. The fully rounded pill is reserved for the reason chip (MotivoChip), so a row's reason is the only rounded capsule on it.

## Components

### Buttons
- **Primary (acao):** white on acao, 14px/700, 6px radius, 6px × 12px padding (8px × 16px for "Salvar nova versão"). Hover turns acao-hover. Disabled uses the paper-disabled fill with ink-muted text.
- **Secondary:** surface with a 1px line-strong ring or border, ink 600 text, sunken on hover ("Incluir na lista de prioridade", "Mostrar mais 60").
- **Quiet:** muted text that darkens to ink on hover (Cancelar, Desfazer). **Text link:** acao 600–700, underline offset 2px, darkens on hover.
- **Destructive:** quiet muted text that gets a vermilion tint on hover only (Remover).

### Reason chip (MotivoChip)
A pill (full radius, 2px × 10px, 12px/700) with a 14px solid icon: list for Lista, clock for Espera, tray for Chegada. The title attribute carries the detailed reason. It appears in the row's Motivo column and in the detail-panel header.

### Status tag and combination alert
Small 4px-radius tags (1px × 6px, 11px/700) with a 12–14px icon. StatusTag stays hidden while an item is Pendente. Em contato, Sem contato, Agendado and Cancelado map to agrupar, separar, ok and chegada. AlertaCombinacao maps Separar, Ordem and Agrupar to their pairs, with the marcador guidance in its title.

### Queue row
Surface white, sunken on hover, acao-suave when selected. A moved row is washed in lista-bg at 45% and keeps a "subiu N" tag (arrow up plus the count) next to its position. The tag stays until the next reload of the queue. The position is shown in 16px/800 tabular figures. The patient cell shows the name with the prontuário below it. Exams stack one per line with a short date, plus the unit when it differs from the current one.

### Re-rank motion
Rows are keyed by patient and slide to their new index over 480ms with `cubic-bezier(0.16, 1, 0.3, 1)`. Entering rows fade in over 200ms and leaving rows fade out over 160ms. After a priority change, rows that moved up get the "subiu N" mark, a toast reports "Subiu de Xº para Yº", and the row scrolls into view. Positions are kept in sessionStorage so a re-rank made on another screen still animates when the queue opens. The detail panel enters with 180ms opacity and a 12px slide. Under `prefers-reduced-motion: reduce` the row slide and the panel transition are removed. The row opacity fades, skeleton pulse and refresh spinner still run.

### Inputs
Surface, 1px line-strong border, 6px radius, 14px ink text with muted placeholder. Search has a 16px leading icon and on focus gets an acao border with a 2px acao ring at 20%. Result choices are radio cards (1px line ring, 2px acao ring when checked or keyboard-focused).

### Navigation
The charcoal sidebar uses gray-300 600 text with 20px outline icons and a 4px radius. Hover uses the active-link color at 70% with white text, and the active item gets solid paper-active-link with white text. The brand block shows AgendaHC 18px/800 with "Central de Marcação" 11px below it. The footer shows the app name and "Versão X | HC-UFPE", or "vX" when the sidebar is collapsed.

### Detail panel
A 400px white aside with a left hairline. It has a sticky header (name, prontuário, "Nº na fila" and the reason chip with its detail), then hairline-divided sections: combination, exams with per-item "Registrar resultado", priority list, missing-data note and history.

### Wait-band bar (BarraFaixas)
A stacked horizontal bar (10px, or 16px when tall, 2px radius, line track) with the four wait bands. It is exposed with `role="img"` and an aria-label listing every band.

## Do's and Don'ts

### Do:
- **Do** print the reason next to every colored mark: icon, text label, and a title for the detail.
- **Do** use acao for every action, link and focus state, and use acao-suave for selection.
- **Do** set every comparable number in tabular figures.
- **Do** say what is missing ("Sem prontuário no extrato", "sem dado") in ink-muted text instead of leaving a gap.
- **Do** keep keyboard paths: the roving-tabindex queue (arrow keys, Enter opens the panel and focuses its heading, Esc closes and returns focus to the row), a 2px acao focus-visible outline, sr-only labels on summary figures and search, and `role="alert"` on errors.
- **Do** keep re-rank motion in place and identity-preserving, and remove the slide under reduced motion.

### Don't:
- **Don't** color a row's day count amber when it is under the unit limit. Don't use vermilion chips, tags or text for anything that is not a conflict or a failure.
- **Don't** put a card inside a panel or separate rows with gaps. Use hairlines and rings.
- **Don't** use the framework's paper-primary/info/success/warning/danger fills for new actions. White text on them falls below 3:1.
- **Don't** add uppercase tracked labels or eyebrow text above headings.
- **Don't** convey state by tint alone. Every pair carries an icon and words.
