# Cambios del delta v4 del manuscrito IJF en español (20-11-2026)

Fuente literal de cifras: secciones Q, R, S y U de OBSERVACIONES_Y_MEJORAS.md. Versión de partida: manuscrito v9c2ba428 (resumen de 147 palabras, sin cambios), apéndice v537baf42, title page v0dc76920, highlights va128551d y checklist vff131b97.

## Manuscrito

- §3.1, Tabla 1 y nota: PIB en volumen a precios del año anterior encadenado (referencia 2018; Banco Central, edición del 23-04-2026, cifras preliminares); desocupación 2025 con 10 de 12 trimestres móviles; cerrado el [PENDIENTE] del PIB
- Tabla 4: valores *p* del OOF 2019–2026 (0,9758 / 0,0992) y del *holdout* 2025 (0,0569 / 0,0052) con nota sobre los 73.349 grupos; §5.2: lectura de R-01 sin suavizar
- §5.9: región con valor observado (11,99 % Los Ríos – 25,50 % Aysén; RM 14,78 %; WAPE menor que la persistencia en 14 de 16, *skill* negativo en 6)
- §5.10: título «*ex ante*, congelados antes del dato»; texto literal del congelamiento del 20-11-2026 con identificadores omitidos y [PENDIENTE: DOI de Zenodo]; criterio asimétrico v2.2 de calibración fijado tras la prueba en seco; eliminada la única [BRECHA Q1]; 15 de 53 caídas confirmadas con base observada; regresión lineal 730.266 (−1,53 %); leyenda de la Figura 5 sin la advertencia de rótulo ni de separador
- Figuras: rutas a figuras_es/; leyendas de las Figuras 1, 3 y 5 sin advertencias de separador; Figura 3 con el punto 2018 observado (653.163)
- §1, §6.4 y §7: el «resultado robusto» se matiza con R-01 (ventaja en WAPE; significativa sólo en 2025–2026, no en el OOF completo); tiempos verbales del congelamiento
- Disponibilidad de datos: publicación con el congelamiento del 20-11-2026; [PENDIENTE: DOI de Zenodo]
- §3.1, nota de la Tabla 1: se eliminó la frase residual sobre precios corrientes (no queda «precios corrientes» en el texto).

## Apéndice

- A.1: PIB en volumen a precios del año anterior encadenado (referencia 2018; edición del 23-04-2026, cifras preliminares; filas anuales 2013–2025; 2026 arrastrado); desocupación 2025 con 10 de 12 trimestres móviles, explicando cuáles faltan. Cerrados ambos [PENDIENTE].
- A.9: Tabla A.13 (región) y Tabla A.14 (modalidad) reemplazadas por las versiones de R.2 con la matrícula observada (región con R² y error agregado; WAPE menor que la persistencia en 14 de 16 regiones, *skill* negativo en 6).
- A.10: leyendas SHAP (Figuras A.2–A.5) declaran que son atribuciones del modelo final entrenado con 2018–2026 sobre filas OOF 2019–2026, dentro de la muestra; Figura A.3 = promedio de |SHAP| por subgrupo; nueva Figura A.4 (fig11b, SHAP medio con signo); Figura A.5 (fig12) conserva institución y carrera por decisión del autor. Cerrados los [PENDIENTE] de leyendas.
- A.12: Figura A.8 (fig07) con deciles por rezago y los sesgos de U.1 (+1,25 %; +0,25 %; −1,70 %; −1,66 %; −1,64 %; −2,48 %; −2,40 %; −2,78 %; −1,87 %; −2,57 %; negativo = sobrepredicción); nueva Figura A.9 (fig07b, deciles por matrícula observada; Q1 −94,44 % … Q10 −0,43 %) como ilustración de la regresión a la media; eliminada la advertencia de ejes en inglés de la Figura A.6.
- A.13: ítem 3 (metadatos) sin [PENDIENTE], declarado como nota; ítem 4 (figuras) actualizado: figuras regeneradas, 2018 observado en la Figura 3 y regresión lineal −1,53 %.
- A.14: protocolo v2.2 aprobado y congelado el 20-11-2026; criterio asimétrico de calibración (subcobertura < 88 %, calibradas 88–95 %, conservadoras > 95 %) fijado tras la prueba en seco sobre 2026; resultados de la prueba en seco en N8 y N2–N7; identificadores omitidos; [PENDIENTE: DOI de Zenodo].
- A.16: nueva tabla A1 en N3, N4, N6 y N7 con la matrícula observada (R.2); cerrado el [PENDIENTE].
- A.17: nueva tabla R.1 (CatBoost frente a la persistencia en el OOF 2019–2026 y el *holdout* 2025, matrícula observada); MCB/Nemenyi por nivel con la matrícula observada para el *holdout* 2026 y la validación 2026 (reemplaza las tres tablas MCB anteriores).
- A.19: Tabla de IS/MSIS reemplazada por la versión completa de R.2 (con grupos comunes).
- **Tablas retiradas** por existir sólo con el valor recortado y sin versión observada en R.2: modelo global frente a la persistencia (*holdout* 2026), N1 con HLN en ambas pérdidas, y ablación N1–N8 en el *holdout* y en el OOF. Su contenido clave con valor observado está en las Tablas A.26 (C49 frente a persistencia y global, con la nota HLN observada) y A.32 (ablación N2 y N8).
- Rutas de figuras a `figuras_es/`.
- Renumeración: tablas A.1–A.41 (incluida la tabla de hipótesis H1–H5 del protocolo, que antes no tenía número: Tabla A.16) y figuras A.1–A.9 en orden de aparición; referencias internas actualizadas y verificadas por código.

