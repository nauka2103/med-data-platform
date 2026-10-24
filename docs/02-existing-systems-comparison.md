# Existing system comparison

| Item | Value |
| --- | --- |
| Project | Intelligent Medical Platform |
| Work item | MDP-3 — Existing system comparison |
| Evidence reviewed | 23 October 2026 |
| Scope | Four existing systems; nine criteria; public primary sources |
| Related document | [Project proposal and scope](01-proposal.md) |

## Purpose and selection

This comparison examines existing approaches to consolidating patient information, reviewing laboratory history, and structuring and summarizing medical documents. Four systems represent complementary product categories: a patient portal, a personal health application, a patient and provider platform, and a configurable clinical record system.

| System and comparison boundary | Reason for inclusion |
| --- | --- |
| **Epic MyChart**, the patient portal; selected provider implementations are identified explicitly | A reference for viewing and sharing records across healthcare organizations. The comparison does not attribute the entire Epic EHR's capabilities to MyChart. [Record sharing][M2] |
| **Apple Health / Health Records**, the patient application on iPhone and iPad | A reference for patient-controlled aggregation, trends and sharing. Provider downloads depend on participating organizations and regional availability. [Health Records][A1], [Health app][A2] |
| **Guava**, patient application and Provider Dashboard | A close functional comparator: uploaded records, structured laboratory charts and AI summaries are documented. Provider Dashboard capabilities are distinguished from the patient application. [FAQ][G1], [Hint integration][G2], [AI summaries][G3] |
| **OpenMRS O3** and the explicitly named platform/module capabilities | A reference for a configurable clinical record system, laboratory workflows and interoperability. Module documentation is evidence of an available component, not proof that every deployment enables it. [Repositories][O1], [FHIR guide][O5] |

## Method and rating rules

Criteria C1–C7 cover patient records, laboratory data, document processing, user workflows and client availability. C8 examines data exchange and export. C9 examines access auditing separately from access permissions.

- **Documented**: a cited primary source explicitly describes the capability within the stated product boundary.
- **Partial**: evidence covers only part of the criterion, or support is limited to the named provider deployment, module or product tier. Unverified aspects are labelled **not documented**.
- **not documented**: the reviewed sources do not establish the capability; its absence cannot be inferred from this rating.

The comparison is based on public primary sources reviewed on 23 October 2026, without hands-on testing of installed systems. Announced future functionality is distinguished from released capabilities. The assessment is qualitative because the systems serve different user groups and missing documentation does not establish a missing feature. Vendor descriptions provide evidence of stated capabilities, not independent measurements of accuracy, security or clinical effectiveness.

## Comparison matrix

