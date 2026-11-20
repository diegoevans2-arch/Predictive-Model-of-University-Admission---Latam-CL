---
title: "Apéndice en línea — Cuando el pronóstico ingenuo es el rezago: evaluación del pronóstico de matrícula universitaria a nivel de programa en Chile"
lang: es-CL
---

<!-- Material suplementario anonimizado para revisión doble anónima. Las cifras provienen del manuscrito y de la documentación técnica del pipeline elaborada por el autor. -->

Este apéndice reúne el detalle operativo y los resultados complementarios referidos desde el manuscrito. Las tablas y figuras se numeran A.1, A.2, …; los orígenes de pronóstico («origen 2025» y «origen 2026») se definen en la Sección 4.1 del manuscrito. Salvo indicación en contrario, las cifras corresponden al origen 2026.

# A.1 Reglas de ingesta por fuente

Cada fuente se procesa por separado y conserva su granularidad original; la ingesta no une fuentes ni imputa entre ellas, sólo limpia, reestructura y verifica que no se pierda información.

**Matrícula (SIES).** Serie 2007–2026, una fila por programa y año, con matrícula total y de primer año por género (mujeres, hombres, no binarios o indefinidos).

**Tabla A.1.** Reglas de ingesta de la base de matriculados del SIES.

| # | Regla | Detalle |
|---:|---|---|
| 1 | Año | Cuatro últimos caracteres del campo de año |
| 2 | Faltantes antes de restar | La matrícula total y de primer año por género se rellena con cero antes de operar, para que una resta con un faltante no produzca un faltante silencioso |
| 3 | Estudiantes antiguos | Total menos primer año, por género, acotado en cero |
| 4 | Universo | Sólo pregrado |
| 5 | Llave por código | Del código institución-sede-carrera-jornada-versión se extraen institución y carrera (código base de carrera), que no cambia con la sede ni el plan |
| 6 | Formato largo | Cada programa se abre en hasta seis filas (3 géneros × 2 condiciones); se eliminan las de matrícula cero |

Controles: conservación exacta de la matrícula de pregrado en tres niveles (total de la fuente, suma de las seis columnas y suma en formato largo: 22.357.425 en los tres); cobertura de la llave por código de 96,5 % de las filas de pregrado; cero nulos y categorías válidas.

**Aranceles, puntajes y duración (CNED, INDICES).** Se seleccionan 19 columnas (aranceles, valor de matrícula, valor del título, duración, puntajes de admisión y de corte) y se conservan las filas de pregrado (215.743 de 260.307). La edición vigente cubre 2005–2026; 2026 trae 10.572 filas frente a 10.865 de 2025.

**Cuerpo docente e infraestructura (CNED, INDICES).** Conteos por grado académico, jornada, horas y sexo, y m² de terreno, construidos y de salas, agregados a institución × región × año, con control de conservación de la superficie antes y después de agregar. Cobertura 2005–2025.

**PIB regional (Banco Central de Chile).** Paso a formato largo año × región, excluyendo subtotales y el PIB extrarregional, con traducción explícita de los 16 nombres de región a la nomenclatura canónica. La serie es el PIB trimestral por región en volumen a precios del año anterior encadenado, series empalmadas, referencia 2018 (miles de millones de pesos encadenados; Banco Central de Chile, edición del 23-04-2026, cifras preliminares, última observación del cuarto trimestre de 2025), entregada en filas anuales 2013–2025; el valor de 2026 se arrastra desde 2025.

**Tasa de desocupación regional (INE, Encuesta Nacional de Empleo).** Se usa la serie de ambos sexos, que es la tasa oficial ponderada por la fuerza de trabajo, y se anualiza como promedio de los trimestres móviles publicados del año. En 2018–2024 se promedian 12 trimestres móviles; en 2025, 10. El INE publica trimestres móviles mensuales; los 10 de 2025 son los que comienzan entre enero y octubre, y faltan los que comienzan en noviembre y diciembre, que en los años completos sí entran al promedio. El control del pipeline sólo marca los años con menos de cuatro períodos.

**Retención de primer año y empleabilidad (mifuturo.cl).** Extracción año a año con hoja, fila de encabezado y orden de columnas declarados; asignación de código institucional faltante en 2020 por nombre normalizado; «s/i» como faltante; retención y empleabilidad acotadas en [0, 1].

# A.2 Consolidación, normalización de llaves y cobertura

**Universo.** Del SIES procesado se conservan 2018–2026 y las tres categorías universitarias: 127.424 filas de 60 códigos de institución. Aparte se conserva el universo universitario 2017–2026, usado para construir el rezago.

**Normalización.** Una única normalización de textos de llave (mayúsculas, sin tildes ni puntos, espacios simples). Las instituciones del CNED y de mifuturo.cl se mapean al código del SIES por nombre normalizado, con unificación de siglas, expansión de abreviaturas y cinco excepciones manuales auditables; cobertura: docentes, infraestructura y aranceles 60 de 60, retención 58 de 60.

**Unión.** Todas las fuentes se unen a la izquierda desde el SIES después de agregarlas a la granularidad exacta de su llave, con control de no inflado (entran 127.424 filas y salen 127.424).

**Tabla A.2.** Cobertura de las fuentes secundarias medida desde el SIES, antes del arrastre.

| Fuente | Combinaciones del SIES | Con dato | Cobertura |
|---|---:|---:|---:|
| PIB | 144 | 120 | 83,33 % |
| Desocupación | 144 | 128 | 88,89 % |
| Docentes | 1.205 | 842 | 69,88 % |
| Infraestructura | 1.205 | 848 | 70,37 % |
| Retención | 22.990 | 4.844 | 21,07 % |
| Aranceles | 30.702 | 19.432 | 63,29 % |

**Defecto conocido de normalización regional (Ñuble).** Por un defecto de orden de operaciones en la consolidación, la reparación del nombre de la región de Ñuble no se aplicó antes de las uniones con docentes, infraestructura y aranceles: sus 3.474 filas (2,73 % del universo) entran a esas uniones sin código de región, de modo que docentes e infraestructura caen a la mediana global y los aranceles se imputan por la cascada. El PIB se vuelve a unir tras la corrección. La corrección está identificada y se evaluará en la siguiente versión metodológica, sin modificar el pronóstico 2027; su efecto sobre el error no está medido.

**Tabla A.3.** Filas por etapa del procesamiento. S1: SIES pregrado, todas las instituciones; S2: universidades 2018–2026; S3: tabla consolidada; S4: con objetivo; S5: panel de modelado.

| Año | S1 | S2 | S3 | S4 | S5 |
|---:|---:|---:|---:|---:|---:|
| 2018 | 34.653 | 15.167 | 15.052 | 14.541 | 9.505 |
| 2019 | 34.090 | 14.738 | 14.652 | 14.070 | 9.424 |
| 2020 | 33.466 | 14.317 | 14.232 | 13.817 | 9.321 |
| 2021 | 34.527 | 14.312 | 14.212 | 13.795 | 9.230 |
| 2022 | 34.950 | 14.330 | 14.231 | 13.904 | 9.161 |
| 2023 | 35.643 | 14.099 | 14.022 | 13.682 | 9.038 |
| 2024 | 34.984 | 13.679 | 13.602 | 13.328 | 9.176 |
| 2025 | 34.569 | 13.475 | 13.401 | 13.055 | 9.043 |
| 2026 | 34.169 | 13.307 | 13.239 | 12.967 | 9.069 |
| Total | 311.051 | 127.424 | 126.643 | 123.159 | 82.967 |

Las caídas se explican así: S1→S2 excluye instituciones no universitarias (deliberado); S2→S3 elimina 781 duplicados exactos (0,12 % de la matrícula, sin efecto en rezago ni objetivo); S3→S4 elimina 3.484 filas sin rezago o con rezago cero; S4→S5 elimina 25.364 filas con rezago menor que diez y colapsa 14.828 filas que comparten celda (sin eliminar matrícula). Ningún criterio depende del error de predicción; todos son estructurales y previos al modelado, pero no son neutrales: lo excluido —celdas pequeñas y nuevas— es lo que más crece. El panel retiene entre 96,0 % y 98,0 % de la matrícula universitaria de cada año.

# A.3 Imputación jerárquica y arrastre de exógenas

**Tabla A.4.** Capas de imputación. Cada capa resuelve sólo lo que la anterior dejó vacío.

| Capa | Variables | Regla |
|---|---|---|
| 1 · Temporal | Docentes e infraestructura | Interpolación lineal en el año dentro de institución-región, con relleno hacia adelante y atrás |
| 2 · Jerárquica | Aranceles, puntajes, duración, retención, empleabilidad | Mediana (institución, carrera) → (institución, área, año) → (área, año) |
| 2.5 · Región y carrera | Las mismas | (región, carrera, año) → (región, carrera) → (carrera, año) → (carrera) |
| 2.7 · Institución | Las mismas | (institución, año) → (institución) |
| 3 · Terminal | Todas | Mediana global |

De 1.292.058 valores faltantes en la tabla consolidada, los de docentes e infraestructura (590.785) se resuelven en 59,0 % por la capa temporal y en 41,0 % por la mediana global, que no aporta señal; los de aranceles, puntajes y retención (701.273) se resuelven completos en la capa jerárquica, con la misma carrera en otros años o el área de la institución. Las capas 2.5 y 2.7 no resuelven nada en esta corrida y se mantienen como red de seguridad. La indicadora de imputación entra al modelo; en el panel de modelado, el 70,9 % de las filas tiene al menos un valor imputado (67,3 % en el origen 2025).

**Arrastre.** El PIB regional y la desocupación no se imputan. Si una fuente no publica el último año de la ventana, se repiten sus valores regionales del último año publicado y se registra el arrastre (fuente, último año publicado y años arrastrados). En el origen 2026 se arrastraron ambos de 2025 a 2026 (16 valores regionales cada uno); docentes e infraestructura de 2026 repiten 2025 por la capa temporal, y la retención y empleabilidad de 2026 son la mediana histórica de cada institución-carrera. La edición 2026 del SIES revisó la matrícula universitaria de 2025 de 731.981 a 732.034 (+53).

# A.4 Llave del rezago: composición y controles

El rezago se calcula sobre el universo universitario 2017–2026, antes de deduplicar, con la cascada fino → código → medio (Tabla 2 del manuscrito). El rezago es el valor del año anterior sólo si ese año es exactamente $t-1$; si una celda-año tiene más de un código, se usa el de mayor matrícula.

**Tabla A.5.** Composición del rezago por nivel de emparejamiento sobre el universo universitario desde 2018 (por celda, antes del filtro de rezago mínimo).

| Origen del rezago | Celdas | % de la matrícula | Tasa mediana | % con tasa < −0,8 | Razón rezago/celda mediana |
|---|---:|---:|---:|---:|---:|
| Fino | 102.036 | 97,80 % | 0,000 | 1,16 % | 1,000 |
| Código | 1.041 | 0,68 % | 0,000 | 1,44 % | 1,000 |
| Medio (escalado) | 4.198 | 0,80 % | +0,194 | 0,45 % | 0,837 |
| Sin rezago | 3.386 | 0,71 % | — | — | — |

**Control de regresión.** En los niveles código y medio la razón rezago/celda debe rondar uno y la tasa mediana no debe ser negativa. Una tasa mediana del nivel medio cercana a −0,87 con razón cercana a 8 indica que el escalado por participación no se aplicó: es exactamente la firma del defecto descrito en la Sección 5.1. La llave por código recupera 42.641 matrículas en 1.041 celdas. En el panel de modelado, la composición es 97,94 % fino, 0,84 % código y 1,22 % medio. Restringido a las celdas evaluadas 2019–2026, el emparejamiento es fino en el 98,10 % de las celdas (98,89 % de la matrícula), por código en el 0,66 % (0,56 %) y medio en el 1,25 % (0,56 %).

**Desempeño por origen del rezago (origen 2026).** De las 50 peores celdas por error absoluto, 49 en el OOF 2019–2025 y las 50 del *holdout* 2026 tienen rezago fino. Los respaldos pesan el 1,1 % de la matrícula y tienen más error relativo, pero no explican el extremo de la distribución: las peores celdas son contracciones reales de programas.

**Tabla A.6.** Desempeño por origen del rezago en el OOF 2019–2025 y en el *holdout* 2026 (origen 2026).

| Conjunto | Origen del rezago | Celdas | WAPE | WAPE pers. | *Skill* | RelMAE |
|---|---|---:|---:|---:|---:|---:|
| OOF 2019–2025 | fino | 63.154 | 14,33 % | 14,79 % | −3,24 % | 0,969 |
| OOF 2019–2025 | código | 420 | 17,93 % | 17,41 % | −14,41 % | 1,030 |
| OOF 2019–2025 | medio | 819 | 31,08 % | 32,44 % | +27,80 % | 0,958 |
| *Holdout* 2026 | fino | 8.909 | 11,99 % | 12,81 % | +14,25 % | 0,936 |
| *Holdout* 2026 | código | 63 | 16,84 % | 15,82 % | −15,55 % | 1,064 |
| *Holdout* 2026 | medio | 97 | 27,29 % | 31,93 % | +29,10 % | 0,855 |

*Nota:* pers. = persistencia. RelMAE = MAE del modelo dividido por el MAE de la persistencia en el mismo conjunto (Sección 4.8 del manuscrito).

**Propiedades del escalado.** (i) $y_{t-1}(1+\text{tasa})$ devuelve exactamente la matrícula de la celda, de modo que la reconstrucción no se distorsiona; (ii) la participación es menor o igual que uno, de modo que el respaldo nunca infla; (iii) si grupo y celda coinciden, la participación es uno; (iv) el rezago queda en la escala de la celda y puede alimentar variables de mercado que suman rezagos.

# A.5 Variables del modelo

**Tabla A.7.** Grupos de columnas del panel de modelado.

| Grupo | Columnas | Notas |
|---|---|---|
| Categóricas (4) | Región, institución, carrera, área | *Target encoding* ajustado dentro del *fold* |
| Tiempo (1) | Año | |
| Grano (6) | Género; jornada diurna, otra, semipresencial, vespertina; condición nuevo | Bases: a distancia, antiguos |
| Rezago (2) | Rezago de matrícula; origen del rezago | Rezago en $\log(1+x)$; el origen es trazabilidad y no entra al modelo |
| Objetivo (1) | Tasa de crecimiento | Arcsinh de la tasa winsorizada (cortes −0,79 y +1,29) |
| Macroeconómicas (3) | PIB, desocupación, matrícula sobre PIB | PIB en $\log(1+x)$ |
| Precio y selectividad (11) | Arancel, valor de matrícula, 3 puntajes, 3 de corte, duración, arancel relativo regional, selectividad relativa | Montos en $\log(1+x)$ |
| Claustro (7) | Número de docentes, 5 ratios, razón docente/estudiante | |
| Infraestructura (1) | Densidad de estudiantes por m² | $\log(1+x)$ |
| Mercado (3) | Densidad competitiva, concentración rezagada, participación regional rezagada | |
| Retención (1) | Retención de primer año | |
| Clasificación y acreditación (7) | Indicadoras de tipo de institución y acreditación | |
| Trazabilidad (1) | Indicadora de imputación | Entra al modelo |
| Indicadoras de shock (3) | Nivel, dispersión, recaída | Dos constantes en cero |

