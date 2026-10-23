# Project proposal and scope

## Project identity

| Item | Value |
| --- | --- |
| Project title | Designing an Intelligent Medical Platform for Structuring, Analyzing, and Visualizing Comprehensive Patient Data Based on Machine Learning Methods |
| Working name | Intelligent Medical Platform |
| Team | Yerkin Yerassyl; Nauryzbay Nurkassymov; Asylzhan Bakytzhan |
| Proposal contributor | Yerkin Yerassyl |
| Supervisor | Myrzakerimova Alua |
| Deliverable | A web application and a mobile application backed by one API and ML services |
| Repository | <https://github.com/nauka2103/med-data-platform> |
| Work item | [MDP-1 — Write project proposal and scope](https://nauka11.youtrack.cloud/issue/MDP-1) |
| Milestone and deadline | M1 pre-defense-1; 24 October 2026 |
| Document date | 23 October 2026 |
| Status | Final proposal; approved by the supervisor |

The Intelligent Medical Platform will bring patient records, laboratory results and medical documents into one system. Patients will be able to follow changes in their health indicators, while doctors will be able to review records and document summaries. The diploma project covers the design, implementation and evaluation of a prototype with web and mobile applications. The first milestone establishes its requirements, architecture and evaluation plan.

## Problem statement

The project addresses a workflow in which a patient's information is distributed across laboratory reports, discharge summaries, visit notes and prescriptions. Documents may arrive as digital PDFs or scans, while numeric results need units, reference ranges and dates to be useful in a longitudinal view. Reviewing these separate records requires users to assemble the context themselves.

The proposed platform addresses three related problems:

1. Patients need a consolidated view of their indicators, visits, prescriptions and laboratory history, with clear displays of values and changes over time.
2. Doctors need to locate relevant facts in long documents and review a patient's history without repeatedly reading every source in full.
3. Laboratory staff need a way to associate uploaded results with the correct patient and make those results available as structured records.

User research under MDP-12 will examine how patients, doctors and laboratory staff handle these tasks in practice. The findings will guide requirement priorities and interface design. The literature review and system comparison will establish how existing approaches address the same problems.

## Target users

| User | Intended needs and interactions |
| --- | --- |
| Patient | View their own record, laboratory history and trends; upload documents; read summaries alongside the source documents. |
| Doctor | Review records of patients they are authorized to access, inspect indicator dynamics and document summaries, and add visit notes and prescriptions. |
| Laboratory staff | Upload and associate laboratory results with the correct patient, including dates, units and supplied reference ranges. |
| Administrator | Manage accounts and roles, and inspect the audit log. Administrative duties do not imply unrestricted access to clinical content. |

Access boundaries and patient-to-doctor relationships will be specified in MDP-5 and enforced through role-based and record-level authorization during implementation.

## Aim

To design and implement a prototype of an intelligent medical platform, available through web and mobile applications, that consolidates patient records, uses machine learning methods to structure and summarize documents and analyze indicator dynamics, and presents the results in a clear dashboard; then evaluate its quality against explicit baseline solutions.

## Objectives

1. Analyze the domain, related research and existing systems, and collect user evidence to validate or revise the problem hypotheses.
2. Specify functional and non-functional requirements with priorities and verifiable acceptance criteria.
3. Design the architecture, data model and interfaces connecting the clients, API, database and document-processing services.
4. Implement authentication, user roles, patient records, visits, prescriptions and laboratory results management.
5. Build document upload and processing, including OCR where needed, structured extraction and summarization; retain access to the original document for verification.
6. Provide a patient dashboard and longitudinal laboratory views, with reference-range flags and trend analysis.
7. Evaluate extraction, summarization, analytics and usability against the defined baselines, and document results, failures and limitations.

## Expected outcomes

| Outcome | Evidence to be delivered |
| --- | --- |
| Patient Health Dashboard | A consolidated view of indicators, visits, prescriptions and laboratory history, with charts of changes over time. |
| Laboratory Results Management System | Authorized upload, storage and retrieval of results with patient association, dates, values, units and reference ranges. |
| Medical Document Summarization System | An upload-to-processing workflow producing structured fields and a readable summary with access to its source document. |
| Integrated prototype | Web and mobile clients, a shared backend API, database and ML services, with reproducible setup instructions once runnable code is available. |
| Engineering documentation | Requirements, architecture and data model, design decisions, test and evaluation plans, and a report of the final results and limitations. |
| Reproducible evaluation | Synthetic fixtures, baseline implementations, evaluation scripts and recorded results on a fixed test set separate from tuning data. |

## Project scope

### In scope

- Registration, login and roles for patients, doctors, laboratory staff and administrators.
- Patient profiles, visit history and prescription records.
- Laboratory result upload, storage, supplied reference ranges, abnormal-value flags, history and trends.
- Medical document upload, digital-text extraction or OCR, structured field extraction and summarization.
- Dashboard views linking patient indicators, visits, prescriptions and processing results.
- Web and mobile applications using the same backend API. The initial mobile scope focuses on patient scenarios; richer doctor workflows are planned for the web client.
- Role-based and record-level access control, audit logging and secure configuration.
- Evaluation using synthetic patient records and templated reports. Public de-identified datasets may be considered only after their licence and access conditions are checked and the decision is documented.

### Out of scope

- Medical diagnosis, treatment recommendations or autonomous clinical decisions.
- Production deployment in a hospital or laboratory, or integration with real clinical systems. FHIR-based interoperability is possible future work.
- Real patient data in development, demonstrations, interviews or the repository.
- Medical-device certification, clinical trials or claims of clinical effectiveness.
- Billing, appointment booking and telemedicine.
- Training a general-purpose medical language model from scratch.

A flag means that a value is outside a supplied reference interval or matches a defined trend rule; it is not a diagnosis. Summaries must be visibly identified as AI-generated and allow users to inspect the source. Prototype evaluation does not establish suitability for clinical use.

## Engineering approach and complexity

The platform will use FastAPI for the backend, PostgreSQL for structured records, React with TypeScript for the web application, React Native with Expo for mobile, and Python for ML services. Docker Compose will support local deployment. The technology comparison documents the rationale for these choices and the alternatives considered.

The system involves two clients, a shared API, persistent structured records, document storage and an asynchronous processing pipeline. Its engineering complexity includes authorization across different user roles, associating extracted data with source documents, representing units and dates consistently, exposing processing failures to users, and integrating ML outputs whose quality must be measured separately from ordinary software correctness.

The document-processing pipeline will combine OCR and extraction with retrieval-assisted summarization and structured output. A separate analytics component will examine laboratory trends. Evaluation against rule-based extraction, extractive summaries and reference-range-only flags will measure the contribution of these methods.

## Verification and success criteria

Evaluation will cover functional correctness, access control, extraction quality, summary faithfulness, trend detection, response time and usability. MDP-8 defines the detailed procedures, test data and measurement conditions for the following targets.

| Area | Verification and target |
| --- | --- |
| Functional scope | Every Must requirement in MDP-5 passes its acceptance criteria, including the patient dashboard, laboratory workflow and document-processing workflow. |
| Authorization | Automated checks verify that each role can access only permitted operations and patient records. |
| Extraction | Field-level precision, recall and F1 on fixed synthetic reports with varied templates and scan quality; target F1 at least 0.85 and improvement over a rule-based parser. |
| Summarization | At least 30 synthetic documents, reviewed by at least two raters using blinded comparisons with extractive summaries and an LLM without retrieval; faithfulness target at least 4/5, with zero numeric inconsistencies in the evaluated outputs. |
| Trend analytics | Compare precision and recall against reference-range-only flags on synthetic series with labelled trends; target higher recall at similar precision, with the comparison tolerance defined before evaluation. |
| Dashboard performance | Target API p95 response time below 2 seconds on a local dataset of 200 synthetic patients; hardware and load conditions must be recorded. |
| Usability | At least five participants perform agreed scenarios; SUS target at least 70 and task success at least 80%. |

The test set will remain separate from the data used to develop and tune the methods. The evaluation report will present measured results, comparison with baselines, error analysis and the limitations of synthetic data and human ratings. Measurement procedures will be fixed before the final experiments.

## Delivery boundaries and dependencies

M1 establishes the proposal, research, requirements, architecture, prototypes and evaluation plan. Later milestones cover the backend and client foundations, laboratory workflows, document processing, summarization, analytics, hardening and final evaluation. Detailed assignments and dates belong in the backlog.

Delivery depends on access to interview participants, individual repository and YouTrack accounts, and an available model provider or local inference environment. Supervisor feedback will guide decisions at subsequent milestones. The principal risks are excessive scope for a three-person team, extraction errors on scans, unsupported facts in generated summaries, and an evaluation set that is insufficiently representative. Mitigations include prioritizing mandatory workflows, starting with digital PDFs, retaining source documents, checking numeric consistency and reporting dataset limitations.