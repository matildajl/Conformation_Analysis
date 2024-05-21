#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restoreStructure.py: Restore the structure to the original 

Created on ‎‎‎April 12 ‏‎14:23:15 2024

@author: Matilda J. Lindvall
"""
#Restore structure to original
from pymol import cmd

cmd.reinitialize() #Remove everything

cmd.load(Window.pdbPath) #Load the pdb

print("\nThe original structure is loaded!")
