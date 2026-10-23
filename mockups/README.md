# MedData — local document workspace

A working local interface for medical-document upload, camera capture, text recognition, laboratory-value review and history. Patient, clinician and laboratory pages are separate. Light and dark themes persist across reloads.

## Start on this Mac

From the repository root:

```bash
python3 mockups/service/server.py
```

The first start compiles the local recognition helper. This requires macOS with Apple's command-line developer tools (`xcrun swiftc`). The service uses Python's standard library, PDFKit and Apple Vision; no model API key or external Python package is required.

| Workspace | Address |
| --- | --- |
| Patient | <http://127.0.0.1:8765/index.html> |
| Clinician | <http://127.0.0.1:8765/doctor.html> |
| Laboratory | <http://127.0.0.1:8765/laboratory.html> |
| Mobile patient entry | <http://127.0.0.1:8765/mobile/index.html> |

Stop the service with Ctrl+C. Opening the HTML as `file://` or using a static-only HTTP server does not enable document processing. The mobile entry is a responsive web interface, not the planned native React Native application. Camera capture on this Mac uses the browser's permission prompt. On a mobile browser the camera file input requests the rear camera; the loopback service is not exposed to other devices.

## Document workflow

1. Choose **Upload document**, drag a file into the drop zone, or choose **Take a photo**.
2. Upload a PDF, JPG or PNG up to 10 MiB. PDFs must be readable, unlocked and no longer than 20 pages. HEIC is not supported; export the image as JPG first.
3. The service saves the original, reads digital PDF text or uses Apple Vision for scans/photos, and identifies supported laboratory rows. Upload and processing statuses come from the service.
4. Open the recognized source beside the extracted values. The parser supports common English/Russian analyte names, including glucose, hemoglobin, platelets, white/red blood cells, creatinine, cholesterol, CRP, ALT, AST, TSH and HbA1c. A result must have a supported explicit unit immediately after the number. Unrecognized formats remain visible in the full text; no missing value is invented.
5. Verify the value and source range, correct recognized numbers if necessary, and confirm the measurement date. The date is only a suggestion extracted from the document and must be checked.
6. Confirm to add reviewed results to history. Units remain separate series. Repeated confirmation does not duplicate the results.

Medical certificates and narrative reports can be uploaded and read as recognized text even when no laboratory rows are identified. The present analysis is OCR plus deterministic extraction and comparison with supplied reference limits. It does not generate a clinical diagnosis, interpret narrative medical meaning or perform LLM-based summarization. The interface identifies the extracted content accordingly.

## Storage and access

Originals, recognized text, reviewed measurements, notes and reading-issue reports persist in:

```text
~/Library/Application Support/MedDataPlatform/
```

The directory and database are restricted to the current OS user. Medical records are not stored in the Git repository or screenshot exports and are not sent to an external model service. The recognizer runs on the same Mac. `MDP_DATA_DIR` can select a different storage location; tests use an isolated temporary directory.

The service binds only to `127.0.0.1`. It checks Host and Origin, validates supported file signatures, bounds upload sizes and processing time, and does not serve its service source or stored files through generic static routes. Original documents use dedicated document-ID routes.

**Current access boundary:** this is a single local record workspace belonging to the OS user. The clinician and laboratory entry pages present different workflows over that same local record; they are not isolated authenticated accounts. Login, multi-patient assignments, role/record authorization, audit logging, encrypted storage, retention/deletion controls and production deployment remain application work. Do not expose this service on a network or treat separate page URLs as access control. These limitations are distinct from the working upload/recognition/persistence functionality.

The programme's requirement to keep development fixtures, repository material and demonstrations synthetic remains applicable. Any personal files voluntarily opened in the local workspace stay in runtime storage and must not be added to the repository or submission exports.

## Browser verification

The optional check requires Node.js and Playwright in the execution environment:

```bash
node mockups/check-wireframes.cjs
```

Use Playwright's Chromium or set `CHROME_PATH` to an installed Google Chrome executable. Set `NODE_PATH` if Playwright is installed outside the repository. The check starts an isolated service on port 8766, generates a synthetic image and PDF, uploads them, exercises real OCR/text extraction and review, checks persistence across a service restart, and removes its temporary data. It verifies separate pages, note persistence, theme persistence, file/origin restrictions and 360/390-pixel layouts. The camera dialog is checked; physical camera image quality and mobile-device capture require manual testing on the target device.

Eight PNG exports are regenerated from empty records, with no uploaded medical content. Their purpose is interface review, not a claim of completed participant testing or clinical validation.

## Source layout

| File | Purpose |
| --- | --- |
| `index.html` | Patient workspace. |
| `doctor.html` | Clinician record and note-entry workspace. |
| `laboratory.html` | Report-processing and confirmation workspace. |
| `mobile/index.html` | Separate responsive patient entry. |
| `wireframes.css` | Responsive light/dark interface styles. |
| `wireframes.js` | File/camera handling and service-backed screens. |
| `service/server.py` | Loopback HTTP API, SQLite storage and reviewed-value extraction. |
| `service/recognize.swift` | PDFKit text extraction and Apple Vision OCR. |
| `check-wireframes.cjs` | Isolated end-to-end checks and empty-record screenshots. |
| `exports/` | Light/dark desktop and mobile review images. |
