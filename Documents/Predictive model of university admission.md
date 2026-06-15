# Predicción de la dinámica de matrícula universitaria en Chile mediante machine learning: un marco replicable con integración multifuente, validación temporal y tratamiento empírico del shock pandémico

**Autor:** Diego Evans Pérez Paz

**Correspondencia:** diego.perezp@example.cl

**Fecha:** Junio de 2026

---

## Resumen

La predicción de matrícula universitaria es un insumo crítico para la planificación institucional y la formulación de política pública en sistemas de educación superior. Sin embargo, la mayoría de los estudios existentes en América Latina trabaja con datos agregados a nivel nacional, utiliza modelos econométricos clásicos sin validación temporal estricta, o reporta métricas inflacionadas por particiones aleatorias que filtran información del futuro al entrenamiento. Este trabajo propone un marco replicable de *machine learning* para forecasting de matrícula universitaria a granularidad fina (institución × carrera × región × jornada × género × condición × año), integrando diez fuentes oficiales del ecosistema de educación superior chileno (SIES, CNED, INE, Banco Central, mifuturo.cl). Se construye un dataset consolidado de 63.165 observaciones para el período 2018-2025, sobre el cual se aplica un pipeline con validación temporal estricta (expanding window cross-validation) y *target encoding* implementado correctamente dentro de los folds para evitar leakage. Se evalúan tres modelos de *gradient boosting* (LightGBM, XGBoost, CatBoost) optimizados con Optuna, junto con cuatro baselines informados. El modelo ganador (CatBoost) alcanza R² = 0.944 y un error porcentual ponderado (WAPE) de 15.0% sobre el holdout 2025 a granularidad fina, mejorando un 49.5% sobre el baseline naïve. La precisión agregada nacional anual alcanza 99.4% de confianza. Adicionalmente, este trabajo aporta tres contribuciones metodológicas: (i) cuantificación empírica del sesgo introducido por *target encoding* mal aplicado, que infla artificialmente el desempeño aparente en un 2.0% del RMSE; (ii) un método automatizado de detección de tres tipos de shock pandémico (nivel, dispersión y recaída) basado en pruebas Z y variación agregada anual; (iii) un pronóstico de matrícula nacional para 2026 de 612.578 estudiantes, equivalente a un crecimiento del +2.60% respecto a 2025, consistente con baselines simples basados en años post-pandemia.

**Palabras clave:** matrícula universitaria, *machine learning*, *gradient boosting*, validación temporal, *target encoding*, COVID-19, sistema universitario chileno.

---

## 1. Introducción

La planificación de la educación superior demanda proyecciones precisas de matrícula a múltiples niveles de agregación. A nivel macro, las autoridades de política pública requieren proyecciones nacionales para anticipar demanda de subsidios, evaluar la sostenibilidad del Sistema de Crédito con Aval del Estado (CAE) y planificar la oferta de cupos del Sistema Único de Admisión [@cned2024informe]. A nivel meso, las universidades necesitan proyecciones por carrera y campus para asignar presupuesto docente, dimensionar infraestructura y anticipar necesidades de retención. A nivel micro, los equipos de marketing, admisión y dirección académica requieren información granular para tomar decisiones sobre apertura de cohortes, cierre de programas y campañas de captación.

Sin embargo, predecir matrícula universitaria es difícil por al menos tres razones estructurales. **Primero**, el sistema universitario chileno integra señales de fuentes heterogéneas que rara vez se modelan conjuntamente: estadísticas de matrícula del Servicio de Información de Educación Superior (SIES) del MINEDUC, indicadores institucionales del Consejo Nacional de Educación (CNED), variables socioeconómicas regionales del Instituto Nacional de Estadísticas (INE) y del Banco Central de Chile, métricas de empleabilidad de mifuturo.cl, y datos de acreditación de la Comisión Nacional de Acreditación (CNA). **Segundo**, la matrícula presenta heterogeneidad estructural en múltiples dimensiones simultáneas: institución, carrera, región, jornada (diurna, vespertina, semipresencial), género y condición (alumno nuevo o antiguo). Modelos agregados a nivel nacional o institucional pierden esta heterogeneidad, mientras que modelos a granularidad fina enfrentan ruido idiosincrático elevado. **Tercero**, el período 2020-2022 introdujo una anomalía estructural sin precedentes —la pandemia de COVID-19— que afectó la matrícula de formas diferenciadas en cada año, requiriendo un tratamiento explícito en cualquier modelo predictivo que aspire a generalización futura.

La literatura aplicada de predicción de matrícula en América Latina presenta varias limitaciones recurrentes. La mayoría de los estudios trabaja con datos agregados a nivel nacional o institucional [@gonzalez2019predicciones; @ramirez2021forecasting], perdiendo la heterogeneidad por programa, jornada y región. Cuando se emplea *machine learning*, frecuentemente se usan particiones aleatorias del dataset (random splits), lo cual filtra información del futuro hacia el entrenamiento e infla artificialmente las métricas reportadas [@cerda2018ml]. Asimismo, los efectos pandémicos suelen tratarse o bien ignorando los años afectados, o bien con dummies binarias para "2020" sin justificación cuantitativa de su selección.

Este trabajo se posiciona en este vacío metodológico. Sus contribuciones son cuatro:

**C1.** Un **marco replicable de integración de diez fuentes oficiales chilenas** a granularidad fina (séxtuple: institución × carrera × región × jornada × género × condición × año), produciendo un dataset consolidado de 63.165 observaciones para el período 2018-2025.

**C2.** **Evidencia empírica del sesgo introducido por *target encoding* mal aplicado**: se cuantifica que un *target encoding* precalculado sobre todo el dataset (práctica común pero técnicamente incorrecta) infla el desempeño aparente en 2.0% del RMSE en validación cruzada, frente a un *target encoding* fold-aware implementado dentro del pipeline.

**C3.** Un **método automatizado de detección de shocks pandémicos** basado en dos criterios complementarios: (a) Z-score sobre la media y desviación estándar de las tasas individuales de crecimiento, comparadas contra años no-pandémicos; (b) variación interanual del total agregado de matrículas. Aplicado al caso chileno, el método clasifica 2020 como shock de nivel, 2021 como shock de dispersión y 2022 como shock de recaída.

**C4.** Un **modelo predictivo validado temporalmente** que alcanza R² = 0.944 y WAPE = 15.01% sobre matrícula 2025 a granularidad fina (mejorando 49.5% sobre el baseline naïve), y produce un pronóstico de matrícula nacional para 2026 de 612.578 estudiantes (+2.60% sobre 2025), consistente con baselines simples basados en años post-pandemia.

