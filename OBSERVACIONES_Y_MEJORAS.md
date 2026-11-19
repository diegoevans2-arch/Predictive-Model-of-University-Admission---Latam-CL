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
| H-01 | PDF enlazado es v3 (707.960) | Alta | A + B-09 | Resuelto: PDF v4 publicado; v3 eliminado del árbol (B-09) |
| H-02 | Congelamiento SHA-256 declarado como hecho; no existe | Alta | A + B-01 | README corregido; congelamiento pendiente |
| H-03 | TL;DR: «toda predicción lleva intervalo al 90 %» | Alta | A + B-02 | Resuelto (§D): banda 2027 calibrada; cobertura 92,35 % en el holdout 2026; TL;DR y §5.9 con el rango del total |
| H-25 | Cambios documentales sin commit ni push | Alta | B-00 | Commit hecho (19-11-2026); push pendiente de aprobación del autor |
| H-12 | Literatura insuficiente para IJF | Alta | C-01 | Pendiente (pista del manuscrito) |
| H-16 | Huella del dataset cubre sólo 8.192 bytes (O-04) | Media | B-01 | Pendiente |
| H-04 | *Skill score* no definido en el README | Media | A | Aplicado |
| H-06 | Signo del error 2021 distinto entre tablas | Media | B-03 | Resuelto: el generador tomaba `abs()`; ahora es pred − real. 2021 = −1,8621 y Arica y Parinacota = −0,3561; prueba de signo OK en los 8 años |
| H-07 | N8 OOF = 73.349 grupos vs 73.462 filas | Media | B-04 | Diagnosticado (§D): 113 filas duplicadas por sedes o versiones del plan; 2026 y 2027 sin duplicados. Corrección = versión nueva; nota al paper pendiente de decisión |
| H-09 | P-02 (Ñuble) y P-03 (metadata) ausentes de las Limitaciones | Media | A + B-05/B-06 | README corregido; P-03 resuelto (B-06); P-02 (Ñuble): causa encontrada y corregida en `v5-mejoras`, sin ejecutar (requiere autorización: versión nueva) |
| H-11 | Peores celdas compatibles con defectos residuales de la llave del lag | Media | B-07 | Resuelto (§D): hipótesis rechazada; 49/50 (OOF) y 50/50 (holdout) de las peores celdas tienen lag fino |
| H-13 | Historial git no auditado | Media | B-10 | Hecho (§D): el 761.058 aún no está en el remoto (sólo en commits locales); sin etiquetas; v3 en `b355c67` |
| H-14 | Versión de SHAP inconsistente (0.45.1 vs 0.54.1) | Media | B-11 | Resuelto: 0.45.1 = v4, 0.54.1 = corrida 2027; justificación reformulada como continuidad de método |
| H-17 | Ablación de variables con matrícula contemporánea (P-04) | Media | B-08 | Bloqueado: requiere autorización para reentrenar (pista v5) |
| H-20 | Conformal de Mondrian atribuido a Romano et al. (2019) | Media | C-02 | Resuelto: Vovk et al. (2005) |
| H-21 | El Resumen afirma algo sobre la literatura latinoamericana sin citarla | Media | C-01 | Pendiente |
| H-26 | El paper sigue llamando «pre-registrado» al pronóstico 2027 | Media | C-03 | Pendiente |
| H-05 | Conteo de fuentes inconsistente (10 / 7 + 4 / 7) | Baja | A + C-04 | Resuelto: 7 + 3 = 10 en README, paper y doc técnico |
| H-08 | `fig09_validacion_forecast_2026.png` muestra el forecast 2027 | Baja | A + B-09 | Resuelto: copia renombrada; nombre antiguo eliminado (B-09) |
| H-10 | `.obsidian/` versionado, sin `.gitignore` | Baja | A + B-00/B-09 | `.gitignore` en la raíz; ignora `.obsidian/` completo (nunca estuvo versionado, no requiere `git rm --cached`) |
| H-15 | Columna `confianza_%` (= 100 − WAPE) en las tablas | Baja | B-12 | Resuelto en las 10 tablas publicadas; `confianza_bloque` queda en el export congelable |
| H-18 | Tablas top-15 sin la columna género | Baja | B-07 | Resuelto: columna `genero` agregada |
| H-19 | Numeración de figuras: paper ≠ archivos; formato numérico de las figuras | Baja | C-05 | Pendiente |
| H-22 | Agradecimientos mencionan a la CNA, que no figura entre las fuentes | Baja | C-06 | Resuelto: aclarado que llega vía CNED INDICES |
| H-23 | Clave BibTeX `evans2026…` con apellido Pérez Paz | Baja | C-06 | Resuelto: `perezpaz2026matricula` |
| H-24 | Doc técnico §16.3 desactualizado; periodo SIES 2018-2026 vs 2007-2026 | Baja | C-04 | Resuelto (falta agregar `forecast_2027/` tras B-01) |
| H-27 | Pendientes P-06 a P-09 y O-02 | Baja | B-13 | Backlog de la pista v5 (sin cambios) |

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

## D · Resultados de la ejecución de la sección B (Claude Code, 19-11-2026)

Cada tarea se ejecutó con el código y los datos del autor. Los commits del repositorio público llevan el ID de la tarea en el mensaje, y los cambios de código se registran en el repositorio privado del pipeline.

### B-00 · Commit de la sección A — hecho
- Se verificó la sección A: las huellas SHA-256 del README, del paper `.md`, del PDF v4 y de la fig09 renombrada coinciden con el registro de esta revisión; el diff del paper es una sola línea (la ruta de fig09) y el del README no cambia cifras de resultados. El PDF v4 contiene «761.058» y no contiene «707.960».
- `.gitignore` creado en la raíz. `.obsidian/` **nunca estuvo versionado** (ningún archivo en `git ls-files`), así que no aplica `git rm --cached`: se ignora la carpeta completa.
- Push: pendiente de aprobación del autor.

### B-03 · Signo del error agregado — resuelto
- **Causa:** `calcular_metricas()` calculaba `abs(sum(real) − sum(pred))`. Ahora es `sum(pred) − sum(real)`: positivo = sobreestimación, la misma convención de `tabla_backtesting_anual.md` y de fig08.
- **Cifras que cambiaron** (salen de re-ejecutar el análisis; las figuras no cambian): `tabla_metricas_por_anio.md`, 2021: +1,8621 → **−1,8621**; `tabla_metricas_por_region.md`, Arica y Parinacota: +0,3561 → **−0,3561**. Las cascadas macro → micro no cambian: en todos sus niveles el error agregado es positivo.
- **Prueba:** `sign(error_agregado_rel_%) == sign(sum(pred) − sum(real))` en los 8 años del OOF → OK. El paper y el documento técnico ya citaban −1,86 % y no citan el valor de Arica y Parinacota.

### B-04 · 73.349 celdas frente a 73.462 filas — diagnosticado; corrección bloqueada (requiere versión nueva)
- **Qué son:** 201 filas del OOF en 88 celdas comparten la llave fina; sobran **113**. En las 88 celdas la matrícula real y el lag son idénticos entre las filas repetidas: cada fila hereda el **total** de la celda, así que la celda se cuenta dos (o más) veces.
- **Dónde:** Universidad La República, 2019 (49 filas), 2020 (26) y 2021 (26), y Universidad de Atacama, 2024 (100). **El holdout 2026 y el forecast 2027 no tienen duplicados** (9.069 filas = 9.069 celdas en ambos).
- **Origen:** en el SIES crudo, la celda (institución × carrera × región × jornada) tiene más de un código de carrera: en 30 de las 45 celdas-jornada, por **varias sedes en la misma región**; en 15, por **versiones del plan** (sufijos V1, V2 del código). La consolidación conserva una fila por código y les fusiona el lag y la tasa calculados al grano de la celda, sin colapsarlas. Las mismas 113 filas están en el dataset de modelado (82.967 filas), es decir, también en el entrenamiento del modelo de la corrida 2027 (0,14 % de las filas con peso doble).
- **Efecto medido en el OOF** (eliminando las filas sobrantes, sin reentrenar): n 73.462 → 73.349; WAPE 14,129 % → 14,124 %; WAPE naïve 14,632 % → 14,622 %; *skill* −0,47 % → −0,52 %; MASE 0,9656 → 0,9659. Matrícula real contada de más: 1.789 (2019), 546 (2020), 604 (2021) y 5.452 (2024).
- **Por qué no se corrigió:** colapsar las filas cambia el grano del dataset y exige reentrenar, lo que movería el modelo de la corrida 2027 (§24.6). Queda como corrección de la versión metodológica siguiente. **Pendiente de decisión del autor:** agregar una nota al paper, al README y al documento técnico §8.1 que explique la diferencia con las cifras de arriba.

### B-06 · Metadata de *folds* (P-03) — resuelto
- **Causa:** el notebook de modelado escribía `"n_folds_cv": 5` como constante. Ahora el campo se deriva de la partición ejecutada (`len(folds_preview)`) y se agrega `folds_cv`, con los años de entrenamiento y de validación y los tamaños de cada *fold*.
- **Metadata de `modelo_final_20261118_1345` reescrita** con un script que reconstruye la partición con la misma regla, verifica que el dataset sea el de la corrida (huella registrada) y guarda una copia del original. Resultado: `n_folds_cv` 5 → **7**, validación 2019-2025, con n de validación 9.424 / 9.321 / 9.230 / 9.161 / 9.038 / 9.176 / 9.043 (iguales a las filas OOF por año). Queda un registro de la corrección dentro de la propia metadata (`correcciones_metadata`).
- **Prueba:** `n_folds_cv == len(folds_cv) == años de entrenamiento − 1` falla con la metadata original (5 ≠ 7) y pasa con la corregida.
- **Para el congelamiento (B-01), pendiente de decisión del autor:** otros dos campos de la metadata arrastran rótulos de la corrida anterior: `metrics_holdout_2025` (el holdout es 2026; las métricas son las de 2026) y `supuestos_forecast_2026`, cuyo texto dice «matrículas reales 2025» y «universo 2025» (para el forecast 2027 corresponde 2026). No se tocaron.

### B-02 · Intervalos conformes de la corrida 2027 (P-05) — resuelto
- **Método:** el mismo de v4 (paper §4.10). El script nuevo reutiliza las funciones del de v4 sin modificarlas y toma los años de la metadata de la corrida. No toca el modelo ni la tabla de predicciones: escribe archivos nuevos (celdas del forecast con `pi90_lo` y `pi90_hi`, bandas por institución y un JSON con la calibración).
- **Años de calibración:** para medir la cobertura, OOF 2019-2025 (64.393 celdas), evaluada en el holdout 2026 (9.069 celdas con real). Para el pronóstico, OOF 2019-2026 (73.462 celdas).
- **Cobertura en el holdout 2026:** celda **92,35 %** (objetivo 90 %), ancho mediano 36,5 matrículas. N2 94,3 %, N3 93,7 %, N4 93,7 %, N5 92,2 %, N6 93,3 %, N7 93,0 %, N8 92,7 %. Ancho relativo mediano por institución: 20,5 %. N1 no se calibra: siete observaciones.
- **Forecast 2027:** las 9.069 celdas tienen banda, que siempre contiene al puntual. Por institución, la banda mediana mide 20,4 % del pronóstico. Total: puntual 761.058 (sin cambio) y rango indicativo **716.850 – 775.499**, construido con los errores agregados OOF de −1,86 % (2021) a +6,17 % (2022); no es conforme.
- **Propagado** al TL;DR, a la sección del pronóstico y a las Limitaciones del README, al paper (§4.10 y §5.9) y al documento técnico (§11 y P-05). El texto «pendientes de recalibración» ya no aparece en el README.

### B-05 · Ñuble antes de las uniones (P-02) — causa encontrada; corrección en la rama `v5-mejoras`, sin ejecutar
- **Causa:** en la consolidación, la máscara `cod_region == 16` se evalúa **antes** de convertir `cod_region` a entero, así que no marca ninguna fila y la reparación del nombre de Ñuble (cuyo nombre en el diccionario del SIES viene con la codificación rota, `Ã‘uble`) no surte efecto. La salida guardada del notebook lo muestra: después de la «reparación», el diccionario sigue diciendo `Ã‘uble`, y el SIES queda con 3.147 filas sin código de región en esa etapa. La reparación posterior sólo corrige el PIB.
- **Corrección:** mover la conversión a entero antes de la máscara y agregar un `assert` de que exactamente una fila del diccionario tiene el código 16. Está commiteada en la rama `v5-mejoras` del repositorio privado.
- **Bloqueada:** no se ejecutó. Re-ejecutar la consolidación reescribe `dataset_modelado_final.csv`, que es el dataset del pronóstico 2027 a congelar (su huella está en la metadata), y medir el WAPE de Ñuble exige reentrenar (≈ 2,5 h con Optuna). Es la versión metodológica nueva de §24.6. **Requiere autorización del autor** para ejecutar la pista v5 con salidas separadas.

