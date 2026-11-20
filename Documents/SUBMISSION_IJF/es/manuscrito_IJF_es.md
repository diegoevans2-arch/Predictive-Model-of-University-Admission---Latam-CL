---
title: "Cuando el pronóstico ingenuo es el rezago: evaluación del pronóstico de matrícula universitaria a nivel de programa en Chile"
lang: es-CL
bibliography: references.bib
csl: apa.csl
link-citations: true
---

<!-- Manuscrito anonimizado para revisión doble anónima. Los datos de autoría, afiliación, financiamiento y agradecimientos están exclusivamente en la página de título (title_page_es.md). -->

## Resumen {-}

La matrícula universitaria es tan inercial que la persistencia es un referente difícil de batir y fácil de medir mal. Se pronostica la matrícula universitaria chilena de pregrado por programa, región, jornada, género y condición, con registros públicos. Contra la matrícula oficial de 2026, fuera de muestra, un modelo global de árboles potenciados redujo el error porcentual ponderado de 12,69 % (persistencia) a 11,49 %, y uno global solo de rezagos llegó a 11,16 %; ETS, ARIMA y Theta por serie fueron peores que la persistencia. Un diseño factorial muestra que el aporte de las exógenas depende del período: no mejora la celda en 2026, pero sí los agregados en 2019-2025. Los intervalos conformes estratificados obtuvieron la mejor *interval score* en casi todos los niveles. Si el ingenuo y el rezago comparten construcción, un defecto de emparejamiento sesga el *skill*. Se congela un contraste prospectivo para 2027.

**Palabras clave:** Benchmark de persistencia (*persistence benchmark*); Gradient boosting; Predicción conforme (*conformal prediction*); Origen móvil (*rolling origin*); Fuga de información (*data leakage*); Modelos globales (*global models*); Educación superior (*higher education*)

# 1. Introducción

La planificación de la educación superior requiere proyecciones de matrícula a varios niveles: la autoridad necesita el total del sistema para dimensionar el financiamiento estudiantil y las vacantes; las universidades, proyecciones por institución, facultad y programa. El problema tiene una larga tradición en la investigación institucional [@orwig1972; @hoenack1979; @brinkman1997], y algunos Estados publican proyecciones oficiales [@nces2024]; en Chile se publican estadísticas descriptivas de gran calidad, pero no un pronóstico de matrícula para el año siguiente. Es un caso de pronóstico en contextos sociales [@makridakis2020social]: la matrícula responde a decisiones individuales, cambios de política y shocks agregados, es heterogénea en varias dimensiones cruzadas (institución, programa, región, jornada, género y condición de estudiante nuevo o antiguo) y sufrió perturbaciones sin precedentes en 2020–2022. Más consecuente para la evaluación, es muy inercial: un programa de cinco años arrastra cuatro cohortes ya matriculadas, de modo que la mayor parte del nivel del año siguiente está determinada antes de la admisión.

Esa inercia convierte la elección y la construcción del pronóstico de referencia en el centro del problema de evaluación. Los métodos nuevos deben compararse contra referentes simples y bien construidos [@makridakis2018plos; @makridakis2020m4; @hewamalage2023], y la elección de la persistencia como referencia modifica la percepción del *skill* [@mittermaier2008]. En matrícula, la persistencia sola alcanza un coeficiente de determinación (R²) sobre niveles de entre 0,967 y 0,972 en los dos últimos años observados. Cualquier modelo obtendrá un R² alto; la pregunta pertinente es si supera a la persistencia, y responderla exige que la persistencia esté bien medida.

Este artículo estudia ese problema con modelos globales de *gradient boosting* [@prokhorenkova2018catboost; @ke2017lightgbm] ajustados sobre un panel de 82.967 celdas-año (2018–2026) a nivel de institución × programa × región × jornada × género × condición, construido a partir de registros administrativos públicos. Los modelos se comparan con la persistencia, con métodos estadísticos clásicos ajustados serie por serie (deriva, ETS, ARIMA, Theta y su combinación) y entre sí, mediante un diseño factorial que cruza el algoritmo (CatBoost o LightGBM) con el conjunto de variables (49 variables, con exógenas, o sólo rezagos). La evaluación combina un origen móvil [@tashman2000], un *holdout* ciego, una validación contra la publicación oficial de 2026 —que reveló un modo de falla no documentado de forma explícita— y un contraste prospectivo de 2027 preespecificado.

**Contribuciones.** El artículo hace cinco contribuciones:

1. **Un modo de falla de la evaluación contra la persistencia.** Cuando el pronóstico ingenuo se construye a partir de la misma columna de rezago que alimenta al modelo, un defecto en la llave que empareja cada celda con su valor del año anterior contamina simultáneamente el numerador y el denominador del *skill score*. En un caso real, el mismo defecto infló el *skill* de un año (+77,4 %) y lo hundió al siguiente (−8,0 %) sin que ningún diagnóstico centrado en el modelo lo detectara; se proponen controles concretos (Secciones 4.2, 5.1 y 6.3).
2. **Evidencia comparativa a nivel de programa.** En la celda, los modelos globales superan a la persistencia y ésta a los métodos por serie; los métodos por serie sólo son competitivos en el total nacional. Un diseño factorial algoritmo × variables muestra que el aporte de las variables exógenas depende del período y del nivel de agregación. Las diferencias se contrastan con pruebas de Diebold–Mariano entre grupos con errores estándar por clúster de institución (Secciones 5.5 y 5.6).
3. **Una evaluación fuera de muestra con estatus declarado y una prueba prospectiva preespecificada.** La evaluación contra el dato oficial de 2026 es fuera de muestra pero no prospectiva, porque ese dato motivó la auditoría que corrigió el pipeline. Se complementa con el congelamiento, el 20 de noviembre de 2026, de los pronósticos 2027 del diseño factorial completo y de los referentes, con un protocolo de evaluación que fija de antemano cinco hipótesis (Secciones 5.4 y 5.10).
4. **Intervalos conformes estratificados con cobertura verificada**: 92,49 % en el *holdout* 2026 con residuos observados, frente a un objetivo de 90 %, y menor *interval score* que un conformal sin estratos y que ETS en casi todos los niveles (Secciones 4.9 y 5.7).
5. **Métricas y fuga en series inerciales.** El R² sobre niveles no discrimina entre el modelo y la persistencia, y el desempeño sobre la tasa y sobre el nivel cuentan historias distintas. La fuga aislada de un *target encoding* precalculado es de 2,92 % a 3,74 % del RMSE de validación, según el codificador, más que las diferencias entre algoritmos (Secciones 5.8, 6.1 y 6.2).

La Sección 2 revisa la literatura; la 3 describe los datos; la 4, la metodología; la 5 reporta los resultados, comenzando por el diagnóstico del defecto de evaluación; la 6 discute implicancias y limitaciones, y la 7 concluye. El Apéndice en línea contiene el detalle operativo y resultados complementarios.

# 2. Literatura relacionada

## 2.1 Pronóstico de matrícula y proyecciones oficiales

El pronóstico de matrícula nació en la investigación institucional, con modelos de proyección para planificación [@orwig1972], modelos de demanda [@hoenack1979] y revisiones de métodos de cohortes, series de tiempo y regresión [@brinkman1997]; trabajos recientes siguen modelando agregados institucionales [@chen2019intl; @bowman2021], y la línea de series de tiempo difusas convirtió la matrícula de una universidad en un *benchmark* recurrente sobre una sola serie [@song1993; @chen1996]. El NCES de Estados Unidos publica proyecciones oficiales [@nces2024]; en Chile, el SIES publica la matrícula por programa [@sies2025matricula; @sies2025informe] y el CNED indicadores institucionales [@cned2026indices], pero ninguno publica un pronóstico para el año siguiente. En la búsqueda realizada para este trabajo, en CrossRef y fuentes abiertas, no se encontró un estudio indexado que pronostique la matrícula a nivel de programa × región × género con evaluación ciega contra la persistencia. \[PENDIENTE: búsqueda sistemática en Scopus/WoS/SciELO sobre *enrollment forecasting* y *higher education demand*, con criterios de inclusión declarados.\]

## 2.2 Evaluación de pronósticos, referentes y pruebas

La evaluación fuera de muestra con origen móvil es el estándar para comparar métodos [@tashman2000]; la validación cruzada bloqueada sólo es válida bajo ciertas condiciones, en particular para modelos autorregresivos puros [@bergmeir2012; @bergmeir2018note], y @hewamalage2023 catalogan las trampas más comunes. Las competiciones M mostraron que los referentes estadísticos simples son difíciles de batir y que la comparación contra ellos es obligatoria [@makridakis2018plos; @makridakis2020m4; @petropoulos2022]. El MASE de @hyndman2006 escala el error por el del ingenuo dentro de muestra, mientras que las medidas relativas lo comparan con un referente en el mismo período [@armstrong1992; @davydenko2013]. El *skill score* basado en el error cuadrático, estándar en meteorología [@murphy1988], se interpreta en @wheatcroft2019, y la elección de la persistencia como referencia cambia la percepción del *skill* [@mittermaier2008]; la consistencia entre pérdida y funcional justifica reportar métricas absolutas y cuadráticas [@gneiting2011], y el *valor agregado del pronóstico* (*forecast value added*) traduce la comparación al lenguaje de la planificación [@fildes2025fva]. Las diferencias de error se contrastan con la prueba de @diebold1995, su corrección de muestra pequeña [@harvey1997] y comparaciones múltiples como MCB [@koning2005].

## 2.3 Pronóstico jerárquico y modelos globales

La matrícula tiene estructura agrupada: institución, región, jornada, género y condición se cruzan. La reconciliación de pronósticos produce pronósticos coherentes en todos los niveles [@hyndman2011optimal; @wickramasuriya2019; @hyndman2016fast; @panagiotelis2021], con aplicaciones regionales clásicas [@athanasopoulos2009] y una revisión reciente [@athanasopoulos2024review]. En datos tabulares, el *gradient boosting* —XGBoost [@chen2016xgboost], LightGBM [@ke2017lightgbm] y CatBoost [@prokhorenkova2018catboost]— iguala o supera a las redes profundas [@shwartz2022tabular]; en pronóstico, los árboles dominaron las competiciones recientes [@januschowski2022trees; @bojer2021kaggle], y un LightGBM global superó a los métodos locales en las series jerárquicas de la M5 [@makridakis2022m5acc; @makridakis2022m5unc]. El fundamento de ajustar un único modelo a muchas series está en @monteromanso2021.

## 2.4 Fuga de información, predicción conforme y evaluación prospectiva

La fuga de información (*leakage*) introduce en el entrenamiento información no disponible al pronosticar [@kaufman2012; @kapoor2023leakage]; el *target encoding* [@micci2001target] es una fuente frecuente cuando se calcula fuera de los *folds* [@pargent2022]. La predicción conforme [@vovk2005] produce intervalos con cobertura marginal garantizada bajo intercambiabilidad, y su variante dividida evita reajustar el modelo [@papadopoulos2002; @lei2018; @angelopoulos2023]. Los predictores conformes de Mondrian calibran por separado dentro de categorías [@vovk2005]; @vovk2013conditional demuestra su validez condicional y @bostrom2020mondrian los define para regresión con categorías por dificultad, que es la idea de estratificar por tamaño; @johansson2015mondrian estudian categorías con pocos residuos, y la regresión cuantílica conformalizada es una alternativa [@romano2019]. @barber2023beyond acotan la pérdida de cobertura bajo deriva, y la *interval score* evalúa cobertura y ancho conjuntamente [@gneiting2007; @gneiting2014]. La distinción entre predicción y postdicción [@nosek2018] da valor a los pronósticos publicados antes del resultado, como en las evaluaciones en tiempo real de influenza y COVID-19 [@reich2019; @cramer2022] y en los torneos de pronóstico [@tetlock2014].