| Criterion | Epic MyChart | Apple Health / Health Records | Guava | OpenMRS O3 / named modules |
| --- | --- | --- | --- | --- |
| **C1. Consolidated patient record** — clinical history and results in one view | **Documented** — Happy Together combines visits, medications and test results from participating organizations. [M2][M2] | **Documented** — imports clinical records, including medications and labs, from supporting organizations; Health also consolidates app/device data. [A1][A1], [A3][A3] | **Documented** — imports portal records, PDFs and C-CDA documents alongside patient-entered and device data. [G1][G1] | **Documented** — patient chart modules include medications, notes, conditions, test results and vitals within an implementation. Automatic cross-provider consolidation is **not documented** in this source. [O1][O1] |
| **C2. Laboratory history and reference ranges** — results over time with range context | **Partial** — UW Medicine documents result history, reference ranges and normal/abnormal status in its MyChart deployment; availability across all providers is **not documented**. [M3][M3] | **Partial** — laboratory record import is documented; preservation/display of report-specific reference ranges and abnormal-value flags is **not documented** in the reviewed sources. [A1][A1] | **Documented** — longitudinal laboratory results and configurable patient/group reference ranges are described for the Hint-connected Provider Dashboard. This does not establish identical controls in the free patient plan. [G2][G2] | **Partial** — test-results widgets and laboratory request/result tables are documented; display of report-specific units, ranges and abnormal flags is **not documented** in this source. [O1][O1] |
| **C3. Longitudinal visualization** — charts of changes over time | **Partial** — UW Medicine documents Trend Results graphs, including separate graphs when methods/ranges differ substantially. Universal provider availability is **not documented**. [M3][M3] | **Documented** — Apple describes existing laboratory result trends; general Health trends and highlights are also documented. This does not establish an ML laboratory anomaly detector. [A4][A4], [A2][A2] | **Documented** — uploaded and integrated laboratory results become interactive longitudinal charts with trendlines. [G2][G2] | **Documented** — configurable clinical summary tiles support graphs and tables of observations, including grouping related measurements. This does not establish ML trend analysis. [O2][O2] |
| **C4. PDF/scan ingestion with structured extraction** — beyond storing an attachment | **Partial** — document uploads and viewing are documented for specified workflows; general PDF/scan OCR into structured laboratory fields is **not documented**. [M1][M1] | **not documented** — the reviewed Health Records instructions describe provider downloads and test-record links/QR codes, not a general PDF/scan OCR workflow. [A1][A1] | **Documented** — PDFs/images can be uploaded and parsed into searchable records and laboratory charts; AI-enabled OCR is explicitly described. [G2][G2], [G3][G3] | **Partial** — an attachments widget is documented; OCR and extraction from attachments into structured fields are **not documented**. [O1][O1] |
| **C5. AI document summaries and source verification** — generated summaries that can be checked against records | **not documented** — health/visit summaries are listed, but these sources do not establish AI summarization of uploaded documents with source verification. [M1][M1] | **not documented** for this workflow — announced Apple Intelligence health insights do not establish summaries of uploaded medical documents with source verification; the redesign was announced for later in 2026. [A4][A4] | **Partial** — AI summaries use records, including scanned PDFs; provider review and checking details against source data in the chart are described. Sentence-level citations or document-span links are **not documented**. [G3][G3] | **not documented** — configurable clinical summary tiles are described, but generative document summarization with source verification is not established. [O2][O2] |
| **C6. Patient, doctor and laboratory workflows** — participation with distinct access boundaries | **Partial** — patient, proxy and provider-sharing workflows are documented; a separate laboratory-staff upload role inside MyChart is **not documented**. [M1][M1], [M2][M2] | **Partial** — patient-controlled sharing with people and participating providers is documented; a laboratory-staff workspace is **not documented**. [A3][A3] | **Partial** — patient application, provider dashboard and selective sharing are documented; a separate laboratory-staff role is **not documented**. [G1][G1], [G2][G2] | **Partial** — clinical chart, laboratory workflow and configurable roles/privileges are documented; a patient self-service application with the proposal's access relationships is **not documented** in these sources. [O1][O1], [O3][O3] |
| **C7. Web and mobile access** — client coverage for project users | **Documented** — CHA documents a web version and iOS/Android applications with a subset of web features. Feature parity is not implied. [M4][M4] | **Partial** — iPhone/iPad application is documented; a corresponding web or Android client is **not documented** in these sources. [A2][A2] | **Documented** — browser access, native iOS/Android apps and a progressive web app are documented. [G1][G1] | **Partial** — O3 documents desktop, tablet and phone browser layouts; a native patient mobile application is **not documented** in this source. [O4][O4] |
| **C8. Data exchange and export** — a documented route beyond one application | **Documented** — Care Everywhere/Share Everywhere sharing, PDF copies and a request for computer-readable records are described; processing depends on the healthcare organization. [M2][M2] | **Documented** — user-authorized app sharing and Export All Health Data are described. This does not imply a general server-side clinical API. [A3][A3] | **Documented** — portal/C-CDA import, individual report PDF downloads and CSV export of manually logged entries are described. CSV export of the entire clinical record is **not documented** by this FAQ. [G1][G1] | **Documented** — the FHIR2 module supplies a FHIR REST API for supported-resource import/export; resource coverage and enabled-module configuration must be checked. [O5][O5] |
| **C9. Access auditing** — evidence of who accessed a record, beyond permissions alone | **Partial** — Epic lists a feature for seeing family members and care providers who accessed the record; complete event coverage and retention are **not documented**. [M1][M1] | **Partial** — users can inspect and revoke sharing permissions; a chronological record-read audit log is **not documented**. [A3][A3] | **Partial** — Guava states that it maintains activity/audit logs and disclosure logs; a patient/admin interface showing every record read and its retention is **not documented**. [G4][G4] | **not documented** — the reviewed role-configuration documentation establishes permissions, not a chronological record-read audit log. [O3][O3] |

