# Observaciones y mejoras · revisión del repositorio (noviembre de 2026)

**Repositorio:** Predictive-Model-of-University-Admission---Latam-CL · **Pipeline:** v4, corrida 2027 (`modelo_final_20261118_1345`)
**Alcance de la revisión:** `README.md`, `Documents/OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md`, `Documents/DOCUMENTO_TECNICO_FUNCIONAL.md`, las 9 tablas de `Documents/OUTPUTS_PAPER/tablas/`, las 12 figuras y el PDF de `Documents/`. **No** se revisó el historial git (git no está instalado en el equipo donde se hizo la revisión) ni el código o los datos, que no se publican.
**Revisión hecha por:** Claude Science (asistente de IA). Las tareas de la sección B están redactadas como instrucciones para **Claude Code** en el equipo del autor, que tiene el código, los datos y git.

---

## Resumen ejecutivo

El repositorio está bien documentado. Las cifras de resultados del README son internamente consistentes: con código se recalcularon, a partir de los propios valores publicados en el README, +2,80 % = 761.058 / 740.318, −98 matrículas = −0,01 % (721.649 − 721.747), la cobertura de 95,09 % (721.747 / 759.045) y los porcentajes y crecimientos de la tabla de participación universitaria 2018-2026. Los problemas encontrados son de **estado declarado** y de **trazabilidad**, no de cifras:

1. **El PDF enlazado como «Paper completo» era el de v3**, con el forecast invalidado de 707.960 y ninguna mención a 2027. → Se generó el PDF de v4 (H-01).
2. **El congelamiento SHA-256 del pronóstico 2027 se describía como hecho, pero no existe**: no hay huella, etiqueta ni archivo de predicciones en el repositorio. El documento técnico (§22, P-01) lo lista como pendiente. → El README ahora lo declara pendiente; el procedimiento completo está en la tarea B-01 (H-02).
3. **El TL;DR afirmaba que «toda predicción lleva intervalo al 90 %»**, pero los intervalos de la corrida 2027 no están recalibrados (P-05). → Corregido en el README (H-03).
4. Dos **inconsistencias internas en las tablas** requieren el código: el signo del error 2021 (H-06) y el conteo de 73.349 frente a 73.462 celdas del OOF (H-07).
5. Para enviar el paper a **International Journal of Forecasting**, la brecha más importante es la **literatura**: tiene 17 referencias, todas metodológicas, y ninguna sobre pronóstico de matrícula ni sobre Chile (H-12).

**Plazo crítico:** el congelamiento (B-01) debe quedar publicado en el remoto **antes del 30-06-2027**, y requiere antes P-03 (metadata) y P-05 (intervalos), porque §24.5 exige congelar la metadata y los intervalos al 90 %.

## Tabla de prioridades

| ID | Hallazgo | Severidad | Sección | Estado |
|---|---|---|---|---|
| H-01 | PDF enlazado es v3 (707.960) | Alta | A + B-09 | PDF v4 generado; falta `git rm` del v3 |
| H-02 | Congelamiento SHA-256 declarado como hecho; no existe | Alta | A + B-01 | README corregido; congelamiento pendiente |
| H-03 | TL;DR: «toda predicción lleva intervalo al 90 %» | Alta | A + B-02 | README corregido; recalibración pendiente |
| H-25 | Cambios documentales sin commit ni push | Alta | B-00 | Commit hecho (19-11-2026); push pendiente de aprobación del autor |
| H-12 | Literatura insuficiente para IJF | Alta | C-01 | Pendiente (pista del manuscrito) |
| H-16 | Huella del dataset cubre sólo 8.192 bytes (O-04) | Media | B-01 | Pendiente |
| H-04 | *Skill score* no definido en el README | Media | A | Aplicado |
| H-06 | Signo del error 2021 distinto entre tablas | Media | B-03 | Resuelto: el generador tomaba `abs()`; ahora es pred − real. 2021 = −1,8621 y Arica y Parinacota = −0,3561; prueba de signo OK en los 8 años |
| H-07 | N8 OOF = 73.349 grupos vs 73.462 filas | Media | B-04 | Pendiente |
| H-09 | P-02 (Ñuble) y P-03 (metadata) ausentes de las Limitaciones | Media | A + B-05/B-06 | README corregido; correcciones pendientes |
| H-11 | Peores celdas compatibles con defectos residuales de la llave del lag | Media | B-07 | Pendiente |
| H-13 | Historial git no auditado | Media | B-10 | Pendiente |
| H-14 | Versión de SHAP inconsistente (0.45.1 vs 0.54.1) | Media | B-11 | Pendiente |
| H-17 | Ablación de variables con matrícula contemporánea (P-04) | Media | B-08 | Pendiente |
| H-20 | Conformal de Mondrian atribuido a Romano et al. (2019) | Media | C-02 | Pendiente |
| H-21 | El Resumen afirma algo sobre la literatura latinoamericana sin citarla | Media | C-01 | Pendiente |
| H-26 | El paper sigue llamando «pre-registrado» al pronóstico 2027 | Media | C-03 | Pendiente |
| H-05 | Conteo de fuentes inconsistente (10 / 7 + 4 / 7) | Baja | A + C-04 | README corregido; doc técnico pendiente |
| H-08 | `fig09_validacion_forecast_2026.png` muestra el forecast 2027 | Baja | A + B-09 | Copia renombrada; falta `git rm` |
| H-10 | `.obsidian/` versionado, sin `.gitignore` | Baja | A + B-00/B-09 | `.gitignore` en la raíz; ignora `.obsidian/` completo (nunca estuvo versionado, no requiere `git rm --cached`) |
| H-15 | Columna `confianza_%` (= 100 − WAPE) en las tablas | Baja | B-12 | Pendiente |
| H-18 | Tablas top-15 sin la columna género | Baja | B-07 | Pendiente |
| H-19 | Numeración de figuras: paper ≠ archivos; formato numérico de las figuras | Baja | C-05 | Pendiente |
| H-22 | Agradecimientos mencionan a la CNA, que no figura entre las fuentes | Baja | C-06 | Pendiente |
| H-23 | Clave BibTeX `evans2026…` con apellido Pérez Paz | Baja | C-06 | Pendiente |
| H-24 | Doc técnico §16.3 desactualizado; periodo SIES 2018-2026 vs 2007-2026 | Baja | C-04 | Pendiente |
| H-27 | Pendientes P-06 a P-09 y O-02 | Baja | B-13 | Backlog |