## 2.5 Contexto: la educación superior chilena

La expansión de la matrícula universitaria chilena se describe como masificación con segmentación, en un sistema entre el mercado y el Estado [@brunner1993; @espinoza2013; @espinoza2024; @bernasconi2026; @oecd2009chile; @oecd2017chile; @ferreyra2017]. Tres rasgos motivan variables del modelo: el financiamiento —el crédito con aval del Estado afecta la matrícula [@solis2017] y la deserción [@rau2013], y la gratuidad cambió el financiamiento de la demanda [@degayardon2017; @rodriguez2021gratuidad; @clasing2024]—; la información sobre retornos, cuya publicación modifica las decisiones de matrícula [@hastings2015; @hastings2013]; y la estructura de la demanda, con un sistema centralizado de admisión [@rios2021] y una brecha de género en la elección de carrera [@bordon2020]. La investigación chilena con aprendizaje automático se ha concentrado en la deserción individual [@miranda2017; @ramirez2018; @palacios2021], un problema de clasificación con datos internos; el de este trabajo es de regresión sobre celdas agregadas con datos públicos de todo el sistema, y la diferencia es de nivel de análisis, no de sofisticación técnica.

# 3. Datos

## 3.1 Fuentes

El panel integra fuentes administrativas y estadísticas públicas del sistema chileno de educación superior y de la economía regional (Tabla 1). La matrícula proviene de la base de matriculados por programa del SIES, que es la única fuente con la variable de interés a la granularidad requerida y actúa como tabla ancla. Las demás fuentes aportan precios, selectividad, planta docente, infraestructura, retención y contexto macroeconómico regional. Tres catálogos de normalización —sedes a regiones, instituciones y nombres de carrera— se derivan de las mismas fuentes y no constituyen conjuntos de datos independientes.

**Tabla 1.** Fuentes de datos integradas en el panel.

| Fuente | Organismo | Variables aportadas | Período |
|---|---|---|---|
| Base de Matriculados en Educación Superior [@sies2025matricula] | SIES, Subsecretaría de Educación Superior | Matrícula por institución × carrera × jornada × género × condición × año (tabla ancla) | 2007–2026 (modelado 2018–2026) |
| INDICES, bases de datos de educación superior [@cned2026indices] | CNED | Aranceles, valor de matrícula, puntajes de admisión, duración de carreras, acreditación | 2005–2026 (2026 parcial) |
| INDICES, procesos de infraestructura y docentes [@cned2026infraestructura] | CNED | Docentes por grado académico y jornada; m² construidos, salas y oficinas por sede | 2018–2025 |
| PIB regional, volumen a precios del año anterior encadenado, referencia 2018 [@bcch2026pibregional] | Banco Central de Chile | PIB regional anual (miles de millones de pesos encadenados; edición del 23-04-2026, cifras preliminares) | 2018–2025 (2026 arrastrado) |
| Encuesta Nacional de Empleo (ENE) [@ine2026ene] | Instituto Nacional de Estadísticas (INE), difundida también en el Sistema de Información del Mercado Laboral (SIMEL) | Tasa de desocupación regional anual (promedio de los trimestres móviles del año; en 2025, 10 de 12) | 2018–2025 (2026 arrastrado) |
| Buscador de Empleabilidad e Ingresos [@mineduc2025empleabilidad] | SIES (portal mifuturo.cl) | Retención de primer año y empleabilidad por carrera e institución | 2018–2025 |

*Nota:* «Arrastrado» indica que el último valor publicado se repite para el año aún no publicado (Sección 3.4). El PIB regional corresponde a la serie en volumen a precios del año anterior encadenado. El valor anual de desocupación de 2025 promedia los 10 trimestres móviles publicados al momento de la corrida (los que comienzan entre enero y octubre), frente a 12 en los años completos.

Como validación cruzada de la ingesta, los totales calculados de forma independiente a partir del archivo de microdatos del SIES coinciden exactamente con los del informe oficial de matrícula 2026: 1.497.548 matrículas totales, 1.372.167 de pregrado y 759.045 de pregrado en universidades [@sies2025matricula]. \[PENDIENTE: añadir al .bib la entrada del *Informe de Matrícula en Educación Superior 2026* del SIES, que es la edición cuyas cifras se citan; el .bib actual contiene sólo la edición 2025, `sies2025informe`.\]

## 3.2 Construcción del panel

El procesamiento normaliza las llaves mediante catálogos canónicos de regiones, instituciones y carreras y une cada fuente a la izquierda desde la tabla ancla, de modo que ninguna fila de matrícula se pierde por falta de una fuente secundaria. Las reglas de ingesta, los controles de conservación y la cobertura de cada fuente se detallan en los Apéndices A.1 y A.2.

La unidad de análisis es la **celda-año**: institución × nombre de carrera × región × jornada × género × condición (estudiante nuevo o antiguo) × año. El panel final contiene **82.967 observaciones** para 2018–2026, con 52 columnas de las que 49 entran al modelo. El año 2018 se usa exclusivamente como base del rezago y no recibe predicciones. El universo comprende 62 instituciones universitarias, 1.432 nombres de carrera canónicos, 16 regiones y 10 áreas del conocimiento. Se excluyen las celdas con matrícula del año anterior inferior a diez estudiantes, cuyas tasas de crecimiento son mayormente ruido; el Apéndice A.2 documenta la retención de filas y de matrícula en cada etapa del procesamiento.

El trabajo cubre exclusivamente universidades. Los centros de formación técnica e institutos profesionales, que representan cerca de la mitad del pregrado del sistema, quedan fuera del alcance.

## 3.3 Variable de interés

La variable a pronosticar es la tasa de crecimiento de la matrícula de la celda,

$$ \text{tasa}_t = \frac{y_t - y_{t-1}}{y_{t-1}}, $$

donde $y_t$ es la matrícula de la celda en el año $t$. Para entrenar, la tasa se acota a los percentiles 1 y 99 (*winsorización*) y se transforma con el seno hiperbólico inverso, que está definido en todos los reales, preserva el signo y se comporta como la identidad cerca de cero y como un logaritmo en las colas:

$$ z_t = \operatorname{arcsinh}(\text{tasa}_t) = \ln\!\left(\text{tasa}_t + \sqrt{\text{tasa}_t^2 + 1}\right). $$

El nivel se reconstruye como

$$ \hat{y}_t = y_{t-1}\,\bigl(1 + \sinh(\hat{z}_t)\bigr). $$

Esta reconstrucción es central para leer los resultados. El modelo se **optimiza** sobre la tasa —una variable de alta varianza y baja predictibilidad— pero se **evalúa** sobre la matrícula absoluta —una variable de altísima inercia—, que es la magnitud que se presupuesta. La Sección 6.2 discute por qué esa asimetría explica la distancia entre un R² del orden de 0,10 sobre la tasa y uno de 0,98 sobre el nivel.

**Evaluación contra el valor observado.** La winsorización sólo se aplica al objetivo de entrenamiento: toda evaluación de este artículo compara los pronósticos con la matrícula observada de cada celda. Una versión anterior de esta evaluación comparaba, en cambio, contra el valor reconstruido con la tasa recortada, que difiere del observado en 1.430 filas de 2018–2026 y eleva el total observado entre +0,03 % y +0,34 % según el año (Apéndice A.15). Con el valor observado ninguna conclusión cambia de signo, pero las cifras sí; las del *holdout* y del OOF se reportan con el valor observado, y la validación contra el dato oficial de 2026 ya lo usaba.

## 3.4 Imputación y exógenas no publicadas

Las fuentes secundarias tienen grados de completitud distintos, por lo que se imputa por capas que respetan la jerarquía de la celda; cada capa resuelve sólo lo que la anterior dejó vacío: temporal (interpolación dentro de institución-región), jerárquica (de institución × carrera hacia institución × área y área), regional por carrera, institucional y, por último, la mediana global (Apéndice A.3). Una indicadora por fila registra si alguna variable fue imputada y entra al modelo. El 70,9 % de las filas contiene al menos una variable imputada, concentrada en aranceles y retención; la proporción aumenta en 2026 porque varias fuentes aún no publican ese año.

El PIB regional y la desocupación no se imputan: cuando una fuente aún no publica el último año, se repite su último valor regional y se registra el arrastre. En la re-estimación con datos hasta 2026, el PIB y la desocupación de 2026 repiten los de 2025, y la planta docente, la infraestructura y la retención toman el último valor o la mediana histórica disponible (Apéndice A.3).

# 4. Metodología

## 4.1 Diseño general y orígenes de pronóstico

El mismo pipeline, sin cambios de método, se ejecuta desde dos orígenes de pronóstico, que se distinguen a lo largo del texto:

- **Origen 2025.** Validación cruzada sobre 2019–2024, *holdout* ciego 2025, modelo final ajustado con 2018–2025 (73.896 observaciones) y pronóstico de 2026, contrastado con la publicación oficial de julio de 2026 (Sección 5.4).
- **Origen 2026.** Validación cruzada sobre 2019–2025, *holdout* ciego 2026, modelo final ajustado con 2018–2026 (82.967 observaciones) y pronóstico *ex ante* de 2027 (Sección 5.10).

Salvo indicación en contrario, las cifras de las Secciones 5.2, 5.3 y 5.5 a 5.10 corresponden al origen 2026; las de la Sección 5.4 y las filas de la Tabla 10 rotuladas como tales, al origen 2025. La validación de 2026 del origen 2025 y el *holdout* 2026 del origen 2026 miden el mismo año con instrumentos distintos (Sección 5.2).

## 4.2 La llave del rezago

La variable de inercia del modelo es la matrícula del año anterior en la misma celda, $y_{t-1}$. Construirla exige emparejar cada celda de un año con su equivalente del año previo, y ese emparejamiento falla cuando cambia la nomenclatura: el SIES renombra programas entre ediciones sin cambiar su código. Con una llave basada en el nombre literal, una celda renombrada pierde su rezago y sale silenciosamente del universo modelable.

Se adopta por ello una llave con tres niveles de respaldo en cascada (Tabla 2). El nivel fino empareja por nombre literal; el primer respaldo, por el código de carrera, que el SIES conserva a través de los renombres; el segundo respaldo empareja el programa en la región, agregando jornada, género y condición.

**Tabla 2.** Niveles de la llave de emparejamiento del rezago.

| Nivel | Llave de emparejamiento |
|---|---|
| Fino | institución, nombre de carrera, región, jornada, género, condición |
| Código | institución, código de carrera, región, jornada, género, condición |
| Medio | institución, código de carrera, región |

**Escalado por participación.** El nivel medio agrega tres dimensiones, de modo que su total no es comparable con el de una celda individual: usarlo directamente compara una parte con el todo que la contiene y produce tasas de crecimiento espurias cercanas a −1. El respaldo se aplica por tanto escalado por la participación de la celda en su grupo,

$$ y^{\text{celda}}_{t-1} = y^{\text{grupo}}_{t-1} \times \frac{y^{\text{celda}}_{t}}{y^{\text{grupo}}_{t}}, $$

de modo que la celda hereda el *crecimiento* de su grupo en lugar de compararse con su *nivel*. La regla general es que **el numerador y el denominador de una tasa deben compartir la llave**.