## Comparative findings

1. **Record consolidation and longitudinal visualization.** MyChart, Apple Health and Guava document aggregation and longitudinal views, while OpenMRS provides configurable observation charts. These capabilities are established approaches among the selected systems. [M2][M2], [M3][M3], [A3][A3], [A4][A4], [G2][G2], [O2][O2]
2. **Document processing and AI summarization.** Guava has the closest documented overlap with the proposed document workflow, combining OCR, structured laboratory extraction and AI summaries. Public feature descriptions alone do not provide a basis for comparing extraction accuracy or summary faithfulness. [G2][G2], [G3][G3]
3. **Source traceability.** Guava describes verification of summary details against source data in the chart, and MyChart identifies information originating from other organizations. These examples demonstrate source-awareness at the record level; sentence-level citations and document-span navigation remain **not documented** in the cited descriptions. [G3][G3], [M2][M2]
4. **Laboratory comparability.** UW Medicine documents cases where changes in equipment and reference ranges require separate trend graphs. Longitudinal visualization therefore depends on measurement context as well as dates and numeric values. [M3][M3]
5. **Access control, auditing and exchange.** OpenMRS documents configurable roles and FHIR-based exchange, while Guava and MyChart describe audit-related capabilities. The available evidence distinguishes permission configuration, access-history visibility and data exchange as separate capabilities with deployment-specific boundaries. [O3][O3], [O5][O5], [G4][G4], [M1][M1]

## Relevance to the proposed platform