**Variables con información del año evaluado.** La densidad de estudiantes por m², la razón docente/estudiante y la matrícula sobre PIB usan la matrícula agregada del año $t$ por institución-región o región; constituyen una excepción declarada a la regla anti-fuga (Sección 6.5 del manuscrito). La densidad competitiva, el arancel relativo y la selectividad relativa usan la oferta, los aranceles y los puntajes del año $t$, que se publican antes del período de matrícula.

# A.6 Detección empírica de años de shock

**Tabla A.8.** Estadísticos anuales del objetivo y clasificación (origen 2026). Años normales de referencia: 2018, 2019, 2023, 2024, 2025 y 2026.

| Año | Media | Desv. | % tasas negativas | Z media | Z desv. | Clasificación |
|---:|---:|---:|---:|---:|---:|---|
| 2018 | 0,0132 | 0,3090 | 47,2 % | | | Normal |
| 2019 | −0,0070 | 0,2876 | 49,0 % | | | Normal |
| 2020 | −0,0384 | 0,2934 | 54,5 % | −4,95 | −0,52 | Shock de nivel |
| 2021 | 0,0126 | 0,3292 | 45,1 % | −0,02 | +1,36 | No detectado |
| 2022 | −0,0270 | 0,3202 | 55,5 % | −3,85 | +0,89 | Shock de nivel |
| 2023 | 0,0176 | 0,3356 | 50,3 % | | | Normal |
| 2024 | 0,0121 | 0,3072 | 48,5 % | | | Normal |
| 2025 | 0,0210 | 0,2983 | 46,2 % | | | Normal |
| 2026 | 0,0200 | 0,2823 | 44,7 % | | | Normal |

El criterio de recaída no se activa: los dos años candidatos con variación agregada negativa (2020 y 2022) ya están clasificados como shock de nivel. La indicadora de shock de nivel vale uno en 18.482 filas. Nótese que el conjunto de años normales incluye el año de *holdout* (imperfección declarada en la Sección 6.5).

# A.7 Referentes informados y candidatos

**Tabla A.9.** Referentes y modelo final en el *holdout* 2026, escala del objetivo (arcsinh de la tasa).

| Modelo | Descripción | RMSE | MAE | R² |
|---|---|---:|---:|---:|
| B0 | Mediana del entrenamiento (≈ persistencia en tasas) | 0,2830 | 0,2015 | −0,0050 |
| B1 | Media histórica institución-carrera | 0,2929 | 0,2093 | −0,0767 |
| B2 | Ridge sólo con el rezago | 0,2831 | 0,2021 | −0,0057 |
| B3 | Ridge con 43 variables (α = 10) | 0,2773 | 0,2008 | 0,0350 |
| CatBoost optimizado | Modelo final | 0,2605 | 0,1867 | 0,1480 |

*Nota:* escala del objetivo de entrenamiento (tasa recortada). Con la tasa observada, el R² del modelo final sobre la tasa en el *holdout* 2026 es 0,141.

**Tabla A.10.** Candidatos de *boosting* y Random Forest en validación cruzada (siete *folds*, origen 2026).

| Modelo | RMSE CV sin optimizar | R² medio sobre la tasa | RMSE CV optimizado | Tiempo de optimización |
|---|---:|---:|---:|---:|
| CatBoost | 0,2964 ± 0,0174 | 0,086 | 0,2949 | 58,5 min |
| XGBoost | 0,2972 ± 0,0178 | 0,081 | 0,2933 | 15,0 min |
| LightGBM | 0,2980 ± 0,0179 | 0,076 | 0,2943 | 63,9 min |
| Random Forest | 0,3013 ± 0,0178 | 0,056 | — | — |

Se evaluó además agregar un conglomerado de instituciones (K-medias sobre nueve variables institucionales, K = 4 por silueta) como variable; el RMSE de validación cruzada no cambió (0,2980 en ambos casos) y se descartó.

# A.8 Hiperparámetros y espacio de búsqueda

Optuna con muestreador TPE y semilla fija, poda por mediana (sin poda en los 10 primeros ensayos ni antes del tercer *fold*), 50 ensayos por modelo, objetivo = RMSE promedio de los siete *folds* en escala arcsinh.

**Tabla A.11.** Espacio de búsqueda y óptimo de CatBoost (origen 2026).

| Hiperparámetro | Rango | Óptimo |
|---|---|---:|
| Iteraciones | 200–2.000, paso 100 | 2.000 |
| Tasa de aprendizaje | 0,005–0,15, logarítmica | 0,0376 |
| Profundidad | 4–10 | 7 |
| Regularización L2 | 0,01–30, logarítmica | 1,746 |
| Temperatura de *bagging* | 0–1 | 0,546 |
| *Border count* | 32–255 | 183 |

El número de iteraciones queda en el límite superior del rango, de modo que el óptimo podría estar fuera de él. Semilla 42 en todas las fuentes de aleatoriedad declaradas; no se ha verificado igualdad bit a bit entre equipos. Versiones de `shap`: 0.45.1 en la corrida del origen 2025 y 0.54.1 en la del origen 2026. La elección de CatBoost se mantuvo por continuidad de método entre ambas corridas y no tiene fundamento de desempeño (Sección 4.7 del manuscrito).

# A.9 Desempeño por año y por región: detalles

**Diferencias entre orígenes.** Las cifras OOF de 2019 a 2025 del origen 2026 no coinciden exactamente con las del origen 2025 por tres motivos: la edición 2026 del SIES revisa levemente los años previos, los hiperparámetros se eligieron sobre un *fold* más y el *target encoding* se ajusta con un año más de datos.

**Tabla A.12.** Persistencia por año en el OOF (origen 2026), complemento de la Tabla 5 del manuscrito, contra la matrícula observada.

| Año | WAPE pers. | RelMAE del modelo |
|---:|---:|---:|
| 2019 | 14,30 % | 1,0041 |
| 2020 | 15,74 % | 0,9333 |
| 2021 | 17,08 % | 0,9073 |
| 2022 | 16,35 % | 0,9971 |
| 2023 | 15,64 % | 1,0360 |
| 2024 | 13,96 % | 0,9768 |
| 2025 | 13,23 % | 0,9409 |
| 2026 | 13,09 % | 0,9372 |

**Tabla A.13.** Desempeño por región en el OOF 2019–2026 (origen 2026), matrícula observada.

| Región | n | WAPE | WAPE pers. | Skill | R² | R² pers. | Error agregado |
|---|---:|---:|---:|---:|---:|---:|---:|
| Los Ríos | 2.157 | 11,99 % | 12,54 % | −3,32 % | 0,9657 | 0,9668 | +2,19 % |
| Maule | 3.310 | 12,47 % | 13,12 % | +3,80 % | 0,9668 | 0,9654 | +2,85 % |
| Biobío | 7.943 | 12,60 % | 13,18 % | +1,97 % | 0,9686 | 0,9680 | +0,95 % |
| La Araucanía | 4.853 | 13,19 % | 13,23 % | +0,88 % | 0,9646 | 0,9643 | +1,87 % |
| Valparaíso | 8.937 | 13,59 % | 14,18 % | +18,24 % | 0,9626 | 0,9542 | +1,88 % |
| Arica y Parinacota | 1.533 | 14,65 % | 14,30 % | −9,17 % | 0,9588 | 0,9622 | −0,37 % |
| Metropolitana | 28.312 | 14,78 % | 15,08 % | −4,26 % | 0,9606 | 0,9622 | +2,56 % |
| Coquimbo | 3.009 | 15,07 % | 16,33 % | +11,30 % | 0,9501 | 0,9438 | +1,46 % |
| Antofagasta | 3.046 | 15,57 % | 16,86 % | +15,42 % | 0,9575 | 0,9497 | +3,16 % |
| Ñuble | 2.002 | 15,64 % | 16,14 % | +6,03 % | 0,9488 | 0,9455 | +0,51 % |
| Los Lagos | 2.912 | 16,41 % | 17,44 % | +5,35 % | 0,9431 | 0,9399 | +3,63 % |
| Atacama | 1.202 | 16,57 % | 17,03 % | −1,89 % | 0,9387 | 0,9398 | +1,28 % |
| Magallanes | 848 | 17,69 % | 17,99 % | −2,00 % | 0,9331 | 0,9345 | +1,75 % |
| Tarapacá | 1.992 | 18,69 % | 18,56 % | −3,87 % | 0,8943 | 0,8982 | +3,71 % |
| Lib. Gral. B. O'Higgins | 1.093 | 18,92 % | 24,64 % | +44,16 % | 0,9513 | 0,9127 | +4,43 % |
| Aysén | 313 | 25,50 % | 25,83 % | +9,21 % | 0,8463 | 0,8307 | +9,85 % |

El WAPE del modelo es menor que el de la persistencia en 14 de las 16 regiones, pero el *skill* es negativo en seis: en esas regiones pocos errores grandes dominan el error cuadrático.

![**Figura A.1.** WAPE por región en las predicciones retrospectivas OOF 2019–2026 (origen 2026). Las regiones se ordenan de menor a mayor error. Matrícula observada.](<figuras_es/fig04_wape_por_region.png>)

**Tabla A.14.** Desempeño por modalidad en el *holdout* 2026 (origen 2026), matrícula observada.

| Jornada | Base 2025 | Real 2026 | Predicho 2026 | Crecimiento real | Crecimiento predicho |
|---|---:|---:|---:|---:|---:|
| Diurna | 631.393 | 650.477 | 649.653 | +3,02 % | +2,89 % |
| A Distancia | 38.565 | 43.050 | 46.621 | +11,63 % | +20,89 % |
| Vespertina | 41.498 | 38.165 | 40.031 | −8,03 % | −3,54 % |
| Semipresencial | 8.265 | 8.954 | 9.579 | +8,34 % | +15,90 % |
| Otra | 1.371 | 969 | 1.218 | −29,32 % | −11,17 % |

El modelo prolonga la tendencia de las modalidades no diurnas y no captura sus inflexiones; con la jornada como indicadora sin interacción temporal, no tiene con qué hacer otra cosa. El agregado acierta porque los errores se compensan.

# A.10 Explicabilidad: resultados complementarios

**Tabla A.15.** Importancia SHAP (media del valor absoluto) de las cinco variables principales.

| # | Variable | Origen 2026 | Origen 2025 |
|---:|---|---:|---:|
| 1 | Nombre de carrera (*target encoding*) | 0,0533 | 0,0546 |
| 2 | Condición de estudiante nuevo | 0,0488 | 0,0514 |
| 3 | Rezago de la matrícula | 0,0364 | 0,0394 |
| 4 | Jornada vespertina | 0,0299 | 0,0289 |
| 5 | Participación rezagada en la matrícula regional de la carrera | 0,0229 | 0,0249 |

*Nota:* origen 2026, sobre las 92.036 filas exportadas (retrospectivas, de base del rezago y de pronóstico). En el origen 2025, restringido a las celdas del pronóstico 2026 con dato oficial, el orden fue idéntico (0,0528; 0,0491; 0,0409; 0,0305; 0,0291). El rezago aparece tercero en parte por escala: entra en logaritmo y su efecto principal está en la reconstrucción del nivel, no en la tasa. Las variables macroeconómicas y las tres variables con matrícula contemporánea no figuran entre las quince más influyentes. No hay relación utilizable entre la magnitud de las contribuciones de una celda y su error: SHAP no es una señal de confianza.

![**Figura A.2.** Distribución de las contribuciones SHAP de las cinco variables más influyentes (origen 2026). La línea discontinua marca contribución nula. Los rótulos de las variables corresponden a los nombres internos de columna. Atribuciones del modelo final del origen 2026 (entrenado con 2018–2026) calculadas sobre las filas OOF 2019–2026, es decir, dentro de la muestra; no son atribuciones de los modelos OOF.](<figuras_es/fig10_shap_top5_distribucion.png>)

![**Figura A.3.** Promedio del valor absoluto de las contribuciones SHAP por subgrupo de condición, jornada y género. Atribuciones del modelo final del origen 2026 (entrenado con 2018–2026) calculadas sobre las filas OOF 2019–2026, es decir, dentro de la muestra; no son atribuciones de los modelos OOF.](<figuras_es/fig11_shap_por_subgrupo.png>)

![**Figura A.4.** Contribución SHAP media, con signo, por subgrupo de condición, jornada y género; la línea marca contribución nula. A diferencia de la Figura A.3, las contribuciones de signo opuesto se compensan. Atribuciones del modelo final del origen 2026 (entrenado con 2018–2026) calculadas sobre las filas OOF 2019–2026, es decir, dentro de la muestra; no son atribuciones de los modelos OOF.](<figuras_es/fig11b_shap_por_subgrupo_con_signo.png>)

![**Figura A.5.** Descomposición SHAP de dos celdas OOF: la primera, en el orden del archivo, con matrícula de al menos 100 y error absoluto no mayor que 2 («bien predicha»), y la de mayor error absoluto («mal predicha»). Los títulos identifican institución, carrera, región, jornada, género y condición; son datos públicos agregados, sin personas. Atribuciones del modelo final del origen 2026 (entrenado con 2018–2026) calculadas sobre las filas OOF 2019–2026, es decir, dentro de la muestra; no son atribuciones de los modelos OOF.](<figuras_es/fig12_caso_estudio_shap.png>)

# A.11 Intervalos conformes: detalles

**Factores de banda.** El factor de banda por nivel de agregación (origen 2025) es de ×0,72–×1,09 en N2 y de ×0,49–×1,54 en N8. Dentro de un nivel, la estratificación por tamaño produce la monotonía esperada: en N3, ×0,34–×1,38 para grupos de menos de 100 estudiantes frente a ×0,87–×1,09 para los de más de 2.000. Los estratos de agregados usan los tramos de tamaño <100, 100–500, 500–2.000 y >2.000, y la banda es $[\hat{y}e^{-q_{\text{hi}}}, \hat{y}e^{-q_{\text{lo}}}]$, con $q$ los cuantiles conformes de $\log(\hat{y}/y)$.

