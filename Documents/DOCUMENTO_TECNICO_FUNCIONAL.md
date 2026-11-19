---
title: "Documento técnico-funcional · Pipeline predictivo de matrícula universitaria chilena"
tags:
  - nota-tecnica
  - pipeline
  - modelo-predictivo
  - matricula
  - educacion-superior
audiencias: [puente, ejecutivo, tecnico]
status: activo
type: documento-tecnico-funcional
project: prediccion-matricula-universitaria-chile
modelo: Pipeline v4 · CatBoost
corrida: re-estimación con datos hasta 2026 · pronóstico 2027
version: "2.0"
fecha_creacion: 2026-11-18
ultima_actualizacion: 2026-11-19
author: Diego Evans Pérez Paz
---

# Documento técnico-funcional · Pipeline predictivo de matrícula universitaria chilena

> [!NOTE]
> **📌 Ficha**
>
> **Artefacto**: pipeline v4 en cinco etapas: ingesta, consolidación, modelado, resultados y validación *out-of-time*
> **Versión documentada**: re-estimación de noviembre de 2026 · corrida del 18-11-2026 · entrena con 2018-2025, evalúa a ciegas 2026 y pronostica 2027
> **Función**: pronostica la matrícula de pregrado universitario del año siguiente en cada celda institución × carrera × región × jornada × género × condición
> **Insumos**: SIES (matrícula) · CNED (aranceles y puntajes, cuerpo docente, inmuebles) · Banco Central (PIB regional) · INE (desocupación regional) · mifuturo.cl (retención) · 4 diccionarios de llaves
> **Salida**: dataset de modelado 82.967 × 52 · tabla de predicciones de 92.036 filas · modelo CatBoost con su metadata
> **Resultado**: holdout 2026 con WAPE 12,09 % frente a 12,91 % de la persistencia (*skill* +14,20 %) · pronóstico 2027 de **761.058** matrículas (+2,80 %)
> **Consumidor**: el [paper](OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md) y el [README](../README.md) del repositorio
> **Tiempo de corrida**: optimización de hiperparámetros 137,4 min; el total no se publica (§20)

**Cómo leer este documento.** Reemplaza la publicación de los notebooks: describe qué hace el pipeline en cada etapa con el detalle necesario para entenderlo, reproducir su lógica y auditar sus decisiones, pero no contiene código. Las marcas indican la audiencia: 👔 lectura ejecutiva · 🧭 puente entre negocio y técnica · 🔧 detalle técnico. §1 y §2 bastan para saber qué hace el modelo y qué no. §4 a §9 explican cada etapa con sus reglas. §15 enseña a reconstruir una cifra con una celda real. §16 a §27 son de consulta.

Tres convenciones atraviesan el documento:

1. Los números usan coma decimal y punto de miles.
2. **Ninguna métrica de error o de R² se reporta sin la de la persistencia al lado.** La matrícula es muy inercial y la comparación contra «el año siguiente será igual al actual» es la única que informa (§6.6 y §10.2).
3. Los nombres de columna se escriben en cursiva (*matriculas_lag1*) y sólo se usan cuando hacen falta para entender una regla.

Las cifras son de la corrida de noviembre de 2026, salvo las marcadas como **v4 original**: el modelo de agosto de 2026, entrenado con datos hasta 2025, cuya validación contra el dato real 2026 se conserva como evidencia *out-of-time* (§19.4).

---

## 1 · Qué resuelve este modelo 👔

La pregunta es **cuántos estudiantes de pregrado habrá el año siguiente en cada carrera de cada universidad chilena**, desagregado por región, jornada, género y condición (nuevo o antiguo), y con qué incertidumbre.

La dificultad no está en el nivel: la matrícula es tan inercial que repetir el año anterior ya acierta casi todo. Está en mejorar esa regla de forma medible y en no engañarse al medirlo. El pipeline responde en cinco pasos:

| # | Paso | Qué produce | Cifra de cierre |
|---:|---|---|---|
| 1 | **Ingerir** siete fuentes públicas | Una tabla limpia por fuente, con controles de conservación | 22.357.425 matrículas de pregrado 2007-2026, sin pérdida |
| 2 | **Consolidar** sobre la matrícula del SIES | Celdas con su año anterior, contexto e imputación | 82.967 celdas-año, 2018-2026, cero nulos |
| 3 | **Modelar** con validación temporal | Modelo CatBoost elegido sin ver el año de prueba | RMSE de CV 0,2949 en 7 *folds* |
| 4 | **Medir** contra la persistencia | Error del holdout 2026 en ocho niveles de agregación | *Skill* positivo en los 8 niveles |
| 5 | **Pronosticar y congelar** | Pronóstico 2027 fijado antes del dato real | 761.058 matrículas (+2,80 %) |

> [!TIP]
> **👔 En una frase**
>
> El modelo dimensiona, no ordena. Acierta el tamaño de la matrícula del año siguiente algo mejor que repetir el año anterior —y mucho mejor a nivel de institución o de área—, pero no anticipa puntos de inflexión ni dice qué programa va a crecer más que otro.

> [!CAUTION]
> **🚨 La regla que no se puede quebrantar**
>
> **El baseline de persistencia es la misma columna que el lag del modelo.** Si la llave que empareja cada celda con su año anterior falla, se degradan a la vez el modelo y la vara con que se lo mide, y el *skill* se sesga en una dirección imprevisible. En la versión de junio de 2026 ese defecto infló el *skill* del holdout hasta +77 % y lo hundió a −8 % en el pronóstico. La llave del lag se audita como el target (§6).

> [!WARNING]
> **⚠️ Lo que el modelo deja fuera**
>
> Institutos profesionales y centros de formación técnica (cerca de la mitad del pregrado), carreras nuevas y celdas con menos de 10 estudiantes. Ese segmento excluido es el que más crece: en 2026 creció +29,4 % frente a +2,3 % de lo modelado. **El pronóstico no es la matrícula universitaria nacional** y compararlo con el titular del SIES subpredice de forma estructural.

---

## 2 · Alcance funcional 🧭

### 2.1 · Universo

| Dimensión | Valor | Regla |
|---|---|---|
| Nivel | Pregrado | Campo de nivel global del SIES |
| Instituciones | Universidades | Categorías de nivel 2 *Universidades CRUCH*, *Universidades Privadas* y *Universidades (\* Carrera en Convenio)* |
| Ventana de entrenamiento | 2018-2026 | 2017 se usa sólo como base del lag de 2018 |
| Holdout | 2026 | Fuera de la selección de modelo y del tuning |
| Horizonte | 2027 | Un año adelante |
| Dataset final | 82.967 filas | 62 nombres de institución, 1.432 de carrera, 16 regiones, 10 áreas |
| Universo del pronóstico 2027 | 9.069 celdas de 53 instituciones | Suman 740.318 matrículas en 2026: el 97,5 % de las 759.045 universitarias de pregrado |
| **Grano** | `institución × carrera × región × jornada × género × condición × año` | Una fila es una **celda**-año |

### 2.2 · Qué queda fuera

| Exclusión | Regla | Dónde |
|---|---|---|
| Institutos profesionales y CFT | Nivel 2 distinto de las tres categorías universitarias | D1 · §5.1 |
| Posgrado y postítulo | Nivel global distinto de pregrado | D1 · §4.2 |
| Celdas pequeñas | Lag menor que 10 estudiantes | D3 · §7.4 |
| Celdas sin año anterior | Sin lag en ninguno de los tres niveles de la llave | D4 · §6.2 |
| Carreras nuevas | No tienen lag: entran al universo al año siguiente de abrir | §8.4 |

### 2.3 · Glosario

| Término | Significado en este pipeline |
|---|---|
| **Celda** | Combinación institución × carrera × región × jornada × género × condición × año. Es la unidad del modelo |
| **Condición** | Alumno nuevo (primer año) o antiguo (cohortes superiores) |
| **Lag** | Matrícula de la misma celda en el año anterior, construida con la llave en cascada (§6) |
| **Persistencia** (*naïve*) | Pronóstico «el año siguiente será igual al actual». Es numéricamente el lag |
| **Llave en cascada** | Emparejamiento de la celda con su año anterior por nombre, por código o por programa-región, en ese orden |
| ***cod_carrera_base*** | Llave de programa con los componentes de institución y carrera del código del SIES |
| ***origen_lag*** | Nivel de la llave que produjo el lag: fino, código o medio |
| **Escalado por participación** | Ajuste del lag de un respaldo agregado por la fracción que la celda representa en su grupo |
| **Target** | Arcsinh de la tasa de crecimiento interanual de la celda, winsorizada |
| **Arrastre** | Repetición del último año publicado de una exógena regional para los años que la fuente aún no publica |
| **Imputación jerárquica** | Relleno de faltantes de lo específico a lo general, en cinco capas |
| ***fue_imputado*** | Bandera: alguna variable de la fila estaba faltante antes de imputar. Entra al modelo |
| **Holdout** | Año reservado que no participa en la selección ni en el tuning |
| ***Expanding window*** | Validación cruzada temporal en que la ventana de entrenamiento crece año a año |
| **OOF** (*out-of-fold*) | Predicción de un año hecha por un modelo entrenado sólo con años anteriores |
| ***Fold-aware*** | Preprocesamiento que se ajusta dentro de cada *fold*, sólo con sus datos de entrenamiento |
| ***Target encoding*** (TE) | Codificación de una categórica por la media del target en esa categoría, suavizada hacia la media global |
| ***Ex ante* / *ex post*** | Evaluación con el contexto disponible al pronosticar / con el contexto del propio año evaluado |
| ***Out-of-time*** | Contraste de un pronóstico contra el dato real publicado después |
| **Congelamiento** | Fijación verificable del pronóstico antes de que se publique el dato real |
| **Cascada de agregación** | Ocho niveles anidados, de nacional (N1) a celda (N8), en que se mide el error |
| **WAPE** | Error absoluto total dividido por la matrícula real total, en porcentaje |
| ***Skill score*** | 1 − (RMSE del modelo / RMSE de la persistencia)². Positivo: el modelo mejora a la persistencia |
| **MASE** | MAE del modelo / MAE de la persistencia. Menor que 1 es mejor |
| **Sesgo agregado** | Diferencia relativa entre la suma predicha y la suma real |
| **Shock de nivel** | Año cuya media del target se aparta más de 1,96 desviaciones del baseline de años normales |
| **Predicción conforme** | Intervalos cuya cobertura se garantiza en muestra finita a partir de residuos de calibración |
| **Universo modelado** | Celdas con lag calculable de al menos 10 estudiantes |

---

## 3 · Arquitectura y linaje de datos 🔧

```
┌─ FUENTES PÚBLICAS (7) + DICCIONARIOS (4) ─────────────────────────────┐
│ SIES matrícula 2007-2026 · CNED aranceles, docentes, inmuebles        │
│ Banco Central PIB regional · INE desocupación · mifuturo.cl retención │
│ Diccionarios de instituciones, carreras, regiones y sedes             │
└───────────────────────────────────┬───────────────────────────────────┘
                                    ▼
┌─ A · INGESTA POR FUENTE (§4) ─────────────────────────────────────────┐
│ Limpieza, formato largo, controles de conservación por fuente         │
│ Salida: SIES de pregrado 664.727 filas · una tabla por fuente         │
└───────────────────────────────────┬───────────────────────────────────┘
                                    ▼
┌─ B · CONSOLIDACIÓN (§5–§7) ───────────────────────────────────────────┐
│ Llaves canónicas, merge desde el SIES, arrastre, imputación,          │
│ llave del lag, target, variables derivadas, filtros                   │
│ Salida: tabla consolidada 126.643 × 61 · dataset 82.967 × 52          │
└───────────────────────────────────┬───────────────────────────────────┘
                                    ▼
┌─ C · MODELADO (§9) ───────────────────────────────────────────────────┐
│ CV temporal 7 folds, shocks, TE fold-aware, baselines, Optuna,        │
│ holdout 2026, OOF 2019-2026, ajuste final y pronóstico 2027           │
│ Salida: modelo + metadata + predicciones 92.036 filas                 │
└───────────────────────────────────┬───────────────────────────────────┘
                                    ▼
┌─ D · RESULTADOS (§10–§12) ────────────────────────────────────────────┐
│ Métricas por año, región y nivel; calibración; SHAP                   │
│ Salida: 12 figuras y 9 tablas del paper                               │
└───────────────────────────────────┬───────────────────────────────────┘
                                    ▼
┌─ CONGELAMIENTO (§24.5) ───────────────────────────────────────────────┐
│ Pronóstico fijado con huella SHA-256 antes del 30 de junio            │
└───────────────────────────────────┬───────────────────────────────────┘
                                    ▼
┌─ E · VALIDACIÓN OUT-OF-TIME (§15.6) ──────────────────────────────────┐
│ SIES del año pronosticado (julio) reconstruido con las mismas reglas, │
│ emparejado por celda y medido en la cascada contra la persistencia    │
└───────────────────────────────────────────────────────────────────────┘
```

### 3.1 · Insumos

