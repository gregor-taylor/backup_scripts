# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:02:53 2018

Takes a comma seperated value where column one is always time and others are variable. Plots the other cols against time.

@author: 0901754T
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter import simpledialog
except ImportError:
    from Tkinter import *
    import ttk
    from tkFileDialog import askopenfilename 
    import tkSimpleDialog as simpledialog


#GUI
class Window(Frame):
    def __init__(self, master=None):
        #super here?
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
    def init_window(self):
        self.master.title("Choose what to plot")
        self.pack(fill=BOTH, expand=1)
        pall_button = ttk.Button(self, text='Plot all', command=lambda: self.plot_what('plot_all'))
        amb_pwr_button = ttk.Button(self, text='Plot ambient temperature and power', command=lambda: self.plot_what('ambient_v_pwr'))
        cryo_pwr_button = ttk.Button(self, text='Plot cryostat temperature and power', command=lambda: self.plot_what('cryo_v_pwr'))
        pwr_button = ttk.Button(self, text='Plot power only', command=lambda: self.plot_what('pwr_only'))
        two_pwr = ttk.Button(self, text='Plot two powers', command=lambda: self.plot_what('two_pwr'))
        pwr_diff = ttk.Button(self, text='Plot power difference', command=lambda: self.plot_what('pwr_diff'))
        
        pall_button.pack(pady=5)
        amb_pwr_button.pack(pady=5)
        cryo_pwr_button.pack(pady=5)
        pwr_button.pack(pady=5)
        two_pwr.pack(pady=5)
        pwr_diff.pack(pady=5)
        
    def plot_what(self, string):
        global plot_type
        plot_type = string
        root.destroy()

root=Tk()
root.geometry("300x250")
filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
app=Window(root)
root.mainloop()


'''
OLD
#Select plot type, choose from:
#plot_all, ambient_v_pwr, cryo_v_pwr, pwr_only
plot_types = {1: 'plot_all', 
              2: 'ambient_v_pwr', 
              3: 'cryo_v_pwr',
              4: 'pwr_only'
              }

root = tk.Tk()
root.withdraw()
filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
plot_type_int = simpledialog.askinteger('Select a plot type', 'Select plot type (enter integer):\n 1: Plot all \n 2: Plot ambient temperature and power \n 3: Plot cryostat temperature and power \n 4: Plot power only', parent=root)
plot_type = plot_types[plot_type_int] 
root.destroy()
'''

titles_list = []
col_dict={}
with open(filename) as csv_file:
    read_csv = csv.reader(csv_file, delimiter=',')
    for index, row in enumerate(read_csv):
        if len(row)>0:
            if index==0:
                for i in row:
                    titles_list.append(i)
                number_cols = len(titles_list)
                for i in range(number_cols):
                    col_dict[i]=[]
            else:
                for i in range(number_cols):
                    col_dict[i].append(row[i])
#convert to arrays
time_arr = np.asarray(col_dict[0], dtype='float')
arrays_dict ={}
for i in range(number_cols):
    if i == 0:
        pass
    else:
        arrays_dict[i]=np.asarray(col_dict[i], dtype='float')


if plot_type == 'plot_all':
#Use for generic plot legend generation       
    legends_list = []
    for i, j in enumerate(titles_list):
        if i == 0:
            pass
        else:
            legends_list.append(j)
            plt.plot(time_arr, arrays_dict[i])
    plt.legend(legends_list)  

#AMBIENT TEMP vs POWER
if plot_type == 'ambient_v_pwr':
    if len(arrays_dict) > 3:
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Voltage (V)')
        ax1.plot(time_arr, arrays_dict[4],'b-', markersize=2)
        ax1.plot(time_arr, arrays_dict[5],'r-', markersize=2)
        ax1.legend(['V1', 'V2'])

        ax2=ax1.twinx()
        ax2.set_ylabel('Power (W)')
        ax2.plot(time_arr, arrays_dict[6],'g-',markersize=2)
        ax2.legend(['Power(W)'])
    else:
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Voltage (V)')
        ax1.plot(time_arr, arrays_dict[1],'b-', markersize=2)
        ax1.plot(time_arr, arrays_dict[2],'r-', markersize=2)
        ax1.legend(['V1', 'V2'])

        ax2=ax1.twinx()
        ax2.set_ylabel('Power (W)')
        ax2.plot(time_arr, arrays_dict[3],'g-',markersize=2)
        ax2.legend(['Power(W)'])

