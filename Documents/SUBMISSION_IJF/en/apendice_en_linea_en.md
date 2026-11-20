---
title: "Online Appendix — When the naïve forecast is the lag: Evaluating program-level university enrollment forecasts in Chile"
lang: es-CL
---

<!-- Anonymized supplementary material for double-anonymous review. The figures come from the manuscript and from the technical documentation of the pipeline prepared by the author. -->

This appendix gathers the operational details and complementary results referred to in the manuscript. Tables and figures are numbered A.1, A.2, …; the forecast origins ("2025 origin" and "2026 origin") are defined in Section 4.1 of the manuscript. Unless otherwise indicated, the figures refer to the 2026 origin.

# A.1 Ingestion rules by source

Each source is processed separately and keeps its original granularity; ingestion does not join sources or impute across them, it only cleans, restructures and verifies that no information is lost.

**Enrollment (SIES).** Series 2007–2026, one row per program and year, with total and first-year enrollment by gender (women, men, non-binary or undefined).

**Table A.1.** Ingestion rules for the SIES enrollment database.

| # | Rule | Detail |
|---:|---|---|
| 1 | Year | Last four characters of the year field |
| 2 | Missing values before subtracting | Total and first-year enrollment by gender are filled with zero before operating, so that a subtraction involving a missing value does not produce a silent missing value |
| 3 | Continuing students | Total minus first-year, by gender, bounded at zero |
| 4 | Universe | Undergraduate only |
| 5 | Code-based key | From the institution-campus-program-attendance mode-version code, the institution and program (base program code) are extracted; the latter does not change with campus or curriculum |
| 6 | Long format | Each program is expanded into up to six rows (3 genders × 2 student statuses); rows with zero enrollment are dropped |

Checks: exact conservation of undergraduate enrollment at three levels (source total, sum of the six columns and sum in long format: 22,357,425 in all three); coverage of the code-based key of 96.5% of undergraduate rows; zero nulls and valid categories.

**Tuition fees, scores and duration (CNED, INDICES).** A total of 19 columns are selected (tuition fees, enrollment fee, degree fee, duration, admission and cut-off scores) and undergraduate rows are kept (215,743 of 260,307). The current edition covers 2005–2026; 2026 has 10,572 rows versus 10,865 in 2025.

**Academic staff and infrastructure (CNED, INDICES).** Counts by academic degree, contract type, hours and sex, and m² of land, built area and classrooms, aggregated to institution × region × year, with a conservation check on floor area before and after aggregation. Coverage 2005–2025.

**Regional GDP (Banco Central de Chile).** Conversion to long format year × region, excluding subtotals and extra-regional GDP, with an explicit translation of the 16 region names into the canonical nomenclature. The series is quarterly GDP by region in volume at previous year's chained prices, spliced series, 2018 reference (billions of chained pesos; Banco Central de Chile, 23-04-2026 edition, preliminary figures, latest observation from the fourth quarter of 2025), delivered in annual rows 2013–2025; the 2026 value is carried forward from 2025.

**Regional unemployment rate (INE, Encuesta Nacional de Empleo).** The both-sexes series is used, which is the official rate weighted by the labor force, and it is annualized as the average of the year's published rolling quarters. For 2018–2024, 12 rolling quarters are averaged; for 2025, 10. INE publishes monthly rolling quarters; the 10 for 2025 are those beginning between January and October, and those beginning in November and December are missing, which in complete years do enter the average. The pipeline control only flags years with fewer than four periods.

**First-year retention and employability (mifuturo.cl).** Year-by-year extraction with declared sheet, header row and column order; assignment of the missing institutional code in 2020 by normalized name; "s/i" (no information) as missing; retention and employability bounded in [0, 1].

# A.2 Consolidation, key normalization and coverage

**Universe.** From the processed SIES data, 2018–2026 and the three university categories are kept: 127,424 rows from 60 institution codes. Separately, the 2017–2026 university universe is kept, used to build the lag.

**Normalization.** A single normalization of key strings (upper case, no accents or periods, single spaces). CNED and mifuturo.cl institutions are mapped to the SIES code by normalized name, with unification of acronyms, expansion of abbreviations and five auditable manual exceptions; coverage: academic staff, infrastructure and tuition fees 60 of 60, retention 58 of 60.

**Join.** All sources are left-joined onto SIES after being aggregated to the exact granularity of their key, with a no-inflation check (127,424 rows in and 127,424 rows out).

**Table A.2.** Coverage of the secondary sources measured from SIES, before carry-forward.

| Source | SIES combinations | With data | Coverage |
|---|---:|---:|---:|
| GDP | 144 | 120 | 83.33% |
| Unemployment | 144 | 128 | 88.89% |
| Academic staff | 1,205 | 842 | 69.88% |
| Infrastructure | 1,205 | 848 | 70.37% |
| Retention | 22,990 | 4,844 | 21.07% |
| Tuition fees | 30,702 | 19,432 | 63.29% |

**Known regional normalization defect (Ñuble).** Because of an order-of-operations defect in the consolidation, the repair of the Ñuble region name was not applied before the joins with academic staff, infrastructure and tuition fees: its 3,474 rows (2.73% of the universe) enter those joins without a region code, so academic staff and infrastructure fall back to the global median and tuition fees are imputed through the cascade. GDP is re-joined after the correction. The correction has been identified and will be evaluated in the next methodological version, without modifying the 2027 forecast; its effect on the error has not been measured.

**Table A.3.** Rows by processing stage. S1: SIES undergraduate, all institutions; S2: universities 2018–2026; S3: consolidated table; S4: with target; S5: modeling panel.

| Year | S1 | S2 | S3 | S4 | S5 |
|---:|---:|---:|---:|---:|---:|
| 2018 | 34,653 | 15,167 | 15,052 | 14,541 | 9,505 |
| 2019 | 34,090 | 14,738 | 14,652 | 14,070 | 9,424 |
| 2020 | 33,466 | 14,317 | 14,232 | 13,817 | 9,321 |
| 2021 | 34,527 | 14,312 | 14,212 | 13,795 | 9,230 |
| 2022 | 34,950 | 14,330 | 14,231 | 13,904 | 9,161 |
| 2023 | 35,643 | 14,099 | 14,022 | 13,682 | 9,038 |
| 2024 | 34,984 | 13,679 | 13,602 | 13,328 | 9,176 |
| 2025 | 34,569 | 13,475 | 13,401 | 13,055 | 9,043 |
| 2026 | 34,169 | 13,307 | 13,239 | 12,967 | 9,069 |
| Total | 311,051 | 127,424 | 126,643 | 123,159 | 82,967 |

The drops are explained as follows: S1→S2 excludes non-university institutions (deliberate); S2→S3 removes 781 exact duplicates (0.12% of enrollment, with no effect on lag or target); S3→S4 removes 3,484 rows with no lag or a zero lag; S4→S5 removes 25,364 rows with a lag below ten and collapses 14,828 rows that share a cell (without removing enrollment). No criterion depends on the prediction error; all are structural and prior to modeling, but they are not neutral: what is excluded—small and new cells—is what grows most. The panel retains between 96.0% and 98.0% of each year's university enrollment.

# A.3 Hierarchical imputation and carry-forward of exogenous variables

**Table A.4.** Imputation layers. Each layer resolves only what the previous one left empty.

| Layer | Variables | Rule |
|---|---|---|
| 1 · Temporal | Academic staff and infrastructure | Linear interpolation over the year within institution-region, with forward and backward fill |
| 2 · Hierarchical | Tuition fees, scores, duration, retention, employability | Median (institution, program) → (institution, field, year) → (field, year) |
| 2.5 · Region and program | The same | (region, program, year) → (region, program) → (program, year) → (program) |
| 2.7 · Institution | The same | (institution, year) → (institution) |
| 3 · Terminal | All | Global median |

Of the 1,292,058 missing values in the consolidated table, those for academic staff and infrastructure (590,785) are resolved 59.0% by the temporal layer and 41.0% by the global median, which contributes no signal; those for tuition fees, scores and retention (701,273) are fully resolved in the hierarchical layer, with the same program in other years or the institution's field. Layers 2.5 and 2.7 resolve nothing in this run and are kept as a safety net. The imputation indicator enters the model; in the modeling panel, 70.9% of rows have at least one imputed value (67.3% at the 2025 origin).

**Carry-forward.** Regional GDP and unemployment are not imputed. If a source has not published the last year of the window, its regional values for the last published year are repeated and the carry-forward is recorded (source, last published year and years carried forward). At the 2026 origin, both were carried forward from 2025 to 2026 (16 regional values each); academic staff and infrastructure for 2026 repeat 2025 through the temporal layer, and retention and employability for 2026 are the historical median of each institution-program. The 2026 SIES edition revised 2025 university enrollment from 731,981 to 732,034 (+53).

# A.4 Lag key: composition and checks

The lag is computed on the 2017–2026 university universe, before deduplication, with the fine → code → intermediate cascade (Table 2 of the manuscript). The lag is the previous year's value only if that year is exactly $t-1$; if a cell-year has more than one code, the one with the largest enrollment is used.

**Table A.5.** Composition of the lag by matching level on the university universe from 2018 onward (by cell, before the minimum-lag filter).

| Lag source | Cells | % of enrollment | Median rate | % with rate < −0.8 | Median lag-to-cell ratio |
|---|---:|---:|---:|---:|---:|
| Fine | 102,036 | 97.80% | 0.000 | 1.16% | 1.000 |
| Code | 1,041 | 0.68% | 0.000 | 1.44% | 1.000 |
| Intermediate (scaled) | 4,198 | 0.80% | +0.194 | 0.45% | 0.837 |
| No lag | 3,386 | 0.71% | — | — | — |

**Regression check.** At the code and intermediate levels, the lag-to-cell ratio should be around one and the median rate should not be negative. A median rate at the intermediate level close to −0.87 with a ratio close to 8 indicates that share-based scaling was not applied: this is exactly the signature of the defect described in Section 5.1. The code-based key recovers 42,641 enrollments in 1,041 cells. In the modeling panel, the composition is 97.94% fine, 0.84% code and 1.22% intermediate. Restricted to the cells evaluated in 2019–2026, matching is at the fine level for 98.10% of cells (98.89% of enrollment), by code for 0.66% (0.56%) and at the intermediate level for 1.25% (0.56%).

**Performance by lag source (2026 origin).** Of the 50 worst cells by absolute error, 49 in the 2019–2025 OOF and all 50 on the 2026 holdout have a fine-level lag. The fallbacks account for 1.1% of enrollment and have a higher relative error, but they do not explain the tail of the distribution: the worst cells are genuine program contractions.

**Table A.6.** Performance by lag source in the 2019–2025 OOF and on the 2026 holdout (2026 origin).

| Set | Lag source | Cells | WAPE | WAPE pers. | Skill | RelMAE |
|---|---|---:|---:|---:|---:|---:|
| OOF 2019–2025 | fine | 63,154 | 14.33% | 14.79% | −3.24% | 0.969 |
| OOF 2019–2025 | code | 420 | 17.93% | 17.41% | −14.41% | 1.030 |
| OOF 2019–2025 | intermediate | 819 | 31.08% | 32.44% | +27.80% | 0.958 |
| Holdout 2026 | fine | 8,909 | 11.99% | 12.81% | +14.25% | 0.936 |
| Holdout 2026 | code | 63 | 16.84% | 15.82% | −15.55% | 1.064 |
| Holdout 2026 | intermediate | 97 | 27.29% | 31.93% | +29.10% | 0.855 |

*Note:* pers. = persistence. RelMAE = MAE of the model divided by the MAE of persistence on the same set (Section 4.8 of the manuscript).

**Properties of the scaling.** (i) $y_{t-1}(1+\text{rate})$ returns exactly the cell's enrollment, so the reconstruction is not distorted; (ii) the share is less than or equal to one, so the fallback never inflates; (iii) if group and cell coincide, the share is one; (iv) the lag remains on the cell's scale and can feed market variables that sum lags.

# A.5 Model variables

**Table A.7.** Column groups of the modeling panel.

| Group | Columns | Notes |
|---|---|---|
| Categorical (4) | Region, institution, program, field | Target encoding fitted within the fold |
| Time (1) | Year | |
| Grain (6) | Gender; daytime, other, blended, evening attendance mode; first-year status | Reference categories: distance, continuing |
| Lag (2) | Lagged enrollment; lag source | Lag in $\log(1+x)$; the source is for traceability and does not enter the model |
| Target (1) | Growth rate | Arcsinh of the winsorized rate (cut-offs −0.79 and +1.29) |
| Macroeconomic (3) | GDP, unemployment, enrollment over GDP | GDP in $\log(1+x)$ |
| Price and selectivity (11) | Tuition fee, enrollment fee, 3 scores, 3 cut-off scores, duration, regional relative tuition, relative selectivity | Amounts in $\log(1+x)$ |
| Faculty (7) | Number of academic staff, 5 ratios, faculty-to-student ratio | |
| Infrastructure (1) | Student density per m² | $\log(1+x)$ |
| Market (3) | Competitive density, lagged concentration, lagged regional share | |
| Retention (1) | First-year retention | |
| Classification and accreditation (7) | Institution type and accreditation indicators | |
| Traceability (1) | Imputation indicator | Enters the model |
| Shock indicators (3) | Level, dispersion, relapse | Two constant at zero |