| # | Insumo | Organismo | Qué aporta | Granularidad original | Cobertura usada |
|---:|---|---|---|---|---|
| 1 | Matrícula en educación superior | MINEDUC · SIES | Target y lag | Programa × año, por género y primer año | 2007-2026, edición del 10-07-2026 |
| 2 | Base INDICES: aranceles, puntajes, duración | CNED | Precio y selectividad | Institución × programa × región × año | 2005-2026 (2026 parcial) |
| 3 | Cuerpo docente | CNED · INDICES | Composición del claustro | Institución × sede × año | 2005-2025 |
| 4 | Inmuebles | CNED · INDICES | Infraestructura | Institución × sede × año | 2005-2025 |
| 5 | PIB regional | Banco Central de Chile | Contexto macroeconómico | Región × año | 2013-2025, referencia 2018 |
| 6 | Tasa de desocupación regional por sexo | INE | Contexto macroeconómico | Región × sexo × trimestre móvil | 2015-2025 |
| 7 | Empleabilidad e ingresos | SIES · mifuturo.cl | Retención de primer año | Institución × carrera genérica × año | 2018-2025, un archivo por año |
| 8 | Diccionario sede-región | Construido sobre el CNED | Llave regional de docentes e inmuebles | 380 sedes | — |
| 9 | Diccionario de instituciones | SIES | Llave institucional canónica | 220 instituciones | — |
| 10 | Diccionario de carreras | SIES | Llave de carreras canónica | 15.940 nombres | — |
| 11 | Diccionario de regiones | Construido | Nombre de cada región en cada fuente | 16 regiones | — |

> [!WARNING]
> **⚠️ Bases fuera del repositorio**
>
> El repositorio no incluye las bases originales ni los intermedios. Todas las fuentes son públicas y se descargan desde los portales de cada organismo. Las ediciones exactas usadas están en esta tabla y en §24.2.

### 3.2 · Formato de las tablas intermedias

Todas las tablas procesadas se escriben con separador punto y coma, coma decimal y codificación UTF-8 con BOM. Así se conservan la Ñ y las tildes, y una planilla con configuración regional chilena no reinterpreta los decimales.

### 3.3 · Orden de ejecución

| Orden | Etapa | Qué hace | Salida |
|---:|---|---|---|
| 1 | A · Ingesta | Una rutina por fuente: lee, limpia, valida y escribe | Siete tablas procesadas |
| 2 | B · Consolidación | Normaliza llaves, une, arrastra, imputa, calcula lag, target y variables | Tabla consolidada y dataset de modelado |
| 3 | C · Modelado | Valida, optimiza, evalúa el holdout, genera el OOF, reentrena y pronostica | Modelo, metadata y predicciones |
| 4 | D · Resultados | Calcula métricas, cascada, calibración y SHAP | Figuras y tablas |
| 5 | E · Validación | Sólo cuando se publica el SIES del año pronosticado | Contraste *out-of-time* |

Las etapas se ejecutan siempre en ese orden, cada una sobre la salida de la anterior, con bitácora de cada ejecución. Ante el primer error la ejecución se detiene e informa dónde ocurrió (§18).

---

## 4 · Etapa A · Ingesta por fuente 🔧🧭

### 4.1 · Principio

Cada fuente se procesa por separado y conserva su granularidad original. La ingesta no une fuentes ni imputa entre ellas: sólo limpia, reestructura y verifica que no se haya perdido nada.

### 4.2 · Matrícula SIES

**Entrada.** Serie 2007-2026, una fila por programa y año, con matrícula total y de primer año por género (mujeres, hombres, no binarios o indefinidos). Se lee en Latin-1 con separador punto y coma.

| # | Regla | Detalle |
|---:|---|---|
| 1 | **Año** | Los cuatro últimos caracteres del campo de año |
| 2 | **Faltantes antes de restar** | Matrícula total y de primer año por género se rellenan con cero antes de operar, para que una resta con un faltante no produzca un faltante silencioso |
| 3 | **Antiguos** | Total menos primer año, por género, acotado en cero si la fuente trae un primer año mayor que el total |
| 4 | **Universo de nivel** | Sólo pregrado |
| 5 | **Llave por código** | Del código institución-sede-carrera-jornada-versión se extraen institución y carrera: *cod_carrera_base*. No se rompe si cambian la sede o el plan (§6) |
| 6 | **Formato largo** | Cada programa se abre en hasta seis filas (3 géneros × 2 condiciones); se eliminan las de matrícula cero |

**Controles.**

| Control | Condición | Resultado |
|---|---|---|
| Conservación en tres niveles | (A) total SIES de pregrado, (B) suma de las seis columnas, (C) suma en formato largo: B = C exacto | **22.357.425 = 22.357.425 = 22.357.425** |
| Cobertura de la llave por código | Más de 95 % de las filas de pregrado | 96,5 % (prácticamente total en el universo universitario) |
| Integridad | Cero nulos, matrícula positiva, géneros y condiciones válidos | Pasa |

**Salida.** 664.727 filas × 13 columnas: año, región, institución (código y nombre), clasificaciones de nivel 2 y 3, área, carrera, jornada, género, condición, *cod_carrera_base* y matrícula.

### 4.3 · Aranceles, puntajes y duración (CNED)

**Entrada.** Aranceles, valor de matrícula, valor del título, duración en semestres, puntajes (máximo, promedio y mínimo del promedio de matemáticas y lenguaje) y de corte (primer seleccionado, promedio, último seleccionado). La edición vigente cubre 2005-2026; 2026 trae 10.572 filas frente a 10.865 de 2025.

| # | Regla |
|---:|---|
| 1 | Se seleccionan 19 columnas y se renombran a un esquema estable |
| 2 | Se conservan sólo las filas de pregrado |

**Controles.** Están todas las columnas; el nivel sólo toma «Pregrado» y «Posgrado»; todos los años están en 2005-2026; se informan los nulos por columna.

**Salida.** 215.743 filas de pregrado (de 260.307 leídas) × 19 columnas.

### 4.4 · Cuerpo docente e inmuebles (CNED)

| | Cuerpo docente | Inmuebles |
|---|---|---|
| **Entrada** | Conteos por grado (doctor, magíster, especialidad médica), jornada (completa, media, por horas), horas y sexo, por institución, sede y año | m² de terreno, construidos y de salas; número de oficinas y salas |
| **Regla 1** | Limpieza de nombres de columna | La superficie de terreno llega como texto con punto de miles: se limpia y convierte |
| **Regla 2** | Se descartan filas sin región; el código queda como entero | — |
| **Regla 3** | Agregación a institución × región × año, sumando 19 conteos | Agregación a institución × región × año, sumando 5 magnitudes |
| **Control** | Existen las 19 columnas antes de agregar | **La suma de m² de terreno es idéntica antes y después de agregar** |
| **Salida** | 5.723 × 25, 2005-2025 | 5.510 × 10, 2005-2025 |

### 4.5 · PIB regional (Banco Central)

| # | Regla |
|---:|---|
| 1 | Encabezados desde la tercera fila del cuadro, datos desde la cuarta; el período pasa a año |
| 2 | Se excluyen el subtotal regionalizado, el extrarregional y el PIB total |
| 3 | Paso a formato largo año × región |
| 4 | Cada nombre de región se traduce a la nomenclatura canónica con 16 equivalencias explícitas |

**Controles.** Toda región traducida existe en el diccionario y toda columna tiene traducción. **Salida:** 208 filas (16 regiones × 13 años, 2013-2025).

### 4.6 · Tasa de desocupación regional (INE)

| # | Regla | Detalle |
|---:|---|---|
| 1 | **Lectura del valor** | Llega como texto con varios puntos («8.872.525.138.950.190»): el primer punto es el decimal y los demás se descartan. El ejemplo es 8,87 % |
| 2 | **Universo** | Sin total nacional; sólo la serie de **ambos sexos**, que es la tasa oficial ponderada por la fuerza de trabajo. Se verifica que no es la suma ni el promedio simple de las series por sexo |
| 3 | **Anualización** | Promedio de los períodos publicados del año |

**Control.** Se informa cuántos períodos se promediaron por región y año: 2018-2024 promedian 12 trimestres móviles; **2025 promedia 10** (§23, O-02). **Salida:** 176 filas (16 regiones × 11 años, 2015-2025).

### 4.7 · Retención de primer año (mifuturo.cl)

| # | Regla | Detalle |
|---:|---|---|
| 1 | **Extracción** | Año, institución, carrera genérica, carrera, retención de primer año, empleabilidad al primer año, ingreso al cuarto año y código institucional. Hoja, fila de encabezado y orden de columnas se declaran año por año |
| 2 | **Notas al pie** | Se descartan las filas sin año; el año de cada fila debe coincidir con el del archivo |
| 3 | **Código faltante en 2020** | Se asigna por nombre normalizado de la institución contra un diccionario de los demás años (código más frecuente). Las 1.479 filas de 2020 reciben código |
| 4 | **«s/i»** | Se trata como faltante |
| 5 | **Imputación en origen** | Con bandera previa: media institución-año → media carrera genérica-año → media carrera genérica → mediana global (sólo 3 filas llegan a la última) |

**Controles.** Están los ocho años; retención y empleabilidad en [0, 1]. **Salida:** 12.711 filas.

---

## 5 · Etapa B · Consolidación 🔧🧭

### 5.1 · Universo y ventana

Del SIES procesado se conservan 2018-2026 y las tres categorías universitarias: **127.424 filas de 60 códigos de institución** (64.261 CRUCH, 62.602 privadas y 561 de carreras en convenio). Aparte se conserva el universo universitario 2017-2026, que es el que se usa para el lag (§6).

### 5.2 · Normalización de nombres

Una sola normalización básica para todos los textos de llave: mayúsculas, sin tildes, sin puntos y con espacios simples. Con ella se construye la llave de carrera del SIES (nombre de carrera), de aranceles (nombre del programa) y de retención (carrera genérica). En docentes e inmuebles se eliminan además saltos de línea incrustados en los nombres de institución.

### 5.3 · Normalización de regiones

Un diccionario de 16 filas asocia el código INE de cada región con el nombre que usa cada fuente. Sobre él:

1. Se repara el doble *encoding* de la columna del SIES (UTF-8 leído como Latin-1).
2. Si falta la región en inmuebles, se toma la de docentes.
3. Las sedes virtuales reciben el código 99, que no coincide con ninguna región del SIES.

> [!WARNING]
> **⚠️ Defecto conocido: Ñuble**
>
> La reparación del nombre de Ñuble no surte efecto en este punto del flujo: sus 3.474 filas del SIES (2,73 % del universo) entran a las uniones sin código de región. Una corrección posterior asigna el código y vuelve a unir el PIB (cero nulos al final), pero **docentes, inmuebles y aranceles de Ñuble no encuentran coincidencia**: docentes e inmuebles caen a la mediana global y los aranceles se imputan por la cascada. Se mantiene sin corregir para no cambiar la metodología publicada (§22, P-02).

### 5.4 · Normalización de instituciones

El SIES usa su propio código, que coincide 60 de 60 con el diccionario canónico. El CNED y mifuturo.cl usan otros códigos y se mapean al del SIES **por nombre normalizado**:

| # | Paso |
|---:|---|
| 1 | Normalización básica |
| 2 | Unificación de siglas espaciadas («C F T», «I P») y expansión de la «U» aislada a «UNIVERSIDAD» |
| 3 | Expansión de abreviaturas frecuentes (enseñanza, estudios, superiores, Santiago, nacional, escuela, CFT, IP) |
| 4 | Del diccionario se eliminan las carreras en convenio y se exige que ningún nombre normalizado se repita |
| 5 | **Cinco excepciones manuales** para universidades cuyos nombres no emparejan por variantes irreductibles (apóstrofes tipográficos, guiones, siglas comerciales) |

Las excepciones se prefieren a una regla genérica porque una regla amplia podría confundir instituciones de nombre parecido; son auditables y no tienen efectos colaterales. **Cobertura:** docentes, inmuebles y aranceles 60 de 60; retención 58 de 60 (las dos restantes se imputan).

### 5.5 · Arrastre de exógenas regionales

El PIB y la desocupación no pasan por la imputación jerárquica. Si una fuente todavía no publica el último año de la ventana, sus filas quedarían vacías y el control de cero nulos detendría el pipeline. La regla de **arrastre**:

| Situación | Acción |
|---|---|
| La fuente publica hasta un año anterior al último de la ventana | Se repiten los valores regionales del último año publicado para cada año faltante |
| La fuente está al día | Nada |
| Siempre que hay arrastre | Aviso visible y registro de auditoría: fuente, último año publicado, año objetivo y años arrastrados |

Es el mismo supuesto del pronóstico —contexto congelado en el último año conocido— llevado un año atrás. **En esta corrida se arrastraron el PIB y la desocupación de 2025 a 2026** (16 valores regionales cada uno).

### 5.6 · Merge SIES-céntrico

El SIES es la tabla ancla: es la única fuente con la variable objetivo a la granularidad requerida. Todo se une por **unión izquierda** desde el SIES: ninguna fila de matrícula se pierde por falta de una fuente secundaria y no aparecen combinaciones que no existen.

**Preparación.** Para que una unión no multiplique filas, cada fuente se agrega antes a la granularidad exacta de su llave. Los aranceles se agregan por año, región, institución y carrera normalizada (196.291 → 124.856 filas): media para numéricas, primer valor para categóricas. El área del conocimiento se toma del SIES.

| # | Fuente | Llave | Granularidad |
|---:|---|---|---|
| 1 | PIB regional | año + región | Regional |
| 2 | Desocupación | año + región | Regional |
| 3 | Cuerpo docente | año + región + institución | Institución-región |
| 4 | Inmuebles | año + región + institución | Institución-región |
| 5 | Retención | año + institución + carrera normalizada | Programa |
| 6 | Aranceles | año + región + institución + carrera normalizada | Programa-región |

**Control de no inflado:** entran 127.424 filas y salen 127.424.

### 5.7 · Cobertura de las fuentes secundarias

