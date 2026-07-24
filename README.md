# Prueba Técnica CxC

Análisis de cartera de Cuentas por Cobrar (CxC): exploración de datos, modelo predictivo de probabilidad de pago y dashboard ejecutivo en Power BI.

## ¿Qué hace este proyecto?

A partir de una base histórica con aproximadamente 21.700 cuentas por cobrar, el proyecto responde tres preguntas:

1. **¿Cómo se comporta la cartera?** Exploración de datos (EDA).
2. **¿Qué probabilidad tiene cada cuenta de pagarse por completo?** Modelo de Machine Learning.
3. **¿Cómo se comunican los resultados al negocio?** Dashboard en Power BI y informe ejecutivo.

## Estructura del repositorio

```
data/               Base de datos original (SQLite)
docs/
  actividad1/        Exploración de datos (EDA)
  actividad2/         Modelo de probabilidad de pago
  actividad3/         Informe ejecutivo del dashboard
powerbi/             Dashboard (.pbix)
src/
  data/               Base de datos y sábanas (CSV) generadas
  sql/                Query SQL que construye la sábana analítica
  modelo/             Código del modelo (Random Forest)
  metricas/           Métricas de desempeño del modelo
  notebooks/          Notebooks de Jupyter (EDA, modelo, dashboard)
requirements.txt     Librerías necesarias
```

## Resumen de cada actividad

- **Actividad 1 — EDA:** el 79,7% de las cuentas se paga en su totalidad, 12,3% de forma parcial y 8,0% no se paga. Se documentan los hallazgos y decisiones en [`docs/actividad1/EDA.md`](docs/actividad1/EDA.md).
- **Actividad 2 — Modelo:** clasificador (Random Forest) que estima la probabilidad de pago total de cada cuenta, con AUC-ROC de 0,739. Detalle completo en [`docs/actividad2/ModeloProbabilidadPago.md`](docs/actividad2/ModeloProbabilidadPago.md).
- **Actividad 3 — Dashboard:** informe ejecutivo con indicadores financieros (valor esperado a recuperar, valor en riesgo) y recomendaciones operativas. Ver [`docs/actividad3/Dashboard.md`](docs/actividad3/Dashboard.md).

## Cómo ejecutar el proyecto

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Abrir los notebooks en orden desde `src/notebooks/`:
   - `01_eda.ipynb`
   - `02_modelo.ipynb`
   - `03_dashboard.ipynb`
3. Abrir `powerbi/dashboard.pbix` con Power BI Desktop para ver el dashboard interactivo.

## Tecnologías

Python (pandas, scikit-learn, matplotlib, seaborn), SQL (SQLite) y Power BI.
