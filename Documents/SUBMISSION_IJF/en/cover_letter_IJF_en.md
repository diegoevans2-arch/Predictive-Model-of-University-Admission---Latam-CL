---
title: "Cover letter"
lang: en-US
---

<!-- Not anonymized: submit together with the title page, never inside the review file. -->

\[PENDING: date of submission\]

Prof. Pierre Pinson \[PENDING: confirm the current Editor-in-Chief at the time of submission\]\
Editor-in-Chief, *International Journal of Forecasting*

Dear Professor Pinson,

I am pleased to submit the research paper "When the naïve forecast is the lag: Evaluating program-level university enrollment forecasts in Chile" for consideration for publication in the *International Journal of Forecasting*.

**Contribution.** The paper forecasts undergraduate university enrollment in Chile at the level of institution × program × region × attendance mode × gender × student status, from public administrative records, and asks what a forecasting model actually adds over persistence in a series this inertial. Its first contribution concerns evaluation: the persistence forecast is, by construction, the same lag column that feeds the model, and the paper documents a real case in which a single defect in the lag-matching key contaminated the numerator and the denominator of the skill score at the same time, inflating the out-of-sample skill in one year and sinking it in the next while every model-centered diagnostic remained reasonable. The paper proposes concrete controls for any study that reports skill against persistence on lagged data.

With persistence correctly constructed, the paper then separates a robust result from a period-dependent one. The robust result is that global models (CatBoost and LightGBM, with or without exogenous features) have lower error than both persistence and series-by-series methods (drift, ETS, ARIMA, Theta and their combination) at the cell level, although the advantage over persistence is statistically significant only in the evaluations with a long training history (2025 and 2026), not across the full retrospective period; on the official 2026 data, the main model reduced the weighted absolute percentage error from 12.69% (persistence) to 11.49%, and a lags-only global model reached 11.16%, whereas the per-series methods are competitive only for the national total. The period-dependent result comes from a factorial algorithm × feature design tested with Diebold–Mariano tests clustered by institution: exogenous features do not improve cell-level accuracy in 2026 but do improve aggregates in 2019–2025. The paper does not claim that exogenous features add nothing; it states this as a hypothesis for a prospective test. It also reports size-stratified conformal intervals with verified coverage and the best interval score at almost all levels, and quantifies the isolated leakage of a precomputed target encoding.

**Fit with the journal.** The paper addresses themes central to the *International Journal of Forecasting*: benchmark construction and evaluation against the naïve method, comparison of global and local methods, evaluation across aggregation levels, formal tests of forecast accuracy, conformal prediction intervals and prospective evaluation. The status of each result is explicit: the evaluation against the 2026 data is out of sample but not prospective, because those data motivated the audit that corrected the pipeline.

**Prospective test and frozen artefacts.** The 2027 forecasts of the full 2×2 design (four models) and of two benchmarks were frozen on 20 November 2026, before the official 2027 release expected in July 2027, together with a prespecified evaluation protocol (version 2.2): first official release without adjustment, absolute primary loss, five hypotheses (including whether exogenous features add value) and explicit failure criteria. The freeze is recorded as follows, for the editor's verification:

- Date of the freeze: 20 November 2026, 10:23:11 (UTC−03:00).
- Commit: `e1f9b448e70d70ccef5e51973ea216fa58dd61d4`, under the annotated tag `forecast-2027`.
- SHA-256 of the 2027 predictions of the 2×2 design: `259d272cd55d6342a21c024b5563467b1116a23265d6b850df9bdf98b1b6111f`.
- SHA-256 of the original C49 predictions: `79b7b5d6880ca50e85baab1465cd25fe349501206524314c43a07d770fcb393e`.
- SHA-256 of the evaluation protocol v2.2: `77856cbf1808d6f463e279a5a037963d2982f00cddbb9d8d1ae936d6478c3c70`.
- SHA-256 of the evaluation program `evaluar_2027.py`: `452ecb37fbab0c0b62f22d80fa3aac82899e0a4a1c896ac05d2ae29ae20708f8`.
- Zenodo DOI: \[PENDING\].

These identifiers are omitted from the manuscript, its Online Appendix and the highlights to preserve double-anonymous review; the manuscript states that they are provided to the editor in this letter. If the review process extends beyond July 2027, I would be glad to add the prospective evaluation to a revised version.

**Data and code.** All primary data sources are public and are cited as data references. The 2027 prediction files, the evaluation protocol and the program that runs it were published with the 20 November 2026 freeze. The consolidated dataset and the full pipeline code will be deposited with a DOI upon acceptance, and during review they will be made available on request to the editor and for the journal's reproducibility check. I understand that the journal's policy requires sharing data and code unless the Editor-in-Chief accepts a justification; should a deposit at submission be required, I can provide one with access restricted to the editorial team. \[PENDING: the author should confirm this wording, or replace it with a formal justification if one is to be requested.\]

**Originality and prior dissemination.** This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. It will not be submitted to another journal while it is under review at the *International Journal of Forecasting*. \[PENDING: decide whether to disclose to the editor the existence of the public documentation repository and dashboard related to this work, which are not linked in the anonymized manuscript, and confirm their status under Elsevier's preprint policy.\]

**Declarations.** The author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. \[PENDING: confirm funding statement.\] The declaration on the use of generative AI is included in the manuscript, before the references. \[PENDING: complete that declaration.\]

\[PENDING, optional: suggested reviewers or reviewers to exclude, if the submission system requests them.\]

Thank you for considering this submission. I look forward to hearing from you.

Yours sincerely,

Diego Evans Pérez Paz\
\[PENDING: affiliation\]\
\[PENDING: email\] · \[PENDING: full postal address\] · ORCID: \[PENDING, optional\]
