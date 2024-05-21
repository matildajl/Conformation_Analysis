#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getDist.py: Calculate distance between atoms in PyMOL 

Created on ‎‎April 16 ‏‎09:53:54 2024

@author: Matilda J. Lindvall
"""

#Get distance between two atoms
from pymol import cmd

if Window.res_dict[2,1] == None:
    res1 = f'{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'
else:
    res1 = f'{Window.res_dict[2,1]}/{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,1]}/{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'

if Window.man_dict[(4,1)] == 'res1':
   Window.man_dict[(4,1)] = res1

elif Window.man_dict[(4,1)] == 'res2':
   Window.man_dict[(4,1)] = res2
   
if Window.man_dict[(5,1)] == 'res1':
   Window.man_dict[(5,1)] = res1

elif Window.man_dict[(5,1)] == 'res2':
   Window.man_dict[(5,1)] = res2

dst = cmd.distance('tmp', Window.man_dict[(4,1)]+f'/{Window.man_dict[(4,2)]}',
                   Window.man_dict[(5,1)]+f'/{Window.man_dict[(5,2)]}')

print(f"\nThe distance is {round(dst, 3)} \u212B") #Å = \u212B
