# v4 delta changes to the IJF manuscript — English version (20 Nov 2026)

## Changes in the Spanish version (translation of `cambios_v4_es.md`)

Literal source of figures: sections Q, R, S and U of OBSERVACIONES_Y_MEJORAS.md. Starting version: manuscript v9c2ba428 (147-word abstract, unchanged), appendix v537baf42, title page v0dc76920, highlights va128551d and checklist vff131b97.

### Manuscript

- ,3.1, Table 1 and note: GDP in volume at previous year's chained prices (reference 2018; Central Bank, 04-23-2026 edition, preliminary figures); 2025 unemployment with 10 of 12 moving quarters; closed the [PENDING] of GDP
- Table 4: *p* values of the 2019–2026 OOF (0.9758 / 0.0992) and of the 2025 *holdout* (0.0569 / 0.0052) with a note on the 73,349 groups; ,5.2: reading of R-01 unsmoothed
- ,5.9: region with observed actual (11.99 % Los Ríos – 25.50 % Aysén; RM 14.78 %; WAPE lower than persistence in 14 of 16, negative *skill* in 6)
- ,5.10: title «*ex ante*, frozen before the data»; literal text of the freeze of 11-20-2026 with identifiers omitted and [PENDING: Zenodo DOI]; asymmetric calibration criterion v2.2 set after the dry run; the only [Q1 GAP] removed; 15 of 53 confirmed drops with observed basis; linear regression 730,266 (−1.53 %); Figure 5 caption without the label or separator warning
- Figures: paths to figuras_es/; captions of Figures 1, 3 and 5 without separator warnings; Figure 3 with the observed 2018 point (653,163)
- ,1, ,6.4 and ,7: the "robust result" is qualified with R-01 (WAPE advantage; significant only in 2025–2026, not in the full OOF); verb tenses of the freeze
- Data availability: publication with the freeze of 11-20-2026; [PENDING: Zenodo DOI]
- ,3.1, Table 1 note: the residual phrase about current prices was removed (no "current prices" remains in the text).

### Appendix

- A.1: GDP in volume at previous year's chained prices (reference 2018; 04-23-2026 edition, preliminary figures; annual rows 2013–2025; 2026 carried forward); 2025 unemployment with 10 of 12 moving quarters, explaining which are missing. Both [PENDING] closed.
- A.9: Table A.13 (region) and Table A.14 (mode) replaced by the R.2 versions with observed enrollment (region with R² and aggregate error; WAPE lower than persistence in 14 of 16 regions, negative *skill* in 6).
- A.10: SHAP captions (Figures A.2–A.5) state that these are attributions of the final model trained on 2018–2026 over OOF 2019–2026 rows, in-sample; Figure A.3 = mean |SHAP| by subgroup; new Figure A.4 (fig11b, signed mean SHAP); Figure A.5 (fig12) keeps institution and program by the author's decision. [PENDING] items in captions closed.
- A.12: Figure A.8 (fig07) with deciles by lag and the U.1 biases (+1.25 %; +0.25 %; −1.70 %; −1.66 %; −1.64 %; −2.48 %; −2.40 %; −2.78 %; −1.87 %; −2.57 %; negative = overprediction); new Figure A.9 (fig07b, deciles by observed enrollment; Q1 −94.44 % … Q10 −0.43 %) as an illustration of regression to the mean; the warning about English-language axes in Figure A.6 removed.
- A.13: item 3 (metadata) without [PENDING], stated as a note; item 4 (figures) updated: figures regenerated, observed 2018 in Figure 3 and linear regression −1.53 %.
- A.14: protocol v2.2 approved and frozen on 11-20-2026; asymmetric calibration criterion (undercoverage < 88 %, calibrated 88–95 %, conservative > 95 %) set after the dry run on 2026; dry run results in N8 and N2–N7; identifiers omitted; [PENDING: Zenodo DOI].
- A.16: new table A1 in N3, N4, N6 and N7 with observed enrollment (R.2); [PENDING] closed.
- A.17: new table R.1 (CatBoost versus persistence in the 2019–2026 OOF and the 2025 *holdout*, observed enrollment); MCB/Nemenyi by level with observed enrollment for the 2026 *holdout* and the 2026 validation (replaces the three previous MCB tables).
- A.19: IS/MSIS table replaced by the complete R.2 version (with common groups).
- **Tables withdrawn** for existing only with the clipped value and without an observed version in R.2: global model versus persistence (2026 *holdout*), N1 with HLN in both losses, and N1–N8 ablation in the *holdout* and in the OOF. Their key content with observed value is in Tables A.26 (C49 versus persistence and global, with the observed HLN note) and A.32 (N2 and N8 ablation).
- Figure paths to `figuras_es/`.
- Renumbering: tables A.1–A.41 (including the H1–H5 hypothesis table from the protocol, which previously had no number: Table A.16) and figures A.1–A.9 in order of appearance; internal references updated and verified by code.

### Highlights and title page

- Highlights: "They froze…" (81–84 characters; without freeze identifiers).
- Title page: 41 tables and 9 figures in the appendix; data availability with the freeze of 11-20-2026 and the identifiers delivered to the editor in the cover letter; [PENDING: Zenodo DOI]; removed the [PENDING: set when translating] from the English working title.

### Code verifications

