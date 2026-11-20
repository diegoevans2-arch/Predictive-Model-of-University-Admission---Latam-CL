# IJF compliance checklist and gaps for Q1 level

*Manuscript:* "When the naïve forecast is the lag: Evaluating program-level university enrollment forecasts in Chile" (English version, v3 rewrite with v4 delta, `manuscrito_IJF_en.md` / `.docx`; one-to-one mirror of `manuscrito_IJF_es.md` v4). Items specific to the English version are marked *(EN)*. *Journal:* International Journal of Forecasting (IJF). *Date:* 20-Nov-2026.

Statuses: **Met** · **Resolved** (analysis executed by the author and incorporated) · **Author pending** · **Analysis gap** (marked in the text as `[Q1 GAP: …]`). The sources for the requirements are those of the *Report on validation of references, data sources, and IJF requirements* (§4.2).

## 1. Formal journal requirements

| # | IJF Requirement | Status | Where it is resolved | Requirement source |
|---:|---|---|---|---|
| 1 | Fit to scope: new contribution to forecasting science or practice | Met: evaluation contributions now supported by comparison with per-series benchmarks, global model, factorial design, DM tests, and prespecified prospective comparison | Title, Abstract, §1, §5.5–5.6, §6.3–6.4 | IJF Guide for Authors (2020) |
| 2 | Abstract of 100–150 words, without references, jargon, or notation | *(EN)* Met (137 words counted by spaces, as in Word; unchanged in the v4 delta) | Abstract | Guide for Authors (ScienceDirect) |
| 3 | At least 5 keywords not repeating the title | Met (7). Author pending: cross-check against the IIF list | Keywords | Guide for Authors; forecasters.org/ijf/keywords |
| 4 | Highlights: 3–5 bullet points of ≤85 characters | *(EN)* Met (5; 74–82 characters, verified by code) | `highlights_en.md` | IJF Checklist; Elsevier standard |
| 5 | Double-blind review | Met in the text: no name, repository, dashboard, tag, commit, digests, or freeze DOI (identifiers omitted and delivered to the editor in the EN cover letter; verified by code). Author pending: clean up `.docx` properties | Manuscript, appendix, title page | Guide for Authors (elsevier.com) |
| 6 | Separate title page | Author pending (affiliation, email, address, ORCID) | `title_page_en.md` | Guide for Authors |
| 7 | English language | *(EN)* Met: American English, one-to-one with the Spanish v4 (figures, tables, numbering, cross-references, markers and set of figures verified by code). Author pending: professional language edit | EN version | IJF Guide (2020) |
| 8 | Author-year style, DOI, and *data references* | Met: 94 cited keys, 94 entries in `references.bib` (five new entries verified in CrossRef: Koning et al. 2005, Hyndman & Khandakar 2008, Hyndman et al. 2002, Assimakopoulos & Nikolopoulos 2000, Cameron & Miller 2015). Author pending: entry for the SIES *2026 Enrollment Report*; verified citation for Nemenyi (no verifiable DOI in CrossRef) | References | Guide for Authors |
| 9 | CRediT statement | Met | Title page | Guide for Authors |
| 10 | Conflict of interest | Met; Elsevier form pending | Manuscript; title page | IJF Guide |
| 11 | Generative AI statement | Author pending (neutral draft) | Before References | Guide for Authors |
| 12 | Funding | Author pending (confirm) | Manuscript; title page | Guide for Authors |
| 13 | Data and code (July 2023) | Author pending: anonymous statement drafted; the 2027 forecasts for the 2×2 and the benchmarks, the protocol, the evaluation program, and their digests were published with the 20-11-2026 freeze; Zenodo DOI pending; panel and code with DOI upon acceptance | Data availability | forecasters.org/ijf |
| 14 | Supplementary material | Met: appendix A.1–A.24 with 41 tables and 9 figures | Online appendix | ScienceDirect |
| 15 | Figures and tables with caption and cited | Met: 5 figures and 13 tables in the body; *(EN)* EN figures from `figuras_en/` with decimal point and English labels (ES figures from `figuras_es/`, decimal comma and Spanish labels); fig07 with deciles by lag, fig07b and fig11b new; SHAP captions state in-sample attributions; cross-references verified by code | §5; Appendix | IJF submission checklist |
| 16 | Length | No explicit limit. *(EN)* Body: ~9,200 words of prose in the English version (script count) | Manuscript | Report §4.2 |

## 2. Analysis gaps

