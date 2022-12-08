import pandas as pd
import seaborn as sns

# função que carrega o dataset
def carregar_dataset(nome_dataset):
    return sns.load_dataset(nome_dataset)