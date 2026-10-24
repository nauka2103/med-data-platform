# Pre-defense 1 submission record

Preparation date: 24 October 2026. Repository: [Medical Data Platform](https://github.com/nauka2103/med-data-platform).

## Version and release status

Submission candidate: [pre-defense-1](https://github.com/nauka2103/med-data-platform/tree/pre-defense-1), prepared on branch `pre-defense-1-integration`. The annotated tag identifies the exact submitted package and must not be moved or replaced. Publication of a tag does not establish teammate or supervisor approval.

Publication sequence: confirm the active contributor and approve the diff; commit and push the candidate; publish the annotated tag; create `main` from the existing proposal baseline and open the integration PR against it. The version link becomes available when the tag push succeeds.

Remaining review gates:

1. Obtain a recorded review from another team member and address findings before merging into `main`.
2. Keep `main` as the reviewed baseline. Creating its initial proposal base does not establish review of this integration.
3. If review requires content changes, publish a new version tag rather than moving `pre-defense-1`.
4. Select `main` as the default branch using a repository administrator if the contributor lacks permission.

The PR and eventual merge commit are discoverable in GitHub history. This record does not assert a review approval or completed merge.

## Included work

| Area | Submitted material |
| --- | --- |
| Problem, scope and expected outcomes | [Proposal](01-proposal.md) and [README](../README.md). |
| Literature | [Critical review](03-literature/README.md) and [references](03-literature/references.md): 14 publications, 12 in the defined five-year window. |
| Alternatives | [Four-system comparison](02-existing-systems-comparison.md) and [technology decisions](03-technology-comparison.md). |
| Minimum functional and quality requirements | [Requirements and acceptance criteria](06-requirements.md), priorities and provisional research clarifications. |
| Architecture | [Architecture](04-architecture.md), three editable DOT diagrams with PNG/SVG renders in [diagrams](../diagrams/). |
| Interfaces and runnable demonstration | [UX specification](08-ux-wireframes.md), [local workspace](../mockups/README.md) and empty-record screenshots. |
| Verification plan | [Evaluation protocol](09-verification-evaluation-plan.md), baselines, metrics and evidence requirements. |
| Feedback preparation | [Supervisor review packet](10-supervisor-review.md), generated findings and linked follow-up work. |
| Research preparation | [Four simulated interviews](11-user-interviews.md), [survey report](12-survey.md) and [normalized export](research/mdp-12/survey-responses.json). |
| Delivery and team coordination | [Contribution rules](../CONTRIBUTING.md), [repository guide](repository-guide.md), README responsibilities and [management plan](project-management.md). |

The existing runnable demonstration provides local upload, OCR/PDF extraction, deterministic laboratory parsing, source review and persistence. Its implementation is smaller than the planned shared platform. No new application behavior is introduced by this integration.

## Limitations and remaining work

- The current macOS service is a single local record. FastAPI/PostgreSQL, account and record authorization, audit logging, a native mobile application, shared deployment and retrieval-assisted summaries remain planned work.
- Evaluation thresholds are targets. The existing browser check does not establish clinical effectiveness, extraction F1, summary quality, SUS scores or completion of every Must requirement.
- Final academic submission still needs actual supervisor/client discussion evidence, independent PR review and the published reviewed version. Full application implementation is later work, tracked by MDP-13–31.
- No license has been granted by the README. Repository administrator permission is needed to change the default branch.

See [project management](project-management.md) for owners, dependencies and risk responses.

## Integration provenance

The candidate uses the MDP-12 tip as its starting tree. It imports the literature, comparisons, architecture and supervisor packet from their published branches, preserving source files and commit ancestry. README and repository guidance are reconciled for the combined checkout. Original documents retain valid historical snapshot links; they need not describe the current integration branch.

| Published source branch | Frozen commit |
| --- | --- |
| `MDP-1-project-proposal` | `7b71fbdfb1161ed0e8a993fd1e07cdade92ddb78` |
| `MDP-2-literature-review` | `5ddbba4508cacfa1e816d170aeadff89499759a0` |
| `MDP-3-existing-systems-comparison` | `0d99f30ed1e87f47fb8d45a2e6e16f740db0f871` |
| `MDP-4-technology-comparison` | `2a35a58d34c10e4a5ee141bb7f8b99911fcfbeba` |
| `MDP-5-requirements-specification` | `dbc7bd494a214f10adacbbcf0761b6ae575d8d30` |
| `MDP-6-architecture-diagrams` | `83cba5885bb70a1a197d90c23eda6f0a037260ba` |
| `MDP-7-ux-wireframes` | `0d6b64b2109cbfa79c0b92b68fa918ba05f7c7d1` |
| `MDP-8-verification-evaluation-plan` | `6c65fb43f54c7edc04e55ae1b3e1328cfac6555f` |
| `MDP-9-repository-setup` | `55a3efda749ef26ffb8f49d3a276c340661d6190` |
| `MDP-11-supervisor-review` | `89f16fc339a28c7f69ded66f35710a1c608f8673` |
| `MDP-12-user-interviews` | `d0c023da9bf979395226819d23c800568088ff8f` |

## Verification record

Checks executed on 24 October 2026:

| Check | Result |
| --- | --- |
| Imported branch content | Literature, system/technology comparisons, architecture and supervisor packet match their published source blobs exactly. |
| Local Markdown file links | 137 checked, none missing. |
| DOT diagrams | All three parse and render successfully with Graphviz; tracked renders preserved. |
| Whitespace | `git diff --check` passes. |
| Private-file exclusions | `.env`, local database and uploads ignored; `.env.example` remains trackable. |
| Limited credential-pattern scan | 50 candidate files checked for private-key headers, GitHub token and AWS access-key patterns; no matches. This is not a comprehensive secret audit. |
| Existing browser verification | Passed using installed Chrome, bundled Node/Python and isolated synthetic fixtures: PNG/PDF upload, OCR/PDF extraction, source review, validation, persistence/restart, duplicate prevention, clinician/lab pages, notes, camera dialog, themes, responsive layouts and origin/file checks. No application source changed. |

The first browser launch could not find Playwright's downloaded Chromium; rerunning with the installed Chrome executable passed. Two regenerated screenshot files differed and were restored to their published originals to keep this integration focused on documentation. The source branches and release state must be rechecked before publication if they change during review.