Medida desde el SIES, antes del arrastre:

| Fuente | Combinaciones del SIES | Con dato | Cobertura |
|---|---:|---:|---:|
| PIB | 144 | 120 | 83,33 % |
| Desocupación | 144 | 128 | 88,89 % |
| Docentes | 1.205 | 842 | 69,88 % |
| Inmuebles | 1.205 | 848 | 70,37 % |
| Retención | 22.990 | 4.844 | 21,07 % |
| Aranceles | 30.702 | 19.432 | 63,29 % |

- Las 24 combinaciones sin PIB son los 16 valores regionales de 2026 (resueltos por el arrastre) y 8 años de Ñuble (resueltos por la corrección de §5.3).
- Docentes e inmuebles no tienen 2026: salen de la imputación temporal.
- La retención no tiene 2026 y, en los demás años, informa por carrera genérica: empareja con entre 22 % y 27 % de las combinaciones de cada año.

### 5.8 · Imputación jerárquica

De lo específico a lo general: cada capa resuelve sólo lo que la anterior dejó vacío. Antes de imputar se registra por fila si había algún faltante (*fue_imputado*), y esa bandera entra al modelo.

| Capa | Variables | Regla |
|---|---|---|
| 1 · Temporal | Docentes e inmuebles | Interpolación lineal en el año dentro de cada institución-región, con relleno hacia adelante y atrás |
| 2 · Jerárquica | Aranceles, puntajes, duración, retención, empleabilidad | Mediana (institución, carrera) todos los años → (institución, área, año) → (área, año) |
| 2.5 · Región y carrera | Las mismas | (región, carrera, año) → (región, carrera) → (carrera, año) → (carrera) |
| 2.7 · Institución | Las mismas | (institución, año) → (institución) |
| 3 · Terminal | Todas | Mediana global |

**Resultado** (1.292.058 valores faltantes):

| Grupo | Faltantes | Capa 1 | Capa 2 | Capas 2.5 y 2.7 | Mediana global |
|---|---:|---:|---:|---:|---:|
| Docentes e inmuebles | 590.785 | 348.445 (59,0 %) | — | — | 242.340 (41,0 %) |
| Aranceles, puntajes y retención | 701.273 | — | 701.273 (100 %) | 0 | 0 |

- Aranceles, puntajes y retención se resuelven completos en la capa 2, con la misma carrera en otros años o el área de la institución: es imputación informativa. **La retención 2026 es la mediana histórica de cada institución-carrera.**
- Docentes e inmuebles: la capa temporal resuelve el 59 % —todo 2026 repite 2025— y el 41 % cae a la mediana global, que no aporta señal. Ahí caen las institución-región sin ningún año con dato, entre ellas Ñuble.
- Las capas 2.5 y 2.7 no resuelven nada en esta corrida; se mantienen como red de seguridad.

**Bandera.** 97.075 de las 127.424 filas consolidadas (76,2 %) tienen algo imputado. En el dataset final baja de 75,3 % (2018) a 60,6 % (2025) y **es 100 % en 2026**, porque ese año faltan por construcción retención, docentes e inmuebles.

### 5.9 · Ratios del claustro

En lugar de conteos por grado —correlacionados entre sí y con el tamaño— se usan ratios sobre el total de docentes:

| Ratio | Definición | Media |
|---|---|---:|
| *pct_doctores* | Doctores / total | 0,205 |
| *pct_magister* | Magíster / total | 0,394 |
| *pct_especialistas* | Especialidad médica / total | 0,053 |
| *pct_sin_posgrado* | 1 − (doctores + magíster + especialistas) / total | 0,348 |
| *pct_horas_jornada_completa* | Horas de doctores y magíster en jornada completa / horas totales | 0,741 |

Un denominador cero da cero. *pct_sin_posgrado* es combinación lineal exacta de los otros tres: se excluye de los modelos lineales; los árboles toleran la redundancia.

### 5.10 · Saneamiento

1. Se corrigen nombres de columna con caracteres dañados.
2. Las categóricas vacías (acreditación, nivel, clasificaciones) pasan a «Sin información».
3. Se eliminan **781 duplicados exactos** (idénticos en las 61 columnas). No alteran lag ni target, que se calculan desde el SIES sin deduplicar.

**Salida:** tabla consolidada imputada de **126.643 filas × 61 columnas**.

---

## 6 · La llave del lag y el baseline de persistencia 🔧🧭

Es el componente más consecuente del pipeline y el que motivó la versión v4.

### 6.1 · El problema

*matriculas_lag1* es la matrícula de la misma celda el año anterior. Construirla exige emparejar cada celda de *t* con la de *t−1*, y eso falla cuando el SIES renombra una carrera sin cambiar su código. Con una llave por nombre literal, la celda renombrada queda sin lag y sale en silencio del universo, porque el filtro de lag mínimo descarta los lags vacíos sin informarlos.

### 6.2 · La cascada de tres niveles

El lag se calcula sobre el universo universitario 2017-2026, **antes** de deduplicar, a tres granularidades:

| Nivel | Llave | Qué empareja | Cuándo actúa |
|---|---|---|---|
| Fino | Institución + nombre de carrera + región + jornada + género + condición | La celda exacta, por nombre | La celda existe en *t−1* con el mismo nombre |
| Código | Institución + *cod_carrera_base* + región + jornada + género + condición | La misma celda, por código | Cambió el nombre pero no el código |
| Medio | Institución + *cod_carrera_base* + región | El programa en la región | La combinación fina es nueva pero el programa existía |

- El lag es el total del año anterior **sólo si ese año es exactamente *t−1***; un salto de años deja el lag vacío.
- Si una celda-año tiene más de un código, se usa el de mayor matrícula.
- El orden es fino → código → medio: el código identifica la celda exacta; el medio es una aproximación.

**Por qué institución + carrera y no un código más fino.** Agregar sede o jornada reduce colisiones, pero pierde justamente la robustez ante renombres. Medido sobre 2018-2025, institución + carrera fue la única variante con menos pérdida que el nombre literal.

### 6.3 · Escalado por participación

Los respaldos agregan dimensiones que la celda no tiene. Usar su lag crudo compara la celda contra un agregado que la contiene y produce tasas espurias cercanas a −1. Por eso se escalan:

```
lag_celda = lag_grupo × matrícula_celda,t / matrícula_grupo,t
⇒ tasa_celda = matrícula_grupo,t / lag_grupo − 1
```

La celda **hereda el crecimiento de su grupo** en vez de compararse contra su nivel.

| Propiedad | Por qué importa |
|---|---|
| lag × (1 + tasa) devuelve exactamente la matrícula de la celda | La reconstrucción no se distorsiona |
| La participación es ≤ 1 | El respaldo nunca infla |
| Si grupo = celda, la participación es 1 | El escalado no cambia nada donde no hace falta |
| El lag queda en la escala de la celda | Alimenta dos variables de mercado que suman lags (§7.2) |

> [!IMPORTANT]
> **🎯 Regla general**
>
> El numerador y el denominador de una tasa deben compartir la llave, y todo respaldo que agregue dimensiones debe escalarse por participación.

### 6.4 · Control de la composición del lag

Cada fila registra su *origen_lag*. Cada corrida imprime la composición sobre el universo universitario desde 2018, por celda y antes del filtro de lag:

| Origen | Celdas | % de la matrícula | Tasa mediana | % con tasa < −0,8 | Razón lag/celda mediana |
|---|---:|---:|---:|---:|---:|
| Fino | 102.036 | 97,80 % | 0,000 | 1,16 % | 1,000 |
| Código | 1.041 | 0,68 % | 0,000 | 1,44 % | 1,000 |
| Medio | 4.198 | 0,80 % | +0,194 | 0,45 % | 0,837 |
| Sin lag | 3.386 | 0,71 % | — | — | — |

En código y medio la razón debe rondar 1 y la tasa mediana no debe ser negativa. **Si el nivel medio vuelve a mostrar una tasa mediana cercana a −0,87 con razón cercana a 8, el escalado no se aplicó.** La llave por código recupera 42.641 matrículas en 1.041 celdas. En el dataset final: 97,94 % fino, 0,84 % código, 1,22 % medio.

**¿Los errores extremos vienen de los respaldos?** No (auditoría del 19-11-2026, corrida 2027, [`tabla_peores_por_origen_lag.md`](OUTPUTS_PAPER/tablas/tabla_peores_por_origen_lag.md)). De las 50 peores celdas por error absoluto, 49 del OOF 2019-2025 y las 50 del holdout 2026 tienen lag **fino**, es decir, la misma celda con el mismo nombre de carrera en t−1. Los respaldos pesan el 1,1 % de la matrícula y tienen más error relativo (WAPE de 17-18 % con código y de 27-31 % con medio, contra 12-14 % con fino), pero no llegan al extremo de la distribución. Las celdas peor predichas son contracciones reales de programas que siguen con el mismo nombre (por ejemplo, Pedagogía en Educación Diferencial de la U. Los Leones, 2019-2020, o Ingeniería de Ejecución Industrial a distancia de la UDLA, 2026), no defectos de la llave.

### 6.5 · Los dos defectos que motivaron la v4

La versión de junio de 2026 (v3) tenía dos defectos, detectados al contrastar su pronóstico 2026 con el dato real:

| # | Defecto | Efecto |
|---:|---|---|
| 1 | **Renombres sin respaldo por código**: el respaldo también usaba el nombre | En 2025 el SIES renombró todos los programas de una institución sin cambiar códigos, y esa institución perdió casi toda su matrícula modelable |
| 2 | **Granularidad mezclada en el respaldo medio**: agregaba jornada, género y condición sólo en el denominador | Cerca de 3.800 filas con razón lag/celda de 8 y tasa mediana de −0,875: contracciones inexistentes que el modelo aprendía como colapsos |

Juntos corrompían cerca del 4 % de los targets y, por la identidad de §6.6, el baseline en la misma proporción. La corrección fue la llave por código y el escalado por participación, sin cambiar la ventana de entrenamiento ni usar datos del año validado.

### 6.6 · El baseline de persistencia es el lag

La persistencia predice ŷ*t* = *y**t−1*: **la misma columna *matriculas_lag1* que alimenta al modelo**. No es una elección de implementación, es una identidad. Un defecto en la llave no degrada al modelo frente a un baseline sano: **degrada a los dos**, y el *skill* —un cociente entre ambos— se sesga de forma imprevisible. En v3 el mismo defecto infló el *skill* del holdout 2025 a +77 % y lo hundió a −8 % en el pronóstico 2026. De ahí cuatro reglas:

1. Auditar la llave del lag como se audita el target, publicando su composición (§6.4).
2. Vigilar la distribución del lag, no sólo la del target.
3. Tratar los saltos grandes de *skill* entre períodos como sospecha del instrumento, no como hallazgo.
4. Verificar que numerador y denominador de cada tasa compartan la llave.

---

## 7 · Target y variables derivadas 🔧

### 7.1 · El target

**Por qué una tasa.** La matrícula por celda va de decenas a cientos. Modelar el nivel haría que el error quedara dominado por las celdas grandes; con la tasa, todas quedan en escala comparable y el lag absorbe el nivel.

| Paso | Regla |
|---|---|
| Tasa | (matrícula*t* − lag*t*) / lag*t*, sólo si el lag existe y no es cero |
| Winsorización | Se acota a los percentiles 1 y 99 de todas las filas filtradas 2018-2026 (incluido el holdout, §13.3). Cortes: −0,79 y +1,29 |
| Transformación | target = arcsinh(tasa) = ln(tasa + √(tasa² + 1)) |
| Reconstrucción | matrícula = lag × (1 + sinh(target)) |

Se usa arcsinh y no logaritmo porque las tasas son con frecuencia negativas: está definido en todos los reales, es simétrico, preserva el signo, se comporta como la identidad cerca de cero y como un logaritmo en las colas, sin parámetros. Distribución del target: media 0,0025, desviación 0,3081, mediana 0,0000, asimetría 0,58, curtosis 1,56.

El dataset no conserva la matrícula del año: la «real» del período retrospectivo se reconstruye con la misma fórmula. En las celdas recortadas por la winsorización difiere del dato del SIES (0,2 % de las celdas del holdout).

### 7.2 · Variables derivadas

| Variable | Definición | Información que usa |
|---|---|---|
| *concentracion_matricula_lag* | Lag de la celda / suma de lags de la institución en el año | Año *t−1* |
| *pct_matricula_regional_lag* | Lag de la celda / suma de lags de la carrera en la región y año | Año *t−1* |
| *densidad_estudiantes_m2* | Matrícula institución-región del año / m² construidos | **Matrícula agregada del año *t*** |
| *ratio_docente_estudiante* | Docentes / matrícula institución-región del año, recortado en p99 | **Matrícula agregada del año *t*** |
| *matriculas_sobre_pib* | Matrícula regional del año / PIB regional | **Matrícula agregada del año *t*** |
| *densidad_competitiva* | Instituciones que ofrecen la misma carrera en la región y año | Oferta del año *t* |
| *arancel_relativo_regional* | Arancel / mediana regional del año | Aranceles del año *t* |
| *selectividad_relativa* | Puntaje de corte del último seleccionado / media institucional de ese puntaje | Puntajes del año *t* |

A ellas se suman los ratios del claustro, el lag y *fue_imputado*. Las tres variables con matrícula del año *t* son una excepción declarada a la regla anti-fuga (§13.2).

### 7.3 · Filtros y transformaciones finales