---

## A · Aplicado por Claude Science en esta revisión

Estos cambios se guardaron en la carpeta local del repositorio, **excepto el `.gitignore`**: la carpeta no admite, desde esta herramienta, archivos cuyo nombre empieza con punto, así que se entregó como artefacto descargable (véase el registro al final). **Ninguno está en git todavía**: el commit y el push son la tarea B-00. No se cambió ninguna cifra de resultados.

### H-01 · El PDF del paper era de v3 — Alta
- **Evidencia:** `Documents/Predictive model of university admission.pdf` tiene en su metadata el título `paper_modelo_matricula_chile_v3_FINAL` y la fecha de creación 2026-06-18. Contiene 5 veces «707.960», el forecast v3 invalidado, y 0 menciones de «2027» o «761.058». El README lo enlazaba como «Paper completo (PDF)».
- **Impacto:** quien abra el PDF lee las cifras que el propio README declara inválidas (R² 0,936, *skill* +77,4 %).
- **Aplicado:** nuevo `Documents/paper_modelo_matricula_chile_v4.pdf`, generado desde el `.md` v4 con pandoc 3.14 y typst 0.15.1. Tiene 23 páginas y 6 figuras embebidas; con pypdf se verificó que contiene «761.058» (4 veces) y no contiene «707.960». Las citas `[@clave]` se convirtieron a (Autor, año). El README enlaza el PDF nuevo y marca el v3 como obsoleto. El PDF v3 **no** se borró.
- **Tarea para Claude Code:** B-09 (eliminar el v3 con `git rm`).

### H-02 · El congelamiento SHA-256 se describía como hecho — Alta
- **Evidencia:** el diagrama del README decía «Pronóstico 2027 fijado con huella SHA-256 antes del 30-06-2027». No hay ningún hash de 64 caracteres hexadecimales en el README, el paper ni el documento técnico, ni hay archivo de predicciones en el repositorio. El documento técnico §22 lista P-01 como pendiente, y §24.5, regla 3, dice: «Un registro sólo local no prueba nada».
- **Impacto:** se declaraba un pre-registro que no es verificable; un revisor de IJF lo detectaría.
- **Aplicado:** la caja del diagrama ahora dice «CONGELAMIENTO (PENDIENTE) … aún no realizado · plazo: antes del 30-06-2027». Se agregó un aviso `[!WARNING]` en la sección del pronóstico 2027, se actualizó la nota de noviembre («publicado»; congelamiento formal pendiente) y se añadió una línea en Limitaciones.
- **Tarea para Claude Code:** B-01.

### H-03 · El TL;DR prometía intervalos para toda predicción — Alta
- **Evidencia:** el TL;DR decía «Toda predicción lleva **intervalo al 90 %**… cobertura verificada de 92,5 %». Esa cobertura (92,53 %) es la de v4 contra el real 2026. P-05 («Recalibrar los intervalos conformes para la corrida 2027») está pendiente, y el paper §4.10 dice que «la sección 5.9 reporta sólo el puntual».
- **Aplicado:** el TL;DR ahora atribuye la cobertura a v4 sobre 2026 y declara pendientes los intervalos 2027. También se matizó la viñeta «Universidades … con su banda al 90 %».
- **Tarea para Claude Code:** B-02.

