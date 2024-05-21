#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getOnlyDist.py: Calculate distance between atoms in PyMOL 

Created on ‎‎‎April 17 ‏‎10:38:34 2024

@author: Matilda J. Lindvall
"""

#Print out the distances from the table
if Window.res_dict[2,1] == None:
    res1 = f'{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'
else:
    res1 = f'{Window.res_dict[2,1]}/{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,1]}/{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'

dst_list = []

a = list(Window.dist_dict.values())

a_lst = []
for i in range(0, len(a), 2): 
    x = i 
    b = a[x:x+2]
    my_string = "/".join(str(element) for element in b)
    a_lst.append(my_string)

df = pd.DataFrame(columns=a_lst)

row=[]

for i in list(Window.dist_dict.keys())[::2]:
    dst = cmd.distance('tmp', res1+f'/{Window.dist_dict[i[0],1]}',
                               res2+f'/{Window.dist_dict[i[0],2]}')
    row.append(dst)

df.loc[len(df)] = row
print('')
print(df)