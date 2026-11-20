# Checklist de cumplimiento IJF y brechas para nivel Q1

*Manuscrito:* «Cuando el pronóstico ingenuo es el rezago: evaluación del pronóstico de matrícula universitaria a nivel de programa en Chile» (versión en español, reescritura v3 con delta v4, `manuscrito_IJF_es.md` / `.docx`). *Revista:* International Journal of Forecasting (IJF). *Fecha:* 20-nov-2026.

Estados: **Cumple** · **Resuelto** (análisis ejecutado por el autor e incorporado) · **Pendiente autor** · **Brecha de análisis** (marcada en el texto como `[BRECHA Q1: …]`). Las fuentes de los requisitos son las del *Informe de validación de referencias, fuentes de datos y requisitos IJF* (§4.2).

## 1. Requisitos formales de la revista

| # | Requisito IJF | Estado | Dónde se resuelve | Fuente del requisito |
|---:|---|---|---|---|
| 1 | Ajuste al alcance: aporte nuevo a la ciencia o práctica del pronóstico | Cumple: contribuciones de evaluación respaldadas ahora por comparación con referentes por serie, modelo global, diseño factorial, pruebas DM y contraste prospectivo preespecificado | Título, Resumen, §1, §5.5–5.6, §6.3–6.4 | IJF Guide for Authors (2020) |
| 2 | Resumen de 100–150 palabras, sin referencias, jerga ni notación | Cumple (146 palabras, texto literal de la especificación) | Resumen | Guide for Authors (ScienceDirect) |
| 3 | Al menos 5 palabras clave sin repetir el título | Cumple (7). Pendiente autor: contrastar con la lista del IIF | Palabras clave | Guide for Authors; forecasters.org/ijf/keywords |
| 4 | Highlights: 3–5 viñetas de ≤85 caracteres | Cumple (5; 81–83 caracteres, verificado por código) | `highlights_es.md` | Checklist IJF; norma Elsevier |
| 5 | Revisión doble anónima | Cumple en el texto: sin nombre, repositorio, tablero, etiqueta, commit, huellas ni DOI del congelamiento (identificadores omitidos y entregados al editor en la carta de presentación EN; verificado por código). Pendiente autor: limpiar propiedades del `.docx` | Manuscrito, apéndice, title page | Guide for Authors (elsevier.com) |
| 6 | Title page separada | Pendiente autor (afiliación, correo, dirección, ORCID) | `title_page_es.md` | Guide for Authors |
| 7 | Idioma inglés | Pendiente (fase de traducción) | Versión EN | IJF Guide (2020) |
| 8 | Estilo autor-año, DOI y *data references* | Cumple: 94 claves citadas, 94 entradas en `references.bib` (cinco nuevas verificadas en CrossRef: Koning et al. 2005, Hyndman & Khandakar 2008, Hyndman et al. 2002, Assimakopoulos & Nikolopoulos 2000, Cameron & Miller 2015). Pendiente autor: entrada del *Informe de Matrícula 2026* del SIES; cita verificada de Nemenyi (sin DOI verificable en CrossRef) | Referencias | Guide for Authors |
| 9 | Declaración CRediT | Cumple | Title page | Guide for Authors |
| 10 | Conflicto de intereses | Cumple; pendiente formulario Elsevier | Manuscrito; title page | IJF Guide |
| 11 | Declaración de IA generativa | Pendiente autor (borrador neutral) | Antes de Referencias | Guide for Authors |
| 12 | Financiamiento | Pendiente autor (confirmar) | Manuscrito; title page | Guide for Authors |
| 13 | Datos y código (julio 2023) | Pendiente autor: declaración anónima redactada; los pronósticos 2027 del 2×2 y de los referentes, el protocolo, el programa de evaluación y sus huellas se publicaron con el congelamiento del 20-11-2026; DOI de Zenodo pendiente; panel y código con DOI al aceptar | Disponibilidad de datos | forecasters.org/ijf |
| 14 | Material suplementario | Cumple: apéndice A.1–A.24 con 41 tablas y 9 figuras | Apéndice en línea | ScienceDirect |
| 15 | Figuras y tablas con leyenda y citadas | Cumple: 5 figuras y 13 tablas en el cuerpo; figuras ES de `figuras_es/` con coma decimal y rótulos en español; fig07 con deciles por rezago, fig07b y fig11b nuevas; leyendas SHAP declaran atribuciones dentro de la muestra; referencias cruzadas verificadas por código | §5; Apéndice | IJF submission checklist |
| 16 | Extensión | Sin límite explícito. Cuerpo: ~11.000 palabras de prosa | Manuscrito | Informe §4.2 |

## 2. Brechas de análisis

