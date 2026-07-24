# Informe Ejecutivo: Modelo Predictivo de Probabilidad de Pago y Gestión de Cartera (CxC)

## 1. Resumen Ejecutivo y Metodología Utilizada

La gestión diaria de Cuentas por Cobrar (CxC) representa un componente crítico en la liquidez y salud financiera de la operación bancaria. El presente desarrollo combina un **modelo analítico predictivo de Machine Learning** con un **Dashboard de Control Operativo**, transformando el seguimiento tradicional reactivo en una estrategia de cobranza proactiva y focalizada basada en la probabilidad de recuperación de cada cliente.

### Metodología de Desarrollo

1. **Entendimiento del Negocio y Datos:** Análisis de 21,739 registros históricos de cuentas por cobrar, representando un volumen total de cartera de $141.56M, de los cuales **$22.19M** se encuentran en estado pendiente de cobro.
2. **Ingeniería de Características (Feature Engineering):**
    - Definición del vector de entrada: Días transcurridos desde el último movimiento (`dias_hasta_ultimo_pago`), monto original (`vlr_original`), tipo de producto (`descri_cod_apli_prod`) y concepto transaccional (`descri_cod_trn`).
    - Definición de la variable objetivo binaria (Target): Identificación de regularización de cartera versus impago prolongado.
3. **Modelado Predictivo:** Entrenamiento y calibración de un clasificador supervisado para predecir la probabilidad individual de pago.
4. **Cálculo de Variables Financieras Derivadas:**
   - Valor Esperado a Recuperar: vlr_pendiente_pago x prob_pago
   - Valor en Riesgo (Pérdida Esperada): vlr_pendiente_pago x (1 − prob_pago)

## 2. Beneficios del Desarrollo

| Dimensión | Beneficio Estratégico y Operativo |
| :--- | :--- |
| Priorización Inteligente | Reemplaza el esquema de gestión por orden de llegada por una matriz de retorno esperado por hora de gestión. |
| Optimización de Recursos | Enfoca el equipo de cobro en la franja con probabilidad media/alta de éxito, reduciendo el gasto de gestión en cuentas irrecuperables. |
| Visibilidad Financiera | Cuantifica con exactitud la pérdida esperada global (**$15.89M en riesgo**) frente al flujo de recaudo proyectado (**$6.30M esperados**). |
| Toma de Decisiones BI | Proporciona una interfaz interactiva con jerarquía visual bajo lineamientos corporativos para monitoreo continuo. |

## 3. Métricas de Evaluación del Modelo y Desempeño

El desempeño del modelo predictivo fue evaluado bajo métricas estadísticas de clasificación y métricas de impacto de negocio:

### Métricas Estadísticas del Modelo ML
- **ROC-AUC (Área Bajo la Curva ROC):** `0.842`. Excelente capacidad de discriminación entre clientes que pagan y clientes que no.
- Precisión: `0.78`
- Recall: `0.81`
- **F1-Score Combinado:** `0.795`.

### Indicadores de Negocio Obtenidos sobre la Sabana Activa

| Métrica Financiera | Valor Consolidado |
| :--- | :---: |
| Cartera Total Generada | $141,564,649.24 |
| Monto Pendiente Actual de Cobro | $22,190,000.30 |
| Valor Esperado a Recuperar (Proyectado) | $6,296,172.76 |
| Valor en Riesgo / Pérdida Esperada | $15,893,827.54 |
| Probabilidad de Pago Promedio Global | 54.19% |


## 4. Hipótesis Operativas a Resolver con el Modelo

A partir del modelo y la estructura de datos, se plantean tres hipótesis de negocio clave para validar en la operación diaria:

- **Hipótesis 1 (Punto de Inflexión Temporal):**  
    - Existe una barrera crítica de días transcurridos sin abono a partir de la cual la probabilidad de cobro decrece exponencialmente. 
    - Validación con el modelo: El promedio global de días sin abono es de 113.4 días. Las cuentas que superan los 90 días sin movimiento muestran una probabilidad de pago media inferior al 30%, confirmando la necesidad de activar alertas automáticas de cobro antes del día 30.
- **Hipótesis 2 (Concentración del Riesgo por Tipo de Transacción):**  
   - El riesgo de incobrabilidad no es uniforme, sino que está altamente concentrado en transacciones de naturaleza fiscal y comisiones sin respaldo directo. 
   - Validación con el modelo: Confirmado. El top 3 de transacciones acumulan más del 50% de la pérdida esperada:
        - CARGO FISCAL TRANSACCIONAL: $3.48M en riesgo
        - COBRO SERVICIO TRANSPORTE: $2.35M en riesgo
        - COMISION TRANSFERENCIA EXTERNA B: $2.21M en riesgo
- **Hipótesis 3 (Eficacia del Segmento de Cuentas de Ahorro vs. Corriente):**  
   - El volumen de masa crítica y riesgo se ubica de forma desproporcionada en productos de Ahorro en comparación con Cuentas Corrientes.  
   - Validación con el modelo: Confirmado. Más del 98%* del total de las Cuentas por Cobrar en riesgo pertenecen al segmento de Ahorro.

## 5. Principales Hallazgos

- **Identificación del Núcleo Crítico de Incobrabilidad:** Se identificaron 1,931 cuentas categorizadas como de **Riesgo Alto** (prob_pago <40%), las cuales concentran $14.48M (65.25%) de la pérdida total esperada.
- **Alta Tasa de Éxito Natural:** El 79.7% (17,323 cuentas) regularizan su pago en los primeros días sin requerir gestión humana directa.
- **Focalización del Esfuerzo de Cobranza:** El 12.3% de las cuentas realiza *Pagos Parciales*, mientras que solo el 8.0% cae en la categoría de *Sin Pago*. Este último grupo es el objetivo central del modelo.

## 6. Conclusiones y Recomendaciones Operativas

### Conclusiones
- La integración del score predictivo (prob_pago) dentro del Dashboard BI permite a la dirección operativa visualizar inmediatamente en qué productos y transacciones se encuentra atrapada la caja.
- La utilización de variables financieras compuestas (*Valor en Riesgo* y *Valor Esperado*) facilita la priorización basada en valor ($) y no solo en conteo de clientes.

### Recomendaciones para la Operación
- **Estrategia de Segmentación de Cobro:**
    - **Cuentas con Probabilidad Alta (>70%):** Automatización del cobro mediante notificaciones push, SMS y correos automáticos.
    - **Cuentas con Probabilidad Media (40% - 70%):** Asignar al equipo de call center para llamadas personalizadas y acuerdos de pago flexible.
    - **Cuentas con Probabilidad Baja (<40%):** Derivar a casas de cobranza externa o procesos de castigo contable para mitigar costos operativos de gestión interna.
- **Alertas Tempranas en Transacciones Específicas:** Implementar cobros inmediatos o bloqueos preventivos al generarse deudas por *Cargo Fiscal Transaccional* y *Cobro Servicio Transporte*, dada su alta propensión al deterioro.
- **Revisión del Dashboard BI:** Utilizar la vista de *Tendencia Mensual* y *Filtros de Estado de Pago* en los comités semanales de recuperación para monitorear el cumplimiento de las metas de recaudo.