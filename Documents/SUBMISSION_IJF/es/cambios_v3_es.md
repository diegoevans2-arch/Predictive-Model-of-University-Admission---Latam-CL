# Cambios de la reescritura v3 del manuscrito IJF en español (20-11-2026)

Fuentes de cifras: secciones G y J (análisis Q1 y reevaluación con la matrícula observada) y secciones M y N (L-01, L-02 y L-03) de OBSERVACIONES_Y_MEJORAS.md; decisiones de las secciones I y L; protocolo de evaluación 2027, versión 2. Regla aplicada: *holdout* 2026 y OOF siempre con la matrícula observada (J.1/J.3/M); validación del origen 2025 contra el dato oficial sin cambios (G/A1); las cifras que sólo existen con el valor recortado se conservan rotuladas «real winsorizado» con [PENDIENTE].

## Por sección

- **Resumen:** texto literal de la especificación (146 palabras).
- **Highlights:** rehechos (5 viñetas, 81–83 caracteres): naïve = rezago; global > persistencia y métodos por serie en la celda; exógenas dependientes del período; conformal estratificado con menor IS (salvo N7); 2×2 congelado para 2027.
- **§1 Introducción:** nuevo párrafo del estudio (modelos globales, métodos por serie, diseño factorial); R² de la persistencia 0,967–0,972; contribuciones 1–5 según la especificación; texto compactado.
- **§2 Literatura:** reorganizada en 2.1–2.5 (antes 2.1–2.8) y compactada de ~1.375 a ~740 palabras, sin eliminar ninguna cita; se agregan MCB (Koning et al., 2005).
- **§3.3:** la winsorización sólo para entrenar; toda evaluación contra la matrícula observada; declaración de la versión anterior (1.430 filas 2018–2026; +0,03 % a +0,34 % por año; Apéndice A.15).
- **§4.1:** alcance de orígenes actualizado (Secciones 5.2–5.10).
- **§4.2:** tasas de emparejamiento de las celdas evaluadas; eliminadas dos frases de detalle.
- **§4.4:** compactada.
- **§4.7:** reescrita: modelo principal (C49, elección por continuidad, versiones de `shap`), referentes por serie (`statsforecast` 2.1.1: RWD, AutoETS, AutoARIMA, Theta, Comb), modelo global solo de rezagos (Lrez), diseño factorial C49/Crez/L49/Lrez, reconciliación; sin [BRECHA Q1].
- **§4.8:** métricas compactadas; DM entre grupos con CR1 por clúster de institución, MCB/Nemenyi (liberal), HLN en N1, IS y MSIS; sin [BRECHA Q1].
- **§4.9:** calibración con residuos observados; sin [BRECHA Q1].
- **§5.1:** nota de la Tabla 3 sobre el valor recortado del *holdout* 2025 (+22,87 % con valor observado); compactada.
- **§5.2:** Tabla 4 con valor observado y valores *p*; lecturas actualizadas.
- **§5.3:** Tabla 5 con valor observado (2021: −2,17 %); figuras regeneradas.
- **§5.4:** Tabla 6 (validación 2026) con valores *p*; nueva Tabla 7 = cascada del *holdout* 2026 con valor observado y *p* (antes Tabla 10); N2 del *holdout* 88,68 % frente a 92,45 %, ±5 % en 40 de 53 y ±10 % en 47; tabla por institución movida al Apéndice A.24.
- **§5.5 (nueva):** comparación con referentes por serie y modelo global (Tabla 8, N1/N2/N5/N8); N1: Comb *p* HLN 0,0142, ARIMA 0,0374.
- **§5.6 (nueva):** diseño factorial (Tabla 9, N2/N8, DM); desglose por año L-02 con la formulación del autor y la advertencia de potencia.
- **§5.7:** Tabla 10 de cobertura con las cuatro bandas de 2027 y la recalibración (92,49 %); nueva Tabla 11 de IS/MSIS; excepción N7 declarada.
- **§5.8:** Tabla 12 = experimento de cuatro brazos (antes Tabla 9); nota I-05.
- **§5.9:** región y explicabilidad fusionadas; advertencia SHAP.
- **§5.10:** «Pronósticos 2027 (*ex ante*; congelamiento en curso)»; Tabla 13 con los seis pronósticos (C49 761.058, Crez 767.934, L49 760.672, Lrez 768.499, persistencia 741.615, Comb 746.696); composición por condición y jornada; bandas de los cuatro modelos; rango no conforme 719.308–777.914; referentes simples +3,40 %, +4,17 % y −1,27 %; protocolo H1–H5 resumido (detalle en A.14).
- **§6.1:** R² con valor observado. **§6.3:** compactada. **§6.4 (nueva):** «Qué aporta el modelo». **§6.5:** reescrita (P-04 cerrado, un año de prueba, valor recortado corregido, 113 duplicados con cifras observadas, Ñuble, reconciliación, shocks). **§6.6:** actualizada.
- **§7 Conclusiones:** reescritas con la tesis nueva.
- **Disponibilidad de datos:** pronósticos 2027 del 2×2 y de los referentes, protocolo y programa con sus huellas, publicados con el congelamiento.
- **Figuras:** las cinco del cuerpo se toman de las figuras regeneradas con la matrícula observada; rutas en la forma `<figuras/…png>`, porque al guardar el artefacto la plataforma reemplazaba la ruta de la Figura 5 por un enlace interno.
- **Referencias:** cinco entradas nuevas verificadas en CrossRef (koning2005, hyndman2008auto, assimakopoulos2000theta, hyndman2002ets, cameron2015cluster); 94 claves citadas, todas en el .bib.
- **Apéndice:** A.7 (R² sobre la tasa 0,141), A.9 (persistencia por año con valor observado), A.11, A.13 y A.14 (protocolo v2) actualizados; nuevas secciones A.15–A.24 con las tablas literales de J.1, A1–A6, el 2×2, L-02, L-01 e instituciones; rótulos de versión eliminados de las tablas copiadas; 43 tablas numeradas.
- **Title page:** extensión y número de tablas; disponibilidad de datos.

