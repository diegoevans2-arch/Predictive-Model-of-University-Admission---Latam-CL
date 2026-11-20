# Pronóstico 2027 congelado · diseño 2×2 + referencias

Pronósticos *ex ante* de la matrícula universitaria de pregrado 2027 en 9.069 celdas (institución × carrera × región × jornada × género × condición) de 53 universidades con programas vigentes en 2026 y al menos 10 matriculados. No es el titular nacional del SIES. La evaluación seguirá `protocolo_evaluacion_2027.md` (versión 2.2, aprobada el 20-11-2026) y la ejecutará `evaluar_2027.py`, ambos congelados en este paquete.

- **Fecha del paquete:** 2026-11-20.
- **Base:** matrícula 2026 observada de esas celdas = **741.615** (SIES, edición del 10-07-2026).
- **C49** es el pronóstico publicado de la corrida `modelo_final_20261118_1345` y se congela sin cambios. Su rezago 2027 es la matrícula 2026 reconstruida desde la tasa recortada del panel, que difiere de la observada en 75 celdas (suma 740.318). Las otras tres variantes usan el real 2026 observado.

## Pronósticos

| ID | Modelo | Total 2027 | Sobre la base observada | Cobertura de su banda en el holdout 2026 |
|---|---|---:|---:|---:|
| C49 | CatBoost · 49 variables (publicado) | 761.058 | +2,62 % | 92,49 % |
| Crez | CatBoost · solo rezagos | 767.934 | +3,55 % | 93,25 % |
| L49 | LightGBM · 49 variables | 760.672 | +2,57 % | 92,25 % |
| Lrez | LightGBM · solo rezagos | 768.499 | +3,63 % | 92,31 % |
| F0 | Persistencia (real 2026 observado) | 741.615 | +0,00 % | — |
| FN | Comb nacional (media de ETS, ARIMA y Theta; sólo N1) | 746.696 | +0,69 % | — |

Bandas al 90 %: conformal estratificado por tamaño (código de v4) sobre los residuos OOF 2019-2026 de cada modelo contra la matrícula observada. La calibración completa (celda y niveles N2-N7) está en `calibracion_bandas_2027.json`. Las bandas del archivo original de C49 (`predicciones_forecast_2027.csv`) se calibraron con residuos recortados y quedan como registro; las que se evalúan son las de `predicciones_forecast_2027_2x2.csv`.

## Por condición y jornada (variación sobre la base observada)

| Corte | Valor | Base 2026 | C49 | Crez | L49 | Lrez |
|---|---|---:|---:|---:|---:|---:|
| condicion | ANTIGUO | 589.678 | +3,44 % | +3,99 % | +3,25 % | +3,80 % |
| condicion | NUEVO | 151.937 | −0,54 % | +1,82 % | −0,07 % | +2,93 % |
| jornada | A Distancia | 43.050 | +14,56 % | +10,71 % | +12,89 % | +12,23 % |
| jornada | Diurna | 650.477 | +2,27 % | +3,71 % | +2,29 % | +3,50 % |
| jornada | Otra | 969 | −22,95 % | −36,33 % | −18,15 % | −14,60 % |
| jornada | Semipresencial | 8.954 | +10,27 % | +9,36 % | +7,94 % | +8,56 % |
| jornada | Vespertina | 38.165 | −5,93 % | −7,66 % | −5,06 % | −4,72 % |

## Por institución