El resto del paper se organiza así: la sección 2 revisa literatura relevante; la sección 3 describe los datos integrados y el procedimiento ETL; la sección 4 detalla la metodología de modelado, validación temporal, *target encoding* fold-aware y tratamiento empírico del shock pandémico; la sección 5 presenta los resultados experimentales globales, por nivel de agregación, por año, por región y de explicabilidad; la sección 6 discute hallazgos, limitaciones y direcciones futuras; la sección 7 concluye.

---

## 2. Trabajos relacionados

### 2.1 Forecasting de matrícula en educación superior

La literatura internacional de predicción de matrícula universitaria se ha desarrollado principalmente sobre datos agregados a nivel nacional o institucional. En Estados Unidos, los estudios basados en el Integrated Postsecondary Education Data System (IPEDS) tienden a alcanzar R² entre 0.75 y 0.95 en predicciones agregadas a institución-año [@smith2018enrollment]. Sin embargo, estas métricas no son comparables con predicciones a nivel programa-jornada porque la agregación temporal e institucional reduce sustancialmente la varianza idiosincrática.

En América Latina, los estudios disponibles son más escasos y predominantemente descriptivos. @gonzalez2019predicciones aplica modelos econométricos clásicos (ARIMA, regresión lineal múltiple) al sistema universitario chileno agregado a nivel nacional, alcanzando errores porcentuales del 4-8%. @ramirez2021forecasting realiza un ejercicio similar para el sistema mexicano. Ninguno de estos trabajos opera a granularidad fina ni evalúa el desempeño con validación temporal estricta.

### 2.2 Machine learning aplicado a educación superior

El uso de *machine learning* en educación superior latinoamericana ha crecido sostenidamente en la última década, mayoritariamente en problemas de predicción a nivel estudiante individual: deserción [@cerda2018ml], rendimiento académico [@perez2020rendimiento], y duración de estudios [@silva2022duracion]. La predicción a nivel programa-cohorte-año (granularidad agregada pero no nacional) ha recibido considerablemente menos atención, a pesar de su relevancia directa para la planificación.

Entre los métodos modernos de *machine learning* tabular, los algoritmos de *gradient boosting* —LightGBM [@ke2017lightgbm], XGBoost [@chen2016xgboost] y CatBoost [@prokhorenkova2018catboost]— han establecido el estado del arte en problemas predictivos sobre datos estructurados de cardinalidad moderada [@shwartz2022tabular]. Su robustez frente a multicolinealidad, su capacidad para capturar no-linealidades e interacciones, y su tolerancia a valores faltantes los hacen particularmente adecuados para problemas como el aquí abordado.

### 2.3 Target encoding y leakage en machine learning aplicado

El *target encoding* es una técnica estándar para variables categóricas de alta cardinalidad, donde cada categoría se reemplaza por el valor medio del *target* condicional a esa categoría [@micci2001target]. Su correcta aplicación requiere que la codificación se calcule **únicamente con datos de entrenamiento**, sin acceso a las etiquetas del conjunto de validación o test, dentro de cada *fold* del *cross-validation*. La aplicación incorrecta —precalcular el *target encoding* sobre todo el dataset antes de partir— introduce *leakage* y produce métricas optimistas que no se sostienen en producción [@kaggle2019leakage]. A pesar de su criticidad, este error es común en la literatura aplicada, y rara vez se cuantifica empíricamente el sesgo que introduce.

### 2.4 Impacto pandémico en matrícula universitaria

El efecto de la pandemia de COVID-19 sobre la matrícula universitaria está bien documentado a nivel descriptivo. En Chile, el sistema universitario experimentó una caída de aproximadamente 4% en matrícula total entre 2019 y 2020, seguida de un rebote desigual entre 2021 y 2025 [@sies2024informe]. Sin embargo, el tratamiento empírico de este shock en modelos predictivos ha sido inconsistente: algunos estudios excluyen los años afectados, otros incluyen una dummy binaria sin justificación cuantitativa, y la mayoría no documenta la sensibilidad del modelo final a esa decisión.

---

## 3. Datos

### 3.1 Fuentes integradas

Se integraron diez fuentes oficiales del ecosistema chileno de educación superior, cuyas características se resumen en la Tabla 1.

**Tabla 1.** Fuentes de datos integradas

| Fuente | Organismo | Variables aportadas | Período cubierto |
|---|---|---|---|
| Base de matrículas SIES | MINEDUC | Matrícula por institución × carrera × jornada × género × condición × año (tabla principal) | 2018-2025 |
| BaseINDICES CNED | CNED | Aranceles, vacantes, puntajes de admisión, duración de carreras | 2005-2025 |
| Cuerpo Docente CNED | CNED | Número de docentes por grado académico y jornada | 2018-2025 |
| Inmuebles e infraestructura CNED | CNED | M² construidos, salas, oficinas por sede | 2018-2025 |
| PIB regional | Banco Central | PIB regional anual a precios corrientes (millones de pesos) | 2018-2025 |
| Tasa de desocupación regional | INE (SIMEL) | Tasa de desempleo anual por región y sexo | 2018-2025 |
| Buscador de Empleabilidad e Ingresos | mifuturo.cl | Retención de primer año, empleabilidad por carrera-institución | 2018-2025 |
| Diccionario sede-región CNED | CNED | Mapeo de códigos de sede a códigos INE de región (380 sedes) | Estático |
| Diccionario de instituciones | SIES | Catálogo canónico de 220 instituciones | Estático |
| Diccionario de carreras | SIES | Catálogo canónico de 15.940 nombres de carrera | Estático |

### 3.2 Procedimiento ETL

El pipeline de integración comprendió cinco fases secuenciales: (i) **auditoría de compatibilidad** entre fuentes para identificar formatos, codificaciones (UTF-8-SIG con BOM, separadores chilenos `;` y `,`) y granularidades originales; (ii) **normalización de llaves** mediante un diccionario canónico de regiones y diccionarios de instituciones y carreras; (iii) **merge secuencial** sobre las llaves comunes año + región y, cuando aplicable, año + institución + carrera; (iv) **imputación por capas jerárquicas** (descritas en la sección 3.4); (v) **ingeniería de variables**, donde se derivaron 30 *features* adicionales (lags, ratios estructurales, densidades competitivas, *target encoding*, etc.).

El dataset final contiene 63.165 observaciones únicas a granularidad institución × carrera × región × jornada × género × condición × año, para el período 2018-2025. El año 2018 se utiliza exclusivamente como base para el lag de matrícula, sin recibir predicciones del modelo.

### 3.3 Variable de interés (target)

La variable a predecir es la **tasa de crecimiento de matrícula** definida como:

$$ \text{tasa}_t = \frac{\text{matrículas}_t - \text{matrículas}_{t-1}}{\text{matrículas}_{t-1}} $$

Para mejorar las propiedades estadísticas durante el entrenamiento se aplica una transformación arcsinh (seno hiperbólico inverso), que es simétrica, comprime las colas y preserva el signo:

$$ \text{target}_t = \text{arcsinh}(\text{tasa}_t) = \ln\left(\text{tasa}_t + \sqrt{\text{tasa}_t^2 + 1}\right) $$

Las predicciones se transforman de vuelta a la escala original mediante la función seno hiperbólico, $\hat{\text{tasa}} = \sinh(\hat{\text{target}})$, y posteriormente se reconstruye el número absoluto de matrículas predichas:

$$ \widehat{\text{matrículas}}_t = \text{matrículas}_{t-1} \times (1 + \sinh(\hat{\text{target}}_t)) $$

Esta reconstrucción es crucial para el análisis de resultados: aunque el modelo se optimiza sobre la tasa de crecimiento (variable de alta varianza), las métricas de desempeño reportadas se calculan sobre matrículas absolutas (variable de alta inercia), que es la magnitud que importa en las decisiones de planificación.

Antes del entrenamiento, se aplica winsorización al 1% y 99% sobre la tasa de crecimiento original para limitar el efecto de valores atípicos extremos. El target final tiene mediana 0.0, media +0.0012 y desviación estándar 0.346 en escala arcsinh.

### 3.4 Sistema de imputación jerárquica

Las fuentes integradas tienen distintos grados de completitud, por lo que se diseñó un sistema de imputación por capas que respeta la lógica de granularidad. Cada capa imputa únicamente las celdas que la capa anterior dejó vacías:

**Tabla 2.** Sistema de imputación jerárquica

| Capa | Aplica a | Llave de agrupación | Celdas imputadas | % del total |
|---|---|---|---|---|
| 1 - Temporal | Docente + Inmuebles | (institución, región): interpolación lineal sobre año + ffill/bfill | 27.406 | 4.3% |
| 2 - Jerárquica | Aranceles + Retención | (institución, carrera) → (institución, área, año) → (área, año) | 115.404 | 18.1% |
| 2.5 - Región+carrera | Aranceles + Retención | (región, carrera, año) → (carrera, año) → (carrera) | 72.741 | 11.4% |
| 2.7 - Institución | Aranceles + Retención | (cod_institucion, año) → (cod_institucion) | 224.940 | 35.3% |
| 3 - Terminal | Ambos | Mediana global de la variable | 196.575 | 30.9% |

Se generó una *flag* binaria `fue_imputado` por fila para preservar trazabilidad y permitir análisis de sensibilidad. El 69.4% de las filas contiene al menos una variable imputada.

---

## 4. Metodología

### 4.1 Diseño general del pipeline

El pipeline predictivo se estructura en seis fases reproducibles: (i) validación de integridad del dataset; (ii) exploración descriptiva del target y *features*; (iii) detección automática de shocks pandémicos; (iv) definición de feature sets y construcción del pipeline de preprocesamiento; (v) evaluación de baselines y modelos candidatos; (vi) tuning de hiperparámetros del modelo seleccionado.

### 4.2 Estrategia de validación temporal

La estructura temporal del dataset (2019-2025, con 2018 como base de lag) impide el uso de particiones aleatorias, que filtrarían información del futuro al entrenamiento. En su lugar se adopta una estrategia de validación temporal estricta con tres componentes:

- **Holdout final:** el año 2025 se reserva como conjunto de prueba ciego, sin uso en ninguna etapa de selección de modelo o tuning.
- **Cross-validation interno:** se utiliza una estrategia de *expanding window* sobre el conjunto de entrenamiento (2019-2024). El *fold* $k$ entrena con los años $\{2019, \ldots, 2018+k\}$ y valida sobre el año $2019+k$, para $k = 1, \ldots, 5$.
- **Predicciones OOF (out-of-fold) retrospectivas:** para cada año $Y \in \{2019, \ldots, 2025\}$ se entrena un modelo independiente con todos los datos del período $< Y$ y se predice $Y$. Esto genera predicciones temporalmente honestas para todo el período histórico, las cuales se reportan en los resultados.

### 4.3 Detección empírica de shocks pandémicos

Para identificar los años de shock de manera reproducible y matemáticamente justificada, se aplican **dos criterios complementarios** sobre la distribución del target:

**Criterio 1: Z-score sobre tasas individuales.** Se calcula la media $\mu_{normal}$ y desviación estándar $\sigma_{normal}$ de las estadísticas anuales (media y desviación estándar del target por año) sobre el conjunto de años no-pandémicos ($\{2018, 2019, 2023, 2024, 2025\}$). Para cada año candidato $y \in \{2020, 2021, 2022\}$ se calcula:

$$ Z_{mean}(y) = \frac{\bar{\text{target}}(y) - \mu_{means,normal}}{\sigma_{means,normal}}, \quad Z_{std}(y) = \frac{\sigma_{target}(y) - \mu_{stds,normal}}{\sigma_{stds,normal}} $$

Si $|Z_{mean}(y)| > 1.96$ (umbral 95%) el año se clasifica como **shock de nivel**; si $|Z_{std}(y)| > 1.96$ se clasifica como **shock de dispersión**.

**Criterio 2: Variación interanual del agregado.** Se calcula la variación porcentual anual del total agregado de matrículas reconstruidas. Cualquier año candidato con variación negativa que no haya sido clasificado por el Criterio 1 se clasifica como **shock de recaída**.

Aplicado al caso chileno, este procedimiento clasifica:
- **2020 → shock de nivel** ($Z_{mean} = -2.19$, $Z_{std} = -0.29$)
- **2021 → shock de dispersión** ($Z_{mean} = -0.68$, $Z_{std} = +2.04$)
- **2022 → shock de recaída** (variación agregada de -0.73%; no detectado por Z-score)

Como tratamiento, se agregan tres variables dummy binarias al feature set (`es_shock_nivel`, `es_shock_dispersion`, `es_shock_recaida`), sin penalización adicional via *sample weight*. Esta decisión se justifica empíricamente: ninguno de los tres shocks presenta varianza inflada que justifique reducir el peso de las observaciones afectadas, y la información de heterogeneidad de 2021 es justamente la que el modelo necesita preservar.

### 4.4 Target encoding fold-aware

Las variables categóricas de alta cardinalidad —`REGIÓN` (16 categorías), `NOMBRE INSTITUCIÓN` (56), `NOMBRE CARRERA` (1.038) y `area_conocimiento` (11)— se codifican mediante *target encoding* con suavizado bayesiano (parámetro $m = 30$). Crucialmente, la codificación se implementa **dentro** del pipeline de scikit-learn mediante la clase `TargetEncoder` de la librería `category_encoders`, lo que garantiza que en cada *fold* del *cross-validation* se ajuste únicamente con los datos de entrenamiento de ese *fold*. La codificación de cada categoría $c$ es:

$$ \text{TE}(c) = \frac{n_c \cdot \bar{y}_c + m \cdot \bar{y}_{global}}{n_c + m} $$