| Orden | Paso | Detalle |
|---:|---|---|
| 1 | Exclusión de columnas | Matrícula del año, crecimiento absoluto, conteos docentes, superficies crudas, valor del título, empleabilidad y llaves auxiliares |
| 2 | **Filtro de estabilidad** | Lag ≥ 10. Una celda que pasa de 2 a 6 crece 200 %: es ruido, no demanda |
| 3 | Filas sin target | Se descartan |
| 4 | Winsorización y arcsinh | §7.1 |
| 5 | log(1 + x) | Lag, arancel, valor de matrícula, PIB, número de docentes, densidad por m² |
| 6 | Género | Entero: mujer 0, hombre 1, no binario 2 |
| 7 | Indicadoras | Jornada (base: a distancia), condición (base: antiguos), nivel 2, nivel 3 y acreditación, sin la primera categoría |
| 8 | TE precalculado | Para región, institución, carrera y área. Queda **sólo como contraste** del experimento de fuga (§9.4); el modelo no lo usa |
| 9 | **Colapso a una fila por celda** | La tabla consolidada puede tener varias filas por celda (no incluye sede ni versión del plan); comparten lag, target y variables y quedan idénticas. No elimina matrícula |
| 10 | Control de cero nulos | Antes de escribir |

**Salida:** dataset de modelado de **82.967 filas × 52 columnas**, 2018-2026, sin nulos ni duplicados.

---

## 8 · Grano, cobertura y trazabilidad 🔧🧭

### 8.1 · Grano

Una fila del dataset es una celda-año. La tabla de predicciones agrega el tipo de registro: retrospectivo (2019-2026), histórico sin predicción (2018) o pronóstico (2027).

### 8.2 · Filas por etapa

- **S1** SIES de pregrado, todas las instituciones · **S2** universidades 2018-2026 · **S3** tabla consolidada · **S4** con target · **S5** dataset de modelado.

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
| **Total** | **311.051** | **127.424** | **126.643** | **123.159** | **82.967** |

### 8.3 · Matrícula por etapa

| Año | S1 | S2 | S3 | S4 | S5 | S5 / S2 |
|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 1.188.045 | 678.213 | 677.121 | 670.591 | 651.272 | 96,0 % |
| 2019 | 1.194.459 | 677.084 | 676.385 | 669.113 | 654.322 | 96,6 % |
| 2020 | 1.151.834 | 660.109 | 659.323 | 654.505 | 637.307 | 96,5 % |
| 2021 | 1.204.376 | 691.375 | 690.249 | 685.271 | 667.324 | 96,5 % |
| 2022 | 1.214.011 | 685.435 | 684.721 | 680.230 | 660.228 | 96,3 % |
| 2023 | 1.249.419 | 693.662 | 692.958 | 689.359 | 669.426 | 96,5 % |
| 2024 | 1.277.610 | 706.040 | 705.248 | 701.645 | 691.898 | 98,0 % |
| 2025 | 1.325.984 | 732.034 | 731.071 | 725.549 | 711.280 | 97,2 % |
| 2026 | 1.372.167 | 759.045 | 758.378 | 754.408 | 740.323 | 97,5 % |

### 8.4 · Justificación de cada caída

| Paso | Filas | Qué se elimina | Efecto en matrícula |
|---|---:|---|---|
| S1 → S2 | 311.051 → 127.424 | Instituciones no universitarias | Deliberado: las universidades son 55 % a 57 % del pregrado |
| S2 → S3 | 127.424 → 126.643 | 781 duplicados exactos | 0,12 %; no altera lag ni target |
| S3 → S4 | 126.643 → 123.159 | 3.484 filas sin lag o con lag cero | Se retiene 98,9 % a 99,5 % por año |
| S4 → S5 | 123.159 → 82.967 | 25.364 con lag < 10 y 14.828 del colapso a celda | Se retiene 97,1 % a 98,6 % por año; el colapso no elimina matrícula |

Ningún criterio depende del error de predicción: todos son estructurales y previos al modelado. **Pero no son neutrales**: lo excluido —celdas pequeñas y nuevas— es lo que más crece (§19.4).

### 8.5 · Revisión de años previos en la edición 2026 del SIES

La matrícula universitaria 2025 pasó de 731.981 a 732.034 (+53, por cinco celdas nuevas; 28 celdas cambiaron con suma neta cero). El pregrado 2025 de todas las instituciones pasó de 1.327.344 a 1.325.984.

### 8.6 · Diccionario del dataset de modelado

| Grupo | Columnas | Notas |
|---|---|---|
| Categóricas (4) | Región, institución, carrera, área | Entran al TE *fold-aware* |
| Tiempo (1) | Año | |
| Grano (6) | Género; jornada diurna, otra, semipresencial, vespertina; condición nuevo | Bases: a distancia, antiguos |
| Lag (2) | *matriculas_lag1*; *origen_lag* | Lag en log(1 + x); *origen_lag* es trazabilidad, no entra al modelo |
| Target (1) | *tasa_crecimiento* | Arcsinh de la tasa winsorizada |
| Macroeconómicas (3) | PIB, desocupación, *matriculas_sobre_pib* | PIB en log(1 + x) |
| Precio y selectividad (11) | Arancel, valor de matrícula, 3 puntajes, 3 de corte, duración, *arancel_relativo_regional*, *selectividad_relativa* | Montos en log(1 + x) |
| Claustro (7) | Número de docentes, 5 ratios, *ratio_docente_estudiante* | Docentes en log(1 + x) |
| Infraestructura (1) | *densidad_estudiantes_m2* | log(1 + x) |
| Mercado (3) | *densidad_competitiva*, *concentracion_matricula_lag*, *pct_matricula_regional_lag* | |
| Retención (1) | Retención de primer año | |
| Clasificación y acreditación (7) | 2 de nivel 2, 3 de nivel 3, 2 de acreditación | |
| Trazabilidad (1) | *fue_imputado* | Entra al modelo |
| TE precalculado (4) | Una por categórica | **Excluidas del modelo** |

Las tres indicadoras de shock se agregan en el modelado (§9.3).

---

## 9 · Etapa C · Modelado 🔧

### 9.1 · Validación temporal

**No se usa partición aleatoria**: mezclar años deja al modelo ver el futuro y produce métricas que no se sostienen en uso. Cuatro niveles:

| Nivel | Qué es | Filas |
|---|---|---:|
| 1 · Holdout 2026 | Reservado por completo; el modelo elegido se reentrena con 2018-2025 y predice 2026 | 9.069 (entrena 73.898) |
| 2 · CV *expanding window* | Cada *fold* entrena con todos los años anteriores al validado | 7 *folds* |
| 3 · OOF 2019-2026 | Cada año predicho por un modelo entrenado sólo con los anteriores, con los hiperparámetros finales | 73.462 |
| 4 · *Out-of-time* 2027 | El modelo final (2018-2026, 82.967 filas) pronostica 2027; se congela y se contrasta con el SIES 2027 | 9.069 |

| Fold | Entrenamiento | n | Validación | n |
|---:|---|---:|---:|---:|
| 1 | 2018 | 9.505 | 2019 | 9.424 |
| 2 | 2018-2019 | 18.929 | 2020 | 9.321 |
| 3 | 2018-2020 | 28.250 | 2021 | 9.230 |
| 4 | 2018-2021 | 37.480 | 2022 | 9.161 |
| 5 | 2018-2022 | 46.641 | 2023 | 9.038 |
| 6 | 2018-2023 | 55.679 | 2024 | 9.176 |
| 7 | 2018-2024 | 64.855 | 2025 | 9.043 |

La predicción OOF de 2026 coincide con la del holdout. 2018 entra al entrenamiento pero no recibe predicción. Como el entrenamiento crece con el año, el desempeño mejora en los años recientes (§10.4).

### 9.2 · Qué información ve cada evaluación

| Evaluación | Hiperparámetros | Exógenas y agregados | Estatus |
|---|---|---|---|
| CV | Se eligen aquí | Del año validado | Selección |
| OOF 2019-2025 | Elegidos con años posteriores al predicho | Del año predicho | Retrospectiva, *ex post* |
| Holdout 2026 | Elegidos sin 2026 | Mixto | Retrospectiva, ciega para la selección |
| Pronóstico 2027 | Elegidos sin 2026 ni 2027 | Congeladas en 2026 | *Ex ante* |

El holdout 2026 es mixto: aranceles y puntajes son los publicados para 2026 y los agregados de matrícula son contemporáneos, pero PIB y desocupación están arrastrados de 2025, docentes e inmuebles repiten 2025 y la retención es la mediana histórica.

### 9.3 · Shock pandémico detectado empíricamente

Para no depender de una dummy definida a mano, dos criterios explícitos.

**Criterio 1 · puntaje Z.** Con los años normales (2018, 2019, 2023, 2024, 2025, 2026) se calculan media y desviación de las medias anuales del target, y de sus desviaciones. Para cada candidato (2020-2022): |Z de la media| > 1,96 es **shock de nivel**; |Z de la desviación| > 1,96, **shock de dispersión**.

| Año | Media | Desv. | % tasas negativas | Z media | Z desv. | Clasificación |
|---:|---:|---:|---:|---:|---:|---|
| 2018 | 0,0132 | 0,3090 | 47,2 % | | | Normal |
| 2019 | −0,0070 | 0,2876 | 49,0 % | | | Normal |
| 2020 | −0,0384 | 0,2934 | 54,5 % | −4,95 | −0,52 | **Shock de nivel** |
| 2021 | 0,0126 | 0,3292 | 45,1 % | −0,02 | +1,36 | No detectado |
| 2022 | −0,0270 | 0,3202 | 55,5 % | −3,85 | +0,89 | **Shock de nivel** |
| 2023 | 0,0176 | 0,3356 | 50,3 % | | | Normal |
| 2024 | 0,0121 | 0,3072 | 48,5 % | | | Normal |
| 2025 | 0,0210 | 0,2983 | 46,2 % | | | Normal |
| 2026 | 0,0200 | 0,2823 | 44,7 % | | | Normal |

Baseline: media de medias +0,0128 (desv. 0,0103); media de desviaciones 0,3033 (desv. 0,0190).

**Criterio 2 · red de seguridad.** Un candidato con variación agregada negativa no clasificado por el criterio 1 es **shock de recaída**. Variaciones: +0,47 % (2019), −2,60 % (2020), +4,71 % (2021), −1,06 % (2022), +1,39 % (2023), +3,36 % (2024), +2,80 % (2025), +4,08 % (2026). Los dos negativos ya están clasificados.

**Tratamiento.** Tres indicadoras: *shock de nivel* vale 1 en 18.482 filas; las otras dos son constantes en cero. Sin reponderación. Lo que queda en pie es el procedimiento reproducible, no la tipología: versiones anteriores del preprocesamiento clasificaron distinto. En árboles el aporte es más de trazabilidad que de desempeño, porque el año ya entra como variable.

### 9.4 · *Target encoding fold-aware*

Carrera (1.432 categorías), institución (62), región (16) y área (10) son demasiadas para indicadoras. Se reemplazan por la media del target en la categoría, suavizada. **La trampa**: calcularla sobre todo el dataset filtra las etiquetas de validación. **La regla**: el codificador se ajusta dentro de cada *fold* con sus datos de entrenamiento, como un paso del mismo flujo que se reajusta en cada evaluación.

| Fórmula | Dónde | Parámetros |
|---|---|---|
| TE(c) = (n*c*·ȳ*c* + m·ȳ) / (n*c* + m) | Columnas precalculadas (contraste) | m = 30 |
| TE(c) = ȳ·(1 − w*c*) + ȳ*c*·w*c*, con w*c* = 1 / (1 + e^−(n*c* − k)/s) | Codificador *fold-aware* (modelo) | s = 30, k = 20 |

**Experimento controlado** (mismos hiperparámetros y *folds*):

| Configuración | RMSE de CV (arcsinh) |
|---|---:|
| TE precalculado sobre todo el dataset | 0,2853 |
| TE *fold-aware* | 0,2949 |
| Diferencia | −0,0096 |

El atajo reporta un RMSE **3,2 % mejor** del real, seis veces la distancia entre el mejor y el peor modelo tuneado. Salvedad: los brazos difieren también en la fórmula de suavizado (§23, O-05).

### 9.5 · Baselines

Holdout 2026, escala del target:

| Modelo | Descripción | RMSE | MAE | R² |
|---|---|---:|---:|---:|
| B0 | Mediana del entrenamiento | 0,2830 | 0,2015 | −0,0050 |
| B1 | Media histórica institución-carrera | 0,2929 | 0,2093 | −0,0767 |
| B2 | Ridge sólo con el lag | 0,2831 | 0,2021 | −0,0057 |
| B3 | Ridge con 43 variables (α = 10) | 0,2773 | 0,2008 | 0,0350 |
| **CatBoost tuneado** | **Modelo final** | **0,2605** | **0,1867** | **0,1480** |

La mediana del target es prácticamente cero: **B0 es la persistencia expresada en tasas**. B2 → B3 mide el aporte del contexto en un marco lineal; B3 → modelo final, el de la no linealidad.

### 9.6 · Candidatos y optimización

*Gradient boosting* porque, en datos tabulares de este tamaño (82.967 × 49), iguala o supera a las redes con menor costo, tolera faltantes y multicolinealidad, captura interacciones y admite SHAP.

| Sin tuning (7 *folds*) | RMSE de CV | R² medio sobre la tasa |
|---|---:|---:|
| CatBoost | 0,2964 ± 0,0174 | 0,086 |
| XGBoost | 0,2972 ± 0,0178 | 0,081 |
| LightGBM | 0,2980 ± 0,0179 | 0,076 |
| Random Forest | 0,3013 ± 0,0178 | 0,056 |