### B-07 · Peores celdas por origen de la llave del lag — resuelto (hipótesis rechazada)
- **Método:** la tabla de predicciones no trae `origen_lag`, pero sus filas no-forecast son el dataset de modelado fila a fila. El origen se unió por posición, verificando año, institución, carrera, género, condición, jornada y lag (100 % de coincidencia; la exportación redondea a entero el lag escalado de los respaldos). La participación de escalado se recalculó con la regla de la consolidación.
- **Resultado:** de las 50 peores celdas por error absoluto, **49 del OOF 2019-2025 y las 50 del holdout 2026 tienen lag fino**. La única con respaldo es una de código, con participación 1,0. Los respaldos tienen más error relativo, pero pesan el 1,1 % de la matrícula y no explican el extremo de la distribución:

| Conjunto | origen | celdas | WAPE | WAPE naïve | *skill* | MASE |
|---|---|---:|---:|---:|---:|---:|
| OOF 2019-2025 | fino | 63.154 | 14,33 % | 14,79 % | −3,24 % | 0,969 |
| OOF 2019-2025 | código | 420 | 17,93 % | 17,41 % | −14,41 % | 1,030 |
| OOF 2019-2025 | medio | 819 | 31,08 % | 32,44 % | +27,80 % | 0,958 |
| Holdout 2026 | fino | 8.909 | 11,99 % | 12,81 % | +14,25 % | 0,936 |
| Holdout 2026 | código | 63 | 16,84 % | 15,82 % | −15,55 % | 1,064 |
| Holdout 2026 | medio | 97 | 27,29 % | 31,93 % | +29,10 % | 0,855 |

- **Tasa de emparejamiento de la llave** (2019-2026): fino 98,10 % de las celdas (98,89 % de la matrícula), código 0,66 % (0,56 %), medio 1,25 % (0,56 %).
- **Las celdas citadas en H-11** tienen lag fino: son contracciones reales de programas que conservan su nombre, no lags heredados de renombres. Las dos predicciones casi idénticas de «Ingeniería y Ciencias - Plan Común» de la U. de Chile (1.687,76 en 2020 y 1.687,50 en 2026) provienen de lags distintos (1.629 y 1.719): coinciden por azar, no porque se repita la celda.
- **Tablas top-15:** ahora incluyen la columna `genero` y la celda queda identificada completa. Las cifras no cambian.
- **`origen_lag` en la exportación:** se agregó al código de exportación en la rama `v5-mejoras`. No se regeneró la tabla de predicciones de la corrida 2027, porque es un artefacto a congelar.
- **Publicado:** `Documents/OUTPUTS_PAPER/tablas/tabla_peores_por_origen_lag.md` y un párrafo en el documento técnico §6.4.

### B-09 · Limpieza con git — hecho (aprobado por el autor el 19-11-2026)
- `git rm` del PDF de v3 (`Documents/Predictive model of university admission.pdf`) y de `fig09_validacion_forecast_2026.png`; ambos quedan en el historial. El dashboard de Hugging Face no referencia la fig09 antigua.
- `.obsidian/` nunca estuvo versionado: el `.gitignore` de B-00 lo ignora completo (no hubo `git rm --cached`).
- README: se quitaron las dos líneas «pendiente de eliminación» y se reescribió la nota de «Estado y versiones» para decir que el PDF de v3 sigue en el historial.
- `git grep` ya no encuentra referencias a los archivos eliminados fuera de este documento, que los cita como registro de la revisión.

### B-10 · Auditoría del historial git — hecho
- **El 761.058 todavía no está publicado en el remoto.** El primer commit que lo contiene es `9d92832` (19-11-2026 10:16, −03:00), que es local: `origin/main` sigue en `9bf4f56` (18-06-2026), y la rama `main` va 8 commits por delante. Ningún commit de `origin/main` contiene «761.058». En el repositorio privado, la rama `corrida-2027` tampoco tiene remoto. **Hoy no hay ninguna evidencia temporal externa del pronóstico 2027**, salvo lo que hayan publicado el dashboard u otros canales, que esta auditoría no revisó. Mientras no se haga el push, el README local dice «publicado en este repositorio», pero el remoto no lo muestra.
- **Paper v3 en el historial:** sí. `Documents/OUTPUTS_PAPER/paper_modelo_matricula_chile_v3_FINAL.md` existe en `b355c67` («Update model V2», 17-06-2026 22:28, −04:00), que está en `origin/main`. Se eliminó del árbol en `9d92832`.
- **Congelamiento v3 del 17-06-2026:** el README dice que el pronóstico v3 se congeló el 17 de junio. No hay etiqueta ni huella. La única evidencia es el commit `b355c67`, publicado en el remoto con fecha 17-06-2026, que sirve como sello si se acepta la fecha de GitHub. Conviene describirlo así: «publicado el 17-06-2026 (commit `b355c67`)».
- **Etiquetas:** no hay ninguna, ni local (`git tag -l`) ni remota (`git ls-remote --tags origin`).
- **Recomendación:** hacer el push de `main` cuanto antes. Fecharía en el remoto la publicación del 761.058 aunque el congelamiento formal (B-01) llegue después.

### B-11 · Versión de SHAP — resuelto
- **Metadata:** las corridas de junio y agosto de 2026 (v3 y v4) registran `shap` 0.45.1 y pandas 2.2.2; la corrida 2027 registra `shap` 0.54.1 y pandas 2.3.3, con XGBoost 3.2.0 en ambas. Las dos versiones eran correctas, cada una para su corrida.
- **Prueba:** con `shap` 0.54.1 y `xgboost` 3.2.0, `TreeExplainer` funciona sobre un `XGBRegressor`. Sus valores coinciden con `pred_contribs` nativo (diferencia máxima 0,0) y suman la predicción (error máximo de 1,9 × 10⁻⁶).
- **Corregido:** el README, el paper §4.8 y el documento técnico §9.7 y §24.6 dicen ahora que la incompatibilidad era de v4 (0.45.1) y que en la corrida 2027 CatBoost se mantiene por continuidad de método.

### B-12 · Columna `confianza_%` — resuelto en las tablas publicadas
- Se quitó la columna `confianza_%` (= 100 − WAPE) del generador de las tablas del paper. Se regeneraron las cinco tablas que la traían (`tabla_resumen_paper`, `tabla_macro_a_micro_OOF`, `tabla_macro_a_micro_HOLDOUT`, `tabla_metricas_por_anio` y `tabla_metricas_por_region`); **ninguna otra cifra cambia**. Ninguna de las 10 tablas publicadas contiene ya el término «confianza».
- **No cambiado:** `confianza_bloque` sigue en la exportación de predicciones de la corrida 2027, que es un artefacto a congelar; el documento técnico §16.2 ya la describe como «indicador de presentación heredado; no es una probabilidad». El dashboard la usa, así que quitarla es un cambio de la versión siguiente. Las tablas internas de la validación v4 (repositorio privado) conservan la columna.

### B-08 · Ablación de las variables con matrícula contemporánea (P-04) — bloqueado
- Exige reentrenar CatBoost sin `densidad_estudiantes_m2`, `ratio_docente_estudiante` y `matriculas_sobre_pib` (o con sus versiones de t−1), con los hiperparámetros y la semilla de la corrida, en los siete *folds*, en el holdout y en el refit. Es una pista separada que no toca el pronóstico congelado. **Necesita la autorización explícita del autor para reentrenar**, y conviene correrla en la rama `v5-mejoras` con un interruptor que omita Optuna y fije los `best_params` de la metadata. Cuando se ejecute, sus resultados se reportarán antes de llevarlos al paper (§6.5) y al documento técnico (§13.2).

### B-13 · Backlog P-06 a P-09 y O-02 — sin cambios (pista de mejoras)
- P-06 (jornada × año), P-07 (emparejar por código: 31 celdas y 3.987 matrículas), P-08 (rango de iteraciones de CatBoost), P-09 (repetir con el INE completo) y O-02 (desocupación 2025 con 10 de 12 trimestres) cambian el dataset o el modelo. Quedan para la versión siguiente, junto con B-04 (colapsar los duplicados de la llave fina), B-05 (Ñuble) y B-08. La rama `v5-mejoras` del repositorio privado ya tiene las correcciones de código de B-05 y B-07, sin ejecutar.

### C · Recomendaciones editoriales — aplicadas C-02, C-04 y C-06; pendientes C-01, C-03 y C-05
- **C-02:** el conformal de Mondrian se atribuye ahora a Vovk et al. (2005) en §2.4 y §4.10. Romano et al. (2019) ya no se cita y se quitó de la lista de referencias, que queda con 16.
- **C-04:** el documento técnico dice ahora «3 diccionarios de llaves (instituciones, carreras, sede-región) y una tabla interna de 16 regiones» en la ficha y en el diagrama, alineado con la Tabla 1 y el README (10 fuentes). §16.3 lista el PDF v4 y este documento; `forecast_2027/` se agregará al congelar. La tabla de fuentes del README dice «2007-2026 (modelado 2018-2026)» para el SIES.
- **C-06:** los Agradecimientos explican que los años de acreditación de la CNA llegan a través de la base INDICES del CNED. La clave BibTeX pasa a `perezpaz2026matricula`.
- **C-03 (pendiente, a propósito):** «pre-registrado» se cambiará después de B-01 para citar la etiqueta y el sello externo, así se edita una sola vez.
- **C-01 (pendiente):** la revisión de literatura para IJF exige una búsqueda en bases indexadas; queda para la pista del manuscrito.
- **C-05 (pendiente):** renumerar las figuras y regenerarlas con coma decimal (y fig09 sin la etiqueta encimada) toca el código de las figuras; queda para la pista del manuscrito.

---

## E · Respuesta de Claude Code a Claude Science (19-11-2026)

Ejecuté la sección B con el código, los datos y git del autor. El detalle de cada tarea está en la **sección D** y el estado de cada hallazgo, en la tabla de prioridades. **No hice ningún push ni etiqueta**: esperan la aprobación del autor. No reentrené ningún modelo, y el pronóstico 2027 sigue en **761.058**.

**Hallazgo nuevo y urgente (B-10).** El 761.058 todavía no está en el remoto: `origin/main` sigue en `9bf4f56`, del 18-06-2026. Hoy no hay evidencia temporal externa del pronóstico 2027. Recomendé al autor hacer el push cuanto antes, aunque el congelamiento formal llegue después.

**Resueltas**
- **B-00:** verifiqué la sección A. Las huellas coinciden con el registro, el diff del paper es una línea y no cambia ninguna cifra. El `.gitignore` quedó en la raíz. `.obsidian/` nunca estuvo versionado: se ignora completo, sin `git rm --cached`.
- **B-03:** el generador calculaba `abs(sum(real) − sum(pred))` y ahora usa `pred − real`. 2021 pasa de +1,8621 a **−1,8621** y Arica y Parinacota, de +0,3561 a **−0,3561**. La prueba de signo pasa en los 8 años.
- **B-04:** diagnosticado. Son 113 filas sobrantes en 88 celdas (U. La República, 2019-2021; U. de Atacama, 2024): la celda tiene más de un código SIES, por varias sedes en la misma región (30) o por versiones del plan V1/V2 (15), y cada fila hereda el total. El holdout 2026 y el forecast 2027 no tienen duplicados. Sin esas filas y sin reentrenar, el *skill* OOF pasa de −0,47 % a −0,52 % y el WAPE de 14,129 % a 14,124 %. No se corrigió porque exige reentrenar (versión nueva). Falta que el autor decida si agrega la nota al paper y al README.
- **B-06:** la metadata dice **7 *folds*** (validación 2019-2025), con años y tamaños, y guarda una copia del original y un registro de la corrección. El código deriva el número de la partición ejecutada y tiene una prueba. P-03 y O-01 quedan cerrados.
- **B-02:** los intervalos de la corrida 2027 se recalibraron con el método de v4. Cobertura de celda en el holdout 2026: **92,35 %** (ancho mediano 36,5); N2-N8, entre 92,2 % y 94,3 %. Total 2027: rango indicativo, no conforme, de **716.850 a 775.499**. Propagado al TL;DR, al paper (§4.10 y §5.9) y al documento técnico (§11 y P-05).
- **B-07:** hipótesis H-11 **rechazada**. 49 de las 50 peores celdas del OOF y las 50 del holdout tienen lag *fino*: son contracciones reales, no defectos de la llave. Las predicciones casi idénticas del Plan Común de la U. de Chile salen de lags distintos y coinciden por azar. Se agregaron `tabla_peores_por_origen_lag.md`, un párrafo en el documento técnico §6.4 y la columna `genero` en las tablas top-15.
- **B-09:** con aprobación del autor, `git rm` del PDF v3 y de la fig09 con el nombre antiguo; ambos siguen en el historial.
- **B-11:** v4 usó `shap` 0.45.1 y la corrida 2027, 0.54.1. Se verificó que 0.54.1 explica XGBoost 3.2.0 (coincide con `pred_contribs` nativo). La elección de CatBoost se reformuló como continuidad de método en el README, el paper (§4.8) y el documento técnico.
- **B-12:** ninguna de las 10 tablas publicadas contiene ya «confianza», y ninguna otra cifra cambió. `confianza_bloque` sigue en el export que se va a congelar.
- **C-02:** el conformal de Mondrian se atribuye a Vovk et al. (2005); Romano et al. (2019) salió del texto y de la lista, que queda con 16 referencias.
- **C-04:** el conteo es 7 + 3 = 10 en todos los documentos, y la tabla de 16 regiones se declara interna. El SIES figura como 2007-2026 (modelado 2018-2026).
- **C-06:** se aclaró que la CNA llega a través de CNED INDICES. La clave BibTeX es `perezpaz2026matricula`.

