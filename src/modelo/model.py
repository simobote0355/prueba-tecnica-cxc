# src/modelo/modelo_cxc.py
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score

class Model:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.modelo = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            class_weight='balanced',   # Compensa el desbalance 80/20 detectado en el EDA
            random_state=random_state
        )

    def entrenar(self, X: pd.DataFrame, y: pd.Series):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=self.random_state
        )
        self.modelo.fit(self.X_train, self.y_train)
        return self

    def predecir_proba(self, X: pd.DataFrame):
        return self.modelo.predict_proba(X)[:, 1]

    def evaluar(self) -> dict:
        proba_test = self.predecir_proba(self.X_test)
        pred_test = (proba_test >= 0.5).astype(int)

        metricas = {
            'auc_roc': roc_auc_score(self.y_test, proba_test),
            'precision': precision_score(self.y_test, pred_test),
            'recall': recall_score(self.y_test, pred_test),
            'f1': f1_score(self.y_test, pred_test),
        }
        return metricas

    def guardar(self, ruta: str = "../../src/modelo/modelo_ejemplo.pkl"):
        with open(ruta, "wb") as f:
            pickle.dump(self.modelo, f)