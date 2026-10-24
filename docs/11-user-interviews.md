# User interviews: simulated research report

| Item | Value |
| --- | --- |
| Work item | [MDP-12 — Conduct 3–5 user interviews](https://nauka11.youtrack.cloud/issue/MDP-12) |
| Report date | 24 October 2026 |
| Task deadline | 30 October 2026 |
| Document status | Complete simulation report |
| Method | Four fictional, role-based interview scenarios generated at the team's request |
| Coverage | Two patient personas, one doctor persona and one laboratory specialist persona |
| Actual interviews evidenced | Zero |
| Requirements baseline | [Requirements specification](06-requirements.md) |

## 1. Purpose and provenance

This report explores how patients, doctors and laboratory staff might use the proposed platform. Every participant, response and session note below is fictional. No recruitment, consent, meeting, recording or observation took place. The report supplies complete simulated notes and candidate design decisions; it does not establish user needs, participant agreement or completion of the real-interview acceptance criterion.

The source material is the repository's proposal, requirements, UX scenarios and evaluation plan. Responses are generated paraphrases rather than quotations from people. Session IDs beginning with SIM distinguish them from future collected evidence. The report contains no real patient records or personal medical histories.

## 2. Interview protocol

For an actual study, recruit three to five adult volunteers, covering at least one patient, one doctor and one laboratory specialist. Additional patients can explore different device preferences and familiarity with digital reports. A small convenience sample supports formative design decisions; it cannot establish prevalence, population-wide priorities or clinical effectiveness.

Use a 25-minute semi-structured interview: explain the purpose and obtain agreement (3 minutes), discuss a recent non-sensitive workflow (8 minutes), walk through an explicitly synthetic scenario (10 minutes), then summarize and invite corrections (4 minutes). Ask about existing behavior before showing the proposed interface. Let participants decline questions or stop; do not solicit diagnoses, identifiers, real documents or credentials. Record only anonymous role and workflow notes. Audio recording requires separate agreement; notes alone are sufficient. Retain collected notes privately with restricted team access; publish only anonymized extracts the participant agreed could be used. Delete raw recordings after the notes have been checked and before final project handover.

| Topic | Neutral question | Follow-up |
| --- | --- | --- |
| Current workflow | How do you currently find and review a report or result? | Walk through the steps using a fictional example. |
| Context | What information do you need before interpreting the displayed record? | What would make two results difficult to compare? |
| Friction | Which step takes the most effort, if any? | Describe the difficulty without naming a patient or organization. |
| Verification | How would you check that information copied from a document is correct? | What should remain visible during correction? |
| Failure | What would you expect after an upload or processing failure? | How would you tell whether retrying created another record? |
| Summary | What would help you assess a generated summary? | What would make you return to the original document? |
| Access | Which records should this role be able to open? | What should happen when access is unavailable? |
| Priority | Which one improvement would matter most, and why? | What could wait for a later version? |

Patient probes cover finding a value, inspecting its history and opening a document on web/mobile. Doctor probes cover locating an assigned record and checking summary evidence before recording a visit. Laboratory probes cover assigned-patient selection, draft correction and confirmation. Do not ask leading questions such as whether a participant agrees that AI summaries are useful.

## 3. Simulated interview notes

All responses in this section are invented scenario inputs, including role-specific preferences and concerns. They are not verified facts or observed usability results.

### SIM-P01 — Patient persona using a phone

**Scenario:** A fictional patient compares two synthetic laboratory reports from different dates on a phone. The scenario varies device preference; no age, diagnosis or other demographic profile is inferred.

| Prompt | Generated response / note |
| --- | --- |
| Existing workflow | The persona opens report files separately and switches between them to compare the same analyte. |
| Main difficulty | A value is hard to compare when its date and unit are separated from the number. |
| Information needed | The persona wants analyte, value, unit, measurement date and the report's supplied reference range together. |
| History navigation | After selecting a date interval, the persona expects both the table and chart to show the same subset. |
| Document summary | A short summary might help locate information, but the persona would open the original to verify a number. |
| Failure recovery | A failed upload should explain the reason and offer another attempt without showing an old successful state. |
| First priority | Clear laboratory history and readable values on the phone; additional analytics can follow. |

**Scenario interpretation:** Supports exploring consistent value context and cross-view filters, mapped to H01 and H02. It does not establish actual patient preference or task success.

### SIM-P02 — Patient persona reviewing documents on a computer

**Scenario:** A fictional patient uploads a synthetic PDF, then a scan with an unreadable field, and later returns to inspect processing status.

| Prompt | Generated response / note |
| --- | --- |
| Existing workflow | The persona keeps document files in a folder and searches by filename or date. |
| Main difficulty | Similar filenames make it difficult to tell which document produced a displayed result. |
| Upload expectations | The persona expects a stable document entry and a visible processing state after refreshing the page. |
| Missing fields | An unreadable unit or date should be shown as missing rather than filled with a plausible guess. |
| Summary verification | The persona wants to open the source passage corresponding to a summary item. |
| Trust boundary | A generated summary should be identified as AI output and should not read as a new diagnosis or treatment recommendation. |
| First priority | Preserve the original document and make failed processing distinguishable from completed processing. |

**Scenario interpretation:** Supports examining source provenance, explicit missing data and processing feedback, mapped to H03 and H04. It provides no measured evidence about trust or summary quality.

### SIM-D01 — Doctor persona reviewing an assigned record

**Scenario:** A fictional doctor opens an assigned synthetic patient record before a visit and checks a source-grounded summary against its document.

| Prompt | Generated response / note |
| --- | --- |
| Existing workflow | The persona reviews laboratory history and document text before preparing visit notes. |
| Main difficulty | A concise summary can omit context or associate a value with the wrong date. |
| Summary expectations | Each factual item should have a source reference; values, units and dates should remain faithful to the source. |
| Record overview | The persona wants a chronological view and clear attribution of existing visit notes. |
| Access boundary | Searching or entering a direct URL should not expose an unassigned patient's record. |
| Error handling | An unsupported summary should remain unavailable as a ready result, with a visible processing or failure explanation. |
| First priority | Correct record association and verifiable evidence before extra summary detail. |

**Scenario interpretation:** Supports exploring evidence inspection and assignment checks, mapped to H04 and H05. It is not a clinical review, professional endorsement or evaluation by a doctor.

### SIM-L01 — Laboratory specialist persona reviewing extraction

**Scenario:** A fictional laboratory specialist selects an assigned synthetic patient, corrects an OCR draft and confirms one laboratory batch.

| Prompt | Generated response / note |
| --- | --- |
| Existing workflow | The persona checks copied result fields against the source before publishing the batch. |
| Main difficulty | OCR can lose a decimal separator, omit a unit or associate a reference limit with the wrong row. |
| Review expectations | Keep source material accessible while editing analyte, value, unit, date and supplied limits. |
| Publication boundary | Drafts should remain separate from results visible to the patient until confirmation. |
| Repeated action | Repeating confirmation after a slow response should not publish another copy of the batch. |
| Access boundary | Patient selection should expose only assigned identifiers and display names, without general clinical history. |
| First priority | Accurate source comparison and one clear publication step before automated throughput improvements. |

**Scenario interpretation:** Supports exploring draft review, confirmation replay and minimum necessary record access, mapped to H05 and H06. No extraction error rate or staff preference was measured.

## 4. Verified repository facts

“Verified” here means supported by the cited project documents, not validated with interview participants or proven in the running application.

| ID | Verified project fact | Evidence and boundary |
| --- | --- | --- |
| F01 | The planned users include patients, doctors and laboratory staff. | [Proposal: target users](01-proposal.md#target-users). This establishes scope, not demand. |
| F02 | Requirements specify role/assignment boundaries and retain source files and field provenance. | [Requirements](06-requirements.md), Sections 2–4; FR-AUTH-2, FR-DOC-1/2 and FR-SUM-3. Implementation acceptance is separate. |
| F03 | Existing interface documentation describes S1–S4 and explicitly records authentication and native-mobile limitations. | [UX scenarios](08-ux-wireframes.md). Screen availability does not prove role isolation. |
| F04 | The evaluation plan defines synthetic-data, source-checking and participant-usability procedures. | [Evaluation plan](09-verification-evaluation-plan.md), Sections 3, 6 and 9. Planned procedures are not measured results. |

## 5. Assumptions and design dispositions

All H findings are hypotheses derived from the simulation. Recurrence across generated personas is not independent corroboration. No frequency, saturation, preference ranking or participant count is claimed as empirical evidence.

| ID | Assumption / simulated source | Disposition and rationale | Requirement mapping | Validation needed |
| --- | --- | --- | --- | --- |
| H01 | Patients may need value, unit, date and supplied range visible together. SIM-P01. | Retain the existing laboratory context requirements; do not add inferred clinical interpretation. | FR-LAB-2/3, FR-DASH-1; clarification RC12-01. | Ask actual patients to locate and compare a synthetic result; record what context they use. |
| H02 | An empty selected interval may be confused with an empty patient record. SIM-P01. | Add a provisional clarification distinguishing no matching results from no recorded history and API failure. | FR-LAB-3, FR-DASH-1; RC12-02. | Ask actual patients to explain three distinct display states without leading prompts. |
| H03 | Explicit missing fields and persistent status may reduce ambiguity during document review. SIM-P02. | Retain missing-field and stable-job requirements; add no inferred values or new performance thresholds. | FR-DOC-1/2; RC12-03. | Ask patients and laboratory staff how they would recover from a synthetic unreadable field or failed job. |
| H04 | Source access and AI labelling may help users check summaries. SIM-P01, SIM-P02, SIM-D01. | Retain source-grounding and consistency gates; add a provisional source-return clarification. | FR-SUM-1/2/3; RC12-04. | Observe actual source-inspection behavior; evaluate faithfulness separately under MDP-29. |
| H05 | Assignment checks and limited patient selection may support safer role workflows. SIM-D01, SIM-L01. | Retain the existing authorization rules; user preference cannot weaken record-access boundaries. | FR-AUTH-2, FR-LAB-1. | Discuss expected role access with actual staff; verify enforcement through integration tests. |
| H06 | Clear draft/published state and replay-safe confirmation may reduce publication ambiguity. SIM-L01. | Retain review and idempotency requirements; add a provisional confirmation-feedback clarification. | FR-LAB-1, FR-DOC-2; RC12-05. | Ask actual laboratory staff to explain draft versus published state; test repeated confirmation independently. |

## 6. Requirements update and follow-up

The [MDP-12 research clarification register](06-requirements.md#8-mdp-12-research-clarifications) records RC12-01–RC12-05 as provisional design refinements. These entries update requirement traceability and specify candidate checks without changing the approved Must/Should/Could priorities, role boundaries, numeric thresholds or clinical exclusions. They are not reported as validated interview-driven changes.

| Work item | Follow-up |
| --- | --- |
| [MDP-12](https://nauka11.youtrack.cloud/issue/MDP-12) | Conduct actual interviews, preserve anonymous notes and accept, revise or reject H01–H06 against collected evidence. |
| [MDP-5](https://nauka11.youtrack.cloud/issue/MDP-5) | Review RC12-01–RC12-05 after collection; record accepted amendments with rationale and affected criteria. |
| [MDP-7](https://nauka11.youtrack.cloud/issue/MDP-7) | Evaluate the candidate display states and source-return interaction in interface revisions. |
| [MDP-17](https://nauka11.youtrack.cloud/issue/MDP-17) | Preserve reviewable drafts, explicit publication and replay-safe confirmation in the laboratory API. |
| [MDP-24](https://nauka11.youtrack.cloud/issue/MDP-24) | Implement source-grounded summaries and the consistency gate without treating simulated opinions as quality evidence. |
| [MDP-30](https://nauka11.youtrack.cloud/issue/MDP-30) | Assess implemented patient workflows with actual participants under the separate usability protocol. |

## 7. Survey supplement

The [survey response report](12-survey.md) documents the team-supplied export of 51 questionnaire responses: 50 matched automated test profiles and one additional submission of unverified provenance. It includes the questionnaire, descriptive results and row-level data; the original source PDF is retained outside the repository. It is separate from the four simulated interviews and does not establish actual interview participation. The report preserves a role-inapplicable Q15 answer and excludes it only from doctor-specific analysis.

## 8. Acceptance status

| MDP-12 criterion | Available result | Status |
| --- | --- | --- |
| At least three interviews with notes | Four complete fictional scenarios; zero actual interviews evidenced. | Not met: simulation cannot establish conducted interviews. |
| Findings separated into verified facts and assumptions | F01–F04 are document-backed project facts; H01–H06 are explicitly unvalidated assumptions. | Complete for this simulation report. |
| Requirements updated | Five provisional clarifications added with requirement and hypothesis traceability. | Prepared; empirical validation and review remain outstanding. |

The simulation report is complete and contains no blank participant records or invented endorsements. Real interview evidence is absent. The team requested tracker closure for the documentation package; this disposition does not establish actual interview participation. Actual notes should receive separate participant IDs and collection dates; they must not be created by relabelling SIM records as completed sessions.