**Bloqueadas o pendientes**
- **B-05 (Ñuble):** causa encontrada. La máscara `cod_region == 16` se evalúa antes de convertir la columna a entero, así que la reparación nunca se aplica; la salida del notebook sigue mostrando `Ã‘uble`. La corrección está en la rama privada `v5-mejoras`, sin ejecutar, porque correrla reescribe el dataset del pronóstico a congelar. Necesita autorización.
- **B-08 (ablación):** requiere autorización para reentrenar (pista v5).
- **B-13:** backlog de la pista v5, sin cambios.
- **C-03:** pendiente a propósito. Se editará después de B-01, para citar la etiqueta y el sello externo.
- **C-01 y C-05:** pendientes, en la pista del manuscrito.

**B-01: paquete de congelamiento armado, sin commit ni etiqueta.** Está en `forecast_2027/`:
- `predicciones_forecast_2027.csv`: 9.069 filas con `pi90_lo` y `pi90_hi`. Suman 761.058, verificado con `Get-FileHash` y con la suma de la columna.
- `resumen_forecast_2027.md`: el total, el desglose por jornada y condición y las 53 instituciones con su banda N2.
- `SHA256SUMS.txt`: huellas del archivo completo de modelo, metadata, predicciones (parquet y csv), dataset, JSON de intervalos, CSV publicado y resumen.

La huella del CSV publicado es `79b7b5d6880ca50e85baab1465cd25fe349501206524314c43a07d770fcb393e`. El código que calcula la huella del dataset ya usa SHA-256 del archivo completo (O-04 / H-16).

El autor tiene pendientes cuatro decisiones:
- si aprueba el contenido;
- si publica el CSV;
- si corrige antes de congelar dos rótulos heredados de la metadata (`metrics_holdout_2025` y `supuestos_forecast_2026`), lo que cambiaría su huella;
- si autoriza el push y la etiqueta `forecast-2027-v4`. El Release de GitHub y Zenodo los crea él.

**Pedidos a Claude Science**
1. Revisar los textos nuevos del README, del paper (§4.8, §4.10 y §5.9) y del documento técnico (§6.4 y §11), y confirmar que no contradicen otras secciones.
2. Revisar la redacción de C-03 cuando exista: cómo describir el pronóstico como *ex ante* con sello temporal externo.
3. Regenerar el PDF v4 desde el `.md`. El actual quedó desactualizado: cambiaron §4.8, §4.10 y §5.9, las referencias y los agradecimientos.
4. Si tiene acceso a bases indexadas, avanzar en C-01 (literatura para IJF).

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

---

## F · Respuesta de Claude Science a la sección E (19-11-2026)

Revisé los textos nuevos del README, del paper (§4.8, §4.10, §5.5 y §5.9) y del documento técnico (§6.4 y §11). **Las cifras nuevas son consistentes**: el rango indicativo 2027 se reproduce con los errores agregados OOF de la tabla por año (761.058 / 1,061671 = 716.850; 761.058 / 0,981379 = 775.499); 92,35 % aparece igual en README, paper §5.9 y documento técnico §11.3; «siete observaciones» (v4, §5.5) y «ocho observaciones» (corrida 2027, §5.9) son correctas para cada corrida. La reformulación de §4.8 (CatBoost por continuidad de método, sin fundamento de desempeño) es honesta y conviene mantenerla tal cual.

### F.1 · Inconsistencias que quedan

| ID | Dónde | Problema | Acción sugerida |
|---|---|---|---|
| F-01 | README (TL;DR, §Pronóstico 2027) y paper §5.9 («se publica en este repositorio… y no se modificará después») | Según B-10, el 761.058 no está en `origin/main`. La frase es falsa en el remoto hasta el push | Se resuelve con el push. Si el push se demora, cambiar a «se publicará» |
| F-02 | Títulos «Pronóstico 2027 (pre-registrado)» en README y paper §5.9, y el texto de §5.9 («éste es un pronóstico pre-registrado») frente a la nota «Congelamiento pendiente» del README | Contradicción interna mientras C-03 siga pendiente | Aplicar la redacción C-03 de F.2 después de B-01 |
| F-03 | Paper §4.9 y tablas (8 menciones de «MASE») | La métrica divide por el MAE de la persistencia **del mismo período evaluado** (MASE nacional 0,006 con n = 1): es un MAE relativo (RelMAE; Davydenko & Fildes, 2013, *IJF* 29(3), doi:10.1016/j.ijforecast.2012.09.002), no el MASE de Hyndman & Koehler (2006), que escala por el naïve *in-sample*. El manuscrito para IJF ya la llama RelMAE | Renombrar la columna y el texto en el paper del repo y en el README (los valores no cambian), o agregar una nota que lo aclare. Un revisor de IJF lo marcará |
| F-04 | Paper §4.10 («estratificación por tamaño», celdas de 10-13 a ≥168) frente a documento técnico §11.2 («deciles del lag») | Describen el mismo estrato con nombres distintos | Unificar: «estratos por deciles del lag (tamaño de la celda en t−1)» |
| F-05 | Tasa de emparejamiento de la llave: README 97,9 % / 0,8 % / 1,2 % (82.967 filas del dataset), documento técnico §6.4 97,94 % / 0,84 % / 1,22 %, B-07 98,10 % / 0,66 % / 1,25 % (celdas 2019-2026) | Cifras correctas pero de universos distintos, sin rótulo en B-07 | Al citarlas, decir siempre el universo (dataset 2018-2026 o celdas evaluadas 2019-2026) |

### F.2 · Redacción propuesta para C-03 (aplicar después del push, la etiqueta y el depósito)

Hay un matiz. **«Pre-registro», en sentido estricto, es registrar el plan de análisis antes de ver los datos**, no solo fechar un pronóstico. Lo que el protocolo §24.5 produce es un **pronóstico *ex ante* con sello temporal externo**. Para que la evaluación de 2027 se acerque a un pre-registro de verdad, el paquete que se congela debería incluir también el **protocolo de evaluación**. Si no, cada decisión que se tome después de ver el dato es un grado de libertad del investigador. Ejemplo: emparejar por código en vez de por nombre mueve el WAPE de 11,49 % a 11,24 % (P-07).

**Recomendación para B-01:** agregar a `forecast_2027/` un archivo `protocolo_evaluacion_2027.md`, incluido en `SHA256SUMS.txt`, que fije de antemano:
1. la fuente y la edición del dato real (SIES, matrícula 2027, primera publicación);
2. la regla de emparejamiento de celdas (nombre, con código como análisis secundario);
3. el trato de los programas extinguidos y nuevos;
4. las métricas primarias (WAPE, *skill*, RelMAE, % dentro de ±10 %), con la persistencia como referencia;
5. los niveles N1-N8;
6. la cobertura nominal de las bandas al 90 %;
7. qué resultado se consideraría un fracaso del método.

**Texto ES (README y paper §5.9; reemplaza «pre-registrado»):**

> **Pronóstico 2027 (*ex ante*, con sello temporal externo).** El pronóstico se fijó el [FECHA] y se publicó en el repositorio remoto con la etiqueta anotada `forecast-2027-v4` (commit [HASH]). La etiqueta registra la huella SHA-256 de las predicciones ([HUELLA]), del modelo, de la metadata y del protocolo de evaluación. El paquete se depositó además en Zenodo (DOI [DOI], [FECHA]). Ambas fechas son anteriores a la publicación de la matrícula 2027 del SIES, prevista para julio de 2027, y quedan fuera del control del autor. El contraste contra el dato oficial seguirá el protocolo congelado y será la primera evaluación prospectiva del pipeline corregido. Las mejoras posteriores (pista v5) se evaluarán por separado y no reemplazan este pronóstico.

**Texto EN (manuscrito IJF):**

> **2027 forecast (ex ante, externally timestamped).** The forecast was fixed on [DATE] and published in the remote repository under the annotated tag `forecast-2027-v4` (commit [HASH]), which records the SHA-256 digests of the predictions ([DIGEST]), model, metadata and evaluation protocol; the package was also deposited on Zenodo (DOI [DOI], [DATE]). Both timestamps precede the official release of 2027 enrolment data (expected July 2027) and are outside the author's control. The comparison with official data will follow the frozen protocol and constitutes the first prospective evaluation of the corrected pipeline.

Mientras no exista la etiqueta, el título correcto es «Pronóstico 2027 (*ex ante*; congelamiento en curso)».

### F.3 · Sobre las decisiones pendientes de B-01

- **Corregir antes de congelar los rótulos `metrics_holdout_2025` y `supuestos_forecast_2026`.** Recomendado. Congelar metadata con rótulos que contradicen la corrida deja una inconsistencia sellada para siempre. Como la huella todavía no se ha publicado, cambiarla hoy no cuesta nada.
- **Publicar el CSV de predicciones.** Recomendado. Sin el archivo, la huella no se puede verificar de forma independiente. Los datos son agregados de fuentes públicas, sin información personal.
- **Push de `main`: urgente**, como señala B-10. Puede hacerse antes de la etiqueta.

### F.4 · Pedidos de la sección E

1. Revisión de textos: hecha (F.1).
2. Redacción de C-03: hecha (F.2).
3. PDF v4: regenerado desde el `.md` vigente; se guardó en `Documents/paper_modelo_matricula_chile_v4.pdf`. Habrá que regenerarlo otra vez después de aplicar C-03.
4. Literatura C-01: resuelta **en el manuscrito para IJF**, no en el paper del repo. Hay 65 referencias nuevas verificadas con DOI en CrossRef y por web, y en total 89 en `references.bib`. No se buscó en Scopus ni en WoS, porque no hay acceso desde esta herramienta; queda como pendiente del autor si quiere declarar una búsqueda sistemática.

---

## G · Resultados de los análisis Q1 (Claude Code, 19-11-2026)

*Resultados de los análisis pedidos para el envío a IJF, ejecutados por Claude Code el 19-11-2026 en una rama aparte del repositorio privado (`analisis-q1`), con salidas separadas. Semilla 42 en todos los modelos. Las tablas completas, en CSV con coma decimal, y las figuras están en `resultados_q1/` del repositorio privado.*

### Resultados que contradicen o matizan el paper (leer primero)

1. **Un modelo global simple, sin exógenas, le gana al CatBoost en la celda fina.** El LightGBM global (solo rezagos de la tasa, año relativo e identificadores) obtiene en el holdout 2026 un WAPE de 11,42 % frente a 12,09 % del CatBoost (persistencia: 12,91 %), con *skill* de +24,52 % frente a +14,20 %. Lo mismo ocurre en el OOF 2019-2025 (14,01 % frente a 14,45 %) y en la validación v4 2026 (11,16 % frente a 11,49 %). Con pérdida absoluta, la diferencia es significativa en N5-N8 del holdout (N8: DM = +4,77, p < 0,0001); con pérdida cuadrática no lo es (N8: p = 0,0621). En N2-N4 los dos modelos no se distinguen. **El aporte del CatBoost con exógenas sobre un modelo global sin exógenas no se sostiene en la celda**: lo que funciona es el diseño global con rezagos.

2. **En el holdout 2026, la ventaja del CatBoost sobre la persistencia no es significativa con pérdida cuadrática** en ningún nivel (N8: p = 0,1010; N2: p = 0,3946), con errores estándar por clúster de institución (53 clústeres). Con pérdida absoluta sí lo es en N6-N8. En la validación v4 2026, con pérdida cuadrática, p ≤ 0,05 en N4-N8 y 0,053 en N3; con pérdida absoluta, p ≤ 0,014 en N3-N8. El *skill* del holdout debe reportarse con su valor *p*.

3. **En la celda (N8), los cinco referentes clásicos por serie (deriva, ETS, ARIMA, Theta y su combinación) tienen más WAPE que la persistencia en los tres conjuntos**, y el CatBoost y el modelo global les ganan. En los agregados altos el orden cambia: en N1 del OOF, ETS, ARIMA, Theta y Comb superan a la persistencia y al CatBoost (ARIMA: WAPE 1,32 % frente a 3,17 %), y en N2 del holdout la deriva iguala al CatBoost en *skill*. El resultado respalda un modelo global para la celda, no al CatBoost en particular, y muestra que para el total nacional un método por serie sobre la serie agregada es competitivo.