### H-04 · El *skill score* no estaba definido en el README — Media
- **Evidencia:** la tabla de desempeño muestra, en el OOF, WAPE 14,13 % frente a 14,63 % y *skill* −0,47 %, sin explicar la aparente contradicción. La definición está sólo en el paper §4.9: 1 − (RMSE_modelo / RMSE_naïve)² (Murphy, 1988).
- **Aplicado:** se agregó el párrafo «Cómo leer el *skill*» bajo la tabla. Define el *skill* y el MASE y explica por qué el WAPE puede mejorar con un *skill* negativo: el RMSE eleva los errores al cuadrado, y unos pocos errores grandes de 2019-2020 dominan.

### H-05 · Conteo de fuentes inconsistente — Baja
- **Evidencia:** el TL;DR del README decía «10 fuentes oficiales»; el diagrama, «7 fuentes públicas + 4 diccionarios» (= 11). La tabla de fuentes del README y la Tabla 1 del paper tienen 10 filas (7 + 3 diccionarios). El documento técnico dice «siete fuentes públicas» y, en su diagrama, «4 diccionarios de llaves»: el cuarto es la tabla de 16 regiones de §5.3, que no figura en la tabla de fuentes.
- **Aplicado:** el README dice ahora «10 fuentes oficiales (7 bases públicas y 3 diccionarios de llaves)» en el TL;DR, y «FUENTES PÚBLICAS (7) + DICCIONARIOS (3) = 10» en el diagrama, con los diccionarios de instituciones, carreras y sede-región.
- **Pendiente:** C-04 (armonizar el documento técnico).

### H-08 · El nombre de fig09 no corresponde a su contenido — Baja
- **Evidencia:** `fig09_validacion_forecast_2026.png` se titula «Comparación del forecast 2027 contra baselines simples», y el paper la usa como Figura 6 para el forecast 2027.
- **Aplicado:** copia byte a byte `Documents/OUTPUTS_PAPER/figuras/fig09_forecast_2027_vs_baselines.png` (SHA-256 `3b65123197fba565424980a388368c77d9d9f709c7dcd6da0438e30306929f03`, idéntico al original). Las referencias en el README y en el paper `.md` apuntan al nombre nuevo. El archivo viejo **no** se borró.
- **Tarea para Claude Code:** B-09.

### H-09 · P-02 y P-03 no aparecían en las Limitaciones — Media
- **Evidencia:** documento técnico §5.3: «sus 3.474 filas del SIES (2,73 % del universo) entran a las uniones sin código de región»; docentes e inmuebles caen a la mediana global. §23, O-01: la metadata registra cinco *folds* cuando se ejecutaron siete.
- **Aplicado:** se agregaron tres viñetas en Limitaciones del README: Ñuble (P-02), metadata de *folds* (P-03) y pronóstico 2027 sin banda ni congelamiento (P-05, P-01).
- **Tareas para Claude Code:** B-05 y B-06.

### H-10 · Carpeta `.obsidian/` versionada sin `.gitignore` — Baja
- **Evidencia:** existen `.obsidian/app.json`, `appearance.json`, `core-plugins.json` y `workspace.json`, y el repositorio no tenía `.gitignore`.
- **Aplicado (entregado como artefacto, no guardado en la carpeta):** `.gitignore` nuevo, que ignora `.obsidian/workspace.json`, la caché de Obsidian, artefactos de Python y del sistema operativo, y artefactos de modelo (`*.cbm`, `*.pkl`, `*.parquet`, `catboost_info/`). Un comentario advierte que, si se publican, las predicciones congeladas deben quedar fuera de esas reglas.
- **Tarea para Claude Code:** B-09 (`git rm --cached`).

### Otros cambios en el README
- Enlaces al paper v4 (Markdown y PDF) y a este documento en la nota de noviembre.
- En la estructura del repositorio: `OBSERVACIONES_Y_MEJORAS.md`, `.gitignore`, el PDF v4 y la figura renombrada; el PDF v3 y la fig09 vieja quedan marcados como «pendiente de eliminación».
- En «Estado y versiones», una aclaración de que el PDF de `Documents/` era de v3.

---

## B · Requiere código, datos o git del autor → tareas para Claude Code

> Orden recomendado: **B-00 → B-10 → B-06 → B-02 → B-01** (antes del 30-06-2027). B-03, B-04, B-07, B-09, B-11 y B-12 no afectan al pronóstico y pueden ir en paralelo. **B-05 (Ñuble) y B-08 (ablación) son una versión metodológica nueva**: no deben tocar el pronóstico 2027 congelado (§24.5, regla 4; §24.6).