**Cobertura por nivel en la validación 2026 (origen 2025).** 98,1 % (N2), 96,6 % (N3), 94,8 % (N4), 91,8 % (N5), 92,8 % (N6), 92,6 % (N7) y 92,3 % (N8, por grupo), con objetivo de 90 %. La cobertura por celda es la de la Tabla 10 del manuscrito (92,53 %).

**Origen 2026 y pronósticos 2027.** Contra la matrícula observada, las bandas calibradas anteriormente con residuos de la tasa recortada cubren el 92,26 % de las celdas del *holdout* 2026 (ancho mediano 36,5); recalibradas con residuos observados (OOF 2019–2025), el 92,49 % (ancho mediano 36,6). Las bandas que se congelan con los pronósticos 2027 se calibran con los residuos OOF 2019–2026 observados de cada modelo (Tabla A.39). La banda mediana por institución del modelo principal recalibrado mide el 20,62 % del pronóstico, y el rango nacional no conforme va de 719.308 a 777.914, construido con los errores agregados OOF contra la matrícula observada, de −2,17 % (2021) a +5,80 % (2022). Con la calibración anterior, esas cifras eran 20,4 % y 716.850 a 775.499.

**Calibrar para medir y calibrar para publicar.** Para medir la cobertura se usan sólo residuos de años anteriores al evaluado; para emitir bandas publicadas se usa todo el OOF disponible. Si un estrato tiene menos de 30 residuos se usa la banda del nivel completo, y si tampoco alcanza, no se emite intervalo.

# A.12 Figuras complementarias

![**Figura A.6.** Distribución de los residuos (matrícula observada menos pronosticada) en el OOF 2019–2026, recortada en ±200 (izquierda), y gráfico cuantil-cuantil frente a la normal (derecha). Las colas pesadas justifican no suponer normalidad en los intervalos. Matrícula observada.](<figuras_es/fig01_distribucion_residuos.png>)

![**Figura A.7.** Matrícula pronosticada frente a observada en los ocho niveles de la cascada de agregación, OOF 2019–2026 (origen 2026), con la matrícula observada. El número de grupos del nivel N8 (73.349) difiere del número de filas OOF (73.462) porque hay 113 filas sobrantes en 88 celdas (dos instituciones; 2019–2021 y 2024), originadas en varias sedes en una misma región o en versiones del plan, que heredan el total de la celda; véase A.13.](<figuras_es/fig05_macro_a_micro.png>)

![**Figura A.8.** Calibración por decil de tamaño definido por el rezago (información disponible al pronosticar), OOF 2019–2026 del origen 2026 (73.462 filas, incluye el *holdout* 2026): matrícula media observada y pronosticada (izquierda) y sesgo relativo (real − pronosticado)/real (derecha; negativo = sobrepredicción). Sesgo de Q1 a Q10: +1,25 %; +0,25 %; −1,70 %; −1,66 %; −1,64 %; −2,48 %; −2,40 %; −2,78 %; −1,87 %; −2,57 %, es decir, una sobrepredicción leve y pareja de 1,6 % a 2,8 % desde el tercer decil, que refleja la sobrepredicción agregada del OOF y no un problema de calibración por tamaño.](<figuras_es/fig07_calibracion.png>)

![**Figura A.9.** La misma calibración con los deciles definidos por la matrícula observada. Sesgo (real − pronosticado)/real de Q1 a Q10: −94,44 %; −23,77 %; −10,15 %; −4,46 %; −1,36 %; −0,74 %; −0,23 %; −0,11 %; −0,32 %; −0,43 %. El sesgo extremo de los deciles inferiores es regresión a la media, porque se condiciona en el resultado.](<figuras_es/fig07b_calibracion_deciles_observados.png>)

# A.13 Inconsistencias conocidas en el material de apoyo

Se declaran para transparencia; ninguna altera las cifras del manuscrito.

1. **Convención de signo y base del error agregado.** El error agregado se define como pronóstico menos valor observado. Para 2021, contra la matrícula observada, es −2,17 % (654.899 pronosticadas frente a 669.403 observadas; Tabla 5 y Figura 3 del manuscrito); contra el valor reconstruido con la tasa recortada era −1,86 %.
2. **Filas duplicadas en la llave fina.** En el OOF hay 113 filas sobrantes en 88 celdas, de dos instituciones (2019–2021 y 2024), originadas en varias sedes dentro de una misma región o en versiones del plan; heredan el total de la celda. El *holdout* 2026 y los pronósticos 2027 no están afectados. La sensibilidad sin esas filas, con la matrícula observada, está en la nota de la Tabla A.23. Se corregirá en la siguiente versión metodológica. \[PENDIENTE: confirmación del autor para incluir esta nota\]
3. **Metadatos del modelo.** Los metadatos del modelo del origen 2026 registraban rótulos heredados de la corrida anterior: el número de *folds* (5 en lugar de los 7 ejecutados) y los rótulos del holdout y de los supuestos del pronóstico. Se corrigieron antes del congelamiento, sin cambiar ningún valor numérico ni las predicciones.
4. **Figuras.** Las figuras se regeneraron con la matrícula observada, con separador decimal en coma y rótulos en español; la Figura 3 del manuscrito usa la matrícula observada de 2018 (653.163) en lugar de la suma de rezagos de ese año, y la regresión lineal de la Figura 5 usa la misma serie corregida (−1,53 %).

# A.14 Protocolo de evaluación y congelamiento de los pronósticos 2027

Estatus: *ex ante*, congelado. El protocolo (versión 2.2) se aprobó y se congeló el 20 de noviembre de 2026 junto con los seis pronósticos, antes de la publicación oficial de la matrícula 2027. Todo análisis que no figure en él se reportará como no planificado.

1. **Pronósticos congelados:** C49 (761.058, sin cambios, con su base declarada: +2,62 % sobre 741.615 y 75 celdas con rezago recortado), Crez (767.934; +3,55 %), L49 (760.672; +2,57 %) y Lrez (768.499; +3,63 %) —todos con bandas al 90 % del conformal estratificado recalibradas sobre sus residuos OOF 2019–2026 observados—, la persistencia (F0) y Comb nacional (FN, sólo N1). Universo: 9.069 celdas.
2. **Dato real:** la primera publicación de la base de matriculados 2027 del SIES, descargada dentro de los 30 días siguientes y con su huella SHA-256 registrada; reconstruida con las reglas de ingesta del panel; **sin winsorización ni ajuste alguno**; con control previo contra el total del informe oficial.
3. **Emparejamiento:** principal por llave de celda con nombre de carrera; secundario por código de carrera; las celdas pronosticadas sin matrícula 2027 y los programas nuevos quedan fuera del análisis principal, y se informan su número y matrícula, junto con la cobertura de la matrícula 2027.
4. **Métricas y niveles:** N1–N8 por suma ascendente; WAPE, RelMAE frente a F0, *skill* frente a F0, porcentaje dentro de ±10 % y error agregado; para los intervalos, cobertura con intervalo de confianza binomial al 95 %, ancho mediano, IS ($\alpha = 0{,}10$), MSIS y, como referencia, un conformal sin estratos.
5. **Hipótesis:** DM entre grupos con error estándar por clúster de institución, bilaterales, $\alpha = 0{,}05$, pérdida principal absoluta y secundaria cuadrática, sin corrección por multiplicidad y reportadas cualquiera sea su resultado.

**Tabla A.16.** Hipótesis preespecificadas del protocolo de evaluación 2027.

| ID | Pregunta | Contraste | Nivel principal | Niveles secundarios |
|---|---|---|---|---|
| H1 | ¿Los modelos superan a la persistencia? | C49 − F0, Crez − F0, L49 − F0 y Lrez − F0 | N8 | N2, N5 |
| H2 | ¿Aportan las variables exógenas? | C49 − Crez y L49 − Lrez | N8 y N2 (ambos principales) | N5 |
| H3 | ¿Importa el algoritmo? | C49 − L49 y Crez − Lrez | N8 | N2, N5 |
| H4 | Total nacional | Error agregado de los cuatro modelos, F0 y FN | N1 | — (descriptivo: un solo año) |
| H5 | Calibración de las bandas | Cobertura de los cuatro modelos frente al 90 % nominal | N8 | N2–N7 |

La lectura de H2 se fija de antemano: si en N8 las exógenas no mejoran con ningún algoritmo, se repite el resultado de 2026; si mejoran en N2 con ambos, el de 2019–2025; cualquier otra combinación se reporta como tal, sin reinterpretarla. El contraste es concreto: C49 y L49 pronostican +2,62 % y +2,57 % sobre 741.615, y Crez y Lrez +3,55 % y +3,63 %, con la diferencia concentrada en los estudiantes nuevos (−0,54 % y −0,07 % frente a +1,82 % y +2,93 %).

6. **Criterios de fracaso y de calibración:** un modelo no supera a la persistencia si su RelMAE en N8 es mayor o igual que uno. Las bandas se clasifican por modelo y nivel, con el intervalo de Wilson, con un criterio asimétrico: subcobertura si la cobertura es menor que 88 %, calibradas entre 88 % y 95 %, y conservadoras por encima de 95 %. El criterio se fijó tras una prueba en seco del programa de evaluación sobre 2026 y antes del congelamiento; en esa prueba, los cuatro modelos quedaron calibrados en N8 (C49 92,49 %, Crez 93,25 %, L49 92,25 %, Lrez 92,31 %), y en N2–N7 (descriptivo) Crez quedó conservador en N2–N4, L49 en N2 y Lrez en N3. Ningún resultado de 2027 modifica los pronósticos congelados.
7. **Ejecución:** un programa de evaluación congelado en el mismo paquete, probado en seco sobre el *holdout* 2026; resultados publicados dentro de los 60 días siguientes a la publicación del SIES, con la huella del archivo real usado y la lista de desvíos.
8. **Congelamiento:** realizado el 20 de noviembre de 2026 mediante una etiqueta anotada en un repositorio público con las huellas SHA-256 de las predicciones, el protocolo de evaluación y el script de evaluación \[identificadores omitidos para la revisión doble anónima; se entregan al editor en la carta de presentación\]. Si aparece un defecto después, se crea una versión nueva y se reportan ambas.

El depósito con DOI se informará en la versión aceptada. \[PENDIENTE: DOI de Zenodo\]

# A.15 Evaluación contra la matrícula observada: diagnóstico de la winsorización

El objetivo de entrenamiento recorta la tasa de crecimiento a sus percentiles 1 y 99; una versión anterior de la evaluación reconstruía también el valor «real» con esa tasa recortada. La tabla compara, por año, el valor reconstruido con el observado (suma del SIES procesado sobre la llave fina de la celda). Las predicciones no cambian. En el *holdout* 2026, el valor observado de las 9.069 celdas suma 741.615, igual que esas celdas en el SIES crudo.

**Tabla A.17.** Filas recortadas y diferencia entre el valor reconstruido con la tasa recortada y el valor observado, por año.

| Año | Filas | Recortadas | Con real distinto | Real winsorizado | Real observado | Diferencia | Diferencia % |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 9.505 | 217 | 190 | 651.273 | 653.163 | +1.890 | +0,29 % |
| 2019 | 9.424 | 172 | 148 | 654.320 | 654.495 | +175 | +0,03 % |
| 2020 | 9.321 | 159 | 130 | 637.304 | 637.998 | +694 | +0,11 % |
| 2021 | 9.230 | 206 | 170 | 667.325 | 669.403 | +2.078 | +0,31 % |
| 2022 | 9.161 | 246 | 206 | 660.215 | 662.479 | +2.264 | +0,34 % |
| 2023 | 9.038 | 262 | 218 | 669.407 | 670.918 | +1.511 | +0,23 % |
| 2024 | 9.176 | 194 | 165 | 691.894 | 692.653 | +759 | +0,11 % |
| 2025 | 9.043 | 157 | 128 | 711.271 | 711.941 | +670 | +0,09 % |
| 2026 | 9.069 | 90 | 75 | 740.318 | 741.615 | +1.297 | +0,17 % |

**Tabla A.18.** Desempeño global antes (valor recortado) y después (valor observado).

| Conjunto | Versión | n | R² | R² pers. | WAPE | WAPE pers. | Skill | RelMAE | Sesgo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF retrospectivo 2019-2026 | antes (real winsorizado) | 73.462 | 0,9652 | 0,9653 | 14,13 % | 14,63 % | −0,47 % | 0,9656 | +2,40 % |
| OOF retrospectivo 2019-2026 | después (real observado) | 73.462 | 0,9617 | 0,9616 | 14,38 % | 14,88 % | +0,09 % | 0,9662 | +2,23 % |
| Holdout 2026 | antes (real winsorizado) | 9.069 | 0,9733 | 0,9689 | 12,09 % | 12,91 % | +14,20 % | 0,9363 | +0,92 % |
| Holdout 2026 | después (real observado) | 9.069 | 0,9710 | 0,9666 | 12,27 % | 13,09 % | +13,21 % | 0,9372 | +0,74 % |
| Holdout 2025, origen 2025 | antes (real winsorizado) | 9.041 | 0,9794 | 0,9735 | 12,24 % | 13,12 % | +22,46 % | 0,9327 | −0,20 % |
| Holdout 2025, origen 2025 | después (real observado) | 9.041 | 0,9782 | 0,9717 | 12,35 % | 13,23 % | +22,87 % | 0,9333 | −0,29 % |

**Tabla A.19.** Desempeño anual del OOF (origen 2026) antes y después.

| Año | Versión | Real | Predicho | WAPE | WAPE pers. | R² | Skill | RelMAE | Error agregado |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | antes | 654.320 | 677.096 | 14,12 % | 14,06 % | 0,9543 | −38,58 % | 1,0042 | +3,48 % |
| 2019 | después | 654.495 | 677.096 | 14,36 % | 14,30 % | 0,9499 | −34,89 % | 1,0041 | +3,45 % |
| 2020 | antes | 637.304 | 666.925 | 14,46 % | 15,51 % | 0,9428 | −13,48 % | 0,9323 | +4,65 % |
| 2020 | después | 637.998 | 666.925 | 14,69 % | 15,74 % | 0,9359 | −13,71 % | 0,9333 | +4,53 % |
| 2021 | antes | 667.325 | 654.899 | 15,13 % | 16,71 % | 0,9674 | +21,59 % | 0,9049 | −1,86 % |
| 2021 | después | 669.403 | 654.899 | 15,50 % | 17,08 % | 0,9625 | +19,99 % | 0,9073 | −2,17 % |
| 2022 | antes | 660.215 | 700.931 | 15,91 % | 15,96 % | 0,9578 | −5,16 % | 0,9970 | +6,17 % |
| 2022 | después | 662.479 | 700.931 | 16,31 % | 16,35 % | 0,9527 | −2,98 % | 0,9971 | +5,80 % |
| 2023 | antes | 669.407 | 702.750 | 15,92 % | 15,35 % | 0,9617 | −12,08 % | 1,0367 | +4,98 % |
| 2023 | después | 670.918 | 702.750 | 16,20 % | 15,64 % | 0,9584 | −8,97 % | 1,0360 | +4,74 % |
| 2024 | antes | 691.894 | 700.168 | 13,46 % | 13,78 % | 0,9740 | +3,07 % | 0,9766 | +1,20 % |
| 2024 | después | 692.653 | 700.168 | 13,63 % | 13,96 % | 0,9725 | +3,68 % | 0,9768 | +1,09 % |
| 2025 | antes | 711.271 | 712.759 | 12,34 % | 13,12 % | 0,9790 | +20,53 % | 0,9404 | +0,21 % |
| 2025 | después | 711.941 | 712.759 | 12,45 % | 13,23 % | 0,9777 | +21,08 % | 0,9409 | +0,11 % |
| 2026 | antes | 740.318 | 747.102 | 12,09 % | 12,91 % | 0,9733 | +14,20 % | 0,9363 | +0,92 % |
| 2026 | después | 741.615 | 747.102 | 12,27 % | 13,09 % | 0,9710 | +13,21 % | 0,9372 | +0,74 % |