| # | Brecha | Estado | Dónde |
|---:|---|---|---|
| 2.1 | Referentes clásicos por serie (RWD, ETS, ARIMA, Theta, Comb) y modelo global simple | **Resuelto** | §4.7, §5.5, Tabla 8; Apéndice A.16 |
| 2.2 | Reconciliación jerárquica (*bottom-up* vs OLS, WLS, MinT) | **Resuelto**: la suma ascendente es la mejor en N1–N5 | §4.7, §6.5; Apéndice A.21 |
| 2.3 | Pruebas DM por clúster, HLN en N1 y MCB/Nemenyi | **Resuelto**: valores *p* junto a cada *skill* en las Tablas 4, 6 y 7 (OOF 2019–2026: ninguna diferencia significativa, menor *p* 0,0992; *holdout* 2025: significativa con pérdida absoluta en N5–N8); MCB por nivel con valor observado | §4.8, §5.2, §5.4–5.6, §6.4; Apéndice A.17 |
| 2.4 | Ablación P-04 | **Resuelto**: +0,06 puntos de WAPE en la celda del *holdout* (12,27 % → 12,33 %, variante ii) | §6.5; Apéndice A.18 |
| 2.5 | Intervalos 2027 (P-05) | **Resuelto** para los cuatro modelos (cobertura en el *holdout* 2026 de 92,25 % a 93,25 %) | §5.7, §5.10; Apéndices A.11 y A.23 |
| 2.6 | Congelamiento formal (P-01) | **Resuelto**: seis pronósticos congelados el 20-11-2026 con etiqueta anotada y huellas; protocolo v2.2 con criterio asimétrico de calibración. Pendiente autor: DOI de Zenodo | §5.10; Apéndice A.14 |
| 2.7 | Auditoría de peores celdas por origen del rezago | **Resuelto** | §4.2, §5.4; Apéndice A.4 |
| 2.8 | *Interval score* y MSIS | **Resuelto**; las bandas estratificadas tienen la menor IS salvo en N7, donde AutoETS es marginalmente menor (79,7 frente a 79,8) | §5.7, Tabla 11; Apéndice A.19 |
| 2.9 | *Target encoding* limpio | **Resuelto**: fuga aislada de 2,92 % (estimador *m*) a 3,74 % (sigmoide) | §5.8, Tabla 12; Apéndice A.20 |
| 2.10 | Diseño factorial algoritmo × variables y desglose por año | **Resuelto** (L-02: ventaja de las exógenas concentrada en años con poca historia y en 2022) | §5.6, §6.4, Tabla 9; Apéndice A.22 |
| 2.11 | Evaluación contra la matrícula observada | **Resuelto** (holdout y OOF reevaluados; validación 2026 sin cambios) | §3.3; Apéndice A.15 |

## 3. Pendientes del autor (sin análisis nuevo)

1. Entrada del *Informe de Matrícula 2026* del SIES en el .bib; cita verificada de la prueba de Nemenyi; búsqueda sistemática en Scopus/WoS/SciELO.
2. Confirmar la nota de las 113 filas duplicadas (B-04).
3. DOI de Zenodo del congelamiento y del depósito.
4. Title page (afiliación, correo, ORCID, financiamiento, agradecimientos), declaración de IA y formulario de intereses.
5. **Resuelto:** los rótulos heredados de los metadatos del modelo (número de *folds*, 5 en lugar de los 7 ejecutados, y rótulos del holdout y de los supuestos del pronóstico) se corrigieron antes del congelamiento, sin cambiar ningún valor numérico ni las predicciones (Apéndice A.13).

## 4. Riesgos de rechazo de escritorio y cómo mitigarlos

1. **Se lee como una aplicación.** Mitigado: la contribución se apoya ahora en comparaciones con referentes por serie y un modelo global, un diseño factorial con pruebas formales y un contraste prospectivo preespecificado; la carta debe abrir con el modo de falla «el pronóstico ingenuo es el rezago».
2. **El modelo principal no es el mejor en la celda.** El global solo de rezagos supera a C49 en 2026. Mitigación: el texto ya lo presenta como resultado y separa el aporte robusto (diseño global) del dependiente del período (exógenas); no reivindicar CatBoost.
3. **Política de datos y código.** Mitigación: acceso para el editor durante la revisión, publicación de los pronósticos 2027 con el congelamiento y depósito con DOI al aceptar; preparar el paquete de replicación antes de enviar.
4. **Anonimato comprometido por el repositorio público.** Mitigación: sin enlaces ni nombres de etiqueta en el manuscrito; considerar retitular el README durante la revisión e informarlo al editor.
5. **Un solo año de prueba reciente y ventaja no significativa en el OOF completo.** Mitigación: ambos se declaran sin suavizar (§5.2, §6.4); el congelamiento del 20-11-2026 convierte 2027 en una prueba prospectiva con hipótesis y criterios fijados de antemano.
6. **Extensión.** ~10.700 palabras y 13 tablas en el cuerpo. Mitigación: en la versión en inglés, considerar pasar la Tabla 12 y parte de la Tabla 10 al apéndice.
7. **Figuras.** Mitigación: regenerarlas en inglés con nombres de archivo por orden de aparición para el envío.
8. **Idioma.** Mitigación: traducción a partir de esta versión.

## 5. Lista priorizada antes de enviar

1. Crear el depósito en Zenodo desde la etiqueta del congelamiento e insertar el DOI en la carta de presentación (no en el manuscrito anónimo).
2. Completar la title page, la declaración de IA y las entradas bibliográficas pendientes.
3. Confirmar la nota B-04 y limpiar las propiedades de los `.docx`.

## 6. Recuento de marcadores (tras el delta v4)

| Archivo | [BRECHA Q1] | [PENDIENTE] |
|---|---:|---:|
| manuscrito_IJF_es.md | 0 | 8 |
| apendice_en_linea_es.md | 0 | 2 |
| title_page_es.md | 0 | 9 |
