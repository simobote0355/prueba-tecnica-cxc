# Modelo analítico de probabilidad de pago

## 1. Objetivo del modelo

Estimar para cada cuenta por cobrar, la probabilidad de que se pague en su totalidad. Esta probabilidad se utiliza posteriormente para traducir el saldo pendiente de cada cuenta en un valor esperado de recuperación y un valor en riesgo, insumos clave para el dashboard de la Actividad 3.

## 2. Definición de la variable objetivo

Se definió `pago_total` (variable binaria, ya calculada en la sábana de la Actividad 1) como variable objetivo: 1 si la cuenta se pagó en su totalidad (`vlr_pendiente_pago = 0`), 0 en caso contrario (pago parcial o sin pago).

En lugar de predecir un valor continuo mediante regresión `porc_recuperado`, se eligió un modelo de clasificación binaria. Esta aproximación se adecua mejor al caso de negocio, enfocado en segmentar y priorizar cuentas por riesgo (alto/bajo) de forma clara, accionable e intuitiva para el equipo de cartera.

## 3. Variables utilizadas (features)

Se incluyeron únicamente variables conocidas al momento de creación de la cuenta:

- `log_vlr_original` (transformación logarítmica de `vlr_original`, dado el fuerte sesgo a la derecha detectado en el EDA de la Actividad 1)
- `descri_cod_apli_prod` (tipo de producto: AHORRO / CORRIENTE), codificada como variable dummy
- `descri_cod_trn` agrupada (`trn_agrupada`): las 10 categorías de transacción más frecuentes se mantienen individuales; el resto (cola larga de baja frecuencia, sobre 71 categorías totales) se agrupa en "OTROS", codificada como variable dummy

### 3.1 Variables excluidas deliberadamente (data leakage)

Se excluyeron `pct_recuperado` y `dias_hasta_ultimo_pago` del conjunto de features, pese a estar disponibles en la sábana. Ambas variables se derivan de `vlr_pagado` y `f_ultimo_pago`, información que solo existe **después** de que la cuenta ha recibido pagos, es decir, posterior al momento en que realmente se necesitaría hacer la predicción (cuenta recién creada). Incluirlas implica data leakage: el modelo dejaría de aprender patrones de negocio genuinos y en su lugar aprendería a leer directamente el resultado que se le pide predecir.

Esta decisión se validó empíricamente entrenando el mismo modelo con y sin estas variables (ver sección 5).

## 4. Metodología

- **Algoritmo:** Random Forest Classifier (`n_estimators=200`, `max_depth=8`, `class_weight='balanced'` para compensar el desbalance de clases identificado en el EDA: ~80% pago total vs. ~20% parcial/sin pago).
- **División de datos:** 80% entrenamiento / 20% prueba, con estratificación sobre la variable objetivo para preservar la proporción de clases en ambos conjuntos.
- **Métricas de evaluación:** AUC-ROC, precisión, recall y F1, evaluadas sobre el conjunto de prueba. Se priorizaron estas métricas por sobre el accuracy dado el desbalance de clases: con ~80% de la clase mayoritaria, un modelo trivial que siempre prediga "pago total" ya alcanzaría ~80% de accuracy sin haber aprendido nada útil.

## 5. Resultados: impacto del data leakage

Se entrenó el modelo en dos escenarios idénticos en todo excepto en la inclusión de las variables con leakage, para cuantificar su impacto:

| Escenario | AUC-ROC | Precision | Recall | F1 |
|---|---|---|---|---|
| Sin leakage | 0,739 | 0,889 | 0,614 | 0,727 |
| Con leakage | 1,000 | 1,000 | 1,000 | 1,000 |

El escenario con leakage alcanza un desempeño perfecto en las cuatro métricas, una señal de alerta que el modelo no está prediciendo, sino leyendo directamente el resultado a través de variables que son una transformación de la propia variable objetivo (`porc_recuperado = 1` implica casi por definición `pago_total = 1`). Un modelo con desempeño perfecto sobre un problema de negocio real es en sí mismo una alerta de leakage, no un resultado perfecto.

