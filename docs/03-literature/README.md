# Literature review

| Item | Value |
| --- | --- |
| Project | Intelligent Medical Platform |
| Contributor | Yerkin Yerassyl |
| Work item | [MDP-2 — Literature review](https://nauka11.youtrack.cloud/issue/MDP-2) |
| Review date | 23 October 2026 |
| Scope | Patient-facing laboratory results, interoperability, document extraction, clinical summarization, retrieval, evaluation and data selection |

The literature supports developing the platform as a prototype for organizing and presenting patient information. It also sets limits on what the project can demonstrate: readable summaries do not establish factual accuracy, document benchmarks do not establish performance on laboratory reports, and synthetic records do not establish clinical validity. These distinctions guide the architecture and evaluation of the [project proposal](../01-proposal.md).

## Review questions

1. How should laboratory results be presented so that patients can understand values and changes over time?
2. Which approaches can turn documents and heterogeneous records into consistent patient data?
3. What evidence supports clinical summarization and retrieval-augmented generation, and where does that evidence remain weak?
4. Which baselines, datasets and checks can support a credible evaluation within the diploma project's scope?

## Source selection

This is a targeted critical review, not an exhaustive systematic review. The initial reading list was checked against publisher records and extended with work on OCR, document layout, evaluation and synthetic records. Searches used paper titles and combinations of terms including "patient laboratory results presentation systematic review", "FHIR semantic interoperability", "TrOCR", "LayoutLMv3", "clinical text summarization evaluation", "retrieval augmented generation healthcare systematic review", "MIMIC-IV" and "Synthea". Publisher pages, author manuscripts and Crossref DOI records were consulted on 23 October 2026.

Sources were included when they addressed a review question, provided an identifiable method or dataset, and had a published journal or conference version with verifiable bibliographic information. Preprint versions of published papers were not counted again. Product marketing, search snippets without an accessible research record, and unrelated clinical prediction studies were excluded from the evidence base.

The selected corpus contains **14 peer-reviewed publications: 12 journal articles and 2 conference papers**. Twelve were published within the five-year window from 23 October 2021 to 23 October 2026. Two older works are retained for specific reasons: Ayaz et al. provide background on FHIR implementations, and Walonoski et al. describe the synthetic-record generator relevant to the data strategy. The recent core comprises publications from 2022–2025.

Titles, authors, venues, publication dates, volumes and page or article numbers were checked against each DOI's Crossref record and the available publisher or author record. The [reference list](references.md) provides the DOI links and explains online-versus-issue dates. This review uses qualitative comparison; it does not pool results from different tasks or treat overlapping reviews as independent sets of patients.

## Critical review

### Patient access and laboratory result presentation

Van der Mee et al. synthesize 18 studies of laboratory-result presentation. Visual ranges and explanatory context can improve how results are perceived, but 16 studies used hypothetical results, and evidence about subsequent action and memory was limited. A preferred display in a controlled task therefore cannot be assumed to improve health outcomes. [R01](references.md#r01)

Petrovskaya et al. examine 27 studies covering patient and provider perspectives. Their findings place result comprehension alongside release timing, uncertainty and communication with clinicians. This broadens the design problem beyond chart selection: patients also need context about what the information means and where it came from. [R02](references.md#r02)

For the platform, these findings support showing the numeric value, unit, date and supplied reference interval together, with a concise label and an optional trend view. Choosing the exact layout remains a usability question. The studies do not establish local needs in Kazakhstan, which will be investigated through MDP-12.

### Interoperability and the meaning of structured data

Ayaz et al. map FHIR implementations across 80 studies published through 2019. This is useful background on exchange patterns, but it cannot establish the current maturity of every implementation. Amar et al. provide a more recent mapping of 70 studies focused on semantics: sharing a resource structure still leaves work in terminology mapping, annotation and interpretation. [R03](references.md#r03), [R04](references.md#r04)

The distinction matters for extracted laboratory results. A successfully parsed number is not usable without its analyte, unit, date and source context. Our design implication is a FHIR-inspired internal model with explicit provenance and unit handling. Full FHIR conformance and hospital connectivity remain outside the prototype scope. Neither review implies that using JSON or naming an entity "Observation" achieves interoperability.

### OCR and document structure

TrOCR demonstrates a pretrained Transformer approach to text recognition across printed, handwritten and scene-text benchmarks. Its evidence concerns recognition, not complete laboratory-report parsing. Page segmentation and the association between a test name, value, unit and interval remain separate problems. [R05](references.md#r05)

LayoutLMv3 combines text, image and layout information for document understanding. Its results motivate evaluating layout when tables and spatial relationships matter, but its general benchmarks do not validate extraction on our report templates. [R06](references.md#r06)

These papers support a staged pipeline: use embedded text for digital PDFs, apply OCR when needed, then extract fields while retaining their source location. A rule-based parser will provide the initial baseline. More complex models will be justified by measured gains on held-out layouts and scan conditions, rather than adopted solely because they perform well on unrelated benchmarks.

### Clinical summarization and evaluation

Bednarczyk et al. identify 30 studies of LLM clinical summarization, all retrospective, with only two reporting external validation. Their review explains why encouraging internal scores provide limited evidence for routine clinical use. [R07](references.md#r07)

Van Veen et al. offer stronger task-specific evidence through adaptation experiments and a reader study with ten physicians. The best adapted model's summaries were rated equivalent to expert summaries in 45% of comparisons and superior in 36%. These results concern selected tasks and models; they do not demonstrate general superiority over clinicians or validate our implementation. [R08](references.md#r08)

Tang et al. study medical evidence summarization, which differs from summarizing an individual patient's record. Their finding that automatic scores can diverge from human judgments is still relevant to evaluation design. [R09](references.md#r09)

The platform will compare an extractive baseline, an LLM without retrieval and a retrieval-assisted variant. Reviewers will assess completeness, correctness and conciseness. Checks of numeric values will also verify their association with the correct test, unit and date: finding the same number somewhere in a source is insufficient evidence of a correct summary.

### Retrieval and factual grounding

Amugongo et al. describe healthcare RAG architectures and identify uneven evaluation practice and a concentration on English and Chinese datasets. Retrieval adds supporting context, but this evidence does not establish reliability in other languages or eliminate unsupported output. [R10](references.md#r10)

Liu et al. synthesize 20 comparative studies and report a pooled odds ratio of 1.35 in favor of RAG. This is not a 35-percentage-point accuracy gain. The tasks and evaluation methods vary, so the pooled result is a reason to test retrieval, not an expected effect size for patient summaries. [R11](references.md#r11)

For this project, retrieval will be restricted to records the requesting user is authorized to access. Summaries will retain source references and handle missing evidence explicitly. Evaluation will separate retrieval failures from generation errors and compare variants using the same model and test documents. These are project design choices informed by the reviews, rather than safety guarantees reported by them.

### Longitudinal analysis and the data strategy

Hama et al. review deep learning on sequential diagnosis codes. Only seven of 84 studies evaluated generalizability, and 59 had a high risk of bias. Diagnosis-code prediction is different from laboratory trend detection, so the review cannot validate our trend rules; it demonstrates the weakness of extending model claims beyond their evaluation setting. [R12](references.md#r12)

MIMIC-IV provides a substantial example of linked clinical records, but its hospital setting and controlled access limit direct reuse for a patient-facing prototype. It is a research reference here, not a dataset already obtained or included in the repository. [R13](references.md#r13)

Synthea provides a method for generating longitudinal synthetic records. Its original US-oriented care models are a useful starting point for fixtures, not evidence that generated records represent Kazakhstan or every clinical condition. [R14](references.md#r14)

The prototype will use synthetic records with explicit ground truth and varied document layouts. Laboratory analytics will begin with reference-range flags and transparent trend rules. Test results will establish behavior on those fixtures; they will not be presented as validation of disease prediction or clinical effectiveness.

## Structured analysis of publications

Each row links to the full bibliographic entry. Findings describe the cited publication; project implications identify how the team will use that evidence.

| Source | Method and evidence | Main finding | Limitation for this project | Project implication |
| --- | --- | --- | --- | --- |
| [R01](references.md#r01) van der Mee et al., 2024 | Systematic review; 18 presentation studies. | Contextual visual displays can support comprehension. | Mostly hypothetical results; limited behavioral evidence. | Test displays with values, ranges and explanations. |
| [R02](references.md#r02) Petrovskaya et al., 2023 | Scoping review; 27 portal studies. | Access involves communication, timing and uncertainty. | Patient and provider evidence is uneven; local transfer is untested. | Include source context and investigate user expectations. |
| [R03](references.md#r03) Ayaz et al., 2021 | Systematic review; 80 FHIR studies. | Maps implementations, resources and migration issues. | Search ends in 2019. | Use as background, not proof of current conformance. |
| [R04](references.md#r04) Amar et al., 2024 | Systematic mapping; 70 studies. | Semantic interoperability requires more than shared structure. | Review covers work through 2022. | Preserve terminology, units and provenance. |
| [R05](references.md#r05) Li et al., 2023 | OCR model evaluated on recognition benchmarks. | Pretrained Transformers support text recognition. | Not a complete medical-table extractor. | Evaluate recognition and field extraction separately. |
| [R06](references.md#r06) Huang et al., 2022 | Multimodal document pretraining and benchmarks. | Text, image and layout support document tasks. | General datasets differ from laboratory reports. | Compare layout-aware extraction with a simpler baseline. |
| [R07](references.md#r07) Bednarczyk et al., 2025 | Scoping review; 30 clinical summarization studies. | External validation and error analysis are uncommon. | Retrospective, concentrated evidence base. | Report failures, inputs and validation conditions. |
| [R08](references.md#r08) Van Veen et al., 2024 | Adaptation experiments and physician reader study. | Adapted summaries can receive strong expert ratings. | Selected models, tasks and study conditions. | Reproduce a structured comparison, not the published performance claim. |
| [R09](references.md#r09) Tang et al., 2023 | Automatic and human evaluation across six domains. | Similarity scores can miss quality and factuality problems. | Medical evidence differs from patient records. | Combine human ratings with factual checks. |
| [R10](references.md#r10) Amugongo et al., 2025 | Systematic review of healthcare RAG. | Retrieval designs and evaluation are heterogeneous. | Language coverage and ethical assessment are limited. | Test source grounding and language transfer explicitly. |
| [R11](references.md#r11) Liu et al., 2025 | Systematic review and meta-analysis; 20 studies. | Comparative evidence favors RAG overall. | Mixed tasks and outcome definitions. | Run a controlled retrieval ablation on our task. |
| [R12](references.md#r12) Hama et al., 2025 | Systematic review; 84 diagnosis-code studies. | Generalizability and bias remain substantial concerns. | Does not evaluate laboratory trend detection. | Keep clinical prediction outside scope. |
| [R13](references.md#r13) Johnson et al., 2023 | Clinical dataset description. | Linked records support reproducible EHR research. | Hospital-specific population and access requirements. | Inform schema design; do not assume data access. |
| [R14](references.md#r14) Walonoski et al., 2018 | Synthetic-record generator and method. | Simulated histories enable distributable test records. | Generated distributions reflect model assumptions. | Build fixtures and document their limitations. |

## Consequences for implementation and evaluation

The following decisions translate the review into work already defined in the backlog. They do not add diagnostic or treatment functions to the scope.

| Decision | Evidence | Related work items | Verification approach |
| --- | --- | --- | --- |
| Present values with units, dates, reference intervals and source context. | R01–R04 | MDP-5, MDP-7, MDP-17, MDP-21 | Scenario-based comprehension and usability tasks. |
| Keep OCR, extraction and source provenance as distinct processing concerns. | R04–R06 | MDP-14, MDP-22, MDP-23 | Field-level precision, recall and F1; errors grouped by template and scan quality. |
| Compare extractive, non-retrieval LLM and retrieval-assisted summaries. | R07–R11 | MDP-8, MDP-24, MDP-29 | Fixed documents, blinded ratings and fact-level error analysis. |
| Restrict retrieved evidence to authorized patient records. | R04, R10 | MDP-15, MDP-24, MDP-28 | Cross-patient and cross-role access tests. |
| Evaluate transparent laboratory trends without claiming disease prediction. | R12 | MDP-8, MDP-25 | Labelled synthetic series and a reference-range-only baseline. |
| Use synthetic fixtures first and separate tuning from final evaluation. | R07, R13, R14 | MDP-16, MDP-29, MDP-30 | Held-out templates, reproducible generation settings and stated population limits. |

## Research gap and limitations

The selected work provides methods and evidence for separate parts of the proposed platform. It does not establish that combining them will improve clinical outcomes or that no comparable product exists. The project's engineering contribution is to connect document processing, traceable summaries and longitudinal displays in one prototype and evaluate the complete workflow against simpler alternatives.

The main unresolved questions are performance on unfamiliar report layouts, whether retrieval improves faithfulness on our records, how users understand the dashboard, and how synthetic-data results transfer to real settings. Local user evidence and any multilingual capability require separate investigation. Several included reviews overlap in their underlying literature, and their study counts must not be added together as a measure of independent evidence. No formal risk-of-bias assessment was performed for this targeted review; limitations reported by the publications are distinguished above from project-specific judgments.

The targets in the proposal, including extraction F1 and usability thresholds, remain project evaluation criteria. They are not performance levels derived or guaranteed by this literature review.