- 94/94 citation keys in references.bib (no changes to the .bib); ES abstract 147 words by spaces; highlights ≤ 84 characters; cross-references to sections, tables, figures and A.x subsections without missing targets; no "−1.27 %" nor "current prices"; no "e1f9b448", "forecast-2027" nor the digests in manuscript, appendix and highlights; new figures verified against Q–U.
- .docx regenerated with pandoc + citeproc + APA, with figures read from `Documents/OUTPUTS_PAPER/figuras_es`: manuscript with 13 tables, 5 figures and 94 references; appendix with 41 tables, all numbered, and 9 figures.
- Body length: ~10,970 words of prose (previously ~10,680), due to the new R-01 and protocol sentences.

### Judgment calls

1. **Sign of fig07.** The R.2 table uses predicted/actual − 1; the figure and U.1 use (actual − predicted)/actual. The captions copy the figures from U.1, which are the figure's.
2. **"Robust result."** With R-01 it was qualified in ,1, ,6.4 and ,7: the global models have lower WAPE than persistence at the cell level, but CatBoost's advantage is not significant in the 2019–2026 OOF and is significant in 2025–2026 with absolute loss.
3. **Model metadata.** Q–U do not confirm that the number of *folds* in the metadata was corrected; the [PENDING] was removed per the specification, but it remains as a note in A.13 and as a point to verify in the checklist.
4. **Nemenyi citation.** No verifiable DOI was found (the original thesis and Demšar 2006 are not in CrossRef); it remains as [PENDING].

### Marker count

| File | [Q1 GAP] | [PENDING] |
|---|---:|---:|
| manuscrito_IJF_es.md | 0 | 8 |
| apendice_en_linea_es.md | 0 | 2 |
| title_page_es.md | 0 | 9 |

No [Q1 GAP] remain.

### Final list of [PENDING]

**Manuscript**

- PENDING: systematic search in Scopus/WoS/SciELO on *enrollment forecasting* and *higher education demand*, with stated inclusion criteria.
- PENDING: add to the .bib the entry for the SIES *Informe de Matrícula en Educación Superior 2026*, which is the edition whose figures are cited; the current .bib contains only the 2025 edition, `sies2025informe`.
- PENDING: verified citation of the Nemenyi test
- PENDING: Zenodo DOI
- PENDING: author's confirmation to include this note
- PENDING: Zenodo DOI
- PENDING: the author must complete this statement according to Elsevier policy, indicating which tool was used, for what purpose and at which stages. Neutral draft for review:
- PENDING: confirm.

**Appendix**

- PENDING: author's confirmation to include this note
- PENDING: Zenodo DOI

**Title page**

- PENDING: full institutional affiliation, city and country
- PENDING
- PENDING
- PENDING, optional
- PENDING: confirm.
- PENDING: also complete Elsevier's declaration of interests form upon submission.
- PENDING: add personal or institutional acknowledgments, if any; these should appear only on this page.
- PENDING: Zenodo DOI
- PENDING: the author must complete according to Elsevier policy; the same statement appears at the end of the manuscript, before the references.

## Changes specific to the English version

- **Mirror of ES v4:** the 45 Spanish blocks changed between v3 and v4 (13 in the manuscript, 32 in the appendix) were translated against the previous English text and spliced in paragraph by paragraph; title page, highlights, checklist and this log updated accordingly.
- **Correction of 20 Nov 2026 (also applied to ES):** Appendix A.13, item 3 now states that the 2026-origin metadata carried inherited labels (number of folds, 5 instead of the 7 run; holdout and forecast-assumption labels) and that they were corrected before the freeze, without changing any numeric value or the predictions; the corresponding checklist item is marked resolved.
- **Abstract:** unchanged (137 words counted by spaces), because the Spanish abstract did not change in v4.
- **Figures:** all 14 image paths point to `figuras_en/` (English labels, decimal point); 5 figures in the manuscript and 9 in the appendix. In A.13, item 4, the sentence on the regenerated figures states both versions (Spanish: decimal comma and Spanish labels; English: decimal point and English labels).
- **Cover letter:** new paragraph "Prospective test and frozen artefacts" with the freeze date (20 November 2026, 10:23:11, UTC−03:00), commit, annotated tag, the four SHA-256 digests (2×2 predictions, original C49, protocol v2.2, `evaluar_2027.py`) and Zenodo DOI [PENDING]; it explains that these identifiers are omitted from the manuscript for double-anonymous review. The robust-result sentence now carries the v4 qualification (significant advantage over persistence only in 2025 and 2026).
- **Title page:** appendix with 41 tables and 9 figures; data availability with the 20 November 2026 freeze; ~9,200 words of prose (script count for the English text).

## Verification of the English version (by script)

- Set of numbers in the EN manuscript and appendix = set in ES v4 converted to English format: 0 discrepancies; highlights and title page likewise (except the intended word count).
- Same headings, captions (13 tables and 5 figures in the manuscript; 41 tables and 9 figures in the appendix), table rows, image file names, footnotes, citation keys (94, all in `references.bib`) and markers as ES.
- Anonymity: no "e1f9b448", "forecast-2027" or freeze digests in the manuscript, appendix or highlights.
- Highlights 74–82 characters.

## Marker count (English version)

| File | [Q1 GAP] | [PENDING] |
|---|---:|---:|
| manuscrito_IJF_en.md | 0 | 8 |
| apendice_en_linea_en.md | 0 | 2 |
| title_page_en.md | 0 | 9 |
| cover_letter_IJF_en.md | 0 | 12 |
