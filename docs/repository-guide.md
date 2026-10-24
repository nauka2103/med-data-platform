# Repository structure and configuration policy

Work item: [MDP-9 — README, repository structure, .gitignore, config examples](https://nauka11.youtrack.cloud/issue/MDP-9).

## Current layout

The root [README](../README.md) is the entry point for setup, configuration, verification, team information and documentation links. [CONTRIBUTING.md](../CONTRIBUTING.md) defines branch, identity, review and publication rules.

| Location | Contents and ownership boundary |
| --- | --- |
| `docs/` | Versioned engineering documents. Preserve existing numbered filenames and requirement IDs; add descriptive names for repository guidance. |
| `diagrams/` | Architecture DOT sources and tracked PNG/SVG renders. |
| `mockups/` | Existing HTML/CSS/JavaScript local workspace and its launch instructions. The name is retained to preserve links and commands. |
| `mockups/mobile/` | Responsive patient web entry; not a native mobile project. |
| `mockups/service/` | Python loopback HTTP service and Swift OCR/PDF helper source. |
| `mockups/exports/` | Reviewed, empty-record interface screenshots intentionally tracked for the UX deliverable. |
| `.env.example` | Trackable, credential-free example of the actual local service setting. |
| `.env`, `.local-data/`, `data/`, `uploads/`, `storage/` | Ignored local configuration or runtime paths; never repository deliverables. |

The service defaults to runtime storage outside the checkout at `~/Library/Application Support/MedDataPlatform`. That directory contains `workspace.sqlite3`, uploaded originals under `files/` and the compiled `recognize` helper. Exporting `MDP_DATA_DIR` selects another absolute directory. Use an ignored location if placing it inside the checkout; do not place runtime data in `docs/` or `mockups/exports/`.

## Future application components

The proposal describes FastAPI, PostgreSQL, a React/TypeScript web client, a React Native/Expo client, Python ML services and Docker Compose. These components are not scaffolded by this documentation task. Add their source directories, dependency manifests, environment examples and runnable commands together when their implementation tasks begin, updating the root tree in the same change. Do not present empty directories or speculative commands as a working deployment.

The pre-defense integration candidate includes research, technology and architecture documents together with requirements, UX and evaluation material. Original feature branches remain provenance records. Historical branch links inside the imported documents refer to those original snapshots. The submission record tracks the review and tag gates; presence in this checkout does not establish review approval.

## Configuration and data handling

The current service consumes only `MDP_DATA_DIR` from its environment and `--port` from its CLI. `.env.example` documents the supported variable without adding unused database, JWT or model-provider settings. The service does not read dotenv files itself; the root README explains how to export the shell-compatible example. Future credentials must have clearly documented, non-secret examples when their consumers are implemented.

Root `.gitignore` covers environment files, common private-key containers, local record directories, SQLite databases, dependency directories, build/test output, Python caches and editor/OS files. `.env.example` is explicitly allowed. This is preventive filtering rather than a secret-scanning guarantee: tracked files and Git history still need review before publication. Do not blanket-ignore PDF or image extensions because synthetic research artifacts and reviewed interface exports may be intentional deliverables.

## Acceptance review

1. README covers project purpose/status, prerequisites, installation/startup, configuration, the actual source tree, documentation, verification, troubleshooting, contribution/team information and license status.
2. Every relative link resolves in the checkout, and every documented current source location exists.
3. The example contains only a supported setting, can be exported with the documented shell commands and remains trackable.
4. Ignore checks cover private configuration, nested environment files, runtime records, databases, caches and dependency/build output while retaining intended source and screenshots.
5. Review staged content and run a secret scan before publication; do not claim that ignore rules prove the absence of credentials.
6. Complete identity confirmation and review approval before commit/push, then verify remote publication and the automatic YouTrack transition.
