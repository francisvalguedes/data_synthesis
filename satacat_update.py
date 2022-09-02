import pandas as pd


print('Downloading Celestrak satcat file')
try:
    satcat_df = pd.read_csv('https://celestrak.org/pub/satcat.csv') 
    print('Downloaded Celestrak satcat file ok')
except:
    print('satcat download error')

satcat_df.to_csv('satcat.csv',  index=False)