**Tabla A.20.** Cascada del *holdout* 2026 antes y después.

| Nivel | Versión | Grupos | WAPE | WAPE pers. | R² | R² pers. | Skill | RelMAE | ± 10 % | ± 10 % pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | antes | 1 | 0,92 % | 2,60 % | — | — | +87,55 % | 0,3529 | 100,00 % | 100,00 % |
| N2 + Institución | antes | 53 | 2,60 % | 3,49 % | 0,9976 | 0,9958 | +43,03 % | 0,7460 | 90,57 % | 92,45 % |
| N3 + Área | antes | 413 | 4,30 % | 4,89 % | 0,9970 | 0,9955 | +34,20 % | 0,8795 | 80,87 % | 77,48 % |
| N4 + Región | antes | 647 | 4,68 % | 5,15 % | 0,9957 | 0,9948 | +16,90 % | 0,9090 | 76,20 % | 74,34 % |
| N5 + Carrera | antes | 2.739 | 8,24 % | 8,63 % | 0,9827 | 0,9811 | +8,60 % | 0,9545 | 57,36 % | 56,33 % |
| N6 + Condición | antes | 4.798 | 10,05 % | 10,65 % | 0,9794 | 0,9768 | +11,25 % | 0,9436 | 49,33 % | 48,06 % |
| N7 + Género | antes | 8.390 | 11,53 % | 12,13 % | 0,9754 | 0,9741 | +5,09 % | 0,9508 | 42,62 % | 41,81 % |
| N8 + Jornada | antes | 9.069 | 12,09 % | 12,91 % | 0,9733 | 0,9689 | +14,20 % | 0,9363 | 41,59 % | 40,56 % |
| N1 Nacional | después | 1 | 0,74 % | 2,77 % | — | — | +92,85 % | 0,2674 | 100,00 % | 100,00 % |
| N2 + Institución | después | 53 | 2,76 % | 3,64 % | 0,9975 | 0,9950 | +49,51 % | 0,7578 | 88,68 % | 92,45 % |
| N3 + Área | después | 413 | 4,44 % | 5,04 % | 0,9968 | 0,9949 | +37,42 % | 0,8799 | 80,15 % | 76,76 % |
| N4 + Región | después | 647 | 4,78 % | 5,30 % | 0,9955 | 0,9941 | +24,45 % | 0,9018 | 75,58 % | 73,42 % |
| N5 + Carrera | después | 2.739 | 8,42 % | 8,81 % | 0,9812 | 0,9796 | +7,86 % | 0,9549 | 57,21 % | 56,26 % |
| N6 + Condición | después | 4.798 | 10,22 % | 10,83 % | 0,9777 | 0,9751 | +10,40 % | 0,9443 | 49,33 % | 48,02 % |
| N7 + Género | después | 8.390 | 11,71 % | 12,31 % | 0,9732 | 0,9719 | +4,47 % | 0,9517 | 42,59 % | 41,81 % |
| N8 + Jornada | después | 9.069 | 12,27 % | 13,09 % | 0,9710 | 0,9666 | +13,21 % | 0,9372 | 41,59 % | 40,56 % |

# A.16 Referentes por serie y modelo global: tablas completas

**Construcción de las series.** En el origen $Y-1$, el valor de la serie en $Y-1$ es el rezago de la celda en $Y$ (así la persistencia es exactamente el referente publicado); los valores en $s \le Y-2$ son la matrícula de la celda en $s$ o, si la celda no estaba en el panel en $s$, su rezago en $s+1$; la serie se corta en el primer año sin dato, y el rezago de 2018 da el valor de 2017. Con menos de tres observaciones, todos los métodos caen a la persistencia. Métodos (`statsforecast` 2.1.1): Naive (control, idéntico a la persistencia y omitido), RWD, AutoETS sin estacionalidad (incluye amortiguado), AutoARIMA, Theta estándar y Comb (media de ETS, ARIMA y Theta); predicciones truncadas en cero; niveles por suma ascendente.

**Tabla A.21.** Celdas que caen a la persistencia por tener menos de tres observaciones.

| Año / conjunto | Celdas | Menos de 3 obs. |
|---|---:|---:|
| 2019 | 9.424 | 9.424 |
| 2020 | 9.321 | 1.275 |
| 2021 | 9.230 | 1.224 |
| 2022 | 9.161 | 1.240 |
| 2023 | 9.038 | 1.140 |
| 2024 | 9.176 | 1.167 |
| 2025 | 9.043 | 1.141 |
| 2026 | 9.069 | 1.126 |
| Validación 2026 | 8.729 | 580 |

**Tabla A.22.** Tiempo de cómputo (un ajuste por serie y origen; 63.794 series).

| Método | Segundos |
|---|---:|
| Naive | 1,0 |
| RWD | 1,3 |
| ETS | 85,9 |
| ARIMA | 461,6 |
| Theta | 4,5 |
| Global LightGBM | 114,9 |

**Tabla A.23.** Referentes por nivel con la matrícula observada: OOF 2019–2025 y *holdout* 2026 (N1, N2, N5 y N8). «Global» = Lrez.

| Conjunto | Nivel | Método | WAPE | Skill | RelMAE | ± 10 % |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N1 Nacional | Persistencia | 1,87 % | +0,00 % | 1,0000 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | Persistencia | 4,66 % | +0,00 % | 1,0000 | 80,05 % |
| OOF 2019-2025 | N5 + Carrera | Persistencia | 10,57 % | +0,00 % | 1,0000 | 48,12 % |
| OOF 2019-2025 | N8 + Jornada | Persistencia | 15,16 % | +0,00 % | 1,0000 | 36,49 % |
| OOF 2019-2025 | N1 Nacional | RWD | 2,35 % | −56,18 % | 1,2552 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | RWD | 4,24 % | +34,16 % | 0,9092 | 80,05 % |
| OOF 2019-2025 | N5 + Carrera | RWD | 10,30 % | −4,31 % | 0,9751 | 48,35 % |
| OOF 2019-2025 | N8 + Jornada | RWD | 15,68 % | −13,85 % | 1,0341 | 34,61 % |
| OOF 2019-2025 | N1 Nacional | ETS | 1,71 % | +10,34 % | 0,9153 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | ETS | 4,89 % | −4,89 % | 1,0501 | 79,30 % |
| OOF 2019-2025 | N5 + Carrera | ETS | 11,21 % | −9,61 % | 1,0605 | 46,09 % |
| OOF 2019-2025 | N8 + Jornada | ETS | 15,76 % | −7,37 % | 1,0393 | 35,42 % |
| OOF 2019-2025 | N1 Nacional | ARIMA | 1,29 % | +55,65 % | 0,6889 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | ARIMA | 5,70 % | −52,54 % | 1,2238 | 76,56 % |
| OOF 2019-2025 | N5 + Carrera | ARIMA | 13,75 % | −72,53 % | 1,3008 | 40,00 % |
| OOF 2019-2025 | N8 + Jornada | ARIMA | 18,61 % | −68,73 % | 1,2275 | 31,50 % |
| OOF 2019-2025 | N1 Nacional | Theta | 1,56 % | +25,76 % | 0,8319 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | Theta | 4,54 % | +14,37 % | 0,9742 | 79,80 % |
| OOF 2019-2025 | N5 + Carrera | Theta | 10,91 % | −2,44 % | 1,0322 | 46,39 % |
| OOF 2019-2025 | N8 + Jornada | Theta | 15,70 % | −5,39 % | 1,0354 | 34,98 % |
| OOF 2019-2025 | N1 Nacional | Comb | 1,48 % | +36,03 % | 0,7929 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | Comb | 4,97 % | −8,70 % | 1,0657 | 79,30 % |
| OOF 2019-2025 | N5 + Carrera | Comb | 11,56 % | −13,97 % | 1,0938 | 44,79 % |
| OOF 2019-2025 | N8 + Jornada | Comb | 16,03 % | −12,16 % | 1,0576 | 34,64 % |
| OOF 2019-2025 | N1 Nacional | Global | 3,10 % | −229,09 % | 1,6572 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | Global | 4,92 % | +15,00 % | 1,0560 | 76,06 % |
| OOF 2019-2025 | N5 + Carrera | Global | 10,03 % | +1,18 % | 0,9491 | 49,46 % |
| OOF 2019-2025 | N8 + Jornada | Global | 14,27 % | +5,38 % | 0,9415 | 37,50 % |
| OOF 2019-2025 | N1 Nacional | CatBoost | 3,08 % | −161,50 % | 1,6451 | 100,00 % |
| OOF 2019-2025 | N2 + Institución | CatBoost | 4,69 % | +22,81 % | 1,0058 | 78,55 % |
| OOF 2019-2025 | N5 + Carrera | CatBoost | 10,14 % | −1,19 % | 0,9592 | 48,67 % |
| OOF 2019-2025 | N8 + Jornada | CatBoost | 14,71 % | −1,86 % | 0,9702 | 36,26 % |
| Holdout 2026 | N1 Nacional | Persistencia | 2,77 % | +0,00 % | 1,0000 | 100,00 % |
| Holdout 2026 | N2 + Institución | Persistencia | 3,64 % | +0,00 % | 1,0000 | 92,45 % |
| Holdout 2026 | N5 + Carrera | Persistencia | 8,81 % | +0,00 % | 1,0000 | 56,26 % |
| Holdout 2026 | N8 + Jornada | Persistencia | 13,09 % | +0,00 % | 1,0000 | 40,56 % |
| Holdout 2026 | N1 Nacional | RWD | 0,85 % | +90,58 % | 0,3070 | 100,00 % |
| Holdout 2026 | N2 + Institución | RWD | 2,85 % | +48,46 % | 0,7829 | 88,68 % |
| Holdout 2026 | N5 + Carrera | RWD | 8,69 % | +3,04 % | 0,9864 | 54,95 % |
| Holdout 2026 | N8 + Jornada | RWD | 13,27 % | +3,17 % | 1,0141 | 38,80 % |
| Holdout 2026 | N1 Nacional | ETS | 2,54 % | +15,86 % | 0,9173 | 100,00 % |
| Holdout 2026 | N2 + Institución | ETS | 3,76 % | −8,90 % | 1,0333 | 90,57 % |
| Holdout 2026 | N5 + Carrera | ETS | 10,31 % | −10,20 % | 1,1698 | 49,65 % |
| Holdout 2026 | N8 + Jornada | ETS | 14,46 % | −9,05 % | 1,1050 | 37,57 % |
| Holdout 2026 | N1 Nacional | ARIMA | 1,96 % | +49,98 % | 0,7073 | 100,00 % |
| Holdout 2026 | N2 + Institución | ARIMA | 3,91 % | +3,40 % | 1,0731 | 88,68 % |
| Holdout 2026 | N5 + Carrera | ARIMA | 11,28 % | −46,61 % | 1,2799 | 47,35 % |
| Holdout 2026 | N8 + Jornada | ARIMA | 15,69 % | −42,00 % | 1,1988 | 35,96 % |
| Holdout 2026 | N1 Nacional | Theta | 1,46 % | +72,09 % | 0,5283 | 100,00 % |
| Holdout 2026 | N2 + Institución | Theta | 3,39 % | +25,70 % | 0,9310 | 88,68 % |
| Holdout 2026 | N5 + Carrera | Theta | 9,67 % | −2,45 % | 1,0968 | 50,93 % |
| Holdout 2026 | N8 + Jornada | Theta | 13,86 % | −3,18 % | 1,0589 | 37,96 % |
| Holdout 2026 | N1 Nacional | Comb | 1,99 % | +48,50 % | 0,7176 | 100,00 % |
| Holdout 2026 | N2 + Institución | Comb | 3,61 % | +10,42 % | 0,9924 | 88,68 % |
| Holdout 2026 | N5 + Carrera | Comb | 10,03 % | −10,73 % | 1,1377 | 50,68 % |
| Holdout 2026 | N8 + Jornada | Comb | 14,08 % | −8,18 % | 1,0754 | 38,46 % |
| Holdout 2026 | N1 Nacional | Global | 0,80 % | +91,54 % | 0,2908 | 100,00 % |
| Holdout 2026 | N2 + Institución | Global | 2,65 % | +43,57 % | 0,7276 | 94,34 % |
| Holdout 2026 | N5 + Carrera | Global | 7,98 % | +15,87 % | 0,9059 | 59,66 % |
| Holdout 2026 | N8 + Jornada | Global | 11,60 % | +23,42 % | 0,8859 | 43,26 % |
| Holdout 2026 | N1 Nacional | CatBoost | 0,74 % | +92,85 % | 0,2674 | 100,00 % |
| Holdout 2026 | N2 + Institución | CatBoost | 2,76 % | +49,51 % | 0,7578 | 88,68 % |
| Holdout 2026 | N5 + Carrera | CatBoost | 8,42 % | +7,86 % | 0,9549 | 57,21 % |
| Holdout 2026 | N8 + Jornada | CatBoost | 12,27 % | +13,21 % | 0,9372 | 41,59 % |

*Nota:* las tablas N1–N8 completas con el valor observado están en el archivo de resultados del autor. Los niveles N3, N4, N6 y N7 están en la Tabla A.24. Sensibilidad sin las 113 filas duplicadas (OOF 2019–2025): N2 persistencia 4,65 %, *skill* +0,00 %; N8 persistencia 15,15 %; N2 global 4,91 %, *skill* +15,17 %; N8 global 14,26 %, *skill* +5,52 %; N2 CatBoost 4,68 %, *skill* +22,74 %; N8 CatBoost 14,70 %, *skill* −2,06 %.