### B-00 · Hacer commit y push de los cambios documentales de esta revisión — Alta (H-25)
- **Paso previo:** copiar el `.gitignore` entregado como artefacto a la raíz del repositorio (la carpeta rechazó el guardado de archivos con nombre que empieza por punto). El README ya lo lista en la estructura.
- **Contexto:** Claude Science escribió en la carpeta local sin git. Los cambios son: `README.md` (modificado), `.gitignore` (a colocar a mano), `OBSERVACIONES_Y_MEJORAS.md`, `Documents/paper_modelo_matricula_chile_v4.pdf`, `Documents/OUTPUTS_PAPER/figuras/fig09_forecast_2027_vs_baselines.png` (nuevos) y `Documents/OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md` (modificado).
- **Tarea:**
  1. `git status` y `git diff README.md Documents/OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md`. Revisar que el diff del paper sea **una sola línea** (la ruta de fig09) y que el del README no cambie ninguna cifra de resultados.
  2. `git add README.md .gitignore OBSERVACIONES_Y_MEJORAS.md Documents/paper_modelo_matricula_chile_v4.pdf Documents/OUTPUTS_PAPER/figuras/fig09_forecast_2027_vs_baselines.png Documents/OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md`
  3. `git commit -m "docs: PDF v4, estado real del congelamiento e intervalos 2027, definición del skill, fig09 renombrada, .gitignore"` y `git push`.
- **Criterio de aceptación:** `git status` limpio para esos archivos; el commit es visible en GitHub; los enlaces del README al PDF v4, a fig09 nueva y a este documento resuelven en la interfaz web.

### B-01 · Congelar el pronóstico 2027 (P-01) según §24.5 — Alta (H-02, H-16)
- **Criterio vinculante (doc. técnico §24.5):** (1) plazo, antes del 30-06-2027; (2) qué se congela: modelo, metadata, predicciones y un resumen legible con el total, el total por institución y los intervalos al 90 %; (3) cómo: huella SHA-256 de **cada** artefacto registrada en el repositorio, etiqueta **anotada** con la huella de las predicciones y publicación en un remoto con fecha fuera del control del autor; (4) inmutabilidad: si aparece un defecto, se crea una versión nueva y se reportan ambas.
- **Prerrequisitos:** B-06 (la metadata congelada debe decir siete *folds*) y B-02 (el resumen debe traer los intervalos al 90 %). Si B-02 no alcanza a estar listo con holgura, congelar igual antes del plazo y declarar en el resumen que los intervalos faltan (regla 5: «un pronóstico sin congelar invalida la prueba»).
- **Pasos:**
  1. Ubicar los tres artefactos de `modelo_final_20261118_1345` (§16.1): el modelo serializado, la metadata y la tabla de predicciones de 92.036 filas. Verificar que la suma de `matriculas_pred` con `tipo_registro == "forecast"` sea **761.058** (redondeada) en **9.069** filas, sobre 53 instituciones.
  2. Crear `forecast_2027/` en el repositorio con:
     - `resumen_forecast_2027.md`: total, total por institución (53 filas), por modalidad y condición, intervalos al 90 % (de B-02), supuestos (exógenas arrastradas y congeladas), identificador del modelo y fecha;
     - `predicciones_forecast_2027.csv`: **recomendado** publicarlo (sólo las 9.069 filas de forecast; columnas de la celda, `matriculas_lag`, `matriculas_pred` e intervalos), porque sin el archivo un tercero no puede verificar la huella. Si el autor decide no publicarlo, el hash igual debe quedar registrado y el archivo, archivado de forma inmutable fuera del equipo;
     - `SHA256SUMS.txt`, con una línea por artefacto (`<hash>  <nombre>`), incluidos el modelo y la metadata aunque no se publiquen.
  3. Calcular las huellas sobre el **archivo completo**, no sobre los primeros 8.192 bytes como hace hoy la metadata (O-04, H-16). En Windows: `Get-FileHash -Algorithm SHA256 <archivo>`; o `sha256sum`. Corregir también el código que calcula la huella del dataset, para que use el archivo completo en las corridas futuras.
  4. `git add forecast_2027/ && git commit -m "Congelamiento del pronóstico 2027 (modelo_final_20261118_1345)"`.
  5. Crear la etiqueta anotada: `git tag -a forecast-2027-v4 -m "Pronóstico 2027 congelado. Modelo modelo_final_20261118_1345. Total 761.058. SHA-256 predicciones: <hash>"`.
  6. `git push origin main` y `git push origin forecast-2027-v4`.
  7. Sello externo, porque las fechas de commit las controla el autor: crear un **GitHub Release** sobre la etiqueta, adjuntando el CSV y `SHA256SUMS.txt`, y, preferentemente, archivarlo en **Zenodo** (integración GitHub → DOI) o en Software Heritage. Registrar el DOI o el enlace.
  8. Actualizar el README: reemplazar el aviso «Congelamiento pendiente» y la caja del diagrama por la huella de las predicciones, el nombre de la etiqueta, la fecha y el enlace al Release o DOI. Actualizar el documento técnico §22 (P-01 → resuelto).