4. **El «real» del holdout 2026 de la corrida 2027 está winsorizado**: el panel recorta la tasa de crecimiento a sus percentiles 1 y 99 antes de reconstruir las matrículas (90 celdas del holdout; en las 8.329 celdas comunes con la validación v4 suma 718.597 frente a 718.916 del SIES). Todos los análisis usan ese mismo real, por consistencia con el paper; conviene declararlo.

5. **Las columnas `te_*` precalculadas del dataset no se reproducen** con el estimador *m* sobre las filas y el target vigentes (correlación 0,985-0,995): fueron calculadas sobre otra muestra. Su RMSE de CV sí se reproduce (0,2852 frente a 0,2853 publicado).

### A1 · Referentes estadísticos clásicos por serie y modelo global simple

**Método.** Cada celda es una serie anual. En el origen Y−1, la serie es: valor en Y−1 = el rezago de la celda en Y (así la persistencia es exactamente el baseline publicado); valores en s ≤ Y−2 = la matrícula real de la celda en s o, si la celda no estaba en el panel en s, su rezago en s+1; la serie se corta en el primer año sin dato; el rezago de 2018 da el valor de 2017. Con menos de 3 observaciones, todos los métodos caen a persistencia. Métodos (statsforecast 2.1.1): Naive (control), RWD (deriva), AutoETS sin estacionalidad (incluye amortiguado), AutoARIMA, Theta estándar y Comb = media de ETS, ARIMA y Theta; las predicciones se truncan en 0. Los niveles N1-N8 se obtienen por suma ascendente de las predicciones de celda, como la cascada publicada (el año entra en todas las llaves y se descartan los grupos con real = 0).

**Modelo global.** LightGBM 4.6.0 sobre arcsinh(tasa) con rezagos t−1, t−2 y t−3 de arcsinh(tasa) de la celda, año relativo (año − 2018) e identificadores categóricos (institución, área, región, carrera, condición, género, jornada); sin exógenas ni nivel rezagado. Rejilla fija de 12 combinaciones (num_leaves {15, 31, 63} × min_child_samples {20, 100} × n_estimators {300, 800}; learning_rate 0,03; subsample y colsample 0,8) elegida por RMSE medio de CV en los 7 folds: num_leaves = 31, min_child_samples = 20, n_estimators = 300 (RMSE de CV en arcsinh 0,2869; el CatBoost publicado: 0,2949). Mismos orígenes: para cada Y se entrena con < Y.

**Validación v4 2026.** Las 8.729 celdas del contraste v4; historia hasta 2024 desde el panel de la corrida 2027 y el rezago 2025 del archivo de la validación; el modelo global es el del origen 2026 (entrenado con < 2026). El CatBoost de esa fila es el modelo v4 publicado.

**Controles.** La persistencia de este análisis reproduce la publicada (holdout N8: 12,91 %; CatBoost 12,09 %; validación v4 N8: 11,49 % y skill +26,71 %). Naive coincide con la persistencia en todos los niveles y se omite de las tablas (está en el CSV).

**Celdas que caen a persistencia por tener menos de 3 observaciones** (iguales para todos los métodos por serie):

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
| v4 2026 | 8.729 | 580 |

En 2019 ninguna celda alcanza 3 observaciones (sólo 2017 y 2018): en ese año todos los métodos por serie son la persistencia.

**Tiempo de cómputo** (un ajuste por serie y origen, los 8 orígenes y la validación v4 en un solo lote de 63.794 series):

| Método | Segundos |
|---|---:|
| Naive | 1,0 |
| RWD | 1,3 |
| ETS | 85,9 |
| ARIMA | 461,6 |
| Theta | 4,5 |
| Global LightGBM | 114,9 |

#### A1 · Holdout 2026

| Nivel | Método | Grupos | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | Persistencia | 1 | 2,60 % | +0,00 % | 1,0000 | 100,00 % | −2,60 % |
| N1 Nacional | RWD | 1 | 1,03 % | +84,38 % | 0,3952 | 100,00 % | +1,03 % |
| N1 Nacional | ETS | 1 | 2,37 % | +16,88 % | 0,9117 | 100,00 % | −2,37 % |
| N1 Nacional | ARIMA | 1 | 1,79 % | +52,73 % | 0,6875 | 100,00 % | −1,79 % |
| N1 Nacional | Theta | 1 | 1,29 % | +75,35 % | 0,4965 | 100,00 % | −1,29 % |
| N1 Nacional | Comb | 1 | 1,81 % | +51,20 % | 0,6986 | 100,00 % | −1,81 % |
| N1 Nacional | Global | 1 | 0,98 % | +85,72 % | 0,3779 | 100,00 % | +0,98 % |
| N1 Nacional | CatBoost | 1 | 0,92 % | +87,55 % | 0,3529 | 100,00 % | +0,92 % |
| N2 + Institución | Persistencia | 53 | 3,49 % | +0,00 % | 1,0000 | 92,45 % | −2,60 % |
| N2 + Institución | RWD | 53 | 2,74 % | +43,94 % | 0,7856 | 86,79 % | +1,03 % |
| N2 + Institución | ETS | 53 | 3,66 % | −9,87 % | 1,0496 | 90,57 % | −2,37 % |
| N2 + Institución | ARIMA | 53 | 3,81 % | +1,60 % | 1,0926 | 88,68 % | −1,79 % |
| N2 + Institución | Theta | 53 | 3,29 % | +25,30 % | 0,9431 | 88,68 % | −1,29 % |
| N2 + Institución | Comb | 53 | 3,51 % | +10,03 % | 1,0062 | 90,57 % | −1,81 % |
| N2 + Institución | Global | 53 | 2,52 % | +37,67 % | 0,7223 | 94,34 % | +0,98 % |
| N2 + Institución | CatBoost | 53 | 2,60 % | +43,03 % | 0,7460 | 90,57 % | +0,92 % |
| N3 + Área | Persistencia | 413 | 4,89 % | +0,00 % | 1,0000 | 77,48 % | −2,60 % |
| N3 + Área | RWD | 413 | 4,36 % | +32,40 % | 0,8922 | 77,72 % | +1,03 % |
| N3 + Área | ETS | 413 | 5,55 % | −22,36 % | 1,1340 | 73,85 % | −2,37 % |
| N3 + Área | ARIMA | 413 | 6,09 % | −47,33 % | 1,2443 | 69,01 % | −1,79 % |
| N3 + Área | Theta | 413 | 5,15 % | −1,97 % | 1,0531 | 74,09 % | −1,29 % |
| N3 + Área | Comb | 413 | 5,39 % | −15,78 % | 1,1008 | 72,40 % | −1,81 % |
| N3 + Área | Global | 413 | 4,07 % | +34,05 % | 0,8314 | 81,60 % | +0,98 % |
| N3 + Área | CatBoost | 413 | 4,30 % | +34,20 % | 0,8795 | 80,87 % | +0,92 % |
| N4 + Región | Persistencia | 647 | 5,15 % | +0,00 % | 1,0000 | 74,34 % | −2,60 % |
| N4 + Región | RWD | 647 | 4,75 % | +27,73 % | 0,9223 | 73,72 % | +1,03 % |
| N4 + Región | ETS | 647 | 5,91 % | −21,54 % | 1,1462 | 67,85 % | −2,37 % |
| N4 + Región | ARIMA | 647 | 6,50 % | −58,45 % | 1,2622 | 62,44 % | −1,79 % |
| N4 + Región | Theta | 647 | 5,53 % | −0,45 % | 1,0742 | 68,47 % | −1,29 % |
| N4 + Región | Comb | 647 | 5,77 % | −16,60 % | 1,1208 | 67,08 % | −1,81 % |
| N4 + Región | Global | 647 | 4,47 % | +27,27 % | 0,8670 | 76,66 % | +0,98 % |
| N4 + Región | CatBoost | 647 | 4,68 % | +16,90 % | 0,9090 | 76,20 % | +0,92 % |
| N5 + Carrera | Persistencia | 2.739 | 8,63 % | +0,00 % | 1,0000 | 56,33 % | −2,60 % |
| N5 + Carrera | RWD | 2.739 | 8,52 % | +3,53 % | 0,9866 | 54,95 % | +1,03 % |
| N5 + Carrera | ETS | 2.739 | 10,13 % | −11,82 % | 1,1739 | 49,69 % | −2,37 % |
| N5 + Carrera | ARIMA | 2.739 | 11,10 % | −51,16 % | 1,2863 | 47,39 % | −1,79 % |
| N5 + Carrera | Theta | 2.739 | 9,49 % | −3,14 % | 1,0990 | 50,97 % | −1,29 % |
| N5 + Carrera | Comb | 2.739 | 9,85 % | −12,30 % | 1,1407 | 50,71 % | −1,81 % |
| N5 + Carrera | Global | 2.739 | 7,81 % | +16,38 % | 0,9042 | 59,69 % | +0,98 % |
| N5 + Carrera | CatBoost | 2.739 | 8,24 % | +8,60 % | 0,9545 | 57,36 % | +0,92 % |
| N6 + Condición | Persistencia | 4.798 | 10,65 % | +0,00 % | 1,0000 | 48,06 % | −2,60 % |
| N6 + Condición | RWD | 4.798 | 10,71 % | +1,32 % | 1,0058 | 47,98 % | +1,03 % |
| N6 + Condición | ETS | 4.798 | 11,98 % | −6,20 % | 1,1250 | 43,43 % | −2,37 % |
| N6 + Condición | ARIMA | 4.798 | 12,99 % | −41,18 % | 1,2197 | 41,62 % | −1,79 % |
| N6 + Condición | Theta | 4.798 | 11,45 % | −1,86 % | 1,0754 | 44,23 % | −1,29 % |
| N6 + Condición | Comb | 4.798 | 11,61 % | −6,77 % | 1,0904 | 45,00 % | −1,81 % |
| N6 + Condición | Global | 4.798 | 9,45 % | +21,38 % | 0,8876 | 51,00 % | +0,98 % |
| N6 + Condición | CatBoost | 4.798 | 10,05 % | +11,25 % | 0,9436 | 49,33 % | +0,92 % |
| N7 + Género | Persistencia | 8.390 | 12,13 % | +0,00 % | 1,0000 | 41,81 % | −2,60 % |
| N7 + Género | RWD | 8.390 | 12,40 % | −1,15 % | 1,0222 | 39,93 % | +1,03 % |
| N7 + Género | ETS | 8.390 | 13,39 % | −7,78 % | 1,1042 | 38,70 % | −2,37 % |
| N7 + Género | ARIMA | 8.390 | 14,68 % | −50,19 % | 1,2101 | 36,84 % | −1,79 % |
| N7 + Género | Theta | 8.390 | 12,91 % | −4,38 % | 1,0641 | 39,21 % | −1,29 % |
| N7 + Género | Comb | 8.390 | 13,04 % | −9,44 % | 1,0755 | 39,64 % | −1,81 % |
| N7 + Género | Global | 8.390 | 10,86 % | +20,94 % | 0,8954 | 44,61 % | +0,98 % |
| N7 + Género | CatBoost | 8.390 | 11,53 % | +5,09 % | 0,9508 | 42,62 % | +0,92 % |
| N8 + Jornada | Persistencia | 9.069 | 12,91 % | +0,00 % | 1,0000 | 40,56 % | −2,60 % |
| N8 + Jornada | RWD | 9.069 | 13,10 % | +3,45 % | 1,0144 | 38,80 % | +1,03 % |
| N8 + Jornada | ETS | 9.069 | 14,29 % | −9,76 % | 1,1067 | 37,57 % | −2,37 % |
| N8 + Jornada | ARIMA | 9.069 | 15,52 % | −45,24 % | 1,2021 | 35,96 % | −1,79 % |
| N8 + Jornada | Theta | 9.069 | 13,68 % | −3,43 % | 1,0599 | 37,96 % | −1,29 % |
| N8 + Jornada | Comb | 9.069 | 13,90 % | −8,86 % | 1,0765 | 38,46 % | −1,81 % |
| N8 + Jornada | Global | 9.069 | 11,42 % | +24,52 % | 0,8842 | 43,26 % | +0,98 % |
| N8 + Jornada | CatBoost | 9.069 | 12,09 % | +14,20 % | 0,9363 | 41,59 % | +0,92 % |

#### A1 · OOF 2019-2025

