---
title: "When the naïve forecast is the lag: Evaluating program-level university enrollment forecasts in Chile"
lang: en-US
bibliography: references.bib
csl: apa.csl
link-citations: true
---

<!-- Anonymized manuscript for double-anonymous review. Authorship, affiliation, funding and acknowledgments appear exclusively on the title page (title_page_en.md). -->

## Abstract {-}

University enrollment is so inertial that persistence is a hard benchmark to beat and an easy one to mismeasure. We forecast Chilean undergraduate university enrollment by program, region, attendance mode, gender and student status from public administrative records. Against official 2026 enrollment, out of sample, a global gradient-boosting model reduced the weighted absolute percentage error from 12.69% (persistence) to 11.49%, and a lags-only global model reached 11.16%; series-by-series ETS, ARIMA and Theta were worse than persistence. A factorial design shows that the contribution of exogenous features depends on the period: it does not improve cell-level accuracy in 2026 but does improve aggregates in 2019-2025. Stratified conformal intervals achieved the best interval score at almost all levels. When the naïve forecast and the lag share their construction, a matching defect biases skill. A prospective 2027 comparison is frozen.

**Keywords:** Persistence benchmark; Gradient boosting; Conformal prediction; Rolling origin; Data leakage; Global models; Higher education

# 1. Introduction

Higher education planning requires enrollment projections at several levels: the authorities need the system total to size student financial aid and the supply of places; universities need projections by institution, faculty and program. This problem has a long tradition in institutional research [@orwig1972; @hoenack1979; @brinkman1997], and some states publish official projections [@nces2024]; in Chile, high-quality descriptive statistics are published, but no enrollment forecast for the following year. It is a case of forecasting in social settings [@makridakis2020social]: enrollment responds to individual decisions, policy changes and aggregate shocks, is heterogeneous along several crossed dimensions (institution, program, region, attendance mode, gender, and first-year versus continuing student status) and suffered unprecedented disturbances in 2020–2022. More consequential for evaluation, it is highly inertial: a five-year program carries four cohorts already enrolled, so most of next year's level is determined before admission.

That inertia turns the choice and construction of the benchmark forecast into the center of the evaluation problem. New methods must be compared against simple, well-constructed benchmarks [@makridakis2018plos; @makridakis2020m4; @hewamalage2023], and choosing persistence as the reference changes the perception of skill [@mittermaier2008]. In enrollment, persistence alone attains a coefficient of determination (R²) on levels of between 0.967 and 0.972 in the last two observed years. Any model will obtain a high R²; the pertinent question is whether it beats persistence, and answering it requires persistence to be measured correctly.

This article studies that problem with global gradient boosting models [@prokhorenkova2018catboost; @ke2017lightgbm] fitted on a panel of 82,967 cell-years (2018–2026) at the institution × program × region × attendance mode × gender × student status level, built from public administrative records. The models are compared with persistence, with classical statistical methods fitted series by series (drift, ETS, ARIMA, Theta and their combination), and against each other, through a factorial design that crosses the algorithm (CatBoost or LightGBM) with the feature set (49 variables, with exogenous features, or lags only). The evaluation combines a rolling origin [@tashman2000], a blind holdout, a validation against the official 2026 release—which revealed a failure mode that the literature does not document explicitly—and a pre-specified prospective comparison for 2027.

**Contributions.** The article makes five contributions:

1. **A failure mode of evaluation against persistence.** When the naïve forecast is built from the same lag column that feeds the model, a defect in the key that matches each cell to its previous-year value contaminates the numerator and the denominator of the skill score simultaneously. In a real case, the same defect inflated the skill of one year (+77.4%) and sank it the following year (−8.0%), without any model-centered diagnostic detecting it; we propose concrete controls (Sections 4.2, 5.1 and 6.3).
2. **Comparative evidence at the program level.** At the cell level, the global models beat persistence and persistence beats the per-series methods; the per-series methods are only competitive at the national total. A factorial algorithm × feature design shows that the contribution of the exogenous variables depends on the period and the aggregation level. The differences are tested with Diebold–Mariano tests between groups with standard errors clustered by institution (Sections 5.5 and 5.6).
3. **An out-of-sample evaluation with a declared status and a pre-specified prospective test.** The evaluation against the official 2026 data is out of sample but not prospective, because that data motivated the audit that corrected the pipeline. It is complemented by freezing, on 20 November 2026, the 2027 forecasts of the full factorial design and of the benchmarks, with an evaluation protocol that fixes five hypotheses in advance (Sections 5.4 and 5.10).
4. **Stratified conformal intervals with verified coverage**: 92.49% on the 2026 holdout with observed residuals, against a 90% target, and a lower interval score than an unstratified conformal predictor and than ETS at nearly all levels (Sections 4.9 and 5.7).
5. **Metrics and leakage in inertial series.** R² on levels does not discriminate between the model and persistence, and performance on the rate and on the level tell different stories. The isolated leakage of a precomputed target encoding is 2.92% to 3.74% of the validation RMSE, depending on the encoder, more than the differences between algorithms (Sections 5.8, 6.1 and 6.2).

Section 2 reviews the literature; Section 3 describes the data; Section 4, the methodology; Section 5 reports the results, beginning with the diagnosis of the evaluation defect; Section 6 discusses implications and limitations, and Section 7 concludes. The Online Appendix contains the operational details and complementary results.

# 2. Related literature

## 2.1 Enrollment forecasting and official projections

Enrollment forecasting originated in institutional research, with projection models for planning [@orwig1972], demand models [@hoenack1979] and reviews of cohort, time-series and regression methods [@brinkman1997]; recent work continues to model institutional aggregates [@chen2019intl; @bowman2021], and the fuzzy time-series line of research turned the annual enrollment of one university into a recurring benchmark over a single series [@song1993; @chen1996]. The US NCES publishes official projections [@nces2024]; in Chile, the SIES publishes enrollment by program [@sies2025matricula; @sies2025informe] and the CNED institutional indicators [@cned2026indices], but neither publishes a forecast for the following year. In the search conducted for this work, in CrossRef and open sources, no indexed study was found that forecasts enrollment at the program × region × gender level with a blind evaluation against persistence. \[PENDING: systematic search in Scopus/WoS/SciELO on *enrollment forecasting* and *higher education demand*, with declared inclusion criteria.\]

## 2.2 Forecast evaluation, benchmarks and tests

Out-of-sample evaluation with a rolling origin is the standard for comparing methods [@tashman2000]; blocked cross-validation is valid only under certain conditions, in particular for purely autoregressive models [@bergmeir2012; @bergmeir2018note], and @hewamalage2023 catalog the most common pitfalls. The M competitions showed that simple statistical benchmarks are hard to beat and that comparison against them is mandatory [@makridakis2018plos; @makridakis2020m4; @petropoulos2022]. The MASE of @hyndman2006 scales the error by that of the naïve forecast within sample, whereas relative measures compare it with a benchmark over the same period [@armstrong1992; @davydenko2013]. The skill score based on the squared error, standard in meteorology [@murphy1988], is interpreted in @wheatcroft2019, and the choice of persistence as the reference changes the perception of skill [@mittermaier2008]; consistency between loss and functional justifies reporting absolute and squared metrics [@gneiting2011], and *forecast value added* translates the comparison into the language of planning [@fildes2025fva]. Error differences are contrasted with the test of @diebold1995, its small-sample correction [@harvey1997] and multiple comparisons such as MCB [@koning2005].

## 2.3 Hierarchical forecasting and global models

Enrollment has a grouped structure: institution, region, attendance mode, gender and student status are crossed. Forecast reconciliation produces coherent forecasts at all levels [@hyndman2011optimal; @wickramasuriya2019; @hyndman2016fast; @panagiotelis2021], with classic regional applications [@athanasopoulos2009] and a recent review [@athanasopoulos2024review]. On tabular data, gradient boosting—XGBoost [@chen2016xgboost], LightGBM [@ke2017lightgbm] and CatBoost [@prokhorenkova2018catboost]—matches or outperforms deep networks [@shwartz2022tabular]; in forecasting, trees dominated recent competitions [@januschowski2022trees; @bojer2021kaggle], and a global LightGBM outperformed local methods on the hierarchical series of the M5 [@makridakis2022m5acc; @makridakis2022m5unc]. The foundation for fitting a single model to many series is given by @monteromanso2021.

## 2.4 Data leakage, conformal prediction and prospective evaluation

Data leakage introduces, in training, information that would not be available at forecast time [@kaufman2012; @kapoor2023leakage]; target encoding [@micci2001target] is a frequent source when it is computed outside the folds [@pargent2022]. Conformal prediction [@vovk2005] produces intervals with a guaranteed marginal coverage under exchangeability, and its split variant avoids refitting the model [@papadopoulos2002; @lei2018; @angelopoulos2023]. Mondrian conformal predictors calibrate separately within categories [@vovk2005]; @vovk2013conditional demonstrates their conditional validity and @bostrom2020mondrian define them for regression with difficulty-based categories, which is the idea behind stratifying by size; @johansson2015mondrian study categories with few residuals, and conformalized quantile regression is an alternative [@romano2019]. @barber2023beyond bound the loss of coverage under drift, and the interval score evaluates coverage and width jointly [@gneiting2007; @gneiting2014]. The distinction between prediction and postdiction [@nosek2018] gives value to forecasts published before the outcome, as in the real-time evaluations of influenza and COVID-19 [@reich2019; @cramer2022] and in forecasting tournaments [@tetlock2014].

## 2.5 Context: Chilean higher education

