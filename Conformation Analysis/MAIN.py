#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py: GUI for the program 

Created on ‎‎‎Mars 13 ‏‎19:25:47 2024

@author: Matilda J. Lindvall
"""

#Import modules
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askyesno
from functools import partial
from tkinter import messagebox
import os.path
import os
import pandas as pd
import threading
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


#Main window
class Window:
    #Global variables
    global df
    global df_rmsd
    global pdbData
    global counter
    df = {}
    df_rmsd = pd.DataFrame()
    counter = 1
    pdbPath = ''
    savePath = ''
    dist_dict = {}
    dihAngle = {}
    res_dict = {}
    exp_dict = {}
    SE_dict = {}
    man_dict = {}
    phi = ''
    psi = ''
    phi_set = ''
    psi_set = ''
    choice = 0
    phi_change = None
    psi_change = None
    ang_set = None
    
    def __init__(self, master):        
        #Widget
        title = Label(master, text="Conformation Analysis",
                      bg = bgC,
                      fg = textC,
                      font=(mainFont, 20))
        
        btn_tut = Button(master, text='Open tutorial pdf',
                         bg = brown,
                         fg = textC,
                         activeforeground = textC,
                         activebackground = beige,
                         width=17,
                         font=(btnFont, 12),
                         command = self.open_tut)        

        btn_data = Button(master, text='Load PDB',
                          bg = blue,
                          fg = textC,
                          activeforeground = textC,
                          activebackground = green,
                          font=(btnFont, 14),
                          width=15,
                          command = self.load_pdb)
        
        btn_res = Button(master, text='Choose residues',
                                font=(btnFont, 14),
                                bg=blue,
                                fg=textC,
                                activebackground=green,
                                activeforeground=textC,
                                width=15,
                                command=self.res)
        
        btn_man = Button(master, text='Change Manually',
                          bg = blue,
                          fg = textC,
                          activeforeground = textC,
                          activebackground = green,
                          font=(btnFont, 14),
                          width=15,
                          command = self.control_pymol)
       
        btn_dist = Button(master, text='Analysis',
                          bg = blue,
                          fg = textC,
                          activeforeground = textC,
                          activebackground = green,
                          font=(btnFont, 14),
                          width=15,
                          command = self.analysis)

        title.grid(row=0, column=0, columnspan=2, sticky='ns')
        btn_tut.grid(row=1, column=0, columnspan=2, padx=15, sticky='n')  
        btn_data.grid(row=2, column=0, columnspan=2, sticky='n')
        btn_res.grid(row=3, column=0, columnspan=2, sticky='n')
        btn_man.grid(row=4, column=0, sticky='n')
        btn_dist.grid(row=4, column=1, sticky='n')
        
    def open_tut(self):
        try:
            os.startfile('ConformationAnalysisTutorial.pdf')
        except:
            messagebox.showerror(title='Error opening file', message='Could not open the tutorial!')
    
    def load_pdb(self):
        self.load_pdb = PDBWindow()
    
    def res(self):
        if Window.pdbPath == '':
            messagebox.showerror(title='No PDB file', message='You must load a PDB file!')
        else:
            self.res = ResTable()
        
    def control_pymol(self):
        if Window.pdbPath == '':
            messagebox.showerror(title='No PDB file', message='You must load a PDB file!')
        elif Window.res_dict == {}:
            messagebox.showerror(title='No residues', message='You must enter the residues!')
        else:
            self.control_pymol = ConPymol()
    
    def analysis(self):
        if Window.pdbPath == '':
            messagebox.showerror(title='No PDB file', message='You must load a PDB file!')
        elif Window.res_dict == {}:
            messagebox.showerror(title='No residues', message='You must enter the residues!')
        else:
            self.analysis = Analysis()

#Window when loading the PDB file
class PDBWindow:
    def __init__(self):
        global counter
        
        if counter < 2:
            #Creating the grid
            data_win = Toplevel(background=bgC)
            data_win.rowconfigure(0, weight=1)
            data_win.rowconfigure(1, weight=1)
            data_win.rowconfigure(2, weight=1)
            data_win.columnconfigure(0, weight=1)            
            data_win.title('Load PDB')
            data_win.geometry("300x200")
            data_win.resizable(False, False)

            self.pdbPath = StringVar()
            
            self.print_stored_data() #Print data from previous input
            
            #Widgets
            pdbLabel = Label(data_win, text='Enter the PDB file',
                              font=(mainFont, 14),
                              bg=bgC,
                              fg=textC)
            
            entry_path = Entry(data_win, textvariable=self.pdbPath,
                               width=20,
                               font=(btnFont, 12))
            
            browsebtn = Button(data_win, text = "Browse",
                                font=(btnFont, 12),
                                bg=blue,
                                fg=textC,
                                activebackground=green,
                                activeforeground=textC,
                               command= lambda:self.browsefunc(entry_path))
            
            sbmitbtn = Button(data_win, text = "Submit",
                              font=(btnFont, 12),
                              bg=blue,
                              fg=textC,
                              activebackground=green,
                              activeforeground=textC,
                              command= lambda:self.submit(data_win))
            
            #Widgets position
            pdbLabel.grid(row=0, column=0,  pady=10, sticky='nsew')
            entry_path.grid(row=1, column=0, pady=10, padx=15, sticky='e')
            browsebtn.grid(row=1, column=0, pady=10, padx=50, sticky='w')
            sbmitbtn.grid(row=2,  column=0, pady =10)

            counter += 1 
            
            data_win.protocol("WM_DELETE_WINDOW", lambda:self.confirm(data_win))
                
    def submit(self, data_win):
        global counter
        
        if self.pdbPath.get() == '':
            messagebox.showerror(title='No file',
                                 message='You must enter a file \nbefore submitting!' )
        elif os.path.isfile(self.pdbPath.get()):
            try:
                Window.pdbPath = self.pdbPath.get() #Save the input
                exec(open("pdbReader.py", encoding="utf8").read()) #Read the PDB file
                counter = 1
                data_win.destroy()
            except:
                messagebox.showerror(title='File not found',
                                 message='The file could not be found!')
                raise
        else:
            messagebox.showerror(title='File not found',
                                 message='The file could not be found!')
            raise
        
    def print_stored_data(self):
        self.pdbPath.set(Window.pdbPath)
        
    def browsefunc(self, entry):
        filename = filedialog.askopenfilename(filetypes=(("PDB files","*.pdb"),
                                                         ("All files","*.*")))
        if filename:
            entry.delete(0, END)
            entry.insert(END, filename)
    
    def confirm(self, data_win):
        global counter
        
        ans = askyesno(title='Exit', message='Do you want to exit without saving?')
        
        if ans:
            counter = 1
            data_win.destroy()


#Window for choosing the residues
class ResTable:
    def __init__(self):
        global counter
        global pdbData
        
        self.pdbData = pdbData
        
        res = list(self.pdbData['resname'].unique())
        resid = list(self.pdbData['resid'].unique())
        chain =list(self.pdbData['chain'].unique())
                
        if counter < 2:
            #Creating the grid and window
            resWin = Toplevel(background=bgC)
            resWin.geometry('400x300')
            resWin.rowconfigure(0, weight=1)
            resWin.rowconfigure(1, weight=1)
            resWin.rowconfigure(2, weight=1)
            resWin.rowconfigure(3, weight=1)
            resWin.rowconfigure(4, weight=1)
            resWin.columnconfigure(0, weight=1)
            resWin.columnconfigure(1, weight=1)
            resWin.columnconfigure(2, weight=1)
            resWin.columnconfigure(3, weight=1)
            resWin.resizable(False, False)
            
            heading=['Chain', 'Res', 'ResID']
            resname=['Res1:', 'Res2:']
            
            #Widgets
            title = Label(resWin, text='Enter the residues',
                          font=(mainFont, 14),
                          bg=bgC,
                          fg=textC)
            title.grid(row=0, column=0, columnspan=4)
            
            for j in range(0,3):
                labelH = Label(resWin, text=heading[j], font=(btnFont, 14),
                              bg=bgC,
                              fg=textC)
                labelH.grid(row=1, column=j+1)
            
            for j in range(2,4):
                label = Label(resWin, text=resname[j-2], font=(btnFont, 14),
                              bg=bgC,
                              fg=textC)
                label.grid(row=j, column=0)
            
            for i in range(2,4):
                j=1
                self.table_pos = StringVar(resWin, name=f'A{(i,j)}')
                self.print_stored_data(resWin)
                dropdown_chain = OptionMenu(resWin, self.table_pos, *chain,
                                      command=partial(self.fetch, (i,j)))
                dropdown_chain.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=4,
                                          font=(btnFont, 14))
                dropdown_chain.grid(row=i, column=j)
            
            for i in range(2,4):
                j=2
                self.table_pos = StringVar(resWin, name=f'B{(i,j)}')
                self.print_stored_data(resWin)
                dropdown_res = OptionMenu(resWin, self.table_pos, *res,
                                      command=partial(self.fetch, (i,j)))
                dropdown_res.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=4,
                                          font=(btnFont, 14))
                dropdown_res.grid(row=i, column=j)
                    
            for i in range(2,4):
                j=3
                self.table_pos = StringVar(resWin, name=f'C{(i,j)}')
                self.print_stored_data(resWin)
                dropdown_resid = OptionMenu(resWin, self.table_pos, *resid,
                                      command=partial(self.fetch, (i,j)))
                dropdown_resid.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=4,
                                          font=(btnFont, 14))
                dropdown_resid.grid(row=i, column=j)          
            
            savebtn = Button(resWin, text='Close',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.close(resWin))
            savebtn.grid(row=4, column=3, pady=20)
            
            helpbtn = Button(resWin, text='Help',
                             bg=brown,
                             fg=textC,
                             activebackground=beige,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=self.help_info)
            helpbtn.grid(row=4, column=1, pady=20)
            
            counter += 1
            
            resWin.protocol("WM_DELETE_WINDOW", lambda:self.confirm(resWin))
        
    def close(self, window):
        global counter
        counter = 1
        self.sort(Window.res_dict)
        window.destroy()
        
    def confirm(self, window):
        global counter
        counter = 1
        window.destroy()
    
    def fetch(self, ind, value):
        Window.res_dict[ind] = value
        
    def sort(self, dictionary):
        keys = list(dictionary.keys())
        keys.sort()
        Window.res_dict = {i: dictionary[i] for i in keys}
    
    def print_stored_data(self, window):
        if Window.res_dict == {}:
            pass
        else:
            for i in Window.res_dict.keys():
                window.setvar(name = f'A{i}', value=Window.res_dict[i])
                window.setvar(name = f'B{i}', value=Window.res_dict[i])
                window.setvar(name = f'C{i}', value=Window.res_dict[i])
                
    def help_info(self):
        messagebox.showinfo("Define the residues",
                            "Here you define the residues for PyMOL.\n\
You need to fill in both res1 and res2!") 


#Window for manually changes
class ConPymol:
    def __init__(self):
        global counter
        global pdbData
        
        self.pdbData = pdbData
        
        atoms = list(self.pdbData['name'].unique())
        atoms.append('')
        res = ['res1', 'res2', '']
        
        phi = chr(981)
        psi = chr(968)
        theta = chr(952)
        
        self.ang_set = StringVar()
        self.phi_change = StringVar()
        self.psi_change = StringVar()
        
        self.choice = 0
        
        lst = ['Atom', 'Atom', 'Atom', 'Atom']
        
        if counter < 2:
            CpymWin = Toplevel(background=bgC)
            CpymWin.geometry('500x675')
            CpymWin.rowconfigure(0, weight=1)
            CpymWin.rowconfigure(1, weight=1)
            CpymWin.rowconfigure(2, weight=1)
            CpymWin.rowconfigure(3, weight=1)
            CpymWin.rowconfigure(4, weight=1)
            CpymWin.rowconfigure(5, weight=1)
            CpymWin.rowconfigure(6, weight=1)
            CpymWin.rowconfigure(7, weight=1)
            CpymWin.rowconfigure(8, weight=1)
            CpymWin.rowconfigure(9, weight=1)
            CpymWin.rowconfigure(10, weight=1)
            CpymWin.rowconfigure(11, weight=1)
            CpymWin.rowconfigure(12, weight=1)
            CpymWin.rowconfigure(13, weight=1)
            CpymWin.rowconfigure(14, weight=1)
            CpymWin.columnconfigure(0, weight=1)
            CpymWin.columnconfigure(1, weight=1)
            CpymWin.columnconfigure(2, weight=1)
            CpymWin.columnconfigure(3, weight=1)
            CpymWin.columnconfigure(4, weight=1)
            CpymWin.columnconfigure(5, weight=1)
            CpymWin.resizable(False, False)
            
            #Widgets
            title = Label(CpymWin, text='Change Manually in Pymol',
                              font=(mainFont, 16),
                              bg=bgC,
                              fg=textC)
            
            restorebtn = Button(CpymWin, text='Restore conformation',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=17,
                             font=(btnFont, 14),
                             command=self.restore)
            
            title_dist = Label(CpymWin, text='Get the distance between two atoms',
                              font=(btnFont, 14),
                              bg=bgC,
                              fg=textC)
            
            label_res1 = Label(CpymWin, text='Res',
                               font=(btnFont, 12),
                               bg=bgC,
                               fg=textC)
            
            label_atom = Label(CpymWin, text='Atom',
                               font=(btnFont, 12),
                               bg=bgC,
                               fg=textC)
            
            label_atom1 = Label(CpymWin, text='Atom1',
                               font=(btnFont, 12),
                               bg=bgC,
                               fg=textC)
            
            label_atom2 = Label(CpymWin, text='Atom2',
                               font=(btnFont, 12),
                               bg=bgC,
                               fg=textC)
            
            for i in range(4,6):
                for j in range(1,2):
                    self.table_pos = StringVar(CpymWin, name=f'H{(i,j)}')
                    dropdown_chain = OptionMenu(CpymWin, self.table_pos, *res,
                                                command=partial(self.fetch, (i,j)))
                    dropdown_chain.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=3,
                                          font=(btnFont, 12))
                    dropdown_chain.grid(row=i, column=j)
                    
                for k in range(2,3):
                    self.table_pos = StringVar(CpymWin, name=f'I{(i,j)}')
                    dropdown_chain = OptionMenu(CpymWin, self.table_pos, *atoms,
                                                command=partial(self.fetch, (i,k)))
                    dropdown_chain.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=3,
                                          font=(btnFont, 12))
                    dropdown_chain.grid(row=i, column=k)
                
            getbtn1 = Button(CpymWin, text='Get',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=self.get_dist)
            
            title_getDH = Label(CpymWin, text='Get or set a dihedral angle',
                              font=(btnFont, 14),
                              bg=bgC,
                              fg=textC)
            
            labelAng = Label(CpymWin, text=theta+':', font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
            
            labelAng2 = Label(CpymWin, text=theta+':', font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
            
            for i in range(1,5):
                self.table_pos = StringVar(CpymWin, name=f'J{(8,i)}')
                dropdown_chain = OptionMenu(CpymWin, self.table_pos, *res,
                                            command=partial(self.fetch, (8,i)))
                dropdown_chain.config(bg=blue,
                                      fg=textC,
                                      activebackground=green,
                                      activeforeground=textC,
                                      width=3,
                                      font=(btnFont, 12))
                dropdown_chain.grid(row=8, column=i)
            
            for i in range(1,5):
                hlabel = Label(CpymWin, text=lst[i-1], font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
                hlabel.grid(row=7, column=i)
                               
            for j in range(1,5):
                self.table_pos = StringVar(CpymWin, name=f'J{(9,j)}')
                dropdown_chain = OptionMenu(CpymWin, self.table_pos, *atoms,
                                            command=partial(self.fetch, (9,j)))
                dropdown_chain.config(bg=blue,
                                      fg=textC,
                                      activebackground=green,
                                      activeforeground=textC,
                                      width=3,
                                      font=(btnFont, 12))
                dropdown_chain.grid(row=9, column=j)
            
            getbtn2 = Button(CpymWin, text='Get',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=self.getDihAng)
            
            ang_entry = Entry(CpymWin, textvariable = self.ang_set,
                              font=(btnFont, 12), width=5) 
            
            phi_label = Label(CpymWin, text=phi+':', font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
            
            psi_label = Label(CpymWin, text=psi+':', font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
            
            phi_entry = Entry(CpymWin, textvariable = self.phi_change,
                              font=(btnFont, 12), width=5)
            
            psi_entry = Entry(CpymWin, textvariable = self.psi_change,
                              font=(btnFont, 12), width=5)
            
            setbtn1 = Button(CpymWin, text='Set',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.set_angle(1))
            
            setbtn2 = Button(CpymWin, text='Set',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.set_angle(2))
            
            setbtn3 = Button(CpymWin, text='Set',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.set_angle(3))
            
            savebtn = Button(CpymWin, text='Close',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.close(CpymWin))
                
            helpbtn = Button(CpymWin, text='Help',
                             bg=brown,
                             fg=textC,
                             activebackground=beige,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=self.help_info)
            
            title.grid(row=0, column=0, columnspan=7, pady=15, padx=10)
            restorebtn.grid(row=1, column=0, columnspan=7, pady=15)
            title_dist.grid(row=2, column=0, columnspan=5, pady=15, sticky='w', padx=10)
            label_res1.grid(row=3, column=1)
            label_atom.grid(row=3, column=2)
            label_atom1.grid(row=4, column=0)
            label_atom2.grid(row=5, column=0)
            getbtn1.grid(row=4, column=3, rowspan=2, columnspan=2)
            title_getDH.grid(row=6, column=0, columnspan=5, pady=10, sticky='w', padx=10)
            labelAng.grid(row=8, column=0, padx =10, pady=10, rowspan=2)
            labelAng2.grid(row=10, column=0, padx=10, pady=5)
            getbtn2.grid(row=8, column=5, rowspan=2, padx=5)
            ang_entry.grid(row=10, column=1, sticky='nw', pady=10)
            phi_label.grid(row=11, column=0, pady=5)
            psi_label.grid(row=12, column=0, pady=5)
            phi_entry.grid(row=11, column=1, pady=5, sticky='w')
            psi_entry.grid(row=12, column=1, pady=5, sticky='w')
            setbtn1.grid(row=10, column=2, pady=5)
            setbtn2.grid(row=11, column=2, pady=5)
            setbtn3.grid(row=12, column=2, pady=5)
            savebtn.grid(row=14, column=5, pady=20)
            helpbtn.grid(row=14, column=4, pady=20)
            
            counter += 1
            
            CpymWin.protocol("WM_DELETE_WINDOW", lambda:self.close(CpymWin))
            
    def restore(self):
        ans = messagebox.askquestion('Restore Structure',
                                     'Do you really want to restore it?\n All changes will be lost')
        if ans == True:
            try:
                exec(open("restoreStructure.py", encoding="utf8").read())
            except:
                raise
            
    def fetch(self, ind, value):
        Window.man_dict[ind] = value
    
    def close(self, window):
        global counter
        counter = 1
        window.destroy()
        
    def help_info(self):
        messagebox.showinfo("Manually",
                            "In this window you can get the distance between two atoms.\n\
You can also define a dihedral angle and get/set the angle.\nNote that φ and ψ need to be \
defined in another window") 
    
    def set_angle(self, choice):
        Window.phi_change = self.phi_change.get()
        Window.psi_change = self.psi_change.get()
        Window.ang_set = self.ang_set.get()
        Window.choice = choice
        try:
            exec(open("setDihAngle.py", encoding="utf8").read())
        except:
            messagebox.showerror(title='Problem with the data',
                                 message='There seems to be some problem with the data\n\
Control your input data!')
            raise
    
    def get_dist(self):
        try:
            exec(open("getDist.py", encoding="utf8").read())
        except:
            messagebox.showerror(title='Problem with the data',
                                 message='There seems to be some problem with the data!\n\
Control your input data!')
            raise
    
    def getDihAng(self):
        try:
            exec(open("getDihAngle.py", encoding="utf8").read())
        except:
            messagebox.showerror(title='Problem with the data',
                                 message='There seems to be some problem with the data!\n\
Control your input data!')
            raise


#Analysis window
class Analysis:    
    def __init__(self):
        global pdbData
        global counter
        
        self.widget = None
        self.toolbar = None
        
        if counter < 2:
            #Creating the grid and window
            atomsWin = Toplevel(background=bgC)
            atomsWin.geometry('900x600')
            
            topframe = Frame(atomsWin, bg=bgC, highlightbackground=green, highlightthickness=2)
            btmframe = Frame(atomsWin, bg=bgC, highlightbackground=green, highlightthickness=2)
            figframe = Frame(atomsWin, bg=bgC, highlightbackground=green, highlightthickness=2)
            toolframe = Frame(atomsWin, bg=bgC)
            
            atomsWin.rowconfigure(0, weight=1)
            atomsWin.rowconfigure(1, weight=1)
            atomsWin.rowconfigure(2, weight=1)
            atomsWin.rowconfigure(3, weight=1)
            atomsWin.rowconfigure(4, weight=1)
            atomsWin.rowconfigure(5, weight=1)
            atomsWin.rowconfigure(6, weight=1)
            atomsWin.rowconfigure(7, weight=1)
            atomsWin.rowconfigure(8, weight=1)
            atomsWin.rowconfigure(9, weight=1)
            atomsWin.rowconfigure(10, weight=1)
            atomsWin.rowconfigure(11, weight=1)
            atomsWin.rowconfigure(12, weight=1)
            atomsWin.columnconfigure(0, weight=2)
            atomsWin.columnconfigure(1, weight=2)
            atomsWin.columnconfigure(2, weight=2)
            atomsWin.columnconfigure(3, weight=2)
            atomsWin.columnconfigure(4, weight=2)
            atomsWin.columnconfigure(5, weight=5)
            atomsWin.columnconfigure(6, weight=5)
            atomsWin.columnconfigure(7, weight=5)
            atomsWin.resizable(False, False)
            
            topframe.grid(row=0, rowspan=5, columnspan=5, pady=5, padx=5,
                          ipady=5, sticky='nsew')
            btmframe.grid(row=5, rowspan=9, columnspan=5, pady=5, padx=5,
                          ipady=5, sticky='nsew')
            figframe.grid(row=0, rowspan=10, column=5, columnspan=3, padx=5,
                          pady=(5,0), sticky='nsew')
            toolframe.grid(row=10, column=5, columnspan=3, padx=5, pady=(0,5),
                           sticky='nsew')
            
            phi = chr(981)
            psi = chr(968)
            
            self.pdbData = pdbData
            atoms = list(self.pdbData['name'].unique())
            atoms.append('')
            
            ang=[phi, psi]
            
            self.phi = StringVar()
            self.psi = StringVar()
            
            self.print_stored_data_range()
            
            #Upper frame
            #Widgets
            title1 = Label(atomsWin, text='Define the dihedral angles',
                              font=(mainFont, 14),
                              bg=bgC,
                              fg=textC)
            title1.grid(row=0, column=0, columnspan=5, pady=15, padx=10)
            
            for j in range(0,2):
                label = Label(atomsWin, text=ang[j], font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
                label.grid(row=j+1, column=0)
            
            for i in range(1,3):
                for j in range(1,5):
                    self.table_pos = StringVar(atomsWin, name=f'D{(i,j)}')
                    self.print_stored_data(atomsWin)
                    dropdown_chain = OptionMenu(atomsWin, self.table_pos, *atoms,
                                          command=partial(self.fetch1, (i,j)))
                    dropdown_chain.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=5,
                                          font=(btnFont, 12))
                    dropdown_chain.grid(row=i, column=j)
                    
            
            phi_label = Label(atomsWin, text=phi+' range:', font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
            phi_label.grid(row=3, column=0, columnspan=2, pady=5)
            
            psi_label = Label(atomsWin, text=psi+' range:', font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
            psi_label.grid(row=4, column=0, columnspan=2, pady=5)
            
            phi_range = Entry(atomsWin, textvariable = self.phi,
                              font=(btnFont, 12), width=12)
            phi_range.grid(row=3, column=2, pady=5, columnspan=2, sticky='w')
            
            psi_range = Entry(atomsWin, textvariable = self.psi,
                              font=(btnFont, 12), width=12)
            psi_range.grid(row=4, column=2, pady=10, columnspan=2, sticky='w')
            
            setbtn1 = Button(atomsWin, text='Set',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.set1(atomsWin))
            setbtn1.grid(row=4, column=4, pady=10)
            
            #Lower frame
            self.table_height = 12

            resname = ['Res1', 'Res2', 'Exp', 'SE']
            
            self.table_pos = {}
            self.entry=[]
            
            #Widgets
            title2 = Label(atomsWin, text='Atoms for distance calculation',
                              font=(mainFont, 14),
                              bg=bgC,
                              fg=textC)
            title2.grid(row=5, column=0, columnspan=5, pady=15, padx=10)
            
            for j in range(0,4):
                label = Label(atomsWin, text=resname[j], font=(btnFont, 12),
                              bg=bgC,
                              fg=textC)
                label.grid(row=6, column=j+1)
            
            for i in range(7, self.table_height):
                for j in range(1,3):
                    self.table_pos = StringVar(atomsWin, name=f'{(i,j)}')
                    self.print_stored_data(atomsWin)
                    dropdown_chain = OptionMenu(atomsWin, self.table_pos, *atoms,
                                          command=partial(self.fetch2, (i,j)))
                    dropdown_chain.config(bg=blue,
                                          fg=textC,
                                          activebackground=green,
                                          activeforeground=textC,
                                          width=5,
                                          font=(btnFont, 12))
                    dropdown_chain.grid(row=i, column=j)
            
            for i in range(7, self.table_height):
                j=3
                self.table_pos = StringVar(atomsWin, name=f'E{(i,j)}')
                entry_exp = Entry(atomsWin, textvariable=self.table_pos,
                               width=10,
                               font=(btnFont, 12))

                entry_exp.grid(row=i, column=j, pady=5)
            
            for i in range(7, self.table_height):
                j=4
                self.table_pos = StringVar(atomsWin, name=f'F{(i,j)}')
                entry_SE = Entry(atomsWin, textvariable=self.table_pos,
                               width=10,
                               font=(btnFont, 12))

                entry_SE.grid(row=i, column=j, pady=5)
            
            setbtn2 = Button(atomsWin, text='Set',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=lambda:self.set2(atomsWin))
            setbtn2.grid(row=(self.table_height), column=2, columnspan=2, pady=20)
            
            distbtn = Button(atomsWin, text='Get dist',
                             bg=blue,
                             fg=textC,
                             activebackground=green,
                             activeforeground=textC,
                             width=8,
                             font=(btnFont, 12),
                             command=self.getDist)
            distbtn.grid(row=(self.table_height), column=3, columnspan=2, pady=20)
            
            btn_calc = Button(atomsWin, text='Calculate distances',
                          bg = brown,
                          fg = textC,
                          activeforeground = textC,
                          activebackground = beige,
                          width=17,
                          font=(btnFont, 12),
                          command=lambda: self.thread_it(self.calc_dist, atomsWin))
            
            btn_rmsd = Button(atomsWin, text='Calculate RMSD',
                          bg = brown,
                          fg = textC,
                          activeforeground = textC,
                          activebackground = beige,
                          width=17,
                          font=(btnFont, 12),
                          command = lambda:self.rmsd(figframe, toolframe))
            
            btn_save = Button(atomsWin, text='Save data',
                         bg = brown,
                         fg = textC,
                         activeforeground = textC,
                         activebackground = beige,
                         width=17,
                         font=(btnFont, 12),
                         command = self.save)
            
            btn_calc.grid(row=11, column=5, sticky='e')
            btn_rmsd.grid(row=11, column=6, sticky='e')
            btn_save.grid(row=12, column=5, sticky='e', pady=10)            
            
            helpbtn = Button(atomsWin, text='Help',
                             bg=brown,
                             fg=textC,
                             activebackground=beige,
                             activeforeground=textC,
                             width=17, 
                             font=(btnFont, 12),
                             command=self.help_info)
            helpbtn.grid(row=12, column=6, sticky='e', pady=10)

            
            counter += 1
            
            atomsWin.protocol("WM_DELETE_WINDOW", lambda:self.close(atomsWin))
    
    def fetch1(self, x, value):
        Window.dihAngle[x] = value
        
    def fetch2(self, x, value):
        Window.dist_dict[x] = value
        if Window.dist_dict[x] == '':
            del Window.dist_dict[x]
        
    def print_stored_data(self, window):
        if Window.dihAngle == {}:
            pass
        else:
            for i in Window.dihAngle.keys():
                window.setvar(name = f'D{i}', value=Window.dihAngle[i])
                
        if Window.dist_dict == {}:
            pass
        else:
            for i in Window.dist_dict.keys():
                window.setvar(name = f'{i}', value=Window.dist_dict[i])
    
    def print_stored_data_range(self):
        self.phi.set(Window.phi)
        self.psi.set(Window.psi)
    
    def sort(self, dictionary):
        keys = list(dictionary.keys())
        keys.sort()
        Window.dist_dict = {i: dictionary[i] for i in keys}
    
    def set1(self, window):
        Window.phi = self.phi.get()
        Window.psi = self.psi.get()
    
    def set2(self, window):
        self.sort(Window.dist_dict)
        for i in range(7, self.table_height):
            j=3
            value = window.getvar(name=f'E{(i,j)}')
            Window.exp_dict[(i,j)] = value
        
        for i in range(7, self.table_height):
            j=4
            value = window.getvar(name=f'F{(i,j)}')
            Window.SE_dict[(i,j)] = value
        
    def close(self, window):
        global counter
        counter = 1
        window.destroy()
        
    def help_info(self):
        messagebox.showinfo("Manually", "Define the dihedral angles φ and ψ and the interval (range) you want to look at.\
 The range must be in the form: start,stop,step.\n\nEnter the atoms and their experimental distances with error (SE).\
 Make sure to press 'set' when done!\n\nThe 'get distance' button will show you the selected distances in PyMOL.\n\n\
'Calculate distance' button will calculate all distances with all angles.\n'Calculate RMSD' will callculate RMSD\
 and create a heatmap.")
        
    def getDist(self):
        try:
            exec(open("getOnlyDist.py", encoding="utf8").read())
        except:
            messagebox.showerror(title='Problem with the data',
                                 message='There seems to be some problem with the data!\n\
Control the input!')
            raise
        
    def calc_dist(self):
        self.exc = None
        try:
            exec(open("calc_dist.py", encoding="utf8").read())
        except BaseException as e:
            self.exc = e
        
    def rmsd(self, window, frame):
        print("\nLoading...")
        try:
            exec(open("calcRMSD.py", encoding="utf8").read())
            self.plot(window, frame)
        except:
            messagebox.showerror(title='Problem with the data',
                                 message='There seems to be some problem with the data!\n\
Control the input!')
            raise
            print("\nRMSD calculation failed!")
    
    def thread_it(self, func, window):
        x = window.winfo_x()
        y = window.winfo_y()
        
        splash = Toplevel()
        splash.geometry("+%d+%d" % (x + 400, y + 200))
        splash_label = Label(splash, text='Calculating...', font=(mainFont, 14))
        splash_label.pack(pady=30, padx=30)
        splash.update()
        
        self.thread = threading.Thread(target=func)
        self.thread.start()
        self.thread.join()
        
        splash.destroy()
        
        if self.exc:
            messagebox.showerror(title='Problem with the data',
                                 message='There seems to be some problem with the data!\n\
Control the input!')
         
    def plot(self, window, frame):
        global df_rmsd
        
        if self.widget is not None:
            self.widget.destroy()
        if self.toolbar is not None:
            self.toolbar.destroy()
    
        fig = plt.figure(figsize=(3,3))
        hmap = df_rmsd.pivot(index="psi", columns="phi", values="RMSD")
        sns.color_palette("Spectral", as_cmap=True)
        plt.rcParams.update(plt.rcParamsDefault)
        ax = sns.heatmap(hmap, cmap="Spectral", annot=False)
        ax.invert_yaxis()
        plt.rcParams["text.usetex"] = True
        plt.rcParams.update({'font.size': 8})
        plt.ylabel(r'$\psi$')
        plt.xlabel(r'$\varphi$')
        plt.title('RMSD mapping')
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, window)
        
        self.toolbar = NavigationToolbar2Tk(canvas, frame)
        self.toolbar.children['!button4'].pack_forget()
        self.toolbar.children['!label'].pack_forget()
        self.toolbar.children['!label2'].pack_forget()

        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH, expand=1)    
        
    def save(self):
        global save_file
        files = [("Excel files", "*.xlsx"), ('All Files', '*.*')] 
        save_file = asksaveasfile(initialfile = 'Data.xlsx', defaultextension=".xlsx",
                                  filetypes = files)
        
        if save_file:
            df_rmsd.to_excel(save_file.name, index=False)

#Style
def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb                
             
bgC = _from_rgb((38,51,59))
green = _from_rgb((56,75,73))
blue = _from_rgb((94,125,120))
beige = _from_rgb((192,139,87))
brown = _from_rgb((153,91,54))
textC = "white"
mainFont = 'Cambria'
btnFont = 'Calibri'

#Run the program
root = Tk()
root.title("Conformation Analysis")
root.geometry("500x450")
root.configure(background=bgC)
root.resizable(False, False)
window = Window(root)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.columnconfigure(0, weight=1, uniform='a')
root.columnconfigure(1, weight=1, uniform='a')

root.mainloop()