El nivel utilizado se registra por fila. De las 82.967 filas, 81.259 (97,9 %) se emparejan en el nivel fino, 694 (0,8 %) por código y 1.014 (1,2 %) por el nivel medio escalado. Restringido a las celdas evaluadas 2019–2026, el emparejamiento es fino en el 98,10 % de las celdas (98,89 % de la matrícula), por código en el 0,66 % (0,56 %) y medio en el 1,25 % (0,56 %). El Apéndice A.4 documenta los controles de distribución del rezago por nivel y el desempeño por origen del rezago.

## 4.3 El pronóstico de persistencia y su identidad con el rezago

El referente principal es la persistencia, o pronóstico ingenuo (*naïve*), $\hat{y}_t = y_{t-1}$. Por construcción, ese pronóstico es **la misma columna de rezago** que alimenta al modelo. No se trata de una elección de implementación sino de una identidad: el pronóstico de persistencia y la variable de inercia del modelo son el mismo objeto.

En consecuencia, un defecto en la llave del rezago degrada **a ambos a la vez** y sesga el *skill score* —un cociente entre los dos errores— en una dirección que depende de cuál resulte más dañado (Secciones 5.1 y 6.3).

## 4.4 Validación temporal

La estructura temporal del panel impide particiones aleatorias. El diseño tiene cuatro componentes:

- ***Holdout* ciego:** el último año observado (2026 en el origen 2026; 2025 en el origen 2025) no interviene en ninguna etapa de selección ni optimización.
- **Validación cruzada con ventana expansiva:** el *fold* $k$ entrena con $\{2018, \ldots, 2017+k\}$ y valida sobre $2018+k$; siete *folds* en el origen 2026 (validación 2019–2025) y seis en el origen 2025. Es el origen móvil de @tashman2000; la validez de la validación cruzada estándar que establecen @bergmeir2018note se restringe a modelos autorregresivos puros, condición que no cumple un modelo con exógenas y un panel de composición cambiante [@bergmeir2012; @hewamalage2023].
- **Predicciones retrospectivas fuera del *fold* (OOF, *out-of-fold*):** para cada año $Y \in \{2019, \ldots, 2026\}$ se ajusta un modelo con todos los años anteriores a $Y$ y se predice $Y$.
- **Validación contra la publicación oficial:** el pronóstico del origen 2025 se contrastó con la matrícula de 2026 publicada por el SIES, que ninguna etapa de ajuste vio, con la salvedad de la Sección 5.1.

Los hiperparámetros se optimizan una vez y se reutilizan en cada modelo OOF anual, de modo que el OOF temprano incorpora información posterior; el *holdout* y el pronóstico no tienen ese problema (Sección 6.5).


## 4.5 Detección empírica de años de shock

Para no depender de una indicadora definida a mano, los años candidatos (2020–2022) se clasifican con un criterio explícito: un año cuya media o desviación anual del objetivo se aparta más de 1,96 desviaciones de la de los años no candidatos es un *shock de nivel* o *de dispersión*, y un candidato con variación agregada negativa no clasificado así es un *shock de recaída* (Apéndice A.6). En ambos orígenes el procedimiento clasifica 2020 y 2022 como shock de nivel y deja vacías las otras dos categorías, cuyas indicadoras son por tanto constantes.

## 4.6 Variables y target encoding dentro del fold

Sobre las variables originales se construyen cuatro grupos de derivadas: el rezago (en escala $\log(1+x)$); ratios del claustro académico (proporción de doctores, de magíster y de horas en jornada completa); indicadores de mercado y competencia (densidad competitiva, arancel relativo regional, selectividad relativa, concentración de la matrícula rezagada en la institución y participación rezagada de la celda en la matrícula regional de la carrera); y las indicadoras de shock. El conjunto final tiene 49 variables: 45 numéricas y 4 categóricas (región, institución, carrera y área del conocimiento). El Apéndice A.5 presenta el diccionario.

Las cuatro categóricas, con cardinalidades de 16, 62, 1.432 y 10, se codifican con *target encoding* suavizado. El codificador pondera la media de cada categoría con una sigmoide de su número de observaciones,

$$ \text{TE}(c) = \bar{z}\,(1 - w_c) + \bar{z}_c\, w_c, \qquad w_c = \frac{1}{1 + e^{-(n_c - k)/s}}, \qquad s = 30,\ k = 20, $$

y se ajusta **dentro** de cada *fold*, como un paso del mismo flujo de preprocesamiento que se reajusta en cada evaluación, usando sólo los datos de entrenamiento del *fold*. Una versión precalculada sobre todo el panel con el estimador $m$ ($m = 30$) se excluye del entrenamiento y sólo se usa en el experimento de la Sección 5.8.

## 4.7 Modelos, referentes y optimización

**Modelo principal.** El modelo de referencia del pipeline es CatBoost [@prokhorenkova2018catboost] con las 49 variables de la Sección 4.6 (en adelante C49). Se optimiza con Optuna [@akiba2019optuna] (TPE, poda por mediana, 50 ensayos por candidato, RMSE promedio de los *folds* en escala arcsinh). Tras la optimización, CatBoost quedó **tercero** por RMSE de validación cruzada (0,2949 frente a 0,2933 de XGBoost y 0,2943 de LightGBM; en el origen 2025, 0,2986 frente a 0,2974 y 0,2982), con una diferencia menor que el sesgo medido del *target encoding* (Sección 5.8). Se mantuvo por continuidad de método entre la corrida validada (origen 2025) y la del pronóstico (origen 2026), y la elección no tiene fundamento de desempeño. Las versiones de `shap` fueron 0.45.1 (origen 2025) y 0.54.1 (origen 2026). Los hiperparámetros seleccionados en el origen 2026 son 2.000 iteraciones, tasa de aprendizaje 0,0376, profundidad 7, regularización L2 de 1,75, temperatura de *bagging* 0,546 y 183 *border counts* (Apéndice A.8). Otros referentes informados sobre la tasa están en el Apéndice A.7.

**Referentes clásicos por serie.** Cada celda se trata como una serie anual cuyo último valor es el rezago, de modo que la persistencia es exactamente el referente de la Sección 4.3. Sobre cada serie se ajustan, con `statsforecast` 2.1.1, una caminata aleatoria con deriva (RWD), AutoETS sin estacionalidad, incluida la variante amortiguada [@hyndman2002ets; @hyndman2008auto], AutoARIMA [@hyndman2008auto], el método Theta [@assimakopoulos2000theta] y la media de ETS, ARIMA y Theta (Comb). Las series con menos de tres observaciones caen a la persistencia; en 2019 lo hacen todas (Apéndice A.16).

**Modelo global solo de rezagos.** Un LightGBM [@ke2017lightgbm] sobre arcsinh de la tasa con los rezagos $t-1$, $t-2$ y $t-3$ de arcsinh de la tasa de la celda, el año relativo y los identificadores categóricos (institución, área, región, carrera, condición, género y jornada), sin exógenas ni nivel rezagado [@monteromanso2021]. Sus hiperparámetros se eligen en una rejilla fija de 12 combinaciones por RMSE medio de validación cruzada en los mismos siete *folds* (31 hojas, 20 observaciones mínimas por hoja y 300 árboles; RMSE de validación cruzada 0,2869). Se denota Lrez.

**Diseño factorial algoritmo × variables.** Para separar el aporte del algoritmo del aporte de las exógenas se cruzan dos algoritmos (CatBoost y LightGBM) con dos conjuntos de variables (las 49 del modelo principal y sólo rezagos), con hiperparámetros fijos, sin nueva optimización y con los mismos orígenes: C49 es el modelo publicado; Crez aplica los hiperparámetros de C49 a las variables del modelo global, con *target encoding* sigmoide dentro del *fold* sobre los siete identificadores; L49 es un LightGBM con las 49 variables y *target encoding* sigmoide dentro del *fold* sobre las cuatro categóricas, con la misma rejilla de 12 (63 hojas, 100 observaciones mínimas por hoja y 800 árboles); y Lrez es el modelo global anterior. En la validación contra el dato oficial de 2026, los cuatro modelos aplican su tasa del origen 2026 al rezago de 2025 en 8.329 celdas comunes, por lo que C49 no coincide exactamente con el modelo del origen 2025 (Apéndice A.22).

**Reconciliación jerárquica.** Los agregados se obtienen por suma ascendente desde la celda; como contraste, se reconcilian N1–N5 con OLS, WLS estructural y MinT con contracción [@wickramasuriya2019; @hyndman2016fast] (Apéndice A.21).

## 4.8 Métricas

Todas las métricas se reportan **con el valor de la persistencia al lado**: RMSE, MAE y R² sobre niveles (con la advertencia de la Sección 6.1); WAPE, $100 \times \sum|y - \hat{y}| / \sum y$, preferible al MAPE en celdas de tamaño muy distinto; sesgo agregado, $100 \times (\sum \hat{y} - \sum y) / \sum y$; el porcentaje de grupos dentro de ±10 % del valor observado; el *skill score* basado en el error cuadrático medio [@murphy1988; @wheatcroft2019], $\text{SS} = 1 - (\text{RMSE}_{\text{modelo}} / \text{RMSE}_{\text{pers}})^2$, positivo cuando el modelo elimina parte del error de la persistencia; y el MAE relativo [@davydenko2013], $\text{RelMAE} = \text{MAE}_{\text{modelo}} / \text{MAE}_{\text{pers}}$ en el mismo conjunto evaluado, menor que uno cuando el modelo supera a la persistencia.[^relmae]

[^relmae]: El RelMAE no es el error absoluto escalado (MASE) de @hyndman2006, que divide por el MAE *dentro de muestra* del pronóstico ingenuo de un paso calculado sobre el período de entrenamiento. Aquí el denominador es el MAE de la persistencia en el mismo período evaluado, lo que define un error relativo en el sentido de @davydenko2013 y @armstrong1992. Con un único grupo, como en el nivel nacional, el cociente se reduce al cociente de los errores absolutos de ese grupo, lo que explica valores como 0,006. Los valores reportados son los mismos que el pipeline calcula; sólo cambia su denominación.

El *skill* es sensible a pocos errores grandes en celdas grandes y el RelMAE no; reportar ambos mantiene la consistencia entre pérdida y funcional [@gneiting2011].

**Significancia de las diferencias.** Para cada nivel N2–N8 se aplica una prueba tipo Diebold–Mariano entre grupos [@diebold1995]: con $d_g = L(\text{método}_g) - L(\text{referente}_g)$ sobre el error del grupo agregado, con pérdida cuadrática y absoluta, se contrasta $E[d] = 0$ con un error estándar robusto por clúster de institución (CR1, 53 clústeres) [@cameron2015cluster] y una distribución $t$ con $G-1$ grados de libertad; en N2 el clúster coincide con el grupo. Como complemento se compara el rango medio del error absoluto entre ocho métodos con la comparación múltiple con el mejor (MCB) y la diferencia crítica de Nemenyi [@koning2005] \[PENDIENTE: cita verificada de la prueba de Nemenyi\]; como supone grupos independientes, lo que no se cumple dentro de una institución, esa prueba es liberal. En el total nacional (N1), donde hay un solo grupo por año, se aplica la prueba de Diebold–Mariano con la corrección de muestra pequeña de @harvey1997 sobre los ocho años del OOF 2019–2026, con potencia muy baja.

**Intervalos.** Los intervalos al 90 % se evalúan por cobertura empírica, ancho mediano e *interval score* $\text{IS}_\alpha(l,u;y) = (u-l) + \tfrac{2}{\alpha}(l-y)\mathbb{1}\{y<l\} + \tfrac{2}{\alpha}(y-u)\mathbb{1}\{y>u\}$ con $\alpha = 0{,}10$ [@gneiting2007], y por su versión escalada MSIS, que divide la *interval score* media por el MAE de la persistencia en los mismos grupos [@makridakis2020m4].