The expansion of Chilean university enrollment is described as massification with segmentation, in a system between the market and the state [@brunner1993; @espinoza2013; @espinoza2024; @bernasconi2026; @oecd2009chile; @oecd2017chile; @ferreyra2017]. Three features motivate variables of the model: funding—the state-guaranteed loan (Crédito con Aval del Estado) affects enrollment [@solis2017] and dropout [@rau2013], and the tuition-free policy (*gratuidad*) changed demand-side funding [@degayardon2017; @rodriguez2021gratuidad; @clasing2024]—; information on returns, whose publication changes enrollment decisions [@hastings2015; @hastings2013]; and the structure of demand, with a centralized admission system [@rios2021] and a gender gap in program choice [@bordon2020]. Chilean research using machine learning has concentrated on individual-level dropout [@miranda2017; @ramirez2018; @palacios2021], a classification problem with internal data; the problem in this work is a regression problem on aggregated cells with public, system-wide data, and the difference lies in the level of analysis, not in technical sophistication.

# 3. Data

## 3.1 Sources

The panel integrates public administrative and statistical sources on the Chilean higher education system and the regional economy (Table 1). Enrollment comes from the SIES database of enrolled students by program, which is the only source containing the variable of interest at the required granularity and serves as the anchor table. The other sources contribute prices, selectivity, academic staff, infrastructure, retention and regional macroeconomic context. Three normalization catalogs—campuses to regions, institutions and program names—are derived from the same sources and do not constitute independent datasets.

**Table 1.** Data sources integrated into the panel.

