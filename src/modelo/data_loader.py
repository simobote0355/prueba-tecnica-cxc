import pandas as pd

class DataLoader:
    def __init__(self, ruta_csv: str = "../../src/data/sabana_cxc.csv"):
        self.ruta_csv = ruta_csv

    def cargar(self) -> pd.DataFrame:
        df = pd.read_csv(self.ruta_csv)
        return df