## Highlights y title page

- Highlights: «Se congelaron…» (81–84 caracteres; sin identificadores del congelamiento).
- Title page: 41 tablas y 9 figuras en el apéndice; disponibilidad de datos con el congelamiento del 20-11-2026 y los identificadores entregados al editor en la carta; [PENDIENTE: DOI de Zenodo]; retirado el [PENDIENTE: fijar al traducir] del título de trabajo en inglés.

## Verificaciones por código

- 94/94 claves de cita en references.bib (sin cambios en el .bib); resumen ES 147 palabras por espacios; highlights ≤ 84 caracteres; referencias cruzadas a secciones, tablas, figuras y apartados A.x sin destinos faltantes; sin «−1,27 %» ni «precios corrientes»; sin «e1f9b448», «forecast-2027» ni las huellas en manuscrito, apéndice y highlights; cifras nuevas verificadas contra Q–U.
- .docx regenerados con pandoc + citeproc + APA, con las figuras leídas de `Documents/OUTPUTS_PAPER/figuras_es`: manuscrito con 13 tablas, 5 figuras y 94 referencias; apéndice con 41 tablas, todas numeradas, y 9 figuras.
- Extensión del cuerpo: ~10.970 palabras de prosa (antes ~10.680), por las frases nuevas de R-01 y del protocolo.

## Decisiones de criterio

1. **Signo de fig07.** La tabla de R.2 usa predicho/real − 1; la figura y U.1 usan (real − predicho)/real. Las leyendas copian las cifras de U.1, que son las de la figura.
2. **«Resultado robusto».** Con R-01 se matizó en §1, §6.4 y §7: los modelos globales tienen menos WAPE que la persistencia en la celda, pero la ventaja del CatBoost no es significativa en el OOF 2019–2026 y sí en 2025–2026 con pérdida absoluta.
3. **Metadatos del modelo.** Q–U no confirman que se haya corregido el número de *folds* en los metadatos; se quitó el [PENDIENTE] según la especificación, pero queda como nota en A.13 y como punto a verificar en el checklist.
4. **Cita de Nemenyi.** No se encontró un DOI verificable (la tesis original y Demšar 2006 no están en CrossRef); queda como [PENDIENTE].

## Recuento de marcadores

| Archivo | [BRECHA Q1] | [PENDIENTE] |
|---|---:|---:|
| manuscrito_IJF_es.md | 0 | 8 |
| apendice_en_linea_es.md | 0 | 2 |
| title_page_es.md | 0 | 9 |

No quedan [BRECHA Q1].

## Lista final de [PENDIENTE]

**Manuscrito**

- PENDIENTE: búsqueda sistemática en Scopus/WoS/SciELO sobre *enrollment forecasting* y *higher education demand*, con criterios de inclusión declarados.
- PENDIENTE: añadir al .bib la entrada del *Informe de Matrícula en Educación Superior 2026* del SIES, que es la edición cuyas cifras se citan; el .bib actual contiene sólo la edición 2025, `sies2025informe`.
- PENDIENTE: cita verificada de la prueba de Nemenyi
- PENDIENTE: DOI de Zenodo
- PENDIENTE: confirmación del autor para incluir esta nota
- PENDIENTE: DOI de Zenodo
- PENDIENTE: el autor debe completar esta declaración según la política de Elsevier, indicando qué herramienta se usó, con qué propósito y en qué etapas. Borrador neutral para revisar:
- PENDIENTE: confirmar.

**Apéndice**

- PENDIENTE: confirmación del autor para incluir esta nota
- PENDIENTE: DOI de Zenodo

**Title page**

- PENDIENTE: afiliación institucional completa, ciudad y país
- PENDIENTE
- PENDIENTE
- PENDIENTE, opcional
- PENDIENTE: confirmar.
- PENDIENTE: completar también el formulario de declaración de intereses de Elsevier al enviar.
- PENDIENTE: agregar agradecimientos personales o institucionales, si los hay; estos sólo deben figurar en esta página.
- PENDIENTE: DOI de Zenodo
- PENDIENTE: el autor debe completar según la política de Elsevier; la misma declaración figura al final del manuscrito, antes de las referencias.