## Numeración de tablas del cuerpo

| Antes | Ahora |
|---|---|
| Tabla 7 (por institución) | Apéndice, Tabla A.43 |
| Tabla 8 (cobertura) | Tabla 10 |
| Tabla 9 (*target encoding*) | Tabla 12 |
| Tabla 10 (cascada del *holdout*) | Tabla 7 |
| — | Tablas 8, 9, 11 y 13 (nuevas) |

## Advertencias para el autor

1. **Interval score en N7.** La especificación y la sección J afirman que las bandas estratificadas tienen la mejor IS en N2–N8, pero la tabla A4 de J (valor observado) da en N7 IS 79,8 frente a 79,7 de AutoETS y MSIS 7,2482 frente a 7,2427. El cuerpo, la Tabla A.35 y el highlight lo reportan como excepción. El resumen conserva la frase literal «obtuvieron la mejor *interval score*», que es cierta en seis de siete niveles: conviene decidir si se matiza.
2. **Extensión.** El cuerpo quedó en ~10.700 palabras de prosa (objetivo ~10.500), con 13 tablas.
3. **Correlación tasa observada–pronosticada.** El texto mantiene 0,365 para la validación 2026 del origen 2025 (sin cambios); el 0,34 de M/N corresponde al *holdout* 2026 y no se usa en el cuerpo.

## Recuento de marcadores

| Archivo | [BRECHA Q1] | [PENDIENTE] |
|---|---:|---:|
| manuscrito_IJF_es.md | 1 | 11 |
| apendice_en_linea_es.md | 0 | 18 |
| title_page_es.md | 0 | 10 |

La única [BRECHA Q1] es el congelamiento formal de los pronósticos 2027 (P-01). Los [PENDIENTE L-01] y [PENDIENTE L-02] quedaron resueltos con las secciones M y N.

## [PENDIENTE] que quedan

**Manuscrito**

- PENDIENTE: búsqueda sistemática en Scopus/WoS/SciELO sobre *enrollment forecasting* y *higher education demand*, con criterios de inclusión declarados.
- PENDIENTE: confirmar si el PIB regional usado está a precios corrientes, como indica la documentación del pipeline, o en volumen encadenado, como describe la referencia del conjunto de datos; registrar ediciones y fechas de descarga de cada fuente.
- PENDIENTE: añadir al .bib la entrada del *Informe de Matrícula en Educación Superior 2026* del SIES, que es la edición cuyas cifras se citan; el .bib actual contiene sólo la edición 2025, `sies2025informe`.
- PENDIENTE: cita verificada de la prueba de Nemenyi
- PENDIENTE: valores *p* del OOF 2019–2026 y del *holdout* 2025 con el valor observado
- PENDIENTE: confirmar con la base observada de 2026
- PENDIENTE: fecha / commit / huellas SHA-256 / DOI Zenodo
- PENDIENTE: confirmación del autor para incluir esta nota
- PENDIENTE: insertar el DOI del depósito tras la aceptación.
- PENDIENTE: el autor debe completar esta declaración según la política de Elsevier, indicando qué herramienta se usó, con qué propósito y en qué etapas. Borrador neutral para revisar:
- PENDIENTE: confirmar.

**Apéndice**

- PENDIENTE: confirmar la serie usada (precios corrientes o volumen encadenado).
- PENDIENTE: declarar en el manuscrito final si el valor anual de 2025 se recalculará con los 12 trimestres.
- PENDIENTE: cifra con real observado
- PENDIENTE: tabla con real observado
- PENDIENTE: el autor debe confirmar el conjunto y el origen que representa esta figura y completar la leyenda.
- PENDIENTE: el autor debe confirmar el conjunto y el origen que representa esta figura, verificar que la celda no permita identificar información sensible y completar la leyenda.
- PENDIENTE: el autor debe confirmar el conjunto y el origen que representa esta figura, y si los deciles se definen por la matrícula observada o por el rezago.
- PENDIENTE: confirmación del autor para incluir esta nota
- PENDIENTE: corregir antes del congelamiento
- PENDIENTE: unificar el rótulo y regenerar las figuras con separador decimal en coma para la versión en español
- PENDIENTE: fecha / commit / huellas SHA-256 / DOI Zenodo
- PENDIENTE: N3, N4, N6 y N7 con real observado 
- PENDIENTE: cifra con real observado
- PENDIENTE: cifra con real observado
- PENDIENTE: cifra con real observado
- PENDIENTE: cifra con real observado
- PENDIENTE: cifra con real observado
- PENDIENTE: cifra con real observado

**Title page**

- PENDIENTE: fijar al traducir
- PENDIENTE: afiliación institucional completa, ciudad y país
- PENDIENTE
- PENDIENTE
- PENDIENTE, opcional
- PENDIENTE: confirmar.
- PENDIENTE: completar también el formulario de declaración de intereses de Elsevier al enviar.
- PENDIENTE: agregar agradecimientos personales o institucionales, si los hay; estos sólo deben figurar en esta página.
- PENDIENTE: DOI del depósito; nota para el editor, si se decide compartir el enlace no anónimo del repositorio documental y del tablero público sólo con el editor.
- PENDIENTE: el autor debe completar según la política de Elsevier; la misma declaración figura al final del manuscrito, antes de las referencias.
