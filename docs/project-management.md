# Project management plan

## Responsibilities and workflow

The [README responsibility table](../README.md#team-and-contribution) names each contributor and the current division of work. The [YouTrack backlog](https://nauka11.youtrack.cloud/issues?q=project:%20MDP) is authoritative for individual assignments, priorities and acceptance criteria. Each contributor uses their own account; repository ownership is not evidence of authorship.

The integration author assembles the candidate and records verification. A different team member reviews the PR for completeness, reproducibility, evidence claims and accidental private data. The authorized maintainer merges only after that review and creates the immutable release tag from the merged commit. The supervisor reviews academic scope and deliverables separately; a teammate PR approval does not establish supervisor approval.

## Milestones and dependencies

| Milestone | Deliverable / exit condition | Dependencies and ownership |
| --- | --- | --- |
| M1, pre-defense 1 — 24 October 2026 | Proposal, literature and system/technology comparisons, requirements, architecture, UX, evaluation plan and repository package; reviewed main and version tag. | All contributors; actual review/access/research evidence remains subject to the submission limitations. |
| Service foundation | Backend/CI, schema, login and role/record authorization. | Nauryzbay: MDP-13–15; agreed requirements and architecture. |
| Records and clients | Labs API, dashboard API, upload/storage and web/mobile entry points. | Nauryzbay and Asylzhan: MDP-17–22; service foundation. |
| Processing and analytics | Synthetic fixtures, OCR/extraction, source-linked summaries and trends. | Yerkin: MDP-16, MDP-23–25; uploads, schema and fixed evaluation inputs. |
| Integrated prototype | Mobile screens, doctor view and audit/security hardening. | Asylzhan and Nauryzbay: MDP-26–28; APIs, authorization and processing. |
| Evaluation and thesis | Controlled experiments, usability study and final report. | Yerkin and Asylzhan: MDP-29–31; stable prototype and evaluation protocol. |

Later milestone dates are not established by this plan. Use agreed YouTrack deadlines rather than treating this sequence as a committed calendar. MDP-10 still requires confirmation of supervisor access and backlog readiness.

## Risks and responses

| Risk | Consequence | Response / owner |
| --- | --- | --- |
| Simulated interviews and automated survey profiles mistaken for participant research | Unsupported requirements validation | Preserve provenance labels; conduct real consented sessions and revise provisional findings. Yerkin, with all contributors. |
| Generated supervisor comments mistaken for actual approval | Submission lacks verifiable academic review | Obtain dated supervisor feedback and record each decision/task. Asylzhan coordinates MDP-11. |
| Local prototype mistaken for the planned platform | Overstated implementation status | Keep implemented/planned boundaries in README; require task acceptance evidence. All contributors. |
| OCR errors, units and reference ranges | Incorrect structured records | Source review and manual confirmation; fixed synthetic evaluation set and failure cases. Yerkin. |
| Missing role/record authorization | Inappropriate access if deployed beyond local use | Keep current service on loopback; implement and test MDP-15/28 before shared deployment. Nauryzbay. |
| Integration or release without independent review | Incomplete or unreviewed baseline | Require another team member's recorded PR review before merge/tag. Integration author and reviewer. |
| Private records or credentials published | Disclosure | Synthetic fixtures, isolated storage, diff and secret review before publication. All contributors. |
| Scope exceeds available time | Incomplete cross-client implementation | Implement Must requirements first; track deferrals and dependencies explicitly. All contributors. |

## Change control

Preserve requirement IDs and acceptance criteria. Link requirement changes to evidence, a decision and a task; generated research supplies provisional design hypotheses only. Track deferred work in YouTrack. Record the final submission version and unresolved limitations in the [submission record](pre-defense-1.md). No performance or usability target is considered met merely because its plan is present.
