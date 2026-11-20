# Changes in the v3 rewrite of the IJF manuscript, English version (20 Nov 2026)

The English version is a one-to-one mirror of the Spanish v3 (`manuscrito_IJF_es.md` v7bc4ac31, `apendice_en_linea_es.md` v537baf42). All content changes below originate in the Spanish rewrite (see `cambios_v3_es.md`); this file records them in English and adds the decisions specific to the English version.

## Verification (by script)

- **Figures:** the set of numbers in each EN file equals the set in the corresponding ES file converted to English format (decimal comma → point; thousands point → comma): 0 discrepancies in the manuscript, the appendix, the highlights and the title page (except the intended prose word count of the title page; see below).
- **Structure:** same headings (41 numbered in the main text; A.1–A.24 in the appendix), same table captions (13 + 43), figure captions (5 + 7), image paths (`](<figuras/…png>)` form), table rows, footnotes and markers; 205 cross-references to sections, tables, figures and A.x subsections, all resolved; reference counts by number identical to ES.
- **Citations:** 94 cited keys, identical to ES, all present in `references.bib` (94 entries); APA 7 (en-US) bibliography with 94 entries in the `.docx`.
- **Abstract:** 139 words; **highlights:** 5 bullets, 74–82 characters.

## By section (mirrors the Spanish rewrite)

- **Abstract:** literal English text of the specification, with one correction: "Stratified conformal intervals achieved the best interval score" → "… at almost all levels" (N7 is the exception: interval score 79.8 versus 79.7 for AutoETS).
- **Highlights:** redone (5 bullets): naïve = lag; global > persistence and per-series methods at the cell level; exogenous features period-dependent; stratified conformal with the lowest interval score (except N7); 2×2 design frozen for 2027.
- **§1 Introduction:** new study paragraph (global models, per-series methods, factorial design); persistence R² 0.967–0.972; contributions 1–5 per the specification.
- **§2 Literature:** reorganized into 2.1–2.5 and shortened, with no citation removed; MCB (Koning et al., 2005) added.
- **§3.3:** winsorization only for training; all evaluation against observed enrollment; statement on the earlier version that used the clipped actual (1,430 rows 2018–2026; +0.03% to +0.34% per year; Appendix A.15).
- **§4.1–4.2, §4.4:** origin scope updated (Sections 5.2–5.10); matching rates of the evaluated cells; shortened.
- **§4.7:** rewritten: main model (C49, chosen for continuity, `shap` versions), per-series benchmarks (`statsforecast` 2.1.1: RWD, AutoETS, AutoARIMA, Theta, Comb), lags-only global model (Lrez), factorial design C49/Crez/L49/Lrez, reconciliation; no [Q1 GAP].
- **§4.8:** metrics shortened; DM between groups with CR1 errors clustered by institution, MCB/Nemenyi (liberal), HLN at N1, IS and MSIS; no [Q1 GAP].
- **§4.9:** calibration with observed residuals; no [Q1 GAP].
- **§5.1:** note to Table 3 on the clipped value of the 2025 holdout (+22.87% with the observed value).
- **§5.2–5.4:** Tables 4, 5, 6 and 7 with observed values and *p*-values (Table 7 = holdout cascade, formerly Table 10); institution table moved to Appendix A.24 (Table A.43).
- **§5.5 (new):** comparison with per-series benchmarks and the global model (Table 8). **§5.6 (new):** factorial design (Table 9) and year-by-year breakdown (L-02).
- **§5.7:** Table 10 (coverage, four 2027 bands, recalibration 92.49%) and new Table 11 (IS/MSIS), with the N7 exception. **§5.8:** Table 12 = four-arm target-encoding experiment; note I-05. **§5.9:** region and explainability merged; SHAP caveat.
- **§5.10:** "2027 forecasts (*ex ante*; freeze in progress)"; Table 13 with six forecasts (C49 761,058; Crez 767,934; L49 760,672; Lrez 768,499; persistence 741,615; Comb 746,696); composition; bands; non-conformal range 719,308–777,914; simple benchmarks; protocol H1–H5 (detail in A.14). No tag or repository named.
- **§6:** 6.1 updated; 6.3 shortened; **6.4 (new)** "What the model contributes"; 6.5 rewritten (P-04 closed, single test year, clipped value corrected, 113 duplicates, Ñuble, reconciliation, shocks); 6.6 updated. **§7** rewritten with the new thesis.
- **Data availability:** 2027 forecasts of the 2×2 design and of the benchmarks, protocol and program with their digests, published with the freeze.
- **Appendix:** A.7, A.9, A.11, A.13 and A.14 (protocol v2) updated; new A.15–A.24; 43 numbered tables.
- **Title page:** length and number of tables; data availability.

## Body table numbering (same as ES)

| Before | Now |
|---|---|
| Table 7 (by institution) | Appendix, Table A.43 |
| Table 8 (coverage) | Table 10 |
| Table 9 (target encoding) | Table 12 |
| Table 10 (holdout cascade) | Table 7 |
| — | Tables 8, 9, 11 and 13 (new) |

## Decisions specific to the English version

1. **Cover letter rewritten** around the new thesis (robust gain of the global design; period-dependent value of exogenous features), the prospective 2027 test of the full 2×2 design with a prespecified protocol, and data and code upon acceptance (prediction files, protocol and evaluation program published with the freeze).
2. **Abstract wording:** the literal specification text uses "schedule" for *jornada*; the body uses "attendance mode", as in previous EN versions. The abstract was kept literal; harmonizing to "attendance mode" is an author decision.
3. **Model labels** C49, Crez, L49 and Lrez are kept as identifiers (identical to ES and to the frozen files), and are defined in §4.7.
4. **Localization:** three caption notes that only apply to the Spanish version were removed (Figure 1 and Figure 5 "labels use the Anglo-Saxon/Anglophone decimal separator"; Figure A.5 "axes labeled in English"); Spanish-style spaced em dashes were closed; percentages are written without a space (12.69%). The A.13 note on regenerating the Spanish figures with a decimal comma is kept, because it describes a pending task.
5. **Title page length:** ~8,900 words of prose by script count for the English text (the Spanish title page states ~10,700 with its own count; the same script gives 9,563 for the Spanish text).
6. **Title page markers:** 9 [PENDING] versus 10 [PENDIENTE] in ES, because the English working title is fixed in this version.
7. **Translation method:** the Spanish text was converted to English number format by script, translated section by section with model assistance under a fixed glossary and the previous EN version as translation memory, then verified by script (numbers, structure, citations, markers, cross-references) and reviewed by hand in the key sections (abstract, introduction and contributions, §4.7, §5.10, §6.4, §7, A.14). A professional language edit is still advisable.

## Marker count

| File | [Q1 GAP] | [PENDING] |
|---|---:|---:|
| manuscrito_IJF_en.md | 1 | 11 |
| apendice_en_linea_en.md | 0 | 18 |
| title_page_en.md | 0 | 9 |
| cover_letter_IJF_en.md | 0 | 12 |

The only [Q1 GAP] is the formal freeze of the 2027 forecasts (P-01).