| # | Gap | Status | Where |
|---:|---|---|---|
| 2.1 | Classical per-series benchmarks (RWD, ETS, ARIMA, Theta, Comb) and simple global model | **Resolved** | §4.7, §5.5, Table 8; Appendix A.16 |
| 2.2 | Hierarchical reconciliation (*bottom-up* vs OLS, WLS, MinT) | **Resolved**: the bottom-up sum is best in N1–N5 | §4.7, §6.5; Appendix A.21 |
| 2.3 | DM tests by cluster, HLN in N1, and MCB/Nemenyi | **Resolved**: *p* values alongside each skill in Tables 4, 6, and 7 (OOF 2019–2026: no significant difference, lowest *p* 0.0992; 2025 holdout: significant with absolute loss in N5–N8); MCB by level with observed value | §4.8, §5.2, §5.4–5.6, §6.4; Appendix A.17 |
| 2.4 | P-04 ablation | **Resolved**: +0.06 WAPE points in the holdout cell (12.27% → 12.33%, variant ii) | §6.5; Appendix A.18 |
| 2.5 | 2027 intervals (P-05) | **Resolved** for the four models (coverage in the 2026 holdout from 92.25% to 93.25%) | §5.7, §5.10; Appendices A.11 and A.23 |
| 2.6 | Formal freeze (P-01) | **Resolved**: six forecasts frozen on 20-11-2026 with annotated tag and digests; protocol v2.2 with asymmetric calibration criterion. Author pending: Zenodo DOI | §5.10; Appendix A.14 |
| 2.7 | Audit of worst cells by lag origin | **Resolved** | §4.2, §5.4; Appendix A.4 |
| 2.8 | Interval score and MSIS | **Resolved**; stratified bands have the lowest IS except in N7, where AutoETS is marginally lower (79.7 vs. 79.8) | §5.7, Table 11; Appendix A.19 |
| 2.9 | Clean target encoding | **Resolved**: isolated leakage of 2.92% (*m*-estimator) to 3.74% (sigmoid) | §5.8, Table 12; Appendix A.20 |
| 2.10 | Algorithm × variables factorial design and breakdown by year | **Resolved** (L-02: exogenous-variable advantage concentrated in years with little history and in 2022) | §5.6, §6.4, Table 9; Appendix A.22 |
| 2.11 | Evaluation against observed enrollment | **Resolved** (holdout and OOF re-evaluated; 2026 validation unchanged) | §3.3; Appendix A.15 |

## 3. Author pending items (no new analysis)

1. Entry for the SIES *2026 Enrollment Report* in the .bib; verified citation for the Nemenyi test; systematic search in Scopus/WoS/SciELO.
2. Confirm the note on the 113 duplicated rows (B-04).
3. Zenodo DOI for the freeze and the deposit.
4. Title page (affiliation, email, ORCID, funding, acknowledgments), AI statement, and conflict-of-interest form.
5. **Resolved:** the labels inherited from the model metadata (number of folds, 5 instead of the 7 executed, and labels for the holdout and forecast assumptions) were corrected before the freeze, without changing any numerical value or the predictions (Appendix A.13).

## 4. Desk-rejection risks and how to mitigate them

1. **Reads like an application.** Mitigated: the contribution is now supported by comparisons with per-series benchmarks and a global model, a factorial design with formal tests, and a prespecified prospective comparison; the cover letter should open with the failure mode "the naïve forecast is the lag."
2. **The main model is not the best in the cell.** The lags-only global model outperforms C49 in 2026. Mitigation: the text already presents this as a result and separates the robust contribution (global design) from the period-dependent one (exogenous variables); do not claim CatBoost as superior.
3. **Data and code policy.** Mitigation: access for the editor during review, publication of the 2027 forecasts with the freeze, and deposit with DOI upon acceptance; prepare the replication package before submission.
4. **Anonymity compromised by the public repository.** Mitigation: no links or tag names in the manuscript; consider retitling the README during review and informing the editor.
5. **Only one recent test year and non-significant advantage in the full OOF.** Mitigation: both are stated without smoothing (§5.2, §6.4); the 20-11-2026 freeze turns 2027 into a prospective test with hypotheses and criteria set in advance.
6. **Length.** *(EN)* ~9,200 words and 13 tables in the body. Mitigation: consider moving Table 12 and part of Table 10 to the appendix.
7. **Figures.** *(EN)* Mitigated: figures regenerated in English (`figuras_en/`); rename files in order of appearance for submission.
8. **Language.** *(EN)* Addressed by this version; a professional language edit is still advisable.

## 5. Prioritized list before submission

1. Create the Zenodo deposit from the freeze tag and insert the DOI in the cover letter (not in the anonymous manuscript).
2. Complete the title page, the AI statement, and the pending bibliographic entries.
3. Confirm note B-04 and clean up the `.docx` properties.

## 6. Marker count (after v4 delta)

| File | [Q1 GAP] | [PENDING] |
|---|---:|---:|
| manuscrito_IJF_en.md | 0 | 8 |
| apendice_en_linea_en.md | 0 | 2 |
| title_page_en.md | 0 | 9 |
| cover_letter_IJF_en.md | 0 | 12 |
