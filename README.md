# Medical Data Platform

An academic prototype for organizing patient records, reviewing laboratory results and structuring medical documents. The planned platform includes a web client, a native mobile client, a shared API and machine-learning services. See the [project proposal](docs/01-proposal.md) for the problem, scope and success criteria.

## Problem, users and expected outcomes

Patients need a consistent view of fragmented laboratory reports and medical documents. Doctors need traceable results and source documents; laboratory staff need a structured upload and correction workflow. The planned outcome is a shared web/mobile platform with patient records, document processing and measurable extraction and summary quality. The current outcome is the local workspace and the M1 engineering package described below.

## Project status and features

This branch contains the M1 documentation and a working macOS local document workspace:

- Separate patient, clinician, laboratory and responsive mobile web pages.
- PDF, JPG and PNG upload, camera capture, digital PDF text extraction and Apple Vision OCR.
- Deterministic extraction of supported laboratory rows, source review, manual corrections and supplied reference-range flags.
- Persistent local documents, reviewed results, notes and light/dark theme selection.

The current workspace uses Python's standard library, SQLite, Swift, PDFKit and Apple Vision with HTML/CSS/JavaScript clients. It serves one local record belonging to the OS user. Separate page URLs do not provide authenticated role isolation. Native React Native/Expo, FastAPI, PostgreSQL, Docker Compose deployment, account/record authorization, audit logging and retrieval-assisted LLM summarization remain planned application work. The mobile page currently provided is responsive web UI.

Use synthetic records for development, demonstrations and evaluation. The prototype does not generate diagnoses or treatment recommendations, and its evaluation does not establish clinical effectiveness.

## Prerequisites

- macOS with Xcode or Apple's command-line developer tools, including `xcrun swiftc`, PDFKit and Vision.
- Python 3.10 or newer, available as `python3`. No external Python packages are required by the local service.
- A browser with JavaScript enabled; camera capture requires browser permission.
- Optional browser verification: Node.js 18 or newer, Playwright and a Chromium browser.

The local OCR service requires macOS. The planned cross-platform service stack is not yet runnable from this branch.

## Installation and quick start

```bash
git clone https://github.com/nauka2103/med-data-platform.git
cd med-data-platform
git switch pre-defense-1-integration
python3 --version
xcrun --find swiftc
python3 mockups/service/server.py
```

The first run compiles the recognition helper into the runtime data directory. Open one of these pages after the service reports that it has started:

| Workspace | Address |
| --- | --- |
| Patient | <http://127.0.0.1:8765/index.html> |
| Clinician | <http://127.0.0.1:8765/doctor.html> |
| Laboratory | <http://127.0.0.1:8765/laboratory.html> |
| Mobile patient web page | <http://127.0.0.1:8765/mobile/index.html> |

Stop with Ctrl+C. To choose another port, run `python3 mockups/service/server.py --port 8767` and use that port in the URLs. Opening HTML files directly or running a static-only server does not enable document processing.

For a first check, upload a synthetic PDF/JPG/PNG, wait for recognition, inspect the original and extracted fields, verify the date and reference limits, then confirm the reviewed results. Supported uploads are at most 10 MiB; PDFs must be readable, unlocked and at most 20 pages. Detailed workflows and limitations are in the [workspace guide](mockups/README.md).

## Configuration

Default startup needs no `.env` file or model API key. To customize storage:

```bash
cp .env.example .env
# Edit the trusted local .env file if needed, then export its settings:
set -a
. ./.env
set +a
python3 mockups/service/server.py
```

The service reads the process environment and does not automatically load `.env`. The example uses shell syntax and is intended to be sourced in Bash or Zsh.

| Setting | Default | Effect |
| --- | --- | --- |
| `MDP_DATA_DIR` | `~/Library/Application Support/MedDataPlatform` | Stores the SQLite database, uploaded originals, recognized text and compiled OCR helper. Set an absolute path in an exported variable. |
| `--port` | `8765` | Command-line argument for the local HTTP port; not an environment variable. |

The host is fixed to `127.0.0.1`. The current service does not support database URLs, external model keys or network binding through configuration. Changing the data directory selects a different workspace and does not migrate existing records.

## Repository structure

```text
.
├── README.md                     # Project entry point and setup
├── CONTRIBUTING.md               # Branch, review and commit workflow
├── .gitignore                    # Configuration, runtime and build exclusions
├── .env.example                  # Supported local configuration example
├── docs/
│   ├── 01-proposal.md
│   ├── 02-existing-systems-comparison.md
│   ├── 03-literature/
│   ├── 03-technology-comparison.md
│   ├── 04-architecture.md
│   ├── 06-requirements.md
│   ├── 08-ux-wireframes.md
│   ├── 09-verification-evaluation-plan.md
│   ├── 10-supervisor-review.md
│   ├── 11-user-interviews.md
│   ├── 12-survey.md
│   ├── pre-defense-1.md            # Submission scope and release gates
│   ├── project-management.md       # Responsibilities, milestones and risks
│   └── repository-guide.md        # Directory ownership and growth rules
├── diagrams/                     # DOT sources and PNG/SVG architecture views
└── mockups/
    ├── README.md
    ├── index.html                # Patient workspace
    ├── doctor.html
    ├── laboratory.html
    ├── mobile/index.html         # Responsive patient web page
    ├── wireframes.css
    ├── wireframes.js
    ├── start.command             # macOS launcher
    ├── service/
    │   ├── server.py             # Local HTTP API and SQLite storage
    │   └── recognize.swift       # OCR and PDF text extraction
    ├── check-wireframes.cjs       # Existing browser verification
    └── exports/                  # Empty-record interface screenshots
```