## 4.9 Intervalos de predicción conformes

Se aplica predicción conforme dividida [@papadopoulos2002; @lei2018] con nivel nominal de 90 %. Sea $\{r_i\}_{i=1}^n$ el conjunto ordenado de residuos de calibración y $\alpha = 0{,}10$; los extremos del intervalo son los estadísticos de orden de posiciones

$$ k_{\text{hi}} = \left\lceil (n+1)(1 - \alpha/2) \right\rceil, \qquad k_{\text{lo}} = \left\lfloor (n+1)\,\alpha/2 \right\rfloor. $$

Tres decisiones de diseño definen el procedimiento:

1. **Estratificación por tamaño (predictor conforme de Mondrian).** El error es fuertemente heterocedástico: el cuantil superior del residuo cae de 0,796 en celdas de 10 a 13 estudiantes a 0,162 en las de 168 o más. Se calibra por separado dentro de estratos definidos por deciles del rezago, siguiendo los predictores conformes de Mondrian [@vovk2005; @vovk2013conditional] en su versión para regresión con categorías por dificultad [@bostrom2020mondrian].
2. **Calibración en el espacio del objetivo**, en escala arcsinh, transformada con la reconstrucción del pipeline, que preserva el orden.
3. **Los agregados no se suman**, porque sumar intervalos supondría que todas las celdas yerran en la misma dirección. Cada nivel se calibra sobre su propio error, $\log(\hat{y}/y)$, estratificado por tamaño del grupo.

Se exigen al menos 30 residuos por estrato, de modo que el total nacional no lleva intervalo conforme. En el origen 2025 se calibra con los residuos OOF 2019–2024; en el origen 2026, con residuos contra la matrícula observada: OOF 2019–2025 para medir la cobertura en el *holdout* 2026 y OOF 2019–2026 para el pronóstico 2027. La garantía de cobertura supone intercambiabilidad entre años, que no se cumple estrictamente bajo deriva temporal [@barber2023beyond]; la cobertura empírica fuera de muestra es, por tanto, la evidencia relevante. Los contrastes son un conformal sin estratos y los intervalos de AutoETS (Sección 5.7).

# 5. Resultados

## 5.1 Diagnóstico de un defecto de evaluación

**Detección.** Una versión preliminar del pipeline, con un defecto en la llave del rezago, emitió y fijó en junio de 2026 un pronóstico para 2026, antes de la publicación oficial del 10 de julio. Su *skill* había sido de +77,4 % en el *holdout* 2025; contra el dato de 2026 fue de **−8,0 %**, peor que la persistencia. Un deterioro de esa magnitud entre años consecutivos motivó una auditoría del pipeline.

**Hallazgo.** La auditoría encontró dos defectos en la llave del rezago:

1. **Renombres sin respaldo por código.** La llave emparejaba por nombre literal sin respaldo por código de carrera. En 2025 el SIES renombró los 20 programas de una institución sin cambiar sus códigos, y el pipeline los descartó: la matrícula modelable de esa institución pasó de 3.726 a 351.
2. **Granularidad mezclada en el respaldo.** El nivel medio agregaba jornada, género y condición sólo en el denominador de la tasa. Esto generaba 3.763 filas con una razón rezago/celda mediana de 8× y una tasa mediana de −0,875: contracciones inexistentes, artefacto de comparar una celda con un agregado que la contiene.

En conjunto, los defectos corrompían cerca del 4 % de los objetivos de entrenamiento y, por la identidad de la Sección 4.3, el pronóstico de persistencia en la misma proporción.

**Corrección.** Con la llave por código y el escalado por participación de la Sección 4.2, el nivel medio pasó de una tasa mediana de −0,875 con razón 8,00× a +0,196 con razón 0,84×, y los objetivos artificiales bajaron de 2.944 a cero. La corrección no usó datos de 2026, y el defecto es verificable con datos de 2018–2025. La Tabla 3 contrasta ambas versiones.

**Tabla 3.** Versión preliminar (llave defectuosa) frente al pipeline corregido, ambos con ventana de entrenamiento cerrada en 2025.

| | Versión preliminar | Pipeline corregido |
|---|---:|---:|
| Filas de entrenamiento | 75.622 | 73.896 |
| *Skill score*, *holdout* 2025 | +77,39 % | +22,46 % |
| *Skill score*, validación 2026 | −8,02 % | +26,71 % |
| Niveles de agregación con *skill* negativo en 2026 | los cuatro más finos | ninguno |
| WAPE 2026, celda fina | 12,20 % | 11,49 % |
| R² 2026 frente al de la persistencia | 0,9648 < 0,9674 | 0,9760 > 0,9673 |
| Error agregado 2026 | −2,04 % | −0,01 % |
| Crecimiento pronosticado frente al observado | +0,23 % vs +2,31 % | +2,26 % vs +2,27 % |

*Nota:* las cifras de persistencia difieren levemente entre columnas porque la persistencia hereda el defecto de la llave (Sección 4.3). Las cifras del *holdout* 2025 de ambas versiones se calcularon contra el valor reconstruido con la tasa recortada, como en la evaluación original (Sección 3.3); contra la matrícula observada, el *skill* del pipeline corregido en ese *holdout* es +22,87 % (Tabla 4). Las de la validación 2026 usan el dato oficial.

**Estatus epistémico.** No hubo fuga de datos —ningún dato de 2026 entra al modelo corregido—, pero ese dato actuó como **señal diagnóstica** de la auditoría: la evaluación del pipeline corregido sobre 2026 es *fuera de muestra* pero no *prospectiva*, porque la corrección se hizo después de conocer el resultado [@nosek2018]. La primera evaluación prospectiva del pipeline corregido será la de 2027 (Sección 5.10).

## 5.2 Desempeño global

Sobre la matrícula absoluta observada, la Tabla 4 resume el desempeño en los conjuntos retrospectivos, con la persistencia al lado de cada métrica y el valor *p* de la diferencia.

**Tabla 4.** Desempeño global sobre la matrícula absoluta observada. Las dos primeras filas corresponden al origen 2026; la tercera, al origen 2025.

| Conjunto | n | R² | R² pers. | WAPE | WAPE pers. | *Skill* | *p* cuadr. | *p* abs. | RelMAE | Sesgo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF retrospectivo 2019–2026 | 73.462 | 0,9617 | 0,9616 | 14,38 % | 14,88 % | +0,09 % | 0,9758 | 0,0992 | 0,9662 | +2,23 % |
| *Holdout* 2026 (ciego) | 9.069 | 0,9710 | 0,9666 | 12,27 % | 13,09 % | +13,21 % | 0,1006 | 0,0049 | 0,9372 | +0,74 % |
| *Holdout* 2025 (ciego), origen 2025 | 9.041 | 0,9782 | 0,9717 | 12,35 % | 13,23 % | +22,87 % | 0,0569 | 0,0052 | 0,9333 | −0,29 % |

*Nota:* pers. = persistencia. RelMAE = MAE del modelo dividido por el MAE de la persistencia en el mismo conjunto (Sección 4.8 y nota 1). *p* = valor *p* de la prueba de Diebold–Mariano entre celdas con error estándar por clúster de institución (Sección 4.8), con pérdida cuadrática y absoluta. En el OOF, las pruebas agrupan en N8 las 113 filas repetidas en su celda (73.349 grupos), con lo que el *skill* de ese cálculo es +0,20 % en lugar del +0,09 % por fila, y usan como clústeres las 60 instituciones del período. El OOF contiene 113 filas sobrantes en 88 celdas que heredan el total de su celda (Sección 6.5).

![**Figura 1.** Matrícula pronosticada frente a matrícula observada por celda. Izquierda: predicciones retrospectivas fuera del *fold* (OOF) 2019–2026 (n = 73.462). Derecha: *holdout* ciego 2026 (n = 9.069), origen 2026. La línea discontinua es la identidad. Matrícula observada.](<figuras_es/fig02_scatter_pred_vs_real.png>)

Tres lecturas. Primera, **los R² del modelo y de la persistencia están pegados** (0,9617 frente a 0,9616 en el OOF): el R² alto lo produce la inercia de la matrícula, no el modelo (Figura 1). Segunda, **el *skill* del OOF completo es prácticamente nulo (+0,09 %)**, por los años tempranos (Sección 5.3). Tercera, **el *holdout* 2026 es más difícil que el de 2025**: el modelo supera a la persistencia en WAPE (12,27 % frente a 13,09 %) y en RelMAE (0,937), pero su *skill* baja de +22,87 % a +13,21 %, porque la persistencia mejoró y el error cuadrático se concentra en pocas instituciones grandes cuyo total el modelo sobreestimó. La ventaja es significativa con pérdida absoluta (*p* = 0,0049) pero no con pérdida cuadrática (*p* = 0,1006). En el OOF 2019–2026, en cambio, la diferencia frente a la persistencia no es significativa en ningún nivel con ninguna pérdida (el menor valor *p* es 0,0992, con pérdida absoluta en N8); en el *holdout* 2025 del origen 2025 lo es con pérdida absoluta en N5–N8 (*p* ≤ 0,031) y no con pérdida cuadrática (*p* entre 0,057 y 0,189) (Apéndice A.17). La ventaja frente a la persistencia se concentra, por tanto, en los años con historia larga y en las evaluaciones de 2025 y 2026.

**Dos cifras de 2026 que no deben confundirse.** El *holdout* 2026 del origen 2026 (*skill* +13,21 %, 9.069 celdas) y la validación de 2026 del origen 2025 (+26,71 %, 8.729 celdas; Sección 5.4) miden el mismo año con instrumentos distintos —el primero con las exógenas de 2026 y celdas nuevas; el segundo con exógenas congeladas en 2025—: ninguno corrige al otro, y la evidencia reciente es un solo año.

## 5.3 Desempeño por año

Cada año $Y$ del OOF se predice con un modelo ajustado sólo con los años anteriores, de modo que el volumen de entrenamiento crece monótonamente (Tabla 5, Figura 2).

**Tabla 5.** Desempeño anual en las predicciones retrospectivas OOF (origen 2026), contra la matrícula observada. Observado y Pronosticado son totales sobre las celdas modeladas; el error agregado es pronóstico menos observado, en porcentaje del observado.

| Año | n | R² | WAPE | WAPE pers. | *Skill* | Observado | Pronosticado | Error agregado |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 9.424 | 0,9499 | 14,36 % | 14,30 % | −34,89 % | 654.495 | 677.096 | +3,45 % |
| 2020 | 9.321 | 0,9359 | 14,69 % | 15,74 % | −13,71 % | 637.998 | 666.925 | +4,53 % |
| 2021 | 9.230 | 0,9625 | 15,50 % | 17,08 % | +19,99 % | 669.403 | 654.899 | −2,17 % |
| 2022 | 9.161 | 0,9527 | 16,31 % | 16,35 % | −2,98 % | 662.479 | 700.931 | +5,80 % |
| 2023 | 9.038 | 0,9584 | 16,20 % | 15,64 % | −8,97 % | 670.918 | 702.750 | +4,74 % |
| 2024 | 9.176 | 0,9725 | 13,63 % | 13,96 % | +3,68 % | 692.653 | 700.168 | +1,09 % |
| 2025 | 9.043 | 0,9777 | 12,45 % | 13,23 % | +21,08 % | 711.941 | 712.759 | +0,11 % |
| 2026 | 9.069 | 0,9710 | 12,27 % | 13,09 % | +13,21 % | 741.615 | 747.102 | +0,74 % |