**Optuna**: muestreador TPE con semilla fija, poda por mediana (sin poda en los 10 primeros ensayos ni antes del tercer *fold*), 50 ensayos por modelo, objetivo = RMSE promedio de los 7 *folds* en arcsinh.

| Tuneado | RMSE de CV | Ensayos | Tiempo |
|---|---:|---:|---:|
| XGBoost | 0,2933 | 50 | 15,0 min |
| LightGBM | 0,2943 | 50 | 63,9 min |
| CatBoost | 0,2949 | 50 | 58,5 min |

| Hiperparámetro de CatBoost | Rango | Óptimo |
|---|---|---:|
| Iteraciones | 200-2.000, paso 100 | 2.000 |
| Tasa de aprendizaje | 0,005-0,15, log | 0,0376 |
| Profundidad | 4-10 | 7 |
| Regularización L2 | 0,01-30, log | 1,746 |
| Temperatura de *bagging* | 0-1 | 0,546 |
| Bordes | 32-255 | 183 |

Las iteraciones quedan en el límite superior: el óptimo podría estar fuera del rango (§22, P-08).

### 9.7 · Por qué CatBoost, aunque no gana el tuning

Queda tercero a 0,0016 (0,5 %) del primero, menos que el sesgo del TE mal aplicado: la implementación de *boosting* es prácticamente indiferente. El modelo final está **fijado por protocolo** (D11): en la corrida original SHAP no podía explicar XGBoost 3 y la explicabilidad por fila es requisito; frente a LightGBM, la elección es de continuidad metodológica. Cambiarlo sería una versión metodológica nueva. Este documento no afirma que CatBoost sea superior.

### 9.8 · *Clustering* descartado

Perfil de las 62 instituciones con nueve variables medias (docentes, cuatro ratios, arancel, valor de matrícula, puntaje de corte, densidad por m²), estandarizado, K-medias con K de 2 a 8; óptimo por silueta K = 4. Agregar el grupo como variable dejó el RMSE de CV en 0,2980 en ambos casos. La regla exige mejora mayor que 0,001: se descarta. Lo que resume ya está en el TE de institución y en el claustro.

### 9.9 · Variables del modelo

**49 variables**: 45 numéricas (ya transformadas, pasan sin cambios) y 4 categóricas con TE *fold-aware*. Son todas las columnas salvo el target, *origen_lag* y las cuatro de TE precalculado, más las tres indicadoras de shock. Sin pesos muestrales.

### 9.10 · Ajuste final y pronóstico

| Paso | Regla |
|---:|---|
| 1 | Reentrenamiento con 2018-2026 (82.967 filas) y los hiperparámetros óptimos |
| 2 | Las 9.069 celdas de 2026 se clonan como filas de 2027 |
| 3 | El lag pasa a ser la matrícula 2026 de cada celda |
| 4 | *concentracion_matricula_lag* y *pct_matricula_regional_lag* se recalculan con la matrícula 2026 de las celdas modeladas, acotadas a [0, 1] |
| 5 | Todo lo demás se congela en 2026: PIB, desocupación, aranceles, puntajes, docentes, inmuebles, retención, *densidad_competitiva*, los tres agregados de matrícula y la bandera. El año pasa a 2027 |
| 6 | El modelo predice la tasa en arcsinh y la matrícula se reconstruye con §7.1 |

> [!NOTE]
> **🧭 Qué es, en lo esencial, este pronóstico**
>
> Una transformación aprendida del lag. Los árboles no extrapolan: un año fuera del rango de entrenamiento cae en las mismas hojas que el último observado (en la v4 original, las predicciones con año 2026 y con año 2025 fueron idénticas en todas las celdas). Con las exógenas congeladas, sólo se mueven el lag y sus dos derivadas.

---

## 10 · Validación y desempeño del modelo 🧭

### 10.1 · Scorecard vigente

| Conjunto | n | R² | R² pers. | WAPE | WAPE pers. | *Skill* | MASE | Sesgo | Sesgo pers. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Holdout 2026** | 9.069 | 0,9733 | 0,9689 | **12,09 %** | 12,91 % | **+14,20 %** | 0,936 | +0,92 % | −2,60 % |
| OOF 2019-2026 | 73.462 | 0,9652 | 0,9653 | 14,13 % | 14,63 % | −0,47 % | 0,966 | +2,40 % | −0,48 % |
| OOF 2019-2025 | 64.393 | 0,9636 | 0,9646 | 14,45 % | 14,90 % | −2,90 % | 0,970 | +2,64 % | −0,15 % |

En el holdout: RMSE 20,26 matrículas por celda (persistencia 21,87), MAE 9,87, MedAE 5,90.

### 10.2 · Métricas y por qué el R² sobre niveles engaña

Sobre la tasa, el R² del holdout es **0,148 frente a −0,005 de la persistencia**. Sobre la matrícula, **0,9733 frente a 0,9689**: el aporte propio del modelo cabe en menos de un punto. Un programa de cinco años arrastra cuatro cohortes ya matriculadas; el nivel del año siguiente está casi determinado antes de la admisión. **Ningún R² sobre niveles se cita sin el de la persistencia.**

| Métrica | Definición | Qué captura | Limitación sola |
|---|---|---|---|
| RMSE | √(Σ(y − ŷ)² / n) | Error medio, penaliza los grandes | Escala y extremos |
| MAE | Σ\|y − ŷ\| / n | Error medio lineal | No distingue los grandes |
| MedAE | Mediana de \|y − ŷ\| | Error típico | Ignora la cola |
| R² | 1 − Σ(y − ŷ)² / Σ(y − ȳ)² | Varianza explicada | Dominado por la inercia |
| WAPE | 100 · Σ\|y − ŷ\| / Σy | Error ponderado por volumen | No muestra dispersión |
| Sesgo agregado | 100 · (Σŷ − Σy) / Σy | Error hacia un lado | Puede esconder compensaciones |
| ±10 % | % de grupos con error relativo ≤ 10 % | Aciertos útiles | Depende del umbral |
| *Skill* | 1 − (RMSE mod. / RMSE pers.)² | Error cuadrático eliminado | Hereda defectos del baseline |
| MASE | MAE mod. / MAE pers. | Error absoluto relativo | Menos sensible a la cola |

**WAPE y no MAPE**: el MAPE pesa igual un error de 3 en una celda de 10 que uno de 240 en una de 800. **Sobre el *skill***: no hay umbral universal; importan el signo, la estabilidad y la consistencia con el MASE. La columna «confianza» (100 − WAPE) de algunas tablas no es una probabilidad y este documento no la usa.

### 10.3 · Holdout 2026 por nivel de agregación

| Nivel | Grupos | WAPE | WAPE pers. | *Skill* | MASE | ±10 % | ±10 % pers. |
|---|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | 1 | 0,92 % | 2,60 % | +87,55 % | 0,353 | 100 % | 100 % |
| N2 + Institución | 53 | 2,60 % | 3,49 % | +43,03 % | 0,746 | 90,6 % | 92,5 % |
| N3 + Área | 413 | 4,30 % | 4,89 % | +34,20 % | 0,879 | 80,9 % | 77,5 % |
| N4 + Región | 647 | 4,68 % | 5,15 % | +16,90 % | 0,909 | 76,2 % | 74,3 % |
| N5 + Carrera | 2.739 | 8,24 % | 8,63 % | +8,60 % | 0,955 | 57,4 % | 56,3 % |
| N6 + Condición | 4.798 | 10,05 % | 10,65 % | +11,25 % | 0,944 | 49,3 % | 48,1 % |
| N7 + Género | 8.390 | 11,53 % | 12,13 % | +5,09 % | 0,951 | 42,6 % | 41,8 % |
| N8 + Jornada (celda) | 9.069 | 12,09 % | 12,91 % | +14,20 % | 0,936 | 41,6 % | 40,6 % |

Además de la cascada anidada se reportan cortes de una dimensión (región, área, jornada), más precisos que el nivel anidado de tamaño comparable porque juntan errores de signo opuesto.

### 10.4 · Por año (OOF)

| Año | n | R² | R² pers. | WAPE | WAPE pers. | *Skill* | Real | Predicho | Sesgo |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 9.424 | 0,954 | 0,967 | 14,12 % | 14,06 % | −38,58 % | 654.320 | 677.096 | +3,48 % |
| 2020 | 9.321 | 0,943 | 0,950 | 14,46 % | 15,51 % | −13,48 % | 637.304 | 666.925 | +4,65 % |
| 2021 | 9.230 | 0,967 | 0,958 | 15,13 % | 16,71 % | +21,59 % | 667.325 | 654.899 | −1,86 % |
| 2022 | 9.161 | 0,958 | 0,960 | 15,91 % | 15,96 % | −5,16 % | 660.215 | 700.931 | +6,17 % |
| 2023 | 9.038 | 0,962 | 0,966 | 15,92 % | 15,35 % | −12,08 % | 669.407 | 702.750 | +4,98 % |
| 2024 | 9.176 | 0,974 | 0,973 | 13,46 % | 13,78 % | +3,07 % | 691.894 | 700.168 | +1,20 % |
| 2025 | 9.043 | 0,979 | 0,974 | 12,34 % | 13,12 % | +20,53 % | 711.271 | 712.759 | +0,21 % |
| 2026 | 9.069 | 0,973 | 0,969 | 12,09 % | 12,91 % | +14,20 % | 740.318 | 747.102 | +0,92 % |

1. **El *skill* es negativo en cuatro de ocho años** (2019, 2020, 2022, 2023): con poca historia el modelo es peor que la persistencia; por eso el *skill* global del OOF es casi nulo.
2. **Sobrepredicción temprana** (+3,5 % a +6,2 %) que desaparece con ventanas largas (+1,20 %, +0,21 %, +0,92 % en 2024-2026).
3. **El desempeño en uso se parece al de los años recientes**, no al promedio OOF.
4. Los R² de modelo y persistencia están pegados todos los años.

### 10.5 · Por región (OOF 2019-2026)

| Región | n | WAPE | WAPE pers. | *Skill* |
|---|---:|---:|---:|---:|
| Los Ríos | 2.157 | 11,94 % | 12,49 % | −3,51 % |
| Maule | 3.310 | 12,39 % | 13,05 % | +3,49 % |
| Biobío | 7.943 | 12,50 % | 13,08 % | +1,64 % |
| La Araucanía | 4.853 | 13,11 % | 13,15 % | +0,49 % |
| Valparaíso | 8.937 | 13,39 % | 13,99 % | +18,05 % |
| Metropolitana | 28.312 | 14,42 % | 14,71 % | −5,16 % |
| Arica y Parinacota | 1.533 | 14,57 % | 14,22 % | −9,47 % |
| Coquimbo | 3.009 | 14,93 % | 16,18 % | +10,86 % |
| Ñuble | 2.002 | 15,36 % | 15,86 % | +5,99 % |
| Antofagasta | 3.046 | 15,38 % | 16,68 % | +15,91 % |
| Los Lagos | 2.912 | 16,27 % | 17,30 % | +5,67 % |
| Atacama | 1.202 | 16,43 % | 16,88 % | −1,67 % |
| Magallanes | 848 | 17,32 % | 17,63 % | −2,91 % |
| Lib. Gral. B. O'Higgins | 1.093 | 18,53 % | 24,28 % | +45,06 % |
| Tarapacá | 1.992 | 18,61 % | 18,48 % | −4,36 % |
| Aysén | 313 | 25,43 % | 25,76 % | +9,05 % |

El error se ordena en buena parte por tamaño. WAPE menor que la persistencia en 14 de 16 regiones, pero *skill* negativo en seis.

### 10.6 · Por modalidad (holdout 2026)

| Jornada | Base 2025 | Real 2026 | Predicho 2026 | Crec. real | Crec. predicho |
|---|---:|---:|---:|---:|---:|
| Diurna | 631.393 | 650.118 | 649.653 | +2,97 % | +2,89 % |
| A Distancia | 38.565 | 42.336 | 46.621 | +9,78 % | +20,89 % |
| Vespertina | 41.498 | 38.001 | 40.031 | −8,43 % | −3,54 % |
| Semipresencial | 8.265 | 8.894 | 9.579 | +7,61 % | +15,90 % |
| Otra | 1.371 | 969 | 1.218 | −29,32 % | −11,17 % |

**El modelo prolonga la tendencia de las modalidades no diurnas y no captura sus inflexiones**: sobrepredice la expansión a distancia y semipresencial y subestima las caídas vespertinas. Con la jornada como indicadora sin interacción temporal, no tiene con qué hacer otra cosa. El agregado acierta porque los errores se compensan.

### 10.7 · A qué grano aporta

| Grano | Lectura |
|---|---|
| Nacional, institución, área | Útil: *skill* +34 % a +88 %; nueve de cada diez instituciones dentro de ±10 % |
| Institución × área × región (N4) | Frontera práctica: tres de cada cuatro grupos dentro de ±10 % |
| Carrera y más abajo | Poco más de uno de cada dos grupos dentro de ±10 %; mejora marginal sobre la persistencia |
| Celda | Correlación tasa real-predicha 0,39; dirección correcta en el 60,1 %. **Dimensiona, no ordena** |

Por institución, modelo y persistencia aciertan dentro de ±10 % en proporciones similares (90,6 % y 92,5 %): el modelo gana en WAPE —cuando falla, falla menos— pero no acierta más veces a ese nivel.