**Variables with information from the evaluated year.** Student density per m², the faculty-to-student ratio and enrollment over GDP use year-$t$ enrollment aggregated by institution-region or region; they constitute a declared exception to the anti-leakage rule (Section 6.5 of the manuscript). Competitive density, relative tuition and relative selectivity use the year-$t$ program supply, tuition fees and scores, which are published before the enrollment period.

# A.6 Empirical detection of shock years

**Table A.8.** Annual target statistics and classification (2026 origin). Normal reference years: 2018, 2019, 2023, 2024, 2025 and 2026.

| Year | Mean | SD | % negative rates | Z mean | Z SD | Classification |
|---:|---:|---:|---:|---:|---:|---|
| 2018 | 0.0132 | 0.3090 | 47.2% | | | Normal |
| 2019 | −0.0070 | 0.2876 | 49.0% | | | Normal |
| 2020 | −0.0384 | 0.2934 | 54.5% | −4.95 | −0.52 | Level shock |
| 2021 | 0.0126 | 0.3292 | 45.1% | −0.02 | +1.36 | Not detected |
| 2022 | −0.0270 | 0.3202 | 55.5% | −3.85 | +0.89 | Level shock |
| 2023 | 0.0176 | 0.3356 | 50.3% | | | Normal |
| 2024 | 0.0121 | 0.3072 | 48.5% | | | Normal |
| 2025 | 0.0210 | 0.2983 | 46.2% | | | Normal |
| 2026 | 0.0200 | 0.2823 | 44.7% | | | Normal |

The relapse criterion is not triggered: the two candidate years with a negative aggregate change (2020 and 2022) are already classified as level shocks. The level-shock indicator equals one in 18,482 rows. Note that the set of normal years includes the holdout year (an imperfection declared in Section 6.5).

# A.7 Informed benchmarks and candidates

**Table A.9.** Benchmarks and final model on the 2026 holdout, target scale (arcsinh of the rate).

| Model | Description | RMSE | MAE | R² |
|---|---|---:|---:|---:|
| B0 | Training median (≈ persistence in rates) | 0.2830 | 0.2015 | −0.0050 |
| B1 | Historical institution-program mean | 0.2929 | 0.2093 | −0.0767 |
| B2 | Ridge with the lag only | 0.2831 | 0.2021 | −0.0057 |
| B3 | Ridge with 43 variables (α = 10) | 0.2773 | 0.2008 | 0.0350 |
| Optimized CatBoost | Final model | 0.2605 | 0.1867 | 0.1480 |

*Note:* training target scale (clipped rate). With the observed rate, the final model's R² on the rate on the 2026 holdout is 0.141.

**Table A.10.** Boosting candidates and Random Forest in cross-validation (seven folds, 2026 origin).

| Model | Untuned CV RMSE | Mean R² on the rate | Tuned CV RMSE | Optimization time |
|---|---:|---:|---:|---:|
| CatBoost | 0.2964 ± 0.0174 | 0.086 | 0.2949 | 58.5 min |
| XGBoost | 0.2972 ± 0.0178 | 0.081 | 0.2933 | 15.0 min |
| LightGBM | 0.2980 ± 0.0179 | 0.076 | 0.2943 | 63.9 min |
| Random Forest | 0.3013 ± 0.0178 | 0.056 | — | — |

Adding an institution cluster (K-means on nine institutional variables, K = 4 by silhouette) as a variable was also evaluated; the cross-validation RMSE did not change (0.2980 in both cases) and it was discarded.

# A.8 Hyperparameters and search space

Optuna with the TPE sampler and a fixed seed, median pruning (no pruning in the first 10 trials or before the third fold), 50 trials per model, objective = mean RMSE over the seven folds on the arcsinh scale.

**Table A.11.** Search space and optimum for CatBoost (2026 origin).

| Hyperparameter | Range | Optimum |
|---|---|---:|
| Iterations | 200–2,000, step 100 | 2,000 |
| Learning rate | 0.005–0.15, logarithmic | 0.0376 |
| Depth | 4–10 | 7 |
| L2 regularization | 0.01–30, logarithmic | 1.746 |
| Bagging temperature | 0–1 | 0.546 |
| Border count | 32–255 | 183 |

The number of iterations sits at the upper limit of the range, so the optimum could lie outside it. Seed 42 in all declared sources of randomness; bit-for-bit equality across machines has not been verified. Versions of `shap`: 0.45.1 in the 2025-origin run and 0.54.1 in the 2026-origin run. The choice of CatBoost was kept for continuity of method between both runs and has no performance basis (Section 4.7 of the manuscript).

# A.9 Performance by year and by region: details

**Differences between origins.** The 2019 to 2025 OOF figures of the 2026 origin do not coincide exactly with those of the 2025 origin for three reasons: the 2026 SIES edition slightly revises previous years, the hyperparameters were chosen on one more fold, and the target encoding is fitted with one more year of data.

**Table A.12.** Persistence by year in the OOF (2026 origin), complementing Table 5 of the manuscript, against observed enrollment.

| Year | WAPE pers. | Model RelMAE |
|---:|---:|---:|
| 2019 | 14.30% | 1.0041 |
| 2020 | 15.74% | 0.9333 |
| 2021 | 17.08% | 0.9073 |
| 2022 | 16.35% | 0.9971 |
| 2023 | 15.64% | 1.0360 |
| 2024 | 13.96% | 0.9768 |
| 2025 | 13.23% | 0.9409 |
| 2026 | 13.09% | 0.9372 |

**Table A.13.** Performance by region in the 2019–2026 OOF (2026 origin), observed enrollment.

| Region | n | WAPE | WAPE pers. | Skill | R² | R² pers. | Aggregate error |
|---|---:|---:|---:|---:|---:|---:|---:|
| Los Ríos | 2,157 | 11.99% | 12.54% | −3.32% | 0.9657 | 0.9668 | +2.19% |
| Maule | 3,310 | 12.47% | 13.12% | +3.80% | 0.9668 | 0.9654 | +2.85% |
| Biobío | 7,943 | 12.60% | 13.18% | +1.97% | 0.9686 | 0.9680 | +0.95% |
| La Araucanía | 4,853 | 13.19% | 13.23% | +0.88% | 0.9646 | 0.9643 | +1.87% |
| Valparaíso | 8,937 | 13.59% | 14.18% | +18.24% | 0.9626 | 0.9542 | +1.88% |
| Arica y Parinacota | 1,533 | 14.65% | 14.30% | −9.17% | 0.9588 | 0.9622 | −0.37% |
| Metropolitana | 28,312 | 14.78% | 15.08% | −4.26% | 0.9606 | 0.9622 | +2.56% |
| Coquimbo | 3,009 | 15.07% | 16.33% | +11.30% | 0.9501 | 0.9438 | +1.46% |
| Antofagasta | 3,046 | 15.57% | 16.86% | +15.42% | 0.9575 | 0.9497 | +3.16% |
| Ñuble | 2,002 | 15.64% | 16.14% | +6.03% | 0.9488 | 0.9455 | +0.51% |
| Los Lagos | 2,912 | 16.41% | 17.44% | +5.35% | 0.9431 | 0.9399 | +3.63% |
| Atacama | 1,202 | 16.57% | 17.03% | −1.89% | 0.9387 | 0.9398 | +1.28% |
| Magallanes | 848 | 17.69% | 17.99% | −2.00% | 0.9331 | 0.9345 | +1.75% |
| Tarapacá | 1,992 | 18.69% | 18.56% | −3.87% | 0.8943 | 0.8982 | +3.71% |
| Lib. Gral. B. O'Higgins | 1,093 | 18.92% | 24.64% | +44.16% | 0.9513 | 0.9127 | +4.43% |
| Aysén | 313 | 25.50% | 25.83% | +9.21% | 0.8463 | 0.8307 | +9.85% |

The model's WAPE is lower than that of persistence in 14 of the 16 regions, but skill is negative in six: in those regions a few large errors dominate the squared error.

![**Figure A.1.** WAPE by region in the retrospective OOF predictions 2019–2026 (2026 origin). Regions are ordered from lowest to highest error. Observed enrollment.](<figuras_en/fig04_wape_por_region.png>)

**Table A.14.** Performance by attendance mode on the 2026 holdout (2026 origin), observed enrollment.

| Attendance mode | Base 2025 | Actual 2026 | Predicted 2026 | Actual growth | Predicted growth |
|---|---:|---:|---:|---:|---:|
| Daytime | 631,393 | 650,477 | 649,653 | +3.02% | +2.89% |
| Distance | 38,565 | 43,050 | 46,621 | +11.63% | +20.89% |
| Evening | 41,498 | 38,165 | 40,031 | −8.03% | −3.54% |
| Blended | 8,265 | 8,954 | 9,579 | +8.34% | +15.90% |
| Other | 1,371 | 969 | 1,218 | −29.32% | −11.17% |

The model extends the trend of the non-daytime modes and does not capture their turning points; with attendance mode as an indicator without a temporal interaction, it has no means to do otherwise. The aggregate is accurate because the errors offset each other.

# A.10 Explainability: complementary results

**Table A.15.** SHAP importance (mean absolute value) of the five main variables.

| # | Variable | 2026 origin | 2025 origin |
|---:|---|---:|---:|
| 1 | Program name (target encoding) | 0.0533 | 0.0546 |
| 2 | First-year student status | 0.0488 | 0.0514 |
| 3 | Lagged enrollment | 0.0364 | 0.0394 |
| 4 | Evening attendance mode | 0.0299 | 0.0289 |
| 5 | Lagged share of the program's regional enrollment | 0.0229 | 0.0249 |

*Note:* 2026 origin, on the 92,036 exported rows (retrospective, lag-base and forecast rows). At the 2025 origin, restricted to the cells of the 2026 forecast with official data, the order was identical (0.0528; 0.0491; 0.0409; 0.0305; 0.0291). The lag appears third partly because of scale: it enters in logarithms and its main effect lies in the reconstruction of the level, not in the rate. The macroeconomic variables and the three variables with contemporaneous enrollment are not among the fifteen most influential. There is no usable relationship between the magnitude of a cell's contributions and its error: SHAP is not a confidence signal.

![**Figure A.2.** Distribution of the SHAP contributions of the five most influential variables (2026 origin). The dashed line marks zero contribution. Variable labels correspond to internal column names. Attributions from the final model of the 2026 origin (trained with 2018–2026) calculated over the OOF 2019–2026 rows, that is, within-sample; these are not attributions from the OOF models.](<figuras_en/fig10_shap_top5_distribucion.png>)

![**Figure A.3.** Average absolute value of the SHAP contributions by subgroup of student status, attendance mode, and gender. Attributions from the final model of the 2026 origin (trained with 2018–2026) calculated over the OOF 2019–2026 rows, that is, within-sample; these are not attributions from the OOF models.](<figuras_en/fig11_shap_por_subgrupo.png>)

![**Figure A.4.** Mean, signed SHAP contribution by subgroup of student status, attendance mode, and gender; the line marks zero contribution. Unlike Figure A.3, contributions of opposite sign offset each other. Attributions from the final model of the 2026 origin (trained with 2018–2026) calculated over the OOF 2019–2026 rows, that is, within-sample; these are not attributions from the OOF models.](<figuras_en/fig11b_shap_por_subgrupo_con_signo.png>)

![**Figure A.5.** SHAP decomposition of two OOF cells: the first, in file order, with enrollment of at least 100 and absolute error no greater than 2 ("well predicted"), and the one with the largest absolute error ("poorly predicted"). The titles identify institution, program, region, attendance mode, gender, and student status; this is aggregated public data, with no individuals. Attributions from the final model of the 2026 origin (trained with 2018–2026) calculated over the OOF 2019–2026 rows, that is, within-sample; these are not attributions from the OOF models.](<figuras_en/fig12_caso_estudio_shap.png>)

# A.11 Conformal intervals: details

**Band factors.** The band factor by aggregation level (2025 origin) is ×0.72–×1.09 at N2 and ×0.49–×1.54 at N8. Within a level, stratification by size produces the expected monotonicity: at N3, ×0.34–×1.38 for groups of fewer than 100 students versus ×0.87–×1.09 for those of more than 2,000. The aggregate strata use the size bands <100, 100–500, 500–2,000 and >2,000, and the band is $[\hat{y}e^{-q_{\text{hi}}}, \hat{y}e^{-q_{\text{lo}}}]$, with $q$ the conformal quantiles of $\log(\hat{y}/y)$.

**Coverage by level in the 2026 validation (2025 origin).** 98.1% (N2), 96.6% (N3), 94.8% (N4), 91.8% (N5), 92.8% (N6), 92.6% (N7) and 92.3% (N8, by group), against a 90% target. Coverage by cell is that of Table 10 of the manuscript (92.53%).

**2026 origin and 2027 forecasts.** Against observed enrollment, the bands previously calibrated with residuals of the winsorized rate cover 92.26% of the cells of the 2026 holdout (median width 36.5); recalibrated with observed residuals (OOF 2019–2025), 92.49% (median width 36.6). The bands frozen with the 2027 forecasts are calibrated with each model's observed OOF 2019–2026 residuals (Table A.39). The median band by institution of the recalibrated main model measures 20.62% of the forecast, and the non-conformal national range runs from 719,308 to 777,914, built with the aggregate OOF errors against observed enrollment, from −2.17% (2021) to +5.80% (2022). With the earlier calibration, those figures were 20.4% and 716,850 to 775,499.

**Calibrating to measure and calibrating to publish.** To measure coverage, only residuals from years prior to the evaluated year are used; to issue published bands, the full available OOF is used. If a stratum has fewer than 30 residuals, the band of the whole level is used, and if that is not enough either, no interval is issued.

