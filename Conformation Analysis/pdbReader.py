#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdbReader.py: Extract the atoms from the pdb

Created on ‎April 22 ‏‎11:08:08 2024

@author: Matilda J. Lindvall
"""
#pdbreader extract data from the pdb
import pdbreader
import pandas as pd

global pdbData

pdb = pdbreader.read_pdb(Window.pdbPath)
try:
    pdbData = pd.DataFrame(pdb['HETATM'])
except KeyError:
    try:
        pdbData = pd.DataFrame(pdb['ATOM'])
    except:
        raise