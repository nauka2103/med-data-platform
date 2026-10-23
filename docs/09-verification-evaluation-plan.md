# Verification and evaluation plan

| Item | Value |
| --- | --- |
| Project | Intelligent Medical Platform |
| Work item | [MDP-8 — Verification and evaluation plan](https://nauka11.youtrack.cloud/issue/MDP-8) |
| Milestone | M1 pre-defense-1; 24 October 2026 |
| Document date | 24 October 2026 |
| Evaluation owner | Yerkin Yerassyl, ML lead |
| Requirements baseline | [MDP-5 — Requirements and acceptance criteria](06-requirements.md) |
| Scope baseline | [MDP-1 — Project proposal](01-proposal.md) |
| Scenario reference | [MDP-7 — UX wireframes](08-ux-wireframes.md) |

## 1. Purpose and acceptance boundary

This plan defines how the final prototype will be verified and how its extraction, summarization, trend analysis, performance and usability will be measured. M1 delivers the plan. Dataset generation, baseline implementations, evaluation scripts and experimental results belong to later implementation and evaluation tasks, including MDP-23, MDP-24, MDP-25, MDP-29 and MDP-30. No experimental result or participant finding is claimed here.

All numeric thresholds from MDP-1 and MDP-5 are retained. Dataset sizes beyond their minimums, matching rules, rating anchors and trend precision tolerance below are protocol decisions fixed before measurement. The local MDP-7 prototype may support design review, but its simulated access controls and local processing do not establish acceptance of the planned shared API or ML services.

Every Must criterion requires passing evidence. Record Should failures and deferrals with their effect on the project outcomes. Could features are tested if included; otherwise record them as deferred. A failed or unexecuted test cannot be reported as passed. Approval of this document does not approve an untested application.

## 2. Test levels and responsibilities

| Level | Scope and procedure | Owner and evidence |
| --- | --- | --- |
| Static review | Inspect requirements coverage, schema versions, fixture provenance, configuration, secret scan and CI configuration. | All contributors; review checklist and scan output. |
| Unit | Exercise pure range/trend rules, normalization, extraction matching, schema validation and consistency checking with fixed expected results. | Component author; machine-readable test results. |
| Integration | Exercise API, database, file store, worker, retrieval, audit and model adapter together, including failures and access denial. | Nauryzbay Nurkassymov with ML lead; request/response assertions, job traces and database checks. |
| End-to-end | Run S1 and S2 on web and mobile, S3 and S4 on web; compare persisted values across clients. | Asylzhan Bakytzhan; scenario outcomes and screenshots without credentials. |
| Quantitative evaluation | Compare extraction, summaries and alerts against fixed gold annotations and baselines; run timed workloads. | ML lead; manifests, raw outputs, scores and error analysis. |
| Participant evaluation | Observe S1/S2 task completion and collect SUS after use. | Asylzhan Bakytzhan; anonymous observations and questionnaire scores. |
| Release/recovery | Start from a clean checkout, replay required scenarios, interrupt processing and restart services. | Backend lead with a second team reviewer; setup log and persistence comparison. |

Mocks may exercise timeout and failure branches. Final ML quality and processing-time acceptance require the documented real model/OCR configuration. A contributor other than the component author reviews release evidence where possible.

## 3. Datasets, annotation and separation

Only authored synthetic records are permitted. No real patient records, hospital exports or personal medical documents enter these sets. Public datasets are not required by this plan; introducing one requires a documented provenance/access decision and a protocol revision before use.

| Dataset ID | Fixed composition | Purpose |
| --- | --- | --- |
| FUNC-v1 | Ten synthetic patients; four clinical/admin roles plus unauthenticated requests; own, assigned, unassigned and revoked relationships; populated and empty histories. | Functional, authorization, dashboard and cross-client checks. |
| DOC-DEV-v1 | 30 documents: ten each of laboratory reports, visit notes and discharge-style summaries. | Develop parsers, prompts, retrieval, rubric training and normalization. Never included in final quality scores. |
| DOC-TEST-v1 | 60 readable documents: 20 of each document type. Within each type: ten digital PDFs, five clean scans and five degraded but independently readable scans. | Held-out summary evaluation; the 20 laboratory reports also form the extraction test set. |
| DOC-FAIL-v1 | At least one fixture per condition: corrupt content, encrypted PDF, unreadable scan, unsupported content, extension/content mismatch, over-limit bytes and over-limit PDF pages. Also exact-limit and immediately-below-limit files. | Negative upload, OCR, timeout and no-publication checks. Excluded from the readable quality corpus by design. |
| TREND-DEV-v1 | 30 series, distinct synthetic patients from the test series. | Develop analytics and choose any learned-model parameters. |
| TREND-TEST-v1 | 120 series: 20 strictly rising, 20 strictly falling, 20 flat, 20 mixed, 20 with fewer than three distinct dates and 20 with an incompatible-unit interruption. | Held-out alert comparison, with anomaly labels defined below. |
| LOAD-v1 | 200 patients, each with 100 lab values, ten visits, ten prescriptions and ten document metadata records. | Dashboard latency benchmark. Source bodies need not be loaded for this endpoint workload. |
| TIME-v1 | 20 readable two-page reports: ten digital PDFs, five clean scans and five degraded readable scans; independent of DOC-DEV-v1. | Full extraction-plus-summary processing time. |
| USE-v1 | Separate synthetic accounts/documents for S1 and S2, with equivalent task variants per client. | Participant sessions; independent of model tuning. |

The development and test sets use different patient identities, source narratives and document template families. All rendered copies, scan variants and documents from one synthetic patient stay in one partition. DOC-TEST-v1 is authored from at least four laboratory template families, two visit-note families and two discharge-summary families absent from development. Laboratory reports contain at least ten rows each and jointly include missing fields, one-sided intervals, decimal commas, negative values and repeated analytes. Include English and Russian content in both development and test; balance the 60-document test set at 30 per language and report results separately. These are source-language tests, independent of optional UI localization.

Scans use fixed render settings: clean at 300 dpi; degraded at 150 dpi with recorded blur/rotation parameters. Two annotators must still be able to read each quality-test document independently. Include readable long documents up to the 20-page limit in DOC-TEST-v1. Do not remove a difficult document after seeing system output. Truly unreadable fixtures belong to DOC-FAIL-v1 before any evaluation.

Each manifest records dataset/version, generator revision and seed, document/patient ID, partition, template family, language, format, page count, scan parameters, SHA-256, provenance and eligibility. Use seed 20261024 for fixture generation and 20261025 for evaluation ordering. Record tool versions because a seed alone does not guarantee identical rendering. Store gold annotations separately from model inputs and retrieval indexes.

Two team annotators independently transcribe laboratory fields and mark source spans and key facts for the summary corpus. Resolve disagreements against the rendered source before freezing gold; retain initial labels and resolution notes. Gold includes absent fields explicitly. Freeze manifests, gold files, aliases, baselines, prompts and scoring code by Git revision/hash before opening test outputs. After test-driven changes, label the run exploratory; obtain a new held-out version for a new confirmatory claim. Reuse of a test set for regression must be disclosed.

## 4. Functional and security verification

For each row below, instantiate all acceptance criteria in MDP-5, with separate case IDs and fixtures for each boundary or failure condition. A row passes only when all its cases pass; the target for every row is 100% case pass rate and zero forbidden disclosures or mutations. Maintain a case inventory before execution so coverage cannot be improved by deleting failing cases.

| Case family | Requirement IDs | Procedure and expected evidence |
| --- | --- | --- |
| V-AUTH | FR-AUTH-1, FR-AUTH-2, FR-ADM-1 | Valid/invalid registration and login; duplicate and privileged-role requests; logout, expiry, account deactivation and assignment revocation. Enumerate every protected endpoint/method and file URL against four roles plus no session, with own/assigned/foreign records. Test lists, searches, nested IDs and direct downloads. Denials disclose no data and cause no mutation; administrator authority alone gives no clinical access. |
| V-PAT | FR-PAT-1, FR-PAT-2, FR-DASH-2 | Compare profile/timeline with gold; check date order, empty histories, author/patient IDs, invalid input and forbidden edits. Valid doctor-created visits/prescriptions appear after refresh within five seconds. Revocation blocks the next overview/source request. |
| V-LAB | FR-LAB-1, FR-LAB-2, FR-LAB-3 | Check draft/review/publish, editing and confirmation replay using a stable batch ID. Reject missing/non-finite fields and inverted limits. Check lower/upper boundaries, interior and exterior values, one/no limit, negative/decimal values, unit mismatches, zero/one/equal-date results and inclusive date filters. Chart and table exactly match published gold; drafts stay absent. |
| V-DOC | FR-DOC-1, FR-DOC-2 | Check actual file content, 10 MiB and 20-page boundaries, DOC-FAIL-v1, original retention and asynchronous job IDs. Observe uploaded/processing/ready or failed across refresh. Force OCR/model failure and processing beyond 120 seconds; no late result may publish after failure. Readable digital/scanned inputs expose source text and editable extraction drafts or explicit failure. |
| V-SUM | FR-SUM-1, FR-SUM-2, FR-SUM-3, FR-SUM-4 | Validate versioned schema, required metadata, AI label and per-item evidence. Absent source categories remain empty. Seed altered values, units, medication names and dates, including a misleading matching token elsewhere; each mutation must fail the consistency gate. Correct controls pass. Check invalid citations and unreadable inputs. Place another patient's canary in the retrieval store; it must appear in neither job context nor output. Check error-report version linkage and persistence. |
| V-CLIENT | FR-DASH-1, FR-UI-1 | Compare all dashboard fields/source links for ten patients. Run S1/S2 on both clients and verify cross-client persisted labs/documents after refresh. Run S3/S4 on web. Inspect loading, empty, error, denial and failed-processing states; primary patient controls remain usable at 360 pixels. |
| V-SEC | NFR-SEC-1, NFR-PRIV-1 | Verify adaptive salted hashes and different hashes for equal passwords; scan tracked files/history for credentials and real records. Send canary passwords/tokens/document and summary bodies and confirm absence from app logs. Inspect captured model requests for minimum authorized context. Confirm TLS on non-loopback connections and document any loopback HTTP setup. |
| V-AUD | NFR-AUD-1 | Exercise each protected read/write, download, denial and administrative mutation. Match actor/anonymous marker, time, action, resource, outcome and correlation ID to audit evidence. Test sink failure: durable audit or fail closed with no disclosure/mutation. Clinical roles cannot read/change/delete events; admin has read-only access. |
| V-OPS | NFR-AVL-1, NFR-MAINT-1 | Start database/API/worker/web from a clean checkout with documented configuration and real model access; follow separate mobile setup. Restart during processing; published data/files persist and interrupted work terminates ready or failed. CI runs lint and required authorization, boundary, job-failure and schema/consistency tests. A deliberately failing check must produce unsuccessful CI. |
| V-OPTIONAL | FR-EXP-1, NFR-I18N-1 | If included, verify own-record export and unauthorized denial, then language switching with unchanged dates/units/values and explicit source language. Otherwise record deferral. |

No role selector in a wireframe substitutes for API authorization evidence. For security negatives, assert payload absence and database/file-state invariance as well as the response code. Exact source spans, keys and hashes may appear in synthetic test evidence; credentials must be redacted.

## 5. Extraction evaluation

**Comparison.** Evaluate the proposed OCR/extraction pipeline against a rule-based baseline on the same 20 held-out laboratory reports. The baseline uses the same digital-text/OCR input, a development-frozen analyte alias dictionary and line/regular-expression rules for numbers, units, dates and limits, without an LLM. Missing matches stay empty. Freeze and record its code, regexes, OCR version and dictionary. Report an end-to-end result including OCR errors; an optional gold-text run isolates parser errors and is labelled separately.

**Scoring unit.** A gold report row has a stable row ID and source location, analyte, numeric value, unit, measurement date and separate lower/upper limits when supplied. The evaluator aligns predicted rows one-to-one within each document by source row/span overlap, then by normalized analyte and occurrence order for rows without spans. Break ties by reading order and never choose a match based on predicted value correctness. Freeze alignment code on development examples; retain alignment traces. Duplicate predictions cannot match the same gold field twice. Unmatched predictions are false positives; unmatched gold fields are false negatives.

**Normalization.** Apply Unicode NFKC and trim whitespace; collapse internal whitespace in labels and units. Use a frozen explicit analyte-alias map and case-sensitive unit-alias map; never infer unit conversion. Parse decimal commas only where the fixture locale specifies them; use exact decimal arithmetic, so 5.0 equals 5 but 5.1 does not. Preserve signs and inequality operators. Normalize unambiguous dates to ISO calendar dates; ambiguous dates remain missing unless the declared source format resolves them. Never substitute upload date for measurement date or infer a missing limit. Dates shared in a report header count once per row to which that header explicitly applies. A correct unsupported/missing field is not a true positive; a guessed value for an absent field is a false positive. Wrong nonempty values incur both FP and FN.

Aggregate TP, FP and FN over documents and the six field types before computing micro precision `TP/(TP+FP)`, recall `TP/(TP+FN)` and F1 `2TP/(2TP+FP+FN)`. This follows the global-count meaning of micro averaging in the [scikit-learn metric documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html). Set zero-denominator precision/recall/F1 to zero and flag the condition. A failed pipeline contributes every expected field as FN; it is not removed. Report raw counts and scores by field, template, language and scan quality.

**Gate E1:** proposed micro F1 must be at least 0.85 and strictly exceed the baseline's unrounded F1. Report paired per-document differences and a 95% percentile bootstrap interval from 2,000 paired document resamples, seed 20261025; the interval describes uncertainty and is not an additional acceptance threshold. Twenty synthetic lab reports support a prototype comparison, not a general clinical claim.

## 6. Summarization evaluation

Use all 60 DOC-TEST-v1 documents, exceeding the 30-document minimum in NFR-ACC-2. Generate and retain one final output per document and method under a frozen configuration; no manual selection of the best candidate.

| Method | Frozen procedure |
| --- | --- |
| B-SUM-EXTRACT | Split the same extracted source text into sentences; rank by matches to development-frozen finding/medication/diagnosis/recommendation headings and terms; break ties by source order. Select up to 250 words, preserving source order and source spans. Use the same language handling and publish the ranking dictionary. |
| B-SUM-NORAG | Use the same LLM version, structured schema, instructions and 250-word content budget as the proposed method, but supply the document text directly in reading order without retrieval or other patient context. Apply a frozen token cap and record truncation. |
| PROPOSED | Use the LLM with retrieval and structured output, restricted to the source document and explicitly authorized context; use the same output budget. Record retrieval chunks, top-k, embedding model, prompt, schema, consistency gate and any fixed repair policy. |

The primary comparison supplies no additional patient documents to any method, isolating retrieval over the target document. Test authorized multi-document context and isolation separately under V-SUM. For a document exceeding the LLM input budget, B-SUM-NORAG uses the start of the extracted text up to the recorded cap; PROPOSED uses retrieval within that same token budget. Report this stratum separately. Baselines retain raw outputs and violations; they are comparisons and do not have to pass the proposed system's publication gate.

Two raters independently assess every output against the source, with method labels hidden and order randomized per document using the recorded seed. Use project members or other competent readers who can read the source language; identify their roles and language competence in the report. They must not rate their own generated gold in isolation: both rate every document. Train them on DOC-DEV-v1 examples before the test. Use identical presentation and source access for all methods; stylistic cues may prevent complete blinding and must be disclosed.

| Faithfulness score | Anchor applied to the whole summary |
| --- | --- |
| 5 | All factual claims are supported by the cited source and correctly attributed; no change to meaning. |
| 4 | Core claims are supported; a minor imprecision does not change a value, identity, date, medication or source meaning. |
| 3 | At least one unsupported or misleading substantive statement changes part of the source meaning. |
| 2 | Multiple substantive errors or a central unsupported assertion make the summary unreliable. |
| 1 | Predominantly unsupported, contradictory, associated with the wrong patient, or unusable as a summary of this source. |

Any altered value, unit, medication or date caps the rating at 3 and is also recorded as an objective inconsistency. Raters record offending claims and source spans. An empty output on a document with gold key facts receives 1; source-supported omissions affect coverage separately. Compute each document's faithfulness as the mean of its two original ratings, then the overall arithmetic mean across the fixed 60 documents. Preserve independent ratings; record consensus/adjudication separately without replacing the acceptance scores. Report exact agreement and the number of documents whose ratings differ by at least two points; these are descriptive, without acceptance cutoffs.

Define a factual numeric claim as a number with its referent and, where present, unit/date. Compare it with its own cited passage, including entity/patient association. Token presence elsewhere is insufficient. Report the count of unsupported/altered numeric claims, all numeric claims reviewed, and documents with at least one such error. Review every output using both automated association-aware checks and the two raters. Report other factual errors separately. Citation coverage is the fraction of factual items with a valid source span; audit every factual item, not a sample.

**Gate S1:** all 60 eligible documents receive a ready, schema-valid proposed summary with an AI label and valid evidence for every factual item (100% schema/label/citation compliance); zero detected numeric inconsistencies; mean faithfulness at least 4/5. Any failed/missing job fails the gate, stays in the denominator and receives rating 1 for aggregate reporting. No rerun may silently replace a failure. A model repair policy may make at most one automatic repair attempt per job, must be frozen before evaluation and must retain both attempts; latency includes it.

Also report key-fact coverage: supported gold key facts represented divided by all gold key facts, micro-aggregated over the fixed corpus; target at least 80% for PROPOSED. Missing summaries contribute zero represented facts. This additional protocol target prevents empty or uninformative summaries from benefiting from a faithfulness-only metric. It does not relax NFR-ACC-2. Report per-method scores and paired document-level faithfulness/coverage differences; superiority over a summary baseline is an empirical question, not a preset claim. Use the same paired bootstrap procedure as E1 for faithfulness differences.

## 7. Trend evaluation and baseline tolerance

Separate two tasks: exact rising/falling rule correctness and comparative detection of informational attention events. Neither task predicts disease or recommends treatment.

For the rule test, sort by date and stable result ID, inspect the latest three published measurements of one analyte/unit, and require three distinct dates. Do not skip an intervening incompatible-unit reading to manufacture a compatible sequence. Strictly increasing values produce Rising; strictly decreasing values produce Falling; flat, mixed, insufficient-date and incompatible-window cases produce neither. Range flags remain independent. Target: 100% agreement with frozen rule labels across TREND-TEST-v1 and boundary fixtures, including duplicate dates.

For the comparison, use one terminal three-measurement window per series (or the available shorter window), so long series do not dominate. Gold attention label is positive if the latest value violates its own compatible supplied limit OR the window has a valid rising/falling pattern. Gold annotators apply this written definition before seeing predictions. Distribute range-positive and range-negative examples through each of the six strata, ten of each per stratum. Thus the 40 trend-positive series include 20 with trends still within supplied ranges. The other 80 series include 40 range violations and 40 negative controls. A unit interruption may still have a valid latest-value range flag; it must not produce a trend flag.

**Baseline B-TREND-RANGE:** flag only a latest-value supplied-range violation. **Proposed alert:** flag a range violation or the implemented trend detector's positive prediction. Score both on the identical 120 windows. Compute positive-class precision and recall from TP/FP/FN; if no alerts or no positives exist, report undefined with counts and fail comparison rather than treating it as success. Report per-stratum confusion matrices and rising/falling label errors separately.

**Gate T1:** proposed recall must be strictly greater than baseline recall, and proposed precision must be at least baseline precision minus 0.05 (five absolute percentage points). This is the predeclared meaning of “higher recall at similar precision” in MDP-1 and FR-LAB-4. Compare unrounded values. Report F1 and paired differences descriptively, with a paired bootstrap interval as in E1. Because the gold attention definition includes the same trend rule, this experiment verifies implementation and incremental coverage over range-only flags; it does not establish predictive ML benefit. A learned detector must still use this fixed test set and disclose training and tuning on TREND-DEV-v1 only.

## 8. Performance and recovery conditions

Record OS, CPU, RAM, GPU if used, power mode, container limits, service/dependency versions, Git revision, database indexes, model/provider version, region/network, decoding parameters, OCR configuration, worker count and cache state. Use a dedicated local run with no unrelated load. Credentials stay outside results. Measure durations with monotonic clocks in the harness; use UTC timestamps and correlation IDs for traces. Pin the serving configuration before running both benchmarks.

**Dashboard gate P1 (NFR-PERF-1).** Seed LOAD-v1. Warm the API with 100 authenticated dashboard requests, then issue 1,000 measured requests from ten concurrent clients, rotating deterministically over the 200 patients with authorized patient credentials. Include client-visible HTTP completion time and assert response correctness. Sort all 1,000 durations; nearest-rank p95 is the value at one-based rank `ceil(0.95 * 1000) = 950`. Target p95 strictly below 2,000 ms and zero unexpected responses/errors. Include failed-request elapsed times and counts; do not calculate an acceptance percentile only on successful requests. Record timeout at 10 seconds as a failed request. Report p50, p95, maximum and error count; p50/maximum are descriptive.

**Processing gate P2 (NFR-PERF-2).** Start a warm worker with one non-test document, then run the fixed 20 TIME-v1 reports sequentially with one active job. Time from the accepted upload response to the first observed ready status, polling at 250 ms; record server queue, extraction, retrieval, generation and gate durations as well. Every test job stays in the denominator. A failed job, missing ready status, timeout or completion after 60 seconds is not a timely success. Target at least 19/20 (95%) ready within 60 seconds; at 120 seconds of processing the timeout/failure rule of FR-DOC-1 must apply. Report provider throttling/network failures without excluding them. Forced-failure experiments are separate from this readable-set benchmark.

For both benchmarks, perform one preregistered acceptance run. Retain failed runs; a post-fix rerun receives a new run ID and revision and reports the reason. Optional repetitions assess variability and cannot be used to choose only the best result. For NFR-AVL-1 recovery, interrupt an active job and restart services; observe terminal state within 120 seconds of worker recovery, verify no duplicate publication and compare persisted lab/source/summary hashes. Also verify the five-second record-visibility bound in FR-PAT-2 with a timed refresh check.

## 9. Participant usability procedure

Recruit at least five adult volunteers who can read the selected interface language and have not developed the tested workflows. Use synthetic accounts only, obtain agreement to participate and retain anonymous IDs, client/device, prior familiarity and session observations. Do not collect personal medical histories. A small convenience sample supports formative findings rather than population-wide claims.

Each participant attempts S1 and S2 on both web and mobile: four assigned attempts per participant, at least 20 attempts overall. Counterbalance client order and use equivalent fixture variants so a repeated task does not reveal its answer. A short neutral introduction may explain the prototype's purpose but must not demonstrate task actions. Fix task text and fixtures before sessions. Start each task signed out; allow up to five minutes for S1 and seven minutes for S2, including processing time. Give no task-specific help during the scored attempt; record any requested/given help.

| Task | Endpoint for unassisted success |
| --- | --- |
| S1 — Review health status | Log in, locate the requested latest lab result, open its history, apply the requested dates and identify the displayed value/unit/date and supplied range correctly against the fixture. |
| S2 — Understand a document | Log in, upload the assigned readable report, observe ready status, open the AI-labelled summary and locate the cited source passage supporting the requested fact. |

Success requires every endpoint within the time limit without task-specific assistance. Wrong endpoints, abandonment, assistance, timeout and application failures count as unsuccessful attempts. Do not drop abandoned assigned attempts. Report success overall and by task/client; the gate is at least 80% of all assigned attempts. With five participants this requires at least 16 of 20. Report task time, help requests and observed problems descriptively without separate time-performance claims.

After both tasks on each client, administer the unchanged ten-item SUS questionnaire with responses 1–5. Following [John Brooke's SUS scoring procedure](https://digital.ahrq.gov/sites/default/files/docs/survey/systemusabilityscale%2528sus%2529_comp%255B1%255D.pdf), subtract one from each odd-item response, subtract each even-item response from five, sum the ten contributions and multiply by 2.5. Scores range from 0 to 100; they are not percentages. Average each participant's web/mobile SUS scores, then average participants; target at least 70. Report client means separately. Collect missing responses before the participant leaves without suggesting answers; if either questionnaire remains incomplete, retain that participant's tasks and mark the SUS gate unestablished rather than silently omitting the participant. No unreported imputation is permitted.

Keep raw item responses and task outcomes under anonymous IDs. Report participant count, recruitment method, full denominator, mean/range of SUS, completion counts and prioritized problems. Link later interface changes to the observations rather than inventing user findings at M1.

## 10. Metric and target register

All acceptance metrics are listed below. Counts, subgroup breakdowns, agreement, intervals and additional latency summaries are descriptive diagnostics, not independent gates.

| Metric | Target | Measurement and source |
| --- | --- | --- |
| Must case pass rate | 100%; zero forbidden disclosures/mutations | Fixed case inventory and V-AUTH through V-OPS evidence; MDP-5 Must criteria. |
| Doctor record visibility | At most five seconds | Save-to-refreshed-timeline elapsed time; V-PAT, FR-PAT-2. |
| Trend rule agreement | 100% | Prediction versus frozen rule labels; Section 7, FR-LAB-4. |
| Extraction micro F1 | At least 0.85 and strictly above rule baseline | Aggregate field TP/FP/FN on 20 held-out reports; E1, NFR-ACC-1. |
| Summary ready coverage | 100% of 60 eligible documents | Fixed manifest versus terminal jobs; S1, NFR-ACC-2. |
| Summary schema/AI-label/citation compliance | 100% of proposed outputs/items as applicable | Schema validator and full item/source audit; S1, FR-SUM-1/3. |
| Numeric inconsistencies | Zero detected | Automated plus independent human source-associated checks; S1, NFR-ACC-2. |
| Human faithfulness | At least 4/5 | Mean of raters per document, then all documents; S1, NFR-ACC-2. |
| Summary key-fact coverage | At least 80% | Supported represented gold facts / all gold facts; Section 6 protocol addition. |
| Trend alert recall | Strictly greater than range-only baseline | Paired binary predictions against attention labels; T1, MDP-1. |
| Trend alert precision | At least baseline precision minus 0.05 | Same test windows and unrounded scores; T1, FR-LAB-4 tolerance. |
| Dashboard latency/error rate | p95 below 2,000 ms; zero unexpected errors | 1,000 measured requests after 100 warm-ups, concurrency ten; P1, NFR-PERF-1. |
| Timely document completion | At least 19/20 within 60 seconds | Accepted-upload to ready, failures included; P2, NFR-PERF-2. |
| Processing timeout/recovery | 120-second processing timeout; terminal state within 120 seconds of recovery | Forced worker/late-result/restart checks; V-DOC/V-OPS. |
| Mean SUS | At least 70 | At least five participants, complete web/mobile questionnaires; Section 9, NFR-USE-1. |
| Unassisted task success | At least 80% | Successful / all assigned participant-task-client attempts; Section 9, NFR-USE-1. |

## 11. Run records, reporting and change control

Each execution receives a unique run ID and a directory in a future `evaluation/results/<run-id>/` package. The following are required outputs of evaluation work, not files claimed to exist at M1:

| Artifact | Minimum fields |
| --- | --- |
| Run manifest | Run ID, timestamp, executor, Git revision, dataset/gold/config hashes, seeds, environment, baseline versions, model/prompt/schema versions and protocol revision. |
| Functional cases | Case ID, requirement, fixture ID, precondition, action, expected result, actual result, pass/fail/not-run and evidence path. |
| Extraction results | Document/row/field IDs, gold, prediction, normalization, alignment, TP/FP/FN and subgroup labels. |
| Summary results | Document, anonymous method key, raw attempts, terminal state, citations, objective inconsistencies, two independent ratings, coverage and adjudication notes. |
| Trend results | Series/window ID, gold attention/direction, baseline prediction, proposed prediction and TP/FP/FN/TN. |
| Timing results | Request/job ID, durations, state, error, warm-up marker, queue/model times and workload configuration. |
| Usability results | Anonymous participant/client/task IDs, assignment, success, assistance, duration, ten SUS responses and notes. |
| Evaluation report | Target, actual value, denominator, baseline, interval if specified, gate decision, failure examples, limitations and reviewer. |

Before experiments, verify that fixture generators, gold annotations, scoring scripts and real model access exist and that all hashes are frozen. Before acceptance, a second team member reproduces metric aggregation from raw records and reviews requirement coverage. Do not replace missing experiments with example numbers. Record not-run/blocked results and their dependency explicitly.

Document-only acceptance for MDP-8 requires test levels, datasets, conditions, baselines, targets and measurement methods for each acceptance metric; Sections 2–10 provide them. Final application acceptance remains subject to actual evidence. Later implementation tasks create the executable harnesses; do not imply a command is available until it has been implemented and verified.

Changing a dataset, threshold, normalization rule, prompt, rubric, endpoint inventory or baseline after unblinding requires a dated amendment with rationale, affected requirements and reviewer decision in the repository review and MDP-8. Retain previous runs and distinguish exploratory results from a fresh held-out evaluation. Report synthetic-template bias, small participant/rater samples, language coverage, model nondeterminism and provider/network dependence in the final thesis.
