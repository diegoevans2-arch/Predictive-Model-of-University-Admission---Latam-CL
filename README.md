<div align="center">

# 🎓 Predicción de la dinámica de matrícula universitaria en Chile

### Un marco replicable de _machine learning_ con integración multifuente, validación temporal y tratamiento empírico del shock pandémico

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success?style=flat-square)](#)
[![CatBoost](https://img.shields.io/badge/Model-CatBoost-FFCC00?style=flat-square)](https://catboost.ai)
[![Optuna](https://img.shields.io/badge/Tuning-Optuna-2DBCE0?style=flat-square)](https://optuna.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)
[![SHAP](https://img.shields.io/badge/Explainability-SHAP-FF0080?style=flat-square)](https://shap.readthedocs.io)
[![Reproducible](https://img.shields.io/badge/Reproducible-100%25-brightgreen?style=flat-square)](#-cómo-replicar)

</div>

---

> **TL;DR** — Marco completo de predicción de matrícula universitaria chilena a granularidad fina (institución × carrera × región × jornada × género × condición × año), integrando 10 fuentes oficiales. El modelo alcanza **R² = 0.936** y **WAPE = 15.2%** sobre el holdout 2025 a granularidad fina, **mejorando un 77.4% sobre el baseline naïve** y escalando a **99.98% de confianza** al agregar a nivel nacional (apenas 163 estudiantes de error sobre ~707.000). Incluye método automatizado de detección de shocks pandémicos y cuantificación empírica del sesgo introducido por _target encoding_ mal aplicado.

---

## 📑 Tabla de contenidos

- [Resumen ejecutivo](#-resumen-ejecutivo)
- [Resultados destacados](#-resultados-destacados)
- [Arquitectura del pipeline](#-arquitectura-del-pipeline)
- [Fuentes de datos](#-fuentes-de-datos)
- [Pipeline de procesamiento](#-pipeline-de-procesamiento)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Cómo replicar](#-cómo-replicar)
- [Hallazgos metodológicos](#-hallazgos-metodológicos)
- [Limitaciones](#%EF%B8%8F-limitaciones)
- [¿Y los IP y CFT? La próxima frontera](#-y-los-ip-y-cft-la-próxima-frontera)
- [Citar este trabajo](#-citar-este-trabajo)
- [Autor](#-autor)
- [Licencia](#-licencia)

---

## 📊 Resumen ejecutivo

### Qué hace este proyecto

Predice cuántos estudiantes se matricularán en cada combinación específica de **institución × carrera × región × jornada × género × condición** del sistema universitario chileno, para los años 2019-2026. Genera tanto **predicciones retrospectivas validadas** (2019-2025) como un **forecast a futuro (2026)**.

### Para quién es útil

- 🏛️ **Autoridades de política pública**: proyecciones nacionales con **99.98% de confianza** para planificación de subsidios, dimensionamiento del Sistema Único de Admisión, y evaluación de sostenibilidad del Crédito con Aval del Estado (CAE).
- 🎓 **Universidades**: anticipación de matrícula institucional con ~97% de confianza, y por carrera específica con ~90% de confianza, útil para asignación de presupuesto docente, dimensionamiento de infraestructura y planificación de retención.
- 🔬 **Investigadores en ML aplicado a educación**: marco metodológico replicable con evidencia empírica sobre target encoding fold-aware, validación temporal estricta, y tratamiento documentado del shock pandémico.

### Pregunta de investigación

¿Es posible construir un modelo predictivo de matrícula universitaria chilena que mantenga utilidad a granularidad fina (programa específico) sin sacrificar precisión a nivel agregado (sistema nacional)?

**Respuesta: sí.** El modelo alcanza simultáneamente:
- **85% de confianza** a granularidad fina (65.439 combinaciones únicas)
- **99.98% de confianza** agregando al nivel nacional anual (apenas 163 estudiantes de error sobre 706.844 reales)

---

## 🎯 Resultados destacados

### Métricas globales del modelo (CatBoost optimizado con Optuna, 50 trials)

| Conjunto | n filas | RMSE | MAE | R² | WAPE (%) | Confianza (%) | **Skill vs naïve** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **OOF retrospectivo (2019-2025)** | 65.967 | 35.82 | 12.99 | **0.887** | 18.32 | 81.68 | **+71.22%** |
| **Holdout 2025** | 9.179 | 29.90 | 11.67 | **0.936** | 15.16 | 84.84 | **+77.39%** ⭐ |

> 💡 **Lo que destaca del modelo:** el skill score de **+77.4%** sobre el baseline naïve es excepcional. La literatura típica de forecasting considera "buenos" skill scores entre +10% y +30%. Un valor sobre +75% indica que el modelo está capturando dinámicas estructurales del sistema universitario que una proyección de inercia simple es incapaz de anticipar.

### Precisión por nivel de agregación (Holdout 2025)

| Nivel | n grupos | WAPE (%) | Confianza (%) | R² |
|---|---:|---:|---:|---:|
| Nacional anual | 1 | **0.02** | **99.98** ⭐ | n/a |
| + Institución | 55 | 2.79 | 97.21 | 0.998 |
| + Área conocimiento | 418 | 5.20 | 94.80 | 0.994 |
| + Región | 688 | 6.09 | 93.91 | 0.990 |
| + Carrera | 2.770 | 10.09 | 89.91 | 0.968 |
| + Condición | 4.829 | 12.44 | 87.56 | 0.959 |
| + Género | 8.446 | 14.38 | 85.62 | 0.943 |
| + Jornada (granularidad fina) | 9.072 | 15.05 | 84.95 | 0.938 |

### 🎨 Visualizaciones clave

<div align="center">

**Backtesting temporal: histórico observado vs predicción OOF retrospectiva + forecast 2026**

![Backtesting temporal](Documents/OUTPUTS_PAPER/figuras/fig08_backtesting_temporal_MONEY_FIGURE.png)

**Evolución de la precisión del modelo al cambiar la granularidad de agregación**

![Macro a micro](Documents/OUTPUTS_PAPER/figuras/fig06_evolucion_metricas_por_nivel.png)

**Predicciones vs valores reales en holdout 2025**

![Scatter](Documents/OUTPUTS_PAPER/figuras/fig02_scatter_pred_vs_real.png)

</div>

### Forecast 2026

> 🔮 **707.960 estudiantes** proyectados a nivel universitario nacional para 2026 (+0.16% sobre 2025).
>
> El crecimiento modesto es **consistente con la realidad estructural del sistema**: con más datos y dummies pandémicas, el modelo aprendió que los crecimientos de 2023-2024 fueron parcialmente un rebote post-pandémico que se está desacelerando. La proyección refleja, además, una tendencia estructural más profunda: la pérdida sostenida de participación universitaria en el sistema chileno de educación superior frente al subsector técnico-profesional (ver sección [¿Y los IP y CFT?](#-y-los-ip-y-cft-la-próxima-frontera)).

---

## 🏗️ Arquitectura del pipeline

```mermaid
flowchart TB
    subgraph FUENTES["📥 1. Fuentes oficiales públicas (10)"]
        direction LR
        F1["📚 SIES<br/>Matrículas"]
        F2["🎓 CNED<br/>BaseINDICES"]
        F3["👥 CNED<br/>Cuerpo Docente"]
        F4["🏢 CNED<br/>Inmuebles"]
        F5["💰 Banco Central<br/>PIB regional"]
        F6["📉 INE<br/>Desempleo"]
        F7["💼 mifuturo.cl<br/>Empleabilidad"]
        F8["🗺️ CNED<br/>Dicc. sede-región"]
        F9["🏛️ SIES<br/>Dicc. instituciones"]
        F10["📋 SIES<br/>Dicc. carreras"]
    end

    subgraph ETL["⚙️ 2. ETL por fuente (8 pipelines independientes)"]
        direction LR
        E1["etl_sies_matriculas<br/>(75K filas base)"]
        E2["etl_aranceles_puntajes<br/>(valores + selectividad)"]
        E3["etl_cuerpo_docente<br/>(ratios por grado)"]
        E4["etl_inmuebles<br/>(M² e infraestructura)"]
        E5["etl_pib_regional<br/>(log1p)"]
        E6["etl_tasa_desempleo<br/>(anual regional)"]
        E7["etl_empleabilidad<br/>(retención 1° año)"]
        E8["etl_sede_region<br/>(380 sedes)"]
    end

    subgraph CONSOLIDADO["🔗 3. Consolidación y feature engineering"]
        direction TB
        M1["Normalización de llaves<br/>(año + región + institución + carrera)"]
        M2["Merge secuencial multi-tabla"]
        M3["Imputación jerárquica<br/>(5 capas, 69.8% en capa de alta calidad)"]
        M4["Feature engineering<br/>(30 variables derivadas:<br/>lags, ratios, OHE, TE)"]
        M5["dataset_modelado_final.csv<br/>75.622 × 51"]
        M1 --> M2 --> M3 --> M4 --> M5
    end

    subgraph MODELADO["🤖 4. Modelado predictivo"]
        direction TB
        P1["Detección de shocks pandémicos<br/>(Z-score + variación agregada)"]
        P2["Validación temporal estricta<br/>(expanding window CV)"]
        P3["Target Encoding fold-aware"]
        P4["Baselines informados (B0-B3)"]
        P5["Optimización Optuna<br/>(LightGBM | XGBoost | CatBoost)"]
        P6["Modelo ganador: CatBoost<br/>R² = 0.936  ·  Skill +77.4%"]
        P7["Predicciones OOF retrospectivas<br/>+ Forecast 2026"]
        P1 --> P2 --> P3 --> P4 --> P5 --> P6 --> P7
    end

    subgraph ANALISIS["📈 5. Análisis post-hoc para el paper"]
        direction TB
        A1["Métricas globales<br/>(RMSE, MAE, R², WAPE)"]
        A2["Análisis macro → micro<br/>(8 niveles de agregación)"]
        A3["Backtesting temporal"]
        A4["Análisis de calibración<br/>y errores extremos"]
        A5["Explicabilidad SHAP<br/>(global + por subgrupo)"]
        A6["Validación forecast 2026<br/>vs baselines simples"]
    end

    F1 --> E1
    F2 --> E2
    F3 --> E3
    F4 --> E4
    F5 --> E5
    F6 --> E6
    F7 --> E7
    F8 --> E8
    F9 -.->|llave canónica| M1
    F10 -.->|llave canónica| M1

    E1 --> M1
    E2 --> M1
    E3 --> M1
    E4 --> M1
    E5 --> M1
    E6 --> M1
    E7 --> M1
    E8 --> M1

    M5 --> P1
    P7 --> A1
    P7 --> A2
    P7 --> A3
    P7 --> A4
    P7 --> A5
    P7 --> A6

    style FUENTES fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style ETL fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style CONSOLIDADO fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style MODELADO fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style ANALISIS fill:#fce4ec,stroke:#c2185b,stroke-width:2px
```

---

## 📂 Fuentes de datos

Todas las fuentes son **públicas y oficiales**. Pueden descargarse directamente desde los organismos correspondientes:

| Fuente | Organismo | Variables aportadas | Período | URL oficial |
|---|---|---|---|---|
| **Base de matrículas SIES** | MINEDUC | Matrícula por institución × carrera × jornada × género × condición × año | 2018-2025 | [mifuturo.cl/bases-de-datos](https://www.mifuturo.cl/bases-de-datos-de-matriculados/) |
| **BaseINDICES CNED** | CNED | Aranceles, vacantes, puntajes de admisión, duración de carreras | 2005-2025 | [cned.cl/indices](https://www.cned.cl/bases-de-datos) |
| **Cuerpo Docente CNED** | CNED | Número de docentes por grado académico y jornada | 2018-2025 | [cned.cl/indices](https://www.cned.cl/bases-de-datos) |
| **Inmuebles e infraestructura CNED** | CNED | M² construidos, salas, oficinas por sede | 2018-2025 | [cned.cl/indices](https://www.cned.cl/bases-de-datos) |
| **PIB regional** | Banco Central de Chile | PIB regional anual a precios corrientes (MM$) | 2018-2025 | [bcentral.cl](https://www.bcentral.cl/web/banco-central/areas/estadisticas) |
| **Tasa de desocupación regional** | INE (SIMEL) | Tasa de desempleo anual por región y sexo | 2018-2025 | [ine.gob.cl](https://www.ine.gob.cl/) |
| **Buscador de Empleabilidad e Ingresos** | mifuturo.cl | Retención de primer año, empleabilidad por carrera-institución | 2018-2025 | [mifuturo.cl](https://www.mifuturo.cl/) |
| **Diccionario sede-región CNED** | CNED | Mapeo de códigos de sede a códigos INE de región (380 sedes) | Estático | CNED |
| **Diccionario de instituciones** | SIES | Catálogo canónico de 222 instituciones | Estático | MINEDUC |
| **Diccionario de carreras** | SIES | Catálogo canónico de 15.940 nombres de carrera | Estático | MINEDUC |

> ⚠️ **Nota sobre las bases de datos**: el repositorio NO incluye las bases originales ni el consolidado intermedio. Las fuentes son todas públicas y descargables desde los organismos. El procedimiento completo para reconstruir el dataset está documentado en el código.

---

## 🔧 Pipeline de procesamiento

### 1️⃣ Ingesta y ETL por fuente

Se desarrollaron **8 pipelines independientes** (uno por fuente o grupo de fuentes), cada uno responsable de:

- **Carga** con codificación `utf-8-sig` y separadores chilenos (`;` y `,`).
- **Validación de integridad**: nulos, duplicados, rangos esperados, cardinalidad.
- **Normalización**: nombres de regiones contra diccionario canónico, códigos institucionales contra SIES, nombres de carrera contra BBDD canónica.
- **Transformación específica**: agregación a la granularidad apropiada, cálculo de ratios estructurales, manejo de excepciones por fuente.
- **Export** en formato CSV chileno (`sep=';'`, `decimal=','`).

### 2️⃣ Consolidación

El consolidado final integra las 8 fuentes mediante **merge secuencial** sobre llaves comunes:

- **Llave maestra**: `año + región + institución`
- **Llave secundaria**: `año + región + institución + carrera + jornada + género + condición`

Tras el merge, se aplica un **sistema de imputación jerárquica de 5 capas** que respeta la lógica de granularidad:

| Capa | Aplica a | Llave de agrupación | % imputado |
|---|---|---|---:|
| 1 — Temporal | Docente + Inmuebles | (institución, región) → interpolación lineal sobre año + ffill/bfill | 4.2% |
| 2 — Jerárquica | Aranceles + Retención | (institución, carrera) → (institución, área, año) → (área, año) | **69.8%** |
| 2.5 — Región+carrera | Aranceles + Retención | (región, carrera, año) → (carrera, año) → (carrera) | 0.0% |
| 2.7 — Institución | Aranceles + Retención | (institución, año) → (institución) | 0.0% |
| 3 — Terminal | Ambos | Mediana global | 26.0% |

> 💡 La **concentración de la imputación en la Capa 2 (69.8%)** representa una mejora estructural sustantiva: mientras versiones previas del dataset concentraban el grueso de la imputación en capas terminales (mediana global, baja calidad informativa), la cobertura completa de `area_conocimiento` permite que la lógica jerárquica por área absorba el grueso del trabajo de imputación.

Luego se construyen **30 features derivadas**: lags temporales (`matriculas_lag1`), ratios estructurales (`pct_doctores`, `densidad_competitiva`), indicadores de mercado (`arancel_relativo_regional`, `concentracion_matricula_lag`), one-hot encoding de variables nominales (incluyendo `CLASIFICACIÓN INSTITUCIÓN NIVEL 2/3` y estado de acreditación), y target encoding fold-aware de categóricas de alta cardinalidad.

El resultado es `dataset_modelado_final.csv`: **75.622 filas × 51 columnas**, con 0 nulls y 0 duplicados, cubriendo **62 universidades** y **1.355 carreras únicas**.

### 3️⃣ Modelado predictivo

📓 [`Notebooks/modelado_predictivo_admision_v3.ipynb`](Notebooks/modelado_predictivo_admision_v3.ipynb)

**31 celdas** ejecutables secuencialmente que producen:

- **Detección automatizada de shocks pandémicos** (Criterio Z-score sobre tasas individuales + variación agregada YoY) → identifica **2020 y 2022 como shocks de nivel** sobre el dataset extendido.
- **Validación temporal estricta**: expanding window CV (5 folds: 2020-2024 como validación) + holdout fijo 2025.
- **Target encoding fold-aware** mediante `category_encoders.TargetEncoder` dentro de `sklearn.Pipeline`, garantizando que el encoding se ajuste solo con datos de entrenamiento de cada fold.
- **Baselines informados**: B0 (mediana constante), B1 (histórica por institución-carrera), B2 (Ridge solo lag), B3 (Ridge full).
- **Modelos candidatos**: LightGBM, XGBoost, CatBoost, Random Forest (sanity check).
- **Optimización con Optuna**: 50 trials por modelo, TPESampler + MedianPruner. **CatBoost resulta ganador** con RMSE CV = 0.3111 en escala arcsinh.
- **Experimento empírico TE-leaky vs TE-fold-aware**: cuantifica un sesgo del **3.4% del RMSE** atribuible al uso ingenuo de target encoding precalculado.
- **Predicciones OOF retrospectivas** para 2019-2025 y **forecast 2026**.
- **Export del modelo final** (`joblib`) + metadata completa (`json`) + dataset de predicciones (`parquet` + `csv`).

### 4️⃣ Análisis post-hoc para el paper

📓 [`Notebooks/analisis_paper_resultados.ipynb`](Notebooks/analisis_paper_resultados.ipynb)

**20 celdas** que se ejecutan sobre el parquet de predicciones (no re-entrena nada) y producen:

- **Análisis macro → micro**: métricas en 8 niveles de agregación (de nacional anual a granularidad fina).
- **Análisis temporal**: desempeño año a año con efecto del crecimiento del conjunto de entrenamiento.
- **Backtesting agregado nacional** con bandas de shock pandémico anotadas.
- **Análisis de calibración** por decil de tamaño de matrícula.
- **Validación del forecast 2026** contra 3 baselines simples (regresión lineal, promedio años normales, último año).
- **Análisis de errores extremos** (top 15 mejores y peores predicciones).
- **Explicabilidad SHAP** global, por subgrupo y caso de estudio.
- **12 figuras en 300 dpi** + **9 tablas en Markdown** listas para el paper.

---

## 📁 Estructura del repositorio

```
Predictive-model-of-university-admission/
│
├── 📄 README.md                                    # Este documento
├── 📄 LICENSE                                      # Licencia MIT
├── 📄 .gitattributes
│
├── 📓 Notebooks/
│   ├── modelado_predictivo_admision_v3.ipynb       # Pipeline completo de modelado
│   └── analisis_paper_resultados.ipynb             # Análisis post-hoc para el paper
│
├── 📂 Documents/
│   ├── Predictive model of university admission.pdf            # Paper completo
│   ├── Predictive model of university admission.md             # Paper en Markdown
│   ├── PREDICTING UNIVERSITY ENROLLMENT DYNAMICS IN CHILE_*.pdf # Versión IFE Conference 2027
│   ├── OFICIAL_GLOSARIO_MATRICULA_WEB_E.pdf                    # Glosario oficial SIES
│   ├── BaseINDICES-2005-2025_*.pdf                              # Documentación CNED
│   ├── INDICES_Institucional_2005-2025_*.pdf                    # Documentación CNED
│   │
│   └── OUTPUTS_PAPER/
│       ├── figuras/                # 12 figuras del análisis (PNG 300dpi)
│       │   ├── fig01_distribucion_residuos.png
│       │   ├── fig02_scatter_pred_vs_real.png
│       │   ├── fig03_metricas_por_anio.png
│       │   ├── fig04_wape_por_region.png
│       │   ├── fig05_macro_a_micro.png
│       │   ├── fig06_evolucion_metricas_por_nivel.png
│       │   ├── fig07_calibracion.png
│       │   ├── fig08_backtesting_temporal_MONEY_FIGURE.png
│       │   ├── fig09_validacion_forecast_2026.png
│       │   ├── fig10_shap_top5_distribucion.png
│       │   ├── fig11_shap_por_subgrupo.png
│       │   └── fig12_caso_estudio_shap.png
│       │
│       └── tablas/                 # 9 tablas en formato Markdown
│           ├── tabla_resumen_paper.md
│           ├── tabla_macro_a_micro_OOF.md
│           ├── tabla_macro_a_micro_HOLDOUT.md
│           ├── tabla_metricas_por_anio.md
│           ├── tabla_metricas_por_region.md
│           ├── tabla_backtesting_anual.md
│           ├── tabla_shap_top5_resumen.md
│           ├── tabla_top15_mejores_predicciones.md
│           └── tabla_top15_peores_predicciones.md
│
└── 📂 BBDD/                        # Carpeta destinada a las bases originales
                                    # (NO se publican; debe poblarse manualmente
                                    # con las descargas oficiales)
```

---

## 🔄 Cómo replicar

### Requisitos

- **Python 3.11+**
- **Jupyter Notebook 7.x** o JupyterLab
- **Sistema operativo**: probado en Windows con locale español. Compatible con Linux/macOS ajustando rutas.
- **Hardware recomendado**: 16 GB RAM, CPU multi-núcleo (la optimización con Optuna paraleliza fits de modelos).

### Instalación

Recomendamos crear un entorno aislado:

```bash
# Con conda
conda create -n matricula python=3.11 -y
conda activate matricula

# Instalar dependencias
pip install numpy==1.26.4 pandas==2.2.0 scipy==1.13.1 scikit-learn==1.5.0 \
            lightgbm==4.5.0 xgboost==2.1.1 catboost==1.2.5 \
            optuna==4.0.0 shap==0.45.1 category_encoders==3.0.1 \
            joblib==1.4.2 seaborn==0.13.0 matplotlib==3.8.4 \
            nbformat==5.10.4 pyarrow==17.0.0
```

### Replicación paso a paso

#### Paso 1 — Obtener las bases originales

Descarga manualmente cada fuente desde el organismo oficial (URLs en la sección [Fuentes de datos](#-fuentes-de-datos)) y deposita los archivos en la carpeta `BBDD/`.

#### Paso 2 — Ejecutar el modelado predictivo

```bash
cd Notebooks
jupyter notebook modelado_predictivo_admision_v3.ipynb
```

Ejecuta las **31 celdas secuencialmente** (`Cell → Run All`). El notebook detecta automáticamente el dataset y produce:

- `OUTPUTS_MODELADO/predicciones_modelo_final_{timestamp}.parquet`
- `OUTPUTS_MODELADO/predicciones_modelo_final_{timestamp}.csv`
- `OUTPUTS_MODELADO/modelo_final_{timestamp}.joblib`
- `OUTPUTS_MODELADO/metadata_modelo_{timestamp}.json`

**Tiempos esperados:**
- Setup + EDA + baselines: ~5-10 min
- Optimización con Optuna (3 modelos × 50 trials): ~45-60 min
- Evaluación + SHAP + export: ~10 min
- **Total: ~60-80 min**

#### Paso 3 — Ejecutar el análisis post-hoc para el paper

```bash
jupyter notebook analisis_paper_resultados.ipynb
```

Ejecuta las **20 celdas** secuencialmente. Detecta automáticamente el parquet más reciente y produce:

- `OUTPUTS_PAPER/figuras/` — 12 figuras en 300 dpi
- `OUTPUTS_PAPER/tablas/` — 9 tablas en Markdown
- `OUTPUTS_PAPER/metricas_completas_paper.json` — trazabilidad completa

**Tiempo esperado: 2-5 min** (no re-entrena modelos, solo análisis sobre el parquet).

---

## 🔬 Hallazgos metodológicos

### 1. Target encoding fold-aware vs precalculado

Cuantificamos empíricamente que **un target encoding precalculado sobre todo el dataset infla el RMSE aparente en 3.4%** frente a su implementación correcta dentro del pipeline de cross-validation. Esta diferencia es considerablemente mayor a lo reportado típicamente en literatura aplicada (~1-2%) debido a la muy alta cardinalidad de `NOMBRE CARRERA` (1.355 categorías). En comparaciones entre modelos donde el primer y segundo lugar suelen diferir en 1-3% de RMSE, **un único error metodológico de TE puede invertir el ranking aparente** y conducir a conclusiones erróneas.

### 2. Detección automatizada de shocks pandémicos

Proponemos un método basado en dos criterios complementarios sobre la distribución del target:

- **Criterio 1**: Z-score sobre media y desviación estándar de las tasas individuales (umbral 95%).
- **Criterio 2**: Variación interanual del total agregado de matrículas.

Aplicado al caso chileno con el dataset extendido, identifica **automáticamente**:
- **2020** → shock de nivel (caída estructural por COVID-19)
- **2022** → shock de nivel (recaída tras rebote parcial de 2021)

Este aporte rompe con el tratamiento monolítico ("años COVID") que predomina en la literatura aplicada y, con más datos, converge a una caracterización **parsimoniosa** de los shocks: solo identifica años verdaderamente anómalos.

### 3. La precisión crece monotónicamente con la agregación

Documentamos cómo **el error porcentual ponderado (WAPE) disminuye sistemáticamente al agregar**, pasando de 15.05% a granularidad fina (institución × carrera × región × jornada × género × condición × año) a 0.02% a nivel nacional anual. Esto tiene una implicación práctica directa: **el modelo es ideal para planificación a nivel sistema y útil con cautela para predicciones programa-específicas**, dada la varianza idiosincrática irreducible a esa granularidad.

### 4. La distinción entre tasa y nivel

Reportar métricas únicamente sobre tasas de crecimiento (R² ≈ 0.22 en escala arcsinh) puede subestimar significativamente la utilidad práctica de los modelos. **La métrica que importa para planificación es el número absoluto de matrículas predichas**, donde el modelo alcanza R² = 0.936.

### 5. Skill score sobre baseline naïve: +77.4%

El modelo mejora en **77.4%** el RMSE cuadrado respecto al baseline naïve (predecir matrícula igual al año anterior). Este nivel de skill score es excepcional en la literatura de forecasting aplicado, donde valores entre +10% y +30% ya se consideran buenos. Refleja que el modelo está capturando dinámicas estructurales del sistema universitario que la inercia simple no anticipa.

---

## ⚠️ Limitaciones

- **Cobertura del universo**: solo universidades (**62 instituciones, ~707.000 estudiantes**). Centros de Formación Técnica (CFT) e Institutos Profesionales (IP) quedan fuera del alcance actual — esto se aborda en detalle en la próxima sección.
- **Heterogeneidad regional**: el desempeño es marcadamente menor en regiones con pocas observaciones (Aysén, Atacama, Magallanes).
- **Forecast 2026 bajo supuestos**: asume estabilidad de variables macroeconómicas (PIB regional, desempleo) al nivel 2025.
- **Naturaleza descriptiva, no causal**: las contribuciones SHAP identifican asociaciones, no relaciones causales.
- **Imputación masiva en variables terminales**: el 26% de las celdas imputadas se resolvieron con mediana global; el modelo conoce este hecho vía la flag `fue_imputado`.

---

## 🚀 ¿Y los IP y CFT? La próxima frontera

> Este trabajo cubre **exclusivamente universidades**. Pero el sistema de educación superior chileno es bicéfalo: universidades, Institutos Profesionales (IP) y Centros de Formación Técnica (CFT). Los IP y CFT —DUOC UC, INACAP, AIEP, entre los más visibles— concentran aproximadamente el **45% de la matrícula de pregrado del país**, y están **creciendo más rápido que las universidades**.

### El fenómeno: las universidades pierden participación de forma sostenida

| Año | Matrícula total nacional | Matrícula universitaria | **% universitario** | Crecimiento universitario YoY |
|---:|---:|---:|---:|---:|
| 2018 | 1.188.045 | 678.213 | **57.09** | — |
| 2019 | 1.194.459 | 677.084 | **56.69** | −0.17% |
| 2020 | 1.151.834 | 660.109 | **57.31** | −2.51% |
| 2021 | 1.204.376 | 691.375 | **57.41** | +4.74% |
| 2022 | 1.214.011 | 685.435 | **56.46** | −0.86% |
| 2023 | 1.249.419 | 693.662 | **55.52** | +1.20% |
| 2024 | 1.277.611 | 706.040 | **55.26** | +1.78% |
| 2025 | 1.327.344 | 731.981 | **55.15** | +3.67% |

**La participación universitaria cayó casi 2 puntos porcentuales en 7 años** (57.09% → 55.15%). En el mismo período:
- Matrícula universitaria creció **7.9% acumulado**
- Matrícula IP/CFT creció **~17% acumulado**

### ¿Qué nos dice esto sobre el forecast 2026 universitario?

El modelo proyecta un crecimiento universitario de **+0.16%** para 2026, sustantivamente por debajo de los baselines basados en años post-pandémicos (+2.15% a +2.41%). Esta moderación es **coherente con la dinámica estructural**: con más datos y dummies pandémicas, el modelo aprendió que los crecimientos de 2023-2024 fueron parcialmente un rebote post-pandémico que se está desacelerando, en un contexto donde el subsistema universitario está perdiendo participación frente al técnico-profesional.

### La próxima pregunta de investigación

**¿Es posible replicar este marco predictivo en el universo completo de IP y CFT chilenos?**

Esta es la **dirección futura prioritaria** del programa de investigación. Una extensión natural implicaría:

| Componente | Estado |
|---|---|
| 🔁 **Replicar la metodología de ETL multifuente** sobre el dataset SIES filtrado a IP/CFT | _Pendiente_ |
| 🔁 **Detectar shocks pandémicos específicos** del subsector técnico-profesional (las dinámicas COVID podrían haber sido distintas) | _Pendiente_ |
| 🔁 **Validar si el patrón macro→micro se mantiene** en un universo con cardinalidades distintas (menos instituciones grandes, más programas técnicos especializados) | _Pendiente_ |
| 🔁 **Construir un forecast integrado del sistema completo** para 2026, combinando el modelo universitario actual con uno para IP/CFT | _Pendiente_ |
| 🔁 **Cuantificar la migración estudiantil estructural** entre subsectores con métodos causales (difference-in-differences, variables instrumentales) | _Pendiente_ |

> 💡 **Si te interesa colaborar en esta extensión**, el código y la metodología están abiertos. Las fuentes oficiales contienen tanto universidades como IP/CFT — basta con ajustar los filtros del ETL y reaplicar el pipeline. El marco propuesto en este trabajo es **agnóstico al subsector** y debería transferirse de forma directa.

### Otras direcciones futuras

1. **Modelado jerárquico bayesiano** para mejorar el desempeño en regiones con pocas observaciones (Aysén, Atacama).
2. **Análisis de sensibilidad explícita** del forecast a supuestos macroeconómicos (PIB, desempleo).
3. **Integración de variables idiosincráticas no observadas**: datos de admisión institucional, campañas de marketing, satisfacción estudiantil.
4. **Aplicación Streamlit**: visualización interactiva del histórico observado, predicciones OOF retrospectivas y forecast 2026 a la granularidad que cada usuario requiera.
5. **Aplicación a planificación CAE/Gratuidad**: utilizar las predicciones agregadas con su 99.98% de confianza nacional para dimensionar el presupuesto anual de los instrumentos de financiamiento estudiantil.

---

## 📚 Citar este trabajo

Si utilizas este código, los hallazgos metodológicos o las predicciones generadas, por favor cita este trabajo:

### BibTeX

```bibtex
@article{evans2026matricula,
  title  = {Predicción de la dinámica de matrícula universitaria en Chile mediante 
            machine learning: un marco replicable con integración multifuente, 
            validación temporal y tratamiento empírico del shock pandémico},
  author = {Pérez Paz, Diego Evans},
  year   = {2026},
  month  = {6},
  note   = {Disponible en \url{https://github.com/diegoevans2-arch/Predictive-model-of-university-admission}}
}
```

### APA 7

> Pérez Paz, D. E. (2026). *Predicción de la dinámica de matrícula universitaria en Chile mediante machine learning: un marco replicable con integración multifuente, validación temporal y tratamiento empírico del shock pandémico*. https://github.com/diegoevans2-arch/Predictive-model-of-university-admission

---

## 👤 Autor

**Diego Evans Pérez Paz**

[![GitHub](https://img.shields.io/badge/GitHub-diegoevans2--arch-181717?style=flat-square&logo=github)](https://github.com/diegoevans2-arch)

Para consultas sobre el código, replicación o colaboración académica, abre un [issue](https://github.com/diegoevans2-arch/Predictive-model-of-university-admission/issues) en el repositorio.

---

## 📜 Licencia

Este proyecto se distribuye bajo licencia [MIT](LICENSE). El código puede ser utilizado, modificado y distribuido libremente, incluyendo uso comercial, siempre que se preserve el aviso de copyright original.

Las **fuentes de datos** son propiedad de sus respectivos organismos públicos (MINEDUC, CNED, INE, Banco Central de Chile, mifuturo.cl) y se rigen por sus propios términos de uso.

---

<div align="center">

**¿Te resultó útil este trabajo?** ⭐ Considera darle una estrella al repositorio.

_Construido con 🐍 Python, ❤️ rigor metodológico, y ☕ mucho café._

</div>