![**Figura 2.** RMSE (matrículas por celda), R² y WAPE por año en las predicciones retrospectivas OOF 2019–2026 (origen 2026). Las bandas sombreadas marcan los años que la detección empírica clasificó como shock de nivel (2020 y 2022). Matrícula observada.](<figuras_es/fig03_metricas_por_anio.png>)

**El modelo tiene *skill* negativo en cuatro de los ocho años retrospectivos**: en 2019 se entrena con un único año previo y es mucho peor que la persistencia, y el *skill* es positivo en los tres últimos años, con seis a ocho años de historia, que es la zona en que opera el pronóstico. Se observa además una **sobrepredicción sistemática en los años tempranos** —de +3,45 % a +5,80 % entre 2019 y 2023, salvo 2021— que se reduce a +1,09 % en 2024, +0,11 % en 2025 y +0,74 % en 2026 (Figura 3). El desempeño en uso se parece al de los últimos años, y los intervalos calibrados con todo el OOF son conservadores (Sección 5.7). Las cifras de 2019 a 2025 difieren levemente de las del origen 2025 (Apéndice A.9).

![**Figura 3.** Matrícula universitaria de pregrado total sobre las celdas modeladas: matrícula observada 2018–2026 (SIES; 653.163 en 2018), predicción retrospectiva OOF con su error agregado anual (en porcentaje) y pronóstico *ex ante* 2027 del modelo principal del origen 2026 (761.058 matrículas). Las bandas marcan los años de shock de nivel.](<figuras_es/fig08_backtesting_temporal_MONEY_FIGURE.png>)

## 5.4 Validación fuera de muestra contra la matrícula oficial de 2026

Este resultado mide el modelo del origen 2025, cuyo pronóstico de 2026 se generó el 13 de agosto de 2026, después de la publicación oficial del 10 de julio, con la ventana de entrenamiento cerrada en 2025 y el estatus declarado en la Sección 5.1.

**Cobertura del universo.** El modelo sólo pronostica programas que existían en 2025 con al menos diez matriculados: de las 759.045 matrículas universitarias de pregrado de 2026, empareja 721.747 (95,09 %) en 8.729 celdas; quedan fuera 37.298 matrículas de programas nuevos o que cruzaron el umbral, y el modelo pronostica 5.611 matrículas en 312 celdas de programas extinguidos. La brecha con el total oficial es mayoritariamente de cobertura, y lo excluido crece más rápido que lo cubierto.

**Tabla 6.** Cascada de agregación sobre la matrícula oficial de 2026 (origen 2025, 8.729 celdas emparejadas). Cada nivel agrega la dimensión indicada al anterior.

| Nivel | n grupos | WAPE | WAPE pers. | *Skill* | *p* cuadr. | *p* abs. | RelMAE | ±10 % | ±10 % pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | 1 | 0,01 % | 2,32 % | +99,99 % | — | — | 0,006 | 100 % | 100 % |
| N2 + Institución | 53 | 2,31 % | 3,26 % | +48,46 % | 0,3151 | 0,1697 | 0,708 | 92,5 % | 92,5 % |
| N3 + Área | 408 | 3,74 % | 4,76 % | +48,93 % | 0,0530 | 0,0137 | 0,786 | 82,4 % | 77,9 % |
| N4 + Región | 649 | 4,16 % | 5,02 % | +37,52 % | 0,0496 | 0,0137 | 0,829 | 76,4 % | 73,2 % |
| N5 + Carrera | 2.668 | 7,59 % | 8,48 % | +24,54 % | 0,0378 | 0,0103 | 0,895 | 58,4 % | 57,0 % |
| N6 + Condición | 4.633 | 9,42 % | 10,47 % | +25,59 % | 0,0205 | 0,0004 | 0,900 | 50,9 % | 49,1 % |
| N7 + Género | 8.094 | 10,93 % | 11,97 % | +22,82 % | 0,0470 | 0,0002 | 0,914 | 44,6 % | 42,3 % |
| N8 + Jornada (celda) | 8.729 | 11,49 % | 12,69 % | +26,71 % | 0,0363 | < 0,0001 | 0,906 | 43,3 % | 40,9 % |

*Nota:* los agregados se obtienen sumando los pronósticos de las celdas (*bottom-up*). *p* = Diebold–Mariano entre grupos con error estándar por clúster de institución (53 clústeres), pérdida cuadrática y absoluta; en N1 no es aplicable (un grupo).

**El *skill* es positivo y el RelMAE menor que uno en los ocho niveles**, y la ventaja sobre la persistencia es significativa al 5 % en N4–N8 con pérdida cuadrática y en N3–N8 con pérdida absoluta; en N2 no lo es. No hay cruce: no existe un nivel de agregación en que convenga usar la persistencia en lugar del modelo. La versión preliminar tenía *skill* negativo en los cuatro niveles más finos (Tabla 3).

**El *holdout* 2026 del origen 2026.** La Tabla 7 reporta la misma cascada para el *holdout* 2026, contra la matrícula observada.

**Tabla 7.** Cascada de agregación sobre el *holdout* 2026 (origen 2026, 9.069 celdas), contra la matrícula observada.

| Nivel | n grupos | WAPE | WAPE pers. | *Skill* | *p* cuadr. | *p* abs. | RelMAE | ±10 % | ±10 % pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | 1 | 0,74 % | 2,77 % | +92,85 % | — | — | 0,2674 | 100,00 % | 100,00 % |
| N2 + Institución | 53 | 2,76 % | 3,64 % | +49,51 % | 0,3414 | 0,2605 | 0,7578 | 88,68 % | 92,45 % |
| N3 + Área | 413 | 4,44 % | 5,04 % | +37,42 % | 0,2311 | 0,2219 | 0,8799 | 80,15 % | 76,76 % |
| N4 + Región | 647 | 4,78 % | 5,30 % | +24,45 % | 0,3947 | 0,2307 | 0,9018 | 75,58 % | 73,42 % |
| N5 + Carrera | 2.739 | 8,42 % | 8,81 % | +7,86 % | 0,3866 | 0,1944 | 0,9549 | 57,21 % | 56,26 % |
| N6 + Condición | 4.798 | 10,22 % | 10,83 % | +10,40 % | 0,2506 | 0,0329 | 0,9443 | 49,33 % | 48,02 % |
| N7 + Género | 8.390 | 11,71 % | 12,31 % | +4,47 % | 0,6259 | 0,0206 | 0,9517 | 42,59 % | 41,81 % |
| N8 + Jornada (celda) | 9.069 | 12,27 % | 13,09 % | +13,21 % | 0,1006 | 0,0049 | 0,9372 | 41,59 % | 40,56 % |

*Nota:* como en la Tabla 6.

El *skill* del *holdout* es menor que el de la validación del origen 2025 en todos los niveles salvo N2, y su ventaja sobre la persistencia sólo es significativa con pérdida absoluta en N6–N8; con pérdida cuadrática no lo es en ningún nivel. En N2, el porcentaje de instituciones dentro de ±10 % queda por debajo del de la persistencia (88,68 % frente a 92,45 %), aunque el WAPE institucional del modelo sea menor; el total institucional cae dentro de ±5 % en 40 de 53 instituciones y dentro de ±10 % en 47. Ambas cascadas coinciden en la frontera de utilidad (Figura 4): hasta institución × área × región, unos tres de cada cuatro grupos caen dentro de ±10 %; al agregar la carrera, poco más de la mitad.

![**Figura 4.** WAPE (izquierda) y R² (derecha) por nivel de agregación, de N1 (total nacional) a N8 (celda fina), en las predicciones retrospectivas OOF 2019–2026 y en el *holdout* 2026 del origen 2026. El R² del nivel nacional en el OOF se calcula sobre ocho observaciones anuales. Matrícula observada.](<figuras_es/fig06_evolucion_metricas_por_nivel.png>)

**El agregado.** El crecimiento pronosticado para las celdas cubiertas fue **+2,26 %** y el observado **+2,27 %**, una diferencia de 0,014 puntos porcentuales. El sistema completo, sin los filtros del modelo, creció 3,69 %, de 732.034 a 759.045 matrículas; la diferencia entre ambas cifras es el crecimiento de lo no cubierto.

**Dónde falla.** La modalidad a distancia es el caso claro: el modelo le asignó más del doble del crecimiento observado. El modelo sirve para proyectar una institución o una facultad, no para anticipar qué programa crecerá: sólo el 43,3 % de las celdas cae dentro de ±10 %; la correlación entre la tasa observada y la pronosticada es 0,365, la dispersión pronosticada es menos de la mitad de la observada y la dirección del cambio es correcta en el 60 % de las celdas. **La frontera de utilidad práctica está entre N4 y N5.**

**Peores celdas.** En el origen 2026, de las 50 peores celdas por error absoluto, 49 en el OOF 2019–2025 y las 50 del *holdout* 2026 tienen rezago fino; los respaldos pesan el 1,1 % de la matrícula y tienen más error relativo, pero no explican el extremo de la distribución, formado por contracciones reales de programas (Apéndice A.4, Tabla A.6).

**Por institución** (Apéndice A.24), el total cayó dentro de ±5 % en 40 de 53 instituciones y dentro de ±10 % en 49, y el modelo superó a la persistencia en WAPE interno en 42. Los errores tiran hacia el centro: el pronóstico quedó por encima del valor observado en las 14 instituciones que cayeron —aunque anticipó la caída en 10— y de las 20 para las que anticipó una caída, sólo 10 cayeron; **el modelo no sirve como alerta temprana de contracción institucional**.

## 5.5 Comparación con referentes por serie y con un modelo global simple

La Tabla 8 compara, en cuatro niveles de la cascada, el modelo principal con la persistencia, con los cinco métodos por serie y con el modelo global solo de rezagos (Sección 4.7).

**Tabla 8.** WAPE por método y nivel en el *holdout* 2026 (origen 2026, matrícula observada) y en la validación contra el dato oficial de 2026 (origen 2025; para los métodos distintos de C49, modelos del origen 2026 aplicados a las 8.729 celdas de esa validación).

| Método | *Holdout* N1 | N2 | N5 | N8 | Validación 2026 N1 | N2 | N5 | N8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Persistencia | 2,77 % | 3,64 % | 8,81 % | 13,09 % | 2,32 % | 3,26 % | 8,48 % | 12,69 % |
| RWD | 0,85 % | 2,85 % | 8,69 % | 13,27 % | 1,25 % | 2,78 % | 8,38 % | 12,89 % |
| ETS | 2,54 % | 3,76 % | 10,31 % | 14,46 % | 2,00 % | 3,47 % | 10,06 % | 14,13 % |
| ARIMA | 1,96 % | 3,91 % | 11,28 % | 15,69 % | 1,25 % | 3,57 % | 11,08 % | 15,43 % |
| Theta | 1,46 % | 3,39 % | 9,67 % | 13,86 % | 0,92 % | 3,11 % | 9,41 % | 13,49 % |
| Comb | 1,99 % | 3,61 % | 10,03 % | 14,08 % | 1,39 % | 3,29 % | 9,77 % | 13,73 % |
| Global solo rezagos (Lrez) | 0,80 % | 2,65 % | 7,98 % | 11,60 % | 0,79 % | 2,36 % | 7,64 % | 11,16 % |
| CatBoost, 49 variables (C49) | 0,74 % | 2,76 % | 8,42 % | 12,27 % | 0,01 % | 2,31 % | 7,59 % | 11,49 % |

*Nota:* RWD = caminata aleatoria con deriva; Comb = media de ETS, ARIMA y Theta. Los agregados se obtienen por suma ascendente desde la celda. Las tablas completas, con *skill*, RelMAE y porcentaje dentro de ±10 % en N1–N8 y en el OOF 2019–2025, están en el Apéndice A.16.