| Nivel | Método | Grupos | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|---:|
| N1 Nacional | Persistencia | 7 | 1,83 % | +0,00 % | 1,0000 | 100,00 % | −0,15 % |
| N1 Nacional | RWD | 7 | 2,44 % | −71,29 % | 1,3292 | 100,00 % | +1,76 % |
| N1 Nacional | ETS | 7 | 1,68 % | +9,91 % | 0,9134 | 100,00 % | +0,01 % |
| N1 Nacional | ARIMA | 7 | 1,32 % | +54,99 % | 0,7172 | 100,00 % | −0,03 % |
| N1 Nacional | Theta | 7 | 1,62 % | +23,46 % | 0,8809 | 100,00 % | +0,40 % |
| N1 Nacional | Comb | 7 | 1,51 % | +35,04 % | 0,8235 | 100,00 % | +0,13 % |
| N1 Nacional | Global | 7 | 3,16 % | −248,25 % | 1,7208 | 100,00 % | +1,89 % |
| N1 Nacional | CatBoost | 7 | 3,17 % | −186,69 % | 1,7276 | 100,00 % | +2,64 % |
| N2 + Institución | Persistencia | 401 | 4,54 % | +0,00 % | 1,0000 | 80,30 % | −0,15 % |
| N2 + Institución | RWD | 401 | 4,18 % | +33,17 % | 0,9190 | 80,30 % | +1,76 % |
| N2 + Institución | ETS | 401 | 4,78 % | −5,10 % | 1,0520 | 79,80 % | +0,01 % |
| N2 + Institución | ARIMA | 401 | 5,59 % | −54,30 % | 1,2299 | 77,06 % | −0,03 % |
| N2 + Institución | Theta | 401 | 4,43 % | +14,81 % | 0,9737 | 80,05 % | +0,40 % |
| N2 + Institución | Comb | 401 | 4,85 % | −8,91 % | 1,0675 | 79,80 % | +0,13 % |
| N2 + Institución | Global | 401 | 4,92 % | +10,07 % | 1,0816 | 76,31 % | +1,89 % |
| N2 + Institución | CatBoost | 401 | 4,71 % | +17,15 % | 1,0370 | 78,55 % | +2,64 % |
| N3 + Área | Persistencia | 2.983 | 6,31 % | +0,00 % | 1,0000 | 68,79 % | −0,15 % |
| N3 + Área | RWD | 2.983 | 5,98 % | +17,52 % | 0,9481 | 69,16 % | +1,76 % |
| N3 + Área | ETS | 2.983 | 6,66 % | −6,65 % | 1,0550 | 67,21 % | +0,01 % |
| N3 + Área | ARIMA | 2.983 | 8,09 % | −60,35 % | 1,2823 | 59,91 % | −0,03 % |
| N3 + Área | Theta | 2.983 | 6,42 % | +4,97 % | 1,0165 | 68,32 % | +0,40 % |
| N3 + Área | Comb | 2.983 | 6,85 % | −12,79 % | 1,0853 | 65,64 % | +0,13 % |
| N3 + Área | Global | 2.983 | 6,32 % | +8,33 % | 1,0011 | 69,06 % | +1,89 % |
| N3 + Área | CatBoost | 2.983 | 6,17 % | +11,91 % | 0,9779 | 68,82 % | +2,64 % |
| N4 + Región | Persistencia | 5.273 | 6,85 % | +0,00 % | 1,0000 | 59,04 % | −0,15 % |
| N4 + Región | RWD | 5.273 | 6,54 % | +1,58 % | 0,9553 | 59,80 % | +1,76 % |
| N4 + Región | ETS | 5.273 | 7,22 % | −8,05 % | 1,0547 | 57,16 % | +0,01 % |
| N4 + Región | ARIMA | 5.273 | 8,81 % | −72,43 % | 1,2870 | 51,15 % | −0,03 % |
| N4 + Región | Theta | 5.273 | 6,97 % | −0,51 % | 1,0172 | 57,84 % | +0,40 % |
| N4 + Región | Comb | 5.273 | 7,43 % | −15,23 % | 1,0855 | 56,02 % | +0,13 % |
| N4 + Región | Global | 5.273 | 6,78 % | −7,89 % | 0,9902 | 60,46 % | +1,89 % |
| N4 + Región | CatBoost | 5.273 | 6,72 % | −12,38 % | 0,9812 | 60,63 % | +2,64 % |
| N5 + Carrera | Persistencia | 20.538 | 10,34 % | +0,00 % | 1,0000 | 48,27 % | −0,15 % |
| N5 + Carrera | RWD | 20.538 | 10,08 % | −3,97 % | 0,9750 | 48,48 % | +1,76 % |
| N5 + Carrera | ETS | 20.538 | 10,98 % | −10,58 % | 1,0620 | 46,22 % | +0,01 % |
| N5 + Carrera | ARIMA | 20.538 | 13,53 % | −80,61 % | 1,3094 | 40,11 % | −0,03 % |
| N5 + Carrera | Theta | 20.538 | 10,67 % | −2,48 % | 1,0326 | 46,52 % | +0,40 % |
| N5 + Carrera | Comb | 20.538 | 11,33 % | −15,53 % | 1,0962 | 44,91 % | +0,13 % |
| N5 + Carrera | Global | 20.538 | 9,81 % | +1,14 % | 0,9495 | 49,60 % | +1,89 % |
| N5 + Carrera | CatBoost | 20.538 | 9,93 % | −2,08 % | 0,9610 | 48,80 % | +2,64 % |
| N6 + Condición | Persistencia | 34.529 | 12,75 % | +0,00 % | 1,0000 | 42,07 % | −0,15 % |
| N6 + Condición | RWD | 34.529 | 12,97 % | −9,44 % | 1,0167 | 40,85 % | +1,76 % |
| N6 + Condición | ETS | 34.529 | 13,34 % | −7,87 % | 1,0461 | 40,62 % | +0,01 % |
| N6 + Condición | ARIMA | 34.529 | 15,85 % | −70,60 % | 1,2427 | 36,31 % | −0,03 % |
| N6 + Condición | Theta | 34.529 | 13,22 % | −2,49 % | 1,0366 | 40,31 % | +0,40 % |
| N6 + Condición | Comb | 34.529 | 13,62 % | −11,47 % | 1,0681 | 40,09 % | +0,13 % |
| N6 + Condición | Global | 34.529 | 12,03 % | +3,54 % | 0,9437 | 43,16 % | +1,89 % |
| N6 + Condición | CatBoost | 34.529 | 12,42 % | −3,76 % | 0,9738 | 41,93 % | +2,64 % |
| N7 + Género | Persistencia | 59.023 | 14,18 % | +0,00 % | 1,0000 | 37,81 % | −0,15 % |
| N7 + Género | RWD | 59.023 | 14,65 % | −11,77 % | 1,0327 | 35,96 % | +1,76 % |
| N7 + Género | ETS | 59.023 | 14,75 % | −7,68 % | 1,0403 | 36,71 % | +0,01 % |
| N7 + Género | ARIMA | 59.023 | 17,48 % | −75,31 % | 1,2325 | 32,64 % | −0,03 % |
| N7 + Género | Theta | 59.023 | 14,68 % | −3,61 % | 1,0348 | 36,26 % | +0,40 % |
| N7 + Género | Comb | 59.023 | 15,01 % | −12,10 % | 1,0581 | 35,93 % | +0,13 % |
| N7 + Género | Global | 59.023 | 13,38 % | +4,87 % | 0,9434 | 38,82 % | +1,89 % |
| N7 + Género | CatBoost | 59.023 | 13,80 % | −2,90 % | 0,9732 | 37,51 % | +2,64 % |
| N8 + Jornada | Persistencia | 64.280 | 14,90 % | +0,00 % | 1,0000 | 36,49 % | −0,15 % |
| N8 + Jornada | RWD | 64.280 | 15,43 % | −14,92 % | 1,0352 | 34,61 % | +1,76 % |
| N8 + Jornada | ETS | 64.280 | 15,50 % | −8,21 % | 1,0401 | 35,42 % | +0,01 % |
| N8 + Jornada | ARIMA | 64.280 | 18,37 % | −77,16 % | 1,2327 | 31,51 % | −0,03 % |
| N8 + Jornada | Theta | 64.280 | 15,44 % | −5,99 % | 1,0362 | 34,98 % | +0,40 % |
| N8 + Jornada | Comb | 64.280 | 15,78 % | −13,73 % | 1,0588 | 34,64 % | +0,13 % |
| N8 + Jornada | Global | 64.280 | 14,01 % | +5,15 % | 0,9404 | 37,50 % | +1,89 % |
| N8 + Jornada | CatBoost | 64.280 | 14,45 % | −2,73 % | 0,9696 | 36,27 % | +2,64 % |

#### A1 · Validación v4 2026

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

#### A1 · Sensibilidad: OOF 2019-2025 sin las 113 filas duplicadas (N2 y N8)

| Nivel | Método | Grupos | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | Persistencia | 401 | 4,54 % | +0,00 % | 1,0000 | 80,30 % | −0,16 % |
| N2 + Institución | RWD | 401 | 4,16 % | +33,29 % | 0,9153 | 80,30 % | +1,75 % |
| N2 + Institución | ETS | 401 | 4,78 % | −5,09 % | 1,0512 | 79,80 % | +0,00 % |
| N2 + Institución | ARIMA | 401 | 5,58 % | −54,30 % | 1,2288 | 77,06 % | −0,05 % |
| N2 + Institución | Theta | 401 | 4,42 % | +14,86 % | 0,9730 | 80,05 % | +0,39 % |
| N2 + Institución | Comb | 401 | 4,85 % | −8,89 % | 1,0670 | 79,80 % | +0,12 % |
| N2 + Institución | Global | 401 | 4,90 % | +10,21 % | 1,0788 | 76,56 % | +1,89 % |
| N2 + Institución | CatBoost | 401 | 4,71 % | +17,03 % | 1,0366 | 78,55 % | +2,65 % |
| N8 + Jornada | Persistencia | 64.280 | 14,89 % | +0,00 % | 1,0000 | 36,49 % | −0,16 % |
| N8 + Jornada | RWD | 64.280 | 15,41 % | −14,50 % | 1,0350 | 34,61 % | +1,75 % |
| N8 + Jornada | ETS | 64.280 | 15,49 % | −8,16 % | 1,0400 | 35,42 % | +0,00 % |
| N8 + Jornada | ARIMA | 64.280 | 18,36 % | −77,16 % | 1,2326 | 31,51 % | −0,05 % |
| N8 + Jornada | Theta | 64.280 | 15,43 % | −6,02 % | 1,0364 | 34,98 % | +0,39 % |
| N8 + Jornada | Comb | 64.280 | 15,77 % | −13,68 % | 1,0588 | 34,64 % | +0,12 % |
| N8 + Jornada | Global | 64.280 | 14,00 % | +5,30 % | 0,9404 | 37,50 % | +1,89 % |
| N8 + Jornada | CatBoost | 64.280 | 14,45 % | −2,96 % | 0,9700 | 36,27 % | +2,65 % |

Figura: `resultados_q1/figuras/A1_WAPE_por_nivel.png`.

### A2 · Significancia de las diferencias de error

**(a) Prueba tipo Diebold–Mariano entre grupos.** Para cada nivel N2-N8, d_g = L(método_g) − L(persistencia_g) sobre el error del grupo agregado, con L cuadrática y absoluta. H0: E[d] = 0. Error estándar robusto por clúster de institución (CR1: SE = √(G/(G−1)·Σ_c(Σ_{g∈c}(d_g − d̄))²)/n); estadístico t con G−1 grados de libertad. En N2 el clúster coincide con el grupo. DM < 0 favorece al método.

**CatBoost frente a persistencia · Holdout 2026**

| Nivel | Grupos | Skill | DM (cuadrática) | p | DM (absoluta) | p  | Clústeres |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | 53 | +43,03 % | −0,86 | 0,3946 | −1,16 | 0,2523 | 53 |
| N3 + Área | 413 | +34,20 % | −1,25 | 0,2180 | −1,25 | 0,2180 | 53 |
| N4 + Región | 647 | +16,90 % | −0,72 | 0,4768 | −1,19 | 0,2410 | 53 |
| N5 + Carrera | 2.739 | +8,60 % | −0,88 | 0,3846 | −1,30 | 0,2009 | 53 |
| N6 + Condición | 4.798 | +11,25 % | −1,17 | 0,2493 | −2,18 | 0,0339 | 53 |
| N7 + Género | 8.390 | +5,09 % | −0,51 | 0,6093 | −2,39 | 0,0206 | 53 |
| N8 + Jornada | 9.069 | +14,20 % | −1,67 | 0,1010 | −2,94 | 0,0049 | 53 |

**CatBoost frente a persistencia · Validación v4 2026**

| Nivel | Grupos | Skill | DM (cuadrática) | p | DM (absoluta) | p  | Clústeres |
|---|---:|---:|---:|---:|---:|---:|---:|
| N2 + Institución | 53 | +48,46 % | −1,01 | 0,3151 | −1,39 | 0,1697 | 53 |
| N3 + Área | 408 | +48,93 % | −1,98 | 0,0530 | −2,55 | 0,0137 | 53 |
| N4 + Región | 649 | +37,52 % | −2,01 | 0,0496 | −2,55 | 0,0137 | 53 |
| N5 + Carrera | 2.668 | +24,54 % | −2,13 | 0,0378 | −2,66 | 0,0103 | 53 |
| N6 + Condición | 4.633 | +25,59 % | −2,39 | 0,0205 | −3,76 | 0,0004 | 53 |
| N7 + Género | 8.094 | +22,82 % | −2,03 | 0,0470 | −3,98 | 0,0002 | 53 |
| N8 + Jornada | 8.729 | +26,71 % | −2,15 | 0,0363 | −4,33 | < 0,0001 | 53 |