- **Criterio de aceptación:** `git cat-file -t forecast-2027-v4` devuelve `tag` (anotada, no ligera); el mensaje de la etiqueta contiene un hash idéntico a `Get-FileHash` del CSV de predicciones; `git ls-remote --tags origin` lista la etiqueta; el Release o DOI tiene fecha anterior al 30-06-2027; el README contiene la huella de 64 caracteres hexadecimales y ya no dice «pendiente».

### B-02 · Recalibrar los intervalos conformes de la corrida 2027 (P-05) — Alta (H-03)
- **Tarea:** aplicar el mismo procedimiento del paper §4.10 (conformal dividido, estratificado por tamaño, calibrado en arcsinh de la tasa, mínimo 30 observaciones por estrato, agregados calibrados por nivel) con los residuos de la **corrida 2027**. Documentar qué años entran a la calibración. Emitir los intervalos al 90 % por celda (9.069) y por nivel de agregación (N2-N8), y para el total nacional el rango indicativo, sin banda conforme, como en v4.
- **Archivos:** tabla de predicciones (nuevas columnas `pi90_lo` y `pi90_hi`); `forecast_2027/resumen_forecast_2027.md`; paper §5.9 y §4.10; README (sección del pronóstico y TL;DR).
- **Criterio de aceptación:** la cobertura empírica de esa calibración, medida sobre el holdout 2026, se reporta junto al ancho mediano; el TL;DR y §5.9 informan la banda del total 2027; el texto «pendientes de recalibración» desaparece del README.

### B-03 · Resolver el signo del error agregado 2021 — Media (H-06)
- **Evidencia:** `tabla_backtesting_anual.md`, fila 2021: real 667.325, pred 654.899, error_abs −12.426, error_rel −1,862 %. En `tabla_metricas_por_anio.md`, fila 2021, `error_agregado_rel_%` = **+1,8621**. Las demás filas coinciden en signo. La fig08 rotula 2021 como −1,86 %.
- **Tarea:** revisar el código que genera `tabla_metricas_por_anio.md` (¿un `abs()`?). Si la columna es un valor absoluto, renombrarla `error_agregado_abs_rel_%` y decirlo; si es un bug, corregirlo y regenerar la tabla. Revisar si el paper o el documento técnico citan el valor +1,86.
- **Criterio de aceptación:** ambas tablas tienen el mismo signo para 2021 (−1,86 %), o la columna está renombrada y documentada; prueba unitaria: `sign(error_agregado_rel) == sign(sum(pred) - sum(real))` para todos los años.

### B-04 · Conciliar 73.349 grupos con 73.462 filas OOF — Media (H-07)
- **Evidencia:** `tabla_macro_a_micro_OOF.md`, N8, tiene `n_grupos` = 73.349 (también en fig05, panel N8). `tabla_resumen_paper.md` y el README dan n = 73.462 para el OOF, y la suma por año y por región es 73.462. Es decir, 113 filas comparten la llave de la celda fina. En el holdout 2026, N8 = 9.069, igual al número de filas. El RMSE de N8 (20,49) difiere del de la tabla resumen (20,44): el *groupby* fusiona celdas.
- **Tarea:** listar las 113 filas duplicadas (`df.duplicated(subset=[anio, institucion, carrera, region, jornada, genero, condicion], keep=False)`) y determinar su origen: ¿dos códigos de carrera con el mismo nombre canónico? ¿La normalización de nombres colapsa programas distintos? ¿El respaldo por código del lag? Decidir si la llave fina debe incluir el código de carrera. Documentar el resultado en el doc técnico §8.1 (grano).
- **Criterio de aceptación:** la cascada N8 y la tabla resumen reportan el mismo n, o el paper y el README explican la diferencia en una nota; queda informe del origen de las 113 filas. Si el grano cambia, es versión nueva (§24.6) y no toca el forecast congelado.

### B-05 · Corregir Ñuble antes de las uniones institucionales (P-02) — Media (H-09)
- **Evidencia:** documento técnico §5.3. Las 3.474 filas de Ñuble (2,73 %) entran sin código de región; docentes e inmuebles caen a la mediana global y los aranceles se imputan por la cascada. El PIB se corrige después.
- **Tarea:** mover la reparación del nombre y código de Ñuble (código INE 16) **antes** de las uniones con docentes, inmuebles y aranceles. Comparar, antes y después, el porcentaje de filas de Ñuble con coincidencia en cada fuente y el WAPE OOF de Ñuble (hoy 15,4 % en fig04).
- **Restricción:** es una **versión metodológica nueva** (v5 o pista de mejoras): no regenerar el forecast 2027 congelado; reportarla por separado.
- **Criterio de aceptación:** cero filas de Ñuble sin código de región al entrar a las uniones; tasa de coincidencia de Ñuble en docentes, inmuebles y aranceles comparable a la de otras regiones; control nuevo en §18.