**En la celda, los modelos globales superan a la persistencia y la persistencia a los métodos por serie.** En N8, los cinco métodos por serie tienen más WAPE que la persistencia en los dos conjuntos de 2026 y en el OOF 2019–2025 (Apéndice A.16); el *skill* de ETS en N8 del *holdout* es −9,05 % y el de ARIMA, −42,00 %. En el *holdout* 2026, el global solo de rezagos tiene menos WAPE que C49 en N5 y N8, con diferencias significativas con pérdida absoluta en N5–N8 (N8: DM = +4,77, *p* < 0,0001) pero no con pérdida cuadrática (N8: *p* = 0,0539); en N2–N4 no se distinguen. En la validación de 2026, la diferencia en N8 sólo es significativa con pérdida absoluta (*p* = 0,0255). La comparación múltiple ordena primero al global en N8 en ambos conjuntos (Apéndice A.17).

**En el total nacional, los métodos por serie son competitivos.** En el OOF 2019–2025, ARIMA (WAPE 1,29 %), Comb (1,48 %), Theta (1,56 %) y ETS (1,71 %) superan en N1 a la persistencia (1,87 %) y a los modelos de *boosting*, cuyo sesgo de sobrepredicción temprana domina el agregado (CatBoost 3,08 %; global 3,10 %). Con la corrección de @harvey1997 sobre los ocho años del OOF 2019–2026, la ventaja sobre la persistencia es significativa para Comb (*p* = 0,0142) y ARIMA (*p* = 0,0374) con pérdida cuadrática, y no para ETS, Theta, la deriva, el global ni CatBoost (Apéndice A.17).

## 5.6 Diseño factorial algoritmo × variables

**Tabla 9.** WAPE del diseño factorial y contrastes de Diebold–Mariano entre grupos (estadístico y valor *p*, error estándar por clúster de institución) del modelo con exógenas frente al modelo solo de rezagos, con cada algoritmo. Matrícula observada.

| Conjunto | Nivel | C49 | Crez | L49 | Lrez | C49 − Crez, cuadr. | C49 − Crez, abs. | L49 − Lrez, cuadr. | L49 − Lrez, abs. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF 2019–2025 | N2 | 4,69 % | 5,28 % | 4,55 % | 4,92 % | −3,13 (0,0027) | −3,70 (0,0005) | −2,18 (0,0332) | −2,50 (0,0151) |
| OOF 2019–2025 | N8 | 14,71 % | 14,78 % | 14,62 % | 14,27 % | −2,40 (0,0195) | −0,83 (0,4093) | +0,81 (0,4228) | +4,22 (< 0,0001) |
| *Holdout* 2026 | N2 | 2,76 % | 2,67 % | 2,46 % | 2,65 % | −0,20 (0,8393) | +0,26 (0,7931) | −1,09 (0,2796) | −0,60 (0,5531) |
| *Holdout* 2026 | N8 | 12,27 % | 11,31 % | 12,14 % | 11,60 % | +2,23 (0,0300) | +5,99 (< 0,0001) | +0,94 (0,3495) | +4,65 (< 0,0001) |
| Validación 2026 (8.329 celdas) | N2 | 2,77 % | 2,54 % | 2,45 % | 2,33 % | +0,19 (0,8482) | +0,73 (0,4683) | −0,74 (0,4610) | +0,44 (0,6626) |
| Validación 2026 (8.329 celdas) | N8 | 11,77 % | 10,73 % | 11,63 % | 11,01 % | +2,20 (0,0325) | +5,92 (< 0,0001) | +0,96 (0,3425) | +4,47 (< 0,0001) |

*Nota:* C49 = CatBoost con 49 variables; Crez = CatBoost solo de rezagos; L49 = LightGBM con 49 variables; Lrez = LightGBM solo de rezagos. Un estadístico DM positivo favorece al modelo solo de rezagos; uno negativo, al de 49 variables. En la validación de 2026, los cuatro modelos son del origen 2026 aplicados al rezago de 2025 (Sección 4.7). RMSE de validación cruzada en escala arcsinh: C49 0,2949; Crez 0,2948; L49 0,2952; Lrez 0,2869. Resultados de N5 y contrastes entre algoritmos en el Apéndice A.22.

El aporte de las exógenas **depende del período y del nivel**. En 2026 —que es el mismo año en el *holdout* y en la validación—, un modelo global solo de rezagos iguala o supera en la celda al de 49 variables con ambos algoritmos: con CatBoost, el WAPE en N8 baja de 12,27 % a 11,31 % sin exógenas en el *holdout* (DM cuadrática *p* = 0,0300; absoluta *p* < 0,0001), y con LightGBM, de 12,14 % a 11,60 % (significativo sólo con pérdida absoluta); en N2 no hay diferencias significativas. En el OOF 2019–2025, en cambio, las 49 variables mejoran los agregados: en N2, con CatBoost (*p* = 0,0027 con pérdida cuadrática) y con LightGBM (*p* = 0,0332); con CatBoost también en N5 y N8 con pérdida cuadrática, mientras que en N8 con pérdida absoluta el LightGBM solo de rezagos es mejor. El algoritmo tampoco es neutro: en 2026 el mejor en la celda es el CatBoost solo de rezagos, y en el OOF, el LightGBM solo de rezagos. El desglose por año del OOF es compatible con que las exógenas compensen la falta de historia de rezagos (Apéndice A.22): en N8, la diferencia de WAPE C49 − Crez es de −1,77 puntos en 2019, con un año de historia, −0,48 en 2020 y −0,92 en 2022, y positiva desde 2023 (+1,29, +0,43 y +0,76 en 2023–2025, y +0,96 en 2026); con LightGBM, L49 − Lrez es −0,74 en 2019 y positiva desde 2022. La correlación de la diferencia con los años de historia (2019–2025, n = 7) es 0,79 con ambos algoritmos en N8, y 0,63 y 0,48 en N2. **La ventaja de las exógenas se concentra en los años con poca historia y en el shock de 2022; con cinco años de historia o más no mejora la celda.** Con siete años no hay potencia para separarlo de la variación entre años. Este contraste es la hipótesis H2 del protocolo prospectivo de 2027 (Sección 5.10).

## 5.7 Intervalos de predicción

La Tabla 10 reporta la cobertura empírica de los intervalos conformes al 90 % por celda.

**Tabla 10.** Cobertura empírica de los intervalos conformes al 90 % por celda.

| Origen | Conjunto | Calibración | n | Cobertura | Ancho mediano (matrículas) |
|---|---|---|---:|---:|---:|
| 2025 | *Holdout* 2025 | OOF 2019–2024 | 9.041 | 91,54 % | 36,3 |
| 2025 | Validación 2026 (dato oficial) | OOF 2019–2024 | 8.729 | 92,53 % | 37,3 |
| 2026 | *Holdout* 2026 | OOF 2019–2025, residuos con tasa recortada | 9.069 | 92,26 % | 36,5 |
| 2026 | *Holdout* 2026 | OOF 2019–2025, residuos observados | 9.069 | 92,49 % | 36,6 |
| 2026 (Crez) | *Holdout* 2026 | OOF 2019–2025, residuos observados | 9.069 | 93,25 % | 36,4 |
| 2026 (L49) | *Holdout* 2026 | OOF 2019–2025, residuos observados | 9.069 | 92,25 % | 37,1 |
| 2026 (Lrez) | *Holdout* 2026 | OOF 2019–2025, residuos observados | 9.069 | 92,31 % | 36,1 |

*Nota:* la cobertura se mide contra la matrícula observada, salvo en el *holdout* 2025, medido como en la evaluación original. La fila de residuos con tasa recortada corresponde a la calibración publicada anteriormente; las de residuos observados son las que se congelan con los pronósticos 2027 de cada modelo.

La cobertura excede el objetivo en todos los conjuntos: **los intervalos son conservadores**, porque la calibración incluye los años tempranos con sobrepredicción. Un ancho mediano de 37,3 matrículas para una celda mediana de 44 es honesto, pero poco informativo para un programa individual (detalles por nivel en el Apéndice A.11). El total nacional no lleva intervalo conforme, porque hay una observación por año; en el origen 2025 se reportó un rango indicativo **no conforme** de 681.899 a 742.062 en torno al pronóstico de 727.260.

**Calibración y nitidez.** La Tabla 11 compara las bandas estratificadas con un conformal sin estratos y con los intervalos al 90 % de AutoETS en el *holdout* 2026.

**Tabla 11.** Cobertura, ancho mediano, *interval score* (IS) media y MSIS de las bandas al 90 % en el *holdout* 2026 (origen 2026), contra la matrícula observada, sobre los grupos con las tres bandas disponibles.

| Nivel | Banda | Cobertura | Ancho mediano | IS medio | MSIS |
|---|---|---:|---:|---:|---:|
| N2 + Institución | Conformal estratificado | 94,34 % | 2.282,9 | 3.178,1 | 6,2410 |
| N2 + Institución | Conformal sin estratos | 96,23 % | 4.095,7 | 5.567,6 | 10,9335 |
| N2 + Institución | AutoETS 90 % | 94,34 % | 2.244,1 | 3.592,3 | 7,0544 |
| N5 + Carrera | Conformal estratificado | 93,72 % | 102,9 | 166,7 | 7,1447 |
| N5 + Carrera | Conformal sin estratos | 95,27 % | 169,0 | 266,5 | 11,4252 |
| N5 + Carrera | AutoETS 90 % | 89,45 % | 92,4 | 179,3 | 7,6881 |
| N8 + Jornada (celda) | Conformal estratificado | 93,86 % | 37,8 | 65,3 | 6,1554 |
| N8 + Jornada (celda) | Conformal sin estratos | 95,10 % | 48,4 | 96,0 | 9,0523 |
| N8 + Jornada (celda) | AutoETS 90 % | 86,99 % | 34,4 | 71,5 | 6,7455 |

*Nota:* MSIS = IS media dividida por el MAE de la persistencia en los mismos grupos. La comparación excluye los grupos con menos de tres años de historia contigua para ETS, por lo que la cobertura difiere de la de la Tabla 10. N3, N4, N6 y N7 en el Apéndice A.19.

Las bandas estratificadas obtienen menor IS y MSIS que el conformal sin estratos en todos los niveles N2–N8, porque son mucho más estrechas con una cobertura todavía superior al 90 %. Frente a AutoETS, cuyas bandas son más estrechas pero subcubren desde N4 (86,99 % en la celda), las estratificadas tienen menor IS en todos los niveles salvo N7, donde quedan prácticamente empatadas (IS 79,8 frente a 79,7; MSIS 7,2482 frente a 7,2427). La estratificación de Mondrian es, por tanto, lo que hace útiles a los intervalos conformes en un panel tan heterocedástico.

## 5.8 Sesgo del target encoding precalculado

La Tabla 12 aísla la fuga del *target encoding* con un experimento de cuatro brazos —estimador $m$ o ponderación sigmoide, ajustado sobre todo el panel o dentro de cada *fold*—, con el mismo CatBoost, los mismos hiperparámetros y los mismos siete *folds* (origen 2026).

**Tabla 12.** RMSE de validación cruzada en escala arcsinh según el codificador y su ajuste (origen 2026).

| Codificador | Con fuga (todo el panel) | Dentro del *fold* | Diferencia | Diferencia relativa |
|---|---:|---:|---:|---:|
| Estimador $m$ ($m = 30$) | 0,2852 | 0,2938 | −0,0086 | −2,92 % |
| Ponderación sigmoide | 0,2838 | 0,2949 | −0,0110 | −3,74 % |
| Comparación publicada anteriormente: $m$ con fuga frente a sigmoide dentro del *fold* | 0,2852 | 0,2949 | −0,0096 | −3,26 % |

