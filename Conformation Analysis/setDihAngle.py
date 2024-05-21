#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setDihAngle.py: Set the dihedral angle to a chosen value

Created on ‎‎‎April 9 ‏‎13:40:11 2024

@author: Matilda J. Lindvall
"""

#Set dihedral angle manually
from pymol import cmd

if Window.res_dict[2,1] == None:
    res1 = f'{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'
else:
    res1 = f'{Window.res_dict[2,1]}/{Window.res_dict[2,2]}`{Window.res_dict[2,3]}'
    res2 = f'{Window.res_dict[3,1]}/{Window.res_dict[3,2]}`{Window.res_dict[3,3]}'

choice = Window.choice

ang = None

if choice == 1:
    for i in range(1,5):
        if Window.man_dict[(8,i)] == 'res1':
           Window.man_dict[(8,i)] = res1

        elif Window.man_dict[(8,i)] == 'res2':
           Window.man_dict[(8,i)] = res2
       
    ang = Window.ang_set
    cmd.set_dihedral(Window.man_dict[(8,1)]+f'/{Window.man_dict[(9,1)]}',
                     Window.man_dict[(8,2)]+f'/{Window.man_dict[(9,2)]}',
                     Window.man_dict[(8,3)]+f'/{Window.man_dict[(9,3)]}',
                     Window.man_dict[(8,4)]+f'/{Window.man_dict[(9,4)]}', ang)

elif choice == 2:
    ang = Window.phi_change
    cmd.set_dihedral(res1+f'/{Window.dihAngle[1,1]}', res1+f'/{Window.dihAngle[1,2]}',
                     res2+f'/{Window.dihAngle[1,3]}', res2+f'/{Window.dihAngle[1,4]}', ang)
elif choice == 3:
    ang = Window.psi_change
    cmd.set_dihedral(res1+f'/{Window.dihAngle[2,1]}', res2+f'/{Window.dihAngle[2,2]}',
                     res2+f'/{Window.dihAngle[2,3]}', res2+f'/{Window.dihAngle[2,4]}', ang)

print("\nThe dihedral angle has been changed to "+f'{ang}\N{DEGREE SIGN}')