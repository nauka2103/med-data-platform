# Medical Data Platform survey: exported response report

| Item | Value |
| --- | --- |
| Work item | [MDP-12 — User research](https://nauka11.youtrack.cloud/issue/MDP-12) |
| Report date | 24 October 2026 |
| Instrument | Medical Data Platform survey, Q01–Q17 |
| Source | Team-supplied response export; source PDF is not included in this repository |
| Exported records | 51 response rows; 17 questions plus submission timestamp |
| Response provenance | 50 matched automated test profiles and one additional submission of unverified provenance |
| Companion data | [Transcribed and normalized responses](research/mdp-12/survey-responses.json) |
| Related qualitative material | [Interview report](11-user-interviews.md) |

## 1. Source and scope

This report documents the supplied response export. It confirms that the PDF contains response records; it does not independently verify the live Google Form, account, consent, respondent identity or recruitment. The PDF contains no form URL, per-row provenance field or response identifiers. The descriptive title alone is not used as proof of participant provenance.

The first 50 rows match the earlier prepared automated test dataset across every Q01–Q17 answer after ordinal-label normalization: 850 matching question values, including blank role-specific fields and optional comments. These rows are automated test responses. A later 51st row is retained as an additional submission with unverified provenance. It is not assumed to be a recruited human participant or counted as a completed interview.

The first 50 timestamps run from 24 October 2026, 05:41:03 to 05:42:00. The additional row is stamped 05:50:56 on the same date. Times are transcribed as printed; the source does not specify a timezone. Submission timing does not establish consent, identity or independent participation.

The original PDF is retained outside the repository. Its transcribed values and displayed timestamps are preserved in the companion JSON; the report and derived data keys are in English. Source SHA-256: `f330b985eb39643ec944063a7d7f3ed0395884349ada275cc199519adcbb1965`.

## 2. Extraction and data quality

The source is a dense spreadsheet export scaled onto one page. Headers are visually crowded, so values were extracted by their table cell coordinates, not by splitting plain text on spaces. The 18 column boundaries were recovered from clustered vertical table edges. Timestamp positions identified the 51 data rows. The questionnaire wording below is taken from the existing instrument; the PDF column order and available headers were checked against it.

Numeric scale labels such as `5 — Very important` become the integer `5` in normalized answers. Original displayed answer labels and timestamps remain in `raw_answers` and `submitted_at_display`. Blank conditional fields become null; blank optional comments remain empty strings. Derived `PDF-R001`–`PDF-R051` IDs identify export rows, not people. `source_row` includes the table header, so PDF-R001 corresponds to table row 2.

| Check | Result |
| --- | --- |
| Export row count | 51, excluding the header. |
| Question columns | All 17 retained, including blank conditional answers. |
| Automated data comparison | First 50 rows match all 850 Q01–Q17 values in the earlier test dataset. |
| Additional response | PDF-R051 retained separately; provenance is unverified. |
| Role consistency | PDF-R051 selects Patient in Q01 but also answers doctor-only Q15 with 4. |
| Role-specific analysis | Preserve the Q15 value in raw/normalized data; exclude it only from doctor-specific calculations. |
| Optional comments | 41 non-empty comments out of 51 rows. |
| Record-level identity and consent | Not evidenced by this export. |

The derived `role_valid_answers` view sets answers outside the declared role to null. Each affected row retains a quality flag. No source response is deleted or silently corrected.

## 3. Composition of exported rows

These counts describe records, not verified participants. The first 50 role counts were set by the test generator; they are not a recruitment outcome.

| Declared role | Exported count | Share of 51 |
| --- | --- | --- |
| Patient | 35 | 68.6% |
| Doctor | 9 | 17.6% |
| Laboratory specialist | 7 | 13.7% |

| Preferred device | Exported count | Share of 51 |
| --- | --- | --- |
| Phone | 24 | 47.1% |
| Computer | 22 | 43.1% |
| Tablet | 4 | 7.8% |
| No preference | 1 | 2.0% |

## 4. Descriptive results

Percentages are rounded to one decimal place and may not sum to exactly 100%.

The following high-rating counts separate known automated tests from the unverified additional row. The all-export column is provided for reconciliation only. It is not evidence of user demand or population preference.

| Item, ratings 4–5 | Automated test profiles | Additional row | All exported rows |
| --- | --- | --- | --- |
| Q07 — Interest in trying the platform | 29/50 (58.0%) | 1/1 | 30/51 (58.8%) |
| Q09 — Willingness to use an AI summary as a reading aid | 21/50 (42.0%) | 1/1 | 22/51 (43.1%) |
| Q11 — Importance of source inspection | 41/50 (82.0%) | 1/1 | 42/51 (82.4%) |

### First feature priority, Q08

| Feature | Exported count | Share of 51 |
| --- | --- | --- |
| Lab history and charts | 6 | 11.8% |
| Document storage and search | 8 | 15.7% |
| Source-linked summaries | 5 | 9.8% |
| Upload and extraction review | 11 | 21.6% |
| Access controls | 10 | 19.6% |
| Mobile access | 9 | 17.6% |
| No new platform needed | 2 | 3.9% |

### Main concern, Q10

| Concern | Exported count | Share of 51 |
| --- | --- | --- |
| Incorrect information | 9 | 17.6% |
| Privacy or access | 15 | 29.4% |
| Extra work | 3 | 5.9% |
| Difficult interface | 9 | 17.6% |
| Service availability | 8 | 15.7% |
| No major concern | 7 | 13.7% |

### Ordinal response distributions

Each count column represents the selected 1–5 response. Endpoint meanings differ by question and appear in the instrument below. Medians describe these export rows only. Doctor-only Q15 excludes the out-of-role value in PDF-R051; its denominator is nine doctors, not ten non-empty cells.

| Item | Applicable group | Valid answers | 1 | 2 | 3 | 4 | 5 | Median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q05 | All exported rows | 51 | 7 | 12 | 14 | 11 | 7 | 3 |
| Q07 | All exported rows | 51 | 2 | 9 | 10 | 18 | 12 | 4 |
| Q09 | All exported rows | 51 | 7 | 4 | 18 | 14 | 8 | 3 |
| Q11 | All exported rows | 51 | 1 | 4 | 4 | 11 | 31 | 5 |
| Q14 | Only Patient | 35 | 1 | 6 | 12 | 8 | 8 | 3 |
| Q15 | Only Doctor | 9 | 0 | 1 | 6 | 2 | 0 | 3 |

### Offline access and interface language

| Offline access, Q12 | Exported count | Share of 51 |
| --- | --- | --- |
| Yes | 16 | 31.4% |
| No | 25 | 49.0% |
| Not sure | 10 | 19.6% |

| Preferred language, Q13 | Exported count | Share of 51 |
| --- | --- | --- |
| English | 14 | 27.5% |
| Russian | 15 | 29.4% |
| Kazakh | 12 | 23.5% |
| Other | 6 | 11.8% |
| No preference | 4 | 7.8% |

Q13 responses do not change the release's localization scope. Offline access and additional languages remain topics for actual user research and a separate scope decision.

## 5. Instrument

The exported instrument covers the same topics as the interview hypotheses but is a separate questionnaire. It is not the SUS usability questionnaire and does not measure clinical outcomes.

| ID | Question | Options / applicability |
| --- | --- | --- |
| Q01 | Which role best describes how you would use this platform? | Patient; Doctor; Laboratory specialist; Other |
| Q02 | Which device would you prefer for this activity? | Phone; Computer; Tablet; No preference |
| Q03 | How often do you currently review or manage laboratory reports or medical documents? | Never; Less than monthly; Monthly; Weekly; Daily |
| Q04 | Where do you mainly keep or access these documents today? | Paper files; Files on a device; Patient portal; Spreadsheet; Clinical information system; I do not manage these documents |
| Q05 | How difficult is it to find a previous result when you need it? | 1 — Very easy; 2; 3; 4; 5 — Very difficult Leave blank when Q03 is Never. |
| Q06 | Which difficulty, if any, affects you most? | Finding an earlier document; Comparing values over time; Understanding units and ranges; Checking copied values; Managing access; No significant difficulty Leave blank when Q03 is Never. |
| Q07 | How interested would you be in trying a platform that organizes records, lab history and source-linked summaries? | 1 — Not interested; 2; 3; 4; 5 — Very interested |
| Q08 | Which one capability would you prioritize? | Lab history and charts; Document storage and search; Source-linked summaries; Upload and extraction review; Access controls; Mobile access; No new platform needed |
| Q09 | How willing would you be to use an AI-generated summary as a reading aid, with the original available for checking? | 1 — Not willing; 2; 3; 4; 5 — Very willing |
| Q10 | What would be your main concern about such a platform? | Incorrect information; Privacy or access; Extra work; Difficult interface; Service availability; No major concern |
| Q11 | How important is being able to open the original source for a summary item? | 1 — Not important; 2; 3; 4; 5 — Very important |
| Q12 | Would access to previously saved records without an internet connection matter to you? | Yes; No; Not sure |
| Q13 | Which interface language would you prefer? | English; Russian; Kazakh; Other; No preference |
| Q14 | How useful would a date-filtered chart of your recorded lab results be? | 1 — Not useful; 2; 3; 4; 5 — Very useful Only Patient. |
| Q15 | How useful would a source-linked summary be when preparing to review an assigned record? | 1 — Not useful; 2; 3; 4; 5 — Very useful Only Doctor. |
| Q16 | Which extraction-review improvement would you prioritize? | Source beside editable fields; Clear missing-field flags; Draft and published states; Duplicate confirmation prevention; No improvement needed Only Laboratory specialist. |
| Q17 | What one change would help your workflow? Please do not include names, diagnoses or medical details. | Optional free text, up to 600 characters; no personal or medical details. |

## 6. Requirement traceability and decisions

Export counts are verified properties of the supplied file. User preferences and workflow benefits remain assumptions because the dataset consists of automated tests plus an unverified additional submission. The material can support questionnaire and data-processing checks; it cannot validate a user need.

| Survey topic | Requirement / interview hypothesis | Decision |
| --- | --- | --- |
| Q05–Q06, Q08, Q14: finding and comparing laboratory results | FR-LAB-2/3, FR-DASH-1; H01/H02; RC12-01/02 | Retain existing requirements. Validate actual result-finding behavior in real sessions. |
| Q04, Q08, Q16: document organization and extraction review | FR-DOC-1/2, FR-LAB-1; H03/H06; RC12-03/05 | Retain source provenance, missing-field handling and confirmation boundaries. Treat test comments as scenarios only. |
| Q09–Q11, Q15: summaries and source checking | FR-SUM-1/2/3; H04; RC12-04 | Retain the evidence-inspection and consistency requirements. Evaluate summary quality separately under MDP-29. |
| Q10: privacy and access concerns | FR-AUTH-2, NFR-PRIV-1; H05 | Retain authorization and minimum-context boundaries, independently of survey ratings. |
| Q02, Q12, Q13: devices, offline access and language | FR-UI-1, NFR-I18N-1 | Keep the established release scope. No offline mode or additional language commitment is introduced by these test records. |
| PDF-R051: role-inapplicable answer | Questionnaire routing and analysis | Preserve the source and flag the inconsistency; exclude out-of-role Q15 from doctor analysis. Use routing or explicit skip instructions in subsequent collection. |

## 7. Relationship to MDP-12

The supplied export is now documented alongside the interview material, with readable question wording, traceable row data, descriptive counts and an explicit data-quality decision. The source PDF is excluded from the repository at the team's request. No requirement priority or acceptance threshold is changed on the basis of these responses.

The original MDP-12 acceptance criterion requires at least three actual interviews with notes and subsequent evidence-based requirement updates. A questionnaire submission is not automatically an interview, and the 50 automatic tests plus one unverified row do not establish that requirement. The existing four simulated interview notes remain unchanged in provenance. Actual collected feedback can be added later as a separately dated evidence record.

The team requested tracker closure for this documentation package. This administrative disposition does not establish that the original real-interview criterion was met.
