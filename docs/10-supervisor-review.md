# M1 deliverable review and feedback report

| Item | Value |
| --- | --- |
| Work item | [MDP-11 — Supervisor review of M1 deliverables and recording of feedback](https://nauka11.youtrack.cloud/issue/MDP-11) |
| Milestone / due date | M1 pre-defense-1 / 24 October 2026 |
| Report date | 24 October 2026 |
| Supervisor | Myrzakerimova Alua |
| Decision status | Recommended dispositions and follow-up actions recorded for all 13 findings |

## Evidence and deliverables

The following immutable links identify the published materials available for review. Remote branch heads were checked with `git ls-remote --heads origin` on the preparation date and matched the local remote-tracking revisions. Tracker states were read separately from YouTrack. A completed work item establishes its recorded delivery status, not supervisor approval or application acceptance. MDP-9 is published and recorded as Done; MDP-10 is still queued and has no linked evidence in this packet. Tracker states were refreshed on 24 October 2026.

| Issue | Published review material | Branch / frozen revision | Tracker state at preparation |
| --- | --- | --- | --- |
| [MDP-1](https://nauka11.youtrack.cloud/issue/MDP-1) | [Proposal and scope](https://github.com/nauka2103/med-data-platform/blob/7b71fbdfb1161ed0e8a993fd1e07cdade92ddb78/docs/01-proposal.md) | `MDP-1-project-proposal` / `7b71fbdfb1161ed0e8a993fd1e07cdade92ddb78` | Done |
| [MDP-2](https://nauka11.youtrack.cloud/issue/MDP-2) | [Literature review](https://github.com/nauka2103/med-data-platform/blob/5ddbba4508cacfa1e816d170aeadff89499759a0/docs/03-literature/README.md) | `MDP-2-literature-review` / `5ddbba4508cacfa1e816d170aeadff89499759a0` | Done |
| [MDP-3](https://nauka11.youtrack.cloud/issue/MDP-3) | [Existing systems comparison](https://github.com/nauka2103/med-data-platform/blob/0d99f30ed1e87f47fb8d45a2e6e16f740db0f871/docs/02-existing-systems-comparison.md) | `MDP-3-existing-systems-comparison` / `0d99f30ed1e87f47fb8d45a2e6e16f740db0f871` | Done |
| [MDP-4](https://nauka11.youtrack.cloud/issue/MDP-4) | [Technology decisions](https://github.com/nauka2103/med-data-platform/blob/2a35a58d34c10e4a5ee141bb7f8b99911fcfbeba/docs/03-technology-comparison.md) | `MDP-4-technology-comparison` / `2a35a58d34c10e4a5ee141bb7f8b99911fcfbeba` | Done |
| [MDP-5](https://nauka11.youtrack.cloud/issue/MDP-5) | [Requirements and acceptance criteria](https://github.com/nauka2103/med-data-platform/blob/dbc7bd494a214f10adacbbcf0761b6ae575d8d30/docs/06-requirements.md) | `MDP-5-requirements-specification` / `dbc7bd494a214f10adacbbcf0761b6ae575d8d30` | Done |
| [MDP-6](https://nauka11.youtrack.cloud/issue/MDP-6) | [Architecture and diagrams](https://github.com/nauka2103/med-data-platform/blob/83cba5885bb70a1a197d90c23eda6f0a037260ba/docs/04-architecture.md) | `MDP-6-architecture-diagrams` / `83cba5885bb70a1a197d90c23eda6f0a037260ba` | Done |
| [MDP-7](https://nauka11.youtrack.cloud/issue/MDP-7) | [UX scenarios and exports](https://github.com/nauka2103/med-data-platform/blob/0d6b64b2109cbfa79c0b92b68fa918ba05f7c7d1/docs/08-ux-wireframes.md) | `MDP-7-ux-wireframes` / `0d6b64b2109cbfa79c0b92b68fa918ba05f7c7d1` | Done |
| [MDP-8](https://nauka11.youtrack.cloud/issue/MDP-8) | [Verification and evaluation plan](https://github.com/nauka2103/med-data-platform/blob/6c65fb43f54c7edc04e55ae1b3e1328cfac6555f/docs/09-verification-evaluation-plan.md) | `MDP-8-verification-evaluation-plan` / `6c65fb43f54c7edc04e55ae1b3e1328cfac6555f` | Done |
| [MDP-9](https://nauka11.youtrack.cloud/issue/MDP-9) | [Repository setup](https://github.com/nauka2103/med-data-platform/blob/55a3efda749ef26ffb8f49d3a276c340661d6190/README.md) | `MDP-9-repository-setup` / `55a3efda749ef26ffb8f49d3a276c340661d6190` | Done |

The literature branch also contains `docs/03-literature/references.md`. The architecture branch contains editable DOT diagrams and PNG/SVG exports in `diagrams/`. The UX branch contains interface sources and exports in `mockups/`. These are separate feature-branch deliveries; the review packet does not merge them. Follow the fixed revision links rather than assuming that every document is on the repository default branch.

## Review findings and recommended decisions

This report contains generated review findings and recommended responses. It does not attribute comments or approval to Myrzakerimova Alua. “Accept” recommends addressing or retaining the stated requirement; “Defer” recommends keeping the item outside the diploma scope. Each finding includes a rationale, an actionable follow-up and existing task links. Suggested roles route the work without changing tracker assignments or deadlines. Implementation completion requires the evidence specified in each row.

| ID | Finding | Recommended decision and reason | Follow-up and completion evidence | Linked task(s) / suggested role |
| --- | --- | --- | --- | --- |
| D01 | Proposal: the breadth of patient records, laboratories, summaries and two clients may exceed the available implementation time. | Accept: preserve the Must/Should/Could priorities and agree an achievable demonstration scope before adding features. | Confirm the M1 scope and map the demonstration to S1–S4; record any deferral and requirement impact explicitly. | [MDP-1](https://nauka11.youtrack.cloud/issue/MDP-1), [MDP-5](https://nauka11.youtrack.cloud/issue/MDP-5) / all |
| D02 | Literature: benchmark results on other document types and synthetic records do not establish this prototype's extraction quality or clinical value. | Accept: retain the documented evidence boundaries in the thesis and presentation. | Trace each performance claim to its dataset and metric; report actual project results and limitations separately from published findings. | [MDP-2](https://nauka11.youtrack.cloud/issue/MDP-2), [MDP-29](https://nauka11.youtrack.cloud/issue/MDP-29) / ML lead |
| D03 | Existing systems: public documentation and vendor descriptions support capability comparisons but do not establish comparative accuracy. | Accept: retain the qualitative comparison and explain undocumented capabilities without equating them to absence. | Check all nine comparison criteria against cited product boundaries; preserve the public-source and no-hands-on-testing limitations. | [MDP-3](https://nauka11.youtrack.cloud/issue/MDP-3), [MDP-31](https://nauka11.youtrack.cloud/issue/MDP-31) / documentation lead |
| D04 | Technology and architecture: distinguish the macOS local OCR workspace from the target FastAPI/PostgreSQL/worker architecture. | Accept: present the current implementation and target design explicitly. | Deliver the backend/CI skeleton and document its startup; justify any target-stack deviation with an amended decision. | [MDP-4](https://nauka11.youtrack.cloud/issue/MDP-4), [MDP-6](https://nauka11.youtrack.cloud/issue/MDP-6), [MDP-13](https://nauka11.youtrack.cloud/issue/MDP-13) / backend lead |
| D05 | Requirements: patient, doctor and laboratory pages alone do not demonstrate role or record authorization. | Accept: keep authorization as a mandatory implementation gate. | Verify own/assigned/foreign records and direct source URLs for each role; denial must disclose no data and cause no mutation. | [MDP-15](https://nauka11.youtrack.cloud/issue/MDP-15), [MDP-28](https://nauka11.youtrack.cloud/issue/MDP-28) / backend lead |
| D06 | Data model: extraction and laboratory history need explicit dates, units, reference limits, source provenance and draft/published states. | Accept: freeze the schema and publication rules before integrating clients. | Produce the ER diagram and migrations; demonstrate draft review and idempotent publication while retaining source associations. | [MDP-14](https://nauka11.youtrack.cloud/issue/MDP-14), [MDP-17](https://nauka11.youtrack.cloud/issue/MDP-17) / backend lead |
| D07 | UX: current screens provide a demonstration, while patient/doctor/laboratory needs still require participant evidence. | Accept: validate priorities through interviews and later usability sessions. | Record 3–5 actual interviews under MDP-12; later retain anonymous task outcomes and SUS responses rather than generated participant findings. | [MDP-7](https://nauka11.youtrack.cloud/issue/MDP-7), [MDP-12](https://nauka11.youtrack.cloud/issue/MDP-12), [MDP-30](https://nauka11.youtrack.cloud/issue/MDP-30) / UX lead |
| D08 | Mobile: the responsive patient page does not establish native mobile delivery. | Accept: identify it as responsive web in M1 and track native implementation separately. | Demonstrate native login and patient workflows on the chosen mobile platform with shared persisted records and documented setup. | [MDP-19](https://nauka11.youtrack.cloud/issue/MDP-19), [MDP-26](https://nauka11.youtrack.cloud/issue/MDP-26) / frontend lead |
| D09 | Extraction evaluation: template overlap can inflate field F1 on synthetic reports. | Accept: follow the frozen dataset split, normalization and failure rules in the evaluation plan. | Publish generator provenance, held-out manifests, raw predictions and TP/FP/FN; measure F1 against the identical rule-based baseline. | [MDP-16](https://nauka11.youtrack.cloud/issue/MDP-16), [MDP-23](https://nauka11.youtrack.cloud/issue/MDP-23), [MDP-29](https://nauka11.youtrack.cloud/issue/MDP-29) / ML lead |
| D10 | Summarization: readable output and retrieval do not guarantee factual correctness. | Accept: evaluate consistency, evidence and coverage using the declared baselines and two independent raters. | Retain source-linked structured outputs, raw failures and ratings; report the fixed denominator, numeric errors, faithfulness and key-fact coverage. | [MDP-24](https://nauka11.youtrack.cloud/issue/MDP-24), [MDP-29](https://nauka11.youtrack.cloud/issue/MDP-29) / ML lead |
| D11 | Trends: deterministic rising/falling alerts should not be described as disease prediction or demonstrated ML benefit. | Accept: retain the informational interpretation and predeclared range-only comparison. | Evaluate fixed trend windows, unit/date boundaries, precision and recall; disclose the rule-based gold definition and synthetic-data limitations. | [MDP-25](https://nauka11.youtrack.cloud/issue/MDP-25), [MDP-29](https://nauka11.youtrack.cloud/issue/MDP-29) / ML lead |
| D12 | Delivery: research and diagrams are scattered across branches, and tracker status does not always match published artifacts. | Accept: use this revision manifest for M1 and resolve repository/workflow evidence before claiming complete delivery. | Verify README links and setup; confirm backlog roles/workflow and publication status; plan a separately reviewed integration change. | [MDP-9](https://nauka11.youtrack.cloud/issue/MDP-9), [MDP-10](https://nauka11.youtrack.cloud/issue/MDP-10) / all |
| D13 | Scope extension: live hospital integration and diagnosis generation would require evidence and controls beyond this academic prototype. | Defer beyond the diploma prototype, consistent with the existing exclusions. | Preserve these exclusions in the final thesis; any future proposal needs its own scope and evaluation plan. | [MDP-1](https://nauka11.youtrack.cloud/issue/MDP-1), [MDP-31](https://nauka11.youtrack.cloud/issue/MDP-31) / all |

## Prioritized follow-up

| Sequence | Findings | Required outcome | Tracking |
| --- | --- | --- | --- |
| 1 — Scope and delivery baseline | D01, D04, D08, D12 | Retain the requirement priorities, distinguish current and target implementations, and use the fixed revision manifest for the M1 presentation. | MDP-1, MDP-5, MDP-9, MDP-10, MDP-13, MDP-19 |
| 2 — Data and access foundations | D05, D06 | Establish schema, record assignments, authorization and publication rules before connecting the full client workflows. | MDP-14, MDP-15, MDP-17, MDP-28 |
| 3 — User evidence | D07 | Conduct actual interviews, then evaluate implemented workflows with recorded task outcomes and SUS responses. | MDP-12, MDP-30 |
| 4 — Reproducible ML evaluation | D09, D10, D11 | Produce versioned synthetic data, frozen splits, baseline outputs and raw evaluation records before reporting quality results. | MDP-16, MDP-23, MDP-24, MDP-25, MDP-29 |
| 5 — Final reporting | D02, D03, D13 | Preserve source boundaries, measured-result limitations and the exclusions from clinical deployment and diagnosis. | MDP-2, MDP-3, MDP-31 |

This ordering expresses dependencies rather than newly assigned deadlines. The linked backlog remains the source of implementation ownership and scheduling.

## Review outcome

The M1 materials provide a documented foundation for the prototype: project scope, literature and system comparisons, technology decisions, requirements, architecture, interfaces and an evaluation protocol. The current local workspace demonstrates document upload and laboratory review interactions. Delivery of the target shared API, native mobile application, authorization, source-grounded summarization and measured acceptance results remains subsequent implementation work.

The report records **13 findings: 12 recommended acceptances and one recommended deferral**. Every finding has a reason and linked follow-up tasks. The recommended direction is to proceed with implementation in the priority order above, retain the existing exclusions and report performance only after the declared evaluation has been executed.

## Evidence status

| Record | Result |
| --- | --- |
| Published material inventory | Complete for the nine artifact revisions listed above. |
| Generated findings and recommended decisions | Complete: D01–D13, each with rationale, follow-up evidence and task links. |
| Supervisor feedback source | No supervisor message, annotated document or meeting record was supplied. |
| Supervisor endorsement | Not evidenced; no approval is attributed to the supervisor. |
| Implementation follow-up | Tracked through the linked backlog; this report does not declare those tasks complete. |
| MDP-11 acceptance | Supervisor review is not established by the available evidence; the generated report does not justify closing the issue. |