# A.12 Complementary figures

![**Figure A.6.** Distribution of the residuals (observed minus forecast enrollment) in the 2019–2026 OOF, truncated at ±200 (left), and quantile-quantile plot against the normal distribution (right). The heavy tails justify not assuming normality for the intervals. Observed enrollment.](<figuras_en/fig01_distribucion_residuos.png>)

![**Figure A.7.** Forecast versus observed enrollment at the eight levels of the aggregation cascade, 2019–2026 OOF (2026 origin), with observed enrollment. The number of N8 groups (73,349) differs from the number of OOF rows (73,462) because there are 113 surplus rows in 88 cells (two institutions; 2019–2021 and 2024), arising from several campuses in the same region or from curriculum versions, that inherit the cell total; see A.13.](<figuras_en/fig05_macro_a_micro.png>)

![**Figure A.8.** Calibration by size decile defined by the lag (information available when forecasting), 2019–2026 OOF for the 2026 origin (73,462 rows, includes the 2026 holdout): mean observed and forecast enrollment (left) and relative bias (observed − forecast)/observed (right; negative = overprediction). Bias from Q1 to Q10: +1.25%; +0.25%; −1.70%; −1.66%; −1.64%; −2.48%; −2.40%; −2.78%; −1.87%; −2.57%, that is, a mild and even overprediction of 1.6% to 2.8% from the third decile onward, which reflects the aggregate overprediction of the OOF and not a size-calibration problem.](<figuras_en/fig07_calibracion.png>)

![**Figure A.9.** The same calibration with deciles defined by observed enrollment. Bias (observed − forecast)/observed from Q1 to Q10: −94.44%; −23.77%; −10.15%; −4.46%; −1.36%; −0.74%; −0.23%; −0.11%; −0.32%; −0.43%. The extreme bias in the lower deciles is regression to the mean, because it conditions on the outcome.](<figuras_en/fig07b_calibracion_deciles_observados.png>)

# A.13 Known inconsistencies in the supporting material

They are declared for transparency; none alters the figures in the manuscript.

1. **Sign convention and basis of the aggregate error.** The aggregate error is defined as forecast minus observed value. For 2021, against observed enrollment, it is −2.17% (654,899 forecast versus 669,403 observed; Table 5 and Figure 3 of the manuscript); against the value reconstructed with the clipped rate it was −1.86%.
2. **Duplicated rows in the fine key.** In the OOF there are 113 surplus rows in 88 cells, from two institutions (2019–2021 and 2024), arising from several campuses within the same region or from curriculum versions; they inherit the cell total. The 2026 holdout and the 2027 forecasts are not affected. The sensitivity without those rows, with observed enrollment, is in the note to Table A.23. This will be corrected in the next methodological version. \[PENDING: author confirmation to include this note\]
3. **Model metadata.** The metadata of the 2026-origin model carried labels inherited from the previous run: the number of folds (5 instead of the 7 actually run) and the labels of the holdout and of the forecast assumptions. These were corrected before the freeze, without changing any numeric value or the predictions.
4. **Figures.** The figures were regenerated with observed enrollment, with a comma decimal separator and Spanish labels in the Spanish version and with a decimal point and English labels in this English version; Figure 3 of the manuscript uses the observed 2018 enrollment (653,163) instead of the sum of that year's lags, and the linear regression in Figure 5 uses the same corrected series (−1.53%).

# A.14 Evaluation and freeze protocol for the 2027 forecasts

Status: *ex ante*, frozen. The protocol (version 2.2) was approved and frozen on 20 November 2026 together with the six forecasts, before the official publication of 2027 enrollment. Any analysis not listed in it will be reported as unplanned.

1. **Frozen forecasts:** C49 (761,058, unchanged, with its declared basis: +2.62% over 741,615 and 75 cells with a clipped lag), Crez (767,934; +3.55%), L49 (760,672; +2.57%) and Lrez (768,499; +3.63%)—all with 90% stratified conformal bands recalibrated on their observed 2019–2026 OOF residuals, persistence (F0) and national Comb (FN, N1 only). Universe: 9,069 cells.
2. **Observed actual:** the first release of the SIES 2027 enrollment database, downloaded within the following 30 days and with its SHA-256 digest recorded; reconstructed with the panel's ingestion rules; **without any winsorization or adjustment whatsoever**; with a prior check against the official report's total.
3. **Matching:** primary by cell key with program name; secondary by program code; forecast cells with no 2027 enrollment and new programs are left out of the main analysis, and their number and enrollment are reported, together with the coverage of 2027 enrollment.
4. **Metrics and levels:** N1–N8 by ascending sum; WAPE, RelMAE relative to F0, skill relative to F0, percentage within ±10% and aggregate error; for the intervals, coverage with a 95% binomial confidence interval, median width, IS ($\alpha = 0.10$), MSIS and, as a reference, a non-stratified conformal.
5. **Hypotheses:** DM between groups with standard error clustered by institution, two-sided, $\alpha = 0.05$, primary absolute loss and secondary squared loss, without multiplicity correction and reported regardless of outcome.

**Table A.16.** Pre-specified hypotheses of the 2027 evaluation protocol.

| ID | Question | Comparison | Primary level | Secondary levels |
|---|---|---|---|---|
| H1 | Do the models outperform persistence? | C49 − F0, Crez − F0, L49 − F0 and Lrez − F0 | N8 | N2, N5 |
| H2 | Do the exogenous variables contribute? | C49 − Crez and L49 − Lrez | N8 and N2 (both primary) | N5 |
| H3 | Does the algorithm matter? | C49 − L49 and Crez − Lrez | N8 | N2, N5 |
| H4 | National total | Aggregate error of the four models, F0 and FN | N1 | — (descriptive: a single year) |
| H5 | Band calibration | Coverage of the four models against the 90% nominal level | N8 | N2–N7 |

The reading of H2 is fixed in advance: if at N8 the exogenous variables do not improve the result with any algorithm, the 2026 result is repeated; if they improve at N2 with both, the 2019–2025 result is repeated; any other combination is reported as such, without reinterpreting it. The comparison is concrete: C49 and L49 forecast +2.62% and +2.57% over 741,615, and Crez and Lrez +3.55% and +3.63%, with the difference concentrated in first-year students (−0.54% and −0.07% versus +1.82% and +2.93%).

6. **Failure and calibration criteria:** a model does not outperform persistence if its RelMAE at N8 is greater than or equal to one. The bands are classified by model and level, using the Wilson interval, with an asymmetric criterion: undercoverage if coverage is less than 88%, calibrated between 88% and 95%, and conservative above 95%. The criterion was fixed after a dry run of the evaluation program on 2026 and before the freeze; in that test, all four models were calibrated at N8 (C49 92.49%, Crez 93.25%, L49 92.25%, Lrez 92.31%), and at N2–N7 (descriptive) Crez was conservative at N2–N4, L49 at N2, and Lrez at N3. No 2027 result modifies the frozen forecasts.
7. **Execution:** an evaluation program frozen within the same package, dry-run tested on the 2026 holdout; results published within the 60 days following the SIES release, with the digest of the actual file used and the list of deviations.
8. **Freeze:** carried out on 20 November 2026 by means of an annotated tag in a public repository with the SHA-256 digests of the predictions, the evaluation protocol, and the evaluation script \[identifiers omitted for double-blind review; provided to the editor in the cover letter\]. If a defect appears afterward, a new version is created and both are reported.

The time-stamped deposit with a DOI will be reported in the accepted version. \[PENDING: Zenodo DOI\]

# A.15 Evaluation against observed enrollment: winsorization diagnostic