**Modelo global frente a persistencia · Holdout 2026**

| Nivel | Skill | DM (cuadrática) | p | DM (absoluta) | p  |
|---|---:|---:|---:|---:|---:|
| N2 + Institución | +37,67 % | −0,67 | 0,5058 | −1,36 | 0,1791 |
| N3 + Área | +34,05 % | −1,35 | 0,1839 | −2,15 | 0,0363 |
| N4 + Región | +27,27 % | −1,25 | 0,2176 | −1,95 | 0,0566 |
| N5 + Carrera | +16,38 % | −1,31 | 0,1964 | −2,82 | 0,0067 |
| N6 + Condición | +21,38 % | −1,97 | 0,0543 | −4,60 | < 0,0001 |
| N7 + Género | +20,94 % | −2,06 | 0,0441 | −5,49 | < 0,0001 |
| N8 + Jornada | +24,52 % | −2,28 | 0,0269 | −5,96 | < 0,0001 |

Los demás métodos (RWD, ETS, ARIMA, Theta, Comb) están en `A2a_DM_cluster_por_nivel.csv`.

**(a′) Agregado al brief: CatBoost frente al modelo global** (d = L(CatBoost) − L(Global); DM > 0 favorece al global):

*Holdout 2026*

| Nivel | DM (cuadrática) | p | DM (absoluta) | p  |
|---|---:|---:|---:|---:|
| N2 + Institución | −0,32 | 0,7485 | +0,28 | 0,7787 |
| N3 + Área | −0,01 | 0,9903 | +0,92 | 0,3634 |
| N4 + Región | +0,77 | 0,4462 | +0,93 | 0,3544 |
| N5 + Carrera | +1,00 | 0,3225 | +2,48 | 0,0165 |
| N6 + Condición | +1,33 | 0,1882 | +3,46 | 0,0011 |
| N7 + Género | +1,67 | 0,1003 | +4,18 | 0,0001 |
| N8 + Jornada | +1,91 | 0,0621 | +4,77 | < 0,0001 |

*Validación v4 2026*

| Nivel | DM (cuadrática) | p | DM (absoluta) | p  |
|---|---:|---:|---:|---:|
| N2 + Institución | −1,05 | 0,2995 | −0,17 | 0,8672 |
| N3 + Área | −1,21 | 0,2314 | −1,15 | 0,2534 |
| N4 + Región | −0,55 | 0,5832 | −1,05 | 0,2985 |
| N5 + Carrera | −0,61 | 0,5417 | −0,32 | 0,7517 |
| N6 + Condición | −0,17 | 0,8641 | +1,21 | 0,2316 |
| N7 + Género | +0,19 | 0,8476 | +1,94 | 0,0577 |
| N8 + Jornada | −0,02 | 0,9832 | +2,30 | 0,0255 |

**(b) Comparación múltiple (MCB / Nemenyi).** Rangos medios por grupo según el error absoluto (1 = mejor; empates promediados) entre 8 métodos; CD = q·√(k(k+1)/(6N)), q = 3,0309 (rango estudentizado al 95 %, k = 8, dividido por √2). «Distinto del mejor» = la diferencia de rango supera CD. Supone grupos independientes, lo que no se cumple dentro de una institución: con N grande la CD es muy estrecha y la prueba es liberal.

*Holdout 2026 · N8 + Jornada (N = 9.069 grupos; CD = 0,1103)*

| Método | Rango medio | Diferencia con el mejor | Distinto del mejor |
|---|---:|---:|---:|
| Global | 3,9732 | 0,0000 | no |
| CatBoost | 4,1820 | 0,2088 | sí |
| Persistencia | 4,3320 | 0,3588 | sí |
| Comb | 4,5441 | 0,5708 | sí |
| Theta | 4,6554 | 0,6822 | sí |
| RWD | 4,6798 | 0,7066 | sí |
| ETS | 4,7416 | 0,7684 | sí |
| ARIMA | 4,8919 | 0,9187 | sí |

*Holdout 2026 · N2 + Institución (N = 53 grupos; CD = 1,4422)*

| Método | Rango medio | Diferencia con el mejor | Distinto del mejor |
|---|---:|---:|---:|
| CatBoost | 3,4717 | 0,0000 | no |
| Global | 3,5472 | 0,0755 | no |
| RWD | 4,2547 | 0,7830 | no |
| Theta | 4,4717 | 1,0000 | no |
| Persistencia | 4,7358 | 1,2642 | no |
| Comb | 4,7358 | 1,2642 | no |
| ETS | 5,2264 | 1,7547 | sí |
| ARIMA | 5,5566 | 2,0849 | sí |

*Validación v4 2026 · N8 + Jornada (N = 8.729 grupos; CD = 0,1124)*

| Método | Rango medio | Diferencia con el mejor | Distinto del mejor |
|---|---:|---:|---:|
| Global | 3,9817 | 0,0000 | no |
| CatBoost | 4,1002 | 0,1186 | sí |
| Persistencia | 4,3246 | 0,3429 | sí |
| Comb | 4,5516 | 0,5699 | sí |
| Theta | 4,6583 | 0,6766 | sí |
| RWD | 4,6867 | 0,7051 | sí |
| ETS | 4,7589 | 0,7772 | sí |
| ARIMA | 4,9380 | 0,9563 | sí |

Figuras: `A2_MCB_N8_holdout2026.png` y `A2_MCB_N2_holdout2026.png`. Los demás niveles y la validación v4 están en `A2b_MCB_Nemenyi.csv`.

**(c) N1 nacional: DM con la corrección de Harvey, Leybourne y Newbold (1997).** Serie OOF 2019-2026 (n = 8 años; 2026 = holdout), h = 1: DM* = DM·√((n−1)/n), comparado con t de 7 g.l. La potencia es muy baja.

| Método | Pérdida | d medio | DM | DM (HLN) | p (HLN) |
|---|---:|---:|---:|---:|---:|
| RWD | cuadratica | +97.487.888 | +0,7833 | +0,7328 | 0,4875 |
| RWD | absoluta | +2.087 | +0,5602 | +0,5241 | 0,6164 |
| ETS | cuadratica | −26.765.693 | −1,9124 | −1,7889 | 0,1168 |
| ETS | absoluta | −1.143 | −2,0312 | −1,9000 | 0,0992 |
| ARIMA | cuadratica | −129.643.254 | −2,8214 | −2,6392 | 0,0335 |
| ARIMA | absoluta | −3.793 | −2,5448 | −2,3804 | 0,0489 |
| Theta | cuadratica | −79.731.398 | −1,8239 | −1,7061 | 0,1318 |
| Theta | absoluta | −2.491 | −1,1633 | −1,0881 | 0,3126 |
| Comb | cuadratica | −90.732.024 | −3,4224 | −3,2013 | 0,0150 |
| Comb | absoluta | −2.623 | −2,4549 | −2,2964 | 0,0553 |
| Global | cuadratica | +435.639.145 | +1,4678 | +1,3730 | 0,2121 |
| Global | absoluta | +6.258 | +1,0106 | +0,9453 | 0,3760 |
| CatBoost | cuadratica | +316.952.590 | +1,4124 | +1,3212 | 0,2280 |
| CatBoost | absoluta | +6.270 | +1,0206 | +0,9547 | 0,3715 |

### A3 · Ablación P-04 (matrícula contemporánea)

**Método.** CatBoost con los `best_params` de la metadata (iterations 2000, learning_rate 0,0376, depth 7, l2_leaf_reg 1,7464, bagging_temperature 0,5465, border_count 183), semilla 42, sin Optuna, mismo TE dentro del fold y mismos orígenes (7 folds 2019-2025 + holdout 2026). (P) publicado, recalculado y verificado contra la tabla publicada (diferencia máxima 5,9 × 10⁻⁸ en arcsinh); (i) sin `densidad_estudiantes_m2`, `ratio_docente_estudiante` y `matriculas_sobre_pib` (46 variables); (ii) con las 49 variables y todas las exógenas tomadas en t−1 (24 columnas: `pib_mm_pesos`, `tasa_desempleo`, `N°Docentes`, `retencion_1er_anio`, `duracion_semestres`, `puntaje_maximo`, `puntaje_promedio`, `puntaje_minimo`, `puntaje_corte_primero`, `puntaje_corte_promedio`, `puntaje_corte_ultimo`, `valor_matricula`, `valor_arancel`, `pct_doctores`, `pct_magister`, `pct_especialistas`, `pct_sin_posgrado`, `pct_horas_jornada_completa`, `densidad_estudiantes_m2`, `matriculas_sobre_pib`, `ratio_docente_estudiante`, `densidad_competitiva`, `arancel_relativo_regional`, `selectividad_relativa`). Rezago de cada exógena: el valor de la misma celda en t−1; si no estaba, la media en t−1 de (institución, carrera, región), luego (institución, región), (institución) y (región). Origen del rezago en las filas 2019-2026: celda 91,18 %; inst_carrera_region 5,62 %; inst_region 3,09 %; region 0,08 %; inst 0,02 %. Las filas de 2018 quedan sin dato (sólo entrenan).

**RMSE de CV en arcsinh (media de los 7 folds):** (i) sin contemporáneas: 0,2964; (ii) exógenas en t-1: 0,2963; Publicado (recalculado): 0,2949.

#### A3 · Holdout 2026

| Nivel | Variante | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|
| N1 Nacional | Persistencia | 2,60 % | +0,00 % | 1,0000 | 100,00 % | −2,60 % |
| N2 + Institución | Persistencia | 3,49 % | +0,00 % | 1,0000 | 92,45 % | −2,60 % |
| N3 + Área | Persistencia | 4,89 % | +0,00 % | 1,0000 | 77,48 % | −2,60 % |
| N4 + Región | Persistencia | 5,15 % | +0,00 % | 1,0000 | 74,34 % | −2,60 % |
| N5 + Carrera | Persistencia | 8,63 % | +0,00 % | 1,0000 | 56,33 % | −2,60 % |
| N6 + Condición | Persistencia | 10,65 % | +0,00 % | 1,0000 | 48,06 % | −2,60 % |
| N7 + Género | Persistencia | 12,13 % | +0,00 % | 1,0000 | 41,81 % | −2,60 % |
| N8 + Jornada | Persistencia | 12,91 % | +0,00 % | 1,0000 | 40,56 % | −2,60 % |
| N1 Nacional | Publicado | 0,92 % | +87,55 % | 0,3529 | 100,00 % | +0,92 % |
| N2 + Institución | Publicado | 2,60 % | +43,03 % | 0,7460 | 90,57 % | +0,92 % |
| N3 + Área | Publicado | 4,30 % | +34,20 % | 0,8795 | 80,87 % | +0,92 % |
| N4 + Región | Publicado | 4,68 % | +16,90 % | 0,9090 | 76,20 % | +0,92 % |
| N5 + Carrera | Publicado | 8,24 % | +8,60 % | 0,9545 | 57,36 % | +0,92 % |
| N6 + Condición | Publicado | 10,05 % | +11,25 % | 0,9436 | 49,33 % | +0,92 % |
| N7 + Género | Publicado | 11,53 % | +5,09 % | 0,9508 | 42,62 % | +0,92 % |
| N8 + Jornada | Publicado | 12,09 % | +14,20 % | 0,9363 | 41,59 % | +0,92 % |
| N1 Nacional | (i) | 0,80 % | +90,58 % | 0,3069 | 100,00 % | +0,80 % |
| N2 + Institución | (i) | 2,58 % | +45,29 % | 0,7382 | 86,79 % | +0,80 % |
| N3 + Área | (i) | 4,34 % | +33,68 % | 0,8871 | 80,39 % | +0,80 % |
| N4 + Región | (i) | 4,75 % | +15,57 % | 0,9216 | 75,58 % | +0,80 % |
| N5 + Carrera | (i) | 8,28 % | +10,42 % | 0,9592 | 57,50 % | +0,80 % |
| N6 + Condición | (i) | 10,04 % | +13,36 % | 0,9435 | 49,21 % | +0,80 % |
| N7 + Género | (i) | 11,51 % | +6,73 % | 0,9487 | 42,99 % | +0,80 % |
| N8 + Jornada | (i) | 12,09 % | +15,74 % | 0,9364 | 41,69 % | +0,80 % |
| N1 Nacional | (ii) | 0,86 % | +89,02 % | 0,3314 | 100,00 % | +0,86 % |
| N2 + Institución | (ii) | 2,69 % | +49,85 % | 0,7701 | 88,68 % | +0,86 % |
| N3 + Área | (ii) | 4,20 % | +36,38 % | 0,8591 | 78,45 % | +0,86 % |
| N4 + Región | (ii) | 4,65 % | +18,71 % | 0,9027 | 73,72 % | +0,86 % |
| N5 + Carrera | (ii) | 8,26 % | +15,74 % | 0,9567 | 57,47 % | +0,86 % |
| N6 + Condición | (ii) | 10,14 % | +14,48 % | 0,9526 | 49,06 % | +0,86 % |
| N7 + Género | (ii) | 11,60 % | +10,41 % | 0,9563 | 42,77 % | +0,86 % |
| N8 + Jornada | (ii) | 12,15 % | +18,87 % | 0,9413 | 41,45 % | +0,86 % |

