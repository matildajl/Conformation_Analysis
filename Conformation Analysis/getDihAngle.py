#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getDihAngle.py: Get the dihedral angle in PyMOL

Created on ‎‎‎April 16 ‏‎10:50:56 2024

@author: Matilda J. Lindvall
"""

#Get dihedral angle
from pymol import cmd

if Window.res_dict[2,1] == None:
    res1 = f'{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'
else:
    res1 = f'{Window.res_dict[2,1]}/{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,1]}/{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'

for i in range(1,5):
    if Window.man_dict[(8,i)] == 'res1':
       Window.man_dict[(8,i)] = res1

    elif Window.man_dict[(8,i)] == 'res2':
       Window.man_dict[(8,i)] = res2

ang = cmd.get_dihedral(Window.man_dict[(8,1)]+f'/{Window.man_dict[(9,1)]}',
                       Window.man_dict[(8,2)]+f'/{Window.man_dict[(9,2)]}',
                        Window.man_dict[(8,3)]+f'/{Window.man_dict[(9,3)]}',
                       Window.man_dict[(8,4)]+f'/{Window.man_dict[(9,4)]}')

print(f'\nThe angle is {round(ang,3)}\N{DEGREE SIGN}')
