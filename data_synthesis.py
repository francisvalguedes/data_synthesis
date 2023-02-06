import glob
import pandas as pd
# import re
from datetime import datetime, timedelta
import numpy as np
import os

def dellfiles(file):
    py_files = glob.glob(file)
    err = 0
    for py_file in py_files:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{e.strerror}")
            err = e.strerror
    return err

satcat_db_ok = False
print('Downloading Celestrak satcat file')
try:
    satcat_df = pd.read_csv('satcat.csv')
    satcat_db_ok = True
    print('Readed Celestrak satcat file')
except:
    satcat_db_ok = False
    print('satcat file error')

txt_files = glob.glob('trajectory/*.trn')
# print(txt_files)
dellfiles('output/*.trn')

data = {'NORAD_CAT_ID':[], 'OBJECT_NAME':[], "RCS":[], "H0":[], "RANGE_H0":[],"MIN_RANGE_H":[],"MIN_RANGE_PT":[],
                    "MIN_RANGE":[],"END_H":[], "END_PT":[], "END_RANGE":[] }


print('Reading trajectory files for summary')
for file_name in txt_files:
    #print(file_name)
    df = pd.read_csv(file_name,skiprows=[0,1], header=None)
    #df.columns = ['ENU_E','ENU_N','ENU_U']
    df.to_csv( 'output' + file_name.split('trajectory')[1], index=False, header=[str(len(df.index)-1),'1000','1'],float_format="%.3f")
    
    if file_name.find('-') != -1:
        info = file_name.split('-')[1].split('_obj_')
    else:
        info = file_name.split(os.sep)[1].split('_obj_')

    datetimestr = info[0]
    norad_cat_id = info[1].split('_')[0]
    datetime_object = datetime.strptime(datetimestr, '%Y%m%d_%H%M%S') + timedelta(seconds=1)
    # print(datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    # print(norad_cat_id)
    rd_range = 0.001*np.linalg.norm(df,axis=1)
    min_index = np.argmin(rd_range)
    min_rd_range = rd_range[min_index]
    datetime_object_min = datetime_object + timedelta(seconds=int(min_index))

    obj_name = ''
    rcs = 0.0
    if satcat_db_ok:
        index_satcat = satcat_df.loc[satcat_df['NORAD_CAT_ID']==int(norad_cat_id)].index
        obj_name = satcat_df.loc[index_satcat, 'OBJECT_NAME'].to_string(index=False)
        if satcat_df.loc[index_satcat, 'RCS'].empty :
            rcs = 0.0
        else:
            rcs = float(satcat_df.loc[index_satcat, 'RCS'] )
 
    data["NORAD_CAT_ID"].append(norad_cat_id)
    data["OBJECT_NAME"].append(obj_name)
    data["RCS"].append(rcs)
    data["H0"].append(datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    data["RANGE_H0"].append(rd_range[0])
    data["MIN_RANGE_H"].append(datetime_object_min.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    data["MIN_RANGE_PT"].append(min_index)
    data["MIN_RANGE"].append(min_rd_range)
    data["END_H"].append((datetime_object + timedelta(seconds= len(df.index))).strftime("%Y-%m-%dT%H:%M:%S.%f"))
    data["END_PT"].append( len(df.index))
    data["END_RANGE"].append(rd_range[-1])

print('Writing summary')
df_synthesis = pd.DataFrame(data)
df_synthesis.to_csv('output/summary.csv',  index=False) # encoding='utf-8',

print(df_synthesis)
print('End')