**Tabla A.24.** Referentes por nivel con la matrícula observada: OOF 2019–2025 y *holdout* 2026 (N3, N4, N6 y N7). «Global» = Lrez.

| Conjunto | Nivel | Método | WAPE | Skill | RelMAE | ± 10 % |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N3 + Área | Persistencia | 6,43 % | +0,00 % | 1,0000 | 68,72 % |
| OOF 2019-2025 | N4 + Región | Persistencia | 6,99 % | +0,00 % | 1,0000 | 58,85 % |
| OOF 2019-2025 | N6 + Condición | Persistencia | 12,99 % | +0,00 % | 1,0000 | 42,04 % |
| OOF 2019-2025 | N7 + Género | Persistencia | 14,42 % | +0,00 % | 1,0000 | 37,78 % |
| OOF 2019-2025 | N3 + Área | RWD | 6,09 % | +17,22 % | 0,9472 | 68,92 % |
| OOF 2019-2025 | N4 + Región | RWD | 6,66 % | +1,59 % | 0,9521 | 59,66 % |
| OOF 2019-2025 | N6 + Condición | RWD | 13,21 % | −9,28 % | 1,0163 | 40,81 % |
| OOF 2019-2025 | N7 + Género | RWD | 14,88 % | −11,37 % | 1,0319 | 35,92 % |
| OOF 2019-2025 | N3 + Área | ETS | 6,77 % | −6,45 % | 1,0537 | 67,15 % |
| OOF 2019-2025 | N4 + Región | ETS | 7,36 % | −7,57 % | 1,0534 | 57,03 % |
| OOF 2019-2025 | N6 + Condición | ETS | 13,58 % | −7,15 % | 1,0452 | 40,58 % |
| OOF 2019-2025 | N7 + Género | ETS | 14,99 % | −6,97 % | 1,0396 | 36,68 % |
| OOF 2019-2025 | N3 + Área | ARIMA | 8,18 % | −58,14 % | 1,2732 | 59,84 % |
| OOF 2019-2025 | N4 + Región | ARIMA | 8,94 % | −67,39 % | 1,2785 | 51,05 % |
| OOF 2019-2025 | N6 + Condición | ARIMA | 16,07 % | −63,56 % | 1,2368 | 36,28 % |
| OOF 2019-2025 | N7 + Género | ARIMA | 17,70 % | −67,62 % | 1,2273 | 32,62 % |
| OOF 2019-2025 | N3 + Área | Theta | 6,52 % | +4,59 % | 1,0147 | 68,29 % |
| OOF 2019-2025 | N4 + Región | Theta | 7,10 % | −0,78 % | 1,0153 | 57,61 % |
| OOF 2019-2025 | N6 + Condición | Theta | 13,46 % | −2,41 % | 1,0362 | 40,27 % |
| OOF 2019-2025 | N7 + Género | Theta | 14,92 % | −3,37 % | 1,0343 | 36,22 % |
| OOF 2019-2025 | N3 + Área | Comb | 6,96 % | −12,40 % | 1,0820 | 65,54 % |
| OOF 2019-2025 | N4 + Región | Comb | 7,57 % | −14,26 % | 1,0832 | 55,85 % |
| OOF 2019-2025 | N6 + Condición | Comb | 13,86 % | −10,31 % | 1,0667 | 40,05 % |
| OOF 2019-2025 | N7 + Género | Comb | 15,25 % | −10,81 % | 1,0570 | 35,90 % |
| OOF 2019-2025 | N3 + Área | Global | 6,40 % | +8,80 % | 0,9963 | 68,92 % |
| OOF 2019-2025 | N4 + Región | Global | 6,89 % | −6,26 % | 0,9860 | 60,16 % |
| OOF 2019-2025 | N6 + Condición | Global | 12,27 % | +3,91 % | 0,9440 | 43,12 % |
| OOF 2019-2025 | N7 + Género | Global | 13,61 % | +4,92 % | 0,9438 | 38,80 % |
| OOF 2019-2025 | N3 + Área | CatBoost | 6,23 % | +13,13 % | 0,9692 | 68,69 % |
| OOF 2019-2025 | N4 + Región | CatBoost | 6,81 % | −9,52 % | 0,9737 | 60,31 % |
| OOF 2019-2025 | N6 + Condición | CatBoost | 12,65 % | −2,43 % | 0,9733 | 41,88 % |
| OOF 2019-2025 | N7 + Género | CatBoost | 14,03 % | −1,90 % | 0,9729 | 37,49 % |
| Holdout 2026 | N3 + Área | Persistencia | 5,04 % | +0,00 % | 1,0000 | 76,76 % |
| Holdout 2026 | N4 + Región | Persistencia | 5,30 % | +0,00 % | 1,0000 | 73,42 % |
| Holdout 2026 | N6 + Condición | Persistencia | 10,83 % | +0,00 % | 1,0000 | 48,02 % |
| Holdout 2026 | N7 + Género | Persistencia | 12,31 % | +0,00 % | 1,0000 | 41,81 % |
| Holdout 2026 | N3 + Área | RWD | 4,47 % | +36,65 % | 0,8874 | 77,24 % |
| Holdout 2026 | N4 + Región | RWD | 4,88 % | +33,20 % | 0,9211 | 73,11 % |
| Holdout 2026 | N6 + Condición | RWD | 10,89 % | +1,11 % | 1,0057 | 47,96 % |
| Holdout 2026 | N7 + Género | RWD | 12,58 % | −1,20 % | 1,0220 | 39,93 % |
| Holdout 2026 | N3 + Área | ETS | 5,65 % | −19,22 % | 1,1212 | 73,61 % |
| Holdout 2026 | N4 + Región | ETS | 6,02 % | −18,31 % | 1,1370 | 67,70 % |
| Holdout 2026 | N6 + Condición | ETS | 12,15 % | −5,70 % | 1,1227 | 43,39 % |
| Holdout 2026 | N7 + Género | ETS | 13,57 % | −7,11 % | 1,1024 | 38,70 % |
| Holdout 2026 | N3 + Área | ARIMA | 6,17 % | −39,50 % | 1,2229 | 68,77 % |
| Holdout 2026 | N4 + Región | ARIMA | 6,61 % | −47,46 % | 1,2469 | 62,60 % |
| Holdout 2026 | N6 + Condición | ARIMA | 13,16 % | −38,23 % | 1,2157 | 41,58 % |
| Holdout 2026 | N7 + Género | ARIMA | 14,85 % | −46,15 % | 1,2065 | 36,84 % |
| Holdout 2026 | N3 + Área | Theta | 5,26 % | +1,57 % | 1,0437 | 73,61 % |
| Holdout 2026 | N4 + Región | Theta | 5,67 % | +3,34 % | 1,0709 | 68,16 % |
| Holdout 2026 | N6 + Condición | Theta | 11,63 % | −1,76 % | 1,0739 | 44,21 % |
| Holdout 2026 | N7 + Género | Theta | 13,08 % | −4,07 % | 1,0630 | 39,21 % |
| Holdout 2026 | N3 + Área | Comb | 5,49 % | −11,92 % | 1,0890 | 72,15 % |
| Holdout 2026 | N4 + Región | Comb | 5,90 % | −11,97 % | 1,1131 | 66,77 % |
| Holdout 2026 | N6 + Condición | Comb | 11,79 % | −6,24 % | 1,0888 | 44,96 % |
| Holdout 2026 | N7 + Género | Comb | 13,22 % | −8,66 % | 1,0742 | 39,63 % |
| Holdout 2026 | N3 + Área | Global | 4,21 % | +36,67 % | 0,8343 | 81,36 % |
| Holdout 2026 | N4 + Región | Global | 4,60 % | +31,14 % | 0,8691 | 76,35 % |
| Holdout 2026 | N6 + Condición | Global | 9,63 % | +20,48 % | 0,8896 | 50,94 % |
| Holdout 2026 | N7 + Género | Global | 11,04 % | +19,86 % | 0,8970 | 44,61 % |
| Holdout 2026 | N3 + Área | CatBoost | 4,44 % | +37,42 % | 0,8799 | 80,15 % |
| Holdout 2026 | N4 + Región | CatBoost | 4,78 % | +24,45 % | 0,9018 | 75,58 % |
| Holdout 2026 | N6 + Condición | CatBoost | 10,22 % | +10,40 % | 0,9443 | 49,33 % |
| Holdout 2026 | N7 + Género | CatBoost | 11,71 % | +4,47 % | 0,9517 | 42,59 % |

**Tabla A.25.** Referentes por nivel en la validación contra el dato oficial de 2026 (8.729 celdas; C49 = modelo del origen 2025). Esta validación usa el dato oficial.

| Nivel | Método | Grupos | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | Persistencia | 1 | 2,32 % | +0,00 % | 1,0000 | 100,00 % | −2,32 % |
| N1 Nacional | RWD | 1 | 1,25 % | +71,08 % | 0,5378 | 100,00 % | +1,25 % |
| N1 Nacional | ETS | 1 | 2,00 % | +25,69 % | 0,8621 | 100,00 % | −2,00 % |
| N1 Nacional | ARIMA | 1 | 1,25 % | +70,97 % | 0,5388 | 100,00 % | −1,25 % |
| N1 Nacional | Theta | 1 | 0,92 % | +84,28 % | 0,3964 | 100,00 % | −0,92 % |
| N1 Nacional | Comb | 1 | 1,39 % | +64,11 % | 0,5991 | 100,00 % | −1,39 % |
| N1 Nacional | Global | 1 | 0,79 % | +88,52 % | 0,3389 | 100,00 % | +0,79 % |
| N1 Nacional | CatBoost | 1 | 0,01 % | +100,00 % | 0,0059 | 100,00 % | −0,01 % |
| N2 + Institución | Persistencia | 53 | 3,26 % | +0,00 % | 1,0000 | 92,45 % | −2,32 % |
| N2 + Institución | RWD | 53 | 2,78 % | +21,81 % | 0,8532 | 86,79 % | +1,25 % |
| N2 + Institución | ETS | 53 | 3,47 % | −10,65 % | 1,0649 | 92,45 % | −2,00 % |
| N2 + Institución | ARIMA | 53 | 3,57 % | −4,45 % | 1,0952 | 88,68 % | −1,25 % |
| N2 + Institución | Theta | 53 | 3,11 % | +17,90 % | 0,9531 | 88,68 % | −0,92 % |
| N2 + Institución | Comb | 53 | 3,29 % | +6,46 % | 1,0088 | 90,57 % | −1,39 % |
| N2 + Institución | Global | 53 | 2,36 % | +25,29 % | 0,7224 | 94,34 % | +0,79 % |
| N2 + Institución | CatBoost | 53 | 2,31 % | +48,46 % | 0,7083 | 92,45 % | −0,01 % |
| N3 + Área | Persistencia | 408 | 4,76 % | +0,00 % | 1,0000 | 77,94 % | −2,32 % |
| N3 + Área | RWD | 408 | 4,42 % | +24,11 % | 0,9290 | 76,72 % | +1,25 % |
| N3 + Área | ETS | 408 | 5,42 % | −25,19 % | 1,1388 | 72,30 % | −2,00 % |
| N3 + Área | ARIMA | 408 | 6,03 % | −53,77 % | 1,2672 | 69,12 % | −1,25 % |
| N3 + Área | Theta | 408 | 5,13 % | −8,45 % | 1,0784 | 72,79 % | −0,92 % |
| N3 + Área | Comb | 408 | 5,33 % | −20,65 % | 1,1184 | 72,06 % | −1,39 % |
| N3 + Área | Global | 408 | 4,02 % | +36,14 % | 0,8436 | 81,37 % | +0,79 % |
| N3 + Área | CatBoost | 408 | 3,74 % | +48,93 % | 0,7855 | 82,35 % | −0,01 % |
| N4 + Región | Persistencia | 649 | 5,02 % | +0,00 % | 1,0000 | 73,19 % | −2,32 % |
| N4 + Región | RWD | 649 | 4,85 % | +16,84 % | 0,9664 | 72,27 % | +1,25 % |
| N4 + Región | ETS | 649 | 5,82 % | −25,51 % | 1,1596 | 66,41 % | −2,00 % |
| N4 + Región | ARIMA | 649 | 6,49 % | −67,89 % | 1,2919 | 62,10 % | −1,25 % |
| N4 + Región | Theta | 649 | 5,59 % | −9,81 % | 1,1143 | 67,18 % | −0,92 % |
| N4 + Región | Comb | 649 | 5,73 % | −23,56 % | 1,1405 | 66,56 % | −1,39 % |
| N4 + Región | Global | 649 | 4,38 % | +32,81 % | 0,8721 | 75,65 % | +0,79 % |
| N4 + Región | CatBoost | 649 | 4,16 % | +37,52 % | 0,8293 | 76,43 % | −0,01 % |
| N5 + Carrera | Persistencia | 2.668 | 8,48 % | +0,00 % | 1,0000 | 56,97 % | −2,32 % |
| N5 + Carrera | RWD | 2.668 | 8,38 % | +2,78 % | 0,9877 | 55,17 % | +1,25 % |
| N5 + Carrera | ETS | 2.668 | 10,06 % | −11,05 % | 1,1869 | 50,07 % | −2,00 % |
| N5 + Carrera | ARIMA | 2.668 | 11,08 % | −46,74 % | 1,3062 | 47,04 % | −1,25 % |
| N5 + Carrera | Theta | 2.668 | 9,41 % | −3,98 % | 1,1095 | 50,97 % | −0,92 % |
| N5 + Carrera | Comb | 2.668 | 9,77 % | −11,43 % | 1,1527 | 51,12 % | −1,39 % |
| N5 + Carrera | Global | 2.668 | 7,64 % | +18,92 % | 0,9005 | 59,97 % | +0,79 % |
| N5 + Carrera | CatBoost | 2.668 | 7,59 % | +24,54 % | 0,8948 | 58,36 % | −0,01 % |
| N6 + Condición | Persistencia | 4.633 | 10,47 % | +0,00 % | 1,0000 | 49,13 % | −2,32 % |
| N6 + Condición | RWD | 4.633 | 10,59 % | +0,25 % | 1,0110 | 48,72 % | +1,25 % |
| N6 + Condición | ETS | 4.633 | 11,89 % | −6,40 % | 1,1355 | 44,36 % | −2,00 % |
| N6 + Condición | ARIMA | 4.633 | 12,95 % | −38,57 % | 1,2369 | 42,28 % | −1,25 % |
| N6 + Condición | Theta | 4.633 | 11,33 % | −3,41 % | 1,0819 | 45,00 % | −0,92 % |
| N6 + Condición | Comb | 4.633 | 11,50 % | −7,06 % | 1,0980 | 45,93 % | −1,39 % |
| N6 + Condición | Global | 4.633 | 9,23 % | +24,21 % | 0,8818 | 51,65 % | +0,79 % |
| N6 + Condición | CatBoost | 4.633 | 9,42 % | +25,59 % | 0,8999 | 50,94 % | −0,01 % |
| N7 + Género | Persistencia | 8.094 | 11,97 % | +0,00 % | 1,0000 | 42,33 % | −2,32 % |
| N7 + Género | RWD | 8.094 | 12,30 % | −1,59 % | 1,0277 | 40,25 % | +1,25 % |
| N7 + Género | ETS | 8.094 | 13,30 % | −7,72 % | 1,1108 | 39,18 % | −2,00 % |
| N7 + Género | ARIMA | 8.094 | 14,64 % | −45,86 % | 1,2234 | 37,29 % | −1,25 % |
| N7 + Género | Theta | 8.094 | 12,79 % | −5,80 % | 1,0684 | 39,56 % | −0,92 % |
| N7 + Género | Comb | 8.094 | 12,93 % | −9,40 % | 1,0805 | 40,10 % | −1,39 % |
| N7 + Género | Global | 8.094 | 10,65 % | +24,05 % | 0,8895 | 45,16 % | +0,79 % |
| N7 + Género | CatBoost | 8.094 | 10,93 % | +22,82 % | 0,9135 | 44,58 % | −0,01 % |
| N8 + Jornada | Persistencia | 8.729 | 12,69 % | +0,00 % | 1,0000 | 40,89 % | −2,32 % |
| N8 + Jornada | RWD | 8.729 | 12,89 % | +4,76 % | 1,0160 | 39,07 % | +1,25 % |
| N8 + Jornada | ETS | 8.729 | 14,13 % | −9,42 % | 1,1131 | 37,92 % | −2,00 % |
| N8 + Jornada | ARIMA | 8.729 | 15,43 % | −40,70 % | 1,2161 | 36,27 % | −1,25 % |
| N8 + Jornada | Theta | 8.729 | 13,49 % | −3,37 % | 1,0632 | 38,24 % | −0,92 % |
| N8 + Jornada | Comb | 8.729 | 13,73 % | −8,15 % | 1,0817 | 38,84 % | −1,39 % |
| N8 + Jornada | Global | 8.729 | 11,16 % | +26,57 % | 0,8793 | 43,87 % | +0,79 % |
| N8 + Jornada | CatBoost | 8.729 | 11,49 % | +26,71 % | 0,9055 | 43,27 % | −0,01 % |