El modelo definitivo y apto para producción corresponde al escenario sin leakage, alcanzando un AUC-ROC de 0.739. Este resultado refleja una capacidad de discriminación moderada y significativamente superior al azar (0.5), sin llegar a ser determinista. Dicho comportamiento concuerda con la complejidad del problema, donde la decisión de pago está sujeta a variables no observadas en el conjunto de datos, tales como el contexto económico o la conducta propia del cliente.

## 6. Interpretación de las métricas del modelo final (sin leakage)

- **Precision (0,889):** de las cuentas que el modelo predice como "se pagarán completamente", el 88,9% efectivamente lo hace. Es una precisión alta, lo que da confianza en las cuentas que el modelo marca como de bajo riesgo.
- **Recall (0,614):** de todas las cuentas que efectivamente se pagan en su totalidad, el modelo identifica correctamente al 61,4%. Este valor más moderado indica que el modelo es conservador: deja una porción de cuentas "buenas" clasificadas como riesgosas.
- **F1 (0,727):** balance entre las dos métricas anteriores.
- **AUC-ROC (0,739):** capacidad global del modelo para ordenar correctamente cuentas de mayor a menor probabilidad de pago, independiente del punto de corte usado.

## 7. Interpretación a nivel de cuenta individual

Es esperable encontrar cuentas cuyo desenlace real (pagada o no) difiere de lo que sugeriría su `prob_pago`. Por ejemplo, una cuenta ya pagada en su totalidad puede tener una probabilidad estimada moderada o baja (ej. 0,35). Esto no es un error del modelo, sino una consecuencia directa de que:

1. El modelo solo utiliza variables conocidas al momento de creación de la cuenta (monto, producto, tipo de transacción), deliberadamente excluye cualquier información posterior al desenlace (ver sección 3.1). Por lo tanto, `prob_pago` representa una tendencia estadística histórica para ese perfil de características, no una lectura del resultado real de esa cuenta específica.
2. El recall del modelo (0,614) indica que un 38,6% de las cuentas que sí se pagan completamente no son identificadas con alta confianza por el modelo, es decir, discrepancias como esta son esperables y consistentes con las métricas reportadas, no un indicio de un modelo mal construido.

En síntesis, la métrica `prob_pago refleja` la tendencia esperada para cuentas con un perfil determinado, no una certeza absoluta a nivel individual. Dado que el modelo cuenta con un AUC-ROC de 0.739, un desempeño intermedio, superior al azar pero no perfecto, es natural encontrar casos particulares que se aparten del comportamiento promedio

## 8. Salidas del modelo

Para cada cuenta se generan tres variables adicionales, que alimentan el dashboard de la Actividad 3:

- `prob_pago`: probabilidad estimada de pago total (entre 0 y 1)
- `valor_esperado_recuperar` = `vlr_pendiente_pago x prob_pago`
- `valor_en_riesgo` = `vlr_pendiente_pago x (1 − prob_pago)`

Por construcción, `valor_esperado_recuperar + valor_en_riesgo = vlr_pendiente_pago` para cada cuenta.

## 8. Limitaciones y supuestos

1. El valor esperado de recuperación asume una relación lineal entre probabilidad y monto recuperado (P(pago) x monto).
2. El modelo se entrena sobre una ventana histórica acotada (cuentas creadas entre fines de 2024 y mediados de 2025, según el rango observado en `f_creacion`), su desempeño en escenarios futuros con condiciones distintas no está garantizado y debería monitorearse.
3. El recall moderado (0,614) implica que, en el punto de corte usado (0,5), una proporción de cuentas de buen comportamiento se clasifica conservadoramente como riesgosa. Para uso operativo, el punto de corte podría ajustarse según el riesgo del negocio (ej. priorizar recall si el costo de perder una cuenta buena es alto).