### B-06 · Corregir la metadata de *folds* (P-03) — Media (H-09)
- **Tarea:** ubicar en el código dónde se escribe el número de *folds* en la metadata (probablemente una constante `n_splits=5` distinta de la partición real de 7). Hacer que se derive de la partición efectivamente ejecutada (validación 2019-2025) y reescribir la metadata de `modelo_final_20261118_1345` **antes** del congelamiento (B-01). Si regenerar el archivo altera su huella, debe hacerse antes de calcularla.
- **Criterio de aceptación:** la metadata dice 7 *folds* con los años de validación listados; prueba que compare `len(folds)` con el campo de la metadata; P-03 y O-01 cerrados en el doc técnico.

### B-07 · Auditar las peores celdas por nivel de respaldo de la llave del lag — Media (H-11, H-18)
- **Evidencia:** en `tabla_top15_peores_predicciones.md`: U. Los Leones, Pedagogía en Educación Diferencial, 2019 NUEVO (real 128, pred 836,9; +554 %) y 2020 ANTIGUO (real 215, pred 1.278,9); UDLA, Ingeniería de Ejecución Industrial A Distancia, 2026 (real 154, pred 767,6); U. de Chile, «Ingeniería y Ciencias - Plan Común», con predicciones casi idénticas en 2020 y 2026 (1.687,76 y 1.687,50). El patrón es compatible con lags heredados de reestructuraciones o renombres. La tabla de predicciones (§16.2) **no incluye `origen_lag`**, aunque el dataset sí lo tiene (§6.4), y las tablas top-15 **no tienen columna de género**, de modo que la celda no queda identificada.
- **Tarea:** (1) agregar `origen_lag` (fino, código o medio) a la tabla de predicciones exportada; (2) agregar `genero` a ambas tablas top-15, o declarar que agregan género; (3) para las 50 peores celdas OOF y holdout, tabular `origen_lag`, el lag, la participación de escalado y si la carrera cambió de nombre o código entre t−1 y t; (4) reportar el WAPE y el *skill* por `origen_lag`; (5) publicar la tasa de emparejamiento por nivel, recomendación 1 del README.
- **Criterio de aceptación:** tabla nueva `tabla_peores_por_origen_lag.md`; el paper §5.x o el doc técnico §6.4 discute si los errores extremos se concentran en los respaldos; las tablas top-15 identifican la celda completa.

### B-08 · Ablación de las tres variables con matrícula contemporánea (P-04) — Media (H-17)
- **Tarea:** reentrenar sin `densidad_estudiantes_m2`, `ratio_docente_estudiante` y `matriculas_sobre_pib` (o con sus versiones de t−1), con los mismos hiperparámetros y la misma semilla, y comparar el OOF y el holdout 2026 (WAPE, *skill*, MASE por nivel).
- **Restricción:** es una pista separada; no reemplaza el forecast congelado.
- **Criterio de aceptación:** tabla comparativa en el paper §6.5 y el doc técnico §13.2; la limitación del README cita el efecto medido.

### B-09 · Limpieza de archivos con git — Baja (H-01, H-08, H-10)
- **Requiere aprobación explícita del autor** antes de ejecutar.
- **Tarea:**
  1. `git rm "Documents/Predictive model of university admission.pdf"` (PDF v3, que queda en el historial).
  2. `git rm Documents/OUTPUTS_PAPER/figuras/fig09_validacion_forecast_2026.png`. Antes, buscar referencias restantes con `git grep -n "fig09_validacion_forecast_2026"`; también en el dashboard de Hugging Face, si lo usa.
  3. `git rm --cached .obsidian/workspace.json`. Decidir si el resto de `.obsidian/` debe versionarse; si no, agregar `.obsidian/` completo al `.gitignore` y `git rm -r --cached .obsidian`.
  4. Quitar del README las dos líneas marcadas «pendiente de eliminación» y el comentario sobre el PDF v3 en «Estado y versiones», dejando la mención al historial.
- **Criterio de aceptación:** `git grep` no devuelve referencias a los archivos eliminados; `git status` no muestra `.obsidian/workspace.json`; README sin líneas «pendiente de eliminación».