donde $n_c$ es el número de filas con la categoría $c$ en el *fold* de entrenamiento, $\bar{y}_c$ es la media del target en esas filas y $\bar{y}_{global}$ es la media global del target en el *fold*. Categorías con pocas observaciones se acercan a la media global, mitigando *overfitting*.

### 4.5 Feature engineering

Adicionalmente a las variables crudas integradas, se construyeron 30 variables derivadas, organizadas en cuatro grupos:

1. **Lags temporales:** `matriculas_lag1` (transformada con log1p), que captura la inercia interanual.
2. **Ratios estructurales:** `pct_doctores`, `pct_magister`, `pct_especialistas`, `pct_horas_jornada_completa`, etc., que describen la composición del cuerpo docente.
3. **Indicadores competitivos y de mercado:** `densidad_competitiva` (número de instituciones que ofrecen la misma carrera en la misma región-año), `arancel_relativo_regional`, `selectividad_relativa`, `concentracion_matricula_lag`, `pct_matricula_regional_lag`.
4. **Dummies de shock pandémico:** las tres descritas en 4.3.

El feature set final del modelo seleccionado incluye 46 variables.

### 4.6 Modelos evaluados

Se evalúan cuatro baselines informados y tres modelos de *gradient boosting*:

**Baselines:**
- **B0:** Predicción constante igual a la mediana del entrenamiento.
- **B1:** Media histórica del target por combinación (institución, carrera).
- **B2:** Regresión Ridge utilizando únicamente `matriculas_lag1`.
- **B3:** Regresión Ridge con el feature set completo (reducido).

**Modelos principales:**
- **LightGBM** [@ke2017lightgbm]: *gradient boosting* basado en árboles con crecimiento *leaf-wise*.
- **XGBoost** [@chen2016xgboost]: *gradient boosting* extremo con regularización L1/L2.
- **CatBoost** [@prokhorenkova2018catboost]: *gradient boosting* con manejo nativo de variables categóricas y *ordered boosting* para reducir *target leakage*.

### 4.7 Optimización de hiperparámetros

Los tres modelos de *gradient boosting* se optimizan con Optuna [@akiba2019optuna] utilizando un *Tree-structured Parzen Estimator* (TPE) como *sampler* y `MedianPruner` (con `n_startup_trials=10`, `n_warmup_steps=2`) para podar *trials* poco prometedores. Se ejecutan 50 *trials* por modelo, evaluando cada *trial* sobre los seis *folds* del *cross-validation* expanding window y reportando el RMSE promedio en escala arcsinh como métrica objetivo.

### 4.8 Métricas de evaluación

Se reportan ocho métricas complementarias:

- **RMSE** (Root Mean Squared Error): error promedio en N° de matrículas, penaliza errores grandes.
- **MAE** (Mean Absolute Error): error promedio en N° de matrículas.
- **MedAE** (Median Absolute Error): mediana del error absoluto, robusta a outliers.
- **R²:** proporción de varianza explicada.
- **WAPE** (Weighted Absolute Percentage Error): $100 \times \sum|y - \hat{y}| / \sum y$. Recomendada para datos con ceros y rangos heterogéneos.
- **% Confianza:** $100 - \text{WAPE}$, interpretable como "el modelo acierta el X% del total agregado".
- **MAPE** (Mean Absolute Percentage Error): porcentaje promedio.
- **Skill Score** vs baseline naïve: $1 - (RMSE_{modelo} / RMSE_{naive})^2$, donde el naïve predice $\text{matrículas}_t = \text{matrículas}_{t-1}$.

---

## 5. Resultados

### 5.1 Resultados globales del modelo

CatBoost resultó el modelo ganador con RMSE de 0.3109 en *cross-validation* sobre el target en escala arcsinh, superando a LightGBM (0.3122) y XGBoost (0.3140). La diferencia entre los tres es marginal, lo que sugiere que para este problema la familia de *gradient boosting* es robusta a la elección específica de algoritmo, siempre que se haga un tuning adecuado.

La Tabla 3 resume el desempeño del modelo final sobre matrículas absolutas, evaluado en dos conjuntos: el OOF retrospectivo completo (2019-2025) y el holdout 2025.

**Tabla 3.** Desempeño global del modelo CatBoost (tras tuning con 50 trials de Optuna)

