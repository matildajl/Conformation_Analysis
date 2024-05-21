#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calc_dist.py: Calculate distance between atoms in PyMOL 

Created on ‎Mars ‎14 ‎‏‎10:01:27 2024

@author: Matilda J. Lindvall
"""

#Calculate distances and store them in a dataframe df
from pymol import cmd
import pandas as pd

global df

phi = Window.phi.split(',')
psi = Window.psi.split(',')

if Window.res_dict[2,1] == None:
    res1 = f'{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'
else:
    res1 = f'{Window.res_dict[2,1]}/{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,1]}/{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'

dst_list = []

a = list(Window.dist_dict.values())

a_lst = ['phi', 'psi']
for i in range(0, len(a), 2): 
    x = i 
    b = a[x:x+2]
    my_string = "/".join(str(element) for element in b)
    a_lst.append(my_string)

df = pd.DataFrame(columns=a_lst)

for a1 in range(int(phi[0]),int(phi[1])+int(phi[2]),int(phi[2])):
    cmd.set_dihedral(res1+f'/{Window.dihAngle[1,1]}', res1+f'/{Window.dihAngle[1,2]}',
                     res2+f'/{Window.dihAngle[1,3]}', res2+f'/{Window.dihAngle[1,4]}', a1)
     
    for a2 in range(int(psi[0]),int(psi[1])+int(psi[2]),int(psi[2])):
        cmd.set_dihedral(res1+f'/{Window.dihAngle[2,1]}', res2+f'/{Window.dihAngle[2,2]}',
                         res2+f'/{Window.dihAngle[2,3]}', res2+f'/{Window.dihAngle[2,4]}', a2)
        row=[]
        row.append(a1)
        row.append(a2)
         
        for i in list(Window.dist_dict.keys())[::2]:
            dst = cmd.distance('tmp', res1+f'/{Window.dist_dict[i[0],1]}',
                               res2+f'/{Window.dist_dict[i[0],2]}')

            row.append(dst)
         
        df.loc[len(df)] = row

print("\nCalculation is done!")
