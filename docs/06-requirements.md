# Requirements specification and acceptance criteria

| Item | Value |
| --- | --- |
| Project | Intelligent Medical Platform |
| Team | Yerkin Yerassyl; Nauryzbay Nurkassymov; Asylzhan Bakytzhan |
| Work item | [MDP-5 — Requirements specification with acceptance criteria](https://nauka11.youtrack.cloud/issue/MDP-5) |
| Milestone | M1 pre-defense-1; 24 October 2026 |
| Document date | 24 October 2026 |
| Baseline | [Project proposal and scope](01-proposal.md), MDP-1 |

This specification defines the functional requirements (FR), non-functional requirements (NFR), priorities and acceptance criteria for the completed diploma prototype. M1 delivers the specification; application implementation and measured results follow in later milestones. A requirement listed here is an acceptance obligation, not a claim that its implementation has passed.

## 1. Scope and prioritization

The system combines patient records, laboratory results, document processing and a dashboard through a shared API, a web application and a mobile application. Development, demonstration and evaluation use synthetic records. It presents recorded information and source-grounded summaries without generating medical diagnoses or treatment advice.

| Priority | Meaning for this project |
| --- | --- |
| Must | Required for acceptance of the final prototype. Every criterion must pass with recorded evidence. |
| Should | Planned after the mandatory workflows; omission requires a documented reason and impact. |
| Could | Optional enhancement after Must and Should work, subject to available time. |
| Won't | Excluded from this diploma release; no implementation is required. |

The source package's requirement IDs are retained for traceability. Compared with its initial list, FR-SUM-3 is split: the AI label and source links are Must because MDP-1 requires them, while error reporting remains Should as FR-SUM-4. FR-ADM-1 is Must to support the account-management boundary defined below. Audit completeness is specified separately as NFR-AUD-1. These priorities define this requirements baseline; user-research findings under MDP-12 may lead to a recorded revision.

The 10 MiB upload limit, 20-page PDF limit, 120-second processing timeout, assignment rules and detailed benchmark workloads are specification decisions introduced here to make acceptance repeatable. They are not reported as existing implementation settings or interview findings. Review them together with the architecture and evaluation plan before implementation.

## 2. Actors and access boundaries

Authorization applies in the API and file-delivery layer, independently of which controls a client displays. Access to a patient record includes its dashboard, laboratory values, visits, prescriptions, documents, summaries, source passages and processing status. Direct requests with another record's identifier must obey the same rules as lists and searches.

| Actor | Permitted operations | Boundary |
| --- | --- | --- |
| Patient | Read own profile, visits, prescriptions, labs and dashboard; upload own documents; read own summaries and sources. | No access to another patient's data; cannot grant clinical roles, publish lab results, or edit clinician-authored records. |
| Doctor | Read assigned patients' clinical records; upload their documents; add their visit notes and prescriptions. | Requires an active doctor-to-patient assignment for every operation. |
| Laboratory staff | Submit, review and publish lab results for patients with an active laboratory assignment; read the submitted batch and its processing result. | Patient selection exposes only assigned patient identifiers and display names; no access to full history, visit notes, prescriptions or general summaries. |
| Administrator | Manage accounts, roles and patient assignments; inspect audit metadata. | Administrative authority alone does not permit reading clinical content or downloading documents. |
| Unauthenticated user | Register a patient account and submit a login request. | No patient records, documents, processing results or audit entries are accessible. |

An assignment is an explicit active association managed by an administrator. Removing an assignment takes effect on the next API request, including requests using an existing login session. Public registration always creates a Patient account; Doctor, Laboratory staff and Administrator roles require an administrator operation. Demo accounts and assignments may be seeded reproducibly, but the same authorization rules apply to them.

## 3. Shared data and verification conventions

- Each patient, document, laboratory result and processing job has a stable identifier. Relationships between them are preserved when data is retrieved.
- A published numeric laboratory result contains patient ID, analyte identifier and display name, numeric value, unit, measurement date and origin (manual entry or document ID). Supplied reference limits are optional; absence is recorded explicitly.
- Dates are stored unambiguously and displayed with their date or time-zone context. For a date-only laboratory report, retain the calendar date without inventing a time. Results sort by measurement date, then stable result ID for ties.
- An analyte series groups one analyte identifier and one unit. Different units form separate series unless an explicitly tested conversion exists. The mandatory workflow needs no automatic unit conversion.
- Extracted values remain a reviewable draft until authorized laboratory staff confirm publication. A document summary is separate from a confirmed laboratory record.
- Acceptance uses synthetic fixtures with expected outputs fixed before execution. Each test records the requirement ID, fixture/version, environment, actual result and pass/fail evidence. No interview finding or measured score is assumed in this specification.

## 4. Functional requirements

### FR-AUTH-1 — Registration, login and logout

**Priority:** Must. **Verification:** API integration and client scenario tests.

The system shall support patient registration, email/password login and session logout.

**Acceptance criteria:** A new valid email/password creates a Patient account; duplicate email and malformed input create no second account. Valid credentials create an authenticated session; invalid credentials return no session. A registration request containing a privileged role cannot create that role. An unauthenticated, expired or logged-out session cannot access a protected resource, including when its previous credentials are replayed.

### FR-AUTH-2 — Role and record authorization

**Priority:** Must. **Verification:** API and document-download authorization matrix.

The system shall enforce the actor matrix in Section 2 for reads and mutations.

**Acceptance criteria:** Test every protected operation with all four roles and no session, using own/assigned and foreign/unassigned records. Every forbidden request returns 401, 403 or a non-disclosing 404, exposes no clinical payload or file, and creates no clinical mutation. Lists and searches omit unauthorized records. After an assignment is removed, the next request is denied. Test nested document, summary and job identifiers independently of their parent URL.

### FR-PAT-1 — Patient record and history

**Priority:** Must. **Verification:** API integration and seeded-record comparison.

The system shall expose a patient profile with basic demographics, visits and recorded prescriptions to the patient and assigned doctors.

**Acceptance criteria:** For fixtures with known demographics, visits and prescriptions, returned and displayed fields match the stored record, and lists are ordered by their recorded date. An empty history shows an explicit empty state. A patient cannot edit clinician-authored visits or prescriptions through either client or a direct API request.

### FR-PAT-2 — Doctor-authored visits and prescriptions

**Priority:** Should. **Verification:** Doctor workflow and authorization tests.

The system shall allow an assigned doctor to add a visit note and a prescription record containing patient, author, date and entered content.

**Acceptance criteria:** After successful creation, both records appear on the patient's refreshed timeline within five seconds on the documented local test environment. Author and patient association match the session and selected record. Empty required fields and unassigned-patient requests are rejected without creating records. Recording a prescription stores the doctor's input; it does not generate treatment recommendations.

### FR-LAB-1 — Laboratory result submission and publication

**Priority:** Must. **Verification:** Submission, validation and publication integration tests.

Laboratory staff shall submit results through a structured form or file and explicitly confirm publication for an assigned patient. Structured entry provides the mandatory path even when extraction fails.

**Acceptance criteria:** A valid structured batch remains a draft until confirmed; after confirmation its values appear in that patient's history with units, dates and origin. Missing patient, analyte, numeric value, unit or date, non-finite values, and inverted reference limits prevent publication with field-specific errors. File extraction drafts are editable before confirmation. Confirmation uses one stable batch ID: replaying the same confirmation creates no duplicate results. Rejected and unconfirmed batches do not appear in patient charts.

### FR-LAB-2 — Reference-range flags

**Priority:** Must. **Verification:** Boundary-value tests and display checks.

The system shall classify values using only the compatible reference limits supplied with that result.

**Acceptance criteria:** For a two-sided interval, values below the lower limit are Low, values above the upper limit are High, and both boundaries and interior values are Within range. With one supplied limit, only crossing that limit is flagged; otherwise show No violation of supplied limit, without claiming a complete normal range. With no compatible range, show Not assessed. All fixed boundary fixtures pass, including negative and decimal values. A flag displays its source limits and unit and does not present a diagnosis.

### FR-LAB-3 — Laboratory history and charts

**Priority:** Must. **Verification:** API/UI comparison against a fixed series.

Patients and assigned doctors shall select an analyte, unit and inclusive date interval to view its history and chart.

**Acceptance criteria:** The table and chart represent every published result in the selected series and interval, in chronological order, with matching values, units and dates. Different-unit results are not joined into one series. Range indicators use the limits attached to each result. Zero results show an empty state; a single result shows one point; equal-date measurements remain distinguishable. Access follows FR-AUTH-2.

### FR-LAB-4 — Trend alerts

**Priority:** Should. **Verification:** Labelled time-series tests and baseline comparison.

The system shall identify strictly rising or falling sequences of at least three results for the same analyte/unit and expose an informational alert.

**Acceptance criteria:** Three distinct measurement dates with increasing values produce Rising; decreasing values produce Falling. Flat, mixed-direction, fewer-than-three and incompatible-unit fixtures do not produce these alerts. The alert links to the contributing measurements and never supplies a diagnosis. Evaluation reports precision and recall against reference-range-only flags; the allowed precision loss is fixed in MDP-8 before evaluation.

### FR-DOC-1 — Upload and asynchronous processing

**Priority:** Must. **Verification:** Upload, worker-failure and client-state tests.

Patients and assigned doctors shall upload PDF, JPG or PNG documents and observe processing status; laboratory staff may upload lab reports within FR-LAB-1.

**Acceptance criteria:** Accept supported, content-validated files up to 10 MiB; accept PDFs up to 20 pages. Unsupported, oversized, corrupt or encrypted/unreadable files return an actionable error without a published record. Valid uploads return a document/job ID without waiting for ML completion, retain the original and move through uploaded, processing and ready or failed. A forced OCR/model failure ends in failed with a readable reason and no ready summary. Jobs exceeding 120 seconds of processing are failed; workers do not publish late outputs for a failed job. Refreshing either client preserves the server status. Downloads and job polling obey FR-AUTH-2.

### FR-DOC-2 — OCR and structured extraction

**Priority:** Should. **Verification:** Fixed document fixtures and extraction evaluation.

The pipeline shall extract text from digital PDFs, apply OCR to supported scans and produce draft laboratory fields linked to their source page or text span.

**Acceptance criteria:** Digital-text and scanned synthetic fixtures both produce inspectable text and draft fields, or an explicit failed result when unreadable. Missing fields remain marked missing rather than guessed. Users can compare a proposed value with its source before confirmation under FR-LAB-1. Extraction quality is evaluated under NFR-ACC-1. Original files and extracted text remain available for source inspection by authorized patients and doctors even when no lab fields are extracted.

### FR-SUM-1 — Structured, source-grounded summary

**Priority:** Must. **Verification:** Schema validation, missing-field and retrieval-isolation tests.

The system shall generate a structured summary from a readable document, using only that document and explicitly authorized patient context retrieved for the job.

**Acceptance criteria:** Each ready summary validates against a versioned schema with document ID, AI label, model/version, source references, key findings, medications, and source-recorded diagnoses and recommendations. Categories absent from the source are empty, with no invented diagnosis or advice. Each factual item identifies a document/page or extracted-text span. A fixture with another patient's retrievable text never includes that text in retrieval context or output. An unreadable source fails processing instead of producing an ungrounded ready summary.

### FR-SUM-2 — Factual consistency gate

**Priority:** Must. **Verification:** Seeded-error checker tests and held-out summary evaluation.

Before publication, the system shall check summary numbers, units, medication names and dates against their cited source passages.

**Acceptance criteria:** Fixtures containing an altered value, unit, medication or date are blocked from ready publication and marked failed with a consistency reason. The checker compares associated facts, not merely the presence of the same token elsewhere in the document. Supported normalization rules are documented and tested. Source-consistent fixtures pass; all held-out published summaries meet NFR-ACC-2. Checker success alone is not treated as proof of clinical correctness.

### FR-SUM-3 — AI label and source inspection

**Priority:** Must. **Verification:** Web/mobile navigation and source-access checks.

Every displayed summary shall be labelled AI-generated and provide direct access to the evidence for each factual item.

**Acceptance criteria:** Both patient clients and the doctor web view display the AI-generated label and a prompt to verify the source. Selecting a cited item opens its authorized source page or extracted-text passage. A missing or invalid citation blocks that item from ready publication. The original document remains accessible to the same authorized patient or doctor. Laboratory staff do not receive general-summary access through source links.

### FR-SUM-4 — Summary error reports

**Priority:** Should. **Verification:** Report submission and persistence tests.

Authorized patients and doctors shall report an error in a summary.

**Acceptance criteria:** A submitted report stores the summary/version ID, reporter ID, timestamp and entered description. After refresh it remains associated with that version. Reporting does not silently change the source or summary; reports on unauthorized documents are rejected.

### FR-DASH-1 — Patient health dashboard

**Priority:** Must. **Verification:** Ten-patient fixture comparison and client scenarios.

The dashboard shall show latest published lab values per analyte/unit, reference flags, available trend alerts, recent visits, prescriptions and documents with their processing status.

**Acceptance criteria:** For ten synthetic patients, every displayed item matches the expected patient record and its source link, and latest values follow the ordering convention in Section 3. Missing categories have explicit empty states. An API error shows a retryable error rather than a misleading empty or successful state. No unconfirmed lab draft or failed summary appears as a published result. Trend-alert absence does not block the dashboard when FR-LAB-4 is deferred.

### FR-DASH-2 — Doctor patient overview

**Priority:** Should. **Verification:** Doctor scenario and assignment-revocation tests.

An assigned doctor shall open a patient overview with timeline, laboratory charts and document summaries.

**Acceptance criteria:** The overview contains only the selected assigned patient's data, orders timeline entries by date, and links to the corresponding charts, sources and summaries. An unassigned patient is absent from the list and inaccessible directly. Revoking assignment prevents subsequent overview and source requests.

### FR-UI-1 — Web and mobile patient workflows

**Priority:** Must. **Verification:** End-to-end scenario evidence for both clients.

The web and mobile clients shall use the shared API for patient login, dashboard, laboratory history/chart, and document upload/summary/source inspection.

**Acceptance criteria:** Scenarios S1 and S2 in Section 6 complete on both clients using the same patient and persisted records. A published lab result and ready document created in one client are visible after refresh in the other. Loading, empty, failed-processing and authorization-error states are distinguishable. Patient screens remain operable at a 360-pixel viewport width without clipped primary controls. S3 and S4 are web workflows; their mobile versions are not required.

### FR-ADM-1 — Account and assignment management

**Priority:** Must. **Verification:** Administrator workflow and privilege-escalation tests.

Administrators shall manage account activation, roles, doctor/patient and laboratory/patient assignments, and inspect audit metadata.

**Acceptance criteria:** An administrator can provision each role, deactivate an account, create/remove assignments and list audit entries. Deactivation prevents the account's next authenticated request, including an existing session. Patients, doctors and laboratory staff cannot invoke these operations. An administrator without a clinical assignment cannot retrieve clinical records, summaries or files. Each management mutation is audited under NFR-AUD-1.

### FR-EXP-1 — Patient export

**Priority:** Could. **Verification:** Export content and access checks.

Patients may export selected sections of their own record as PDF.

**Acceptance criteria:** The export contains only the requested own-record sections with dates, units, AI labels and source identifiers preserved where applicable. Another patient's identifiers are rejected and no export is returned.

## 5. Non-functional requirements

| ID | Priority | Requirement and measurable acceptance criteria | Verification |
| --- | --- | --- | --- |
| NFR-SEC-1 | Must | Store passwords with a salted adaptive password hash; inspect seeded storage to confirm that no plaintext or reversible password is present and equal passwords have different stored hashes. Keep real credentials out of tracked files and history; the recorded secret scan has no confirmed credential findings. All browser/mobile and cross-host service connections use TLS; packet/configuration checks show no plaintext credentials or patient payload on a non-loopback connection. Loopback-only local development may use HTTP and must be documented. | Authentication integration tests, hash inspection, repository secret scan, deployment configuration and transport checks. |
| NFR-PRIV-1 | Must | Use only documented synthetic patient fixtures for development, demonstrations, interviews and evaluation. Every fixture set has a generator/template and provenance manifest; the review finds no real patient records in tracked files, history or demonstration storage. Do not log passwords, tokens, document bodies or summary bodies. A canary credential/body test confirms these strings are absent from application logs. Only the minimum authorized synthetic context is sent to a configured model provider. | Fixture/provenance review, repository review, log-canary and captured model-request checks. |
| NFR-AUD-1 | Must | Every authorized patient-data read/write, document download, denied protected request and administrative mutation produces an audit event with actor or anonymous marker, timestamp, action, resource ID, outcome and correlation ID. Clinical bodies and credentials are excluded. If the audit sink is unavailable, protected operations fail without disclosing data or committing a mutation; a durable audit buffer may be used. Clinical roles cannot read, edit or delete audit events through the application; administrators have read-only audit access. | Exercise each operation category, verify its event, simulate audit failure and attempt audit read/edit/delete with each role. |
| NFR-ACC-2 | Must | On a fixed held-out set of at least 30 readable synthetic documents, ready summaries contain zero detected numeric inconsistencies and achieve mean human faithfulness of at least 4/5. At least two raters independently assess every document; average their ratings per document, then average over documents. Record rubric, raw ratings, disagreement and comparisons with an extractive baseline and the same LLM without retrieval. Every eligible document must receive a ready summary; failed jobs cannot be silently removed from the denominator. | Checker output, schema/source checks, blinded human evaluation and versioned results. |
| NFR-AVL-1 | Must | A clean checkout starts the database, shared API, workers and web client using documented Docker Compose commands and example configuration; mobile setup is documented separately. Seeded login and patient workflows run using the documented model configuration. A restart retains published labs, source files and ready summaries; an interrupted job becomes ready or explicitly failed after recovery, never indefinitely processing. Required external model access is documented; mocks do not count as final ML acceptance evidence. | Clean-environment setup and service-restart scenario with persisted-record comparison. |
| NFR-PERF-1 | Should | Dashboard API p95 latency is below two seconds with 200 synthetic patients, each with 100 lab results, ten visits, ten prescription records and ten document metadata records. Measure at least 1,000 requests after 100 warm-up requests with ten concurrent authenticated clients; report errors separately and require zero unexpected errors. | Repeatable local load run with hardware, versions, cache state and dataset seed recorded. |
| NFR-PERF-2 | Should | At least 95% of 20 fixed readable two-page synthetic reports complete extraction and summary within 60 seconds from accepted upload to ready, with one active job and a warm worker. Include digital PDFs and scans; report failed jobs and queue/model times rather than excluding them. | Timed processing benchmark recording hardware, file resolution, OCR/model versions and provider/network conditions. |
| NFR-ACC-1 | Should | Extracted analyte, value, unit, measurement date and supplied reference limits achieve micro-averaged field F1 of at least 0.85 and exceed the rule-based parser on the identical held-out reports. Predefine document set, gold fields, matching/normalization and missing-field rules; report precision, recall and per-field/template results. | Fixed-set extraction evaluation against a versioned rule-based baseline. |
| NFR-USE-1 | Should | At least five participants attempt patient scenarios S1 and S2 with synthetic records. Mean SUS is at least 70; unassisted task success is at least 80% of all assigned participant/scenario attempts. Fix task endpoints, time limits and scoring before sessions; report failed attempts and findings. | Anonymized session records, task outcomes and SUS calculation. |
| NFR-MAINT-1 | Should | Each pull request runs configured lint and automated tests. Required tests cover role/record authorization, lab-range boundaries, upload/job failures and summary schema/consistency gates; a deliberately failing check prevents a successful CI result. | CI configuration and successful/negative-control run evidence. |
| NFR-I18N-1 | Could | Provide English and Russian interface text, retaining the same values, dates and unit meaning when language changes; do not translate original source content silently. Kazakh localization is future work. | Language-switch scenarios and missing-translation review. |

MDP-8 will define executable procedures, fixture versions, the faithfulness rubric, normalization rules and trend-comparison tolerance before measurement. It must retain the thresholds above or record an explicitly reviewed change before experiments. These targets are not measured results. This specification makes no claim of legal certification or clinical effectiveness.

## 6. Scenario traceability and release gates

| Scenario | Actors and client | Steps and observable completion | Requirements |
| --- | --- | --- | --- |
| S1 — Review health status | Patient; web and mobile | Log in, open dashboard, select a flagged lab, inspect history, chart and supplied range. Displayed values match the fixture. Trend alerts are included when implemented. | FR-AUTH-1, FR-AUTH-2, FR-PAT-1, FR-DASH-1, FR-LAB-2, FR-LAB-3, FR-LAB-4, FR-UI-1 |
| S2 — Understand a document | Patient; web and mobile | Upload a synthetic report, observe processing, read its labelled structured summary and open cited evidence. Repeat with a corrupt file and forced worker failure to verify visible failure states. Error reporting is included when implemented. | FR-DOC-1, FR-SUM-1, FR-SUM-2, FR-SUM-3, FR-SUM-4, FR-UI-1 |
| S3 — Prepare for a visit | Assigned doctor; web | Open assigned record, inspect timeline, labs and summary; add a visit note and prescription. Verify denial for an unassigned patient. | FR-AUTH-2, FR-PAT-1, FR-PAT-2, FR-LAB-3, FR-SUM-3, FR-DASH-2 |
| S4 — Publish laboratory results | Laboratory staff; web | Select assigned patient, enter results or review extraction draft, correct fields and confirm once. Patient then sees the published values. Check duplicate confirmation and unauthorized patient selection. | FR-AUTH-2, FR-LAB-1, FR-LAB-2, FR-DOC-1, FR-DOC-2 |

All scenarios additionally obey NFR-SEC-1, NFR-PRIV-1 and NFR-AUD-1. S3 includes Should capabilities; S4 has a mandatory structured-entry path and a Should extraction path. These distinctions prevent optional features from obscuring acceptance of the required workflows.

The proposal outcomes map to requirements as follows:

| MDP-1 outcome | Acceptance coverage |
| --- | --- |
| Patient Health Dashboard | FR-PAT-1, FR-DASH-1, FR-LAB-2, FR-LAB-3, FR-UI-1; planned trends under FR-LAB-4. |
| Laboratory Results Management System | FR-LAB-1, FR-LAB-2, FR-LAB-3; extraction under FR-DOC-2. |
| Medical Document Summarization System | FR-DOC-1, FR-SUM-1, FR-SUM-2, FR-SUM-3, NFR-ACC-2. |
| Integrated web/mobile prototype | FR-AUTH-1, FR-AUTH-2, FR-ADM-1, FR-UI-1, NFR-SEC-1, NFR-PRIV-1, NFR-AUD-1, NFR-AVL-1. |
| Reproducible evaluation | NFR-ACC-1, NFR-ACC-2, NFR-PERF-1, NFR-PERF-2, NFR-USE-1; procedures and evidence under MDP-8. |

**MDP-5 document acceptance:** Functional and non-functional requirements have stable IDs and MoSCoW priorities; every Must includes observable inputs/conditions, expected results and a verification method. Role boundaries, failure cases and evaluation conditions are explicit and consistent with MDP-1. Document review does not mark any application requirement as implemented.

**Final prototype acceptance:** Every Must criterion passes and has evidence linked to its requirement ID. Record every unmet Should/Could requirement and its effect on the proposal's outcomes. A deferred Should does not erase an unmet project objective: the final report must describe incomplete extraction, analytics or other planned outcomes. Report measured baseline comparisons and limitations separately from functional pass/fail results.

## 7. Exclusions and change control

The following are Won't for this release: autonomous diagnosis or treatment recommendations; real patient data; production hospital/laboratory integration or full FHIR conformance; billing, appointment booking and telemedicine; medical-device certification or clinical-effectiveness claims; training a general-purpose medical language model from scratch. Full doctor and laboratory workflows on mobile and Kazakh localization are also deferred. Source-recorded diagnoses and prescriptions may be displayed as records, with attribution, without generating new clinical decisions.

Architecture (MDP-6), wireframes (MDP-7) and verification planning (MDP-8) should reference these requirement IDs. Any change to scope, priority, access rules, numeric targets or fixtures must record its rationale, affected requirements and reviewer decision in the relevant YouTrack task and repository review. Findings from MDP-12 inform revisions only after they have actually been collected.


## 8. MDP-12 research clarifications

Work item: [MDP-12](https://nauka11.youtrack.cloud/issue/MDP-12). Register date: 24 October 2026. Source: [simulated interview report](11-user-interviews.md), H01–H06. These are provisional design refinements generated from fictional scenarios, not collected interview findings or approved changes to the acceptance baseline. Existing requirement priorities, access boundaries, limits and quantitative targets remain authoritative. Candidate checks below become acceptance obligations only after a recorded review decision.

| ID | Existing requirements | Provisional clarification / candidate check | Basis and disposition |
| --- | --- | --- | --- |
| RC12-01 | FR-LAB-2, FR-LAB-3, FR-DASH-1 | Keep analyte, value, unit and measurement date available together in the result view. Show the supplied reference limits or explicit absence; do not infer limits. Check one synthetic result with a range and one without on web and mobile. | H01; restates existing data context, awaiting participant validation. |
| RC12-02 | FR-LAB-3, FR-DASH-1 | Distinguish no recorded history, no matching results in the selected date interval and a retrieval error. For a patient with results outside the interval, retain the active filter and allow changing it; do not present a retrieval error as empty history. Check all three states against fixed fixtures. | H02; candidate refinement of existing empty/error states. |
| RC12-03 | FR-DOC-1, FR-DOC-2 | In extraction review, display missing required fields explicitly and keep source access available. Refresh must retain the stable document/job association and terminal failure reason. Check a missing unit, missing date and failed job without substituting plausible values. | H03; retains existing missing-data and job-state rules. |
| RC12-04 | FR-SUM-3, FR-UI-1 | After opening a summary item's evidence, provide a way back to the same document's summary. The AI label and document identity remain unambiguous. Check source opening and return on both patient clients with the same synthetic record. | H04; candidate navigation clarification, with no implied summary-quality result. |
| RC12-05 | FR-LAB-1, FR-DOC-2 | After a successful batch confirmation, show the published state associated with the stable batch ID. Replaying confirmation must retain the same published records and avoid duplicate success entries. Check initial confirmation, refresh and replay using a single synthetic batch. | H06; candidate feedback clarification of existing publication/idempotency rules. |

Validation requires actual interview notes and a review decision for each accepted refinement. Record contradictory evidence as well as supportive evidence. A simulation cannot justify changing requirement priority, claiming user endorsement or marking an application criterion passed.