---

## 11 · Incertidumbre: intervalos conformes 🔧

### 11.1 · Método

Predicción conforme dividida con α = 0,10. Con los residuos de calibración ordenados, los extremos son los de posición ⌈(n + 1)(1 − α/2)⌉ y ⌊(n + 1)α/2⌋. La corrección (n + 1) da cobertura marginal garantizada en muestra finita sin supuestos de distribución. **Mínimo 30 observaciones de calibración**: con menos se usa la banda del nivel completo; si tampoco llega, no hay intervalo.

### 11.2 · Decisiones de diseño

| # | Decisión | Razón |
|---:|---|---|
| 1 | **Estratificación por deciles del lag** (Mondrian) | El error es muy heterocedástico: una banda global sería inútil en celdas grandes y falsamente estrecha en pequeñas |
| 2 | **Calibración en el espacio del target**: banda = [lag·(1 + sinh(t̂ + r_lo)), lag·(1 + sinh(t̂ + r_hi))], acotada en cero | sinh es monótono y el lag positivo: el orden se preserva |
| 3 | **Los agregados no se suman**: cada nivel se calibra sobre ε = log(ŷ / y), por tamaño (<100, 100-500, 500-2.000, >2.000); banda [ŷ·e^−q_hi, ŷ·e^−q_lo] | Sumar bandas supone que todas las celdas yerran hacia el mismo lado |
| 4 | **Calibrar para medir ≠ calibrar para publicar** | Para medir, sólo residuos de años anteriores al evaluado; para publicar, todo el OOF |
| 5 | **El total nacional no lleva intervalo conforme** | Una observación por año. Se da un **rango indicativo no conforme** con el mayor sobre y subpronóstico del OOF |

### 11.3 · Cobertura verificada (v4 original)

| Conjunto | n | Cobertura | Objetivo | Ancho mediano | Celda mediana |
|---|---:|---:|---:|---:|---:|
| Holdout 2025 | 9.041 | 91,54 % | 90 % | 36,3 | 41 |
| *Out-of-time* 2026 | 8.729 | 92,53 % | 90 % | 37,3 | 44 |

Por nivel, la cobertura 2026 fue 98,1 % (N2), 96,6 % (N3), 94,8 % (N4), 91,8 % (N5), 92,8 % (N6), 92,6 % (N7) y 92,3 % (N8). Los intervalos son conservadores porque la calibración incluye los OOF tempranos, con sobrepredicción de hasta +6 %. Un ancho de 37 en una celda de 44 es honesto y poco informativo.

> [!NOTE]
> **Corrida 2027: banda calibrada (19-11-2026)**
>
> Mismo procedimiento sobre los residuos de la corrida 2027. Calibrada con el OOF 2019-2025, la cobertura en el holdout 2026 es de 92,35 % por celda (ancho mediano 36,5) y de 92,2 % a 94,3 % en N2-N8. Para el pronóstico se recalibra con el OOF 2019-2026. El total 2027 lleva un rango indicativo, no conforme, de 716.850 a 775.499 (§22, P-05 resuelto).

---

## 12 · Explicabilidad SHAP 🧭

### 12.1 · Variables más influyentes

Explicador exacto para árboles, muestra de 5.000 filas de entrenamiento (modelo 2018-2025):

| # | Variable | SHAP medio absoluto |
|---:|---|---:|
| 1 | Carrera (TE) | 0,0558 |
| 2 | Condición nuevo | 0,0480 |
| 3 | *matriculas_lag1* | 0,0364 |
| 4 | Jornada vespertina | 0,0266 |
| 5 | *pct_matricula_regional_lag* | 0,0229 |
| 6 | Año | 0,0219 |
| 7 | Institución (TE) | 0,0177 |
| 8 | Género | 0,0150 |
| 9 | Jornada diurna | 0,0131 |
| 10 | Puntaje máximo | 0,0118 |
| 11 | *concentracion_matricula_lag* | 0,0117 |
| 12 | Área (TE) | 0,0107 |
| 13 | Puntaje mínimo | 0,0102 |
| 14 | Corte del primer seleccionado | 0,0095 |
| 15 | Número de docentes | 0,0089 |

Las cinco primeras se exportan por fila en la tabla de predicciones.

### 12.2 · Lectura

- **La condición compite con el lag**: nuevos dependen de admisión; antiguos, de retención. Son procesos distintos.
- **El lag aparece tercero en parte por escala**: entra en logaritmo y su efecto principal está en la reconstrucción, no en la tasa.
- **La jornada vespertina** discrimina modalidad; sin interacción con el año, es un nivel fijo, no una tendencia.
- **Las macroeconómicas y las tres variables con matrícula contemporánea** no están entre las quince.
- **Las indicadoras de shock** no aparecen; el año sí, sexto.

### 12.3 · SHAP no es una señal de confianza

No hay relación utilizable entre la magnitud de las contribuciones de una celda y su error: el modelo no sabe cuándo va a fallar. La incertidumbre se estima con residuos históricos (§11), no con la introspección del modelo.

---

## 13 · Anti-fuga 🔧

### 13.1 · Reglas

| Regla | Cómo se cumple |
|---|---|
| Ninguna variable contiene la matrícula que se predice | Concentración y participación de mercado usan el lag (sufijo «_lag») |
| Ningún preprocesamiento ve las etiquetas de validación | TE dentro de cada *fold* (§9.4) |
| Nunca se valida con años anteriores al entrenamiento | *Expanding window*; holdout = último año |
| El año de prueba no participa en la selección | Holdout fuera del CV y del tuning |
| El pronóstico se fija antes del dato real | Congelamiento (§24.5) |

### 13.2 · Excepción declarada: tres variables con matrícula del año *t*

*densidad_estudiantes_m2*, *ratio_docente_estudiante* y *matriculas_sobre_pib* usan la matrícula del año agregada por institución-región o por región. La celda es una parte pequeña del agregado, pero el agregado se mueve con sus celdas. Consecuencias: métricas retrospectivas algo optimistas, y entrenamiento y pronóstico ven cosas distintas (en el pronóstico quedan congeladas). Lo que acota el problema: ninguna está entre las quince más influyentes y, en la validación 2026 de la v4 original, con las tres congeladas, el *skill* no fue menor que en el holdout. Es compatible con un efecto pequeño, pero no lo mide: falta una ablación (§22, P-04).

### 13.3 · Imperfecciones declaradas

| # | Imperfección | Por qué se mantiene |
|---:|---|---|
| 1 | Hiperparámetros elegidos con el CV reutilizados en los OOF de años anteriores | Las cifras OOF tempranas son indicativas; el holdout no tiene el problema |
| 2 | El año de holdout entra en el baseline de años normales y en los percentiles de winsorización | Son umbrales sobre muchas filas que no entregan etiquetas; se mantienen para replicar la metodología publicada |
| 3 | Los denominadores de las variables de mercado se suman distinto en entrenamiento (tabla consolidada) y en pronóstico (celdas modeladas) | Efecto no medido |

---

## 14 · Reglas de negocio y decisiones que implementa 🧭

| Regla | Enunciado | Dónde vive |
|---|---|---|
| **D1** | Sólo pregrado universitario | §2.1, §5.1 |
| **D2** | La unidad es la celda institución × carrera × región × jornada × género × condición | §2.1 |
| **D3** | Sólo celdas con lag ≥ 10 | §7.3 |
| **D4** | Lag por llave en cascada fino → código → medio, con escalado por participación | §6 |
| **D5** | Target = arcsinh de la tasa winsorizada en p1-p99 | §7.1 |
| **D6** | Validación temporal; nunca partición aleatoria; holdout = último año | §9.1 |
| **D7** | *Target encoding* sólo dentro de cada *fold* | §9.4 |
| **D8** | Toda métrica se reporta con la de la persistencia al lado | §10 |
| **D9** | Exógena regional faltante: arrastre del último año publicado, con registro | §5.5 |
| **D10** | Imputación de lo específico a lo general; la bandera entra al modelo | §5.8 |
| **D11** | Modelo final CatBoost por protocolo | §9.7 |
| **D12** | Pronóstico con contexto congelado en el último año observado | §9.10 |
| **D13** | Los intervalos agregados se calibran por nivel; no se suman | §11.2 |
| **D14** | Pronóstico congelado antes del 30 de junio del año pronosticado | §24.5 |
| **D15** | Una re-estimación no cambia parámetros metodológicos | §24.6 |

---

## 15 · Cómo demostrar un cálculo 🧭

### 15.1 · Qué se demuestra con la salida y qué requiere los insumos

| Factor | ¿Se demuestra con la tabla de predicciones? | Para reconstruirlo desde el origen |
|---|---|---|
| Matrícula real de la celda | Sí (*matriculas_real*) | SIES, reglas §4.2 |
| Lag | Sí (*matriculas_lag*) | SIES del año anterior, llave §6 |
| Predicción | Sí: lag × (1 + sinh(*tasa_pred_arcsinh*)) | Modelo y variables de la celda |
| Error y persistencia | Sí | — |
| Variables del modelo | Parcial: cinco de contexto y cinco SHAP | Dataset de modelado |

### 15.2 · Procedimiento para cualquier celda

| Paso | Qué mirar | Cómo se verifica |
|---:|---|---|
| 1 | Ubicar la celda | Filtrar por año, región, institución, carrera, jornada, género y condición |
| 2 | Pasar de tasa a matrícula | predicción = lag × (1 + sinh(tasa en arcsinh)) |
| 3 | Comparar con la persistencia | La persistencia es el lag |
| 4 | Agregar | Sumar real y predicho dentro del grupo; nunca promediar porcentajes |

### 15.3 · Demostración completa: una celda de Psicología

**Celda**: Región Metropolitana · una universidad privada · Psicología · diurna · mujeres · nuevas. Se eligió por ser una celda de tamaño mediano-grande en que el modelo mejora a la persistencia y que sigue en el pronóstico 2027. La institución no se nombra: el ejemplo ilustra el cálculo, no evalúa a nadie.

**Paso 1 · Holdout 2026**

| Qué | Valor | Columna |
|---|---:|---|
| Matrícula 2025 (lag) | 182 | *matriculas_lag* |
| Matrícula real 2026 | 198 | *matriculas_real* |
| Tasa real | +8,79 % | *tasa_real* |
| Tasa predicha en arcsinh | 0,13878 | *tasa_pred_arcsinh* |
| Bandera de imputación | 1 (como todas las celdas 2026) | *fue_imputado* |

**Paso 2 · De la tasa a la matrícula**

```
tasa predicha     = sinh(0,13878)       = 0,13923
matrícula 2026    = 182 × (1 + 0,13923) = 207,3
```

**Paso 3 · Contra la persistencia**

| | Predicción | Error | Error relativo |
|---|---:|---:|---:|
| Modelo | 207,3 | +9,3 | +4,7 % |
| Persistencia | 182 | −16 | −8,1 % |

En esta celda el modelo anticipó el crecimiento (+13,9 % frente a +8,8 % real) y quedó más cerca que repetir 2025.

**Paso 4 · Pronóstico 2027 de la misma celda**

```
lag 2027          = matrícula real 2026          = 198
tasa en arcsinh   = 0,06421   →  tasa = sinh(0,06421) = 0,06426
matrícula 2027    = 198 × (1 + 0,06426)          = 210,7
```

**Paso 5 · De la celda al total nacional**

| Nivel | Cálculo | Valor |
|---|---|---:|
| Holdout 2026, real | Suma de 9.069 celdas | 740.318 |
| Holdout 2026, modelo | Suma de predicciones | 747.102 (+0,92 %) |
| Holdout 2026, persistencia | Suma de lags 2025 | 721.092 (−2,60 %) |
| Pronóstico 2027 | Suma de 9.069 predicciones sobre base 740.318 | **761.058 (+2,80 %)** |

### 15.4 · Variante: celda con lag por respaldo

*Ejemplo ilustrativo con números redondos.* Una carrera cambia de nombre en 2026 sin cambiar código. El nivel fino no encuentra 2025; el nivel por código sí, y la celda recibe su lag sin escalar (la llave identifica la misma celda). Si en cambio la celda es una jornada nueva de un programa que existía, actúa el nivel medio: el programa en la región tenía 400 en 2025 y 440 en 2026, y la celda nueva tiene 44. El lag escalado es 400 × 44 / 440 = 40, y la tasa de la celda es +10 %: la del programa. Sin escalado, el lag sería 400 y la tasa −89 %, la contracción espuria de §6.5.

### 15.5 · Cómo auditar el punto de partida contra las cifras oficiales

No requiere el pipeline, sólo la base pública del SIES:

| Paso | Acción | Debe dar (2026) |
|---:|---|---:|
| 1 | Descargar la base de matrícula 2007-2026 (edición del 10-07-2026) | — |
| 2 | Tomar el año de los cuatro últimos caracteres del campo de año | — |
| 3 | Sumar la matrícula total sin filtro de nivel | **1.497.548** |
| 4 | Filtrar nivel global «Pregrado» | **1.372.167** (columna S1 de §8.3) |
| 5 | Filtrar además las tres categorías universitarias de nivel 2 | **759.045** (S2; para 2025, 732.034) |

Son las cifras del informe oficial del SIES 2026. Si coinciden, el punto de partida es correcto y cada etapa se sigue con las tablas de §4 a §8.

