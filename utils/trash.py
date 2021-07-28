import pandas as pd
df_ = pd.read_csv('./static/static_assets/bhavcopy/bhavcopy27JUL2021_delivery.csv')
df_ = df_.loc[df_['Name of Security'] == 'RELIANCE.NS'.replace('.NS', '')][' Quantity Traded'].iloc[0]
print(df_)