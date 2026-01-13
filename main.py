# oi, dis the main file, innit?

df = pd.read_csv(path)
df.columns = df.columns.str.lower()

# utils/helpers.py
import pandas as pd
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    return df
    
# preprocessing.py
from utils.helpers import load_data

df_name = load_data(path)