| Etapa | Qué verificar | Referencia |
|---|---|---|
| Ingesta del SIES | Conservación exacta; antiguos = total − primer año, acotado en cero | §4.2 |
| Uniones | Mismas filas antes y después; coberturas | §5.6, §5.7 |
| Exógenas | Registro de arrastres | §5.5, §21 |
| Imputación | Faltantes por grupo y capa; prevalencia de la bandera | §5.8 |
| Lag | Composición por nivel y controles del nivel medio | §6.4 |
| Filtros | Filas y matrícula por etapa | §8 |
| Resultados | Siempre con la persistencia al lado | §10 |

### 15.6 · Cómo auditar un pronóstico contra el dato publicado

| Paso | Acción |
|---:|---|
| 1 | Verificar que el archivo de predicciones tenga la huella SHA-256 registrada al congelar |
| 2 | Reconstruir la matrícula real con §4.2 y §5.1 y verificarla contra el informe oficial |
| 3 | Emparejar por celda y separar: cubiertas, sólo en el pronóstico (programas extinguidos), sólo en la realidad (fuera del universo) |
| 4 | Sobre las cubiertas, calcular WAPE, sesgo, *skill* y MASE **del modelo y de la persistencia** en los ocho niveles |
| 5 | Descomponer la brecha con el titular oficial en error del modelo, extinciones y matrícula fuera del universo (§19.4) |
| 6 | Registrar la revisión que la nueva edición hizo del año base |

### 15.7 · Preguntas frecuentes de cálculo

**¿Por qué el pronóstico 2027 no se compara con el titular del SIES 2027?**
Porque cubre el universo modelado, no todas las carreras. En 2026 lo excluido creció +29,4 % y lo cubierto +2,3 % (§19.4). La comparación válida es por celda emparejada.

**¿Por qué la matrícula real de una celda puede no coincidir con el SIES?**
Porque el dataset la reconstruye desde el target winsorizado. Coincide en el 99,8 % de las celdas del holdout; en el resto la tasa fue recortada (§7.1).

**¿Por qué el modelo acierta casi exacto el total nacional del holdout?**
Porque los errores de signo opuesto se compensan, en particular entre modalidades (§10.6). Una sola observación no prueba calibración.

**¿Puedo sumar los intervalos de las celdas para tener el de una institución?**
No. Cada nivel se calibra sobre su propio error (§11.2, D13).

**¿Por qué el *skill* del holdout 2026 (+14,2 %) es menor que el de la validación 2026 de la v4 original (+26,7 %)?**
Miden el mismo año con instrumentos distintos: universo modelado de cada corrida frente a celdas emparejadas con el dato publicado, y lags distintos. Signo y orden de magnitud son estables.

**¿Por qué todas las celdas de 2026 y 2027 tienen *fue_imputado* = 1?**
Porque retención, docentes e inmuebles no tienen 2026 en sus fuentes (§5.8). Es un patrón que no ocurre en años previos y su efecto no está medido (§23, O-03).

**¿Una predicción con decimales es un error?**
No. El modelo predice tasas y la reconstrucción da decimales; se redondea sólo al presentar.

---

## 16 · Especificación de los resultados 🔧

### 16.1 · Artefactos de cada corrida

Cada corrida produce tres artefactos con la misma marca de fecha y hora. No se publican en el repositorio; se registran con su huella al congelar (§24.5).

| Artefacto | Contenido |
|---|---|
| Modelo | El flujo completo de preprocesamiento y CatBoost, serializado |
| Metadata | Hiperparámetros, variables, categóricas, filas, validación, holdout y pronóstico, mejor RMSE de CV, métricas, baselines, shocks, supuestos, huella del dataset y versiones de librerías |
| Predicciones | 92.036 filas: 73.462 retrospectivas, 9.505 de 2018 sin predicción y 9.069 de pronóstico |

### 16.2 · Diccionario de la tabla de predicciones

| Columna | Qué es |
|---|---|
| *anio*, *region*, *institucion*, *carrera*, *area_conocimiento*, *jornada*, *genero*, *condicion* | La celda |
| *tipo_registro* | retrospectivo, historico_sin_pred o forecast |
| *matriculas_lag* | Matrícula del año anterior: la persistencia |
| *matriculas_real* | Matrícula del año (vacía en el pronóstico) |
| *tasa_pred_arcsinh*, *tasa_pred* | Tasa predicha en arcsinh y en escala natural |
| *tasa_real* | Tasa observada |
| *matriculas_pred* | lag × (1 + *tasa_pred*) |
| *residuo_tasa*, *residuo_matriculas*, *error_absoluto_pct* | Errores de la celda |
| *fue_imputado* | Bandera de imputación |
| *densidad_competitiva*, *arancel_relativo_regional*, *concentracion_matricula_lag*, *selectividad_relativa*, *matriculas_lag1_log* | Contexto para lectura |
| *shap_top1* a *shap_top5* | Contribuciones de carrera, condición nuevo, lag, jornada vespertina y participación regional |
| *cluster_arquetipo* | Vacía: el *clustering* se descartó (§9.8) |
| *confianza_bloque* | Indicador de presentación heredado; no es una probabilidad (§10.2) |

### 16.3 · Lo que se publica en el repositorio

| Carpeta | Contenido |
|---|---|
| [OUTPUTS_PAPER/figuras](OUTPUTS_PAPER/figuras/) | 12 figuras de la corrida vigente |
| [OUTPUTS_PAPER/tablas](OUTPUTS_PAPER/tablas/) | 9 tablas en Markdown |
| [OUTPUTS_PAPER](OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md) | El paper |

---

## 17 · Parámetros 🔧

| Parámetro | Valor vigente | Efecto |
|---|---|---|
| Lag mínimo | 10 | Define el universo modelado |
| Winsorización | Percentiles 1 y 99 | Acota la tasa antes de arcsinh |
| Umbral de shock | \|Z\| > 1,96 | Clasifica años candidatos |
| Años normales | 2018, 2019, 2023-2026 | Baseline del detector de shocks |
| Años candidatos | 2020-2022 | Se evalúan como shock |
| Suavizado TE | s = 30, k = 20 (*fold-aware*); m = 30 (precalculado) | Peso de la media global |
| Ensayos de Optuna | 50 por modelo | Búsqueda de hiperparámetros |
| Poda | Mediana; sin poda en 10 ensayos ni antes del 3.er *fold* | Aborta ensayos poco prometedores |
| Regla de inclusión de variables | Mejora de RMSE de CV > 0,001 | Descartó el *clustering* |
| Semilla | 42 | Numérico global, K-medias, modelos, Optuna, muestra SHAP |
| Nivel de los intervalos | α = 0,10 | Bandas al 90 % |
| Mínimo de calibración | 30 | Por estrato |
| Muestra SHAP | 5.000 filas | Importancias globales |
| Plazo de congelamiento | 30 de junio del año pronosticado | §24.5 |

---

## 18 · Controles, guards y validaciones 🔧🧭

El pipeline está diseñado para **fallar en voz alta**: si una condición estructural no se cumple, se detiene en vez de seguir con datos dudosos.

| Control | Etapa | Condición | Resultado 18-11-2026 |
|---|---|---|---|
| Conservación del SIES | A | Suma en formato largo = suma original | OK: diferencia 0 |
| Llave por código | A | > 95 % de filas de pregrado | OK: 96,5 % |
| Esquema de aranceles | A | Columnas, niveles y años válidos | OK |
| Conservación de superficie | A | m² de terreno iguales antes y después | OK |
| Rango de retención | A | Proporciones en [0, 1]; ocho años | OK |
| Existencia de entradas | B | Todas las tablas y diccionarios | OK |
| No inflado del merge | B | Filas iguales tras seis uniones | OK: 127.424 = 127.424 |
| Imputación completa | B | Sin faltantes en las variables imputadas | OK |
| Unicidad institucional | B | Ningún nombre normalizado repetido | OK |
| Composición del lag | B | Medio con razón ≈ 1 y tasa mediana ≥ 0 | OK: 0,837 y +0,194 |
| Cero nulos al exportar | B | Dataset sin faltantes | OK |
| Tamaño esperado | C | Filas = las registradas para la corrida | OK: 82.967 |
| Integridad del dataset | C | Sin nulos ni duplicados; años 2018-2026; cuatro categóricas | OK |
| Reconstrucción no negativa | C | Toda matrícula reconstruida ≥ 0 | OK |

**Controles de una corrida nueva** (no detienen, se revisan antes de publicar):

| Control | Valor esperado |
|---|---|
| Totales del SIES contra el informe oficial | Coincidencia exacta (§15.5) |
| Caída de filas por institución entre T−1 y T | Más de 30 % en una institución es la firma de un renombre masivo |
| Cobertura de fuentes | Comparable a la corrida anterior |
| *Skill* del holdout | Comparable al anterior; un salto grande se investiga |
| Plausibilidad del pronóstico | Contrastado con reglas simples (§19.3) |

---

## 19 · Resultados de referencia 📊

Cifras contra las que se comparará la próxima corrida.

### 19.1 · La corrida

| Elemento | Valor |
|---|---|
| Versión | Pipeline v4 re-estimado con datos hasta 2026 |
| Dataset | 82.967 filas, 2018-2026 |
| Entrenamiento del holdout | 73.898 filas (2018-2025) |
| Entrenamiento final | 82.967 filas (2018-2026) |
| CV | 7 *folds*, validación 2019-2025; CatBoost 0,2949 |
| Holdout | 2026, 9.069 celdas |
| OOF | 2019-2026, 73.462 celdas-año |
| Pronóstico | 2027, 9.069 celdas de 53 instituciones |

### 19.2 · Pronóstico 2027

| Concepto | Valor |
|---|---:|
| Base 2026 | 740.318 |
| **Pronóstico 2027** | **761.058** |
| **Crecimiento** | **+2,80 %** |

| Jornada | Crecimiento pronosticado |
|---|---:|
| Diurna | +2,32 % |
| A Distancia | +16,49 % |
| Semipresencial | +11,01 % |
| Vespertina | −5,53 % |
| Otra | −22,95 % |

Dado el holdout (§10.6), A Distancia y Semipresencial deben leerse como prolongación de tendencia, con riesgo de sobrepredicción.

### 19.3 · Contraste con reglas simples

| Regla | Pronóstico 2027 | Crecimiento |
|---|---:|---:|
| Modelo | 761.058 | +2,80 % |
| Tendencia lineal 2018-2026 | 730.661 | −1,30 % |
| Promedio de años normales | 765.596 | +3,41 % |
| Arrastre del crecimiento 2025-2026 | 770.551 | +4,08 % |

El modelo queda dentro del rango de las reglas basadas en crecimiento reciente y por debajo del arrastre del último año.

### 19.4 · Evidencia *out-of-time*: validación 2026 de la v4 original

La v4 original (agosto de 2026, entrenada con 2018-2025) pronosticó 2026 y se contrastó con el SIES del 10-07-2026. Ningún dato de 2026 entró al modelo, pero la corrección de la llave la motivó el mal resultado de v3 contra ese dato: es *out-of-sample* pero **no pre-registrada**. La prueba pre-registrada es el pronóstico 2027.

| | Celdas | Matrículas 2026 |
|---|---:|---:|
| Universo real (universidades, pregrado) | 11.570 | 759.045 |
| Cubiertas por el pronóstico | 8.729 | 721.747 (95,09 %) |
| Sólo en el pronóstico (extinguidas) | 312 | 5.611 predichas |
| Sólo en la realidad (fuera del universo) | 2.841 | 37.298 |

| 8.729 celdas | RMSE | MAE | R² | WAPE | Sesgo |
|---|---:|---:|---:|---:|---:|
| Modelo | 19,49 | 9,50 | 0,9760 | **11,49 %** | **−0,01 %** |
| Persistencia | 22,77 | 10,49 | 0,9673 | 12,69 % | −2,32 % |

**Skill +26,71 %; MASE 0,906**, positivo en los ocho niveles (máximo +48,9 % en institución × área). Crecimiento predicho +2,26 %, observado +2,27 %. Por institución, 40 de 53 dentro de ±5 % y 49 de 53 dentro de ±10 %.

**Sesgo de selección del universo.** Lo modelado creció +2,27 %; lo excluido, **+29,41 %**; el sistema, +3,69 %.

| Brecha entre pronóstico (727.260) y titular SIES (759.045) | Matrículas |
|---|---:|
| Error del modelo en las celdas cubiertas | −98 |
| Pronóstico sobre celdas extinguidas | +5.611 |
| Matrícula real fuera del universo | −37.298 |
| **Total** | **−31.785** |

**Lo que mostró que el modelo no hace bien:** sobrepredijo las cuatro modalidades no diurnas (A Distancia: 16,3 % predicho frente a 7,3 % real); correlación de tasas 0,365 y dispersión predicha menor que la mitad de la real; quedó por encima del real en las 14 instituciones que cayeron; y para el titular agregado, arrastrar el crecimiento del año anterior quedó a −0,08 % del real. El valor del modelo está en la desagregación.

---

## 20 · Volumetría y performance 🔧🧭

### 20.1 · Volumen

| Objeto | Filas | Columnas |
|---|---:|---:|
| SIES de pregrado en formato largo | 664.727 | 13 |
| Aranceles de pregrado | 215.743 | 19 |
| Tabla consolidada imputada | 126.643 | 61 |
| Dataset de modelado | 82.967 | 52 |
| Tabla de predicciones | 92.036 | 31 |

### 20.2 · Tiempo de corrida

| Fase | Tiempo |
|---|---:|
| Optuna XGBoost | 15,0 min |
| Optuna LightGBM | 63,9 min |
| Optuna CatBoost | 58,5 min |
| **Subtotal de optimización** | **137,4 min** |

