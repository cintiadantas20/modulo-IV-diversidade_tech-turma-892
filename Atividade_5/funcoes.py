import pandas as pd
import seaborn as sns

# função que carrega o dataset
def carrega_dataset(nome_dataset:str) -> pd.DataFrame:
    return sns.load_dataset(nome_dataset)