#CRYO_TEMP vs POWER
if plot_type == 'cryo_v_pwr':
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Temp (K)')
    ax1.plot(time_arr, arrays_dict[1],'b-', markersize=2)
    ax1.plot(time_arr, arrays_dict[3],'r-', markersize=2)
    ax1.legend(['T1', 'T2'])

    ax2=ax1.twinx()
    ax2.set_ylabel('Power (W)')
    ax2.plot(time_arr, arrays_dict[6],'g-',markersize=2)
    ax2.plot(time_arr, arrays_dict[7], '-')
    ax2.legend(['Power(W)'])

#Power only
if plot_type == 'pwr_only':
    fig, ax = plt.subplots()
    if len(arrays_dict) > 3:
        ax.plot(time_arr, arrays_dict[6], 'g-')
    else:
        ax.plot(time_arr, arrays_dict[3], 'g-')
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Power(W)')

if plot_type =='two_pwr':
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Power_1 (W)')
    ax1.plot(time_arr, arrays_dict[6],'b-', markersize=2)
    ax1.legend(['Power_1(W)'])

    ax2=ax1.twinx()
    ax2.set_ylabel('Power_2 (W)')
    ax2.plot(time_arr, arrays_dict[7],'g-',markersize=2)
    ax2.legend(['Power_2(W)'])

if plot_type == 'pwr_diff':
    diff_arr=arrays_dict[7]-arrays_dict[6]
    pwr_1_av = np.mean(arrays_dict[7])
    loss=10*np.log10(arrays_dict[6]/arrays_dict[7])
    pwr_1_cond=abs(arrays_dict[7]-pwr_1_av)
    pwr_1_pc=(pwr_1_cond/pwr_1_av)

    pwr_2_av = np.mean(arrays_dict[6])
    pwr_2_cond=abs(arrays_dict[6]-pwr_2_av)
    pwr_2_pc=(pwr_2_cond/pwr_2_av)

    diff_pc=abs(pwr_1_pc-pwr_2_pc)

    fig, ax = plt.subplots()
    ax.plot(time_arr, pwr_1_pc, 'g-')
    ax.plot(time_arr, pwr_2_pc, 'b-')
    ax.plot(time_arr, diff_pc, 'r-')
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Difference to average (%)')
    ax.legend(['Pwr_1', 'Pwr_2', 'Diff'])
    
    fig2, ax2 = plt.subplots()
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Temp (K)')
    ax2.plot(time_arr, arrays_dict[1],'b-', markersize=2)
    ax2.plot(time_arr, arrays_dict[3],'r-', markersize=2)
    ax2.legend(['T1', 'T2'])

    ax3=ax2.twinx()
    ax3.set_ylabel('Power (W)')
    ax3.plot(time_arr, arrays_dict[6],'g-',markersize=2)
    ax3.legend(['Power(W)'])

    fig3, ax4 = plt.subplots()
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Voltage (V)')
    ax4.plot(time_arr, arrays_dict[4],'b-', markersize=2)
    ax4.plot(time_arr, arrays_dict[5],'r-', markersize=2)
    ax4.legend(['V1', 'V2'])

    ax5=ax4.twinx()
    ax5.set_ylabel('Power (W)')
    ax5.plot(time_arr, arrays_dict[6],'g-',markersize=2)
    ax5.legend(['Power(W)'])

    fig4, ax6 = plt.subplots()
    ax6.plot(time_arr, loss, 'g-')
    ax6.set_ylabel('Loss (dB)')
    ax6.set_xlabel('Time (s)')
    ax7=ax6.twinx()
    ax7.plot(time_arr, arrays_dict[1],'b-', markersize=2)
    ax7.plot(time_arr, arrays_dict[3],'r-', markersize=2)
    ax7.set_ylabel('Tempt (K)')

plt.grid()
plt.show()