| Conjunto | n filas | RMSE | MAE | R² | WAPE (%) | Confianza (%) | Skill score vs naïve (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| OOF retrospectivo (2019-2025) | 54.721 | 36.64 | 13.40 | **0.877** | 18.36 | 81.64 | +62.13 |
| Holdout 2025 | 7.752 | 26.59 | 11.56 | **0.944** | 15.01 | 84.99 | +49.45 |

El R² de 0.944 en holdout 2025 indica que el modelo explica el 94.4% de la varianza del número de matrículas a granularidad fina. El WAPE de 15.01% se traduce en una "confianza" agregada del 85.0% (es decir, la suma de errores absolutos representa solo el 15% del total real). El skill score positivo de +49.45% sobre el baseline naïve confirma que el modelo aporta valor predictivo sustantivo más allá de simplemente proyectar la matrícula del año anterior.

La Figura 1 presenta el gráfico de dispersión de predicciones vs. valores reales, tanto para el OOF retrospectivo como para el holdout 2025. La concentración cercana a la línea de identidad confirma visualmente el desempeño reportado.

![Figura 1. Predicciones vs valores reales en OOF retrospectivo y holdout 2025](figuras/fig02_scatter_pred_vs_real.png)

### 5.2 Análisis macro → micro: la precisión en función del nivel de agregación

Uno de los hallazgos centrales de este trabajo es que la **precisión del modelo varía sistemáticamente con el nivel de agregación**. La Tabla 4 documenta este patrón sobre el OOF retrospectivo (2019-2025).

**Tabla 4.** Métricas del modelo por nivel de agregación (OOF retrospectivo 2019-2025)

| Nivel | n grupos | WAPE (%) | Confianza (%) | R² | RMSE | MAE |
|---|---:|---:|---:|---:|---:|---:|
| 1. Nacional anual | 7 | 3.43 | **96.57** | -1.65* | 24.216 | 19.547 |
| 2. + Institución | 368 | 6.14 | 93.86 | 0.978 | 1.340 | 666.66 |
| 3. + Área conocimiento | 2.755 | 8.87 | 91.13 | 0.973 | 398.59 | 128.57 |
| 4. + Región | 4.324 | 9.52 | 90.48 | 0.970 | 281.87 | 87.93 |
| 5. + Carrera | 15.586 | 13.35 | 86.65 | 0.857 | 109.90 | 34.21 |
| 6. + Condición | 29.509 | 16.10 | 83.90 | 0.876 | 66.26 | 21.78 |
| 7. + Género | 51.293 | 17.90 | 82.10 | 0.877 | 38.98 | 13.94 |
| 8. + Jornada (fina) | 54.504 | 18.32 | 81.68 | 0.874 | 37.18 | 13.42 |

*El R² negativo en Nivel 1 se debe a que con solo 7 observaciones (años) y baja varianza absoluta, el denominador del estadístico se aproxima a cero; el WAPE es la métrica relevante en este nivel.*

El patrón observado es coherente con la teoría: a mayor agregación, los errores idiosincráticos se cancelan parcialmente y la confianza agregada aumenta. En el nivel 1 (proyección nacional anual) el modelo predice con 96.57% de confianza el total agregado. En el nivel 8 (granularidad fina, casi una predicción por fila) la confianza es de 81.68%.

Este resultado tiene una implicación práctica directa: **el modelo es altamente apto para planificación a nivel sistema (nacional, regional, institucional)** y **moderadamente apto para predicciones a nivel de programa específico**. La Figura 2 visualiza este patrón.

![Figura 2. Evolución de WAPE y R² conforme aumenta la granularidad de agregación](figuras/fig06_evolucion_metricas_por_nivel.png)

Es relevante destacar que el patrón se mantiene en el holdout 2025, con confianza de **99.36%** a nivel nacional anual y **85.00%** a granularidad fina (Tabla 5).

**Tabla 5.** Métricas por nivel de agregación (Holdout 2025)

| Nivel | n grupos | WAPE (%) | Confianza (%) | R² |
|---|---:|---:|---:|---:|
| 1. Nacional anual | 1 | 0.64 | **99.36** | n/a |
| 2. + Institución | 51 | 3.88 | 96.12 | 0.993 |
| 3. + Área conocimiento | 390 | 6.27 | 93.73 | 0.987 |
| 4. + Región | 598 | 6.92 | 93.08 | 0.988 |
| 5. + Carrera | 2.197 | 10.48 | 89.52 | 0.963 |
| 6. + Condición | 4.206 | 12.84 | 87.16 | 0.956 |
| 7. + Género | 7.363 | 14.70 | 85.30 | 0.946 |
| 8. + Jornada (fina) | 7.720 | 15.00 | 85.00 | 0.944 |

### 5.3 Desempeño por año: el rol del tamaño del conjunto de entrenamiento

Un análisis crucial para comprender la robustez del modelo es el desempeño desagregado año a año. La estrategia de predicciones OOF retrospectivas implica que cada año $Y$ se predijo entrenando exclusivamente con los datos de los años previos $\{2018, \ldots, Y-1\}$. Esto significa que **la cantidad de información disponible para el entrenamiento crece monotónicamente** con el año predicho, partiendo de 8.444 filas para predecir 2019 (solo el año 2018 disponible como lag) hasta 47.529 filas para predecir 2024. La Tabla 6 documenta este patrón.

**Tabla 6.** Desempeño del modelo por año (OOF retrospectivo)

| Año | n filas predichas | n train acumulado | RMSE | MAE | R² | WAPE (%) | Confianza (%) | Error agregado (%) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 8.264 | 8.444 | 28.19 | 12.22 | 0.921 | 17.60 | 82.40 | +3.47 |
| 2020 | 7.967 | 16.708 | 55.12 | 14.14 | 0.674 | 20.44 | 79.56 | +6.80 |
| 2021 | 7.652 | 24.675 | 38.20 | 15.41 | 0.866 | 20.99 | 79.01 | +1.02 |
| 2022 | 7.595 | 32.327 | 31.03 | 14.01 | 0.912 | 19.08 | 80.92 | +7.22 |
| 2023 | 7.607 | 39.922 | 42.34 | 14.56 | 0.841 | 19.49 | 80.51 | +4.37 |
| 2024 | 7.884 | 47.529 | 25.38 | 12.02 | **0.943** | 16.22 | 83.78 | +0.84 |
| 2025 | 7.752 | 55.413 | 26.59 | 11.56 | **0.944** | 15.01 | 84.99 | -0.64 |

Tres patrones merecen destacarse:

**1. Tendencia ascendente del R² en años post-pandémicos.** El R² del modelo crece sostenidamente de 0.841 en 2023 a 0.944 en 2025. Este crecimiento refleja directamente que **el modelo aprende mejor cuando dispone de más datos**: predecir 2025 con cinco años de historial relevante post-pandémica produce predicciones sustantivamente mejores que predecir 2019 con un único año previo (2018). Este resultado debe ponderarse al interpretar el desempeño de cualquier modelo entrenado con datos longitudinales cortos.

**2. Caída transitoria del R² durante el período pandémico (2020-2023).** El R² cae a 0.674 en 2020 y se recupera gradualmente, alcanzando 0.866 en 2021 y volviendo al rango pre-pandémico solo en 2024. Esta caída tiene dos causas técnicas complementarias: (a) el shock de nivel de 2020 introduce una discontinuidad estructural que ningún modelo entrenado solo con datos pre-pandémicos (es decir, 2018) podía anticipar; (b) la varianza del target en 2020-2022 es naturalmente más alta, lo que reduce el R² aun manteniendo el RMSE relativamente acotado. Es importante notar que el RMSE de 2020 (55.12) es notoriamente más alto que el de cualquier otro año, mientras que el WAPE (20.4%) y el error agregado nacional (+6.80%) se mantienen en rangos manejables. Esto refuerza la conveniencia de reportar múltiples métricas: el R² es informativo pero sensible a cambios en la varianza del target, mientras que WAPE y el error agregado son más estables y prácticamente interpretables.

**3. El año 2019 supera al período pandémico a pesar de tener el conjunto de entrenamiento más pequeño.** El R² de 2019 (0.921) supera al de 2020-2023 a pesar de que el modelo entrenado para predecir 2019 sólo dispone de 8.444 filas de un único año previo (2018). Este resultado refuerza que **el factor limitante del desempeño en 2020-2023 fue la anomalía estructural pandémica, no la cantidad de datos disponibles**. Cuando las condiciones del sistema vuelven a la "normalidad" en 2024-2025, el modelo recupera y supera el desempeño observado en 2019, confirmando que la capacidad de generalización del marco es robusta una vez que se dispone de información representativa.

La Figura 3 visualiza la evolución conjunta de RMSE, R² y WAPE por año, con las bandas de shock pandémico anotadas para contextualizar las caídas observadas.

![Figura 3. Evolución temporal de RMSE, R² y WAPE por año (OOF retrospectivo). Las bandas coloreadas indican los tres tipos de shock pandémico identificados: rojo (shock de nivel, 2020), naranja (shock de dispersión, 2021), morado (shock de recaída, 2022)](figuras/fig03_metricas_por_anio.png)

### 5.4 Backtesting agregado nacional: errores anuales y forecast 2026

Más allá del desempeño a nivel fila individual, el modelo debe evaluarse en su capacidad de predecir agregados nacionales, que es lo que importa para planificación a nivel sistema. La Tabla 7 documenta los errores agregados anuales reconstruidos a partir de las predicciones OOF retrospectivas.

**Tabla 7.** Errores agregados anuales del modelo (nivel nacional)

| Año | Real | Predicho | Error abs | Error rel (%) |
|---:|---:|---:|---:|---:|
| 2019 | 573.548 | 593.433 | +19.885 | +3.47 |
| 2020 | 550.847 | 588.279 | +37.432 | +6.80 |
| 2021 | 561.614 | 567.338 | +5.724 | +1.02 |
| 2022 | 557.507 | 597.755 | +40.248 | +7.22 |
| 2023 | 568.204 | 593.047 | +24.843 | +4.37 |
| 2024 | 584.391 | 589.273 | +4.882 | +0.84 |
| 2025 | 597.058 | 593.244 | -3.814 | -0.64 |

A pesar de la heterogeneidad de los R² por año documentada en la sección 5.3, el **error agregado nacional se mantiene siempre por debajo del 7.3%**, y para los años post-pandémicos cae bajo el 5%. Este resultado tiene implicancias prácticas relevantes: aun cuando el modelo enfrenta dificultades para capturar la dinámica granular durante el período pandémico (R² = 0.674 en 2020), su predicción agregada nacional permanece útil para planificación.

![Figura 4. Backtesting temporal agregado nacional: histórico real, predicción OOF retrospectiva y forecast 2026](figuras/fig08_backtesting_temporal_MONEY_FIGURE.png)

Es notable que el modelo sub-predice levemente en 2025 (sólo 0.64% por debajo del valor real), lo cual contrasta con la sobrepredicción consistente en años anteriores. Esto sugiere que el modelo ha incorporado adecuadamente las dinámicas post-pandémicas y que su pronóstico para 2026 puede considerarse calibrado.

### 5.5 Forecast 2026 y validación contra baselines simples

El modelo proyecta una matrícula nacional total de **612.578 estudiantes para 2026**, equivalente a un crecimiento de **+2.60% sobre 2025**. La Tabla 8 contrasta esta predicción contra tres baselines simples.

**Tabla 8.** Comparación del forecast 2026 contra baselines

| Método | Predicción 2026 | Crecimiento (%) | Diferencia vs modelo (pp) |
|---|---:|---:|---:|
| Modelo CatBoost (este trabajo) | 612.578 | +2.60 | — |
| Regresión lineal 2018-2025 | 575.348 | -3.64 | +6.24 |
| Promedio variaciones 2023-2025 | 610.860 | +2.31 | +0.29 |
| Variación 2025 (último año) | 610.000 | +2.17 | +0.43 |

El forecast del modelo se aleja sustancialmente de la regresión lineal simple sobre todo el período (-3.64%), porque el baseline lineal incorpora el shock de 2020 y subestima la recuperación post-pandémica. Por el contrario, el forecast es **consistente** (diferencias menores a 0.5 puntos porcentuales) con baselines que utilizan exclusivamente años post-pandémicos, lo que apoya la razonabilidad de la predicción. La Figura 5 visualiza la comparación.

![Figura 5. Validación del forecast 2026 contra baselines simples](figuras/fig09_validacion_forecast_2026.png)

### 5.6 Desempeño por región

La Tabla 9 (resumida; completa en el apéndice digital) muestra el desempeño del modelo desagregado por región. La heterogeneidad regional es moderada: la confianza varía entre 66.6% (Aysén) y 87.0% (Los Ríos). Las regiones con peor desempeño son las de menor cantidad de observaciones (Aysén, Atacama, Magallanes), lo cual es consistente con la lógica del modelo: regiones con pocas instituciones y carreras tienen mayor varianza idiosincrática.

**Tabla 9.** Desempeño por región (OOF 2019-2025; selección)

| Región | n | R² | WAPE (%) | Confianza (%) |
|---|---:|---:|---:|---:|
| Los Ríos | 1.637 | 0.948 | 12.99 | **87.01** |
| Maule | 2.557 | 0.891 | 15.93 | 84.07 |
| La Araucanía | 3.771 | 0.894 | 16.42 | 83.58 |
| Antofagasta | 2.213 | 0.934 | 16.70 | 83.30 |
| Metropolitana | 20.913 | 0.868 | 19.01 | 80.99 |
| Atacama | 843 | 0.750 | 26.53 | 73.47 |
| Aysén | 239 | 0.669 | 33.44 | **66.56** |

La Región Metropolitana, a pesar de concentrar el 38% de las observaciones, presenta una confianza intermedia (81.0%), reflejando la heterogeneidad propia del mercado capitalino. La Figura 6 visualiza el ranking completo.

![Figura 6. WAPE por región (OOF 2019-2025)](figuras/fig04_wape_por_region.png)

### 5.7 Cuantificación del sesgo de target encoding mal aplicado

Como aporte metodológico complementario, se cuantificó empíricamente el sesgo introducido por un *target encoding* precalculado (leaky) versus uno implementado correctamente dentro del *cross-validation* (fold-aware). El experimento controla todos los demás aspectos del pipeline, modificando únicamente este paso.

**Tabla 10.** TE-leaky vs. TE-fold-aware (RMSE en CV)

| Configuración | RMSE CV |
|---|---:|
| TE-leaky (precalculado) | 0.3047 |
| **TE-fold-aware (correcto)** | **0.3109** |
| Delta (leaky − correcto) | -0.0062 |

El uso ingenuo del *target encoding* reportaría un RMSE 2.0% mejor de lo que el modelo realmente alcanzaría en producción. Aunque la diferencia es modesta en magnitud absoluta, su importancia conceptual es significativa: en estudios donde el *target encoding* se aplica sobre múltiples variables de alta cardinalidad y donde las comparaciones entre modelos son ajustadas (diferencias del orden del 1-2%), un sesgo de esta magnitud puede invertir el ranking aparente de modelos. Este resultado constituye una llamada de atención metodológica para la literatura aplicada.

### 5.8 Explicabilidad: análisis SHAP

Para interpretar el modelo se aplicó análisis SHAP (SHapley Additive exPlanations) [@lundberg2017shap] sobre el conjunto completo. La Tabla 11 lista las 15 variables más influyentes según la magnitud absoluta de su contribución SHAP promedio.

**Tabla 11.** Top 15 features por importancia SHAP

| # | Feature | SHAP medio absoluto |
|---:|---|---:|
| 1 | matriculas_lag1 | 0.0730 |
| 2 | CONDICION_NUEVO | 0.0705 |
| 3 | NOMBRE CARRERA | 0.0482 |
| 4 | pct_matricula_regional_lag | 0.0311 |
| 5 | GENERO | 0.0217 |
| 6 | JORNADA_Diurna | 0.0202 |
| 7 | puntaje_maximo | 0.0152 |
| 8 | area_conocimiento | 0.0136 |
| 9 | concentracion_matricula_lag | 0.0123 |
| 10 | NOMBRE INSTITUCIÓN | 0.0121 |
| 11 | ratio_docente_estudiante | 0.0116 |
| 12 | puntaje_minimo | 0.0101 |
| 13 | AÑO_AUX | 0.0084 |
| 14 | N°Docentes | 0.0083 |
| 15 | retencion_1er_anio | 0.0077 |

El hallazgo más destacable es que `CONDICION_NUEVO` —indicador binario de si una fila corresponde a alumnos nuevos vs. antiguos— es **casi tan importante como el lag temporal**. Esto refleja una realidad estructural del sistema: la dinámica de crecimiento de matrículas de alumnos nuevos (que depende de admisión y captación) es fundamentalmente distinta a la de antiguos (que depende de retención). Cualquier modelo que ignore esta distinción —es decir, que agregue ambos grupos— pierde una fracción sustantiva del poder predictivo.

Las tres dummies de shock pandémico (`es_shock_nivel`, `es_shock_dispersion`, `es_shock_recaida`) **no aparecen en el top 15 de importancia SHAP**. Esto sugiere que CatBoost captura los efectos pandémicos principalmente a través de la variable `AÑO_AUX` (posición 13 en el ranking), mediante *splits* específicos sobre años. Las dummies cumplen, no obstante, un rol de robustez metodológica: hacen el tratamiento del shock explícito y trazable, permitiendo análisis de sensibilidad.

---

## 6. Discusión

### 6.1 Lectura general de los resultados

Este trabajo proporciona, hasta donde se conoce, el primer benchmark publicado de predicción de matrícula universitaria chilena a granularidad fina (institución × carrera × jornada × género × condición × año). Los resultados muestran que un modelo de *gradient boosting* correctamente entrenado y validado temporalmente alcanza un desempeño predictivo robusto: R² = 0.944 y WAPE = 15.0% en holdout 2025 a granularidad fina, escalando a 99.4% de confianza al agregar a nivel nacional.

Estos números son comparables o superiores a los reportados en literatura internacional para predicciones agregadas, **a pesar de operar a una granularidad mucho mayor**. Esto sugiere que la combinación de (i) un dataset multifuente bien integrado, (ii) una metodología de *machine learning* moderna y (iii) una validación temporal estricta permite alcanzar precisión competitiva sin sacrificar la riqueza interpretativa de la granularidad fina.

### 6.2 La distinción entre tasa y nivel: una observación metodológica relevante

Un resultado conceptualmente importante de este trabajo es la diferencia entre el desempeño medido sobre la **tasa de crecimiento** (R² aproximadamente 0.18 en escala arcsinh) y el desempeño medido sobre el **nivel absoluto de matrículas** (R² aproximadamente 0.94). Esta diferencia se explica por la presencia de inercia institucional: la mayoría de las matrículas de un año dado pueden anticiparse a partir del lag, mientras que la tasa de crecimiento marginal está sujeta a alta varianza idiosincrática.

Implicación para la literatura aplicada: los estudios que reporten métricas únicamente sobre tasas pueden estar subestimando significativamente la utilidad práctica de sus modelos. Para audiencias de planificación, el desempeño sobre niveles es la métrica relevante.

### 6.3 La importancia del experimento TE-leaky

La cuantificación del sesgo introducido por *target encoding* mal aplicado (2.0% del RMSE) puede parecer modesta. Sin embargo, su importancia trasciende la magnitud absoluta. En la mayoría de comparaciones entre modelos en literatura aplicada, las diferencias entre el primer y segundo lugar suelen ser del orden de 1-3% en RMSE. Esto significa que **un único error metodológico de target encoding puede invertir el ranking aparente** y conducir a conclusiones erróneas sobre cuál algoritmo es superior. La recomendación práctica es clara: cualquier estudio que utilice *target encoding* sobre variables de alta cardinalidad debe implementarlo dentro del *pipeline*, no como paso de preprocesamiento previo.

### 6.4 El tratamiento de la pandemia: hallazgos y matices

El método propuesto de detección automatizada identifica tres tipos de shock pandémico diferenciados: nivel (2020), dispersión (2021) y recaída (2022). Este es un aporte conceptual porque rompe con el tratamiento monolítico ("años COVID") que predomina en la literatura aplicada.

Sin embargo, el análisis SHAP revela que para árboles de decisión las dummies resultantes no son highly informativas: el modelo ya captura los patrones temporales mediante la variable `AÑO_AUX`. Esto no invalida el tratamiento (no introduce ruido y aporta robustez metodológica), pero sí sugiere que para algoritmos de árboles la importancia práctica del tratamiento explícito es limitada. Para modelos lineales —donde la relación temporal debe codificarse explícitamente— el aporte de las dummies probablemente sea mayor.

### 6.5 Limitaciones

**Cobertura del universo.** Este trabajo cubre exclusivamente universidades (56 instituciones, ~600 mil estudiantes), excluyendo los Centros de Formación Técnica (CFT) e Institutos Profesionales (IP) que en conjunto representan aproximadamente la mitad de la matrícula de educación superior del país. La extensión del marco a esos subsectores es una dirección futura natural.

**Heterogeneidad regional en regiones pequeñas.** El desempeño del modelo es claramente más bajo en Aysén (confianza 66.6%) y Atacama (73.5%), las dos regiones con menor cantidad de programas. Esto sugiere que, en regiones con baja cantidad de observaciones, podría ser beneficioso utilizar modelos jerárquicos bayesianos que regularicen las predicciones hacia el comportamiento promedio del sistema.

**Forecast 2026 bajo supuesto de estabilidad de variables exógenas.** El pronóstico para 2026 asume que las variables macroeconómicas (PIB regional, tasa de desempleo) y estructurales (composición docente, infraestructura, aranceles) permanecen al nivel 2025. Si bien esto es razonable bajo condiciones normales, eventos macroeconómicos significativos podrían invalidar parcialmente la proyección. Un análisis de sensibilidad explícito a estos supuestos es trabajo pendiente.

**Naturaleza descriptiva, no causal.** Este es un modelo predictivo, no causal. Las contribuciones SHAP identifican asociaciones, no relaciones causales. Cualquier interpretación de tipo "esta variable causa que la matrícula crezca" requiere métodos adicionales (variables instrumentales, *difference-in-differences*, etc.) que están fuera del alcance de este trabajo.

**Imputación masiva en algunas variables.** El 35% de las celdas de la columna aranceles fueron imputadas en la capa terminal (mediana global), lo cual implica que para esos casos el modelo cuenta con una señal débil de la variable. Sin embargo, la *flag* `fue_imputado` permite al modelo conocer este hecho y ajustar sus predicciones en consecuencia.

### 6.6 Direcciones futuras

Cuatro líneas de extensión natural se identifican:

1. **Extensión al ecosistema CFT/IP.** Replicar el pipeline en los subsectores no-universitarios, ajustando las fuentes SIES/CNED correspondientes y evaluando si el método de detección de shocks pandémicos identifica patrones similares.

2. **Modelado jerárquico para regiones pequeñas.** Aplicar técnicas de *partial pooling* (modelos bayesianos jerárquicos) para mejorar el desempeño en regiones de baja cardinalidad.

3. **Análisis de sensibilidad explícita del forecast a supuestos macroeconómicos.** Generar bandas de pronóstico bajo distintos escenarios de PIB regional y desempleo (optimista, neutro, pesimista).

4. **Integración de variables idiosincráticas no observadas hoy.** Datos de admisión institucional, campañas de marketing, satisfacción estudiantil, o decisiones internas de los rectores podrían reducir significativamente la varianza no explicada actual (~17% del agregado).

---

## 7. Conclusiones

Este trabajo propuso un marco replicable para predicción de matrícula universitaria chilena a granularidad fina, integrando diez fuentes oficiales y aplicando *machine learning* con validación temporal estricta. Los principales aportes son: (i) un dataset integrado de 63.165 observaciones a granularidad institución × carrera × región × jornada × género × condición × año; (ii) un modelo predictivo (CatBoost) que alcanza R² = 0.944 y WAPE = 15.0% en holdout 2025 a granularidad fina, escalando a 99.4% de confianza al agregar a nivel nacional; (iii) un método automatizado de detección de tres tipos de shock pandémico (nivel, dispersión, recaída); (iv) cuantificación empírica del sesgo introducido por *target encoding* mal aplicado (2.0% del RMSE); (v) un pronóstico de matrícula nacional 2026 de 612.578 estudiantes (+2.60% sobre 2025).

Las implicancias prácticas son directas. Para las autoridades de política pública, el modelo aporta una herramienta de proyección agregada con 99% de confianza al nivel nacional, útil para la planificación de subsidios y dimensionamiento del sistema. Para las universidades, el modelo es directamente aplicable para anticipar matrícula institucional con ~96% de confianza, y carrera-específica con ~89% de confianza. Para investigadores en *machine learning* aplicado a educación, este trabajo aporta evidencia empírica concreta sobre la importancia de la implementación correcta del *target encoding* y un método replicable de tratamiento de shocks externos.

El código de los notebooks de modelado y análisis está disponible públicamente, en línea con buenas prácticas de ciencia abierta y reproducibilidad. Las fuentes de datos utilizadas son todas públicas y oficiales, permitiendo la replicación íntegra del trabajo a partir del código publicado.

---

## Disponibilidad de código

En línea con buenas prácticas de ciencia abierta y reproducibilidad, se publican los dos notebooks principales del pipeline:

- **`modelado_predictivo_admision_v2.ipynb`**: pipeline completo de entrenamiento, validación temporal, optimización de hiperparámetros con Optuna, evaluación contra baselines y generación de predicciones OOF retrospectivas y forecast 2026. Incluye la implementación de target encoding fold-aware y la detección automatizada de shocks pandémicos.
- **`analisis_paper_resultados.ipynb`**: notebook de análisis post-hoc que produce todas las figuras, tablas y métricas reportadas en este trabajo a partir de las predicciones exportadas por el pipeline principal.

Ambos notebooks están disponibles en el repositorio público: https://github.com/diegoevans/Predictive-model-of-university-admission (placeholder; se actualizará en la versión publicada).

**Sobre las bases de datos**: las fuentes originales utilizadas en este trabajo son todas de acceso público y pueden descargarse directamente desde los organismos correspondientes (SIES del MINEDUC, BaseINDICES del CNED, INE, Banco Central de Chile, mifuturo.cl). El detalle de las fuentes, sus rutas de descarga y el período cubierto se documenta en la Tabla 1 y en el README del repositorio. El dataset consolidado intermedio (`dataset_modelado_final.csv`) no se publica directamente, pero su construcción es completamente trazable a partir del código provisto y las fuentes públicas referenciadas, permitiendo reproducir el procedimiento integralmente.

## Agradecimientos

A las instituciones que mantienen pública la información del sistema universitario chileno: MINEDUC (SIES), CNED, INE, Banco Central de Chile, CNA y mifuturo.cl. Sin esa apertura, este trabajo no sería posible.

## Conflicto de intereses

El autor declara no tener conflicto de intereses.

---

## Referencias

[@akiba2019optuna] Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A Next-generation Hyperparameter Optimization Framework. *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining*, 2623–2631.

[@cerda2018ml] Cerda, F., & otros. (2018). Aplicación de machine learning para la predicción de deserción estudiantil en universidades chilenas. *Revista Chilena de Ingeniería*, 26(3), 412–423.

[@chen2016xgboost] Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794.

[@cned2024informe] Consejo Nacional de Educación. (2024). *Informe Anual del Sistema de Educación Superior Chileno*. Santiago: CNED.

[@gonzalez2019predicciones] González, P., & Muñoz, R. (2019). Predicciones de matrícula universitaria en Chile mediante modelos ARIMA. *Calidad en la Educación*, 51, 134–158.

[@kaggle2019leakage] Kaggle. (2019). *Data Leakage Best Practices*. Recuperado de https://www.kaggle.com/learn/intro-to-machine-learning

[@ke2017lightgbm] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. *Advances in Neural Information Processing Systems*, 30.

[@lundberg2017shap] Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems*, 30.

[@micci2001target] Micci-Barreca, D. (2001). A preprocessing scheme for high-cardinality categorical attributes in classification and prediction problems. *ACM SIGKDD Explorations Newsletter*, 3(1), 27–32.

[@perez2020rendimiento] Pérez, M., & Soto, J. (2020). Predicción del rendimiento académico mediante machine learning en universidades chilenas. *Revista Iberoamericana de Educación Superior*, 11(32), 89–106.

[@prokhorenkova2018catboost] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: unbiased boosting with categorical features. *Advances in Neural Information Processing Systems*, 31.

[@ramirez2021forecasting] Ramírez, A., & Vargas, L. (2021). Forecasting de matrícula universitaria en México: una comparación de métodos econométricos. *Perfiles Educativos*, 43(172), 78–96.

[@shwartz2022tabular] Shwartz-Ziv, R., & Armon, A. (2022). Tabular data: Deep learning is not all you need. *Information Fusion*, 81, 84–90.

[@sies2024informe] Servicio de Información de Educación Superior. (2024). *Informe de matrícula 2024*. Santiago: MINEDUC.

[@silva2022duracion] Silva, R., & Rojas, C. (2022). Modelos predictivos de duración de estudios universitarios en Chile. *Estudios Pedagógicos*, 48(2), 145–162.

[@smith2018enrollment] Smith, J., & Williams, K. (2018). Enrollment forecasting using IPEDS data: A multi-institution study. *Research in Higher Education*, 59(8), 945–971.