# A.17 Significancia de las diferencias de error

Prueba tipo Diebold–Mariano entre grupos: $d_g = L(\text{método}_g) - L(\text{referente}_g)$ sobre el error del grupo agregado, pérdida cuadrática y absoluta, error estándar CR1 por clúster de institución (53), $t$ con $G-1$ grados de libertad. Un estadístico negativo favorece al método frente al referente.

**Tabla A.26.** CatBoost (C49) frente a la persistencia y frente al modelo global (Lrez), *holdout* 2026, matrícula observada. Un DM positivo en las columnas CatBoost − Global favorece al global.

| Nivel | Skill CatBoost | p cuadr. vs pers. | p abs. vs pers. | DM cuadr. CatBoost − Global | p | DM abs. CatBoost − Global | p  |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | +49,51 % | 0,3414 | 0,2605 | −0,42 | 0,6771 | +0,37 | 0,7115 |
| N3 + Área | +37,42 % | 0,2311 | 0,2219 | −0,07 | 0,9450 | +0,90 | 0,3716 |
| N4 + Región | +24,45 % | 0,3947 | 0,2307 | +0,56 | 0,5753 | +0,73 | 0,4680 |
| N5 + Carrera | +7,86 % | 0,3866 | 0,1944 | +1,10 | 0,2760 | +2,46 | 0,0171 |
| N6 + Condición | +10,40 % | 0,2506 | 0,0329 | +1,40 | 0,1685 | +3,45 | 0,0011 |
| N7 + Género | +4,47 % | 0,6259 | 0,0206 | +1,73 | 0,0900 | +4,17 | 0,0001 |
| N8 + Jornada | +13,21 % | 0,1006 | 0,0049 | +1,97 | 0,0539 | +4,77 | < 0,0001 |

*Nota:* N1 nacional, DM con corrección HLN (n = 8, OOF 2019–2026, pérdida cuadrática, matrícula observada): RWD DM* +0,4693, *p* 0,6531; ETS −1,8220, *p* 0,1112; ARIMA −2,5632, *p* 0,0374; Theta −1,8872, *p* 0,1011; Comb −3,2443, *p* 0,0142; Global +1,3203, *p* 0,2283; CatBoost +1,1610, *p* 0,2837.

**Tabla A.27.** CatBoost (C49) frente a la persistencia en el OOF 2019–2026 (origen 2026) y en el *holdout* 2025 (origen 2025), matrícula observada. DM negativo favorece al CatBoost.

| Conjunto | Nivel | Grupos | Skill | RelMAE | DM cuadr. | p | DM abs. | p  | Clústeres |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF 2019-2026 (origen 2026) | N2 + Institución | 454 | +25,41 % | 0,9786 | −0,83 | 0,4092 | −0,24 | 0,8110 | 60 |
| OOF 2019-2026 (origen 2026) | N3 + Área | 3.396 | +15,12 % | 0,9594 | −0,65 | 0,5197 | −0,68 | 0,4994 | 60 |
| OOF 2019-2026 (origen 2026) | N4 + Región | 5.920 | −6,14 % | 0,9660 | +0,52 | 0,6083 | −0,70 | 0,4894 | 60 |
| OOF 2019-2026 (origen 2026) | N5 + Carrera | 23.277 | +0,10 % | 0,9587 | −0,01 | 0,9908 | −1,34 | 0,1859 | 60 |
| OOF 2019-2026 (origen 2026) | N6 + Condición | 39.327 | −0,64 % | 0,9700 | +0,08 | 0,9328 | −1,22 | 0,2255 | 60 |
| OOF 2019-2026 (origen 2026) | N7 + Género | 67.413 | −1,04 % | 0,9704 | +0,15 | 0,8827 | −1,41 | 0,1649 | 60 |
| OOF 2019-2026 (origen 2026) | N8 + Jornada | 73.349 | +0,20 % | 0,9662 | −0,03 | 0,9758 | −1,68 | 0,0992 | 60 |
| Holdout 2025 (origen 2025) | N2 + Institución | 55 | +61,79 % | 0,6904 | −1,69 | 0,0973 | −1,74 | 0,0874 | 55 |
| Holdout 2025 (origen 2025) | N3 + Área | 418 | +43,34 % | 0,8811 | −1,83 | 0,0730 | −1,30 | 0,1993 | 55 |
| Holdout 2025 (origen 2025) | N4 + Región | 688 | +29,33 % | 0,9058 | −1,33 | 0,1887 | −1,18 | 0,2437 | 55 |
| Holdout 2025 (origen 2025) | N5 + Carrera | 2.792 | +21,80 % | 0,9216 | −1,55 | 0,1269 | −2,22 | 0,0309 | 55 |
| Holdout 2025 (origen 2025) | N6 + Condición | 4.826 | +20,64 % | 0,9350 | −1,67 | 0,1000 | −2,28 | 0,0268 | 55 |
| Holdout 2025 (origen 2025) | N7 + Género | 8.361 | +21,42 % | 0,9389 | −1,87 | 0,0664 | −2,69 | 0,0095 | 55 |
| Holdout 2025 (origen 2025) | N8 + Jornada | 9.041 | +22,87 % | 0,9333 | −1,95 | 0,0569 | −2,91 | 0,0052 | 55 |

*Nota:* en el OOF el año entra en la llave de cada grupo y los clústeres son las 60 instituciones del período; en N8 las 113 filas repetidas se suman en su celda (73.349 grupos), por lo que el *skill* de N8 (+0,20 %) difiere del calculado por fila (+0,09 %). En el OOF ninguna diferencia es significativa con ninguna pérdida (menor *p* = 0,0992, absoluta, N8); en el *holdout* 2025, lo es con pérdida absoluta en N5–N8 (*p* ≤ 0,031) y no con cuadrática (*p* entre 0,057 y 0,189).

**Tabla A.28.** CatBoost frente a la persistencia, validación contra el dato oficial de 2026 (origen 2025).

| Nivel | Grupos | Skill | DM (cuadrática) | p | DM (absoluta) | p  | Clústeres |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | 53 | +48,46 % | −1,01 | 0,3151 | −1,39 | 0,1697 | 53 |
| N3 + Área | 408 | +48,93 % | −1,98 | 0,0530 | −2,55 | 0,0137 | 53 |
| N4 + Región | 649 | +37,52 % | −2,01 | 0,0496 | −2,55 | 0,0137 | 53 |
| N5 + Carrera | 2.668 | +24,54 % | −2,13 | 0,0378 | −2,66 | 0,0103 | 53 |
| N6 + Condición | 4.633 | +25,59 % | −2,39 | 0,0205 | −3,76 | 0,0004 | 53 |
| N7 + Género | 8.094 | +22,82 % | −2,03 | 0,0470 | −3,98 | 0,0002 | 53 |
| N8 + Jornada | 8.729 | +26,71 % | −2,15 | 0,0363 | −4,33 | < 0,0001 | 53 |

**Tabla A.29.** CatBoost frente al modelo global, validación contra el dato oficial de 2026. Un DM positivo favorece al global.

| Nivel | DM (cuadrática) | p | DM (absoluta) | p  |
|---|---:|---:|---:|---:|
| N2 + Institución | −1,05 | 0,2995 | −0,17 | 0,8672 |
| N3 + Área | −1,21 | 0,2314 | −1,15 | 0,2534 |
| N4 + Región | −0,55 | 0,5832 | −1,05 | 0,2985 |
| N5 + Carrera | −0,61 | 0,5417 | −0,32 | 0,7517 |
| N6 + Condición | −0,17 | 0,8641 | +1,21 | 0,2316 |
| N7 + Género | +0,19 | 0,8476 | +1,94 | 0,0577 |
| N8 + Jornada | −0,02 | 0,9832 | +2,30 | 0,0255 |

**Tabla A.30.** Comparación múltiple con el mejor (MCB/Nemenyi) por nivel, *holdout* 2026, matrícula observada: rango medio del error absoluto entre ocho métodos (1 = mejor); «*» = distinto del mejor (diferencia mayor que la diferencia crítica, CD).

| Nivel | CD | Persistencia | RWD | ETS | ARIMA | Theta | Comb | Global | CatBoost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | 1,4422 | 4,755 | 4,179 | 5,226* | 5,538* | 4,434 | 4,717 | 3,566 | 3,585 |
| N3 + Área | 0,5166 | 4,051 | 4,264 | 4,908* | 5,397* | 4,754* | 4,788* | 3,782 | 4,056 |
| N4 + Región | 0,4128 | 4,086 | 4,199 | 4,940* | 5,352* | 4,751* | 4,776* | 3,841 | 4,054 |
| N5 + Carrera | 0,2006 | 4,122* | 4,323* | 5,007* | 5,250* | 4,671* | 4,745* | 3,827 | 4,054* |
| N6 + Condición | 0,1516 | 4,237* | 4,547* | 4,829* | 4,957* | 4,668* | 4,592* | 4,016 | 4,154 |
| N7 + Género | 0,1146 | 4,311* | 4,680* | 4,729* | 4,881* | 4,650* | 4,537* | 3,995 | 4,218* |
| N8 + Jornada | 0,1103 | 4,332* | 4,679* | 4,742* | 4,892* | 4,655* | 4,545* | 3,973 | 4,182* |

*Nota:* la prueba supone grupos independientes, lo que no se cumple dentro de una institución; con miles de grupos la diferencia crítica es muy estrecha y la prueba es liberal.

**Tabla A.31.** MCB/Nemenyi por nivel, validación contra el dato oficial de 2026.

| Nivel | CD | Persistencia | RWD | ETS | ARIMA | Theta | Comb | Global | CatBoost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | 1,4422 | 4,792 | 4,396 | 5,019* | 5,377* | 4,604 | 4,585 | 3,509 | 3,717 |
| N3 + Área | 0,5198 | 4,034 | 4,304* | 4,968* | 5,402* | 4,869* | 4,859* | 3,836 | 3,728 |
| N4 + Región | 0,4121 | 4,049 | 4,274* | 5,020* | 5,396* | 4,857* | 4,833* | 3,877 | 3,693 |
| N5 + Carrera | 0,2033 | 4,089 | 4,268* | 5,038* | 5,314* | 4,680* | 4,771* | 3,895 | 3,944 |
| N6 + Condición | 0,1543 | 4,196* | 4,558* | 4,836* | 5,019* | 4,671* | 4,586* | 4,041 | 4,093 |
| N7 + Género | 0,1167 | 4,299* | 4,701* | 4,738* | 4,925* | 4,654* | 4,539* | 4,012 | 4,132* |
| N8 + Jornada | 0,1124 | 4,325* | 4,687* | 4,759* | 4,938* | 4,658* | 4,552* | 3,982 | 4,100* |

# A.18 Ablación de las variables con matrícula contemporánea

CatBoost con los hiperparámetros del modelo principal (2.000 iteraciones, tasa de aprendizaje 0,0376, profundidad 7, regularización L2 1,7464, temperatura de *bagging* 0,5465, 183 *border counts*), semilla 42, sin nueva optimización, mismo *target encoding* dentro del *fold* y mismos orígenes. (i) sin densidad de estudiantes por m², razón docente/estudiante ni matrícula sobre PIB (46 variables); (ii) con las 49 variables y las 24 exógenas tomadas en $t-1$ (el valor de la misma celda en $t-1$ o, si no estaba, la media en $t-1$ de institución × carrera × región, luego institución × región, institución y región). RMSE de validación cruzada en escala arcsinh: (i) 0,2964; (ii) 0,2963; publicado (recalculado) 0,2949.

**Tabla A.32.** Ablación con la matrícula observada (N2 y N8).

