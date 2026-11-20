# Protocolo de evaluación del pronóstico 2027 — versión 2.2 (aprobada por el autor el 20-11-2026)

*Versión 2.2, del 20-11-2026, redactada por Claude Science. El autor aprobó la v2.1, y la v2.2 solo cambia el criterio de calibración de §6 y la descripción de H5. Incorpora las decisiones del autor de esa fecha:*
- *se congela el diseño 2×2 completo;*
- *el CatBoost publicado se congela tal cual, con su base declarada;*
- *las bandas se recalibran con residuos observados;*
- *la pérdida principal es la absoluta;*
- *el criterio de calibración es asimétrico (v2.2).*

*Una vez aprobada, esta versión se copia como `forecast_2027/protocolo_evaluacion_2027.md`, entra en `SHA256SUMS.txt` y se congela con la etiqueta. Todo análisis que no figure aquí se reportará como no planificado.*

## 1. Pronósticos congelados

| ID | Modelo | Variables | Rezago 2027 usado | Total 2027 | Crecimiento sobre el real 2026 observado (741.615) |
|---|---|---|---|---:|---:|
| C49 | CatBoost publicado (corrida 2027) | 49 | Real 2026 **winsorizado** en 75 celdas (740.318) | 761.058 | +2,62 % |
| Crez | CatBoost, solo rezagos | Rezagos t−1 a t−3 de arcsinh(tasa), año relativo e identificadores | Real 2026 observado | 767.934 | +3,55 % |
| L49 | LightGBM global | 49 | Real 2026 observado | 760.672 | +2,57 % |
| Lrez | LightGBM global, solo rezagos | Como Crez | Real 2026 observado | 768.499 | +3,63 % |
| F0 | Persistencia | — | — | 741.615 | 0,00 % |
| FN | Comb nacional: media de ETS, ARIMA y Theta sobre la serie nacional (solo para N1) | — | — | 746.696 | +0,69 % |

- **Especificaciones fijas:** las de la sección J.3 de `OBSERVACIONES_Y_MEJORAS.md` (hiperparámetros, semilla 42, target encoding dentro del fold y entrenamiento con 2018-2026).
- **Declaración sobre C49:** se congela sin cambios porque su total ya estaba publicado. Las 75 celdas con rezago recortado son una propiedad documentada de C49, no un error que se corrige después.
- **Bandas al 90 %:** conformal estratificado por tamaño, con el código de v4, sobre los residuos OOF 2019-2026 de cada modelo contra el real observado. **Se congelan las bandas recalibradas con residuos observados**, también las de C49. Cobertura en el holdout 2026 (calibrando con OOF 2019-2025): C49 92,49 %, Crez 93,25 %, L49 92,25 % y Lrez 92,31 %.
- **Archivo de predicciones:** `predicciones_forecast_2027_2x2.csv` (9.069 celdas con el puntual y la banda de los cuatro modelos, el rezago congelado de C49 y el real 2026 observado), más el archivo original de C49 sin tocar.
- **Universo:** 9.069 celdas de programas universitarios de pregrado vigentes en 2026 con al menos 10 matriculados.

## 2. Dato real

- **Fuente:** la base de matriculados 2027 del SIES, en su primera publicación (prevista para julio de 2027). Se descarga dentro de los 30 días siguientes y se registra su huella SHA-256.
- **Reconstrucción:** con las reglas de ingesta del documento técnico (§4.2 y §5.1): pregrado, universidades y la misma llave de celda.
- **Sin winsorización ni ajuste alguno.** El recorte de la tasa solo se usa para entrenar, nunca para evaluar.
- **Control previo:** el total universitario de pregrado reconstruido debe coincidir con el del informe oficial 2027 del SIES. Si no coincide, la diferencia se documenta antes de evaluar.

## 3. Emparejamiento

- **Principal:** por llave de celda con el nombre de la carrera, como en la validación 2026.
- **Secundario:** por código de carrera (P-07), como análisis de sensibilidad.
- **Programas cerrados:** las celdas pronosticadas sin matrícula 2027 quedan fuera del análisis principal. Se informan su número y la matrícula pronosticada que representan.
- **Programas nuevos 2027:** fuera de alcance. Se informan su número y su matrícula.
- **Cobertura:** se informa la proporción de la matrícula universitaria de pregrado 2027 que cae en celdas emparejadas.

## 4. Métricas y niveles

- **Niveles:** N1-N8 por suma ascendente de celdas, como en el paper.
- **Métricas:**
  - WAPE;
  - RelMAE = MAE / MAE de F0;
  - *skill* = 1 − (RMSE / RMSE de F0)²;
  - % de grupos dentro de ±10 %;
  - error agregado = (Σpred − Σreal) / Σreal.