| Institución | Base 2026 | C49 | Banda 90 % de C49 | Crez | L49 | Lrez |
|---|---:|---:|---:|---:|---:|---:|
| UNIVERSIDAD ANDRES BELLO | 63.244 | 66.375 | 57.926 – 71.613 | 66.738 | 67.087 | 67.057 |
| UNIVERSIDAD SAN SEBASTIAN | 47.311 | 48.675 | 42.480 – 52.516 | 47.960 | 48.492 | 49.704 |
| UNIVERSIDAD DE LAS AMERICAS | 35.823 | 38.253 | 33.384 – 41.271 | 39.334 | 38.101 | 39.336 |
| UNIVERSIDAD DE CHILE | 36.833 | 37.288 | 32.541 – 40.230 | 37.518 | 37.485 | 37.901 |
| PONTIFICIA UNIVERSIDAD CATOLICA DE CHILE | 34.082 | 34.685 | 30.270 – 37.422 | 34.892 | 34.476 | 34.767 |
| UNIVERSIDAD AUTONOMA DE CHILE | 32.254 | 32.974 | 28.777 – 35.576 | 33.141 | 33.252 | 33.504 |
| UNIVERSIDAD SANTO TOMAS | 28.615 | 29.350 | 25.614 – 31.666 | 30.309 | 29.667 | 29.834 |
| UNIVERSIDAD DE CONCEPCION | 25.556 | 25.308 | 22.086 – 27.305 | 25.883 | 25.247 | 25.821 |
| UNIVERSIDAD MAYOR | 23.332 | 24.145 | 21.072 – 26.050 | 24.176 | 24.170 | 24.405 |
| UNIVERSIDAD DE SANTIAGO DE CHILE | 22.598 | 22.947 | 20.026 – 24.757 | 23.177 | 22.972 | 23.111 |
| UNIVERSIDAD TECNICA FEDERICO SANTA MARIA | 20.646 | 20.518 | 17.907 – 22.137 | 21.017 | 20.519 | 20.963 |
| UNIVERSIDAD DIEGO PORTALES | 19.081 | 19.863 | 17.335 – 21.431 | 19.859 | 19.686 | 20.017 |
| PONTIFICIA UNIVERSIDAD CATOLICA DE VALPARAISO | 18.595 | 18.888 | 16.484 – 20.378 | 19.228 | 18.819 | 19.148 |
| UNIVERSIDAD DEL DESARROLLO | 18.227 | 18.583 | 16.218 – 20.050 | 18.820 | 18.615 | 18.819 |
| UNIVERSIDAD CENTRAL DE CHILE | 16.241 | 17.630 | 15.386 – 19.021 | 17.761 | 17.579 | 17.564 |
| UNIVERSIDAD AUSTRAL DE CHILE | 17.195 | 17.269 | 15.071 – 18.632 | 17.666 | 17.269 | 17.489 |
| UNIVERSIDAD CATOLICA DE LA SANTISIMA CONCEPCION | 16.497 | 17.168 | 14.983 – 18.523 | 17.372 | 17.082 | 17.157 |
| UNIVERSIDAD DE VALPARAISO | 14.875 | 14.774 | 12.894 – 15.940 | 15.106 | 14.837 | 14.999 |
| UNIVERSIDAD CATOLICA DEL MAULE | 13.658 | 14.248 | 12.435 – 15.372 | 14.225 | 14.247 | 14.279 |
| UNIVERSIDAD CATOLICA DE TEMUCO | 11.884 | 12.379 | 10.804 – 13.356 | 12.298 | 12.387 | 12.221 |
| UNIVERSIDAD DE TALCA | 11.962 | 12.333 | 10.763 – 13.306 | 12.664 | 12.211 | 12.356 |
| UNIVERSIDAD DE LOS LAGOS | 11.715 | 12.107 | 10.566 – 13.062 | 12.474 | 11.905 | 12.429 |
| UNIVERSIDAD CATOLICA DEL NORTE | 11.780 | 12.078 | 10.541 – 13.031 | 12.400 | 12.089 | 12.209 |
| UNIVERSIDAD DEL BIO-BIO | 11.318 | 11.352 | 9.907 – 12.248 | 11.678 | 11.286 | 11.527 |
| UNIVERSIDAD DE LA FRONTERA | 11.118 | 11.141 | 9.723 – 12.020 | 11.438 | 11.156 | 11.292 |
| UNIVERSIDAD DE TARAPACA | 10.665 | 10.845 | 9.465 – 11.701 | 10.908 | 10.822 | 10.958 |
| UNIVERSIDAD DE O'HIGGINS | 9.599 | 10.627 | 9.274 – 11.465 | 10.859 | 10.597 | 10.755 |
| UNIVERSIDAD DE VIÑA DEL MAR | 9.689 | 10.517 | 9.178 – 11.346 | 9.368 | 10.008 | 9.810 |
| UNIVERSIDAD ADOLFO IBAÑEZ | 10.684 | 10.386 | 9.064 – 11.206 | 10.915 | 10.764 | 10.858 |
| UNIVERSIDAD DEL ALBA | 9.061 | 9.989 | 8.718 – 10.778 | 9.571 | 9.880 | 9.634 |
| UNIVERSIDAD ARTURO PRAT | 9.436 | 9.577 | 8.358 – 10.332 | 9.555 | 9.523 | 9.389 |
| UNIVERSIDAD DE LOS ANDES | 9.133 | 9.196 | 8.026 – 9.922 | 9.477 | 9.200 | 9.297 |
| UNIVERSIDAD FINIS TERRAE | 8.992 | 9.136 | 7.973 – 9.857 | 9.271 | 9.173 | 9.275 |
| UNIVERSIDAD TECNOLOGICA METROPOLITANA | 8.513 | 8.751 | 7.637 – 9.442 | 8.977 | 8.779 | 8.781 |
| UNIVERSIDAD ALBERTO HURTADO | 8.148 | 8.535 | 7.449 – 9.209 | 8.483 | 8.407 | 8.552 |
| UNIVERSIDAD BERNARDO O'HIGGINS | 7.547 | 7.963 | 6.950 – 8.592 | 7.818 | 7.975 | 7.849 |
| UNIVERSIDAD DE ATACAMA | 7.794 | 7.713 | 6.731 – 8.322 | 8.071 | 7.713 | 8.157 |
| UNIVERSIDAD DE LA SERENA | 7.610 | 7.486 | 6.533 – 8.077 | 7.828 | 7.501 | 7.745 |
| UNIVERSIDAD DE ANTOFAGASTA | 6.756 | 6.734 | 5.877 – 7.266 | 6.809 | 6.736 | 6.798 |
| UNIVERSIDAD CATOLICA CARDENAL RAUL SILVA HENRIQUEZ | 5.975 | 6.154 | 5.371 – 6.640 | 6.160 | 6.144 | 6.106 |
| UNIVERSIDAD DE ARTES, CIENCIAS Y COMUNICACION - UNIACC | 6.019 | 5.782 | 5.046 – 6.238 | 5.806 | 5.751 | 5.920 |
| UNIVERSIDAD DE PLAYA ANCHA DE CIENCIAS DE LA EDUCACION | 5.791 | 5.531 | 4.827 – 5.968 | 5.609 | 5.474 | 5.528 |
| UNIVERSIDAD GABRIELA MISTRAL | 4.493 | 5.127 | 4.474 – 5.531 | 4.734 | 5.004 | 4.540 |
| UNIVERSIDAD METROPOLITANA DE CIENCIAS DE LA EDUCACION | 4.158 | 4.257 | 3.715 – 4.593 | 4.244 | 4.208 | 4.119 |
| UNIVERSIDAD DE MAGALLANES | 4.163 | 4.218 | 3.681 – 4.550 | 4.315 | 4.188 | 4.256 |
| UNIVERSIDAD ACADEMIA DE HUMANISMO CRISTIANO | 3.768 | 3.648 | 3.184 – 3.936 | 3.720 | 3.659 | 3.671 |
| UNIVERSIDAD ADVENTISTA DE CHILE | 2.608 | 2.633 | 2.298 – 2.841 | 2.662 | 2.612 | 2.609 |
| UNIVERSIDAD SEK | 2.319 | 2.286 | 1.995 – 2.467 | 1.916 | 2.253 | 2.124 |
| UNIVERSIDAD DE ACONCAGUA | 2.341 | 1.774 | 522 – 2.539 | 1.794 | 1.786 | 1.918 |
| UNIVERSIDAD MIGUEL DE CERVANTES | 1.035 | 1.018 | 300 – 1.458 | 1.047 | 1.020 | 1.056 |
| UNIVERSIDAD DE AYSEN | 788 | 803 | 236 – 1.150 | 835 | 822 | 825 |
| UNIVERSIDAD BOLIVARIANA | 77 | 35 | 25 – 39 | 45 | 32 | 50 |
| UNIVERSIDAD TECNOLOGICA DE CHILE INACAP | 13 | 4 | 3 – 5 | 4 | 4 | 6 |

