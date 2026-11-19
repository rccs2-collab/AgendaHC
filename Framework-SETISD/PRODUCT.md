# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- **Primary: marcador(a) da Central de Marcação de Exames do HC-UFPE.** Works at a desktop in the Central during the shift, clearing the day's exam requests: decides who gets the next open slot, books it in the AGHU, contacts the patient and records the outcome.
- **Secondary: gestão da Central de Marcação.** Watches demand and waiting time per exam; maintains priority rules.
- **Secondary: áreas solicitantes (e.g. nefrologia).** Maintain their list of priority patients (e.g. hemodialysis) instead of sending loose lists.
- Patients do not use the system (confirmed scope decision, Oct 2026).

## Product Purpose
AgendaHC reads exam requests (solicitações de exame) from the AGHU and turns them into one prioritized queue per exam for the Central de Marcação, replacing the Forms → spreadsheet → AGHU retyping loop and the informal, memory-based prioritization. Success: the marcador opens a ready, ordered queue and trusts why each request is where it is; management sees demand and waiting time per exam.

## Positioning
The queue order is explainable: every request shows the rule that placed it (priority list, waiting time, order of arrival), and the rules are the Central's own, configurable per exam. The AGHU stays the official system; AgendaHC never writes to it.

## Operating Context
- HC-UFPE (EBSERH), Recife. Exams handled by the UDI (ultrassonografia, medicina nuclear, mamografia, densitometria, radiologia, tomografia, ressonância) and fonoaudiologia.
- Today: patient fills a form, answers land in a spreadsheet, the marcador retypes the request number into the AGHU, marks the row green, contacts the patient by WhatsApp. Slots open roughly every two months.
- HC scope summary ("Otimização da Gestão de Vagas para Exames Diagnósticos") also asks to avoid incompatible exam combinations, respect preparation needs and use capacity well.
- Built on the HC's Framework SETISD (FastAPI + Vue 3 + Tailwind), institutional AD login, local SQLite for app data, AGHU read through SQL templates or an anonymized CSV in development.

## Capabilities and Constraints
- AGHU is read-only; booking, cancelling and the patient ticket stay in the AGHU.
- Requests identified by `codigo_solicitacao`; patients by prontuário.
- Current AGHU extract (Drive, Oct 2026): prontuário, nome (masked), telefone and cidade (placeholders), código da solicitação, data, unidade solicitante, código e nome do exame, funcionário solicitante. No return date, no real município, no phone yet.
- Undecided: priority rules per exam and their owner; minimum lead time by município; behavior when an exam has no open slots; whether the patient form is retired; extra AGHU fields; refresh frequency.
- Out of scope: any patient-facing channel, writing to AGHU, SUS/SES regulation, automatic WhatsApp.

## Brand Commitments
Framework SETISD layout and identity (HC-UFPE / EBSERH): sidebar app shell, version in the sidebar footer, pt-BR throughout.

## Evidence on Hand
- Anonymized AGHU extract: 576 exam items, 493 requests, 415 patients, 49 exam types, Aug–Sep 2026. Kept out of Git (`data/solicitacoes.csv`); the repo ships `data/solicitacoes_sinteticas.csv`, same shape with fictitious identifiers.
- Example AGHU ticket (Drive) and the extraction SQL.
- No real priority lists, return dates or incompatibility rules yet; anything shown for those is example data and must be labeled so.

## Product Principles
1. Explain every position: no request sits in the queue without a readable reason.
2. AGHU is the source of truth; AgendaHC reads, organizes and records, never books.
3. Rules belong to the Central, not to the code: configurable per exam, versioned, audited.
4. Built for a shift at a desk: dense, scannable, fast to act on, nothing decorative.
5. Show what is missing instead of inventing it (no return date yet means "sem dado", not a guess).

## Accessibility & Inclusion
Long shifts on shared hospital desktops: readable sizes, strong contrast, status never conveyed by color alone, full keyboard use of the queue.