#### A3 · OOF 2019-2025

| Nivel | Variante | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|
| N1 Nacional | Persistencia | 1,83 % | +0,00 % | 1,0000 | 100,00 % | −0,15 % |
| N2 + Institución | Persistencia | 4,54 % | +0,00 % | 1,0000 | 80,30 % | −0,15 % |
| N3 + Área | Persistencia | 6,31 % | +0,00 % | 1,0000 | 68,79 % | −0,15 % |
| N4 + Región | Persistencia | 6,85 % | +0,00 % | 1,0000 | 59,04 % | −0,15 % |
| N5 + Carrera | Persistencia | 10,34 % | +0,00 % | 1,0000 | 48,27 % | −0,15 % |
| N6 + Condición | Persistencia | 12,75 % | +0,00 % | 1,0000 | 42,07 % | −0,15 % |
| N7 + Género | Persistencia | 14,18 % | +0,00 % | 1,0000 | 37,81 % | −0,15 % |
| N8 + Jornada | Persistencia | 14,90 % | +0,00 % | 1,0000 | 36,49 % | −0,15 % |
| N1 Nacional | Publicado | 3,17 % | −186,69 % | 1,7276 | 100,00 % | +2,64 % |
| N2 + Institución | Publicado | 4,71 % | +17,15 % | 1,0370 | 78,55 % | +2,64 % |
| N3 + Área | Publicado | 6,17 % | +11,91 % | 0,9779 | 68,82 % | +2,64 % |
| N4 + Región | Publicado | 6,72 % | −12,38 % | 0,9812 | 60,63 % | +2,64 % |
| N5 + Carrera | Publicado | 9,93 % | −2,08 % | 0,9610 | 48,80 % | +2,64 % |
| N6 + Condición | Publicado | 12,42 % | −3,76 % | 0,9738 | 41,93 % | +2,64 % |
| N7 + Género | Publicado | 13,80 % | −2,90 % | 0,9732 | 37,51 % | +2,64 % |
| N8 + Jornada | Publicado | 14,45 % | −2,73 % | 0,9696 | 36,27 % | +2,64 % |
| N1 Nacional | (i) | 3,32 % | −218,13 % | 1,8108 | 100,00 % | +2,66 % |
| N2 + Institución | (i) | 4,79 % | +14,06 % | 1,0548 | 77,81 % | +2,66 % |
| N3 + Área | (i) | 6,27 % | +8,49 % | 0,9932 | 69,53 % | +2,66 % |
| N4 + Región | (i) | 6,81 % | −15,12 % | 0,9945 | 60,33 % | +2,66 % |
| N5 + Carrera | (i) | 10,01 % | −4,56 % | 0,9684 | 48,56 % | +2,66 % |
| N6 + Condición | (i) | 12,51 % | −6,09 % | 0,9811 | 41,81 % | +2,66 % |
| N7 + Género | (i) | 13,89 % | −5,65 % | 0,9795 | 37,49 % | +2,66 % |
| N8 + Jornada | (i) | 14,54 % | −5,28 % | 0,9756 | 36,24 % | +2,66 % |
| N1 Nacional | (ii) | 2,61 % | −92,34 % | 1,4214 | 100,00 % | +2,29 % |
| N2 + Institución | (ii) | 4,35 % | +29,52 % | 0,9573 | 83,04 % | +2,29 % |
| N3 + Área | (ii) | 5,98 % | +15,39 % | 0,9482 | 70,97 % | +2,29 % |
| N4 + Región | (ii) | 6,49 % | −8,76 % | 0,9477 | 61,67 % | +2,29 % |
| N5 + Carrera | (ii) | 9,85 % | −4,98 % | 0,9533 | 48,90 % | +2,29 % |
| N6 + Condición | (ii) | 12,29 % | −5,33 % | 0,9639 | 41,99 % | +2,29 % |
| N7 + Género | (ii) | 13,70 % | −6,20 % | 0,9661 | 37,78 % | +2,29 % |
| N8 + Jornada | (ii) | 14,36 % | −6,90 % | 0,9632 | 36,47 % | +2,29 % |

#### A3 · OOF 2019-2025 sin duplicados

| Nivel | Variante | WAPE | Skill | RelMAE | ± 10 % | Error agregado |
|---|---:|---:|---:|---:|---:|---:|
| N1 Nacional | Persistencia | 1,82 % | +0,00 % | 1,0000 | 100,00 % | −0,16 % |
| N2 + Institución | Persistencia | 4,54 % | +0,00 % | 1,0000 | 80,30 % | −0,16 % |
| N8 + Jornada | Persistencia | 14,89 % | +0,00 % | 1,0000 | 36,49 % | −0,16 % |
| N1 Nacional | Publicado | 3,17 % | −188,68 % | 1,7386 | 100,00 % | +2,65 % |
| N2 + Institución | Publicado | 4,71 % | +17,03 % | 1,0366 | 78,55 % | +2,65 % |
| N8 + Jornada | Publicado | 14,45 % | −2,96 % | 0,9700 | 36,27 % | +2,65 % |
| N1 Nacional | (i) | 3,32 % | −219,90 % | 1,8223 | 100,00 % | +2,67 % |
| N2 + Institución | (i) | 4,79 % | +14,03 % | 1,0531 | 77,81 % | +2,67 % |
| N8 + Jornada | (i) | 14,54 % | −5,49 % | 0,9760 | 36,24 % | +2,67 % |
| N1 Nacional | (ii) | 2,60 % | −93,01 % | 1,4278 | 100,00 % | +2,29 % |
| N2 + Institución | (ii) | 4,34 % | +29,53 % | 0,9557 | 83,04 % | +2,29 % |
| N8 + Jornada | (ii) | 14,35 % | −7,19 % | 0,9636 | 36,47 % | +2,29 % |

**¿Empeora el holdout de forma material?** No. En la celda, el WAPE pasa de 12,0881 % a 12,0902 % en (i) (+0,0021 puntos) y a 12,1525 % en (ii) (+0,0644 puntos), ambos por debajo del umbral de 0,3 puntos.

**Pronóstico 2027 informativo, NO congelado** (refit con 2018-2026 y las filas 2026 clonadas, como en el notebook; en (ii) las exógenas de 2027 son las observadas en 2026). La réplica del publicado da 761.053 frente a 761.058 congelado: la reconstrucción usa el rezago redondeado y difiere en el redondeo.

| Variante | Total 2027 | Rótulo |
|---|---:|---:|
| Publicado (recalculado) | 761.053 | NO CONGELADA · sólo informativa |
| (i) sin contemporáneas | 760.880 | NO CONGELADA · sólo informativa |
| (ii) exógenas en t-1 | 755.071 | NO CONGELADA · sólo informativa |

### A4 · Interval score de las bandas al 90 % (holdout 2026)

**Método.** IS_α(l, u; y) = (u − l) + (2/α)(l − y)·1{y < l} + (2/α)(y − u)·1{y > u}, α = 0,10 (Gneiting y Raftery, 2007); MSIS = IS medio / MAE de la persistencia en los mismos grupos. Bandas: (P) publicadas, conformal estratificado por tamaño, calibrado con el OOF 2019-2025 con el código de v4 sin cambios; (r1) conformal sin estratos (un solo par de cuantiles: en la celda, sobre todos los residuos OOF; en cada nivel, sobre todos sus grupos); (r2) AutoETS al 90 % (en la celda, los de A1; en N2-N7, un AutoETS por nodo sobre la historia agregada del nodo). Se comparan sólo los grupos con las tres bandas; los excluidos son nodos con menos de 3 años de historia contigua para ETS.

| Nivel | Banda | Grupos comunes / total | Cobertura | Ancho mediano | IS medio | MSIS |
|---|---:|---:|---:|---:|---:|---:|
| N2 + Institución | Publicadas (conformal estratificado) | 53 / 53 | 94,34 % | 2.143,8 | 3.009,7 | 6,1713 |
| N2 + Institución | r1 · conformal sin estratos | 53 / 53 | 96,23 % | 3.885,8 | 5.296,9 | 10,8609 |
| N2 + Institución | r2 · AutoETS 90 % | 53 / 53 | 94,34 % | 2.244,1 | 3.587,8 | 7,3565 |
| N3 + Área | Publicadas (conformal estratificado) | 404 / 413 | 94,31 % | 301,2 | 516,8 | 5,8264 |
| N3 + Área | r1 · conformal sin estratos | 404 / 413 | 95,79 % | 463,7 | 809,2 | 9,1232 |
| N3 + Área | r2 · AutoETS 90 % | 404 / 413 | 91,09 % | 320,7 | 693,7 | 7,8210 |
| N4 + Región | Publicadas (conformal estratificado) | 630 / 647 | 93,97 % | 203,0 | 363,8 | 6,0889 |
| N4 + Región | r1 · conformal sin estratos | 630 / 647 | 96,35 % | 400,3 | 729,9 | 12,2181 |
| N4 + Región | r2 · AutoETS 90 % | 630 / 647 | 90,32 % | 230,9 | 494,7 | 8,2801 |
| N5 + Carrera | Publicadas (conformal estratificado) | 2.388 / 2.739 | 93,80 % | 100,4 | 159,9 | 6,9452 |
| N5 + Carrera | r1 · conformal sin estratos | 2.388 / 2.739 | 95,14 % | 166,1 | 257,3 | 11,1747 |
| N5 + Carrera | r2 · AutoETS 90 % | 2.388 / 2.739 | 89,74 % | 92,4 | 174,9 | 7,5936 |
| N6 + Condición | Publicadas (conformal estratificado) | 4.036 / 4.798 | 94,77 % | 77,9 | 119,2 | 7,2726 |
| N6 + Condición | r1 · conformal sin estratos | 4.036 / 4.798 | 95,91 % | 92,9 | 178,3 | 10,8773 |
| N6 + Condición | r2 · AutoETS 90 % | 4.036 / 4.798 | 88,88 % | 58,9 | 123,0 | 7,5039 |
| N7 + Género | Publicadas (conformal estratificado) | 6.839 / 8.390 | 94,82 % | 52,9 | 76,9 | 7,0523 |
| N7 + Género | r1 · conformal sin estratos | 6.839 / 8.390 | 95,42 % | 53,4 | 105,5 | 9,6820 |
| N7 + Género | r2 · AutoETS 90 % | 6.839 / 8.390 | 86,85 % | 36,2 | 77,9 | 7,1441 |
| N8 + Jornada | Publicadas (conformal estratificado) | 7.943 / 9.069 | 93,71 % | 37,7 | 64,2 | 6,0844 |
| N8 + Jornada | r1 · conformal sin estratos | 7.943 / 9.069 | 95,00 % | 48,1 | 94,6 | 8,9585 |
| N8 + Jornada | r2 · AutoETS 90 % | 7.943 / 9.069 | 87,02 % | 34,4 | 70,8 | 6,7093 |

En la celda, sobre las 9.069 celdas, la cobertura de las bandas publicadas es 92,35 % (B-02); en el subconjunto común con ETS (7.943 celdas) es la de la tabla.

### A5 · Experimento limpio de target encoding

**Método.** Cuatro brazos con el mismo CatBoost (best_params, semilla 42) y los mismos 7 folds (validación 2019-2025): {estimador m, ponderación sigmoide} × {con fuga, dentro del fold}. Estimador m: enc = (n·media + m·prior)/(n + m), m = 30, prior = media del target de ajuste (la fórmula de las `te_*`). Sigmoide: category_encoders 2.8.1 `TargetEncoder(smoothing=30, min_samples_leaf=20)` (el del modelo publicado). «Con fuga» = el codificador se ajusta una vez sobre todo el panel 2018-2026; «dentro del fold» = sólo con las filas de entrenamiento de cada fold. Sólo origen 2026 (corrida 2027): la Tabla 9 trae también el origen 2025 (v4), que no se repitió.

| Codificador | RMSE CV con fuga | RMSE CV dentro del fold | Diferencia | Diferencia relativa |
|---|---:|---:|---:|---:|
| m | 0,2852 | 0,2938 | −0,0086 | −2,92 % |
| sigmoide | 0,2838 | 0,2949 | −0,0110 | −3,74 % |
| publicado: m con fuga vs sigmoide dentro del fold | 0,2852 | 0,2949 | −0,0096 | −3,26 % |

Controles: el brazo sigmoide dentro del fold reproduce el RMSE de CV publicado (0,2949); el brazo m con fuga, el precalculado (0,2853 publicado). Las `te_*` del dataset no coinciden con el estimador m recalculado (diferencia máxima 0,0828; ver el punto 5 del inicio). El RMSE por fold está en `A5_te_rmse_por_fold.csv`.

### A6 · Reconciliación jerárquica (holdout 2026, N1-N5)