This integration candidate consolidates the published M1 branches. The quick start selects the candidate branch; the final `pre-defense-1` tag is reserved for the version merged after teammate review. See the [submission record](docs/pre-defense-1.md) for release status and evidence limitations. See the [repository guide](docs/repository-guide.md) before adding application components or generated files.

## Documentation

| Document | Purpose |
| --- | --- |
| [Proposal](docs/01-proposal.md) | Aim, users, scope, planned stack and outcomes. |
| [Literature review](docs/03-literature/README.md) | Critical analysis and verified bibliography. |
| [Existing systems](docs/02-existing-systems-comparison.md) | Comparison of four systems against nine criteria. |
| [Technology decisions](docs/03-technology-comparison.md) | Alternatives and selection rationale. |
| [Architecture](docs/04-architecture.md) | Context, use cases and components with diagram sources. |
| [Supervisor review preparation](docs/10-supervisor-review.md) | Generated review findings and proposed decisions; actual supervisor review remains unverified. |
| [Submission record](docs/pre-defense-1.md) | Included work, limitations, outstanding tasks and version publication gates. |
| [Project management](docs/project-management.md) | Named responsibilities, milestones, dependencies and risks. |
| [Requirements](docs/06-requirements.md) | Functional/non-functional requirements, priorities and acceptance criteria. |
| [UX wireframes](docs/08-ux-wireframes.md) | Interfaces, scenarios and implementation boundaries. |
| [Verification and evaluation plan](docs/09-verification-evaluation-plan.md) | Fixed evaluation procedures, baselines and evidence requirements. |
| [Simulated user interviews](docs/11-user-interviews.md) | Four fictional sessions, evidence boundaries and provisional requirement clarifications. |
| [Survey response report](docs/12-survey.md) | Supplied 51-row export, questionnaire, descriptive results and data-quality decisions. |
| [Local workspace](mockups/README.md) | Upload, review, storage and browser checks. |
| [Repository guide](docs/repository-guide.md) | Source layout, generated artifacts and configuration policy. |
| [Contribution workflow](CONTRIBUTING.md) | Branches, identities, review and YouTrack commands. |

The [YouTrack project backlog](https://nauka11.youtrack.cloud/issues?q=project:%20MDP) tracks assignments and completion. This repository setup corresponds to [MDP-9](https://nauka11.youtrack.cloud/issue/MDP-9).

## Verification

For documentation/configuration changes, review links and the actual directory tree, then run:

```bash
git diff --check
git status --short
git check-ignore .env .local-data/workspace.sqlite3 uploads/example.pdf
git check-ignore .env.example
```

The first ignore check should print all three private paths. The last command should print nothing and exit with status 1: the example must remain trackable. Ignore rules do not remove files already tracked; inspect the proposed diff and use an approved secret scanner before publication. Do not print credential values in review output.

The existing functional browser check uses isolated temporary storage and synthetic fixtures. Install its optional dependencies outside this repository:

```bash
npm install --prefix "$HOME/.local/share/mdp-browser-check" playwright
"$HOME/.local/share/mdp-browser-check/node_modules/.bin/playwright" install chromium
NODE_PATH="$HOME/.local/share/mdp-browser-check/node_modules" node mockups/check-wireframes.cjs
```

The check uses port 8766, exercises OCR, PDF extraction, review, persistence, access restrictions and responsive layouts, and regenerates eight screenshots in `mockups/exports/`. It checks a camera dialog; physical camera quality needs manual testing. If using an installed Chrome instead, set `CHROME_PATH` to its executable. `PYTHON` can select the Python executable used by the check. These variables configure the check, not the application. Full prototype acceptance is defined in the evaluation plan; a passing local check does not satisfy all planned requirements.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `xcrun` or `swiftc` is missing | Install/select Apple's developer tools, then rerun `xcrun --find swiftc`. |
| Address already in use | Stop the other local service or start with `--port 8767`. |
| `.env` changes have no effect | Export the file's values in the same shell before starting the service. |
| Recognition fails or produces no fields | Use a readable supported synthetic document; inspect recognized text and the supported formats in the workspace guide. |
| Playwright cannot be found | Install the optional dependencies and set `NODE_PATH` as shown above. |

## Team and contribution

Team: Yerkin Yerassyl, Nauryzbay Nurkassymov and Asylzhan Bakytzhan. Supervisor: Myrzakerimova Alua. The working responsibility allocation follows the existing backlog; individual YouTrack assignments remain authoritative.

| Contributor | Responsibility | Related tasks |
| --- | --- | --- |
| Yerkin Yerassyl | Research, document intelligence and evaluation; requirements feedback analysis. | MDP-1, MDP-2, MDP-8, MDP-12, MDP-16, MDP-23–25, MDP-29, MDP-31 |
| Nauryzbay Nurkassymov | Architecture, backend, data model, authentication, storage and operations. | MDP-3, MDP-4, MDP-6, MDP-10, MDP-13–15, MDP-17, MDP-20, MDP-22, MDP-28 |
| Asylzhan Bakytzhan | UX, requirements specification, repository setup, web/mobile interfaces and usability. | MDP-5, MDP-7, MDP-9, MDP-11, MDP-18–19, MDP-21, MDP-26–27, MDP-30 |
| Myrzakerimova Alua | Academic supervision and feedback on scope and evidence. | Supervisor review; no approval is asserted by this allocation. |

See the [project management plan](docs/project-management.md) for dependencies and release responsibilities. Repository documentation, commit messages and tracker deliverables are written in English. See [CONTRIBUTING.md](CONTRIBUTING.md) for the review and publication process.

## License

No license file is currently included. Reuse permissions must be agreed with the project owners; this README does not grant a license.
