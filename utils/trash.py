from numpy import average
import pandas as pd
df = pd.read_csv(f'./static/static_assets/max_1d/RELIANCE.NS.csv')
print(average(df['% Dly Qt to Traded Qty'].tail(10).values))