*Nota:* el brazo sigmoide dentro del *fold* reproduce el RMSE del modelo principal (0,2949). El experimento no se repitió para el origen 2025, donde la comparación no aislada daba 3,5 %. Las columnas precalculadas con el estimador $m$ que trae el panel se calcularon antes de eliminar 13.235 filas duplicadas exactas, de modo que ponderan dos veces las filas repetidas; ninguna cifra publicada depende de ellas, y el brazo $m$ de esta tabla las recalcula.

Con el mismo codificador en ambos brazos, la fuga aislada hace que la validación cruzada reporte un RMSE entre 2,92 % y 3,74 % mejor que el real. La distancia entre los tres candidatos de *boosting* tras la optimización (0,5 %) y entre las cuatro celdas del diseño factorial en validación cruzada (de 0,2869 a 0,2952) es menor que ese sesgo, de modo que un solo error de este tipo puede invertir el orden aparente de los modelos [@kaufman2012; @kapoor2023leakage].

## 5.9 Heterogeneidad regional y explicabilidad

**Región.** La heterogeneidad regional es moderada y se ordena en buena parte por el número de observaciones: en el OOF 2019–2026, el WAPE va de 11,99 % en Los Ríos a 25,50 % en Aysén, la región con menos programas (313 observaciones), y la Región Metropolitana queda en un rango intermedio (14,78 %). El WAPE del modelo es menor que el de la persistencia en 14 de las 16 regiones, pero el *skill* es negativo en 6 (Apéndice A.9, Figura A.1).

**Explicabilidad.** El análisis de valores SHAP [@lundberg2017shap], calculados con el algoritmo exacto para árboles [@lundberg2020treeshap] sobre las 92.036 filas exportadas por el origen 2026 —retrospectivas, de base del rezago y de pronóstico—, ordena las cinco variables más influyentes (media del valor absoluto) así: nombre de carrera codificado (0,0533), condición de estudiante nuevo (0,0488), rezago de la matrícula (0,0364), jornada vespertina (0,0299) y participación rezagada de la celda en la matrícula regional de la carrera (0,0229). El orden de las cinco primeras no cambia entre orígenes (Apéndice A.10).

El hallazgo estable es que **la condición de estudiante nuevo compite con el rezago en importancia**. La dinámica de los nuevos depende de la admisión y la de los antiguos de la retención, que son procesos distintos. La jornada vespertina en el cuarto lugar es consistente con la Sección 5.4: las modalidades no diurnas son las que se mueven de forma diferenciada y donde el modelo más se equivoca.

**Las atribuciones no son aporte predictivo.** Que variables exógenas aparezcan entre las influyentes del modelo principal no implica que mejoren el pronóstico: en 2026, el mismo algoritmo sin exógenas es igual o mejor en la celda (Sección 5.6). Las contribuciones SHAP describen cómo usa el modelo sus variables, no cuánto aportaría cada una a la exactitud fuera de muestra.

## 5.10 Pronósticos 2027 (*ex ante*, congelados antes del dato)

El universo son las 9.069 celdas de 53 instituciones con programas vigentes en 2026 y al menos diez matriculados, no comparable con el total oficial del SIES. Se congelaron los cuatro modelos del diseño factorial y dos referentes (Tabla 13).

**Tabla 13.** Pronósticos 2027 congelados, con su crecimiento sobre la matrícula observada de 2026 en las mismas celdas (741.615).

| ID | Modelo | Total 2027 | Crecimiento |
|---|---|---:|---:|
| C49 | CatBoost, 49 variables (modelo principal) | 761.058 | +2,62 % |
| Crez | CatBoost, solo rezagos | 767.934 | +3,55 % |
| L49 | LightGBM, 49 variables | 760.672 | +2,57 % |
| Lrez | LightGBM, solo rezagos (modelo global) | 768.499 | +3,63 % |
| F0 | Persistencia | 741.615 | +0,00 % |
| FN | Comb nacional (media de ETS, ARIMA y Theta sobre la serie nacional; sólo N1) | 746.696 | +0,69 % |

*Nota:* C49 se congeló sin cambios porque su total ya se había publicado. Usa como rezago de 75 celdas el valor reconstruido con la tasa recortada (740.318 en total, frente a 741.615 observados); su crecimiento sobre esa base sería +2,80 %. Los demás modelos usan como rezago la matrícula observada de 2026.

**Composición.** Los dos modelos con exógenas pronostican menos crecimiento que los dos sin exógenas, con ambos algoritmos (alrededor de +2,6 % frente a +3,6 %), y la diferencia está sobre todo en los estudiantes nuevos: −0,54 % con C49 y −0,07 % con L49, frente a +1,82 % con Crez y +2,93 % con Lrez. Los cuatro prevén alzas de 10,71 % a 14,56 % en la modalidad a distancia, que en 2026 el modelo del origen 2025 sobreestimó (Sección 5.4), y caídas de 4,72 % a 7,66 % en la vespertina (Apéndice A.23). Por institución, C49 prevé una caída en 15 de las 53 sobre la base observada de 2026.

**Incertidumbre.** Las bandas al 90 % de cada modelo se calibran con el conformal estratificado sobre sus residuos OOF 2019–2026 contra la matrícula observada; las de C49 se recalibraron así sin tocar su pronóstico puntual. Calibradas con OOF 2019–2025, cubren en el *holdout* 2026 entre 92,25 % y 93,25 % de las celdas (Tabla 10), y la banda mediana por institución mide 20,62 % del pronóstico con C49, 25,16 % con Crez, 20,74 % con L49 y 23,21 % con Lrez. El total nacional de C49 lleva un rango indicativo **no conforme** de 719.308 a 777.914, construido con los errores agregados OOF observados de −2,17 % (2021) a +5,80 % (2022).

**Frente a referentes simples.** C49 queda 0,8 y 1,6 puntos por debajo de la variación promedio de 2024–2026 (+3,40 %) y de la de 2026 (+4,17 %), calculadas sobre la serie agregada observada; la tendencia lineal 2018–2026 (730.266; −1,53 %) es una referencia débil, porque 2026 quedó por encima de la tendencia de largo plazo (Figura 5).

![**Figura 5.** Crecimiento agregado 2027 sobre la matrícula observada de 2026 en las celdas modeladas: pronóstico del modelo principal (C49, origen 2026; +2,62 %) frente a tres referentes simples calculados sobre la serie agregada observada —regresión lineal 2018–2026 (−1,53 %), promedio de las variaciones 2024–2026 (+3,40 %) y variación 2026 (+4,17 %)—.](<figuras_es/fig09_forecast_2027_vs_baselines.png>)

**Estatus y protocolo.** Los pronósticos son *ex ante*. Los seis pronósticos se congelaron el 20 de noviembre de 2026, antes de la publicación oficial de la matrícula 2027, mediante una etiqueta anotada en un repositorio público con las huellas SHA-256 de las predicciones, el protocolo de evaluación y el script de evaluación \[identificadores omitidos para la revisión doble anónima; se entregan al editor en la carta de presentación\]. El depósito con DOI se informará en la versión aceptada. \[PENDIENTE: DOI de Zenodo\] El protocolo (Apéndice A.14) fija el dato (primera publicación del SIES, sin winsorización ni ajuste), el emparejamiento, las métricas y cinco hipótesis contrastadas con Diebold–Mariano entre grupos por clúster de institución, con **pérdida principal absoluta**: si los cuatro modelos superan a la persistencia (H1); si aportan las exógenas, C49 − Crez y L49 − Lrez en N8 y N2 (H2), con lectura fijada de antemano y un contraste concreto, porque los modelos con exógenas pronostican alrededor de +2,6 % y los sin exógenas alrededor de +3,6 %; si importa el algoritmo (H3); el error del total nacional (H4); y la calibración de las bandas (H5). Un modelo **fracasa** si su RelMAE en N8 es mayor o igual que uno. Las bandas se clasifican, por modelo y nivel y con el intervalo de Wilson, con un criterio asimétrico: subcobertura si la cobertura es menor que 88 %, calibradas entre 88 % y 95 % y conservadoras por encima de 95 %. El criterio se fijó tras una prueba en seco del programa de evaluación sobre 2026 y antes del congelamiento; en esa prueba, las bandas de los cuatro modelos quedaron calibradas en N8 (C49 92,49 %, Crez 93,25 %, L49 92,25 %, Lrez 92,31 %). Ningún resultado se reinterpreta ni modifica los pronósticos congelados [@reich2019; @cramer2022; @tetlock2014].

**Supuestos.** Las exógenas de 2027 quedan congeladas en su último valor observado, que para el PIB y la desocupación es el de 2025 (Sección 3.4); si el dato de 2027 se aparta del pronóstico de los modelos con exógenas, la primera revisión será ese arrastre.

# 6. Discusión

## 6.1 El R² sobre niveles no discrimina

El resultado más transferible del trabajo no es una cifra de desempeño sino una advertencia de medición. En el *holdout* 2026, el modelo alcanza un R² de 0,9710 y la persistencia de 0,9666 (en el *holdout* 2025 del origen 2025, 0,9782 y 0,9717). Un estudio que reportara el primero sin el segundo comunicaría que su modelo explica el 97 % de la varianza, cuando la contribución propia del modelo sobre la inercia es de menos de un punto. Es una propiedad de cualquier serie de matrícula con programas de varios años, y la misma lógica que llevó a la meteorología a evaluar contra la persistencia [@murphy1988; @mittermaier2008] se aplica aquí con especial fuerza.

**Recomendación:** ningún R² sobre niveles de matrícula debería publicarse sin el de la persistencia al lado. Las métricas informativas en este dominio son el *skill score*, el error relativo (RelMAE) y el porcentaje de grupos dentro de una banda declarada, todas expresadas frente a la persistencia.

## 6.2 Tasa y nivel

Existe una distancia grande entre el desempeño sobre la tasa de crecimiento —R² del orden de 0,10 en escala arcsinh en los *folds* de validación— y sobre el nivel —R² de 0,98—. Es la misma inercia vista desde el otro lado: casi todo el nivel es anticipable y casi nada del crecimiento marginal lo es. Para la planificación la métrica relevante es la del nivel, porque el nivel es lo que se presupuesta. Pero la implicación debe explicitarse: un modelo con R² de 0,98 sobre niveles puede tener muy poca capacidad de anticipar *cambios*, y ambas afirmaciones son simultáneamente ciertas. La compresión hacia la media observada a nivel de celda (Sección 5.4) es la manifestación de esa baja predictibilidad del cambio.

## 6.3 Cuando el pronóstico ingenuo es el rezago

El pronóstico de persistencia y la variable de inercia del modelo son la misma columna. Cuando esa columna tiene un defecto de construcción, el *skill score* se contamina en numerador y denominador a la vez, y el sesgo **no tiene dirección predecible**: aquí, el mismo defecto infló el *skill* del *holdout* 2025 hasta +77,4 % y lo hundió a −8,0 % en 2026, lo que sugería, erróneamente, que el margen del modelo se había evaporado. El modo de falla es invisible para los diagnósticos habituales —curvas de aprendizaje, residuos, importancia de variables—, y se relaciona con la fuga de información [@kaufman2012; @kapoor2023leakage] sin ser lo mismo: no hay información del futuro en el entrenamiento, sino un error en la variable que define a la vez el predictor principal y el referente. Las listas de verificación advierten contra los referentes débiles [@hewamalage2023]; este caso muestra que un referente *correcto en su definición* puede estar mal *construido*.

