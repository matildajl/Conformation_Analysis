#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
installation_file.py: Install and import modules in PyMOL 

Created on ‎‎Mars 13 ‎‏‎19:25:47 2024

@author: Matilda J. Lindvall
"""
#Import modules
import subprocess
import sys

def install(package):
    try:
        __import__(package)
    except:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except:
            subprocess.run(['pip', 'install', package])
    finally:
        __import__(package)
        print(package, 'is installed and imported')
    
packages_to_install = ['pandas', 'subprocess', 'seaborn', 'matplotlib.pyplot', 'numpy',
                       'pdbreader', 'openpyxl']

print('\nRunning installation file...')

for package in packages_to_install:
    install(package)
    
print('\nInstallation is complete!')
