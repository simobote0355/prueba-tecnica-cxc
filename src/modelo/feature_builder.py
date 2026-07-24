import numpy as np
import pandas as pd

class FeatureBuilder:
    def __init__(self, top_n_transacciones: int = 10):
        self.top_n_transacciones = top_n_transacciones
        self.categorias_frecuentes_ = None 

    def fit(self, df: pd.DataFrame):
        conteo = df['descri_cod_trn'].value_counts()
        self.categorias_frecuentes_ = conteo.head(self.top_n_transacciones).index.tolist()
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # grupa transacciones poco frecuentes en "OTROS"
        df['trn_agrupada'] = df['descri_cod_trn'].where(
            df['descri_cod_trn'].isin(self.categorias_frecuentes_), 
            'OTROS'
        )

        # Log-transform para el sesgo detectado en el EDA
        df['log_vlr_original'] = np.log1p(df['vlr_original'])

        # Encoding de variables categóricas
        df = pd.get_dummies(df, columns=['descri_cod_apli_prod', 'trn_agrupada'], drop_first=True)

        # Se xcluye porc_recuperado y dias_hasta_ultimo_pago: 
        # ambas se derivan de vlr_pagado / f_ultimo_pago, 
        # información que no existe al momento de creación de la cuenta (data leakage)
        columnas_modelo = [c for c in df.columns if c.startswith((
            'log_vlr_original', 'descri_cod_apli_prod_', 'trn_agrupada_'
        ))] 

        return df[columnas_modelo]

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)