**Recomendaciones** para todo trabajo que reporte *skill* frente a la persistencia sobre datos con rezago: (1) auditar la llave del rezago como se audita el objetivo, publicando la tasa de emparejamiento por nivel de respaldo; (2) vigilar la distribución del rezago —una razón rezago/celda con mediana de 8× es detectable antes de entrenar—; (3) tratar los saltos grandes de *skill* entre períodos como sospecha sobre el instrumento; (4) verificar que numerador y denominador de una tasa compartan la llave; y (5) publicar pronósticos fijados antes del dato y contrastarlos: la evaluación fuera de muestra también audita el pipeline.


## 6.4 Qué aporta el modelo

La evidencia separa un resultado robusto de uno dependiente del período. **El resultado robusto** es que, con la persistencia bien construida, los modelos globales —CatBoost y LightGBM, con o sin exógenas— tienen en la celda menos WAPE que la persistencia, y ésta que los métodos ajustados serie por serie, en el OOF 2019–2025 y en las dos evaluaciones de 2026 (Secciones 5.5 y 5.6). La ventaja del modelo principal frente a la persistencia, sin embargo, no es significativa en el OOF 2019–2026 completo con ninguna pérdida, y sí lo es en las evaluaciones de 2025 y 2026 con pérdida absoluta (Sección 5.2): se concentra en los años con historia larga. Es la lección de las competiciones recientes y de la teoría de los modelos globales [@makridakis2022m5acc; @januschowski2022trees; @monteromanso2021]. En el total nacional, en cambio, los métodos por serie sobre la serie agregada son competitivos y, con la potencia baja de ocho años, Comb y ARIMA superan a la persistencia de forma significativa, mientras que los modelos de celda no lo hacen: para el agregado del sistema conviene mantener un referente por serie al lado del modelo [@makridakis2020m4].

**El resultado dependiente del período** es el aporte de las exógenas. En 2026, un modelo global solo de rezagos iguala o supera al de 49 variables en la celda con ambos algoritmos; en el OOF 2019–2025, las 49 variables mejoran los agregados, en particular el nivel institucional. La evidencia reciente es un solo año, y no permite afirmar ni que las exógenas no aportan ni que la precisión provenga sólo del diseño global. El desglose por año del OOF es compatible con una explicación: las exógenas ayudan cuando la historia de rezagos es corta —en 2019 el modelo se entrena con un solo año— y en el shock de 2022, y dejan de mejorar la celda con cinco años de historia o más (Sección 5.6). Si fuera así, el resultado de 2026 sería lo esperable en adelante; pero con siete años no hay potencia para separar ese patrón de la variación entre años, y la hipótesis H2 del protocolo de 2027 lo someterá a una prueba prospectiva con la lectura fijada de antemano. La elección de algoritmo tampoco es neutra, y depende del conjunto evaluado.

## 6.5 Limitaciones

**Componente extrapolativo nulo.** Los árboles no extrapolan en el año, y las exógenas se congelan en su último valor: **el pronóstico es, en lo esencial, una transformación aprendida del rezago**. Para el total nacional de 2026, arrastrar el crecimiento del año anterior quedó a −0,08 % del valor observado: el valor del modelo frente a reglas agregadas está en la desagregación (Sección 5.5).

**Variables con información del año evaluado (ablación cerrada).** Tres variables usan la matrícula agregada del año $t$. Reentrenado sin ellas (variante i) o con todas las exógenas en $t-1$ (variante ii), con los mismos hiperparámetros, semilla y *folds*, el WAPE del *holdout* 2026 en la celda queda en 12,27 % con la variante i y sube a 12,33 % con la variante ii (+0,06 puntos), frente a 12,27 % del modelo publicado; el optimismo atribuible a la información contemporánea es pequeño (Apéndice A.18).

**Un solo año de prueba reciente.** El *holdout* 2026 y la validación del origen 2025 miden el mismo año; el contraste de 2027 agrega el segundo. Los hiperparámetros elegidos en la validación cruzada se reutilizan en el OOF, cuyas cifras tempranas son indicativas, y el año de *holdout* entra en los estadísticos del detector de shocks y en los percentiles de la winsorización del objetivo.

**Calidad de los datos.** Una versión anterior de la evaluación usaba el valor reconstruido con la tasa recortada; la corrección no cambia el signo de ninguna conclusión, y algunas cifras secundarias del apéndice se rotulan como calculadas con ese valor. En el OOF hay 113 filas sobrantes en 88 celdas, de dos instituciones (2019–2021 y 2024), por varias sedes en una misma región o versiones del plan, que heredan el total de la celda; el *holdout* 2026 y los pronósticos 2027 no están afectados, y sin ellas el WAPE de C49 en la celda del OOF 2019–2025 pasa de 14,71 % a 14,70 % y su *skill* de −1,86 % a −2,06 %; se corregirá en la siguiente versión metodológica. \[PENDIENTE: confirmación del autor para incluir esta nota\] Por un defecto de orden de operaciones en la consolidación, la reparación del nombre de la región de Ñuble no se aplicó, y las uniones institucionales de docentes, inmuebles y aranceles de esa región quedaron afectadas; la corrección está identificada y se evaluará en la siguiente versión; su efecto sobre el error no está medido. El 70,9 % de las filas tiene alguna variable imputada, y el PIB y la desocupación de 2026 se arrastraron desde 2025.

**Reconciliación y detección de shocks.** La suma ascendente es la mejor reconciliación en N1–N5, y MinT con contracción no mejora la frontera N4/N5, aunque con pronósticos base ETS débiles (Apéndice A.21). La detección de shocks se sostiene como criterio reproducible, no como tipología: dos de sus tres categorías quedan vacías y su clasificación es sensible al preprocesamiento.

**Alcance y uso.** El trabajo cubre sólo universidades (unas 759 mil de 1.372.167 matrículas de pregrado del sistema), y dentro de ellas el 95,09 % de la matrícula; lo excluido es lo que más crece. Las contribuciones SHAP son asociaciones, no efectos causales, y el modelo es una herramienta de **planificación agregada**, no de decisión sobre postulantes individuales.


## 6.6 Direcciones futuras

La primera prioridad es la evaluación prospectiva de 2027 según el protocolo congelado; las mejoras se evaluarán en una línea separada, con su propio pronóstico fijado de antemano. En orden de retorno esperado: (i) explotar la estructura de cohortes mediante la identidad contable $\text{Antiguos}_t \approx \text{retención} \times (\text{Antiguos}_{t-1} + \text{Nuevos}_{t-1})$, que daría al modelo un componente dinámico propio; (ii) verificar si el aporte de las exógenas depende de la longitud de la historia de rezagos (Sección 6.4); (iii) emparejar el contraste con el dato oficial por código y no por nombre, lo que recupera 31 celdas y 3.987 matrículas y mueve el WAPE de 11,49 % a 11,24 %; (iv) incorporar proyecciones oficiales de las exógenas, en particular la demográfica, en lugar de congelarlas; (v) dar dinámica propia a la modalidad mediante una interacción entre jornada y año; (vi) agrupamiento parcial (*partial pooling*) para regiones pequeñas [@athanasopoulos2024review]; (vii) extender el análisis a centros de formación técnica e institutos profesionales; y (viii) recalibrar los intervalos sobre una ventana que excluya los años tempranos sesgados.

# 7. Conclusiones

En una serie tan inercial como la matrícula, el pronóstico de persistencia es el referente correcto y a la vez el más fácil de medir mal, porque coincide con la variable de rezago que alimenta al modelo: un defecto en la llave de emparejamiento contaminó en este caso modelo y referente a la vez, infló el *skill* de un año y lo hundió en el siguiente, y sólo se detectó porque un pronóstico emitido antes del dato pudo contrastarse con él.

Con la persistencia bien construida, los modelos globales de *gradient boosting* tienen menos error que la persistencia en la celda, y la persistencia menos que los métodos por serie, aunque la ventaja frente a la persistencia sólo es significativa en los años con historia larga (2025 y 2026) y no en el OOF completo: sobre el dato oficial de 2026, el modelo principal redujo el WAPE de 12,69 % a 11,49 % (*skill* +26,71 %, significativo con ambas pérdidas en la celda) y el modelo global solo de rezagos llegó a 11,16 %, mientras que ETS, ARIMA y Theta por serie fueron peores que la persistencia; en el total nacional, en cambio, los métodos por serie son competitivos. El aporte de las exógenas depende del período: no mejora la celda en 2026 y sí los agregados en 2019–2025, con una ventaja concentrada en los años con poca historia y en el shock de 2022. Los intervalos conformes estratificados cubrieron el 92,53 % de las celdas en la validación de 2026 y el 92,49 % en el *holdout* 2026, con menor *interval score* que sus alternativas en casi todos los niveles, y la fuga aislada de un *target encoding* precalculado (2,92 % a 3,74 % del RMSE) supera las diferencias entre algoritmos.

Los modelos son útiles para proyectar instituciones, facultades y el agregado universitario —al lado de un referente por serie para el total—, y **no** para programas individuales ni como alerta temprana de contracción institucional. Los pronósticos 2027 del diseño factorial y de los referentes se congelaron con un protocolo que fija de antemano qué contará como éxito y qué como fracaso; el contraste de julio de 2027 dirá si el resultado de 2026 sobre las exógenas se repite.


# Disponibilidad de datos y código {-}

Todas las fuentes primarias son de acceso público y se citan como conjuntos de datos en la Tabla 1 y en la lista de referencias [@sies2025matricula; @cned2026indices; @cned2026infraestructura; @bcch2026pibregional; @ine2026ene; @mineduc2025empleabilidad]. Con el congelamiento del 20 de noviembre de 2026 (Sección 5.10) se publicaron, antes del dato oficial, los archivos de predicciones 2027 de los cuatro modelos del diseño factorial (9.069 celdas, con bandas al 90 %) y de los referentes (persistencia y Comb nacional), el protocolo de evaluación, el programa que lo ejecuta y sus huellas SHA-256. El panel consolidado, el código completo del pipeline (ingesta, consolidación, construcción de la llave del rezago, modelado, evaluación e intervalos) y las predicciones retrospectivas se depositarán en un repositorio con identificador persistente (DOI), por ejemplo Zenodo, al momento de la aceptación. Durante la revisión, estos materiales estarán disponibles a solicitud para el editor y para la verificación de reproducibilidad de la revista. Para preservar el anonimato, este manuscrito no incluye enlaces a repositorios ni a tableros públicos asociados al trabajo. \[PENDIENTE: DOI de Zenodo\]

# Declaración sobre el uso de inteligencia artificial generativa y tecnologías asistidas por IA en el proceso de redacción {-}

\[PENDIENTE: el autor debe completar esta declaración según la política de Elsevier, indicando qué herramienta se usó, con qué propósito y en qué etapas. Borrador neutral para revisar:\] Durante la preparación de este trabajo, el autor utilizó [herramienta] para [reestructurar el texto según el formato de la revista, revisar la redacción y verificar referencias bibliográficas]. Tras usar esta herramienta, el autor revisó y editó el contenido según fue necesario y asume plena responsabilidad por el contenido de la publicación.

# Financiamiento {-}

\[PENDIENTE: confirmar.\] Esta investigación no recibió financiamiento específico de agencias de los sectores público, comercial o sin fines de lucro.

# Conflicto de intereses {-}

El autor declara no tener intereses financieros en competencia ni relaciones personales conocidas que pudieran haber influido en el trabajo reportado en este artículo.

# Referencias {-}

::: {#refs}
:::