### B-10 · Auditar el historial git — Media (H-13)
- **Tarea:** (1) `git log --follow -p README.md | Select-String "761.058"` para encontrar el **primer commit pusheado** que publica 761.058 y su fecha en el remoto: esa fecha es hoy la única evidencia temporal del pronóstico; (2) verificar que `paper_modelo_matricula_chile_v3_FINAL.md` existe en el historial, como afirma el README; (3) verificar si existe etiqueta o evidencia remota del congelamiento v3 del 17-06-2026 que el README cita; (4) `git tag -l -n` para ver las etiquetas existentes.
- **Criterio de aceptación:** informe breve, agregable a este documento, con el hash y la fecha del primer commit con 761.058, la existencia del paper v3 en el historial y las etiquetas existentes.

### B-11 · Versión de SHAP inconsistente — Media (H-14)
- **Evidencia:** el README y el paper §4.8 dicen que `shap` 0.45.1 es incompatible con `xgboost` 3.x y que esa es una de las razones para usar CatBoost. El documento técnico §24.6 registra «SHAP 0.54.1» junto a XGBoost 3.2.0.
- **Tarea:** leer en la metadata de la corrida 2027 y de v4 la versión de `shap` efectivamente usada. Verificar si `TreeExplainer` sobre XGBoost 3.2.0 sigue fallando con esa versión. Corregir el README, el paper §4.8 y el doc técnico para que coincidan; si la incompatibilidad ya no existe, reformular la justificación de CatBoost como «continuidad de método entre corridas».
- **Criterio de aceptación:** una sola versión de SHAP citada en los tres documentos, consistente con la metadata.

### B-12 · Columna `confianza_%` en las tablas — Baja (H-15)
- **Evidencia:** en `tabla_macro_a_micro_*.md` y `tabla_resumen_paper.md`, `confianza_%` = 100 − WAPE (p. ej., 85,8711 = 100 − 14,1289). La tabla de predicciones trae `confianza_bloque`, «indicador de presentación heredado; no es una probabilidad» (§16.2). Es el mismo encuadre de la v3 («99,98 % de confianza») que el README desautoriza.
- **Tarea:** eliminar la columna de los generadores de tablas o renombrarla `100_menos_WAPE_%`, y regenerar las 9 tablas. Evaluar quitar `confianza_bloque` del export.
- **Criterio de aceptación:** ninguna tabla publicada contiene el término «confianza» para una métrica que no es probabilística.

### B-13 · Backlog de pendientes del doc técnico — Baja (H-27)
- P-06 (jornada × año), P-07 (emparejar por código: 31 celdas y 3.987 matrículas), P-08 (rango de iteraciones de CatBoost), P-09 (repetir con el INE completo) y O-02 (la desocupación 2025 promedia 10 de 12 trimestres y el control la acepta: exigir el año completo o declararlo en el control). Todos van en la pista de mejoras, no en el forecast congelado.

---

## C · Recomendaciones editoriales (paper, documento técnico y README)

### C-01 · Literatura y estado del arte para IJF — Alta (H-12, H-21)
- **Evidencia:** el paper v4 tiene 12.428 palabras y 17 referencias, todas metodológicas (*gradient boosting*, validación temporal, conformal, métricas); ninguna sobre pronóstico de matrícula ni sobre literatura chilena. §2.2 menciona trabajos chilenos (FONDEF, retención) sin citarlos, y §2 declara que el levantamiento se hizo con «buscador general y no en bases académicas indexadas». El Resumen afirma que «la mayoría de los estudios disponibles en América Latina» valida con particiones aleatorias, sin cita. §2.3 discute proveedores comerciales en lugar de literatura arbitrada.
- **Recomendación:** hacer una búsqueda en Scopus/WoS/SciELO sobre *enrollment forecasting* y *higher education demand* (incluida la literatura de pronóstico jerárquico y reconciliación, central en IJF); citar con DOI los trabajos chilenos de §2.2; respaldar o eliminar la afirmación del Resumen; reducir §2.3. Esto lo cubre la pista de manuscrito IJF, con validación de referencias y `references.bib`.

### C-02 · Atribución del conformal de Mondrian — Media (H-20)
- **Evidencia:** §2.4 atribuye la estratificación de Mondrian a «[@romano2019; @angelopoulos2023]», y §4.10 a «[@romano2019]». Romano, Patterson y Candès (2019) es *Conformalized Quantile Regression*, otro método. La lista de referencias ya incluye Vovk et al. (2005), la fuente original de los predictores conformes de Mondrian.
- **Recomendación:** citar Vovk et al. (2005) para Mondrian; dejar Romano et al. (2019) sólo si se discute CQR como alternativa para la heterocedasticidad.