- **Intervalos de los cuatro modelos:**
  - cobertura empírica, con intervalo de confianza binomial al 95 %;
  - ancho mediano;
  - *interval score* (α = 0,10) y MSIS escalada por el MAE de F0;
  - como referencia, un conformal sin estratos calibrado con los mismos residuos.

## 5. Hipótesis y comparaciones preespecificadas

Todas las pruebas son DM entre grupos, con error estándar robusto por clúster de institución, bilaterales y con α = 0,05.
- **Pérdida principal: absoluta.**
- **Pérdida secundaria: cuadrática.**

| ID | Pregunta | Contraste | Nivel principal | Niveles secundarios |
|---|---|---|---|---|
| H1 | ¿Los modelos superan a la persistencia? | C49 − F0, Crez − F0, L49 − F0 y Lrez − F0 | N8 | N2, N5 |
| H2 | ¿Aportan las variables exógenas? | **C49 − Crez** y **L49 − Lrez** | N8 y N2 (ambos principales) | N5 |
| H3 | ¿Importa el algoritmo? | C49 − L49 y Crez − Lrez | N8 | N2, N5 |
| H4 | Total nacional | Error agregado de los cuatro modelos, F0 y FN | N1 | — (descriptivo: un solo año) |
| H5 | Calibración de las bandas | Cobertura de los cuatro modelos frente al 90 % nominal, clasificada con el criterio asimétrico de §6 | N8 | N2-N7 |

- No se corrige por multiplicidad.
- Todas las comparaciones se reportan, cualquiera sea su resultado.
- **H2 en cifras, antes de ver el dato:** los dos modelos con exógenas pronostican menos crecimiento que los dos sin exógenas (C49 +2,62 % y L49 +2,57 %, frente a Crez +3,55 % y Lrez +3,63 %). La diferencia se concentra en los alumnos nuevos (C49 −0,54 %, L49 −0,07 %, Crez +1,82 %, Lrez +2,93 %). Por eso, H2 también se reporta por condición (nuevo/antiguo) en N8 como comparación secundaria.
- La lectura de H2 se fija de antemano. Si en N8 las exógenas no mejoran con ningún algoritmo, se repite el resultado de 2026. Si mejoran en N2 con ambos, se repite el de 2019-2025. Cualquier otra combinación se reporta como tal, sin reinterpretarla.

## 6. Criterios de éxito y de fracaso

- Un modelo **no supera a la persistencia** si su RelMAE en N8 es mayor o igual a 1. Se reporta como fracaso de ese modelo en 2027, sin reinterpretación.
- **Calibración de las bandas (criterio asimétrico).** La garantía del predictor conforme es una cobertura de *al menos* 1 − α. Por eso, la falla relevante es la subcobertura, y la sobrecobertura es solo ineficiencia, que mide la *interval score*. Con la cobertura empírica de cada modelo en N8 (9.069 celdas, o las emparejadas):
  - **Subcobertura (fracaso de las bandas):** cobertura < 88 %.
  - **Calibradas:** 88 % ≤ cobertura ≤ 95 %.
  - **Conservadoras (no es fracaso):** cobertura > 95 %. La ineficiencia se evalúa con la IS y la MSIS frente al conformal sin estratos (H5).
  - En todos los casos se informan el IC de Wilson al 95 % de la cobertura, el ancho mediano, la IS y la MSIS. Los niveles N2-N7 se informan con la misma clasificación, solo de forma descriptiva.
  - **Justificación de los umbrales, fijada antes de ver 2027:** 88 % admite hasta 2 puntos de pérdida de cobertura por cambio de distribución entre 2026 y 2027 antes de declarar fracaso. 95 % refleja la sobrecobertura ya documentada: 92,25-93,25 % en el holdout 2026, por los residuos de los años OOF tempranos.
  - **Declaración:** este criterio reemplaza al de la versión 2.1 (IC al 95 % que contenga el 90 %). El cambio se hizo después de la prueba en seco sobre el holdout 2026, que mostró que con 9.069 celdas ese IC mide ±0,5 puntos y habría declarado «mal calibradas» unas bandas con 92-93 % de cobertura. Se hizo antes del congelamiento y sin ningún dato de 2027.
- Ningún resultado de 2027 modifica los pronósticos congelados. Las versiones posteriores del pipeline se evalúan por separado.

## 7. Ejecución y publicación

- La evaluación la ejecuta `evaluar_2027.py`, que se congela en el mismo paquete (con su huella en `SHA256SUMS.txt`) después de una prueba en seco sobre el holdout 2026.
- Los resultados se publican dentro de los 60 días siguientes a la publicación del SIES, con la huella del archivo real usado y la lista de desvíos respecto de este protocolo.