| Source | Agency | Variables contributed | Period |
|---|---|---|---|
| Base de Matriculados en Educación Superior (Higher Education Enrollment Database) [@sies2025matricula] | SIES, Subsecretaría de Educación Superior (Undersecretariat of Higher Education) | Enrollment by institution × program × attendance mode × gender × student status × year (anchor table) | 2007–2026 (modeled 2018–2026) |
| INDICES, higher education databases [@cned2026indices] | CNED | Tuition fees, enrollment fee, admission scores, program duration, accreditation | 2005–2026 (2026 partial) |
| INDICES, infrastructure and academic staff processes [@cned2026infraestructura] | CNED | Academic staff by degree and contract type; built m², classrooms and offices by campus | 2018–2025 |
| Regional GDP, volume at previous year's chained prices, 2018 reference [@bcch2026pibregional] | Banco Central de Chile (Central Bank of Chile) | Annual regional GDP (billions of chained pesos; edition dated 23-04-2026, preliminary figures) | 2018–2025 (2026 carried forward) |
| Encuesta Nacional de Empleo (National Employment Survey, ENE) [@ine2026ene] | Instituto Nacional de Estadísticas (National Statistics Institute, INE), also disseminated through the Sistema de Información del Mercado Laboral (Labor Market Information System, SIMEL) | Annual regional unemployment rate (average of the year's moving quarters; in 2025, 10 of 12) | 2018–2025 (2026 carried forward) |
| Buscador de Empleabilidad e Ingresos (Employability and Earnings Finder) [@mineduc2025empleabilidad] | SIES (mifuturo.cl portal) | First-year retention and employability by program and institution | 2018–2025 |

*Note:* "Carried forward" indicates that the last published value is repeated for the year not yet published (Section 3.4). Regional GDP corresponds to the volume series at previous year's chained prices. The 2025 annual unemployment value averages the 10 moving quarters published at the time of the run (those beginning between January and October), versus 12 in complete years.

As a cross-validation of data ingestion, the totals computed independently from the SIES microdata file match those of the official 2026 enrollment report exactly: 1,497,548 total enrollments, 1,372,167 undergraduate enrollments and 759,045 undergraduate enrollments at universities [@sies2025matricula]. \[PENDING: add to the .bib the entry for the SIES *Informe de Matrícula en Educación Superior 2026* (Higher Education Enrollment Report), which is the edition whose figures are cited; the current .bib contains only the 2025 edition, `sies2025informe`.\]

## 3.2 Panel construction

Processing normalizes the keys through canonical catalogs of regions, institutions and programs and left-joins each source onto the anchor table, so that no enrollment row is lost for lack of a secondary source. The ingestion rules, conservation checks and coverage of each source are detailed in Appendices A.1 and A.2.

The unit of analysis is the **cell-year**: institution × program name × region × attendance mode × gender × student status (first-year or continuing) × year. The final panel contains **82,967 observations** for 2018–2026, with 52 columns, of which 49 enter the model. The year 2018 is used exclusively as the base of the lag and receives no predictions. The universe comprises 62 university institutions, 1,432 canonical program names, 16 regions and 10 academic fields. Cells with previous-year enrollment below ten students, whose growth rates are mostly noise, are excluded; Appendix A.2 documents row and enrollment retention at each processing stage.

The work covers universities exclusively. Centros de formación técnica (technical training centers) and institutos profesionales (professional institutes), which account for about half of undergraduate enrollment in the system, are outside its scope.

## 3.3 Target variable

The variable to be forecast is the growth rate of the cell's enrollment,

$$ \text{rate}_t = \frac{y_t - y_{t-1}}{y_{t-1}}, $$

where $y_t$ is the cell's enrollment in year $t$. For training, the rate is capped at the 1st and 99th percentiles (winsorization) and transformed with the inverse hyperbolic sine, which is defined on all real numbers, preserves the sign, and behaves like the identity near zero and like a logarithm in the tails:

$$ z_t = \operatorname{arcsinh}(\text{rate}_t) = \ln\!\left(\text{rate}_t + \sqrt{\text{rate}_t^2 + 1}\right). $$

The level is reconstructed as

$$ \hat{y}_t = y_{t-1}\,\bigl(1 + \sinh(\hat{z}_t)\bigr). $$

This reconstruction is central to reading the results. The model is **optimized** on the rate—a high-variance, low-predictability variable—but **evaluated** on absolute enrollment—an extremely inertial variable—which is the quantity that is budgeted. Section 6.2 discusses why this asymmetry explains the gap between an R² of the order of 0.10 on the rate and one of 0.98 on the level.

**Evaluation against the observed value.** Winsorization is applied only to the training target: every evaluation in this article compares forecasts with each cell's observed enrollment. An earlier version of this evaluation instead compared against the value reconstructed with the clipped rate, which differs from the observed value in 1,430 rows of 2018–2026 and raises the observed total by between +0.03% and +0.34% depending on the year (Appendix A.15). With the observed value, no conclusion changes sign, but the figures do; those for the holdout and the OOF are reported with the observed value, and the validation against the official 2026 data already used it.

## 3.4 Imputation and unpublished exogenous variables

The secondary sources have different degrees of completeness, so imputation proceeds in layers that respect the cell hierarchy; each layer resolves only what the previous one left empty: temporal (interpolation within institution-region), hierarchical (from institution × program to institution × field and field), regional by program, institutional and, finally, the global median (Appendix A.3). A row-level indicator records whether any variable was imputed and enters the model. Of the rows, 70.9% contain at least one imputed variable, concentrated in tuition fees and retention; the proportion increases in 2026 because several sources have not yet published that year.

Regional GDP and unemployment are not imputed: when a source has not yet published the latest year, its last regional value is repeated and the carry-forward is recorded. In the re-estimation with data up to 2026, the 2026 GDP and unemployment repeat those of 2025, and academic staff, infrastructure and retention take the latest value or the available historical median (Appendix A.3).

# 4. Methodology

## 4.1 Overall design and forecast origins

The same pipeline, with no change in method, is run from two forecast origins, which are distinguished throughout the text:

- **2025 origin.** Cross-validation on 2019–2024, blind holdout 2025, final model fitted on 2018–2025 (73,896 observations) and forecast for 2026, evaluated against the official release of July 2026 (Section 5.4).
- **2026 origin.** Cross-validation on 2019–2025, blind holdout 2026, final model fitted on 2018–2026 (82,967 observations) and *ex ante* forecast for 2027 (Section 5.10).

Unless otherwise indicated, the figures in Sections 5.2, 5.3 and 5.5 to 5.10 refer to the 2026 origin; those in Section 5.4 and the rows of Table 10 labeled as such, to the 2025 origin. The 2026 validation of the 2025 origin and the 2026 holdout of the 2026 origin measure the same year with different instruments (Section 5.2).

## 4.2 The lag key

The model's inertia variable is the previous-year enrollment of the same cell, $y_{t-1}$. Building it requires matching each cell in a year with its counterpart in the previous year, and this matching fails when the nomenclature changes: SIES renames programs between editions without changing their code. With a key based on the literal name, a renamed cell loses its lag and silently leaves the modelable universe.

We therefore adopt a key with three cascading fallback levels (Table 2). The fine level matches on the literal name; the first fallback, on the program code, which SIES preserves across renamings; the second fallback matches the program within the region, aggregating attendance mode, gender and student status.

**Table 2.** Levels of the lag-matching key.

| Level | Matching key |
|---|---|
| Fine | institution, program name, region, attendance mode, gender, student status |
| Code | institution, program code, region, attendance mode, gender, student status |
| Intermediate | institution, program code, region |

**Share-based scaling.** The intermediate level aggregates three dimensions, so its total is not comparable with that of an individual cell: using it directly compares a part with the whole that contains it and produces spurious growth rates close to −1. The fallback is therefore applied scaled by the cell's share in its group,

$$ y^{\text{cell}}_{t-1} = y^{\text{group}}_{t-1} \times \frac{y^{\text{cell}}_{t}}{y^{\text{group}}_{t}}, $$

so that the cell inherits the *growth* of its group instead of being compared with its *level*. The general rule is that **the numerator and the denominator of a rate must share the key**.

The level used is recorded for each row. Of the 82,967 rows, 81,259 (97.9%) are matched at the fine level, 694 (0.8%) by code and 1,014 (1.2%) at the scaled intermediate level. Restricted to the cells evaluated in 2019–2026, matching is at the fine level for 98.10% of cells (98.89% of enrollment), by code for 0.66% (0.56%) and at the intermediate level for 1.25% (0.56%). Appendix A.4 documents the checks on the distribution of the lag by level and the performance by lag source.

## 4.3 The persistence forecast and its identity with the lag

The main benchmark is persistence, or the naïve forecast, $\hat{y}_t = y_{t-1}$. By construction, this forecast is **the same lag column** that feeds the model. This is not an implementation choice but an identity: the persistence forecast and the model's inertia variable are the same object.

Consequently, a defect in the lag key degrades **both at once** and biases the skill score—a ratio between the two errors—in a direction that depends on which of the two is damaged more (Sections 5.1 and 6.3).

## 4.4 Temporal validation

The temporal structure of the panel rules out random splits. The design has four components:

- **Blind holdout:** the last observed year (2026 at the 2026 origin; 2025 at the 2025 origin) plays no role in any selection or optimization stage.
- **Expanding-window cross-validation:** fold $k$ trains on $\{2018, \ldots, 2017+k\}$ and validates on $2018+k$; seven folds at the 2026 origin (validation 2019–2025) and six at the 2025 origin. This is the rolling origin of @tashman2000; the validity of standard cross-validation established by @bergmeir2018note is restricted to purely autoregressive models, a condition not met by a model with exogenous variables and a panel of changing composition [@bergmeir2012; @hewamalage2023].
- **Retrospective out-of-fold (OOF) predictions:** for each year $Y \in \{2019, \ldots, 2026\}$, a model is fitted on all data prior to $Y$ and $Y$ is predicted.
- **Validation against the official release:** the forecast from the 2025 origin was evaluated against the 2026 enrollment published by SIES, data that no fitting stage saw, with the caveat stated in Section 5.1.

Hyperparameters are optimized once and reused for each annual OOF model, so the early OOF incorporates later information; the holdout and the forecast do not have this problem (Section 6.5).

## 4.5 Empirical detection of shock years

To avoid relying on a hand-defined indicator, the candidate years (2020–2022) are classified with an explicit criterion: a year whose annual mean or standard deviation of the target departs by more than 1.96 standard deviations from that of the non-candidate years is a *level shock* or a *dispersion shock*, and a candidate with a negative aggregate change not so classified is a *relapse shock* (Appendix A.6). At both origins the procedure classifies 2020 and 2022 as level shocks and leaves the other two categories empty, so their indicators are constant.

## 4.6 Variables and within-fold target encoding

Four groups of derived variables are built on top of the original ones: the lag (on a $\log(1+x)$ scale); faculty ratios (share of PhDs, of master's degree holders and of full-time hours); market and competition indicators (competitive density, regional relative tuition, relative selectivity, concentration of lagged enrollment within the institution and the cell's lagged share of the program's regional enrollment); and the shock indicators. The final set has 49 variables: 45 numerical and 4 categorical (region, institution, program and academic field). Appendix A.5 presents the data dictionary.

The four categorical variables, with cardinalities of 16, 62, 1,432 and 10, are encoded with smoothed target encoding. The encoder weights each category's mean with a sigmoid of its number of observations,

$$ \text{TE}(c) = \bar{z}\,(1 - w_c) + \bar{z}_c\, w_c, \qquad w_c = \frac{1}{1 + e^{-(n_c - k)/s}}, \qquad s = 30,\ k = 20, $$

and is fitted **within** each fold, as a step of the same preprocessing pipeline that is refitted at each evaluation, using only the fold's training data. A version precomputed on the whole panel with the $m$-estimator ($m = 30$) is excluded from training and used only in the experiment in Section 5.8.

## 4.7 Models, benchmarks and optimization

**Main model.** The pipeline's reference model is CatBoost [@prokhorenkova2018catboost] with the 49 variables of Section 4.6 (hereafter C49). It is optimized with Optuna [@akiba2019optuna] (TPE, median pruning, 50 trials per candidate, mean fold RMSE on the arcsinh scale). After optimization, CatBoost ranked **third** by cross-validation RMSE (0.2949 versus 0.2933 for XGBoost and 0.2943 for LightGBM; at the 2025 origin, 0.2986 versus 0.2974 and 0.2982), with a difference smaller than the measured bias of the target encoding (Section 5.8). It was retained for continuity of method between the validated run (2025 origin) and the forecast run (2026 origin), and the choice has no performance basis. The versions of `shap` were 0.45.1 (2025 origin) and 0.54.1 (2026 origin). The hyperparameters selected at the 2026 origin are 2,000 iterations, learning rate 0.0376, depth 7, L2 regularization of 1.75, bagging temperature 0.546 and 183 border counts (Appendix A.8). Other benchmarks reported on the rate are in Appendix A.7.

**Classical per-series benchmarks.** Each cell is treated as an annual series whose last value is the lag, so that persistence is exactly the benchmark of Section 4.3. On each series we fit, with `statsforecast` 2.1.1, a random walk with drift (RWD), AutoETS without seasonality, including the damped variant [@hyndman2002ets; @hyndman2008auto], AutoARIMA [@hyndman2008auto], the Theta method [@assimakopoulos2000theta], and the mean of ETS, ARIMA and Theta (Comb). Series with fewer than three observations fall back to persistence; in 2019 all of them do (Appendix A.16).

**Lags-only global model.** A LightGBM [@ke2017lightgbm] on the arcsinh of the rate with the $t-1$, $t-2$ and $t-3$ lags of the cell's arcsinh rate, the relative year, and the categorical identifiers (institution, field, region, program, student status, gender and attendance mode), without exogenous variables or lagged level [@monteromanso2021]. Its hyperparameters are chosen on a fixed grid of 12 combinations by mean cross-validation RMSE on the same seven folds (31 leaves, 20 minimum observations per leaf and 300 trees; cross-validation RMSE 0.2869). It is denoted Lrez.

**Factorial algorithm × feature design.** To separate the algorithm's contribution from that of the exogenous variables, we cross two algorithms (CatBoost and LightGBM) with two feature sets (the 49 of the main model and lags only), with fixed hyperparameters, no new optimization, and the same origins: C49 is the published model; Crez applies C49's hyperparameters to the global model's variables, with within-fold sigmoid target encoding on the seven identifiers; L49 is a LightGBM with the 49 variables and within-fold sigmoid target encoding on the four categorical variables, with the same grid of 12 (63 leaves, 100 minimum observations per leaf and 800 trees); and Lrez is the global model above. In the validation against the official 2026 data, all four models apply their 2026-origin rate to the 2025 lag in 8,329 common cells, so C49 does not coincide exactly with the 2025-origin model (Appendix A.22).

**Hierarchical reconciliation.** Aggregates are obtained by bottom-up summation from the cell; as a comparison, N1–N5 are reconciled with OLS, structural WLS and MinT with shrinkage [@wickramasuriya2019; @hyndman2016fast] (Appendix A.21).

## 4.8 Metrics

All metrics are reported **with the persistence value alongside**: RMSE, MAE and R² on levels (with the caveat of Section 6.1); WAPE, $100 \times \sum|y - \hat{y}| / \sum y$, preferable to the MAPE in cells of very different sizes; aggregate bias, $100 \times (\sum \hat{y} - \sum y) / \sum y$; the percentage of groups within ±10% of the observed value; the skill score based on the mean squared error [@murphy1988; @wheatcroft2019], $\text{SS} = 1 - (\text{RMSE}_{\text{model}} / \text{RMSE}_{\text{pers}})^2$, positive when the model removes part of the persistence error; and the relative MAE [@davydenko2013], $\text{RelMAE} = \text{MAE}_{\text{model}} / \text{MAE}_{\text{pers}}$ over the same evaluated set, below one when the model outperforms persistence.[^relmae]

[^relmae]: The RelMAE is not the mean absolute scaled error (MASE) of @hyndman2006, which divides by the *in-sample* MAE of the one-step naïve forecast computed over the training period. Here the denominator is the MAE of persistence over the same evaluation period, which defines a relative error in the sense of @davydenko2013 and @armstrong1992. With a single group, as at the national level, the ratio reduces to the ratio of that group's absolute errors, which explains values such as 0.006. The reported values are the same as those computed by the pipeline; only their name changes.

Skill is sensitive to a few large errors in large cells, and the RelMAE is not; reporting both maintains consistency between loss function and functional [@gneiting2011].

**Significance of the differences.** For each level N2–N8 we apply a Diebold–Mariano-type test between groups [@diebold1995]: with $d_g = L(\text{method}_g) - L(\text{benchmark}_g)$ over the aggregated group's error, with squared and absolute loss, we test $E[d] = 0$ with a cluster-robust standard error by institution (CR1, 53 clusters) [@cameron2015cluster] and a $t$ distribution with $G-1$ degrees of freedom; at N2 the cluster coincides with the group. As a complement, we compare the mean rank of the absolute error among eight methods with the multiple comparison with the best (MCB) and the Nemenyi critical difference [@koning2005] \[PENDING: verified citation for the Nemenyi test\]; since it assumes independent groups, which does not hold within an institution, that test is liberal. At the national total (N1), where there is a single group per year, we apply the Diebold–Mariano test with the small-sample correction of @harvey1997 over the eight years of the OOF 2019–2026, with very low power.

**Intervals.** The 90% intervals are evaluated by empirical coverage, median width and interval score $\text{IS}_\alpha(l,u;y) = (u-l) + \tfrac{2}{\alpha}(l-y)\mathbb{1}\{y<l\} + \tfrac{2}{\alpha}(y-u)\mathbb{1}\{y>u\}$ with $\alpha = 0.10$ [@gneiting2007], and by its scaled version MSIS, which divides the mean interval score by the MAE of persistence on the same groups [@makridakis2020m4].

## 4.9 Conformal prediction intervals

We apply split conformal prediction [@papadopoulos2002; @lei2018] with a nominal level of 90%. Let $\{r_i\}_{i=1}^n$ be the ordered set of calibration residuals and $\alpha = 0.10$; the interval endpoints are the order statistics at positions

$$ k_{\text{hi}} = \left\lceil (n+1)(1 - \alpha/2) \right\rceil, \qquad k_{\text{lo}} = \left\lfloor (n+1)\,\alpha/2 \right\rfloor. $$

Three design decisions define the procedure:

1. **Stratification by size (Mondrian conformal predictor).** The error is strongly heteroskedastic: the upper quantile of the residual falls from 0.796 in cells of 10 to 13 students to 0.162 in cells of 168 or more. Calibration is performed separately within strata defined by deciles of the lag, following Mondrian conformal predictors [@vovk2005; @vovk2013conditional] in their regression version with difficulty-based categories [@bostrom2020mondrian].
2. **Calibration in the target space**, on the arcsinh scale, transformed with the pipeline's reconstruction, which preserves the order.
3. **Aggregates are not summed**, because summing intervals would assume that all cells err in the same direction. Each level is calibrated on its own error, $\log(\hat{y}/y)$, stratified by group size.

At least 30 residuals per stratum are required, so the national total carries no conformal interval. At the 2025 origin, calibration uses the 2019–2024 OOF residuals; at the 2026 origin, calibration uses residuals against observed enrollment: 2019–2025 OOF to measure coverage on the 2026 holdout and 2019–2026 OOF for the 2027 forecast. The coverage guarantee assumes exchangeability across years, which does not hold strictly under temporal drift [@barber2023beyond]; the empirical out-of-sample coverage is therefore the relevant evidence. The comparisons are an unstratified conformal predictor and the AutoETS intervals (Section 5.7).

# 5. Results

## 5.1 Diagnosis of an evaluation defect

**Detection.** A preliminary version of the pipeline, with a defect in the lag key, issued and fixed a forecast for 2026 in June 2026, before the official release of 10 July. Its skill had been +77.4% on the 2025 holdout; against the 2026 data it was **−8.0%**, worse than persistence. A deterioration of that magnitude between consecutive years prompted an audit of the pipeline.

**Finding.** The audit found two defects in the lag key:

1. **Renamings without a code fallback.** The key matched on the literal name without a fallback on the program code. In 2025, SIES renamed all 20 programs of one institution without changing their codes, and the pipeline discarded them: that institution's modelable enrollment fell from 3,726 to 351.
2. **Mixed granularity in the fallback.** The intermediate level aggregated attendance mode, gender and student status only in the denominator of the rate. This generated 3,763 rows with a median lag-to-cell ratio of 8× and a median rate of −0.875: nonexistent contractions, an artifact of comparing a cell with an aggregate that contains it.

Together, the defects corrupted about 4% of the training targets and, through the identity of Section 4.3, the persistence forecast in the same proportion.

**Correction.** With the code-based key and the share-based scaling of Section 4.2, the intermediate level went from a median rate of −0.875 with a ratio of 8.00× to +0.196 with a ratio of 0.84×, and the artificial targets fell from 2,944 to zero. The correction did not use 2026 data, and the defect is verifiable with 2018–2025 data. Table 3 contrasts both versions.

**Table 3.** Preliminary version (defective key) versus the corrected pipeline, both with the training window closed in 2025.

| | Preliminary version | Corrected pipeline |
|---|---:|---:|
| Training rows | 75,622 | 73,896 |
| Skill score, 2025 holdout | +77.39% | +22.46% |
| Skill score, 2026 validation | −8.02% | +26.71% |
| Aggregation levels with negative skill in 2026 | the four finest | none |
| WAPE 2026, fine cell | 12.20% | 11.49% |
| R² 2026 versus that of persistence | 0.9648 < 0.9674 | 0.9760 > 0.9673 |
| Aggregate error 2026 | −2.04% | −0.01% |
| Forecast versus observed growth | +0.23% vs +2.31% | +2.26% vs +2.27% |

*Note:* the persistence figures differ slightly between columns because persistence inherits the key defect (Section 4.3). The 2025 holdout figures for both versions were computed against the value reconstructed with the clipped rate, as in the original evaluation (Section 3.3); against observed enrollment, the skill of the corrected pipeline on that holdout is +22.87% (Table 4). Those for the 2026 validation use the official data.

**Epistemic status.** There was no data leakage — no 2026 data enter the corrected model — but that data acted as a **diagnostic signal** for the audit: the evaluation of the corrected pipeline on 2026 is *out of sample* but not *prospective*, because the correction was made after the outcome was known [@nosek2018]. The first prospective evaluation of the corrected pipeline will be that of 2027 (Section 5.10).

## 5.2 Overall performance

On the observed absolute enrollment, Table 4 summarizes performance on the retrospective sets, with persistence alongside each metric and the *p*-value of the difference.

**Table 4.** Overall performance on observed absolute enrollment. The first two rows correspond to the 2026 origin; the third, to the 2025 origin.

| Set | n | R² | R² pers. | WAPE | WAPE pers. | Skill | *p* sq. | *p* abs. | RelMAE | Bias |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Retrospective OOF 2019–2026 | 73,462 | 0.9617 | 0.9616 | 14.38% | 14.88% | +0.09% | 0.9758 | 0.0992 | 0.9662 | +2.23% |
| Holdout 2026 (blind) | 9,069 | 0.9710 | 0.9666 | 12.27% | 13.09% | +13.21% | 0.1006 | 0.0049 | 0.9372 | +0.74% |
| Holdout 2025 (blind), 2025 origin | 9,041 | 0.9782 | 0.9717 | 12.35% | 13.23% | +22.87% | 0.0569 | 0.0052 | 0.9333 | −0.29% |

*Note:* pers. = persistence. RelMAE = MAE of the model divided by the MAE of persistence on the same set (Section 4.8 and note 1). *p* = *p*-value of the Diebold–Mariano test between cells with institution-cluster standard errors (Section 4.8), with squared and absolute loss. In the OOF, the tests group the 113 rows repeated within their cell into N8 (73,349 groups), which gives that calculation a skill of +0.20% instead of the per-row +0.09%, and they use as clusters the 60 institutions of the period. The OOF contains 113 surplus rows in 88 cells that inherit their cell's total (Section 6.5).

![**Figure 1.** Forecast versus observed enrollment by cell. Left: retrospective out-of-fold (OOF) predictions 2019–2026 (n = 73,462). Right: blind holdout 2026 (n = 9,069), 2026 origin. The dashed line is the identity. Observed enrollment.](<figuras_en/fig02_scatter_pred_vs_real.png>)

Three readings. First, **the R² of the model and that of persistence are nearly glued together** (0.9617 versus 0.9616 in the OOF): the high R² is produced by the inertia of enrollment, not by the model (Figure 1). Second, **the skill of the full OOF is practically null (+0.09%)**, owing to the early years (Section 5.3). Third, **the 2026 holdout is harder than the 2025 holdout**: the model beats persistence in WAPE (12.27% versus 13.09%) and in RelMAE (0.937), but its skill drops from +22.87% to +13.21%, because persistence improved and the squared error is concentrated in a few large institutions whose total the model overestimated. The advantage is significant with absolute loss (*p* = 0.0049) but not with squared loss (*p* = 0.1006). In the 2019–2026 OOF, by contrast, the difference versus persistence is not significant at any level with either loss (the lowest *p*-value is 0.0992, with absolute loss in N8); in the 2025 holdout from the 2025 origin it is significant with absolute loss in N5–N8 (*p* ≤ 0.031) and not with squared loss (*p* between 0.057 and 0.189) (Appendix A.17). The advantage over persistence is therefore concentrated in the years with a long history and in the 2025 and 2026 evaluations.

**Two 2026 figures that must not be confused.** The 2026 holdout of the 2026 origin (skill +13.21%, 9,069 cells) and the 2026 validation of the 2025 origin (+26.71%, 8,729 cells; Section 5.4) measure the same year with different instruments—the former with the 2026 exogenous variables and new cells; the latter with exogenous variables frozen at 2025—: neither corrects the other, and the recent evidence is a single year.

## 5.3 Performance by year

Each OOF year $Y$ is predicted with a model fitted only on the preceding years, so the training volume grows monotonically (Table 5, Figure 2).

**Table 5.** Annual performance of the retrospective OOF predictions (2026 origin), against observed enrollment. Observed and Forecast are totals over the modeled cells; the aggregate error is forecast minus observed, as a percentage of the observed value.

| Year | n | R² | WAPE | WAPE pers. | Skill | Observed | Forecast | Aggregate error |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 9,424 | 0.9499 | 14.36% | 14.30% | −34.89% | 654,495 | 677,096 | +3.45% |
| 2020 | 9,321 | 0.9359 | 14.69% | 15.74% | −13.71% | 637,998 | 666,925 | +4.53% |
| 2021 | 9,230 | 0.9625 | 15.50% | 17.08% | +19.99% | 669,403 | 654,899 | −2.17% |
| 2022 | 9,161 | 0.9527 | 16.31% | 16.35% | −2.98% | 662,479 | 700,931 | +5.80% |
| 2023 | 9,038 | 0.9584 | 16.20% | 15.64% | −8.97% | 670,918 | 702,750 | +4.74% |
| 2024 | 9,176 | 0.9725 | 13.63% | 13.96% | +3.68% | 692,653 | 700,168 | +1.09% |
| 2025 | 9,043 | 0.9777 | 12.45% | 13.23% | +21.08% | 711,941 | 712,759 | +0.11% |
| 2026 | 9,069 | 0.9710 | 12.27% | 13.09% | +13.21% | 741,615 | 747,102 | +0.74% |

![**Figure 2.** RMSE (enrollments per cell), R² and WAPE by year in the retrospective OOF predictions 2019–2026 (2026 origin). Shaded bands mark the years that the empirical detection classified as level shocks (2020 and 2022). Observed enrollment.](<figuras_en/fig03_metricas_por_anio.png>)

**The model has negative skill in four of the eight retrospective years**: in 2019 it is trained on a single previous year and is much worse than persistence, and skill is positive in the last three years, with six to eight years of history, which is the regime in which the forecast operates. There is also **systematic overprediction in the early years**—from +3.45% to +5.80% between 2019 and 2023, except 2021—which falls to +1.09% in 2024, +0.11% in 2025 and +0.74% in 2026 (Figure 3). Performance in use resembles that of the last years, and intervals calibrated on the full OOF are conservative (Section 5.7). The 2019 to 2025 figures differ slightly from those of the 2025 origin (Appendix A.9).

![**Figure 3.** Total undergraduate university enrollment over the modeled cells: observed enrollment 2018–2026 (SIES; 653,163 in 2018), retrospective OOF prediction with its annual aggregate error (in percent) and *ex ante* 2027 forecast from the main model of the 2026 origin (761,058 enrollments). The bands mark the level-shock years.](<figuras_en/fig08_backtesting_temporal_MONEY_FIGURE.png>)

## 5.4 Out-of-sample validation against official 2026 enrollment

This result measures the 2025-origin model, whose 2026 forecast was generated on 13 August 2026, after the official release of 10 July, with the training window closed in 2025 and the status declared in Section 5.1.

**Universe coverage.** The model only forecasts programs that existed in 2025 with at least ten enrolled students: of the 759,045 undergraduate university enrollments of 2026, it matches 721,747 (95.09%) in 8,729 cells; left out are 37,298 enrollments in new programs or programs that crossed the threshold, and the model forecasts 5,611 enrollments in 312 cells of discontinued programs. The gap with the official total is mostly one of coverage, and what is excluded grows faster than what is covered.

**Table 6.** Aggregation cascade on official 2026 enrollment (2025 origin, 8,729 matched cells). Each level adds the indicated dimension to the previous one.

| Level | n groups | WAPE | WAPE pers. | Skill | *p* sq. | *p* abs. | RelMAE | ±10% | ±10% pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N1 National | 1 | 0.01% | 2.32% | +99.99% | — | — | 0.006 | 100% | 100% |
| N2 + Institution | 53 | 2.31% | 3.26% | +48.46% | 0.3151 | 0.1697 | 0.708 | 92.5% | 92.5% |
| N3 + Field | 408 | 3.74% | 4.76% | +48.93% | 0.0530 | 0.0137 | 0.786 | 82.4% | 77.9% |
| N4 + Region | 649 | 4.16% | 5.02% | +37.52% | 0.0496 | 0.0137 | 0.829 | 76.4% | 73.2% |
| N5 + Program | 2,668 | 7.59% | 8.48% | +24.54% | 0.0378 | 0.0103 | 0.895 | 58.4% | 57.0% |
| N6 + Student status | 4,633 | 9.42% | 10.47% | +25.59% | 0.0205 | 0.0004 | 0.900 | 50.9% | 49.1% |
| N7 + Gender | 8,094 | 10.93% | 11.97% | +22.82% | 0.0470 | 0.0002 | 0.914 | 44.6% | 42.3% |
| N8 + Attendance mode (cell) | 8,729 | 11.49% | 12.69% | +26.71% | 0.0363 | < 0.0001 | 0.906 | 43.3% | 40.9% |

*Note:* aggregates are obtained by summing the cell forecasts (bottom-up). *p* = Diebold–Mariano between groups with cluster-robust standard errors by institution cluster (53 clusters), squared and absolute loss; at N1 it is not applicable (one group).

**Skill is positive and RelMAE is below one at all eight levels**, and the advantage over persistence is significant at the 5% level in N4–N8 with squared loss and in N3–N8 with absolute loss; at N2 it is not. There is no crossover: there is no aggregation level at which it would be preferable to use persistence instead of the model. The preliminary version had negative skill at the four finest levels (Table 3).

**The 2026 holdout of the 2026 origin.** Table 7 reports the same cascade for the 2026 holdout, against observed enrollment.

**Table 7.** Aggregation cascade on the 2026 holdout (2026 origin, 9,069 cells), against observed enrollment.

| Level | n groups | WAPE | WAPE pers. | Skill | *p* sq. | *p* abs. | RelMAE | ±10% | ±10% pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N1 National | 1 | 0.74% | 2.77% | +92.85% | — | — | 0.2674 | 100.00% | 100.00% |
| N2 + Institution | 53 | 2.76% | 3.64% | +49.51% | 0.3414 | 0.2605 | 0.7578 | 88.68% | 92.45% |
| N3 + Field | 413 | 4.44% | 5.04% | +37.42% | 0.2311 | 0.2219 | 0.8799 | 80.15% | 76.76% |
| N4 + Region | 647 | 4.78% | 5.30% | +24.45% | 0.3947 | 0.2307 | 0.9018 | 75.58% | 73.42% |
| N5 + Program | 2,739 | 8.42% | 8.81% | +7.86% | 0.3866 | 0.1944 | 0.9549 | 57.21% | 56.26% |
| N6 + Student status | 4,798 | 10.22% | 10.83% | +10.40% | 0.2506 | 0.0329 | 0.9443 | 49.33% | 48.02% |
| N7 + Gender | 8,390 | 11.71% | 12.31% | +4.47% | 0.6259 | 0.0206 | 0.9517 | 42.59% | 41.81% |
| N8 + Attendance mode (cell) | 9,069 | 12.27% | 13.09% | +13.21% | 0.1006 | 0.0049 | 0.9372 | 41.59% | 40.56% |

*Note:* as in Table 6.

The holdout skill is lower than that of the 2025-origin validation at all levels except N2, and its advantage over persistence is significant only with absolute loss at N6–N8; with squared loss it is not significant at any level. At N2, the percentage of institutions within ±10% falls below that of persistence (88.68% versus 92.45%), even though the model's institutional WAPE is lower; the institutional total falls within ±5% for 40 of 53 institutions and within ±10% for 47. Both cascades agree on the usefulness frontier (Figure 4): up to institution × field × region, about three out of four groups fall within ±10%; once the program is added, just over half.

![**Figure 4.** WAPE (left) and R² (right) by aggregation level, from N1 (national total) to N8 (fine cell), in the retrospective OOF predictions 2019–2026 and on the 2026 holdout of the 2026 origin. The national-level R² in the OOF is computed on eight annual observations. Observed enrollment.](<figuras_en/fig06_evolucion_metricas_por_nivel.png>)

**The aggregate.** Forecast growth for the covered cells was **+2.26%** and observed growth **+2.27%**, a difference of 0.014 percentage points. The full system, without the model's filters, grew by 3.69%, from 732,034 to 759,045 enrollments; the difference between the two figures is the growth of what is not covered.

**Where it fails.** Distance education is the clear case: the model assigned it more than double the observed growth. The model is useful for projecting an institution or a faculty, not for anticipating which program will grow: only 43.3% of cells fall within ±10%; the correlation between the observed and the forecast rate is 0.365, the forecast dispersion is less than half of the observed one, and the direction of change is correct in 60% of cells. **The practical usefulness frontier lies between N4 and N5.**

**Worst cells.** At the 2026 origin, of the 50 worst cells by absolute error, 49 in the 2019–2025 OOF and all 50 of the 2026 holdout have a fine-level lag; the fallbacks account for 1.1% of enrollment and have higher relative error, but they do not explain the tail of the distribution, which is made up of genuine program contractions (Appendix A.4, Table A.6).

**By institution** (Appendix A.24), the total fell within ±5% for 40 of 53 institutions and within ±10% for 49, and the model beat persistence in internal WAPE for 42. Errors pull toward the center: the forecast was above the observed value in all 14 institutions that declined—although it anticipated the decline in 10—and of the 20 for which it anticipated a decline, only 10 declined; **the model is not useful as an early warning of institutional contraction**.

## 5.5 Comparison with per-series benchmarks and with a simple global model

Table 8 compares, at four levels of the cascade, the main model with persistence, with the five per-series methods, and with the lags-only global model (Section 4.7).

**Table 8.** WAPE by method and level on the 2026 holdout (2026 origin, observed enrollment) and on the validation against the official 2026 data (2025 origin; for the methods other than C49, 2026-origin models applied to the 8,729 cells of that validation).

| Method | Holdout N1 | N2 | N5 | N8 | Validation 2026 N1 | N2 | N5 | N8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Persistence | 2.77% | 3.64% | 8.81% | 13.09% | 2.32% | 3.26% | 8.48% | 12.69% |
| RWD | 0.85% | 2.85% | 8.69% | 13.27% | 1.25% | 2.78% | 8.38% | 12.89% |
| ETS | 2.54% | 3.76% | 10.31% | 14.46% | 2.00% | 3.47% | 10.06% | 14.13% |
| ARIMA | 1.96% | 3.91% | 11.28% | 15.69% | 1.25% | 3.57% | 11.08% | 15.43% |
| Theta | 1.46% | 3.39% | 9.67% | 13.86% | 0.92% | 3.11% | 9.41% | 13.49% |
| Comb | 1.99% | 3.61% | 10.03% | 14.08% | 1.39% | 3.29% | 9.77% | 13.73% |
| Lags-only global model (Lrez) | 0.80% | 2.65% | 7.98% | 11.60% | 0.79% | 2.36% | 7.64% | 11.16% |
| CatBoost, 49 variables (C49) | 0.74% | 2.76% | 8.42% | 12.27% | 0.01% | 2.31% | 7.59% | 11.49% |

*Note:* RWD = random walk with drift; Comb = mean of ETS, ARIMA and Theta. Aggregates are obtained by bottom-up summation from the cell. The full tables, with skill, RelMAE and percentage within ±10% at N1–N8 and in the 2019–2025 OOF, are in Appendix A.16.

**At the cell level, the global models outperform persistence, and persistence outperforms the per-series methods.** At N8, all five per-series methods have higher WAPE than persistence in both 2026 sets and in the 2019–2025 OOF (Appendix A.16); the skill of ETS at N8 of the holdout is −9.05% and that of ARIMA, −42.00%. On the 2026 holdout, the lags-only global model has lower WAPE than C49 at N5 and N8, with significant differences with absolute loss at N5–N8 (N8: DM = +4.77, *p* < 0.0001) but not with squared loss (N8: *p* = 0.0539); at N2–N4 they are not distinguishable. In the 2026 validation, the difference at N8 is significant only with absolute loss (*p* = 0.0255). The multiple comparison ranks the global model first at N8 in both sets (Appendix A.17).

**At the national total, the per-series methods are competitive.** In the 2019–2025 OOF, ARIMA (WAPE 1.29%), Comb (1.48%), Theta (1.56%) and ETS (1.71%) outperform persistence (1.87%) and the boosting models at N1, whose early-year overprediction bias dominates the aggregate (CatBoost 3.08%; global 3.10%). With the @harvey1997 correction over the eight years of the 2019–2026 OOF, the advantage over persistence is significant for Comb (*p* = 0.0142) and ARIMA (*p* = 0.0374) with squared loss, and not for ETS, Theta, the drift, the global model or CatBoost (Appendix A.17).

## 5.6 Factorial algorithm × feature design

**Table 9.** WAPE of the factorial design and Diebold–Mariano comparisons between groups (statistic and *p*-value, standard error clustered by institution) of the model with exogenous variables versus the lags-only model, for each algorithm. Observed enrollment.

| Set | Level | C49 | Crez | L49 | Lrez | C49 − Crez, sq. | C49 − Crez, abs. | L49 − Lrez, sq. | L49 − Lrez, abs. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF 2019–2025 | N2 | 4.69% | 5.28% | 4.55% | 4.92% | −3.13 (0.0027) | −3.70 (0.0005) | −2.18 (0.0332) | −2.50 (0.0151) |
| OOF 2019–2025 | N8 | 14.71% | 14.78% | 14.62% | 14.27% | −2.40 (0.0195) | −0.83 (0.4093) | +0.81 (0.4228) | +4.22 (< 0.0001) |
| Holdout 2026 | N2 | 2.76% | 2.67% | 2.46% | 2.65% | −0.20 (0.8393) | +0.26 (0.7931) | −1.09 (0.2796) | −0.60 (0.5531) |
| Holdout 2026 | N8 | 12.27% | 11.31% | 12.14% | 11.60% | +2.23 (0.0300) | +5.99 (< 0.0001) | +0.94 (0.3495) | +4.65 (< 0.0001) |
| Validation 2026 (8,329 cells) | N2 | 2.77% | 2.54% | 2.45% | 2.33% | +0.19 (0.8482) | +0.73 (0.4683) | −0.74 (0.4610) | +0.44 (0.6626) |
| Validation 2026 (8,329 cells) | N8 | 11.77% | 10.73% | 11.63% | 11.01% | +2.20 (0.0325) | +5.92 (< 0.0001) | +0.96 (0.3425) | +4.47 (< 0.0001) |

*Note:* C49 = CatBoost with 49 variables; Crez = CatBoost lags-only; L49 = LightGBM with 49 variables; Lrez = LightGBM lags-only. A positive DM statistic favors the lags-only model; a negative one, the 49-variable model. In the 2026 validation, all four models are from the 2026 origin applied to the 2025 lag (Section 4.7). Cross-validation RMSE on the arcsinh scale: C49 0.2949; Crez 0.2948; L49 0.2952; Lrez 0.2869. N5 results and comparisons between algorithms are in Appendix A.22.

The contribution of the exogenous variables **depends on the period and the level**. In 2026 — the same year in the holdout and in the validation — a lags-only global model matches or outperforms the 49-variable model at the cell level with both algorithms: with CatBoost, the WAPE at N8 falls from 12.27% to 11.31% without exogenous variables in the holdout (squared DM *p* = 0.0300; absolute *p* < 0.0001), and with LightGBM, from 12.14% to 11.60% (significant only with absolute loss); at N2 there are no significant differences. In the 2019–2025 OOF, by contrast, the 49 variables improve the aggregates: at N2, with CatBoost (*p* = 0.0027 with squared loss) and with LightGBM (*p* = 0.0332); with CatBoost also at N5 and N8 with squared loss, whereas at N8 with absolute loss the lags-only LightGBM is better. The algorithm is not neutral either: in 2026 the best model at the cell level is the lags-only CatBoost, and in the OOF, the lags-only LightGBM. The year-by-year breakdown of the OOF is consistent with the exogenous variables compensating for the lack of lag history (Appendix A.22): at N8, the C49 − Crez WAPE difference is −1.77 points in 2019, with one year of history, −0.48 in 2020 and −0.92 in 2022, and positive from 2023 onward (+1.29, +0.43 and +0.76 in 2023–2025, and +0.96 in 2026); with LightGBM, L49 − Lrez is −0.74 in 2019 and positive from 2022 onward. The correlation of the difference with years of history (2019–2025, n = 7) is 0.79 with both algorithms at N8, and 0.63 and 0.48 at N2. **The advantage of the exogenous variables is concentrated in the years with little history and in the 2022 shock; with five years of history or more it does not improve the cell level.** With seven years there is no power to separate it from year-to-year variation. This comparison is hypothesis H2 of the prospective 2027 protocol (Section 5.10).

## 5.7 Prediction intervals

Table 10 reports the empirical coverage of the 90% conformal intervals by cell.

**Table 10.** Empirical coverage of the 90% conformal intervals by cell.

| Origin | Set | Calibration | n | Coverage | Median width (enrollments) |
|---|---|---|---:|---:|---:|
| 2025 | Holdout 2025 | OOF 2019–2024 | 9,041 | 91.54% | 36.3 |
| 2025 | Validation 2026 (official data) | OOF 2019–2024 | 8,729 | 92.53% | 37.3 |
| 2026 | Holdout 2026 | OOF 2019–2025, winsorized-rate residuals | 9,069 | 92.26% | 36.5 |
| 2026 | Holdout 2026 | OOF 2019–2025, observed residuals | 9,069 | 92.49% | 36.6 |
| 2026 (Crez) | Holdout 2026 | OOF 2019–2025, observed residuals | 9,069 | 93.25% | 36.4 |
| 2026 (L49) | Holdout 2026 | OOF 2019–2025, observed residuals | 9,069 | 92.25% | 37.1 |
| 2026 (Lrez) | Holdout 2026 | OOF 2019–2025, observed residuals | 9,069 | 92.31% | 36.1 |

*Note:* coverage is measured against observed enrollment, except in the 2025 holdout, measured as in the original evaluation. The winsorized-rate-residuals row corresponds to the previously published calibration; the observed-residuals rows are the ones frozen with the 2027 forecasts of each model.

Coverage exceeds the target in all sets: **the intervals are conservative**, because the calibration includes the early years with overprediction. A median width of 37.3 enrollments for a median cell of 44 is honest, but not very informative for an individual program (details by level in Appendix A.11). The national total carries no conformal interval, because there is one observation per year; at the 2025 origin an indicative **non-conformal** range of 681,899 to 742,062 was reported around the point forecast of 727,260.

**Calibration and sharpness.** Table 11 compares the stratified bands with an unstratified conformal predictor and with the 90% AutoETS intervals on the 2026 holdout.

**Table 11.** Coverage, median width, mean interval score (IS), and MSIS of the 90% bands on the 2026 holdout (2026 origin), against observed enrollment, over the groups with all three bands available.

| Level | Band | Coverage | Median width | Mean IS | MSIS |
|---|---|---:|---:|---:|---:|
| N2 + Institution | Stratified conformal | 94.34% | 2,282.9 | 3,178.1 | 6.2410 |
| N2 + Institution | Unstratified conformal | 96.23% | 4,095.7 | 5,567.6 | 10.9335 |
| N2 + Institution | AutoETS 90% | 94.34% | 2,244.1 | 3,592.3 | 7.0544 |
| N5 + Program | Stratified conformal | 93.72% | 102.9 | 166.7 | 7.1447 |
| N5 + Program | Unstratified conformal | 95.27% | 169.0 | 266.5 | 11.4252 |
| N5 + Program | AutoETS 90% | 89.45% | 92.4 | 179.3 | 7.6881 |
| N8 + Attendance mode (cell) | Stratified conformal | 93.86% | 37.8 | 65.3 | 6.1554 |
| N8 + Attendance mode (cell) | Unstratified conformal | 95.10% | 48.4 | 96.0 | 9.0523 |
| N8 + Attendance mode (cell) | AutoETS 90% | 86.99% | 34.4 | 71.5 | 6.7455 |

*Note:* MSIS = mean IS divided by the MAE of persistence on the same groups. The comparison excludes groups with fewer than three years of contiguous history for ETS, so coverage differs from that of Table 10. N3, N4, N6 and N7 in Appendix A.19.

The stratified bands obtain a lower IS and MSIS than the unstratified conformal predictor at all levels N2–N8, because they are much narrower with coverage still above 90%. Compared with AutoETS, whose bands are narrower but undercover from N4 onward (86.99% at the cell), the stratified bands have lower IS at all levels except N7, where they are practically tied (IS 79.8 versus 79.7; MSIS 7.2482 versus 7.2427). Mondrian stratification is therefore what makes conformal intervals useful in a panel this heteroskedastic.

## 5.8 Bias of the precomputed target encoding

Table 12 isolates the leakage of the target encoding with a four-arm experiment — $m$-estimator or sigmoid weighting, fitted on the whole panel or within each fold — with the same CatBoost, the same hyperparameters and the same seven folds (2026 origin).

**Table 12.** Cross-validation RMSE on the arcsinh scale by encoder and fitting method (2026 origin).

| Encoder | With leakage (whole panel) | Within fold | Difference | Relative difference |
|---|---:|---:|---:|---:|
| $m$-estimator ($m = 30$) | 0.2852 | 0.2938 | −0.0086 | −2.92% |
| Sigmoid weighting | 0.2838 | 0.2949 | −0.0110 | −3.74% |
| Previously published comparison: $m$ with leakage versus sigmoid within fold | 0.2852 | 0.2949 | −0.0096 | −3.26% |

*Note:* the within-fold sigmoid arm reproduces the RMSE of the main model (0.2949). The experiment was not repeated for the 2025 origin, where the non-isolated comparison gave 3.5%. The precomputed columns with the panel's built-in $m$-estimator were calculated before removing 13,235 exact duplicate rows, so they weight the repeated rows twice; no published figure depends on them, and the $m$ arm of this table recomputes them.

With the same encoder in both arms, the isolated leakage makes cross-validation report an RMSE between 2.92% and 3.74% better than the actual one. The distance between the three boosting candidates after optimization (0.5%) and between the four cells of the factorial design in cross-validation (from 0.2869 to 0.2952) is smaller than that bias, so a single error of this kind can reverse the apparent ranking of the models [@kaufman2012; @kapoor2023leakage].

## 5.9 Regional heterogeneity and explainability

**Region.** Regional heterogeneity is moderate and is largely ordered by the number of observations: in the 2019–2026 OOF, the WAPE ranges from 11.99% in Los Ríos to 25.50% in Aysén, the region with the fewest programs (313 observations), and the Región Metropolitana (Santiago Metropolitan Region) lies in an intermediate range (14.78%). The model's WAPE is lower than that of persistence in 14 of the 16 regions, but the skill is negative in 6 (Appendix A.9, Figure A.1).

**Explainability.** The analysis of SHAP values [@lundberg2017shap], computed with the exact algorithm for trees [@lundberg2020treeshap] on the 92,036 rows exported by the 2026 origin — retrospective, lag-base and forecast rows — ranks the five most influential variables (mean absolute value) as follows: encoded program name (0.0533), first-year student status (0.0488), lagged enrollment (0.0364), evening attendance mode (0.0299) and the cell's lagged share of the program's regional enrollment (0.0229). The order of the top five does not change between origins (Appendix A.10).

The stable finding is that **first-year status competes with the lag in importance**. The dynamics of first-year students depend on admissions and those of continuing students on retention, which are different processes. The evening attendance mode in fourth place is consistent with Section 5.4: the non-daytime modes are the ones that move differently and where the model errs most.

**Attributions are not predictive contribution.** That exogenous variables appear among the most influential in the main model does not imply that they improve the forecast: in 2026, the same algorithm without exogenous variables is equal or better at the cell level (Section 5.6). SHAP contributions describe how the model uses its variables, not how much each would contribute to out-of-sample accuracy.

## 5.10 2027 forecasts (*ex ante*, frozen before the data)

The universe is the 9,069 cells of 53 institutions with programs active in 2026 and at least ten enrolled students, not comparable with the official SIES total. We froze the four models of the factorial design and two benchmarks (Table 13).

**Table 13.** Frozen 2027 forecasts, with their growth over the 2026 observed enrollment in the same cells (741,615).

| ID | Model | Total 2027 | Growth |
|---|---|---:|---:|
| C49 | CatBoost, 49 variables (main model) | 761,058 | +2.62% |
| Crez | CatBoost, lags only | 767,934 | +3.55% |
| L49 | LightGBM, 49 variables | 760,672 | +2.57% |
| Lrez | LightGBM, lags only (global model) | 768,499 | +3.63% |
| F0 | Persistence | 741,615 | +0.00% |
| FN | National Comb (average of ETS, ARIMA and Theta on the national series; N1 only) | 746,696 | +0.69% |

*Note:* C49 was frozen unchanged because its total had already been published. It uses as the lag for 75 cells the value reconstructed with the winsorized rate (740,318 in total, versus 741,615 observed); its growth over that base would be +2.80%. The other models use the observed 2026 enrollment as the lag.

**Composition.** The two models with exogenous variables forecast less growth than the two without exogenous variables, with both algorithms (around +2.6% versus +3.6%), and the difference lies mainly in first-year students: −0.54% with C49 and −0.07% with L49, versus +1.82% with Crez and +2.93% with Lrez. All four foresee increases of 10.71% to 14.56% in the distance-education mode, which in 2026 the 2025-origin model overestimated (Section 5.4), and declines of 4.72% to 7.66% in the evening mode (Appendix A.23). By institution, C49 foresees a decline in 15 of the 53 based on the 2026 observed database.

**Uncertainty.** The 90% bands of each model are calibrated with the stratified conformal predictor on its 2019–2026 OOF residuals against observed enrollment; those of C49 were recalibrated this way without touching its point forecast. Calibrated with 2019–2025 OOF, they cover on the 2026 holdout between 92.25% and 93.25% of the cells (Table 10), and the median band by institution measures 20.62% of the forecast with C49, 25.16% with Crez, 20.74% with L49 and 23.21% with Lrez. The national total of C49 carries an indicative **non-conformal** range of 719,308 to 777,914, built with the observed OOF aggregate errors of −2.17% (2021) to +5.80% (2022).

**Against simple benchmarks.** C49 lies 0.8 and 1.6 points below the average 2024–2026 change (+3.40%) and the 2026 change (+4.17%), computed on the observed aggregate series; the 2018–2026 linear trend (730,266; −1.53%) is a weak benchmark, because 2026 lay above the long-term trend (Figure 5).

![**Figure 5.** Aggregate 2027 growth over 2026 observed enrollment in the modeled cells: main model forecast (C49, 2026 origin; +2.62%) versus three simple benchmarks computed on the observed aggregate series: 2018–2026 linear regression (−1.53%), average of the 2024–2026 changes (+3.40%) and 2026 change (+4.17%).](<figuras_en/fig09_forecast_2027_vs_baselines.png>)

**Status and protocol.** The forecasts are *ex ante*. The six forecasts were frozen on 20 November 2026, before the official release of 2027 enrollment, by means of an annotated tag in a public repository with the SHA-256 digests of the predictions, the evaluation protocol and the evaluation script \[identifiers omitted for double-blind review; provided to the editor in the cover letter\]. The deposit with a DOI will be reported in the accepted version. \[PENDING: Zenodo DOI\] The protocol (Appendix A.14) fixes the data (first SIES release, without winsorization or adjustment), the matching, the metrics and five hypotheses tested with Diebold–Mariano between groups by institution cluster, with **absolute primary loss**: whether all four models beat persistence (H1); whether the exogenous variables add value, C49 − Crez and L49 − Lrez at N8 and N2 (H2), with a reading fixed in advance and a concrete comparison, because the models with exogenous variables forecast around +2.6% and those without around +3.6%; whether the algorithm matters (H3); the error of the national total (H4); and the calibration of the bands (H5). A model **fails** if its RelMAE at N8 is greater than or equal to one. The bands are classified, by model and level and with the Wilson interval, with an asymmetric criterion: undercoverage if coverage is below 88%, calibrated between 88% and 95% and conservative above 95%. The criterion was fixed after a dry run of the evaluation program on 2026 and before the freeze; in that dry run, the bands of all four models were calibrated at N8 (C49 92.49%, Crez 93.25%, L49 92.25%, Lrez 92.31%). No result is reinterpreted or modifies the frozen forecasts [@reich2019; @cramer2022; @tetlock2014].

**Assumptions.** The 2027 exogenous variables are frozen at their last observed value, which for GDP and unemployment is that of 2025 (Section 3.4); if the 2027 data depart from the forecast of the models with exogenous variables, the first revision will be that carry-forward.

# 6. Discussion

## 6.1 R² on levels does not discriminate

The most transferable result of this work is not a performance figure but a measurement warning. On the 2026 holdout, the model attains an R² of 0.9710 and persistence one of 0.9666 (on the 2025 holdout of the 2025 origin, 0.9782 and 0.9717). A study reporting the former without the latter would convey that its model explains 97% of the variance, when the model's own contribution over inertia is less than one point. This is a property of any enrollment series with multi-year programs, and the same logic that led meteorology to evaluate against persistence [@murphy1988; @mittermaier2008] applies here with particular force.

**Recommendation:** no R² on enrollment levels should be published without that of persistence alongside. The informative metrics in this domain are the skill score, the relative error (RelMAE) and the percentage of groups within a declared band, all expressed relative to persistence.

## 6.2 Rate and level

There is a large gap between performance on the growth rate—R² of the order of 0.10 on the arcsinh scale in the validation folds— and on the level—R² of 0.98—. It is the same inertia seen from the other side: almost all of the level is predictable and almost none of the marginal growth is. For planning, the relevant metric is that of the level, because the level is what is budgeted. But the implication must be made explicit: a model with an R² of 0.98 on levels can have very little ability to anticipate *changes*, and both statements are simultaneously true. The shrinkage toward the mean observed at the cell level (Section 5.4) is the manifestation of that low predictability of change.

## 6.3 When the naïve forecast is the lag

The persistence forecast and the model's inertia variable are the same column. When that column has a construction defect, the skill score is contaminated in the numerator and the denominator at once, and the bias **has no predictable direction**: here, the same defect inflated the skill of the 2025 holdout to +77.4% and sank it to −8.0% in 2026, which erroneously suggested that the model's margin had evaporated. The failure mode is invisible to the usual diagnostics—learning curves, residuals, variable importance—and it relates to data leakage [@kaufman2012; @kapoor2023leakage] without being the same thing: there is no information from the future in training, but rather an error in the variable that defines at once the main predictor and the benchmark. Checklists warn against weak benchmarks [@hewamalage2023]; this case shows that a benchmark that is *correct in its definition* can be incorrectly *constructed*.

**Recommendations** for any work reporting skill relative to persistence on lagged data: (1) audit the lag key as the target is audited, publishing the matching rate by fallback level; (2) monitor the distribution of the lag—a lag-to-cell ratio with a median of 8× is detectable before training; (3) treat large jumps in skill between periods as suspicion about the instrument; (4) verify that the numerator and denominator of a rate share the key; and (5) publish forecasts fixed before the data and compare them against it: out-of-sample evaluation also audits the pipeline.

## 6.4 What the model contributes

The evidence separates a robust result from a period-dependent one. **The robust result** is that, with persistence correctly constructed, global models—CatBoost and LightGBM, with or without exogenous variables—have lower WAPE than persistence at the cell level, and persistence in turn has lower WAPE than per-series methods, in the 2019–2025 OOF and in the two 2026 evaluations (Sections 5.5 and 5.6). The advantage of the main model over persistence, however, is not significant in the full 2019–2026 OOF with any loss, and is significant in the 2025 and 2026 evaluations with absolute loss (Section 5.2): it is concentrated in the years with long history. This is the lesson of recent competitions and of global-model theory [@makridakis2022m5acc; @januschowski2022trees; @monteromanso2021]. At the national total, by contrast, per-series methods on the aggregate series are competitive and, with the low power of eight years, Comb and ARIMA beat persistence significantly, whereas the cell-level models do not: for the system aggregate it is worth keeping a per-series benchmark alongside the model [@makridakis2020m4].

**The period-dependent result** is the contribution of the exogenous variables. In 2026, a lags-only global model matches or outperforms the 49-variable one at the cell level with both algorithms; in the 2019–2025 OOF, the 49 variables improve the aggregates, particularly the institutional level. The recent evidence is a single year, and it does not allow us to claim either that the exogenous variables add nothing or that the accuracy comes only from the global design. The year-by-year breakdown of the OOF is compatible with one explanation: the exogenous variables help when the lag history is short—in 2019 the model is trained on a single year—and during the 2022 shock, and stop improving the cell once there are five or more years of history (Section 5.6). If that were so, the 2026 result would be what to expect going forward; but with seven years there is no power to separate that pattern from year-to-year variation, and hypothesis H2 of the 2027 protocol will subject it to a prospective test with the reading fixed in advance. The choice of algorithm is likewise not neutral, and depends on the evaluated set.

## 6.5 Limitations

**Null extrapolative component.** Trees do not extrapolate in the year, and the exogenous variables are frozen at their last value: **the forecast is, in essence, a learned transformation of the lag**. For the 2026 national total, carrying forward the previous year's growth came within −0.08% of the observed value: the model's value relative to aggregate rules lies in disaggregation (Section 5.5).

**Variables with information from the evaluated year (closed ablation).** Three variables use the aggregated enrollment of year $t$. Retrained without them (variant i) or with all exogenous variables at $t-1$ (variant ii), with the same hyperparameters, seed and folds, the WAPE of the 2026 holdout at the cell level is 12.27% with variant i and rises to 12.33% with variant ii (+0.06 points), versus 12.27% for the published model; the optimism attributable to contemporaneous information is small (Appendix A.18).

**A single year of recent testing.** The 2026 holdout and the validation of the 2025 origin measure the same year; the 2027 comparison adds the second. The hyperparameters chosen in cross-validation are reused in the OOF, whose early figures are indicative, and the holdout year enters the statistics of the shock detector and the winsorization percentiles of the target.

**Data quality.** An earlier version of the evaluation used the value reconstructed with the clipped rate; the correction does not change the sign of any conclusion, and some secondary figures in the appendix are labeled as computed with that value. In the OOF there are 113 surplus rows in 88 cells, from two institutions (2019–2021 and 2024), arising from several campuses within the same region or curriculum versions, that inherit the cell total; the 2026 holdout and the 2027 forecasts are not affected, and without them the WAPE of C49 at the cell level in the 2019–2025 OOF moves from 14.71% to 14.70% and its skill from −1.86% to −2.06%; this will be corrected in the next methodological version. \[PENDING: author confirmation to include this note\] Because of an order-of-operations defect in the consolidation, the repair of the Ñuble region name was not applied, and the institutional joins of academic staff, infrastructure and tuition fees for that region were affected; the correction has been identified and will be evaluated in the next version; its effect on the error has not been measured. Of the rows, 70.9% have some imputed variable, and the 2026 GDP and unemployment were carried forward from 2025.

**Reconciliation and shock detection.** Bottom-up summation is the best reconciliation at N1–N5, and MinT with shrinkage does not improve the N4/N5 frontier, although with weak ETS base forecasts (Appendix A.21). Shock detection holds up as a reproducible criterion, not as a typology: two of its three categories remain empty and its classification is sensitive to preprocessing.

**Scope and use.** The work covers only universities (about 759 thousand of the system's 1,372,167 undergraduate enrollments), and within them 95.09% of enrollment; what is excluded is what grows the most. The SHAP contributions are associations, not causal effects, and the model is a tool for **aggregate planning**, not for decisions about individual applicants.

## 6.6 Future directions

The first priority is the prospective evaluation of 2027 under the frozen protocol; improvements will be evaluated in a separate line, with their own forecast fixed in advance. In order of expected return: (i) exploit the cohort structure through the accounting identity $\text{Continuing}_t \approx \text{retention} \times (\text{Continuing}_{t-1} + \text{FirstYear}_{t-1})$, which would give the model a dynamic component of its own; (ii) check whether the contribution of the exogenous variables depends on the length of the lag history (Section 6.4); (iii) match the comparison with the official data by code rather than by name, which recovers 31 cells and 3,987 enrollments and moves the WAPE from 11.49% to 11.24%; (iv) incorporate official projections of the exogenous variables, in particular the demographic one, instead of freezing them; (v) give the attendance mode its own dynamics through an interaction between attendance mode and year; (vi) partial pooling for small regions [@athanasopoulos2024review]; (vii) extend the analysis to technical training centers and professional institutes; and (viii) recalibrate the intervals on a window that excludes the biased early years.

# 7. Conclusions

In a series as inertial as enrollment, the persistence forecast is the correct benchmark and, at the same time, the easiest to measure badly, because it coincides with the lag variable that feeds the model: a defect in the matching key contaminated, in this case, the model and the benchmark at the same time, inflated the skill in one year and sank it the next, and was detected only because a forecast issued before the data could be compared with it.

With persistence correctly constructed, global gradient boosting models have lower error than persistence at the cell level, and persistence has lower error than the per-series methods, although the advantage over persistence is only significant in the years with long history (2025 and 2026) and not in the full OOF: on the official 2026 data, the main model reduced the WAPE from 12.69% to 11.49% (skill +26.71%, significant with both losses at the cell level) and the lags-only global model reached 11.16%, while ETS, ARIMA and Theta by series were worse than persistence; at the national total, by contrast, the per-series methods are competitive. The contribution of the exogenous variables depends on the period: it does not improve the cell in 2026, but it does improve the aggregates in 2019–2025, with an advantage concentrated in the years with little history and in the 2022 shock. The stratified conformal intervals covered 92.53% of the cells in the 2026 validation and 92.49% in the 2026 holdout, with a lower interval score than its alternatives at almost all levels, and the isolated leakage of a precomputed target encoding (2.92% to 3.74% of the RMSE) exceeds the differences between algorithms.

The models are useful for projecting institutions, faculties and the university aggregate—alongside a per-series benchmark for the total—and **not** for individual programs or as an early warning of institutional contraction. The 2027 forecasts from the factorial design and from the benchmarks were frozen with a protocol that fixes in advance what will count as success and what as failure; the July 2027 comparison will tell whether the 2026 result on the exogenous variables is repeated.


# Data and code availability {-}

All primary sources are publicly accessible and are cited as datasets in Table 1 and in the reference list [@sies2025matricula; @cned2026indices; @cned2026infraestructura; @bcch2026pibregional; @ine2026ene; @mineduc2025empleabilidad]. With the 20 November 2026 freeze (Section 5.10), the prediction files for the 2027 forecasts of the four models in the factorial design (9,069 cells, with 90% bands) and of the benchmarks (persistence and national Comb), the evaluation protocol, the program that runs it and their SHA-256 digests were published before the official data. The consolidated panel, the full pipeline code (ingestion, consolidation, construction of the lag key, modeling, evaluation and intervals) and the retrospective predictions will be deposited in a repository with a persistent identifier (DOI), for example Zenodo, upon acceptance. During review, these materials will be available on request to the editor and for the journal's reproducibility check. To preserve anonymity, this manuscript includes no links to repositories or public dashboards associated with the work. \[PENDING: Zenodo DOI\]

# Declaration of generative AI and AI-assisted technologies in the writing process {-}

\[PENDING: the author must complete this declaration in accordance with Elsevier's policy, indicating which tool was used, for what purpose and at which stages. Neutral draft for review:\] During the preparation of this work the author used [tool] in order to [restructure the text according to the journal's format, revise the wording and verify bibliographic references]. After using this tool, the author reviewed and edited the content as needed and takes full responsibility for the content of the publication.

# Funding {-}

\[PENDING: confirm.\] This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Declaration of competing interest {-}

The author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# References {-}

::: {#refs}
:::

