#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calcRMSD.py: Calculate RMSD between distances

Created on ‎‎‎Mars 18 ‏‎15:54:12 2024

@author: Matilda J. Lindvall
"""

#Calculate rmsd between PyMOL distances
#and experimental distances
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

global df
global df_rmsd

exp_data = []
err = []

for i,v in Window.exp_dict.items():
    if v == '':
        pass
    else:
        exp_data.append(float(v))
        
for i,v in Window.SE_dict.items():
    if v == '':
        pass
    else:
        err.append(float(v))
    
df_rmsd = pd.DataFrame()
df_rmsd = df.copy()

new_df = df.iloc[:,2:]
diff_df = pd.DataFrame(columns=new_df.columns)

noe_lim = float(4) #NOE limit 4Å

for i, rows in new_df.iterrows():
    n=0
    row=[]
    for j in rows:
        if exp_data[n] == noe_lim:
            if j < noe_lim:
                diff = abs(j-exp_data[n])
            else:
                diff = 0
        else:
            diff = abs(j-exp_data[n])
            if diff > err[n]:
                diff = diff-err[n]
            else:
                diff = 0
        n+=1
        row.append(diff)

    diff_df.loc[len(diff_df)] = row

rmsd=[]

for i, r in diff_df.iterrows():
    w = np.sqrt(sum(np.power(r,2))/len(r))
    rmsd.append(w)

df_rmsd.loc[:,'RMSD'] = rmsd

df_min = df_rmsd.sort_values(by=['RMSD'])
print(df_min)

print("\nRMSD calculation succeeded!")