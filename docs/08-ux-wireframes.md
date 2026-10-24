# Document workspace and key user flows

| Item | Value |
| --- | --- |
| Project | Intelligent Medical Platform |
| Work item | [MDP-7 — UX wireframes of key scenarios](https://nauka11.youtrack.cloud/issue/MDP-7) |
| Milestone | M1 pre-defense-1; 24 October 2026 |
| Date | 23 October 2026 |
| Requirements baseline | [MDP-5 — Requirements and acceptance criteria](06-requirements.md) |
| Source and launch instructions | [Workspace guide](../mockups/README.md) |

## Interface structure

The patient, clinician and laboratory interfaces have separate entry pages. There is no shared role selector, mobile-preview switch, fixture selector or simulated-state toolbar in the product interface. Patient screens adapt to narrow widths, with a separate mobile web entry. Each workspace includes a light/dark theme toggle; the chosen theme persists locally. Both palettes use neutral black, white and gray surfaces and accents. A visible notice on every workspace explains that MedData is not a medical service, does not make medical conclusions or diagnoses, and does not assume responsibility for medical decisions based on extracted information. It directs users to check the original and consult a qualified healthcare professional. The notice describes the intended use; it does not establish legal enforceability of a liability exclusion.

The document workflow now uses a local service instead of synthetic UI events. Uploaded files are stored, read and processed. The initial record is empty and displays only data that has actually been imported or entered.

| Entry | Purpose | Source |
| --- | --- | --- |
| Patient | Upload or photograph documents, review extracted values, inspect source text and follow laboratory history. | [Patient entry](../mockups/index.html) |
| Clinician | Review the local record and enter consultation notes or prescription records. | [Clinician entry](../mockups/doctor.html) |
| Laboratory | Process reports and review/confirm measurement values. | [Laboratory entry](../mockups/laboratory.html) |
| Mobile patient web | Narrow-screen patient entry using the same local service. | [Mobile entry](../mockups/mobile/index.html) |

These are separate interfaces over a single local record. They do not implement authenticated multi-user role isolation. MDP-5 authorization, assignment and audit requirements remain acceptance obligations for the later application, not completed capabilities of this local service.

## S1 — Patient reviews recorded results

1. Open the patient workspace and review the latest confirmed measurements.
2. Select a measurement's history or open **Lab results**.
3. Choose an analyte/unit and date interval. Review the plotted points and chronological table.
4. Open the source report from the measurement table.

The chart and table use persisted reviewed values. Different units form separate series. Supplied lower/upper limits determine range flags; absent limits produce **Not assessed**. Empty history, invalid date intervals and service failures have explicit states. No synthetic measurements are preloaded.

**Requirements addressed by the interaction:** FR-DASH-1, FR-LAB-2, FR-LAB-3 and the responsive patient scope of FR-UI-1. Full profile/history completeness, authentication and clinical validation remain outside this implementation.

## S2 — Patient uploads or photographs a document

1. Choose **Upload document**, drag a file onto the drop zone, or choose **Take a photo**.
2. For camera capture, allow browser camera access, keep the page in frame and capture the image. If the camera is unavailable, choose an existing photo.
3. The service stores the file and moves through waiting, reading and ready or failed states.
4. Inspect extracted measurements alongside the recognized page text. Open the original PDF/image for comparison.
5. Verify the suggested date, edit recognized numbers or source limits if needed, then confirm reviewed values into the personal laboratory history.
6. Record a reading issue against the document when necessary.

PDF text is read through PDFKit; images and scanned PDF pages use Apple Vision. Values are selected from supported laboratory rows with explicit units. Certificates and narrative documents remain available as recognized text even when they contain no supported measurements. Unreadable, unsupported and oversized files produce an actionable error. Processing exceeding two minutes fails; failed documents may be retried.

The current output is automatically extracted text and laboratory facts, not an LLM-generated clinical summary. No interpretation of a narrative diagnosis or treatment advice is generated. Source inspection remains part of every document record.

**Requirements addressed by the interaction:** FR-DOC-1, the local extraction portion of FR-DOC-2, source inspection from FR-SUM-3 and issue reporting from FR-SUM-4. FR-SUM-1/2 and the quantitative ML-evaluation targets are not completed by deterministic extraction.

## S3 — Clinician reviews a record

1. Open the separate clinician entry.
2. Inspect document status, extracted values, originals and reviewed laboratory history.
3. Enter a consultation note or an existing clinician-authored prescription record.
4. Save and reload the page to verify that the entered record persists.

The service records the entered content without generating recommendations. This local record interface exercises note-entry and persistence. Assigned-patient lists, authentication and denied-access scenarios must be implemented with real authorization in a later application increment.

**Requirements addressed by the interaction:** the note-entry portion of FR-PAT-2 and record-review aspects of FR-DASH-2. FR-AUTH-1/2 are not implemented.

## S4 — Laboratory reviews and confirms results

1. Open the laboratory entry and upload a report.
2. Open a processed document under **Awaiting review**.
3. Compare every extracted value and unit with the original and its recognized source line.
4. Correct the numeric values/limits, verify the measurement date and confirm.
5. The document moves to confirmed reports and the values appear in laboratory history. Repeating confirmation does not add another copy.

An inverted reference interval prevents confirmation. Missing limits remain missing. Originals and source lines remain associated with the reviewed values. Extracted drafts are not included in history before confirmation.

This increment supports document-derived drafts. Fully manual structured batch creation, multi-patient associations and staff assignment checks from FR-LAB-1/FR-AUTH-2 remain later application work.

## Changes from the initial requirements baseline

The user requested real upload/camera capture, separate entry pages and day/night themes. The personal workspace therefore supports confirmation of user-reviewed imported measurements into a personal history. These records are not represented as institution-verified laboratory publications. Institution staff workflows and patient-to-staff authorization must remain separate when multi-user access is implemented.

Local runtime files are kept outside the repository. Development/evaluation fixtures and submitted screenshots remain synthetic or empty. The native mobile application, clinician assignment model, production security, diagnostic interpretation and generative document summarization are not implied by this interface increment.

## Readable exports

| View | Export |
| --- | --- |
| Patient overview, light | [Overview](../mockups/exports/01-patient-overview.png) |
| Patient documents | [Documents](../mockups/exports/02-documents.png) |
| Laboratory history | [Lab results](../mockups/exports/03-laboratory-results.png) |
| Separate clinician workspace | [Clinician](../mockups/exports/04-doctor-workspace.png) |
| Separate laboratory workspace | [Laboratory](../mockups/exports/05-laboratory-workspace.png) |
| Patient overview, dark | [Dark overview](../mockups/exports/06-dark-overview.png) |
| Mobile entry, dark | [Mobile dark](../mockups/exports/07-mobile-dark.png) |
| Mobile entry, light | [Mobile light](../mockups/exports/08-mobile-light.png) |

Exports contain empty records, so personal uploaded files cannot accidentally become submission material. The editable interface is implemented in the HTML/CSS/JavaScript sources; screenshots are generated from those sources.

## Verification and limitations

Automated browser/API verification uses a separate temporary database and synthetic documents. It checks actual image upload and Apple Vision recognition, digital PDF extraction, source review, validation, confirmation, duplicate prevention, persisted laboratory values across a service restart, persisted consultation notes, separate entry pages, theme persistence and narrow layouts at 360/390 pixels. It also rejects an unsupported file, rejects a foreign Origin and verifies that server sources are not publicly served by the static handler.

Physical-camera capture quality, performance across diverse medical layouts, extraction quality metrics, clinical faithfulness and participant usability have not been established. Certificates and unsupported tables may yield text without structured results. The local service is intended for the current OS user and is bound to loopback; it has no authenticated multi-user access model. See the workspace guide for its storage location, operation and remaining application requirements.