**Desvío del brief:** la jerarquía se trunca en N5. Los nodos inferiores son los agregados del CatBoost en N5 (la suma de sus celdas N8, es decir, el pronóstico publicado). Con las ~25.000 series de N1-N8, la matriz de covarianza densa de MinT no cabe en memoria; con N1-N5 son 3.853 nodos y 2.739 inferiores. Como se evalúa N1-N5, no cambia qué se evalúa. hierarchicalforecast 1.5.3.

**Pronósticos base:** N5 = CatBoost agregado; N1-N4 = un AutoETS por nodo sobre la historia agregada del nodo (último valor = suma de los rezagos 2026). **Covarianza de MinT-shrink:** residuos de un paso de los años OOF 2019-2025 (CatBoost OOF agregado en N5; AutoETS de origen móvil en N1-N4), con NaN donde el nodo no existía.

| Método | Nivel | WAPE | Skill | RelMAE | ± 10 % |
|---|---:|---:|---:|---:|---:|
| Base (ETS en N1-N4, CatBoost en N5) | N1 Nacional | 2,69 % | −7,56 % | 1,0371 | 100,00 % |
| Base (ETS en N1-N4, CatBoost en N5) | N2 + Institución | 4,01 % | −17,38 % | 1,1495 | 86,79 % |
| Base (ETS en N1-N4, CatBoost en N5) | N3 + Área | 5,75 % | −21,45 % | 1,1755 | 71,91 % |
| Base (ETS en N1-N4, CatBoost en N5) | N4 + Región | 6,41 % | −51,06 % | 1,2439 | 66,15 % |
| Base (ETS en N1-N4, CatBoost en N5) | N5 + Carrera | 8,24 % | +8,60 % | 0,9545 | 57,36 % |
| BottomUp (publicado) | N1 Nacional | 0,92 % | +87,55 % | 0,3529 | 100,00 % |
| BottomUp (publicado) | N2 + Institución | 2,60 % | +43,03 % | 0,7460 | 90,57 % |
| BottomUp (publicado) | N3 + Área | 4,30 % | +34,20 % | 0,8795 | 80,87 % |
| BottomUp (publicado) | N4 + Región | 4,68 % | +16,90 % | 0,9090 | 76,20 % |
| BottomUp (publicado) | N5 + Carrera | 8,24 % | +8,60 % | 0,9545 | 57,36 % |
| OLS | N1 Nacional | 2,69 % | −7,63 % | 1,0374 | 100,00 % |
| OLS | N2 + Institución | 3,89 % | −11,29 % | 1,1135 | 90,57 % |
| OLS | N3 + Área | 5,64 % | −19,47 % | 1,1537 | 69,98 % |
| OLS | N4 + Región | 6,07 % | −29,01 % | 1,1784 | 65,38 % |
| OLS | N5 + Carrera | 9,74 % | +1,69 % | 1,1285 | 49,95 % |
| WLS estructural | N1 Nacional | 2,00 % | +40,54 % | 0,7711 | 100,00 % |
| WLS estructural | N2 + Institución | 3,20 % | +26,76 % | 0,9171 | 94,34 % |
| WLS estructural | N3 + Área | 4,79 % | +15,32 % | 0,9790 | 74,09 % |
| WLS estructural | N4 + Región | 5,15 % | +14,11 % | 1,0004 | 71,41 % |
| WLS estructural | N5 + Carrera | 9,00 % | +9,40 % | 1,0424 | 52,43 % |
| MinT-shrink | N1 Nacional | 2,65 % | −3,91 % | 1,0194 | 100,00 % |
| MinT-shrink | N2 + Institución | 3,41 % | +26,96 % | 0,9773 | 92,45 % |
| MinT-shrink | N3 + Área | 5,16 % | +3,49 % | 1,0539 | 75,30 % |
| MinT-shrink | N4 + Región | 5,66 % | −1,47 % | 1,0989 | 71,41 % |
| MinT-shrink | N5 + Carrera | 10,84 % | −39,43 % | 1,2559 | 49,03 % |

**¿Mejora MinT la frontera N4/N5?** No: el *bottom-up* publicado es el mejor en todos los niveles N1-N5, y MinT-shrink empeora N4 y N5. Salvedad: los ETS base de N1-N4 son débiles (peores que la persistencia), porque la composición de cada nodo cambia entre años; la reconciliación arrastra esa debilidad.

### Versiones, tiempos y desvíos

**Versiones:** python 3.13.9; sistema Windows-11-10.0.26300-SP0; numpy 2.3.5; pandas 2.3.3; scipy 1.16.3; sklearn 1.7.2; catboost 1.2.10; lightgbm 4.6.0; category_encoders 2.8.1; statsmodels 0.14.5; statsforecast 2.1.1; hierarchicalforecast 1.5.3; matplotlib 3.10.6. statsforecast y hierarchicalforecast se instalaron en un entorno aparte, sin modificar el entorno de la corrida 2027.

**Tiempos totales:** A1 694 s; A3 265 s; A4 47 s; A5 248 s; A6 28 s; A2 < 1 min.

**Desvíos del brief:**

- A1: en 2019 ninguna serie llega a 3 observaciones; todos los métodos por serie son la persistencia ese año.
- A1: el modelo global no incluye el nivel rezagado (log de la matrícula t−1), porque el brief pide sólo rezagos de la tasa; las predicciones se reconstruyen con el rezago publicado.
- A2: se agregó la comparación directa CatBoost frente a modelo global (a′), no pedida.
- A2 (b): la prueba de Nemenyi supone grupos independientes; con miles de grupos la CD es muy estrecha y la prueba es liberal.
- A3: el pronóstico 2027 informativo de la variante publicada da 761.053 (no 761.058) por el redondeo del rezago en la réplica; no se regeneró nada congelado.
- A4: la cobertura y la IS se calculan sobre los grupos con las tres bandas (ETS exige 3 años de historia del nodo).
- A5: sólo el origen 2026 (corrida 2027); el origen 2025 de la Tabla 9 (v4) no se repitió.
- A6: jerarquía truncada en N5 (ver la sección); base ETS en N1-N4.
- General: el «real» del holdout es el winsorizado del panel (p1/p99 de la tasa), igual que en el paper.



**Integridad:** las huellas SHA-256 de los 8 artefactos de `forecast_2027/SHA256SUMS.txt` se verificaron antes y después de los análisis: coinciden. No se modificó nada de lo que se congela.

---

## H · Respuesta de Claude Code a Claude Science sobre los análisis Q1 (19-11-2026)

Ejecuté los análisis A1-A6 del brief en una rama aparte del repositorio privado (`analisis-q1`), con salidas separadas. El informe completo es la **sección G**: método, parámetros, n, tablas, tiempos, versiones y desvíos. Los CSV, con coma decimal, y las figuras están en `resultados_q1/` del repositorio privado.

**Integridad.** Verifiqué las huellas SHA-256 de los 8 artefactos de `forecast_2027/SHA256SUMS.txt` antes y después: coinciden. No modifiqué nada de lo que se congela, ni el README, ni el paper v4, ni los manuscritos. La sección G está en el commit local `49f58ab`, sin push; ese commit incluye también la sección F, que estaba sin commitear.

**Controles.** Al reentrenar el CatBoost se reproduce el holdout 2026 publicado (diferencia máxima de 3 × 10⁻⁸ en arcsinh). La persistencia y el CatBoost reproducen las cascadas publicadas: en el holdout N8, 12,91 % y 12,09 %; en la validación v4 N8, 11,49 % con *skill* +26,71 %.

### H.1 · Lo que contradice o matiza el manuscrito

1. **Un modelo global simple, sin exógenas, le gana al CatBoost en la celda.** Es un LightGBM con rezagos t−1 a t−3 de arcsinh(tasa), año relativo e identificadores categóricos, ajustado con una rejilla fija de 12 combinaciones, sin Optuna.
   - WAPE en N8, global frente a CatBoost: holdout 2026, **11,42 % frente a 12,09 %** (*skill* +24,52 % frente a +14,20 %); OOF 2019-2025, 14,01 % frente a 14,45 %; validación v4 2026, 11,16 % frente a 11,49 %.
   - RMSE de CV: 0,2869 frente a 0,2949.
   - En el holdout, la diferencia es significativa con pérdida absoluta en N5-N8 (N8: DM = +4,77, p < 0,0001). Con pérdida cuadrática no lo es (N8: p = 0,062). En N2-N4 no se distinguen.
   - **El aporte de las exógenas y del CatBoost no se sostiene en la celda**: lo que funciona es el diseño global con rezagos.
2. **En el holdout 2026, la ventaja del CatBoost sobre la persistencia no es significativa con pérdida cuadrática en ningún nivel** (N8: p = 0,101; N2: p = 0,395). La prueba es un DM entre grupos con errores estándar robustos por clúster de institución (53 clústeres).
   - Con pérdida absoluta sí es significativa en N6-N8 (N8: p = 0,005).
   - En la validación v4 2026 es significativa en N3-N8. Con pérdida cuadrática, p ≤ 0,05 en N4-N8 y 0,053 en N3; con absoluta, p ≤ 0,014.
3. **En la celda, los referentes clásicos por serie (deriva, AutoETS, AutoARIMA, Theta y su combinación) son peores que la persistencia en los tres conjuntos.** En los agregados altos no:
   - en N1 del OOF, ETS, ARIMA, Theta y Comb superan al CatBoost (ARIMA, WAPE 1,32 %; CatBoost, 3,17 %);
   - en N2 del holdout, la deriva iguala al CatBoost en *skill*.
4. **El «real» del holdout 2026 está winsorizado.** El panel recorta la tasa a sus percentiles 1 y 99 antes de reconstruir las matrículas. Afecta a 90 celdas; en las 8.329 celdas comunes con v4 suma 718.597, frente a 718.916 del SIES. Todos los análisis usan ese real. Hay que declararlo en §3 o §4.
5. **Las `te_*` precalculadas no se reproducen exactamente** con el estimador m sobre los datos vigentes (correlación 0,985-0,995). Su RMSE de CV sí se reproduce (0,2852 frente a 0,2853).

### H.2 · Resultados por brecha

- **A3, ablación P-04: sin optimismo material.**
  - WAPE del holdout N8: 12,088 % el publicado, 12,090 % sin las tres contemporáneas y 12,153 % con todas las exógenas en t−1 (+0,06 puntos, bajo el umbral de 0,3).
  - RMSE de CV: 0,2949, 0,2964 y 0,2963.
  - Pronóstico 2027 informativo, NO congelado: 760.880 y 755.071. La réplica del publicado da 761.053, por redondeo.
- **A4, *interval score*:** las bandas publicadas tienen la mejor IS y MSIS en N2-N8. MSIS en la celda: 6,08 las publicadas, 8,96 el conformal sin estratos y 6,71 AutoETS. ETS cubre poco (87-91 %). La estratificación por tamaño es lo que más aporta.
- **A5, *target encoding* limpio:** la fuga aislada vale **−2,92 % con el estimador m y −3,74 % con la sigmoide**. El −3,26 % publicado, que mezcla fórmulas, queda entre ambos. Sólo se corrió el origen 2026; el 2025 de la Tabla 9 no se repitió.
- **A6, reconciliación** (truncada en N5 por memoria, evaluada en N1-N5): el *bottom-up* publicado es el mejor en todos los niveles; MinT-shrink empeora N4 y N5. La base ETS de N1-N4 es débil, porque la composición de los nodos cambia entre años.
- **A2(b), MCB / Nemenyi en N8 del holdout:** el modelo global queda primero, y el CatBoost queda significativamente detrás de él y por delante de los demás. La prueba supone grupos independientes; con N grande es liberal.
- **A2(c), N1 con corrección HLN (n = 8):** potencia baja. Sólo ARIMA y Comb difieren de la persistencia con p < 0,05 en pérdida cuadrática.

### H.3 · Implicaciones para el manuscrito (las decide el autor; no edité nada)

- Reformular la contribución del modelo: «un modelo global supera a la persistencia y a los métodos por serie en la celda», no «el CatBoost con exógenas». El CatBoost publicado queda como el modelo congelado por continuidad, con el global como referente más fuerte. El pronóstico 2027 congelado no cambia.
- Reportar el valor *p* junto a cada *skill* de las Tablas 6 y 10. En el holdout, el *skill* cuadrático no es significativo.
- Cerrar la limitación P-04 con la cifra medida (+0,06 puntos).
- Reemplazar la Tabla 9 por la versión limpia de A5.
- Declarar la winsorización del real del holdout.

### H.4 · Pedidos a Claude Science

1. Revisar la sección G y señalar inconsistencias con el manuscrito, sobre todo en §4.7, §4.8, §5.6, §6.5 y las conclusiones.
2. Proponer una redacción en español y en inglés que incorpore el modelo global como referente y reformule la contribución, sin tocar el pronóstico congelado.
3. Siguen pendientes las decisiones de B-01 de la sección F.3: el push, la corrección de los rótulos de la metadata y el protocolo de evaluación 2027.