The training target clips the growth rate at its 1st and 99th percentiles; an earlier version of the evaluation also reconstructed the "actual" value using that clipped rate. The table compares, by year, the reconstructed value with the observed value (sum of the processed SIES over the cell's fine key). The predictions do not change. In the 2026 holdout, the observed value of the 9,069 cells sums to 741,615, the same as those cells in the raw SIES.

**Table A.17.** Clipped rows and difference between the value reconstructed with the clipped rate and the observed value, by year.

| Year | Rows | Clipped | With different actual | Winsorized actual | Observed actual | Difference | Difference % |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 9,505 | 217 | 190 | 651,273 | 653,163 | +1,890 | +0.29% |
| 2019 | 9,424 | 172 | 148 | 654,320 | 654,495 | +175 | +0.03% |
| 2020 | 9,321 | 159 | 130 | 637,304 | 637,998 | +694 | +0.11% |
| 2021 | 9,230 | 206 | 170 | 667,325 | 669,403 | +2,078 | +0.31% |
| 2022 | 9,161 | 246 | 206 | 660,215 | 662,479 | +2,264 | +0.34% |
| 2023 | 9,038 | 262 | 218 | 669,407 | 670,918 | +1,511 | +0.23% |
| 2024 | 9,176 | 194 | 165 | 691,894 | 692,653 | +759 | +0.11% |
| 2025 | 9,043 | 157 | 128 | 711,271 | 711,941 | +670 | +0.09% |
| 2026 | 9,069 | 90 | 75 | 740,318 | 741,615 | +1,297 | +0.17% |

**Table A.18.** Overall performance before (clipped value) and after (observed value).

| Set | Version | n | R² | R² pers. | WAPE | WAPE pers. | Skill | RelMAE | Bias |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Retrospective OOF 2019-2026 | before (winsorized actual) | 73,462 | 0.9652 | 0.9653 | 14.13% | 14.63% | −0.47% | 0.9656 | +2.40% |
| Retrospective OOF 2019-2026 | after (observed actual) | 73,462 | 0.9617 | 0.9616 | 14.38% | 14.88% | +0.09% | 0.9662 | +2.23% |
| Holdout 2026 | before (winsorized actual) | 9,069 | 0.9733 | 0.9689 | 12.09% | 12.91% | +14.20% | 0.9363 | +0.92% |
| Holdout 2026 | after (observed actual) | 9,069 | 0.9710 | 0.9666 | 12.27% | 13.09% | +13.21% | 0.9372 | +0.74% |
| Holdout 2025, 2025 origin | before (winsorized actual) | 9,041 | 0.9794 | 0.9735 | 12.24% | 13.12% | +22.46% | 0.9327 | −0.20% |
| Holdout 2025, 2025 origin | after (observed actual) | 9,041 | 0.9782 | 0.9717 | 12.35% | 13.23% | +22.87% | 0.9333 | −0.29% |

**Table A.19.** Annual OOF performance (2026 origin) before and after.

| Year | Version | Actual | Predicted | WAPE | WAPE pers. | R² | Skill | RelMAE | Aggregate error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | before | 654,320 | 677,096 | 14.12% | 14.06% | 0.9543 | −38.58% | 1.0042 | +3.48% |
| 2019 | after | 654,495 | 677,096 | 14.36% | 14.30% | 0.9499 | −34.89% | 1.0041 | +3.45% |
| 2020 | before | 637,304 | 666,925 | 14.46% | 15.51% | 0.9428 | −13.48% | 0.9323 | +4.65% |
| 2020 | after | 637,998 | 666,925 | 14.69% | 15.74% | 0.9359 | −13.71% | 0.9333 | +4.53% |
| 2021 | before | 667,325 | 654,899 | 15.13% | 16.71% | 0.9674 | +21.59% | 0.9049 | −1.86% |
| 2021 | after | 669,403 | 654,899 | 15.50% | 17.08% | 0.9625 | +19.99% | 0.9073 | −2.17% |
| 2022 | before | 660,215 | 700,931 | 15.91% | 15.96% | 0.9578 | −5.16% | 0.9970 | +6.17% |
| 2022 | after | 662,479 | 700,931 | 16.31% | 16.35% | 0.9527 | −2.98% | 0.9971 | +5.80% |
| 2023 | before | 669,407 | 702,750 | 15.92% | 15.35% | 0.9617 | −12.08% | 1.0367 | +4.98% |
| 2023 | after | 670,918 | 702,750 | 16.20% | 15.64% | 0.9584 | −8.97% | 1.0360 | +4.74% |
| 2024 | before | 691,894 | 700,168 | 13.46% | 13.78% | 0.9740 | +3.07% | 0.9766 | +1.20% |
| 2024 | after | 692,653 | 700,168 | 13.63% | 13.96% | 0.9725 | +3.68% | 0.9768 | +1.09% |
| 2025 | before | 711,271 | 712,759 | 12.34% | 13.12% | 0.9790 | +20.53% | 0.9404 | +0.21% |
| 2025 | after | 711,941 | 712,759 | 12.45% | 13.23% | 0.9777 | +21.08% | 0.9409 | +0.11% |
| 2026 | before | 740,318 | 747,102 | 12.09% | 12.91% | 0.9733 | +14.20% | 0.9363 | +0.92% |
| 2026 | after | 741,615 | 747,102 | 12.27% | 13.09% | 0.9710 | +13.21% | 0.9372 | +0.74% |

**Table A.20.** Cascade of the 2026 holdout before and after.

| Level | Version | Groups | WAPE | WAPE pers. | R² | R² pers. | Skill | RelMAE | ± 10% | ± 10% pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N1 National | before | 1 | 0.92% | 2.60% | — | — | +87.55% | 0.3529 | 100.00% | 100.00% |
| N2 + Institution | before | 53 | 2.60% | 3.49% | 0.9976 | 0.9958 | +43.03% | 0.7460 | 90.57% | 92.45% |
| N3 + Field | before | 413 | 4.30% | 4.89% | 0.9970 | 0.9955 | +34.20% | 0.8795 | 80.87% | 77.48% |
| N4 + Region | before | 647 | 4.68% | 5.15% | 0.9957 | 0.9948 | +16.90% | 0.9090 | 76.20% | 74.34% |
| N5 + Program | before | 2,739 | 8.24% | 8.63% | 0.9827 | 0.9811 | +8.60% | 0.9545 | 57.36% | 56.33% |
| N6 + Status | before | 4,798 | 10.05% | 10.65% | 0.9794 | 0.9768 | +11.25% | 0.9436 | 49.33% | 48.06% |
| N7 + Gender | before | 8,390 | 11.53% | 12.13% | 0.9754 | 0.9741 | +5.09% | 0.9508 | 42.62% | 41.81% |
| N8 + Attendance mode | before | 9,069 | 12.09% | 12.91% | 0.9733 | 0.9689 | +14.20% | 0.9363 | 41.59% | 40.56% |
| N1 National | after | 1 | 0.74% | 2.77% | — | — | +92.85% | 0.2674 | 100.00% | 100.00% |
| N2 + Institution | after | 53 | 2.76% | 3.64% | 0.9975 | 0.9950 | +49.51% | 0.7578 | 88.68% | 92.45% |
| N3 + Field | after | 413 | 4.44% | 5.04% | 0.9968 | 0.9949 | +37.42% | 0.8799 | 80.15% | 76.76% |
| N4 + Region | after | 647 | 4.78% | 5.30% | 0.9955 | 0.9941 | +24.45% | 0.9018 | 75.58% | 73.42% |
| N5 + Program | after | 2,739 | 8.42% | 8.81% | 0.9812 | 0.9796 | +7.86% | 0.9549 | 57.21% | 56.26% |
| N6 + Status | after | 4,798 | 10.22% | 10.83% | 0.9777 | 0.9751 | +10.40% | 0.9443 | 49.33% | 48.02% |
| N7 + Gender | after | 8,390 | 11.71% | 12.31% | 0.9732 | 0.9719 | +4.47% | 0.9517 | 42.59% | 41.81% |
| N8 + Attendance mode | after | 9,069 | 12.27% | 13.09% | 0.9710 | 0.9666 | +13.21% | 0.9372 | 41.59% | 40.56% |

# A.16 Per-series benchmarks and the lags-only global model: complete tables

**Construction of the series.** At the $Y-1$ origin, the value of the series at $Y-1$ is the cell's lag at $Y$ (so persistence is exactly the published benchmark); values at $s \le Y-2$ are the cell's enrollment at $s$ or, if the cell was not in the panel at $s$, its lag at $s+1$; the series is cut at the first year without data, and the 2018 lag gives the 2017 value. With fewer than three observations, all methods fall back to persistence. Methods (`statsforecast` 2.1.1): Naive (control, identical to persistence and omitted), RWD, AutoETS without seasonality (includes damped), AutoARIMA, standard Theta and Comb (mean of ETS, ARIMA and Theta); predictions truncated at zero; levels by bottom-up summation.

**Table A.21.** Cells that fall back to persistence for having fewer than three observations.

| Year / set | Cells | Fewer than 3 obs. |
|---|---:|---:|
| 2019 | 9,424 | 9,424 |
| 2020 | 9,321 | 1,275 |
| 2021 | 9,230 | 1,224 |
| 2022 | 9,161 | 1,240 |
| 2023 | 9,038 | 1,140 |
| 2024 | 9,176 | 1,167 |
| 2025 | 9,043 | 1,141 |
| 2026 | 9,069 | 1,126 |
| 2026 validation | 8,729 | 580 |

**Table A.22.** Computation time (one fit per series and origin; 63,794 series).

| Method | Seconds |
|---|---:|
| Naive | 1.0 |
| RWD | 1.3 |
| ETS | 85.9 |
| ARIMA | 461.6 |
| Theta | 4.5 |
| Global LightGBM | 114.9 |

**Table A.23.** Benchmarks by level with observed enrollment: OOF 2019–2025 and 2026 holdout (N1, N2, N5 and N8). "Global" = Lrez.

| Set | Level | Method | WAPE | Skill | RelMAE | ± 10% |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N1 National | Persistence | 1.87% | +0.00% | 1.0000 | 100.00% |
| OOF 2019-2025 | N2 + Institution | Persistence | 4.66% | +0.00% | 1.0000 | 80.05% |
| OOF 2019-2025 | N5 + Program | Persistence | 10.57% | +0.00% | 1.0000 | 48.12% |
| OOF 2019-2025 | N8 + Attendance mode | Persistence | 15.16% | +0.00% | 1.0000 | 36.49% |
| OOF 2019-2025 | N1 National | RWD | 2.35% | −56.18% | 1.2552 | 100.00% |
| OOF 2019-2025 | N2 + Institution | RWD | 4.24% | +34.16% | 0.9092 | 80.05% |
| OOF 2019-2025 | N5 + Program | RWD | 10.30% | −4.31% | 0.9751 | 48.35% |
| OOF 2019-2025 | N8 + Attendance mode | RWD | 15.68% | −13.85% | 1.0341 | 34.61% |
| OOF 2019-2025 | N1 National | ETS | 1.71% | +10.34% | 0.9153 | 100.00% |
| OOF 2019-2025 | N2 + Institution | ETS | 4.89% | −4.89% | 1.0501 | 79.30% |
| OOF 2019-2025 | N5 + Program | ETS | 11.21% | −9.61% | 1.0605 | 46.09% |
| OOF 2019-2025 | N8 + Attendance mode | ETS | 15.76% | −7.37% | 1.0393 | 35.42% |
| OOF 2019-2025 | N1 National | ARIMA | 1.29% | +55.65% | 0.6889 | 100.00% |
| OOF 2019-2025 | N2 + Institution | ARIMA | 5.70% | −52.54% | 1.2238 | 76.56% |
| OOF 2019-2025 | N5 + Program | ARIMA | 13.75% | −72.53% | 1.3008 | 40.00% |
| OOF 2019-2025 | N8 + Attendance mode | ARIMA | 18.61% | −68.73% | 1.2275 | 31.50% |
| OOF 2019-2025 | N1 National | Theta | 1.56% | +25.76% | 0.8319 | 100.00% |
| OOF 2019-2025 | N2 + Institution | Theta | 4.54% | +14.37% | 0.9742 | 79.80% |
| OOF 2019-2025 | N5 + Program | Theta | 10.91% | −2.44% | 1.0322 | 46.39% |
| OOF 2019-2025 | N8 + Attendance mode | Theta | 15.70% | −5.39% | 1.0354 | 34.98% |
| OOF 2019-2025 | N1 National | Comb | 1.48% | +36.03% | 0.7929 | 100.00% |
| OOF 2019-2025 | N2 + Institution | Comb | 4.97% | −8.70% | 1.0657 | 79.30% |
| OOF 2019-2025 | N5 + Program | Comb | 11.56% | −13.97% | 1.0938 | 44.79% |
| OOF 2019-2025 | N8 + Attendance mode | Comb | 16.03% | −12.16% | 1.0576 | 34.64% |
| OOF 2019-2025 | N1 National | Global | 3.10% | −229.09% | 1.6572 | 100.00% |
| OOF 2019-2025 | N2 + Institution | Global | 4.92% | +15.00% | 1.0560 | 76.06% |
| OOF 2019-2025 | N5 + Program | Global | 10.03% | +1.18% | 0.9491 | 49.46% |
| OOF 2019-2025 | N8 + Attendance mode | Global | 14.27% | +5.38% | 0.9415 | 37.50% |
| OOF 2019-2025 | N1 National | CatBoost | 3.08% | −161.50% | 1.6451 | 100.00% |
| OOF 2019-2025 | N2 + Institution | CatBoost | 4.69% | +22.81% | 1.0058 | 78.55% |
| OOF 2019-2025 | N5 + Program | CatBoost | 10.14% | −1.19% | 0.9592 | 48.67% |
| OOF 2019-2025 | N8 + Attendance mode | CatBoost | 14.71% | −1.86% | 0.9702 | 36.26% |
| Holdout 2026 | N1 National | Persistence | 2.77% | +0.00% | 1.0000 | 100.00% |
| Holdout 2026 | N2 + Institution | Persistence | 3.64% | +0.00% | 1.0000 | 92.45% |
| Holdout 2026 | N5 + Program | Persistence | 8.81% | +0.00% | 1.0000 | 56.26% |
| Holdout 2026 | N8 + Attendance mode | Persistence | 13.09% | +0.00% | 1.0000 | 40.56% |
| Holdout 2026 | N1 National | RWD | 0.85% | +90.58% | 0.3070 | 100.00% |
| Holdout 2026 | N2 + Institution | RWD | 2.85% | +48.46% | 0.7829 | 88.68% |
| Holdout 2026 | N5 + Program | RWD | 8.69% | +3.04% | 0.9864 | 54.95% |
| Holdout 2026 | N8 + Attendance mode | RWD | 13.27% | +3.17% | 1.0141 | 38.80% |
| Holdout 2026 | N1 National | ETS | 2.54% | +15.86% | 0.9173 | 100.00% |
| Holdout 2026 | N2 + Institution | ETS | 3.76% | −8.90% | 1.0333 | 90.57% |
| Holdout 2026 | N5 + Program | ETS | 10.31% | −10.20% | 1.1698 | 49.65% |
| Holdout 2026 | N8 + Attendance mode | ETS | 14.46% | −9.05% | 1.1050 | 37.57% |
| Holdout 2026 | N1 National | ARIMA | 1.96% | +49.98% | 0.7073 | 100.00% |
| Holdout 2026 | N2 + Institution | ARIMA | 3.91% | +3.40% | 1.0731 | 88.68% |
| Holdout 2026 | N5 + Program | ARIMA | 11.28% | −46.61% | 1.2799 | 47.35% |
| Holdout 2026 | N8 + Attendance mode | ARIMA | 15.69% | −42.00% | 1.1988 | 35.96% |
| Holdout 2026 | N1 National | Theta | 1.46% | +72.09% | 0.5283 | 100.00% |
| Holdout 2026 | N2 + Institution | Theta | 3.39% | +25.70% | 0.9310 | 88.68% |
| Holdout 2026 | N5 + Program | Theta | 9.67% | −2.45% | 1.0968 | 50.93% |
| Holdout 2026 | N8 + Attendance mode | Theta | 13.86% | −3.18% | 1.0589 | 37.96% |
| Holdout 2026 | N1 National | Comb | 1.99% | +48.50% | 0.7176 | 100.00% |
| Holdout 2026 | N2 + Institution | Comb | 3.61% | +10.42% | 0.9924 | 88.68% |
| Holdout 2026 | N5 + Program | Comb | 10.03% | −10.73% | 1.1377 | 50.68% |
| Holdout 2026 | N8 + Attendance mode | Comb | 14.08% | −8.18% | 1.0754 | 38.46% |
| Holdout 2026 | N1 National | Global | 0.80% | +91.54% | 0.2908 | 100.00% |
| Holdout 2026 | N2 + Institution | Global | 2.65% | +43.57% | 0.7276 | 94.34% |
| Holdout 2026 | N5 + Program | Global | 7.98% | +15.87% | 0.9059 | 59.66% |
| Holdout 2026 | N8 + Attendance mode | Global | 11.60% | +23.42% | 0.8859 | 43.26% |
| Holdout 2026 | N1 National | CatBoost | 0.74% | +92.85% | 0.2674 | 100.00% |
| Holdout 2026 | N2 + Institution | CatBoost | 2.76% | +49.51% | 0.7578 | 88.68% |
| Holdout 2026 | N5 + Program | CatBoost | 8.42% | +7.86% | 0.9549 | 57.21% |
| Holdout 2026 | N8 + Attendance mode | CatBoost | 12.27% | +13.21% | 0.9372 | 41.59% |

*Note:* the complete N1–N8 tables with the observed value are in the author's results file. Levels N3, N4, N6 and N7 are in Table A.24. Sensitivity without the 113 duplicated rows (OOF 2019–2025): N2 persistence 4.65%, skill +0.00%; N8 persistence 15.15%; N2 global 4.91%, skill +15.17%; N8 global 14.26%, skill +5.52%; N2 CatBoost 4.68%, skill +22.74%; N8 CatBoost 14.70%, skill −2.06%.

**Table A.24.** Benchmarks by level with observed enrollment: OOF 2019–2025 and 2026 holdout (N3, N4, N6 and N7). "Global" = Lrez.

| Set | Level | Method | WAPE | Skill | RelMAE | ± 10% |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N3 + Field | Persistence | 6.43% | +0.00% | 1.0000 | 68.72% |
| OOF 2019-2025 | N4 + Region | Persistence | 6.99% | +0.00% | 1.0000 | 58.85% |
| OOF 2019-2025 | N6 + Status | Persistence | 12.99% | +0.00% | 1.0000 | 42.04% |
| OOF 2019-2025 | N7 + Gender | Persistence | 14.42% | +0.00% | 1.0000 | 37.78% |
| OOF 2019-2025 | N3 + Field | RWD | 6.09% | +17.22% | 0.9472 | 68.92% |
| OOF 2019-2025 | N4 + Region | RWD | 6.66% | +1.59% | 0.9521 | 59.66% |
| OOF 2019-2025 | N6 + Status | RWD | 13.21% | −9.28% | 1.0163 | 40.81% |
| OOF 2019-2025 | N7 + Gender | RWD | 14.88% | −11.37% | 1.0319 | 35.92% |
| OOF 2019-2025 | N3 + Field | ETS | 6.77% | −6.45% | 1.0537 | 67.15% |
| OOF 2019-2025 | N4 + Region | ETS | 7.36% | −7.57% | 1.0534 | 57.03% |
| OOF 2019-2025 | N6 + Status | ETS | 13.58% | −7.15% | 1.0452 | 40.58% |
| OOF 2019-2025 | N7 + Gender | ETS | 14.99% | −6.97% | 1.0396 | 36.68% |
| OOF 2019-2025 | N3 + Field | ARIMA | 8.18% | −58.14% | 1.2732 | 59.84% |
| OOF 2019-2025 | N4 + Region | ARIMA | 8.94% | −67.39% | 1.2785 | 51.05% |
| OOF 2019-2025 | N6 + Status | ARIMA | 16.07% | −63.56% | 1.2368 | 36.28% |
| OOF 2019-2025 | N7 + Gender | ARIMA | 17.70% | −67.62% | 1.2273 | 32.62% |
| OOF 2019-2025 | N3 + Field | Theta | 6.52% | +4.59% | 1.0147 | 68.29% |
| OOF 2019-2025 | N4 + Region | Theta | 7.10% | −0.78% | 1.0153 | 57.61% |
| OOF 2019-2025 | N6 + Status | Theta | 13.46% | −2.41% | 1.0362 | 40.27% |
| OOF 2019-2025 | N7 + Gender | Theta | 14.92% | −3.37% | 1.0343 | 36.22% |
| OOF 2019-2025 | N3 + Field | Comb | 6.96% | −12.40% | 1.0820 | 65.54% |
| OOF 2019-2025 | N4 + Region | Comb | 7.57% | −14.26% | 1.0832 | 55.85% |
| OOF 2019-2025 | N6 + Status | Comb | 13.86% | −10.31% | 1.0667 | 40.05% |
| OOF 2019-2025 | N7 + Gender | Comb | 15.25% | −10.81% | 1.0570 | 35.90% |
| OOF 2019-2025 | N3 + Field | Global | 6.40% | +8.80% | 0.9963 | 68.92% |
| OOF 2019-2025 | N4 + Region | Global | 6.89% | −6.26% | 0.9860 | 60.16% |
| OOF 2019-2025 | N6 + Status | Global | 12.27% | +3.91% | 0.9440 | 43.12% |
| OOF 2019-2025 | N7 + Gender | Global | 13.61% | +4.92% | 0.9438 | 38.80% |
| OOF 2019-2025 | N3 + Field | CatBoost | 6.23% | +13.13% | 0.9692 | 68.69% |
| OOF 2019-2025 | N4 + Region | CatBoost | 6.81% | −9.52% | 0.9737 | 60.31% |
| OOF 2019-2025 | N6 + Status | CatBoost | 12.65% | −2.43% | 0.9733 | 41.88% |
| OOF 2019-2025 | N7 + Gender | CatBoost | 14.03% | −1.90% | 0.9729 | 37.49% |
| Holdout 2026 | N3 + Field | Persistence | 5.04% | +0.00% | 1.0000 | 76.76% |
| Holdout 2026 | N4 + Region | Persistence | 5.30% | +0.00% | 1.0000 | 73.42% |
| Holdout 2026 | N6 + Status | Persistence | 10.83% | +0.00% | 1.0000 | 48.02% |
| Holdout 2026 | N7 + Gender | Persistence | 12.31% | +0.00% | 1.0000 | 41.81% |
| Holdout 2026 | N3 + Field | RWD | 4.47% | +36.65% | 0.8874 | 77.24% |
| Holdout 2026 | N4 + Region | RWD | 4.88% | +33.20% | 0.9211 | 73.11% |
| Holdout 2026 | N6 + Status | RWD | 10.89% | +1.11% | 1.0057 | 47.96% |
| Holdout 2026 | N7 + Gender | RWD | 12.58% | −1.20% | 1.0220 | 39.93% |
| Holdout 2026 | N3 + Field | ETS | 5.65% | −19.22% | 1.1212 | 73.61% |
| Holdout 2026 | N4 + Region | ETS | 6.02% | −18.31% | 1.1370 | 67.70% |
| Holdout 2026 | N6 + Status | ETS | 12.15% | −5.70% | 1.1227 | 43.39% |
| Holdout 2026 | N7 + Gender | ETS | 13.57% | −7.11% | 1.1024 | 38.70% |
| Holdout 2026 | N3 + Field | ARIMA | 6.17% | −39.50% | 1.2229 | 68.77% |
| Holdout 2026 | N4 + Region | ARIMA | 6.61% | −47.46% | 1.2469 | 62.60% |
| Holdout 2026 | N6 + Status | ARIMA | 13.16% | −38.23% | 1.2157 | 41.58% |
| Holdout 2026 | N7 + Gender | ARIMA | 14.85% | −46.15% | 1.2065 | 36.84% |
| Holdout 2026 | N3 + Field | Theta | 5.26% | +1.57% | 1.0437 | 73.61% |
| Holdout 2026 | N4 + Region | Theta | 5.67% | +3.34% | 1.0709 | 68.16% |
| Holdout 2026 | N6 + Status | Theta | 11.63% | −1.76% | 1.0739 | 44.21% |
| Holdout 2026 | N7 + Gender | Theta | 13.08% | −4.07% | 1.0630 | 39.21% |
| Holdout 2026 | N3 + Field | Comb | 5.49% | −11.92% | 1.0890 | 72.15% |
| Holdout 2026 | N4 + Region | Comb | 5.90% | −11.97% | 1.1131 | 66.77% |
| Holdout 2026 | N6 + Status | Comb | 11.79% | −6.24% | 1.0888 | 44.96% |
| Holdout 2026 | N7 + Gender | Comb | 13.22% | −8.66% | 1.0742 | 39.63% |
| Holdout 2026 | N3 + Field | Global | 4.21% | +36.67% | 0.8343 | 81.36% |
| Holdout 2026 | N4 + Region | Global | 4.60% | +31.14% | 0.8691 | 76.35% |
| Holdout 2026 | N6 + Status | Global | 9.63% | +20.48% | 0.8896 | 50.94% |
| Holdout 2026 | N7 + Gender | Global | 11.04% | +19.86% | 0.8970 | 44.61% |
| Holdout 2026 | N3 + Field | CatBoost | 4.44% | +37.42% | 0.8799 | 80.15% |
| Holdout 2026 | N4 + Region | CatBoost | 4.78% | +24.45% | 0.9018 | 75.58% |
| Holdout 2026 | N6 + Status | CatBoost | 10.22% | +10.40% | 0.9443 | 49.33% |
| Holdout 2026 | N7 + Gender | CatBoost | 11.71% | +4.47% | 0.9517 | 42.59% |

**Table A.25.** Benchmarks by level in the validation against the 2026 official data (8,729 cells; C49 = 2025-origin model). This validation uses the official data.

| Level | Method | Groups | WAPE | Skill | RelMAE | ± 10% | Aggregate error |
|---|---:|---:|---:|---:|---:|---:|---:|
| N1 National | Persistence | 1 | 2.32% | +0.00% | 1.0000 | 100.00% | −2.32% |
| N1 National | RWD | 1 | 1.25% | +71.08% | 0.5378 | 100.00% | +1.25% |
| N1 National | ETS | 1 | 2.00% | +25.69% | 0.8621 | 100.00% | −2.00% |
| N1 National | ARIMA | 1 | 1.25% | +70.97% | 0.5388 | 100.00% | −1.25% |
| N1 National | Theta | 1 | 0.92% | +84.28% | 0.3964 | 100.00% | −0.92% |
| N1 National | Comb | 1 | 1.39% | +64.11% | 0.5991 | 100.00% | −1.39% |
| N1 National | Global | 1 | 0.79% | +88.52% | 0.3389 | 100.00% | +0.79% |
| N1 National | CatBoost | 1 | 0.01% | +100.00% | 0.0059 | 100.00% | −0.01% |
| N2 + Institution | Persistence | 53 | 3.26% | +0.00% | 1.0000 | 92.45% | −2.32% |
| N2 + Institution | RWD | 53 | 2.78% | +21.81% | 0.8532 | 86.79% | +1.25% |
| N2 + Institution | ETS | 53 | 3.47% | −10.65% | 1.0649 | 92.45% | −2.00% |
| N2 + Institution | ARIMA | 53 | 3.57% | −4.45% | 1.0952 | 88.68% | −1.25% |
| N2 + Institution | Theta | 53 | 3.11% | +17.90% | 0.9531 | 88.68% | −0.92% |
| N2 + Institution | Comb | 53 | 3.29% | +6.46% | 1.0088 | 90.57% | −1.39% |
| N2 + Institution | Global | 53 | 2.36% | +25.29% | 0.7224 | 94.34% | +0.79% |
| N2 + Institution | CatBoost | 53 | 2.31% | +48.46% | 0.7083 | 92.45% | −0.01% |
| N3 + Field | Persistence | 408 | 4.76% | +0.00% | 1.0000 | 77.94% | −2.32% |
| N3 + Field | RWD | 408 | 4.42% | +24.11% | 0.9290 | 76.72% | +1.25% |
| N3 + Field | ETS | 408 | 5.42% | −25.19% | 1.1388 | 72.30% | −2.00% |
| N3 + Field | ARIMA | 408 | 6.03% | −53.77% | 1.2672 | 69.12% | −1.25% |
| N3 + Field | Theta | 408 | 5.13% | −8.45% | 1.0784 | 72.79% | −0.92% |
| N3 + Field | Comb | 408 | 5.33% | −20.65% | 1.1184 | 72.06% | −1.39% |
| N3 + Field | Global | 408 | 4.02% | +36.14% | 0.8436 | 81.37% | +0.79% |
| N3 + Field | CatBoost | 408 | 3.74% | +48.93% | 0.7855 | 82.35% | −0.01% |
| N4 + Region | Persistence | 649 | 5.02% | +0.00% | 1.0000 | 73.19% | −2.32% |
| N4 + Region | RWD | 649 | 4.85% | +16.84% | 0.9664 | 72.27% | +1.25% |
| N4 + Region | ETS | 649 | 5.82% | −25.51% | 1.1596 | 66.41% | −2.00% |
| N4 + Region | ARIMA | 649 | 6.49% | −67.89% | 1.2919 | 62.10% | −1.25% |
| N4 + Region | Theta | 649 | 5.59% | −9.81% | 1.1143 | 67.18% | −0.92% |
| N4 + Region | Comb | 649 | 5.73% | −23.56% | 1.1405 | 66.56% | −1.39% |
| N4 + Region | Global | 649 | 4.38% | +32.81% | 0.8721 | 75.65% | +0.79% |
| N4 + Region | CatBoost | 649 | 4.16% | +37.52% | 0.8293 | 76.43% | −0.01% |
| N5 + Program | Persistence | 2,668 | 8.48% | +0.00% | 1.0000 | 56.97% | −2.32% |
| N5 + Program | RWD | 2,668 | 8.38% | +2.78% | 0.9877 | 55.17% | +1.25% |
| N5 + Program | ETS | 2,668 | 10.06% | −11.05% | 1.1869 | 50.07% | −2.00% |
| N5 + Program | ARIMA | 2,668 | 11.08% | −46.74% | 1.3062 | 47.04% | −1.25% |
| N5 + Program | Theta | 2,668 | 9.41% | −3.98% | 1.1095 | 50.97% | −0.92% |
| N5 + Program | Comb | 2,668 | 9.77% | −11.43% | 1.1527 | 51.12% | −1.39% |
| N5 + Program | Global | 2,668 | 7.64% | +18.92% | 0.9005 | 59.97% | +0.79% |
| N5 + Program | CatBoost | 2,668 | 7.59% | +24.54% | 0.8948 | 58.36% | −0.01% |
| N6 + Student status | Persistence | 4,633 | 10.47% | +0.00% | 1.0000 | 49.13% | −2.32% |
| N6 + Student status | RWD | 4,633 | 10.59% | +0.25% | 1.0110 | 48.72% | +1.25% |
| N6 + Student status | ETS | 4,633 | 11.89% | −6.40% | 1.1355 | 44.36% | −2.00% |
| N6 + Student status | ARIMA | 4,633 | 12.95% | −38.57% | 1.2369 | 42.28% | −1.25% |
| N6 + Student status | Theta | 4,633 | 11.33% | −3.41% | 1.0819 | 45.00% | −0.92% |
| N6 + Student status | Comb | 4,633 | 11.50% | −7.06% | 1.0980 | 45.93% | −1.39% |
| N6 + Student status | Global | 4,633 | 9.23% | +24.21% | 0.8818 | 51.65% | +0.79% |
| N6 + Student status | CatBoost | 4,633 | 9.42% | +25.59% | 0.8999 | 50.94% | −0.01% |
| N7 + Gender | Persistence | 8,094 | 11.97% | +0.00% | 1.0000 | 42.33% | −2.32% |
| N7 + Gender | RWD | 8,094 | 12.30% | −1.59% | 1.0277 | 40.25% | +1.25% |
| N7 + Gender | ETS | 8,094 | 13.30% | −7.72% | 1.1108 | 39.18% | −2.00% |
| N7 + Gender | ARIMA | 8,094 | 14.64% | −45.86% | 1.2234 | 37.29% | −1.25% |
| N7 + Gender | Theta | 8,094 | 12.79% | −5.80% | 1.0684 | 39.56% | −0.92% |
| N7 + Gender | Comb | 8,094 | 12.93% | −9.40% | 1.0805 | 40.10% | −1.39% |
| N7 + Gender | Global | 8,094 | 10.65% | +24.05% | 0.8895 | 45.16% | +0.79% |
| N7 + Gender | CatBoost | 8,094 | 10.93% | +22.82% | 0.9135 | 44.58% | −0.01% |
| N8 + Attendance mode | Persistence | 8,729 | 12.69% | +0.00% | 1.0000 | 40.89% | −2.32% |
| N8 + Attendance mode | RWD | 8,729 | 12.89% | +4.76% | 1.0160 | 39.07% | +1.25% |
| N8 + Attendance mode | ETS | 8,729 | 14.13% | −9.42% | 1.1131 | 37.92% | −2.00% |
| N8 + Attendance mode | ARIMA | 8,729 | 15.43% | −40.70% | 1.2161 | 36.27% | −1.25% |
| N8 + Attendance mode | Theta | 8,729 | 13.49% | −3.37% | 1.0632 | 38.24% | −0.92% |
| N8 + Attendance mode | Comb | 8,729 | 13.73% | −8.15% | 1.0817 | 38.84% | −1.39% |
| N8 + Attendance mode | Global | 8,729 | 11.16% | +26.57% | 0.8793 | 43.87% | +0.79% |
| N8 + Attendance mode | CatBoost | 8,729 | 11.49% | +26.71% | 0.9055 | 43.27% | −0.01% |

# A.17 Significance of the error differences

Diebold–Mariano-type test between groups: $d_g = L(\text{method}_g) - L(\text{benchmark}_g)$ on the aggregate group error, squared and absolute loss, CR1 standard error clustered by institution (53), $t$ with $G-1$ degrees of freedom. A negative statistic favors the method over the benchmark.

**Table A.26.** CatBoost (C49) versus persistence and versus the global model (Lrez), 2026 holdout, observed enrollment. A positive DM in the CatBoost − Global columns favors the global model.

| Level | Skill CatBoost | p sq. vs pers. | p abs. vs pers. | DM sq. CatBoost − Global | p | DM abs. CatBoost − Global | p  |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institution | +49.51% | 0.3414 | 0.2605 | −0.42 | 0.6771 | +0.37 | 0.7115 |
| N3 + Field | +37.42% | 0.2311 | 0.2219 | −0.07 | 0.9450 | +0.90 | 0.3716 |
| N4 + Region | +24.45% | 0.3947 | 0.2307 | +0.56 | 0.5753 | +0.73 | 0.4680 |
| N5 + Program | +7.86% | 0.3866 | 0.1944 | +1.10 | 0.2760 | +2.46 | 0.0171 |
| N6 + Status | +10.40% | 0.2506 | 0.0329 | +1.40 | 0.1685 | +3.45 | 0.0011 |
| N7 + Gender | +4.47% | 0.6259 | 0.0206 | +1.73 | 0.0900 | +4.17 | 0.0001 |
| N8 + Attendance mode | +13.21% | 0.1006 | 0.0049 | +1.97 | 0.0539 | +4.77 | < 0.0001 |

*Note:* N1 national, DM with HLN correction (n = 8, OOF 2019–2026, squared loss, observed enrollment): RWD DM* +0.4693, *p* 0.6531; ETS −1.8220, *p* 0.1112; ARIMA −2.5632, *p* 0.0374; Theta −1.8872, *p* 0.1011; Comb −3.2443, *p* 0.0142; Global +1.3203, *p* 0.2283; CatBoost +1.1610, *p* 0.2837.

**Table A.27.** CatBoost (C49) versus persistence in the OOF 2019–2026 (2026 origin) and in the 2025 holdout (2025 origin), observed enrollment. Negative DM favors CatBoost.

| Set | Level | Groups | Skill | RelMAE | DM quadr. | p | DM abs. | p  | Clusters |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF 2019-2026 (2026 origin) | N2 + Institution | 454 | +25.41% | 0.9786 | −0.83 | 0.4092 | −0.24 | 0.8110 | 60 |
| OOF 2019-2026 (2026 origin) | N3 + Field | 3,396 | +15.12% | 0.9594 | −0.65 | 0.5197 | −0.68 | 0.4994 | 60 |
| OOF 2019-2026 (2026 origin) | N4 + Region | 5,920 | −6.14% | 0.9660 | +0.52 | 0.6083 | −0.70 | 0.4894 | 60 |
| OOF 2019-2026 (2026 origin) | N5 + Program | 23,277 | +0.10% | 0.9587 | −0.01 | 0.9908 | −1.34 | 0.1859 | 60 |
| OOF 2019-2026 (2026 origin) | N6 + Student status | 39,327 | −0.64% | 0.9700 | +0.08 | 0.9328 | −1.22 | 0.2255 | 60 |
| OOF 2019-2026 (2026 origin) | N7 + Gender | 67,413 | −1.04% | 0.9704 | +0.15 | 0.8827 | −1.41 | 0.1649 | 60 |
| OOF 2019-2026 (2026 origin) | N8 + Attendance mode | 73,349 | +0.20% | 0.9662 | −0.03 | 0.9758 | −1.68 | 0.0992 | 60 |
| Holdout 2025 (2025 origin) | N2 + Institution | 55 | +61.79% | 0.6904 | −1.69 | 0.0973 | −1.74 | 0.0874 | 55 |
| Holdout 2025 (2025 origin) | N3 + Field | 418 | +43.34% | 0.8811 | −1.83 | 0.0730 | −1.30 | 0.1993 | 55 |
| Holdout 2025 (2025 origin) | N4 + Region | 688 | +29.33% | 0.9058 | −1.33 | 0.1887 | −1.18 | 0.2437 | 55 |
| Holdout 2025 (2025 origin) | N5 + Program | 2,792 | +21.80% | 0.9216 | −1.55 | 0.1269 | −2.22 | 0.0309 | 55 |
| Holdout 2025 (2025 origin) | N6 + Student status | 4,826 | +20.64% | 0.9350 | −1.67 | 0.1000 | −2.28 | 0.0268 | 55 |
| Holdout 2025 (2025 origin) | N7 + Gender | 8,361 | +21.42% | 0.9389 | −1.87 | 0.0664 | −2.69 | 0.0095 | 55 |
| Holdout 2025 (2025 origin) | N8 + Attendance mode | 9,041 | +22.87% | 0.9333 | −1.95 | 0.0569 | −2.91 | 0.0052 | 55 |

*Note:* in the OOF the year enters the key of each group and the clusters are the 60 institutions of the period; in N8 the 113 repeated rows are summed into their cell (73,349 groups), so the skill of N8 (+0.20%) differs from the one computed per row (+0.09%). In the OOF no difference is significant with either loss (lowest p = 0.0992, absolute, N8); in the 2025 holdout, it is significant with absolute loss in N5–N8 (p ≤ 0.031) and not with quadratic loss (p between 0.057 and 0.189).

**Table A.28.** CatBoost versus persistence, validation against the official 2026 data (2025 origin).

| Level | Groups | Skill | DM (squared) | p | DM (absolute) | p  | Clusters |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institution | 53 | +48.46% | −1.01 | 0.3151 | −1.39 | 0.1697 | 53 |
| N3 + Field | 408 | +48.93% | −1.98 | 0.0530 | −2.55 | 0.0137 | 53 |
| N4 + Region | 649 | +37.52% | −2.01 | 0.0496 | −2.55 | 0.0137 | 53 |
| N5 + Program | 2,668 | +24.54% | −2.13 | 0.0378 | −2.66 | 0.0103 | 53 |
| N6 + Status | 4,633 | +25.59% | −2.39 | 0.0205 | −3.76 | 0.0004 | 53 |
| N7 + Gender | 8,094 | +22.82% | −2.03 | 0.0470 | −3.98 | 0.0002 | 53 |
| N8 + Attendance mode | 8,729 | +26.71% | −2.15 | 0.0363 | −4.33 | < 0.0001 | 53 |

**Table A.29.** CatBoost versus the global model, validation against the official 2026 data. A positive DM favors the global model.

| Level | DM (squared) | p | DM (absolute) | p  |
|---|---:|---:|---:|---:|
| N2 + Institution | −1.05 | 0.2995 | −0.17 | 0.8672 |
| N3 + Field | −1.21 | 0.2314 | −1.15 | 0.2534 |
| N4 + Region | −0.55 | 0.5832 | −1.05 | 0.2985 |
| N5 + Program | −0.61 | 0.5417 | −0.32 | 0.7517 |
| N6 + Status | −0.17 | 0.8641 | +1.21 | 0.2316 |
| N7 + Gender | +0.19 | 0.8476 | +1.94 | 0.0577 |
| N8 + Attendance mode | −0.02 | 0.9832 | +2.30 | 0.0255 |

**Table A.30.** Multiple comparison with the best (MCB/Nemenyi) by level, 2026 holdout, observed enrollment: mean rank of the absolute error among eight methods (1 = best); "*" = different from the best (difference greater than the critical difference, CD).

| Level | CD | Persistence | RWD | ETS | ARIMA | Theta | Comb | Global | CatBoost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institution | 1.4422 | 4.755 | 4.179 | 5.226* | 5.538* | 4.434 | 4.717 | 3.566 | 3.585 |
| N3 + Field | 0.5166 | 4.051 | 4.264 | 4.908* | 5.397* | 4.754* | 4.788* | 3.782 | 4.056 |
| N4 + Region | 0.4128 | 4.086 | 4.199 | 4.940* | 5.352* | 4.751* | 4.776* | 3.841 | 4.054 |
| N5 + Program | 0.2006 | 4.122* | 4.323* | 5.007* | 5.250* | 4.671* | 4.745* | 3.827 | 4.054* |
| N6 + Status | 0.1516 | 4.237* | 4.547* | 4.829* | 4.957* | 4.668* | 4.592* | 4.016 | 4.154 |
| N7 + Gender | 0.1146 | 4.311* | 4.680* | 4.729* | 4.881* | 4.650* | 4.537* | 3.995 | 4.218* |
| N8 + Attendance mode | 0.1103 | 4.332* | 4.679* | 4.742* | 4.892* | 4.655* | 4.545* | 3.973 | 4.182* |

*Note:* the test assumes independent groups, which does not hold within an institution; with thousands of groups the critical difference is very narrow and the test is liberal.

**Table A.31.** MCB/Nemenyi by level, validation against the official 2026 data.

| Level | CD | Persistence | RWD | ETS | ARIMA | Theta | Comb | Global | CatBoost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institution | 1.4422 | 4.792 | 4.396 | 5.019* | 5.377* | 4.604 | 4.585 | 3.509 | 3.717 |
| N3 + Field | 0.5198 | 4.034 | 4.304* | 4.968* | 5.402* | 4.869* | 4.859* | 3.836 | 3.728 |
| N4 + Region | 0.4121 | 4.049 | 4.274* | 5.020* | 5.396* | 4.857* | 4.833* | 3.877 | 3.693 |
| N5 + Program | 0.2033 | 4.089 | 4.268* | 5.038* | 5.314* | 4.680* | 4.771* | 3.895 | 3.944 |
| N6 + Status | 0.1543 | 4.196* | 4.558* | 4.836* | 5.019* | 4.671* | 4.586* | 4.041 | 4.093 |
| N7 + Gender | 0.1167 | 4.299* | 4.701* | 4.738* | 4.925* | 4.654* | 4.539* | 4.012 | 4.132* |
| N8 + Attendance mode | 0.1124 | 4.325* | 4.687* | 4.759* | 4.938* | 4.658* | 4.552* | 3.982 | 4.100* |

# A.18 Ablation of the variables with contemporaneous enrollment

CatBoost with the hyperparameters of the main model (2,000 iterations, learning rate 0.0376, depth 7, L2 regularization 1.7464, bagging temperature 0.5465, 183 border counts), seed 42, with no further optimization, the same target encoding within the fold and the same origins. (i) without student density per m², faculty-to-student ratio or enrollment over GDP (46 variables); (ii) with the 49 variables and the 24 exogenous variables taken at $t-1$ (the value of the same cell at $t-1$ or, if unavailable, the $t-1$ mean of institution × program × region, then institution × region, institution and region). Cross-validation RMSE on the arcsinh scale: (i) 0.2964; (ii) 0.2963; published (recalculated) 0.2949.

**Table A.32.** Ablation with observed enrollment (N2 and N8).

| Set | Level | Variant | WAPE | Skill | RelMAE |
|---|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N2 + Institution | Persistence | 4.66% | +0.00% | 1.0000 |
| OOF 2019-2025 | N8 + Attendance mode | Persistence | 15.16% | +0.00% | 1.0000 |
| OOF 2019-2025 | N2 + Institution | Published | 4.69% | +22.81% | 1.0058 |
| OOF 2019-2025 | N8 + Attendance mode | Published | 14.71% | −1.86% | 0.9702 |
| OOF 2019-2025 | N2 + Institution | (i) | 4.78% | +19.83% | 1.0247 |
| OOF 2019-2025 | N8 + Attendance mode | (i) | 14.80% | −4.13% | 0.9760 |
| OOF 2019-2025 | N2 + Institution | (ii) | 4.36% | +32.67% | 0.9351 |
| OOF 2019-2025 | N8 + Attendance mode | (ii) | 14.61% | −6.18% | 0.9639 |
| Holdout 2026 | N2 + Institution | Persistence | 3.64% | +0.00% | 1.0000 |
| Holdout 2026 | N8 + Attendance mode | Persistence | 13.09% | +0.00% | 1.0000 |
| Holdout 2026 | N2 + Institution | Published | 2.76% | +49.51% | 0.7578 |
| Holdout 2026 | N8 + Attendance mode | Published | 12.27% | +13.21% | 0.9372 |
| Holdout 2026 | N2 + Institution | (i) | 2.66% | +52.53% | 0.7305 |
| Holdout 2026 | N8 + Attendance mode | (i) | 12.27% | +14.68% | 0.9374 |
| Holdout 2026 | N2 + Institution | (ii) | 2.85% | +55.14% | 0.7824 |
| Holdout 2026 | N8 + Attendance mode | (ii) | 12.33% | +17.71% | 0.9422 |

**Informative (non-frozen) 2027 forecast of the variants.** Refit with 2018–2026: published (recalculated) 761,053; (i) 760,880; (ii) 755,071. The replication of the published figure differs from the frozen one (761,058) because of lag rounding; these figures are not part of the freeze.

# A.19 Interval score of the 90% bands

$\text{IS}_\alpha$ with $\alpha = 0.10$ and MSIS = mean IS / MAE of persistence on the same groups. Bands: size-stratified conformal (those of the main model), unstratified conformal (a single pair of quantiles per level) and AutoETS at 90% (at N2–N7, one AutoETS per node on its aggregated history). Only groups with all three bands are compared.

**Table A.33.** Coverage, median width, mean IS and MSIS by level, 2026 holdout, enrollment observed at calibration and at evaluation, over the groups with all three bands.

| Level | Band | Common groups | Coverage | Median width | Mean IS | MSIS |
|---|---:|---:|---:|---:|---:|---:|
| N2 + Institution | Published (stratified conformal) | 53 | 94.34% | 2,282.9 | 3,178.1 | 6.2410 |
| N2 + Institution | r1 · unstratified conformal | 53 | 96.23% | 4,095.7 | 5,567.6 | 10.9335 |
| N2 + Institution | r2 · AutoETS 90% | 53 | 94.34% | 2,244.1 | 3,592.3 | 7.0544 |
| N3 + Field | Published (stratified conformal) | 404 | 94.31% | 305.2 | 538.1 | 5.8765 |
| N3 + Field | r1 · unstratified conformal | 404 | 95.79% | 478.1 | 833.4 | 9.1020 |
| N3 + Field | r2 · AutoETS 90% | 404 | 91.09% | 320.7 | 706.7 | 7.7180 |
| N4 + Region | Published (stratified conformal) | 630 | 93.49% | 205.9 | 383.8 | 6.2356 |
| N4 + Region | r1 · unstratified conformal | 630 | 95.71% | 409.3 | 752.1 | 12.2206 |
| N4 + Region | r2 · AutoETS 90% | 630 | 89.84% | 230.9 | 506.9 | 8.2369 |
| N5 + Program | Published (stratified conformal) | 2,388 | 93.72% | 102.9 | 166.7 | 7.1447 |
| N5 + Program | r1 · unstratified conformal | 2,388 | 95.27% | 169.0 | 266.5 | 11.4252 |
| N5 + Program | r2 · AutoETS 90% | 2,388 | 89.45% | 92.4 | 179.3 | 7.6881 |
| N6 + Student status | Published (stratified conformal) | 4,036 | 94.82% | 79.1 | 123.9 | 7.4753 |
| N6 + Student status | r1 · unstratified conformal | 4,036 | 95.94% | 94.1 | 183.5 | 11.0731 |
| N6 + Student status | r2 · AutoETS 90% | 4,036 | 88.75% | 58.9 | 126.0 | 7.6041 |
| N7 + Gender | Published (stratified conformal) | 6,839 | 94.87% | 53.6 | 79.8 | 7.2482 |
| N7 + Gender | r1 · unstratified conformal | 6,839 | 95.45% | 53.7 | 108.0 | 9.8169 |
| N7 + Gender | r2 · AutoETS 90% | 6,839 | 86.83% | 36.2 | 79.7 | 7.2427 |
| N8 + Attendance mode | Published (stratified conformal) | 7,943 | 93.86% | 37.8 | 65.3 | 6.1554 |
| N8 + Attendance mode | r1 · unstratified conformal | 7,943 | 95.10% | 48.4 | 96.0 | 9.0523 |
| N8 + Attendance mode | r2 · AutoETS 90% | 7,943 | 86.99% | 34.4 | 71.5 | 6.7455 |

*Note:* at N7, AutoETS obtains a mean IS (79.7) and an MSIS (7.2427) marginally lower than the stratified bands (79.8 and 7.2482); at the other levels, the stratified bands have the lowest IS.

# A.20 Target encoding experiment and provenance of the precomputed columns

Four arms with the same CatBoost and the same seven folds: $m$-estimator ($\text{enc} = (n\,\bar{z}_c + m\,\bar{z})/(n+m)$, $m = 30$) or sigmoid weighting (`category_encoders` 2.8.1, `TargetEncoder(smoothing = 30, min_samples_leaf = 20)`, the one used in the main model), fitted on the entire 2018–2026 panel (with leakage) or only on the training rows of each fold. 2026 origin only. The RMSE by fold is in the author's files.

**Provenance of the precomputed columns.** The consolidation computes the four precomputed target-encoding columns ($m$-estimator, $m = 30$) before removing exact duplicates: according to the recorded output of the 2025-origin run, there were 87,131 rows after the minimum-lag filter and 13,235 exact duplicates were removed, down to 73,896. The means and counts by category weight the repeated rows twice; recomputed on the final rows, they differ from the saved values by up to 0.083 (program), 0.037 (institution), 0.016 (region) and 0.011 (field). No published figure changes, because the model does not use these columns and the experiment recomputes them.

# A.21 Hierarchical reconciliation

Hierarchy truncated at N5 (3,853 nodes, 2,739 lower-level): with approximately 25,000 series from N1–N8, MinT's dense covariance matrix does not fit in memory. Base forecasts: N5 = main model aggregated; N1–N4 = one AutoETS per node on the aggregated history (last value = sum of the 2026 lags). MinT covariance with shrinkage: one-step residuals from the 2019–2025 OOF years. `hierarchicalforecast` 1.5.3.

**Table A.34.** Reconciliation on the 2026 holdout (N1–N5), observed enrollment.

| Method | Level | WAPE | Skill | RelMAE | ±10% |
|---|---:|---:|---:|---:|---:|
| Base (ETS at N1-N4, CatBoost at N5) | N1 National | 2.86% | −7.07% | 1.0348 | 100.00% |
| Base (ETS at N1-N4, CatBoost at N5) | N2 + Institution | 4.18% | −15.43% | 1.1494 | 86.79% |
| Base (ETS at N1-N4, CatBoost at N5) | N3 + Field | 5.92% | −20.41% | 1.1747 | 71.19% |
| Base (ETS at N1-N4, CatBoost at N5) | N4 + Region | 6.55% | −46.44% | 1.2357 | 65.38% |
| Base (ETS at N1-N4, CatBoost at N5) | N5 + Program | 8.42% | +7.86% | 0.9549 | 57.21% |
| BottomUp (published) | N1 National | 0.74% | +92.85% | 0.2674 | 100.00% |
| BottomUp (published) | N2 + Institution | 2.76% | +49.51% | 0.7578 | 88.68% |
| BottomUp (published) | N3 + Field | 4.44% | +37.42% | 0.8799 | 80.15% |
| BottomUp (published) | N4 + Region | 4.78% | +24.45% | 0.9018 | 75.58% |
| BottomUp (published) | N5 + Program | 8.42% | +7.86% | 0.9549 | 57.21% |
| OLS | N1 National | 2.86% | −7.14% | 1.0351 | 100.00% |
| OLS | N2 + Institution | 4.06% | −10.10% | 1.1149 | 88.68% |
| OLS | N3 + Field | 5.81% | −19.13% | 1.1529 | 69.25% |
| OLS | N4 + Region | 6.21% | −26.40% | 1.1724 | 64.61% |
| OLS | N5 + Program | 9.92% | +0.35% | 1.1253 | 49.87% |
| Structural WLS | N1 National | 2.17% | +38.29% | 0.7856 | 100.00% |
| Structural WLS | N2 + Institution | 3.37% | +24.99% | 0.9267 | 94.34% |
| Structural WLS | N3 + Field | 4.97% | +13.69% | 0.9850 | 73.85% |
| Structural WLS | N4 + Region | 5.30% | +14.50% | 1.0011 | 70.94% |
| Structural WLS | N5 + Program | 9.17% | +7.81% | 1.0409 | 52.32% |
| MinT-shrink | N1 National | 3.03% | −19.77% | 1.0944 | 100.00% |
| MinT-shrink | N2 + Institution | 3.75% | +22.27% | 1.0305 | 92.45% |
| MinT-shrink | N3 + Field | 5.52% | +1.96% | 1.0952 | 72.40% |
| MinT-shrink | N4 + Region | 6.14% | −5.76% | 1.1591 | 68.47% |
| MinT-shrink | N5 + Program | 12.32% | −88.48% | 1.3981 | 47.65% |

*Note:* the published bottom-up sum is the best at N1–N5, and MinT with shrinkage worsens N4 and N5. The ETS base forecasts for N1–N4 are worse than persistence, because the composition of each node changes between years, and the reconciliation carries over that weakness.

# A.22 Factorial algorithm × feature design: complete results

Fixed hyperparameters, no new optimization, same origins and observed enrollment. C49 = published model; Crez = C49 hyperparameters on the lags-only global model's features, with sigmoid target encoding within the fold on the seven identifiers; L49 = LightGBM with sigmoid target encoding within the fold on the four categorical variables and the grid of 12 (chosen: 63 leaves, 100 minimum observations per leaf, 800 trees); Lrez = lags-only global model. In the 2026 validation, the 8,329 cells of that validation present in the 2026 holdout; the four models apply their 2026-origin rate to the 2025 lag and are compared with the official figure (the 2025-origin model is not included because it was trained with a different panel). Cross-validation RMSE (arcsinh, seven folds): C49 0.2949; Crez 0.2948; L49 0.2952; Lrez 0.2869.

**Table A.35.** WAPE, skill, RelMAE and percentage within ±10% of the factorial design (N2, N5 and N8).

| Set | Level | Model | WAPE | Skill | RelMAE | ± 10% |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019–2025 | N2 + Institution | CatBoost · 49 variables | 4.69% | +22.81% | 1.0058 | 78.55% |
| OOF 2019–2025 | N2 + Institution | CatBoost · lags only | 5.28% | +1.52% | 1.1335 | 74.31% |
| OOF 2019–2025 | N2 + Institution | LightGBM · 49 variables | 4.55% | +28.98% | 0.9767 | 80.55% |
| OOF 2019–2025 | N2 + Institution | LightGBM · lags only | 4.92% | +15.00% | 1.0560 | 76.06% |
| OOF 2019–2025 | N5 + Program | CatBoost · 49 variables | 10.14% | −1.19% | 0.9592 | 48.67% |
| OOF 2019–2025 | N5 + Program | CatBoost · lags only | 10.58% | −16.50% | 1.0014 | 48.00% |
| OOF 2019–2025 | N5 + Program | LightGBM · 49 variables | 10.04% | +4.29% | 0.9499 | 48.98% |
| OOF 2019–2025 | N5 + Program | LightGBM · lags only | 10.03% | +1.18% | 0.9491 | 49.46% |
| OOF 2019–2025 | N8 + Attendance mode | CatBoost · 49 variables | 14.71% | −1.86% | 0.9702 | 36.26% |
| OOF 2019–2025 | N8 + Attendance mode | CatBoost · lags only | 14.78% | −11.05% | 0.9752 | 36.72% |
| OOF 2019–2025 | N8 + Attendance mode | LightGBM · 49 variables | 14.62% | +3.17% | 0.9644 | 36.27% |
| OOF 2019–2025 | N8 + Attendance mode | LightGBM · lags only | 14.27% | +5.38% | 0.9415 | 37.50% |
| Holdout 2026 | N2 + Institution | CatBoost · 49 variables | 2.76% | +49.51% | 0.7578 | 88.68% |
| Holdout 2026 | N2 + Institution | CatBoost · lags only | 2.67% | +47.38% | 0.7331 | 90.57% |
| Holdout 2026 | N2 + Institution | LightGBM · 49 variables | 2.46% | +64.94% | 0.6755 | 90.57% |
| Holdout 2026 | N2 + Institution | LightGBM · lags only | 2.65% | +43.57% | 0.7276 | 94.34% |
| Holdout 2026 | N5 + Program | CatBoost · 49 variables | 8.42% | +7.86% | 0.9549 | 57.21% |
| Holdout 2026 | N5 + Program | CatBoost · lags only | 7.86% | +16.87% | 0.8915 | 59.51% |
| Holdout 2026 | N5 + Program | LightGBM · 49 variables | 8.15% | +17.34% | 0.9250 | 57.83% |
| Holdout 2026 | N5 + Program | LightGBM · lags only | 7.98% | +15.87% | 0.9059 | 59.66% |
| Holdout 2026 | N8 + Attendance mode | CatBoost · 49 variables | 12.27% | +13.21% | 0.9372 | 41.59% |
| Holdout 2026 | N8 + Attendance mode | CatBoost · lags only | 11.31% | +26.97% | 0.8640 | 44.62% |
| Holdout 2026 | N8 + Attendance mode | LightGBM · 49 variables | 12.14% | +19.01% | 0.9274 | 42.18% |
| Holdout 2026 | N8 + Attendance mode | LightGBM · lags only | 11.60% | +23.42% | 0.8859 | 43.26% |
| 2026 validation (8,329 common cells) | N2 + Institution | CatBoost · 49 variables | 2.77% | +23.90% | 0.8497 | 90.57% |
| 2026 validation (8,329 common cells) | N2 + Institution | CatBoost · lags only | 2.54% | +26.28% | 0.7794 | 90.57% |
| 2026 validation (8,329 common cells) | N2 + Institution | LightGBM · 49 variables | 2.45% | +45.52% | 0.7517 | 90.57% |
| 2026 validation (8,329 common cells) | N2 + Institution | LightGBM · lags only | 2.33% | +26.63% | 0.7130 | 94.34% |
| 2026 validation (8,329 common cells) | N5 + Program | CatBoost · 49 variables | 8.08% | +10.97% | 0.9588 | 58.88% |
| 2026 validation (8,329 common cells) | N5 + Program | CatBoost · lags only | 7.44% | +19.48% | 0.8832 | 61.67% |
| 2026 validation (8,329 common cells) | N5 + Program | LightGBM · 49 variables | 7.81% | +19.14% | 0.9273 | 59.65% |
| 2026 validation (8,329 common cells) | N5 + Program | LightGBM · lags only | 7.58% | +18.97% | 0.9004 | 61.59% |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | CatBoost · 49 variables | 11.77% | +17.05% | 0.9401 | 43.34% |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | CatBoost · lags only | 10.73% | +29.82% | 0.8568 | 46.62% |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | LightGBM · 49 variables | 11.63% | +21.05% | 0.9291 | 44.10% |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | LightGBM · lags only | 11.01% | +26.59% | 0.8796 | 45.35% |

**Table A.36.** Diebold–Mariano comparisons between groups (standard error clustered by institution). A positive DM favors the second term.

| Set | Level | Comparison | DM sq. | p | DM abs. | p  |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N2 + Institution | C49 − Crez | −3.13 | 0.0027 | −3.70 | 0.0005 |
| OOF 2019-2025 | N2 + Institution | L49 − Lrez | −2.18 | 0.0332 | −2.50 | 0.0151 |
| OOF 2019-2025 | N2 + Institution | Crez − Lrez | +3.82 | 0.0003 | +3.92 | 0.0002 |
| OOF 2019-2025 | N2 + Institution | C49 − L49 | +1.73 | 0.0880 | +1.44 | 0.1542 |
| OOF 2019-2025 | N5 + Program | C49 − Crez | −2.97 | 0.0043 | −4.44 | < 0.0001 |
| OOF 2019-2025 | N5 + Program | L49 − Lrez | −0.72 | 0.4745 | +0.10 | 0.9205 |
| OOF 2019-2025 | N5 + Program | Crez − Lrez | +3.31 | 0.0016 | +7.50 | < 0.0001 |
| OOF 2019-2025 | N5 + Program | C49 − L49 | +2.47 | 0.0164 | +2.01 | 0.0486 |
| OOF 2019-2025 | N8 + Attendance mode | C49 − Crez | −2.40 | 0.0195 | −0.83 | 0.4093 |
| OOF 2019-2025 | N8 + Attendance mode | L49 − Lrez | +0.81 | 0.4228 | +4.22 | < 0.0001 |
| OOF 2019-2025 | N8 + Attendance mode | Crez − Lrez | +2.78 | 0.0073 | +7.11 | < 0.0001 |
| OOF 2019-2025 | N8 + Attendance mode | C49 − L49 | +2.29 | 0.0258 | +1.74 | 0.0866 |
| Holdout 2026 | N2 + Institution | C49 − Crez | −0.20 | 0.8393 | +0.26 | 0.7931 |
| Holdout 2026 | N2 + Institution | L49 − Lrez | −1.09 | 0.2796 | −0.60 | 0.5531 |
| Holdout 2026 | N2 + Institution | Crez − Lrez | −0.40 | 0.6883 | +0.09 | 0.9298 |
| Holdout 2026 | N2 + Institution | C49 − L49 | +1.91 | 0.0621 | +1.70 | 0.0948 |
| Holdout 2026 | N5 + Program | C49 − Crez | +1.05 | 0.2993 | +3.18 | 0.0025 |
| Holdout 2026 | N5 + Program | L49 − Lrez | −0.23 | 0.8226 | +1.03 | 0.3061 |
| Holdout 2026 | N5 + Program | Crez − Lrez | −0.24 | 0.8075 | −1.16 | 0.2521 |
| Holdout 2026 | N5 + Program | C49 − L49 | +1.61 | 0.1140 | +2.96 | 0.0047 |
| Holdout 2026 | N8 + Attendance mode | C49 − Crez | +2.23 | 0.0300 | +5.99 | < 0.0001 |
| Holdout 2026 | N8 + Attendance mode | L49 − Lrez | +0.94 | 0.3495 | +4.65 | < 0.0001 |
| Holdout 2026 | N8 + Attendance mode | Crez − Lrez | −1.20 | 0.2350 | −2.07 | 0.0432 |
| Holdout 2026 | N8 + Attendance mode | C49 − L49 | +1.47 | 0.1474 | +1.60 | 0.1166 |
| 2026 validation (8,329 common cells) | N2 + Institution | C49 − Crez | +0.19 | 0.8482 | +0.73 | 0.4683 |
| 2026 validation (8,329 common cells) | N2 + Institution | L49 − Lrez | −0.74 | 0.4610 | +0.44 | 0.6626 |
| 2026 validation (8,329 common cells) | N2 + Institution | Crez − Lrez | +0.03 | 0.9744 | +0.92 | 0.3628 |
| 2026 validation (8,329 common cells) | N2 + Institution | C49 − L49 | +1.68 | 0.0990 | +1.81 | 0.0768 |
| 2026 validation (8,329 common cells) | N5 + Program | C49 − Crez | +1.00 | 0.3204 | +3.46 | 0.0011 |
| 2026 validation (8,329 common cells) | N5 + Program | L49 − Lrez | −0.02 | 0.9843 | +1.26 | 0.2149 |
| 2026 validation (8,329 common cells) | N5 + Program | Crez − Lrez | −0.12 | 0.9013 | −1.32 | 0.1920 |
| 2026 validation (8,329 common cells) | N5 + Program | C49 − L49 | +1.68 | 0.0996 | +2.73 | 0.0085 |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | C49 − Crez | +2.20 | 0.0325 | +5.92 | < 0.0001 |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | L49 − Lrez | +0.96 | 0.3425 | +4.47 | < 0.0001 |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | Crez − Lrez | −1.41 | 0.1656 | −2.39 | 0.0204 |
| 2026 validation (8,329 common cells) | N8 + Attendance mode | C49 − L49 | +1.64 | 0.1064 | +1.65 | 0.1054 |

**Table A.37.** Year-by-year breakdown of the factorial design in the OOF and the 2026 holdout: WAPE at N8 and differences in WAPE points (negative = the 49 variables improve), observed enrollment; years of history = year − 2018.

| Year | History (years) | N8 C49 | N8 Crez | N8 L49 | N8 Lrez | N8 C49 − Crez | N8 L49 − Lrez | N2 C49 − Crez | N2 L49 − Lrez |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 1 | 14.36% | 16.13% | 14.32% | 15.06% | −1.77 | −0.74 | −2.17 | −1.68 |
| 2020 | 2 | 14.69% | 15.17% | 14.88% | 14.44% | −0.48 | +0.44 | −0.70 | +0.75 |
| 2021 | 3 | 15.50% | 15.49% | 15.36% | 15.37% | +0.01 | −0.01 | −0.97 | −1.21 |
| 2022 | 4 | 16.31% | 17.22% | 16.47% | 16.31% | −0.92 | +0.16 | −2.15 | −0.86 |
| 2023 | 5 | 16.20% | 14.91% | 15.39% | 14.40% | +1.29 | +0.99 | +1.63 | +0.26 |
| 2024 | 6 | 13.63% | 13.20% | 13.59% | 12.76% | +0.43 | +0.82 | −0.24 | −0.19 |
| 2025 | 7 | 12.45% | 11.69% | 12.52% | 11.83% | +0.76 | +0.69 | +0.31 | +0.31 |
| 2026 | 8 | 12.27% | 11.31% | 12.14% | 11.60% | +0.96 | +0.54 | +0.09 | −0.19 |

*Note:* mean 2019–2021 versus 2022–2025 at N8: C49 − Crez −0.75 versus +0.39 points; L49 − Lrez −0.10 versus +0.67. Correlation of the difference with years of history (2019–2025, n = 7): 0.79 with both algorithms at N8; 0.63 and 0.48 at N2. At N2, the advantage of the exogenous variables is greater in 2019–2021 (C49 − Crez −1.28) and almost disappears in 2022–2025 (−0.11), with 2022 as an exception (−2.15 points). With seven years there is no power to separate the pattern from year-to-year variation.

# A.23 2027 forecasts: details

C49 is the frozen forecast with no changes (lag = 2026 value clipped in 75 cells); only its bands are recalibrated with observed residuals. Crez, L49 and Lrez use the specifications of the factorial design, trained with 2018–2026 on the same 9,069 cells, with the 2027 lag equal to the observed 2026 enrollment (in L49, the lag and the two lagged market variables are recomputed with the observed enrollment and the exogenous variables remain at their 2026 value). Bands: conformal, stratified by size, on the OOF residuals of each model against observed enrollment (validation with 2019–2025 OOF against the 2026 holdout; production with 2019–2026 OOF). The global model (Lrez) is LightGBM 4.6.0 with 31 leaves, 20 minimum observations per leaf, 300 trees, learning rate 0.03, subsampling 0.8 and seed 42.

**Table A.38.** 2027 totals of the factorial design, growth over 741,615 and bands.

| Model | 2027 total | Growth over 741,615 | Cell coverage, 2026 holdout | Median cell width | Median band by institution |
|---|---:|---:|---:|---:|---:|
| CatBoost · 49 variables | 761,058 | +2.62% | 92.49% | 36.6 | 20.62% |
| CatBoost · lags only | 767,934 | +3.55% | 93.25% | 36.4 | 25.16% |
| LightGBM · 49 variables | 760,672 | +2.57% | 92.25% | 37.1 | 20.74% |
| LightGBM · lags only | 768,499 | +3.63% | 92.31% | 36.1 | 23.21% |

*Note:* persistence (F0) 741,615; national Comb (FN) 746,696 (+0.69%). With the frozen (clipped) lag, the global model would give 766,790 (+3.39%). National benchmark (N1 only) on the observed 2017–2026 national series: ETS 741,612; ARIMA 752,425; Theta 746,051; Comb 746,696. Indicative non-conformal range of the C49 total: 719,308 to 777,914 (OOF aggregate errors from −2.17% to +5.80%).

**Table A.39.** Coverage of the bands on the 2026 holdout by level (calibration with 2019–2025 OOF, observed enrollment).

| Model | Cell | N2 + Institution | N3 + Field | N4 + Region | N5 + Program | N6 + Status | N7 + Gender | N8 + Attendance mode |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CatBoost · 49 variables | 92.49% | 94.34% | 93.70% | 93.04% | 92.19% | 93.43% | 93.09% | 92.74% |
| CatBoost · lags only | 93.25% | 98.11% | 96.13% | 96.29% | 94.19% | 94.21% | 93.67% | 93.73% |
| LightGBM · 49 variables | 92.25% | 96.23% | 93.46% | 93.35% | 92.44% | 93.25% | 92.92% | 92.67% |
| LightGBM · lags only | 92.31% | 94.34% | 95.88% | 94.74% | 93.36% | 93.62% | 93.43% | 93.28% |

**Table A.40.** 2027 breakdown by student status and attendance mode (change over the 2026 observed enrollment of each cut).

| Cut | Value | Actual 2026 | CatBoost · 49 variables | CatBoost · lags only | LightGBM · 49 variables | LightGBM · lags only |
|---|---:|---:|---:|---:|---:|---:|
| student status | Continuing | 589,678 | +3.44% | +3.99% | +3.25% | +3.80% |
| student status | First-year | 151,937 | −0.54% | +1.82% | −0.07% | +2.93% |
| attendance mode | Distance | 43,050 | +14.56% | +10.71% | +12.89% | +12.23% |
| attendance mode | Daytime | 650,477 | +2.27% | +3.71% | +2.29% | +3.50% |
| attendance mode | Other | 969 | −22.95% | −36.33% | −18.15% | −14.60% |
| attendance mode | Blended | 8,954 | +10.27% | +9.36% | +7.94% | +8.56% |
| attendance mode | Evening | 38,165 | −5.93% | −7.66% | −5.06% | −4.72% |

# A.24 Performance by institution in the 2026 validation

**Table A.41.** Performance by institution on the 2026 official enrollment (2025 origin).

| Measure | Institutions |
|---|---:|
| Institutional total within ±5% | 40 of 53 |
| Institutional total within ±10% | 49 of 53 |
| Internal WAPE lower than that of persistence | 42 of 53 (79%) |
| Fell in 2026 and the forecast was above the observed value | 14 of 14 |
| Fell in 2026 and the forecast also anticipated the decline | 10 of 14 |
| Grew in 2026 and the forecast was below the observed value | 30 of 39 |

*Note:* among the 49 institutions with at least 50 cells and 2,000 enrollments, the median total error falls from 3.67% in the smaller half to 1.74% in the larger half, and the median internal WAPE, from 14.20% to 10.03%.