### C-03 · «Pre-registrado» en el paper — Media (H-26)
- **Evidencia:** el título de §5.9 y su párrafo «Estatus», el Resumen («queda pre-registrado») y la nota de noviembre usan el término, pero el congelamiento formal (§24.5) está pendiente.
- **Recomendación:** hasta completar B-01, decir «publicado antes del dato oficial; congelamiento formal pendiente». Después de B-01, citar la etiqueta y el DOI. En IJF conviene describirlo como un **pronóstico ex ante publicado con sello temporal externo**, y no como un pre-registro en sentido estricto, salvo que se registre en una plataforma de pre-registro.

### C-04 · Armonizar el documento técnico — Baja (H-05, H-24)
- El diagrama del doc técnico dice «4 diccionarios de llaves», mientras que la tabla de fuentes del README y la Tabla 1 del paper tienen 3. Recomendación: o se añade la tabla de 16 regiones como cuarto diccionario en la Tabla 1 y en el README (y entonces son 11), o se dice explícitamente que es una tabla interna y no una fuente.
- §16.3, «Lo que se publica», no lista el PDF v4, este documento ni `forecast_2027/` (tras B-01).
- La tabla de fuentes del README da para el SIES el periodo «2018-2026», y la Tabla 1 del paper y el diagrama, «2007-2026». Conviene aclarar «2007-2026 (modelado 2018-2026)».

### C-05 · Figuras — Baja (H-19)
- El paper usa 6 de las 12 figuras, con numeración propia (Figura 1 = fig02, Figura 3 = fig08, Figura 6 = fig09). Para IJF: numerar los archivos según el orden del manuscrito (`Fig1_….png`) y mover el resto a material suplementario.
- Las figuras usan formato numérico anglosajón (761,058; 2.80 %; n=73,462) y ejes en inglés en el Q-Q plot de fig01 («Ordered Values», «Theoretical quantiles»). Para el manuscrito en inglés está bien; para la versión en español, regenerarlas con coma decimal.
- En fig09, la barra «Prom. años normales» (+3,41 %) se describe en el texto como «promedio de las variaciones 2024-2026». Conviene unificar la etiqueta. La etiqueta «−1.30 %» se superpone al eje.
- El *caption* de fig05 informa n = 73.349 en N8 (véase B-04).

### C-06 · Detalles menores — Baja (H-22, H-23)
- Los Agradecimientos mencionan a la CNA, que no figura entre las fuentes (los años de acreditación llegan vía CNED INDICES). Aclararlo o quitarla.
- Clave BibTeX `evans2026matricula`: el primer apellido es Pérez Paz; sugerencia: `perezpaz2026matricula`.
- El README aún describe a SHAP 0.45.1 como la causa de descartar XGBoost (véase B-11).

---

## Registro de lo guardado en la carpeta del repositorio

| Archivo (ruta relativa al repositorio) | Acción | Resultado de `save_to_folder` | SHA-256 |
|---|---|---|---|
| `README.md` | Reemplazado (`replaces` = `958da2bf…716b`) | ✓ guardado, 47.189 bytes | `c6bfacd49199649962b2aadde47af8fa6ef3225a54dcc9b310a214c7befb5400` |
| `Documents/OUTPUTS_PAPER/paper_modelo_matricula_chile_v4.md` | Reemplazado (`replaces` = `122403b3…1dbc`); sólo cambia la ruta de fig09 | ✓ guardado, 79.060 bytes | `eba2be92d89bcb06c34282ba2a50ed639d72d6d8695b3fd58e84b26dba45ee25` |
| `Documents/paper_modelo_matricula_chile_v4.pdf` | Nuevo | ✓ guardado, 1.861.899 bytes | `defd3d8ce0544bd2cfe1624f6c794bc61ce1949712a62774d490fdf2a5eec56f` |
| `Documents/OUTPUTS_PAPER/figuras/fig09_forecast_2027_vs_baselines.png` | Nuevo (copia byte a byte de `fig09_validacion_forecast_2026.png`) | ✓ guardado, 127.836 bytes | `3b65123197fba565424980a388368c77d9d9f709c7dcd6da0438e30306929f03` |
| `OBSERVACIONES_Y_MEJORAS.md` | Nuevo (este documento) | ✓ guardado (véase el informe de la sesión) | — |
| `.gitignore` | Nuevo | ✗ **rechazado** (`name_not_allowed`: no se copian archivos cuyo nombre empieza por punto) → entregado como artefacto; copiar a la raíz a mano (B-00) | — |

No se borró ni se sobrescribió ningún archivo preexistente aparte del README y del paper `.md`. Siguen en la carpeta, para eliminarlos con aprobación del autor (B-09), `Documents/Predictive model of university admission.pdf` (v3) y `fig09_validacion_forecast_2026.png`.

---
*Documento generado el 19-11-2026. Las cifras citadas se verificaron leyendo los archivos del repositorio; las que dependen del código o los datos (B-03, B-04, B-07) son observaciones de consistencia entre archivos publicados, no verificaciones contra los datos.*
