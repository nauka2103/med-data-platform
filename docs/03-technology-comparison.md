# Technology comparison and selection

| Item | Value |
| --- | --- |
| Project | Intelligent Medical Platform |
| Work item | [MDP-4 — Technology comparison](https://nauka11.youtrack.cloud/issue/MDP-4) |
| Document date | 23 October 2026 |
| Scope | Six technology decisions; three candidate options per decision |
| Basis | [Project proposal](01-proposal.md), [requirements baseline][REQ], [existing system comparison](https://github.com/nauka2103/med-data-platform/blob/0d99f30ed1e87f47fb8d45a2e6e16f740db0f871/docs/02-existing-systems-comparison.md) |

## 1. Decision context

The platform combines structured patient records, laboratory histories, document extraction, source-grounded summaries and dashboards through a shared API, web application and mobile application. The approved proposal specifies FastAPI, PostgreSQL, React with TypeScript, React Native with Expo, Python processing services and Docker Compose. This comparison evaluates those choices against alternatives and selects supporting OCR and job-processing technologies.

The intended deployment is a reproducible diploma prototype using synthetic records. Production hospital integration, autonomous diagnosis and training a general-purpose medical language model are outside scope. The decisions therefore prioritize correctness, traceable processing and maintainability within a three-person project over distributed infrastructure intended for a hospital-scale deployment. [Project scope](01-proposal.md#project-scope)

### Requirement traceability

The identifiers below refer to the published MDP-5 requirements baseline at commit `dbc7bd494a214f10adacbbcf0761b6ae575d8d30`. [Requirements specification][REQ]

| Requirement group | Relevant obligations | Technology implications |
| --- | --- | --- |
| FR-AUTH-1, FR-AUTH-2, FR-ADM-1 | Patient registration; revocable sessions; role and record authorization; administrator account/assignment management | Central API authorization, persisted assignments and session revocation; client controls cannot enforce access by themselves. |
| FR-PAT-1, FR-LAB-1–3 | Related patient records; draft/confirmed laboratory batches; units, dates and supplied ranges; duplicate-safe publication | Transactions, relationship constraints and explicit data validation; chart queries retain measurement context. |
| FR-DOC-1, FR-DOC-2 | PDF/JPG/PNG upload; retained originals; asynchronous jobs; readable failure states; OCR and draft fields with source references | A separate processing worker, persisted job state, local document tools and inspectable extraction outputs. |
| FR-SUM-1–3, NFR-ACC-2 | Schema-valid summaries; authorized retrieval context; item-level evidence; consistency gate before publication | Versioned input/output schemas, source mapping and an independently evaluated summarization component. |
| FR-DASH-1, FR-UI-1 | Shared records and patient scenarios on web/mobile; distinct loading, empty and failure states; usable narrow layouts | Two clients using one API contract, with explicit state handling and platform-specific verification. |
| NFR-SEC-1, NFR-PRIV-1, NFR-AUD-1 | Transport security, synthetic data, no clinical bodies in logs, comprehensive access auditing | Server-side security and audit policies; technology selection alone does not satisfy these obligations. |
| NFR-AVL-1, NFR-MAINT-1 | Compose setup, restart persistence, job recovery, automated checks | Persistent volumes, pinned dependencies, repeatable seeds and failure/recovery tests. |
| NFR-PERF-1–2, NFR-ACC-1, NFR-USE-1 | Dashboard p95 below 2 s; processing target; extraction F1 at least 0.85; usability targets | Verification on fixed workloads and fixtures; these are acceptance targets, not demonstrated technology performance. |

## 2. Comparison method

Each decision compares three candidate options against explicit criteria. A candidate must support the applicable mandatory workflow; preference is then given to integration with the proposed stack, manageable operations and reproducible evaluation. The tables distinguish documented capabilities from project-specific consequences.

Official documentation and project repositories support capability claims. Statements about integration effort and operational burden are architectural judgments for this prototype, not measured development-time or performance results. No numerical ranking is assigned without benchmark evidence. The selected options define the implementation baseline; their acceptance remains subject to the verification conditions below.

## 3. D1 — Shared backend API

**Requirements:** FR-AUTH-1–2, FR-ADM-1, FR-UI-1, FR-SUM-1–2, NFR-MAINT-1.

**Criteria:** Python processing integration; API schemas and validation; authorization extensibility; implementation and maintenance burden.

| Candidate | Capabilities relevant to the criteria | Integration and limitations | Decision |
| --- | --- | --- | --- |
| **FastAPI with Python** | OpenAPI/JSON Schema documentation, Pydantic data validation and dependency injection provide an explicit API boundary. [B1][B1] | Shares the Python ecosystem with extraction and ML code. Authentication, session revocation, record filtering, audit behavior and persistence still require application logic. CPU-heavy OCR belongs in workers. | **Selected** |
| **Django REST framework with Python** | Provides request permissions and object-level permission hooks. Its documentation explicitly distinguishes object checks from list filtering and creation policies. [B2][B2] | Also compatible with Python processing. A viable alternative, but changes the proposal's backend framework without removing the need for assignment-aware authorization or separate workers. | Alternative |
| **NestJS with TypeScript** | Modular Node.js framework with dependency injection; guards and policies support authorization. [B3][B3], [B4][B4] | Aligns backend language with the clients, but Python document processing would cross a language/service boundary. That extra boundary is not required for the initial prototype. | Alternative |

**Chosen option and justification.** FastAPI preserves the proposal's Python backend while supporting a documented contract shared by both clients. Pydantic schemas can represent upload/job responses and structured summary outputs, with additional factual-consistency checks implemented separately. Python reuse is the deciding integration criterion; no claim is made that FastAPI is inherently faster or more secure than the alternatives. [B1][B1]

**Consequences and verification.** Authorization must cover individual resources, lists, searches, nested job/source identifiers and assignment revocation. Logout must invalidate subsequent use of the session; a self-contained token without a revocation mechanism would not satisfy FR-AUTH-1. Verify the complete access matrix, schema rejection and session replay behavior through API tests. Worker execution is addressed in D6.

## 4. D2 — Primary database

**Requirements:** FR-AUTH-2, FR-PAT-1, FR-LAB-1–3, FR-DOC-1, FR-SUM-1, NFR-AUD-1, NFR-AVL-1.

**Criteria:** Related-record integrity; atomic publication and duplicate prevention; structured and variable metadata; concurrent API/worker access and recovery.

| Candidate | Capabilities relevant to the criteria | Integration and limitations | Decision |
| --- | --- | --- | --- |
| **PostgreSQL** | Primary/foreign keys, unique and check constraints support related records; transactions provide atomic updates, and JSON/JSONB types support variable metadata. [DB1][DB1], [DB2][DB2], [DB6][DB6] | Requires a database service and migrations. Fits a shared API and worker writing patient, job and audit records. Constraint design remains an application responsibility. | **Selected** |
| **MongoDB** | Supports embedded/reference-based document models and multi-document transactions. [DB3][DB3], [DB4][DB4] | Flexible for variable reports. Related patients, assignments, batches and audit events still need explicit modeling and consistency rules; multi-document transactions require a replica set or sharded cluster. | Alternative |
| **SQLite** | Embedded SQL storage suits local and embedded applications. The official guidance distinguishes this from client/server workloads and documents the single-writer limitation. [DB5][DB5] | Minimal service setup, but concurrent API/worker writes and use across separate containers require additional care. Suitable for isolated tools, not selected as the shared application database. | Alternative |

**Chosen option and justification.** PostgreSQL matches the relationship-heavy record model and FR-LAB-1's atomic, duplicate-safe confirmation workflow. Patient assignments, document ownership and source relationships remain relational. JSONB is reserved for versioned processing metadata and schema-validated summary structures; it does not replace explicit laboratory columns for value, unit, date and reference limits. [DB1][DB1], [DB2][DB2], [DB6][DB6]

**Consequences and verification.** Use a unique publication key for a confirmed laboratory batch and commit its published results atomically. Test repeated and concurrent confirmation, invalid references, rollback and restart persistence. Index patient/analyte/unit/date access paths, then measure NFR-PERF-1 on its specified workload. The database choice alone does not establish the latency target.

Original files are retained in private persistent file storage, with ownership, checksum and storage reference in PostgreSQL. Database transactions do not make filesystem writes atomic: stage the file, commit its metadata and reconcile incomplete/orphaned uploads. Audit persistence must obey NFR-AUD-1, including failure behavior before a protected response or mutation is released.

## 5. D3 — Web application

**Requirements:** FR-LAB-3, FR-DASH-1–2, FR-UI-1, FR-SUM-3, NFR-USE-1, NFR-MAINT-1.

**Criteria:** Component/state model; typed API integration; consistency with mobile development; explicit client-state and responsive-interface handling.

| Candidate | Capabilities relevant to the criteria | Integration and limitations | Decision |
| --- | --- | --- | --- |
| **React with TypeScript** | Component composition, events and shared state support interactive screens; official guidance covers TypeScript integration. [W1][W1], [W2][W2] | Shares React concepts and TypeScript models with React Native. Web uses DOM components, so mobile views still need separate implementation. Routing, forms and chart libraries require explicit selection. | **Selected** |
| **Vue with TypeScript** | Declarative, component-based interfaces with documented TypeScript tooling and Single-File Components. [W3][W3], [W4][W4] | A viable dashboard framework. With React Native retained for mobile, it introduces a second UI component model without a requirement-driven benefit established by this review. | Alternative |
| **Angular** | Provides a component framework with dependency injection, routing and forms facilities in its documented platform. [W5][W5] | A viable option for structured clinical forms. Its framework conventions would coexist with React Native's distinct model; the project does not require this additional framework boundary. | Alternative |

**Chosen option and justification.** React with TypeScript aligns the web client with the proposed mobile stack while supporting reusable typed API models and validation utilities. This is conceptual and non-visual code reuse; it does not imply that web charts or DOM components run unchanged on mobile. [W1][W1], [W2][W2], [M1][M1]

**Consequences and verification.** Represent loading, empty, unauthorized, failed-processing and retry states explicitly. Keep chart labels and tables consistent with the API's units, dates and per-result ranges. TypeScript does not validate network data at runtime or replace server authorization. Verify S1–S4 on web, source navigation, incompatible-unit separation, narrow layouts and the usability targets in NFR-USE-1.

## 6. D4 — Mobile application

**Requirements:** FR-UI-1, FR-DOC-1, FR-SUM-3, FR-LAB-3, NFR-SEC-1, NFR-USE-1.

**Criteria:** Android/iOS coverage; document selection and source viewing; integration with the TypeScript/React stack; platform maintenance and verification burden.

| Candidate | Capabilities relevant to the criteria | Integration and limitations | Decision |
| --- | --- | --- | --- |
| **React Native with Expo and TypeScript** | React Native supports native application development with frameworks such as Expo. Expo documents a system document picker on Android/iOS. [M1][M1], [M2][M2] | Reuses React concepts and typed API models. File permissions, local file URIs, source viewing and native dependencies remain platform-specific concerns. Expo Go is not a substitute for testing the intended application build. | **Selected** |
| **Flutter with Dart** | Documents a reactive widget architecture, its Dart framework and platform integration mechanisms. [M3][M3] | Supports a shared mobile codebase, but adds Dart alongside the proposed TypeScript web application. No project-specific advantage has been measured to justify that language boundary. | Alternative |
| **Separate Kotlin/Jetpack Compose and Swift/SwiftUI applications** | Official Android and Apple frameworks provide native UI and platform integration. [M4][M4], [M5][M5] | Direct platform control, but two UI implementations and toolchains in addition to the web client. This expands maintenance scope beyond the initial patient workflows. | Alternative |

**Chosen option and justification.** React Native with Expo provides a mobile implementation consistent with the proposal and the selected web development model. Expo's document picker supports the upload entry point; the full upload-to-summary workflow remains an application feature using the shared API. [M1][M1], [M2][M2]

**Consequences and verification.** Handle document-picker cancellation and readable cache copies before upload, as required by the selected Expo APIs. Server-side validation still enforces the 10 MiB limit, supported content and PDF page limit. Verify S1 and S2, source inspection, session expiry and processing recovery on the documented Android/iOS test configurations. Platform build/signing prerequisites belong in setup documentation; no app-store publication is required by this selection.

## 7. D5 — Document text extraction and OCR

**Requirements:** FR-DOC-1–2, FR-LAB-1, FR-SUM-1–3, NFR-PRIV-1, NFR-ACC-1, NFR-PERF-2.

**Criteria:** Digital and scanned input coverage; inspectable source mapping; local reproducibility and deployment dependencies; independence from an external OCR service.

All candidates use the same digital-PDF first path where usable text exists. pypdf provides text extraction but does not perform OCR or recover text embedded only in images. Scanned or unreadable-text pages therefore require an OCR path; text presence alone does not establish extraction quality. [O1][O1]

| Candidate OCR path | Capabilities relevant to the criteria | Integration and limitations | Decision |
| --- | --- | --- | --- |
| **Local Tesseract 5, with pypdf for digital PDFs** | Local OCR engine with language data and documented hOCR/TSV outputs for text and location inspection. [O2][O2], [O3][O3] | An explicit CLI/model configuration can be packaged in the worker. PDF rasterization and image preprocessing are separate steps. Reading order, decimal recognition and table-to-field mapping need evaluation and downstream logic. | **Selected** |
| **Local PaddleOCR, with pypdf for digital PDFs** | Official project provides OCR and document-parsing capabilities, including structured-document pipelines. [O4][O4] | A viable alternative where layout processing improves measured results. Adds its inference/model dependencies; its accuracy, language coverage for project fixtures and hardware cost must be evaluated rather than inferred from examples. | Alternative |
| **Azure AI Document Intelligence Layout** | Managed document-analysis API returning text, tables and document structure. [O5][O5] | Reduces responsibility for operating OCR inference, but introduces service credentials, network availability and external processing. Costs, quotas and supported configurations require a separate check before use. | Alternative |

**Chosen option and justification.** The local pypdf/Tesseract path separates digital-text extraction from OCR and provides inspectable intermediate outputs without requiring an external OCR account. This supports reproducible synthetic-data experiments and source inspection. The choice establishes a controllable initial OCR implementation, not superior medical-report accuracy. PaddleOCR remains an alternative if fixed-set evaluation demonstrates a requirement-relevant improvement. [O1][O1], [O2][O2], [O3][O3], [O4][O4]

**Consequences and verification.** Preserve the original, page identity, versioned extracted text and text-span references; retain OCR boxes when available. Store the engine, language data and preprocessing configuration for each run. Missing fields remain missing, and extracted laboratory fields remain reviewable drafts until authorized confirmation. OCR confidence is not a calibrated guarantee of correctness.

Evaluate field-level precision/recall/F1 on fixed digital and scanned fixtures, including decimals, units, dates, missing ranges and varied layouts. Separately measure OCR failures and full-pipeline latency. The extraction target of F1 ≥ 0.85 applies to the pipeline under NFR-ACC-1, not to a vendor benchmark or OCR confidence value. Any engine change requires rerunning the same evaluation before accepting it.

## 8. D6 — Asynchronous document execution

**Requirements:** FR-DOC-1, FR-LAB-1, FR-SUM-2, NFR-AUD-1, NFR-AVL-1, NFR-PERF-2.

**Criteria:** Separation from API request execution; restart recovery; timeouts and controlled retries; operating complexity for a bounded local workload.

| Candidate | Capabilities relevant to the criteria | Integration and limitations | Decision |
| --- | --- | --- | --- |
| **RQ workers with Valkey** | RQ runs Python jobs in worker processes, supports Redis/Valkey, job timeouts and retry/failure handling. Valkey supports persistent storage modes. [J1][J1], [J2][J2], [J3][J3], [J4][J4] | Introduces a worker and queue service while retaining ordinary Python functions. Durable application state, duplicate protection and reconciliation remain necessary. Suits an initial single active processing job. | **Selected** |
| **Celery workers with RabbitMQ** | Distributed Python task queue with broker transport, worker execution and workflow facilities. RabbitMQ is a supported broker. [J5][J5] | Also meets the separation requirement. Its broader routing/workflow capabilities introduce configuration choices beyond the initial document-job workflow. Prefer if later requirements justify those facilities. | Alternative |
| **FastAPI BackgroundTasks** | Runs tasks after the response; FastAPI's guidance recommends separate queue-based tools for heavy background computation. [J6][J6] | Minimizes service setup, but by itself supplies no durable job queue and recovery policy satisfying FR-DOC-1/NFR-AVL-1. Adding those facilities would require a separate implementation. | Not selected for the mandatory pipeline |

**Chosen option and justification.** RQ with Valkey separates OCR/model work from the API and provides timeout/failure mechanisms without selecting a broader distributed workflow platform. PostgreSQL remains the authoritative store for document status, ownership, processing attempts and publication. Queue results are not the patient record. This is an engineering judgment for the specified local workload, not a throughput comparison. [J1][J1], [J2][J2], [J3][J3]

**Consequences and verification.** Configure persistent queue storage and volumes, with the persistence tradeoffs documented. Broker persistence alone cannot guarantee that a database transaction and enqueue operation both succeed: use a persisted dispatch record and reconciliation to recover jobs committed before enqueue failure. Queue messages contain job identifiers; workers load only authorized job context. [J4][J4]

Use stable application job IDs and attempt identifiers, bounded retries and guarded state transitions. Enforce the 120-second processing limit from FR-DOC-1 in both worker configuration and the publication check; a timed-out or superseded attempt cannot publish late results. Duplicate execution must not create duplicate laboratory records or ready summaries. On restart, unfinished work must become ready or explicitly failed. Verify API/worker/queue restarts, duplicate delivery, enqueue failure, OCR/model failure, timeout and late-result rejection. Exactly-once execution is not assumed.

## 9. Selected technology baseline

| Area | Selection | Primary requirement rationale |
| --- | --- | --- |
| API | Python and FastAPI | Shared validated API for both clients and integration with Python processing; FR-UI-1, FR-SUM-1. |
| Primary database | PostgreSQL | Related-record integrity and atomic, duplicate-safe publication; FR-AUTH-2, FR-LAB-1. |
| Web | React and TypeScript | Patient/doctor/laboratory workflows and typed integration with the common API; FR-DASH-1–2, FR-UI-1. |
| Mobile | React Native, Expo and TypeScript | Patient login, charts, uploads and source inspection through the same API; FR-UI-1, FR-SUM-3. |
| Text/OCR | pypdf for usable digital text; local Tesseract 5 for scans | Inspectable extraction with source references and reproducible configuration; FR-DOC-2, NFR-ACC-1. |
| Processing execution | RQ workers and Valkey; application job state in PostgreSQL | Asynchronous execution, failure handling and restart recovery; FR-DOC-1, NFR-AVL-1. |
| Local service setup | Docker Compose with persistent database, queue and document volumes | Reproducible multi-service startup; NFR-AVL-1. Compose documents services and volumes in one application model. [DEP1][DEP1] |

The API and workers can use separate processes built from a shared Python codebase; these decisions do not require independent microservices for each feature. Mobile development/build setup remains separate from the Compose services.

The summarization model/provider, retrieval implementation, PDF rasterizer, charting libraries and authentication/session packages require implementation-level selection. Their evaluation must retain the requirements above. In particular, an LLM's structured output does not establish factual consistency: schema checks, authorized retrieval, source references and the FR-SUM-2 consistency gate remain separate obligations. No specific model is selected without testing the fixed synthetic-document workload and documenting its access conditions.

## 10. Validation and decision limits

| Decision | Evidence required during implementation | Condition for reconsideration |
| --- | --- | --- |
| D1 — API | Role/record/session matrix; schema rejection; no clinical payload leakage in logs | Unresolved correctness or integration problems that persist after application-level fixes. |
| D2 — Database | Concurrent publication/rollback tests, restart persistence and NFR-PERF-1 workload | A demonstrated data-access requirement that cannot be met reasonably by the selected model/indexes. |
| D3 — Web | S1–S4 evidence, chart/table agreement, source navigation and usability results | Required interactions remain unusable after interface improvements, or client integration costs are demonstrated to be excessive. |
| D4 — Mobile | S1/S2 evidence on documented platform builds, file handling, authorization and source viewing | Required native/file features cannot be delivered through the chosen Expo/React Native configuration. |
| D5 — OCR | Held-out extraction metrics and timing with all failures reported | Accuracy or processing targets remain unmet, or an alternative improves the same fixed-set results at an acceptable operating cost. |
| D6 — Workers | Restart, dispatch reconciliation, duplicate execution, timeout and late-publication tests | Required recovery cannot be achieved, or workflow/routing needs justify a broader execution platform. |

These are future implementation checks, not completed test results. Technology documentation does not establish the project's extraction F1, summary faithfulness, latency or usability. Exact supported dependency versions, model files, container images and licences must be recorded in the implementation's lockfiles and setup instructions. Changes to selections must identify affected requirement IDs and preserve the evaluation baseline.

## 11. References

Technical sources are official documentation or official project repositories. All were accessed on **23 October 2026**. Capability descriptions apply to the documented configurations; rolling documentation may change. Project-specific implementation and operating-cost judgments are identified in the comparison method.

| ID | Source | Evidence used |
| --- | --- | --- |
| REQ | [MDP-5 — Requirements specification and acceptance criteria][REQ] | Fixed requirement IDs, priorities, actor boundaries and measurable targets. |
| B1 | [FastAPI — Features][B1] | OpenAPI, JSON Schema, Pydantic and dependency injection. |
| B2 | [Django REST framework — Permissions][B2] | Request/object permission hooks and list/create authorization boundaries. |
| B3 | [NestJS — Introduction][B3] | TypeScript/Node.js framework, modules and dependency injection. |
| B4 | [NestJS — Authorization][B4] | Guards, roles and policy-based authorization. |
| DB1 | [PostgreSQL — Constraints][DB1] | Keys, relationship constraints and validation constraints. |
| DB2 | [PostgreSQL — JSON Types][DB2] | JSON/JSONB storage and indexing facilities. |
| DB3 | [MongoDB — Embedded Data][DB3] | Embedded-document modeling and its constraints. |
| DB4 | [MongoDB — Consistency with Transactions][DB4] | Multi-document transactions and deployment prerequisites. |
| DB5 | [SQLite — Appropriate Uses][DB5] | Embedded/client-server distinction and concurrent-write limits. |
| DB6 | [PostgreSQL — Transactions][DB6] | Atomic multi-step operations, isolation of intermediate changes and rollback. |
| W1 | [React — Quick Start][W1] | Components, events and shared state. |
| W2 | [React — Using TypeScript][W2] | Typed React application development. |
| W3 | [Vue — Introduction][W3] | Declarative component model and application approaches. |
| W4 | [Vue — TypeScript Overview][W4] | TypeScript and Single-File Component tooling. |
| W5 | [Angular — Overview][W5] | Components, dependency injection and application facilities. |
| M1 | [React Native — Get Started][M1] | Framework-based mobile development, including Expo. |
| M2 | [Expo — DocumentPicker][M2] | Android/iOS document selection and readable cache-copy behavior. |
| M3 | [Flutter — Architectural Overview][M3] | Dart/widget architecture and platform integration. |
| M4 | [Android — Jetpack Compose][M4] | Kotlin-based native Android UI toolkit. |
| M5 | [Apple — SwiftUI][M5] | Native interfaces on Apple platforms. |
| O1 | [pypdf — Extract Text from a PDF][O1] | Digital-text extraction and limitations on scanned/image-only content. |
| O2 | [Tesseract — User Manual][O2] | Local OCR engine and trained language data. |
| O3 | [Tesseract — Command Line Usage][O3] | Language configuration and hOCR/TSV outputs. |
| O4 | [PaddleOCR — Official Repository][O4] | OCR and document-parsing capabilities. |
| O5 | [Microsoft — Document Intelligence Layout][O5] | Managed API for text, tables and document structure. |
| J1 | [RQ — Queues][J1] | Python workers, supported queue stores and job configuration. |
| J2 | [RQ — Jobs][J2] | Job identity, status and execution-time limits. |
| J3 | [RQ — Exceptions and Retries][J3] | Failure handling and controlled retries. |
| J4 | [Valkey — Persistence][J4] | Snapshot/AOF persistence and their tradeoffs. |
| J5 | [Celery — Introduction][J5] | Worker/broker architecture, RabbitMQ support and workflows. |
| J6 | [FastAPI — Background Tasks][J6] | Post-response tasks and guidance for heavy computation. |
| DEP1 | [Docker — How Compose Works][DEP1] | Multi-service application configuration and persistent volumes. |

[REQ]: https://github.com/nauka2103/med-data-platform/blob/dbc7bd494a214f10adacbbcf0761b6ae575d8d30/docs/06-requirements.md
[B1]: https://fastapi.tiangolo.com/features/
[B2]: https://www.django-rest-framework.org/api-guide/permissions/
[B3]: https://docs.nestjs.com/
[B4]: https://docs.nestjs.com/security/authorization
[DB1]: https://www.postgresql.org/docs/18/ddl-constraints.html
[DB2]: https://www.postgresql.org/docs/18/datatype-json.html
[DB3]: https://www.mongodb.com/docs/manual/data-modeling/embedding/
[DB4]: https://www.mongodb.com/docs/manual/data-modeling/enforce-consistency/transactions/
[DB5]: https://www.sqlite.org/whentouse.html
[DB6]: https://www.postgresql.org/docs/18/tutorial-transactions.html
[W1]: https://react.dev/learn
[W2]: https://react.dev/learn/typescript
[W3]: https://vuejs.org/guide/introduction.html
[W4]: https://vuejs.org/guide/typescript/overview.html
[W5]: https://angular.dev/overview
[M1]: https://reactnative.dev/docs/environment-setup
[M2]: https://docs.expo.dev/versions/latest/sdk/document-picker/
[M3]: https://docs.flutter.dev/resources/architectural-overview
[M4]: https://developer.android.com/compose
[M5]: https://developer.apple.com/swiftui/
[O1]: https://pypdf.readthedocs.io/en/stable/user/extract-text.html
[O2]: https://tesseract-ocr.github.io/tessdoc/
[O3]: https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html
[O4]: https://github.com/PaddlePaddle/PaddleOCR
[O5]: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0
[J1]: https://python-rq.org/docs/
[J2]: https://python-rq.org/docs/jobs/
[J3]: https://python-rq.org/docs/exceptions/
[J4]: https://valkey.io/topics/persistence/
[J5]: https://docs.celeryq.dev/en/stable/getting-started/introduction.html
[J6]: https://fastapi.tiangolo.com/tutorial/background-tasks/
[DEP1]: https://docs.docker.com/compose/intro/compose-application-model/