| Conjunto | Nivel | Variante | WAPE | Skill | RelMAE |
|---|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N2 + Institución | Persistencia | 4,66 % | +0,00 % | 1,0000 |
| OOF 2019-2025 | N8 + Jornada | Persistencia | 15,16 % | +0,00 % | 1,0000 |
| OOF 2019-2025 | N2 + Institución | Publicado | 4,69 % | +22,81 % | 1,0058 |
| OOF 2019-2025 | N8 + Jornada | Publicado | 14,71 % | −1,86 % | 0,9702 |
| OOF 2019-2025 | N2 + Institución | (i) | 4,78 % | +19,83 % | 1,0247 |
| OOF 2019-2025 | N8 + Jornada | (i) | 14,80 % | −4,13 % | 0,9760 |
| OOF 2019-2025 | N2 + Institución | (ii) | 4,36 % | +32,67 % | 0,9351 |
| OOF 2019-2025 | N8 + Jornada | (ii) | 14,61 % | −6,18 % | 0,9639 |
| Holdout 2026 | N2 + Institución | Persistencia | 3,64 % | +0,00 % | 1,0000 |
| Holdout 2026 | N8 + Jornada | Persistencia | 13,09 % | +0,00 % | 1,0000 |
| Holdout 2026 | N2 + Institución | Publicado | 2,76 % | +49,51 % | 0,7578 |
| Holdout 2026 | N8 + Jornada | Publicado | 12,27 % | +13,21 % | 0,9372 |
| Holdout 2026 | N2 + Institución | (i) | 2,66 % | +52,53 % | 0,7305 |
| Holdout 2026 | N8 + Jornada | (i) | 12,27 % | +14,68 % | 0,9374 |
| Holdout 2026 | N2 + Institución | (ii) | 2,85 % | +55,14 % | 0,7824 |
| Holdout 2026 | N8 + Jornada | (ii) | 12,33 % | +17,71 % | 0,9422 |

**Pronóstico 2027 informativo de las variantes (no congelado).** Reajuste con 2018–2026: publicado (recalculado) 761.053; (i) 760.880; (ii) 755.071. La réplica del publicado difiere del congelado (761.058) por el redondeo del rezago; estas cifras no forman parte del congelamiento.

# A.19 Interval score de las bandas al 90 %

$\text{IS}_\alpha$ con $\alpha = 0{,}10$ y MSIS = IS media / MAE de la persistencia en los mismos grupos. Bandas: conformal estratificado por tamaño (las del modelo principal), conformal sin estratos (un solo par de cuantiles por nivel) y AutoETS al 90 % (en N2–N7, un AutoETS por nodo sobre su historia agregada). Se comparan sólo los grupos con las tres bandas.

**Tabla A.33.** Cobertura, ancho mediano, IS media y MSIS por nivel, *holdout* 2026, matrícula observada en la calibración y en la evaluación, sobre los grupos con las tres bandas.

| Nivel | Banda | Grupos comunes | Cobertura | Ancho mediano | IS medio | MSIS |
|---|---:|---:|---:|---:|---:|---:|
| N2 + Institución | Publicadas (conformal estratificado) | 53 | 94,34 % | 2.282,9 | 3.178,1 | 6,2410 |
| N2 + Institución | r1 · conformal sin estratos | 53 | 96,23 % | 4.095,7 | 5.567,6 | 10,9335 |
| N2 + Institución | r2 · AutoETS 90 % | 53 | 94,34 % | 2.244,1 | 3.592,3 | 7,0544 |
| N3 + Área | Publicadas (conformal estratificado) | 404 | 94,31 % | 305,2 | 538,1 | 5,8765 |
| N3 + Área | r1 · conformal sin estratos | 404 | 95,79 % | 478,1 | 833,4 | 9,1020 |
| N3 + Área | r2 · AutoETS 90 % | 404 | 91,09 % | 320,7 | 706,7 | 7,7180 |
| N4 + Región | Publicadas (conformal estratificado) | 630 | 93,49 % | 205,9 | 383,8 | 6,2356 |
| N4 + Región | r1 · conformal sin estratos | 630 | 95,71 % | 409,3 | 752,1 | 12,2206 |
| N4 + Región | r2 · AutoETS 90 % | 630 | 89,84 % | 230,9 | 506,9 | 8,2369 |
| N5 + Carrera | Publicadas (conformal estratificado) | 2.388 | 93,72 % | 102,9 | 166,7 | 7,1447 |
| N5 + Carrera | r1 · conformal sin estratos | 2.388 | 95,27 % | 169,0 | 266,5 | 11,4252 |
| N5 + Carrera | r2 · AutoETS 90 % | 2.388 | 89,45 % | 92,4 | 179,3 | 7,6881 |
| N6 + Condición | Publicadas (conformal estratificado) | 4.036 | 94,82 % | 79,1 | 123,9 | 7,4753 |
| N6 + Condición | r1 · conformal sin estratos | 4.036 | 95,94 % | 94,1 | 183,5 | 11,0731 |
| N6 + Condición | r2 · AutoETS 90 % | 4.036 | 88,75 % | 58,9 | 126,0 | 7,6041 |
| N7 + Género | Publicadas (conformal estratificado) | 6.839 | 94,87 % | 53,6 | 79,8 | 7,2482 |
| N7 + Género | r1 · conformal sin estratos | 6.839 | 95,45 % | 53,7 | 108,0 | 9,8169 |
| N7 + Género | r2 · AutoETS 90 % | 6.839 | 86,83 % | 36,2 | 79,7 | 7,2427 |
| N8 + Jornada | Publicadas (conformal estratificado) | 7.943 | 93,86 % | 37,8 | 65,3 | 6,1554 |
| N8 + Jornada | r1 · conformal sin estratos | 7.943 | 95,10 % | 48,4 | 96,0 | 9,0523 |
| N8 + Jornada | r2 · AutoETS 90 % | 7.943 | 86,99 % | 34,4 | 71,5 | 6,7455 |

*Nota:* en N7, AutoETS obtiene una IS media (79,7) y un MSIS (7,2427) marginalmente menores que las bandas estratificadas (79,8 y 7,2482); en los demás niveles, las bandas estratificadas tienen la menor IS.

# A.20 Experimento de target encoding y procedencia de las columnas precalculadas

Cuatro brazos con el mismo CatBoost y los mismos siete *folds*: estimador $m$ ($\text{enc} = (n\,\bar{z}_c + m\,\bar{z})/(n+m)$, $m = 30$) o ponderación sigmoide (`category_encoders` 2.8.1, `TargetEncoder(smoothing = 30, min_samples_leaf = 20)`, el del modelo principal), ajustados sobre todo el panel 2018–2026 (con fuga) o sólo con las filas de entrenamiento de cada *fold*. Sólo origen 2026. El RMSE por *fold* está en los archivos del autor.

**Procedencia de las columnas precalculadas.** La consolidación calcula las cuatro columnas de *target encoding* precalculadas (estimador $m$, $m = 30$) antes de eliminar duplicados exactos: según la salida registrada de la corrida del origen 2025, había 87.131 filas tras el filtro de rezago mínimo y se eliminaron 13.235 duplicados exactos, hasta 73.896. Las medias y los conteos por categoría ponderan dos veces las filas repetidas; recalculadas sobre las filas finales, difieren de las guardadas hasta en 0,083 (carrera), 0,037 (institución), 0,016 (región) y 0,011 (área). No cambia ninguna cifra publicada, porque el modelo no usa esas columnas y el experimento las recalcula.

# A.21 Reconciliación jerárquica

Jerarquía truncada en N5 (3.853 nodos, 2.739 inferiores): con las aproximadamente 25.000 series de N1–N8, la matriz de covarianza densa de MinT no cabe en memoria. Pronósticos base: N5 = modelo principal agregado; N1–N4 = un AutoETS por nodo sobre la historia agregada (último valor = suma de los rezagos 2026). Covarianza de MinT con contracción: residuos de un paso de los años OOF 2019–2025. `hierarchicalforecast` 1.5.3.

**Tabla A.34.** Reconciliación en el *holdout* 2026 (N1–N5), matrícula observada.

| Método | Nivel | WAPE | Skill | RelMAE | ± 10 % |
|---|---:|---:|---:|---:|---:|
| Base (ETS en N1-N4, CatBoost en N5) | N1 Nacional | 2,86 % | −7,07 % | 1,0348 | 100,00 % |
| Base (ETS en N1-N4, CatBoost en N5) | N2 + Institución | 4,18 % | −15,43 % | 1,1494 | 86,79 % |
| Base (ETS en N1-N4, CatBoost en N5) | N3 + Área | 5,92 % | −20,41 % | 1,1747 | 71,19 % |
| Base (ETS en N1-N4, CatBoost en N5) | N4 + Región | 6,55 % | −46,44 % | 1,2357 | 65,38 % |
| Base (ETS en N1-N4, CatBoost en N5) | N5 + Carrera | 8,42 % | +7,86 % | 0,9549 | 57,21 % |
| BottomUp (publicado) | N1 Nacional | 0,74 % | +92,85 % | 0,2674 | 100,00 % |
| BottomUp (publicado) | N2 + Institución | 2,76 % | +49,51 % | 0,7578 | 88,68 % |
| BottomUp (publicado) | N3 + Área | 4,44 % | +37,42 % | 0,8799 | 80,15 % |
| BottomUp (publicado) | N4 + Región | 4,78 % | +24,45 % | 0,9018 | 75,58 % |
| BottomUp (publicado) | N5 + Carrera | 8,42 % | +7,86 % | 0,9549 | 57,21 % |
| OLS | N1 Nacional | 2,86 % | −7,14 % | 1,0351 | 100,00 % |
| OLS | N2 + Institución | 4,06 % | −10,10 % | 1,1149 | 88,68 % |
| OLS | N3 + Área | 5,81 % | −19,13 % | 1,1529 | 69,25 % |
| OLS | N4 + Región | 6,21 % | −26,40 % | 1,1724 | 64,61 % |
| OLS | N5 + Carrera | 9,92 % | +0,35 % | 1,1253 | 49,87 % |
| WLS estructural | N1 Nacional | 2,17 % | +38,29 % | 0,7856 | 100,00 % |
| WLS estructural | N2 + Institución | 3,37 % | +24,99 % | 0,9267 | 94,34 % |
| WLS estructural | N3 + Área | 4,97 % | +13,69 % | 0,9850 | 73,85 % |
| WLS estructural | N4 + Región | 5,30 % | +14,50 % | 1,0011 | 70,94 % |
| WLS estructural | N5 + Carrera | 9,17 % | +7,81 % | 1,0409 | 52,32 % |
| MinT-shrink | N1 Nacional | 3,03 % | −19,77 % | 1,0944 | 100,00 % |
| MinT-shrink | N2 + Institución | 3,75 % | +22,27 % | 1,0305 | 92,45 % |
| MinT-shrink | N3 + Área | 5,52 % | +1,96 % | 1,0952 | 72,40 % |
| MinT-shrink | N4 + Región | 6,14 % | −5,76 % | 1,1591 | 68,47 % |
| MinT-shrink | N5 + Carrera | 12,32 % | −88,48 % | 1,3981 | 47,65 % |

*Nota:* la suma ascendente publicada es la mejor en N1–N5, y MinT con contracción empeora N4 y N5. Los pronósticos base ETS de N1–N4 son peores que la persistencia, porque la composición de cada nodo cambia entre años, y la reconciliación arrastra esa debilidad.

# A.22 Diseño factorial algoritmo × variables: resultados completos

Hiperparámetros fijos, sin nueva optimización, mismos orígenes y matrícula observada. C49 = modelo publicado; Crez = hiperparámetros de C49 sobre las variables del modelo global, con *target encoding* sigmoide dentro del *fold* sobre los siete identificadores; L49 = LightGBM con *target encoding* sigmoide dentro del *fold* sobre las cuatro categóricas y la rejilla de 12 (elegida: 63 hojas, 100 observaciones mínimas por hoja, 800 árboles); Lrez = modelo global. En la validación de 2026, las 8.329 celdas de esa validación presentes en el *holdout* 2026; los cuatro modelos aplican su tasa del origen 2026 al rezago de 2025 y se comparan con el dato oficial (el modelo del origen 2025 no entra porque se entrenó con otro panel). RMSE de validación cruzada (arcsinh, siete *folds*): C49 0,2949; Crez 0,2948; L49 0,2952; Lrez 0,2869.

**Tabla A.35.** WAPE, *skill*, RelMAE y porcentaje dentro de ±10 % del diseño factorial (N2, N5 y N8).

| Conjunto | Nivel | Modelo | WAPE | Skill | RelMAE | ± 10 % |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N2 + Institución | CatBoost · 49 variables | 4,69 % | +22,81 % | 1,0058 | 78,55 % |
| OOF 2019-2025 | N2 + Institución | CatBoost · solo rezagos | 5,28 % | +1,52 % | 1,1335 | 74,31 % |
| OOF 2019-2025 | N2 + Institución | LightGBM · 49 variables | 4,55 % | +28,98 % | 0,9767 | 80,55 % |
| OOF 2019-2025 | N2 + Institución | LightGBM · solo rezagos | 4,92 % | +15,00 % | 1,0560 | 76,06 % |
| OOF 2019-2025 | N5 + Carrera | CatBoost · 49 variables | 10,14 % | −1,19 % | 0,9592 | 48,67 % |
| OOF 2019-2025 | N5 + Carrera | CatBoost · solo rezagos | 10,58 % | −16,50 % | 1,0014 | 48,00 % |
| OOF 2019-2025 | N5 + Carrera | LightGBM · 49 variables | 10,04 % | +4,29 % | 0,9499 | 48,98 % |
| OOF 2019-2025 | N5 + Carrera | LightGBM · solo rezagos | 10,03 % | +1,18 % | 0,9491 | 49,46 % |
| OOF 2019-2025 | N8 + Jornada | CatBoost · 49 variables | 14,71 % | −1,86 % | 0,9702 | 36,26 % |
| OOF 2019-2025 | N8 + Jornada | CatBoost · solo rezagos | 14,78 % | −11,05 % | 0,9752 | 36,72 % |
| OOF 2019-2025 | N8 + Jornada | LightGBM · 49 variables | 14,62 % | +3,17 % | 0,9644 | 36,27 % |
| OOF 2019-2025 | N8 + Jornada | LightGBM · solo rezagos | 14,27 % | +5,38 % | 0,9415 | 37,50 % |
| Holdout 2026 | N2 + Institución | CatBoost · 49 variables | 2,76 % | +49,51 % | 0,7578 | 88,68 % |
| Holdout 2026 | N2 + Institución | CatBoost · solo rezagos | 2,67 % | +47,38 % | 0,7331 | 90,57 % |
| Holdout 2026 | N2 + Institución | LightGBM · 49 variables | 2,46 % | +64,94 % | 0,6755 | 90,57 % |
| Holdout 2026 | N2 + Institución | LightGBM · solo rezagos | 2,65 % | +43,57 % | 0,7276 | 94,34 % |
| Holdout 2026 | N5 + Carrera | CatBoost · 49 variables | 8,42 % | +7,86 % | 0,9549 | 57,21 % |
| Holdout 2026 | N5 + Carrera | CatBoost · solo rezagos | 7,86 % | +16,87 % | 0,8915 | 59,51 % |
| Holdout 2026 | N5 + Carrera | LightGBM · 49 variables | 8,15 % | +17,34 % | 0,9250 | 57,83 % |
| Holdout 2026 | N5 + Carrera | LightGBM · solo rezagos | 7,98 % | +15,87 % | 0,9059 | 59,66 % |
| Holdout 2026 | N8 + Jornada | CatBoost · 49 variables | 12,27 % | +13,21 % | 0,9372 | 41,59 % |
| Holdout 2026 | N8 + Jornada | CatBoost · solo rezagos | 11,31 % | +26,97 % | 0,8640 | 44,62 % |
| Holdout 2026 | N8 + Jornada | LightGBM · 49 variables | 12,14 % | +19,01 % | 0,9274 | 42,18 % |
| Holdout 2026 | N8 + Jornada | LightGBM · solo rezagos | 11,60 % | +23,42 % | 0,8859 | 43,26 % |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | CatBoost · 49 variables | 2,77 % | +23,90 % | 0,8497 | 90,57 % |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | CatBoost · solo rezagos | 2,54 % | +26,28 % | 0,7794 | 90,57 % |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | LightGBM · 49 variables | 2,45 % | +45,52 % | 0,7517 | 90,57 % |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | LightGBM · solo rezagos | 2,33 % | +26,63 % | 0,7130 | 94,34 % |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | CatBoost · 49 variables | 8,08 % | +10,97 % | 0,9588 | 58,88 % |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | CatBoost · solo rezagos | 7,44 % | +19,48 % | 0,8832 | 61,67 % |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | LightGBM · 49 variables | 7,81 % | +19,14 % | 0,9273 | 59,65 % |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | LightGBM · solo rezagos | 7,58 % | +18,97 % | 0,9004 | 61,59 % |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | CatBoost · 49 variables | 11,77 % | +17,05 % | 0,9401 | 43,34 % |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | CatBoost · solo rezagos | 10,73 % | +29,82 % | 0,8568 | 46,62 % |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | LightGBM · 49 variables | 11,63 % | +21,05 % | 0,9291 | 44,10 % |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | LightGBM · solo rezagos | 11,01 % | +26,59 % | 0,8796 | 45,35 % |

