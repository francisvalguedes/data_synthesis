import glob
import pandas as pd
import re

txt_files = glob.glob('data/*.txt')

# print(txt_files)

data = {'NORAD_ID':[], 'N':[],  'h0':[], 'd_h0':[],'d_min':[], 'd_fin':[]  }

for file_name in txt_files:
    df = pd.read_csv(file_name)
    # print(df.head())
    df = df.drop(0)
    # df1 = df.iloc[[0, df["Range (km)"].idxmin(),-1]]
    # a = min(df.loc[:,"Range (km)"] )
    norad_id = re.findall(r'[0-9]+', file_name)
    # print(norad_id)

    data['NORAD_ID'].append(norad_id[0])
    data['N'].append(norad_id[1])
    data['h0'].append(df.iloc[0]["Time (UTCG)"])
    data['d_h0'].append(df.loc[1,"Range (km)"])
    data['d_min'].append(min(df.loc[:,"Range (km)"]))
    data['d_fin'].append(df.iloc[-1]["Range (km)"])
    # df2 = pd.DataFrame([{'NORAD_ID':array[0], 'N':array[1],  'h0':df.iloc[0]["Range (km)"] , 'd_h0':df.loc[1,"Range (km)"],'d_min':min(df.loc[:,"Range (km)"]), 'd_fin':df.iloc[-1]["Range (km)"]  }])


df_synthesis = pd.DataFrame(data)

df_synthesis.to_csv('so.csv', encoding='utf-8', index=False)

print(df_synthesis)