El tiempo total de la corrida no se publica; la optimización es la mayor parte.

### 20.3 · Memoria

No medida.

---

## 21 · Supuestos, limitaciones y riesgos ⚠️

| # | Supuesto, limitación o riesgo | Impacto | Estado |
|---:|---|---|---|
| 1 | **PIB 2026 arrastrado desde 2025** | 2026 y el pronóstico ven el contexto regional de 2025 | Supuesto declarado |
| 2 | **Desocupación 2026 arrastrada; 2025 con 10 de 12 trimestres** | El modelo no ve el alza de desocupación de 2026 | Supuesto declarado |
| 3 | **Docentes e inmuebles 2026 = 2025** | Claustro e infraestructura congelados un año | Supuesto declarado |
| 4 | **Retención 2026 = mediana histórica** | Sin información propia de 2026 | Supuesto declarado |
| 5 | **CNED con 2026 parcial** | Más imputación de aranceles y puntajes en 2026 | Supuesto declarado |
| 6 | **Exógenas de 2027 congeladas en 2026** | El pronóstico es una transformación del lag | Por diseño (D12) |
| 7 | **Bandera = 1 en todo 2026 y 2027** | Patrón que no ocurre en años previos | Efecto no medido |
| 8 | **Metodología v4 sin cambios** | Replica también sus imperfecciones | Por diseño (D15) |
| 9 | **Ñuble sin código en las uniones institucionales** | Docentes e inmuebles en mediana global; aranceles imputados | Pendiente P-02 |
| 10 | **Sólo universidades; lo excluido crece más** | Subpredicción estructural del titular nacional | Por diseño (D1) |
| 11 | **Señal débil a nivel de celda** | Correlación ≈ 0,4; dirección correcta en 60 % | Aceptado |
| 12 | **No anticipa inflexiones**, en particular no diurnas | Sobrepredicción de A Distancia y Semipresencial | Pendiente P-06 |
| 13 | ***Skill* negativo en cuatro de ocho años OOF** | Con poca historia el modelo es peor que la persistencia | Aceptado |
| 14 | **Tres variables con matrícula contemporánea** | Métricas retrospectivas algo optimistas | Pendiente P-04 |
| 15 | **Imputación extensa**: 70,9 % de las filas; 41 % de docentes e inmuebles en mediana global | Señal débil en esas variables | Aceptado |
| 16 | **Regiones pequeñas con error alto** (Aysén, Tarapacá) | Menos confiabilidad regional | Aceptado |
| 17 | **Shocks sensibles al preprocesamiento** | Dos de tres indicadoras constantes | Aceptado |
| 18 | **Óptimo de iteraciones en el borde** | Posible mejora fuera del rango | Pendiente P-08 |
| 19 | **Intervalos conservadores; total nacional sin garantía** | Bandas anchas | Aceptado |
| 20 | **Validación 2026 de la v4 original no pre-registrada** | Evidencia más débil que la de 2027 | Se resuelve con P-01 |
| 21 | **Validación 2026 emparejada por nombre** | Por código se recuperan 31 celdas y 3.987 matrículas | Pendiente P-07 |

> [!WARNING]
> **⚠️ Lo que este modelo no cubre**
>
> No es causal: SHAP describe asociaciones. No sirve como alerta temprana de contracción institucional: en 2026 subestimó todas las caídas. No ordena programas: usarlo para decidir qué cerrar o expandir sería un mal uso. No se usa para decisiones sobre postulantes individuales.

---

## 22 · Pendientes 🧭

| # | Pendiente | Tipo | Qué destraba |
|---|---|---|---|
| P-01 | **Congelar el pronóstico 2027** con huella SHA-256 y etiqueta publicada antes del 30-06-2027 | Protocolo | La primera prueba pre-registrada del pipeline corregido |
| P-02 | Corregir la región de Ñuble antes de las uniones institucionales | Datos | Docentes, inmuebles y aranceles de Ñuble. Es una versión metodológica nueva |
| P-03 | ~~Corregir la metadata que registra cinco *folds*~~ **Resuelto el 19-11-2026**: la metadata registra siete *folds* con sus años, y el código los deriva de la partición ejecutada | Trazabilidad | Que la metadata diga lo ejecutado (siete) |
| P-04 | Ablación de las tres variables con matrícula contemporánea | Método | Medir cuánto optimismo introducen |
| P-05 | ~~Recalibrar los intervalos conformes para la corrida 2027~~ **Resuelto el 19-11-2026** (§11) | Método | Publicar el pronóstico 2027 con banda |
| P-06 | Evaluar interacción jornada × año | Método | Inflexiones de las modalidades no diurnas |
| P-07 | Emparejar la validación *out-of-time* por código de carrera | Método | 31 celdas y 3.987 matrículas más en el contraste |
| P-08 | Ampliar el rango de iteraciones de CatBoost | Método | Saber si el óptimo está fuera del rango |
| P-09 | Repetir la corrida cuando el INE complete 2025 y publique 2026 | Datos | Desocupación sin promedio parcial ni arrastre |

---

## 23 · Observaciones del levantamiento 🔎

> [!IMPORTANT]
> **🎯 Alcance**
>
> Revisión de la corrida del 18-11-2026 y de sus salidas, hecha al escribir este documento. No se modificó el pipeline.

| # | Hallazgo | Evidencia | Impacto | Sugerencia |
|---|---|---|---|---|
| O-01 | **La metadata registraba cinco *folds*** (cerrada el 19-11-2026) | La partición impresa en la ejecución tiene siete (2019-2025); la metadata ya lo dice | Bajo: trazabilidad | P-03 |
| O-02 | **La desocupación 2025 promedia 10 de 12 trimestres y el control la acepta** | Conteo de períodos por región y año (§4.6) | Medio: el valor 2025 se arrastra a 2026 y 2027 | Exigir año completo o declararlo |
| O-03 | ***fue_imputado* = 1 en el 100 % de 2026** | §5.8 | Desconocido: patrón ausente en años previos | Medir con una ablación |
| O-04 | **La huella del dataset cubre sólo los primeros 8.192 bytes** | Metadata de la corrida | Bajo: no detecta cambios en filas posteriores | Huella del archivo completo |
| O-05 | **El experimento de TE confunde fuga y fórmula de suavizado** | §9.4 | Bajo: el 3,2 % no es una medición pura | Repetir con la misma fórmula |
| O-06 | **Las capas 2.5 y 2.7 de imputación no resuelven nada** | §5.8 | Nulo | Mantener como red de seguridad |

---

## 24 · Ciclo de actualización anual y cómo re-ejecutar 🔧

### 24.1 · Dependencias

Sea **T** el último año con matrícula SIES publicada.

1. **Sin el SIES del año T no hay nada que reentrenar**: aporta a la vez target y lag.
2. **Para pronosticar T+1 basta con datos hasta T**: el pronóstico clona las celdas de T y congela el contexto.

### 24.2 · Calendario de publicación

| Fuente | Organismo | Publicación habitual del año T | Observado |
|---|---|---|---|
| Matrícula | SIES | Julio de T | 15-07-2025 (2025); 10-07-2026 (2026) |
| Docentes e inmuebles | CNED | Diciembre de T | Edición con 2025: 04-12-2025 |
| Aranceles y puntajes | CNED | Incluye T con cobertura parcial | La edición vigente trae 2026 |
| Empleabilidad y retención | mifuturo.cl | Diciembre de T | Edición 2025: 27-12-2025 |
| Desocupación regional | INE | Año completo hacia el primer trimestre de T+1 | 2025 con 10 de 12 trimestres |
| PIB regional | Banco Central | Anual, rezago variable; puede cambiar de referencia | Último año 2025 (referencia 2018) |

### 24.3 · Si falta una fuente del año T

| Fuente | ¿Obligatoria? | Si falta |
|---|---|---|
| Matrícula SIES | **Sí** | Esperar la publicación |
| PIB, desocupación | No | Arrastre con registro (§5.5) |
| Docentes, inmuebles | No | La imputación temporal repite el último año |
| Aranceles, puntajes, retención | No | Mediana histórica institución × carrera |

Un **cambio de base** de una exógena (nueva referencia del PIB) reemplaza la serie completa; nunca se empalma. Cada edición del SIES revisa el año anterior: se entrena con la disponible al congelar y se valida con la siguiente, registrando la revisión.

### 24.4 · Matriz de decisión

| Escenario | Datos | Acción |
|---|---|---|
| A | Nada nuevo | El modelo vigente sigue vigente |
| B | Contexto nuevo, sin SIES de T | Ingestar; no reentrenar |
| C | SIES de T y un pronóstico congelado de T | Validar *out-of-time* |
| D | SIES de T y parte del contexto | Reentrenar con arrastre o imputación y pronosticar T+1 |
| E | SIES de T y todo el contexto | Reentrenamiento completo y pronóstico T+1 |

En julio, al publicarse el SIES, primero se valida (C) y después se reentrena (D o E).

### 24.5 · Protocolo de congelamiento

| # | Regla |
|---:|---|
| 1 | **Plazo**: antes del 30 de junio de T+1. El SIES publica entre el 10 y el 15 de julio; la holgura cubre una publicación adelantada o un congelamiento fallido |
| 2 | **Qué**: modelo, metadata, predicciones y un resumen legible con total, total por institución e intervalos al 90 % |
| 3 | **Cómo**: huella SHA-256 de cada artefacto registrada en el repositorio, etiqueta anotada con la huella de las predicciones y publicación en un remoto con fecha fuera del control del autor. Un registro sólo local no prueba nada |
| 4 | **Inmutabilidad**: si después aparece un defecto, se crea una versión nueva y se reportan ambas: la congelada como prueba, la corregida como información adicional |
| 5 | **Fuente atrasada**: se congela igual con el último año disponible. Una exógena atrasada degrada poco; un pronóstico sin congelar invalida la prueba |
| 6 | **Al publicarse T+1**: se verifica la huella, se reconstruye el real, se verifica contra el informe oficial y se contrasta con la persistencia al lado (§15.6) |

Es la lección de 2026: el pronóstico de v3 estaba congelado y su contraste reveló los defectos de la llave; la v4 corrigió después de conocer el resultado. **La prueba pre-registrada de la v4 es el pronóstico 2027.**

### 24.6 · Reglas de versión y re-ejecución

Los parámetros metodológicos —llave del lag, lista de variables, semilla, ensayos de optimización, modelo final y años normales del detector— **no cambian en una re-estimación**; cambiarlos es una versión nueva que se evalúa por separado.

| Paso | Acción | Cuándo |
|---:|---|---|
| 1 | Descargar las ediciones nuevas de las fuentes | Al publicarse |
| 2 | Verificar los totales del SIES contra el informe oficial | Siempre |
| 3 | Ejecutar las etapas A → B → C → D en orden | Escenarios D y E |
| 4 | Revisar los controles de §18 y la composición del lag | Siempre |
| 5 | Congelar el pronóstico (§24.5) | Antes del 30 de junio |
| 6 | Ejecutar la etapa E | Al publicarse el SIES del año pronosticado |

**Reproducibilidad.** Semilla 42 en todas las fuentes de aleatoriedad declaradas; no se ha verificado igualdad bit a bit entre equipos. Versiones registradas: pandas 2.3.3, LightGBM 4.6.0, XGBoost 3.2.0, CatBoost 1.2.10, Optuna 4.9.0, SHAP 0.54.1. Con los datos de la v4 original, la regeneración de ingesta y consolidación reprodujo byte a byte todas las tablas intermedias y el dataset.

---

## 25 · Documentos relacionados

| Documento | Qué aporta | Vigencia |
|---|---|---|
| [Paper v4](OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md) | Método, resultados y discusión; pronóstico 2027 en §5.9 | Vigente |
| [README](../README.md) | Resumen del proyecto y resultados principales | Vigente |
| [Figuras](OUTPUTS_PAPER/figuras/) | 12 figuras de la corrida vigente | Vigente |
| [Tablas](OUTPUTS_PAPER/tablas/) | 9 tablas de la corrida vigente | Vigente |
| [Glosario oficial del SIES](OFICIAL_GLOSARIO_MATRICULA_WEB_E.pdf) | Definiciones de la fuente de matrícula | Referencia |

---

## 26 · Consideraciones de uso

- Este documento describe un modelo de investigación de acceso público. **No entrega reglas de negocio** para los análisis en que se use.
- Quien use estos resultados es **responsable de evaluar si los supuestos y parámetros** de §17 y §21 son adecuados para su objetivo.
- El pronóstico es una herramienta de planificación agregada: no evalúa instituciones, no ordena programas ni se usa para decisiones sobre personas.
- Las dudas que este documento no resuelva se pueden plantear como *issue* en el repositorio.

---

## 27 · Historial de versiones

| Versión | Fecha | Corrida documentada | Cambios |
|---|---|---|---|
| 1.0 | 2026-11-18 | Re-estimación con datos hasta 2026 (18-11-2026) | Versión inicial; reemplaza la publicación de los notebooks |
| 2.0 | 2026-11-19 | La misma | Formato técnico-funcional por audiencias: ficha, reglas de negocio, demostración con una celda real, parámetros, controles con resultado, supuestos y riesgos, pendientes y observaciones |

---

*Documento generado el 2026-11-19 a partir de la corrida del 18-11-2026. La demostración de §15.3 se recalculó sobre la tabla de predicciones de esa corrida; las cifras de la v4 original provienen de su validación de agosto de 2026.*

---

> **Diego Evans Pérez Paz**
> Pipeline predictivo de matrícula universitaria · Chile
