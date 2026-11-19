<!-- Generado por scripts/validacion/32_peores_por_origen_lag.py (corrida 20261118_1345) -->

**Tasa de emparejamiento de la llave del lag** (filas con lag, 2019-2026)

| origen_lag | celdas | % celdas | matrícula | % matrícula |
|---|---:|---:|---:|---:|
| fino | 72.063 | 98,10 % | 5.371.504 | 98,89 % |
| codigo | 483 | 0,66 % | 30.238 | 0,56 % |
| medio | 916 | 1,25 % | 30.312 | 0,56 % |

**Métricas por origen del lag**

| Conjunto | origen_lag | celdas | WAPE | WAPE naïve | skill | MASE |
|---|---|---:|---:|---:|---:|---:|
| OOF 2019-2025 | fino | 63.154 | 14,33 % | 14,79 % | -3,24 % | 0,969 |
| OOF 2019-2025 | codigo | 420 | 17,93 % | 17,41 % | -14,41 % | 1,030 |
| OOF 2019-2025 | medio | 819 | 31,08 % | 32,44 % | 27,80 % | 0,958 |
| Holdout 2026 | fino | 8.909 | 11,99 % | 12,81 % | 14,25 % | 0,936 |
| Holdout 2026 | codigo | 63 | 16,84 % | 15,82 % | -15,55 % | 1,064 |
| Holdout 2026 | medio | 97 | 27,29 % | 31,93 % | 29,10 % | 0,855 |

**Las 50 peores celdas por error absoluto, según el origen del lag**

| Conjunto | fino | codigo | medio | % de la matrícula en respaldos (conjunto completo) |
|---|---:|---:|---:|---:|
| OOF 2019-2025 | 49 | 1 | 0 | 1,13 % |
| Holdout 2026 | 50 | 0 | 0 | 1,04 % |

**Celdas citadas en la revisión (H-11)**

| Año | Institución | Carrera | Género | Condición | origen_lag | Lag | Real | Pred |
|---:|---|---|---|---|---|---:|---:|---:|
| 2020 | UNIVERSIDAD LOS LEONES | PEDAGOGIA EN EDUCACION DIFERENCIAL | MUJER | ANTIGUO | fino | 1.030 | 215 | 1.278,9 |
| 2019 | UNIVERSIDAD LOS LEONES | PEDAGOGIA EN EDUCACION DIFERENCIAL | MUJER | NUEVO | fino | 615 | 128 | 836,9 |
| 2020 | UNIVERSIDAD SEK | PEDAGOGIA EN EDUCACION DIFERENCIAL CON ESPECIALIDAD EN DISCAPACIDAD INTELECTUAL | MUJER | ANTIGUO | fino | 1.359 | 575 | 1.215,1 |
| 2026 | UNIVERSIDAD DE LAS AMERICAS | INGENIERIA DE EJECUCION INDUSTRIAL | HOMBRE | ANTIGUO | fino | 662 | 154 | 767,6 |
| 2026 | UNIVERSIDAD DE CHILE | INGENIERIA Y CIENCIAS - PLAN COMUN | HOMBRE | ANTIGUO | fino | 1.719 | 1.089 | 1.687,5 |
| 2019 | UNIVERSIDAD SEK | PEDAGOGIA EN EDUCACION DIFERENCIAL CON ESPECIALIDAD EN DISCAPACIDAD INTELECTUAL | MUJER | ANTIGUO | fino | 1.367 | 1.359 | 1.910,6 |
| 2020 | UNIVERSIDAD DE CHILE | INGENIERIA Y CIENCIAS - PLAN COMUN | HOMBRE | ANTIGUO | fino | 1.629 | 1.230 | 1.687,8 |
| 2021 | UNIVERSIDAD DE CHILE | INGENIERIA Y CIENCIAS - PLAN COMUN | HOMBRE | ANTIGUO | fino | 1.230 | 1.550 | 1.262,8 |