## Supuestos

- Las exógenas de 2027 quedan en su último valor observado; el PIB regional y la desocupación de 2026 se arrastraron desde 2025.
- La base INDICES del CNED cubre 2026 sólo en parte.
- Metadata de C49 con 7 *folds* de validación (2019-2025) y rótulos corregidos el 20-11-2026 (`correcciones_metadata`).

## Artefactos no publicados en este repositorio

Se archivan fuera del repositorio; su huella SHA-256 (del archivo completo) permite verificar que no cambiaron.

| Artefacto | SHA-256 |
|---|---|
| `modelo_final_20261118_1345.joblib` | `201c0a9f6c4107b61855a3a819134c3d16e7cb8dbd3b7d1a22a46963985df7d8` |
| `metadata_modelo_20261118_1345.json` | `c42591c76df35b9e0154ba48b9a373421e183089eec50874a2aacff5abc1620b` |
| `predicciones_modelo_final_20261118_1345.parquet` | `22502ce71a26302a59284481b124a192c07fe2a782cc9656d80debb49effe585` |
| `predicciones_modelo_final_20261118_1345.csv` | `ee00675b4f5f4b39d9405a5432016f5c3945d6e80a126d45baa94ef6810a2e57` |
| `dataset_modelado_final.csv` | `25cd339b3c4049a48336ff04023ef30cf532226860abde3bc6fa2cd7b15cfe9f` |
| `modelo_2027_Crez_20261118_1345.joblib` | `8e145a4c7a7ecb8bd49704387ab116cb9136973bf9fd8cca9468190e9681942c` |
| `modelo_2027_L49_20261118_1345.joblib` | `732b304ac0c6a81fc23fc57f889e3019704224c6f91956d029983f805134c5b3` |
| `modelo_2027_Lrez_20261118_1345.joblib` | `3287c99fc39b59e5327f3dd608b750ee1651a41489f8932e14760128e3487fc5` |