**Tabla A.36.** Contrastes de Diebold–Mariano entre grupos (error estándar por clúster de institución). Un DM positivo favorece al segundo término.

| Conjunto | Nivel | Contraste | DM cuadr. | p | DM abs. | p  |
|---|---:|---:|---:|---:|---:|---:|
| OOF 2019-2025 | N2 + Institución | C49 − Crez | −3,13 | 0,0027 | −3,70 | 0,0005 |
| OOF 2019-2025 | N2 + Institución | L49 − Lrez | −2,18 | 0,0332 | −2,50 | 0,0151 |
| OOF 2019-2025 | N2 + Institución | Crez − Lrez | +3,82 | 0,0003 | +3,92 | 0,0002 |
| OOF 2019-2025 | N2 + Institución | C49 − L49 | +1,73 | 0,0880 | +1,44 | 0,1542 |
| OOF 2019-2025 | N5 + Carrera | C49 − Crez | −2,97 | 0,0043 | −4,44 | < 0,0001 |
| OOF 2019-2025 | N5 + Carrera | L49 − Lrez | −0,72 | 0,4745 | +0,10 | 0,9205 |
| OOF 2019-2025 | N5 + Carrera | Crez − Lrez | +3,31 | 0,0016 | +7,50 | < 0,0001 |
| OOF 2019-2025 | N5 + Carrera | C49 − L49 | +2,47 | 0,0164 | +2,01 | 0,0486 |
| OOF 2019-2025 | N8 + Jornada | C49 − Crez | −2,40 | 0,0195 | −0,83 | 0,4093 |
| OOF 2019-2025 | N8 + Jornada | L49 − Lrez | +0,81 | 0,4228 | +4,22 | < 0,0001 |
| OOF 2019-2025 | N8 + Jornada | Crez − Lrez | +2,78 | 0,0073 | +7,11 | < 0,0001 |
| OOF 2019-2025 | N8 + Jornada | C49 − L49 | +2,29 | 0,0258 | +1,74 | 0,0866 |
| Holdout 2026 | N2 + Institución | C49 − Crez | −0,20 | 0,8393 | +0,26 | 0,7931 |
| Holdout 2026 | N2 + Institución | L49 − Lrez | −1,09 | 0,2796 | −0,60 | 0,5531 |
| Holdout 2026 | N2 + Institución | Crez − Lrez | −0,40 | 0,6883 | +0,09 | 0,9298 |
| Holdout 2026 | N2 + Institución | C49 − L49 | +1,91 | 0,0621 | +1,70 | 0,0948 |
| Holdout 2026 | N5 + Carrera | C49 − Crez | +1,05 | 0,2993 | +3,18 | 0,0025 |
| Holdout 2026 | N5 + Carrera | L49 − Lrez | −0,23 | 0,8226 | +1,03 | 0,3061 |
| Holdout 2026 | N5 + Carrera | Crez − Lrez | −0,24 | 0,8075 | −1,16 | 0,2521 |
| Holdout 2026 | N5 + Carrera | C49 − L49 | +1,61 | 0,1140 | +2,96 | 0,0047 |
| Holdout 2026 | N8 + Jornada | C49 − Crez | +2,23 | 0,0300 | +5,99 | < 0,0001 |
| Holdout 2026 | N8 + Jornada | L49 − Lrez | +0,94 | 0,3495 | +4,65 | < 0,0001 |
| Holdout 2026 | N8 + Jornada | Crez − Lrez | −1,20 | 0,2350 | −2,07 | 0,0432 |
| Holdout 2026 | N8 + Jornada | C49 − L49 | +1,47 | 0,1474 | +1,60 | 0,1166 |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | C49 − Crez | +0,19 | 0,8482 | +0,73 | 0,4683 |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | L49 − Lrez | −0,74 | 0,4610 | +0,44 | 0,6626 |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | Crez − Lrez | +0,03 | 0,9744 | +0,92 | 0,3628 |
| Validación 2026 (8.329 celdas comunes) | N2 + Institución | C49 − L49 | +1,68 | 0,0990 | +1,81 | 0,0768 |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | C49 − Crez | +1,00 | 0,3204 | +3,46 | 0,0011 |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | L49 − Lrez | −0,02 | 0,9843 | +1,26 | 0,2149 |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | Crez − Lrez | −0,12 | 0,9013 | −1,32 | 0,1920 |
| Validación 2026 (8.329 celdas comunes) | N5 + Carrera | C49 − L49 | +1,68 | 0,0996 | +2,73 | 0,0085 |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | C49 − Crez | +2,20 | 0,0325 | +5,92 | < 0,0001 |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | L49 − Lrez | +0,96 | 0,3425 | +4,47 | < 0,0001 |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | Crez − Lrez | −1,41 | 0,1656 | −2,39 | 0,0204 |
| Validación 2026 (8.329 celdas comunes) | N8 + Jornada | C49 − L49 | +1,64 | 0,1064 | +1,65 | 0,1054 |

**Tabla A.37.** Desglose por año del diseño factorial en el OOF y el *holdout* 2026: WAPE en N8 y diferencias en puntos de WAPE (negativo = las 49 variables mejoran), matrícula observada; años de historia = año − 2018.

| Año | Historia (años) | N8 C49 | N8 Crez | N8 L49 | N8 Lrez | N8 C49 − Crez | N8 L49 − Lrez | N2 C49 − Crez | N2 L49 − Lrez |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 1 | 14,36 % | 16,13 % | 14,32 % | 15,06 % | −1,77 | −0,74 | −2,17 | −1,68 |
| 2020 | 2 | 14,69 % | 15,17 % | 14,88 % | 14,44 % | −0,48 | +0,44 | −0,70 | +0,75 |
| 2021 | 3 | 15,50 % | 15,49 % | 15,36 % | 15,37 % | +0,01 | −0,01 | −0,97 | −1,21 |
| 2022 | 4 | 16,31 % | 17,22 % | 16,47 % | 16,31 % | −0,92 | +0,16 | −2,15 | −0,86 |
| 2023 | 5 | 16,20 % | 14,91 % | 15,39 % | 14,40 % | +1,29 | +0,99 | +1,63 | +0,26 |
| 2024 | 6 | 13,63 % | 13,20 % | 13,59 % | 12,76 % | +0,43 | +0,82 | −0,24 | −0,19 |
| 2025 | 7 | 12,45 % | 11,69 % | 12,52 % | 11,83 % | +0,76 | +0,69 | +0,31 | +0,31 |
| 2026 | 8 | 12,27 % | 11,31 % | 12,14 % | 11,60 % | +0,96 | +0,54 | +0,09 | −0,19 |

*Nota:* media 2019–2021 frente a 2022–2025 en N8: C49 − Crez −0,75 frente a +0,39 puntos; L49 − Lrez −0,10 frente a +0,67. Correlación de la diferencia con los años de historia (2019–2025, n = 7): 0,79 con ambos algoritmos en N8; 0,63 y 0,48 en N2. En N2, la ventaja de las exógenas es mayor en 2019–2021 (C49 − Crez −1,28) y casi desaparece en 2022–2025 (−0,11), con 2022 como excepción (−2,15 puntos). Con siete años no hay potencia para separar el patrón de la variación entre años.

# A.23 Pronósticos 2027: detalles

C49 es la predicción congelada sin cambios (rezago = valor de 2026 recortado en 75 celdas); sólo se recalibran sus bandas con residuos observados. Crez, L49 y Lrez usan las especificaciones del diseño factorial, entrenadas con 2018–2026 sobre las mismas 9.069 celdas, con rezago 2027 igual a la matrícula observada de 2026 (en L49, el rezago y las dos variables de mercado rezagadas se recalculan con la matrícula observada y las exógenas quedan en su valor de 2026). Bandas: conformal estratificado por tamaño sobre los residuos OOF de cada modelo contra la matrícula observada (validación con OOF 2019–2025 sobre el *holdout* 2026; producción con OOF 2019–2026). El modelo global (Lrez) es LightGBM 4.6.0 con 31 hojas, 20 observaciones mínimas por hoja, 300 árboles, tasa de aprendizaje 0,03, submuestreo 0,8 y semilla 42.

**Tabla A.38.** Totales 2027 del diseño factorial, crecimiento sobre 741.615 y bandas.

| Modelo | Total 2027 | Crecimiento sobre 741.615 | Cobertura celda, holdout 2026 | Ancho mediano celda | Banda mediana por institución |
|---|---:|---:|---:|---:|---:|
| CatBoost · 49 variables | 761.058 | +2,62 % | 92,49 % | 36,6 | 20,62 % |
| CatBoost · solo rezagos | 767.934 | +3,55 % | 93,25 % | 36,4 | 25,16 % |
| LightGBM · 49 variables | 760.672 | +2,57 % | 92,25 % | 37,1 | 20,74 % |
| LightGBM · solo rezagos | 768.499 | +3,63 % | 92,31 % | 36,1 | 23,21 % |

*Nota:* persistencia (F0) 741.615; Comb nacional (FN) 746.696 (+0,69 %). Con rezago congelado (recortado), el modelo global daría 766.790 (+3,39 %). Referencia nacional (sólo N1) sobre la serie nacional observada 2017–2026: ETS 741.612; ARIMA 752.425; Theta 746.051; Comb 746.696. Rango indicativo no conforme del total de C49: 719.308 a 777.914 (errores agregados OOF de −2,17 % a +5,80 %).

**Tabla A.39.** Cobertura de las bandas en el *holdout* 2026 por nivel (calibración con OOF 2019–2025, matrícula observada).

| Modelo | Celda | N2 + Institución | N3 + Área | N4 + Región | N5 + Carrera | N6 + Condición | N7 + Género | N8 + Jornada |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CatBoost · 49 variables | 92,49 % | 94,34 % | 93,70 % | 93,04 % | 92,19 % | 93,43 % | 93,09 % | 92,74 % |
| CatBoost · solo rezagos | 93,25 % | 98,11 % | 96,13 % | 96,29 % | 94,19 % | 94,21 % | 93,67 % | 93,73 % |
| LightGBM · 49 variables | 92,25 % | 96,23 % | 93,46 % | 93,35 % | 92,44 % | 93,25 % | 92,92 % | 92,67 % |
| LightGBM · solo rezagos | 92,31 % | 94,34 % | 95,88 % | 94,74 % | 93,36 % | 93,62 % | 93,43 % | 93,28 % |

**Tabla A.40.** Desglose 2027 por condición y jornada (variación sobre la matrícula observada de 2026 de cada corte).

| Corte | Valor | Real 2026 | CatBoost · 49 variables | CatBoost · solo rezagos | LightGBM · 49 variables | LightGBM · solo rezagos |
|---|---:|---:|---:|---:|---:|---:|
| condicion | ANTIGUO | 589.678 | +3,44 % | +3,99 % | +3,25 % | +3,80 % |
| condicion | NUEVO | 151.937 | −0,54 % | +1,82 % | −0,07 % | +2,93 % |
| jornada | A Distancia | 43.050 | +14,56 % | +10,71 % | +12,89 % | +12,23 % |
| jornada | Diurna | 650.477 | +2,27 % | +3,71 % | +2,29 % | +3,50 % |
| jornada | Otra | 969 | −22,95 % | −36,33 % | −18,15 % | −14,60 % |
| jornada | Semipresencial | 8.954 | +10,27 % | +9,36 % | +7,94 % | +8,56 % |
| jornada | Vespertina | 38.165 | −5,93 % | −7,66 % | −5,06 % | −4,72 % |

# A.24 Desempeño por institución en la validación de 2026

**Tabla A.41.** Desempeño por institución sobre la matrícula oficial de 2026 (origen 2025).

| Medida | Instituciones |
|---|---:|
| Total institucional dentro de ±5 % | 40 de 53 |
| Total institucional dentro de ±10 % | 49 de 53 |
| WAPE interno menor que el de la persistencia | 42 de 53 (79 %) |
| Cayeron en 2026 y el pronóstico quedó por encima del valor observado | 14 de 14 |
| Cayeron en 2026 y el pronóstico también anticipó caída | 10 de 14 |
| Crecieron en 2026 y el pronóstico quedó por debajo del valor observado | 30 de 39 |

*Nota:* entre las 49 instituciones con al menos 50 celdas y 2.000 matrículas, la mediana del error del total baja de 3,67 % en la mitad más pequeña a 1,74 % en la más grande, y la del WAPE interno, de 14,20 % a 10,03 %.