The proposed Intelligent Medical Platform combines patient records, laboratory history, document extraction, summarization and visualization within a web and mobile prototype. Its evaluation focuses on field-level extraction quality, summary faithfulness, trend detection and usability against explicit baselines. Original documents remain available for verification, and authorization is defined at both role and record levels. Live clinical integration, including FHIR-based exchange, remains outside the implementation scope. [Project scope](01-proposal.md#project-scope), [evaluation targets](01-proposal.md#verification-and-success-criteria)

The comparison establishes functional overlap with existing systems rather than a market-wide feature gap or measured superiority of the proposed platform.

## Limitations

The review covers four systems and their publicly available descriptions. Capabilities may depend on region, subscription, enabled modules or provider configuration. Kazakhstan-specific provider connectivity, extraction quality for Russian and Kazakh documents, and comparable accuracy and performance measurements are **not documented** in the reviewed evidence. These aspects cannot be assessed from the matrix alone.

## Evidence register

The register contains vendor and project documentation, official repositories, and instructions published by the healthcare provider operating the named deployment. All sources were accessed on **23 October 2026**. The descriptions identify the relevant sections and scope of evidence. Web pages and repository branches may change after the access date.

| ID | Source | Relevant evidence and boundary |
| --- | --- | --- |
| M1 | [Epic — Explore MyChart][M1] | Connecting and Sharing: access history and family access. Health: summaries, document upload/viewing. A feature catalogue, not proof that every provider enables every feature. |
| M2 | [Epic — Share your medical record][M2] | Happy Together, Care Everywhere, Share Everywhere, source-organization indicator, PDF and computer-readable copy requests. |
| M3 | [UW Medicine — Lab equipment and reference ranges][M3] | FAQs on historical results, normal/abnormal status and Trend Results when equipment/reference ranges change. Evidence for UW Medicine's deployment. |
| M4 | [Cambridge Health Alliance — MyCHArt][M4] | Manage Your Health Care from a Phone or Tablet: web version and iOS/Android apps; mobile contains selected web features. |
| A1 | [Apple — Download health records on iPhone][A1] | Automatic downloads of labs and other clinical records; supporting organizations, account connection and availability constraints. |
| A2 | [Apple — Use the Health app on your iPhone or iPad][A2] | Supported device context, highlights and trend notifications. |
| A3 | [Apple — Health App & Privacy][A3] | Aggregation, export, app permissions and sharing/revocation with people and healthcare providers. Describes controls, not a read-audit interface. |
| A4 | [Apple — Health and fitness capabilities using Apple Intelligence][A4] | 9 September 2026 announcement: existing lab import/trends; future redesigned Health app and insights. Future announcements are not counted as released features. |
| G1 | [Guava — FAQ][G1] | Supported data/import formats; devices; sharing; PDF downloads; CSV export limited to manually logged entries. |
| G2 | [Guava — Hint integration][G2] | Updated 15 October 2026: provider integration, PDF/image parsing, laboratory charts, patient/provider access and custom reference ranges. Context is the Provider Dashboard integration. |
| G3 | [Guava — AI clinical summaries][G3] | 7 October 2026: OCR inputs, generation/review workflow and FAQ on checking details against source data in the patient's chart. No independent quality benchmark. |
| G4 | [Guava — Privacy & Security][G4] | HIPAA Security Rule and Privacy Rule sections: vendor statements about access control, activity/audit logs and disclosure logs. Not an independent compliance audit. |
| O1 | [OpenMRS O3 — Key repositories][O1] | Patient Chart: attachments, notes, test results and other widgets. Laboratory app: request queues and results tables. Component availability depends on implementation. |
| O2 | [OpenMRS O3 — Configuring the Patient Chart][O2] | Clinical summary tiles: observation graphs/tables, graph grouping and date ordering. These are not evidence of generative summaries. |
| O3 | [OpenMRS O3 — Configuration overview, official source][O3] | Backend configuration: initializer supports roles and privileges. Configuration support does not establish patient-level authorization or read auditing in a specific deployment. |
| O4 | [OpenMRS O3 — Workspaces overview][O4] | Desktop side panels and tablet/phone overlay layouts; evidence of responsive browser UI. |
| O5 | [OpenMRS — FHIR strategy, tools and API][O5] | FHIR2 module, import/export, supported-resource limitations and lab-system exchange examples. Module/API capability, not automatic integration. |

[M1]: https://www.mychart.org/l/en-us/explore/
[M2]: https://www.mychart.org/l/en-us/features/share/
[M3]: https://www.uwmedicine.org/specialties/laboratory-medicine-and-pathology/clinical-lab-locations/lab-equipment-updates
[M4]: https://www.challiance.org/mychart
[A1]: https://support.apple.com/en-ie/guide/iphone/iphc30019594/ios
[A2]: https://support.apple.com/en-us/104997
[A3]: https://www.apple.com/legal/privacy/data/en/health-app/
[A4]: https://www.apple.com/newsroom/2026/09/apple-advances-health-and-fitness-capabilities-using-apple-intelligence/
[G1]: https://guavahealth.com/faq
[G2]: https://guavahealth.com/article/guava-hint-integration
[G3]: https://guavahealth.com/article/ai-clinical-summaries
[G4]: https://guavahealth.com/privacy-and-security
[O1]: https://o3-docs.openmrs.org/en-US/docs/key-repositories/
[O2]: https://o3-docs.openmrs.org/en-US/docs/configure-o3/configure-the-patient-chart/
[O3]: https://github.com/openmrs/openmrs-contrib-o3-docs/blob/main/content/en-US/docs/configure-o3/overview.mdx
[O4]: https://o3-docs.openmrs.org/en-US/docs/workspaces/
[O5]: https://openmrs.atlassian.net/wiki/spaces/docs/pages/26935684?atl_f=content-tree
