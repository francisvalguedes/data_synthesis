import glob
import pandas as pd
import re
from datetime import date
from datetime import datetime, timedelta
import numpy as np

satcat_df = pd.read_csv('https://celestrak.org/pub/satcat.csv') 

txt_files = glob.glob('trajetory/*.trn')
# print(txt_files)

data = {'NORAD_CAT_ID':[], 'OBJECT_NAME':[], "H0":[], "RANGE_H0":[],"MIN_RANGE_H":[],"MIN_RANGE_PT":[],
                    "MIN_RANGE":[],"END_H":[], "END_PT":[], "END_RANGE":[],"RCS":[] }

for file_name in txt_files:
    #print(file_name)
    df = pd.read_csv(file_name,skiprows=[0,1], header=None)
    df.columns = ['ENU_E','ENU_N','ENU_U']
    df.to_csv( 'output/' + file_name.split("\\")[1], index=False, header=['1','1000', str(len(df.index))],float_format="%.3f")    # print(df)
    info = file_name.split('-')[1].split('_obj_')
    datetimestr = info[0]
    norad_cat_id = info[1].split('_')[0]
    datetime_object = datetime.strptime(datetimestr, '%Y%m%d_%H%M%S') - timedelta(seconds=1)
    print(datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    print(norad_cat_id)
    rd_range = 0.001*np.linalg.norm(df,axis=1)
    min_index = np.argmin(rd_range)
    min_rd_range = rd_range[min_index]
    datetime_object_min = datetime_object + timedelta(seconds=int(min_index))

    index_satcat = satcat_df.loc[satcat_df['NORAD_CAT_ID']==int(norad_cat_id)].index

    if satcat_df.loc[index_satcat, 'RCS'].empty :
        rcs = 0.0
    else:
        rcs = float(satcat_df.loc[index_satcat, 'RCS'] )
  
    data["NORAD_CAT_ID"].append(norad_cat_id)
    data["OBJECT_NAME"].append(satcat_df.loc[index_satcat, 'OBJECT_NAME'].to_string(index=False))
    data["RCS"].append(rcs)
    data["H0"].append(datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    data["RANGE_H0"].append(rd_range[0])
    data["MIN_RANGE_H"].append(datetime_object_min.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    data["MIN_RANGE_PT"].append(min_index)
    data["MIN_RANGE"].append(min_rd_range)
    data["END_H"].append((datetime_object + timedelta(seconds= len(df.index))).strftime("%Y-%m-%dT%H:%M:%S.%f"))
    data["END_PT"].append( len(df.index))
    data["END_RANGE"].append(rd_range[-1])

df_synthesis = pd.DataFrame(data)
df_synthesis.to_csv('so.csv',  index=False) # encoding='utf-8',

print(df_synthesis)