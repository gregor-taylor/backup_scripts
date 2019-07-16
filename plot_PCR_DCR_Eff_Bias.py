# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:21:45 2017
FOr use with data from the DCR v bias plots from DataGatherSNSPD
@author: G Taylor
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename
from matplotlib import style
style.use('fivethirtyeight_V2')

ip_pwr = 0.28e-6
atten = 73
wav = 1550
h = 6.626070040e-34
c = 2.99792458e8

root = tk.Tk()
photon_count_file = askopenfilename(initialdir="Z:\\", title="Choose a photon count file")
dark_count_file = askopenfilename(initialdir="Z:\\", title="Choose a dark count file")
root.withdraw()
#photon_count_files_dir="Z:\\User folders\\Gregor Taylor\\MIR work\\Scontel detectors\\545\\New attens\\2"
#dark_count_file = ""
DC_offset = 0
#DC
if dark_count_file == '':
    pass
else:
    with open(dark_count_file) as DC_csv:
        bias_list = []
        counts_list=[]
        read_DC_csv_file = csv.reader(DC_csv, delimiter=',')
        for index, row in enumerate(read_DC_csv_file):
            if len(row) >= 2:
                if index == 0:
                    pass
                elif index == 2:# not always neccessary
                    pass
                else:
                    bias_list.append(row[2])
                    counts_list.append(row[3])
        bias_array = np.asarray(bias_list, dtype='float')
        bias_array = bias_array*1e6 - DC_offset #uA
        DC_counts_array = np.asarray(counts_list, dtype='float')
        fig, ax1 = plt.subplots()
        ax1.semilogy(bias_array, DC_counts_array, 's', markersize=10)
    


#PC      
#file_names = [fn for fn in os.listdir(photon_count_files_dir)if any(fn.endswith(ext) for ext in 'txt')]
#for file_name in file_names:
#    full_path = photon_count_files_dir+'\\'+file_name
#    filter_stripped_name = file_name.split('_')[-1][:-4]
#    filter_name = re.sub('[^0-9]','', filter_stripped_name)
#    legends_list.append('PC')
with open(photon_count_file) as PC_csv:
    bias_list = []
    counts_list = []
    read_PC_csv = csv.reader(PC_csv, delimiter=',')
    for index,  row in enumerate(read_PC_csv):
        if len(row) >= 2:
            if index == 0:
                pass
            elif index == 2:# not always neccessary
                pass
            else:
                bias_list.append(row[2])
                counts_list.append(row[3])
    bias_array=np.asarray(bias_list, dtype='float')
    bias_array=bias_array*1e6 - DC_offset #convert to uA and take away offset.
    PC_counts_array=np.asarray(counts_list, dtype='float')
    ax1.semilogy(bias_array, PC_counts_array, 'o', markersize=10)

e_per_phot = h*(c/(float(wav)/1e9))
phot_per_sec = (float(ip_pwr)*(10**(-(float(atten)/10))))/e_per_phot
eff_arr = (PC_counts_array-DC_counts_array)/phot_per_sec
#ax2 = ax1.twinx()
#ax2.plot(bias_array, eff_arr, 'ro', markersize=3)
ax1.set_ylabel('Counts (CPS)')
ax1.set_xlabel('Bias ($\mathrm{\mu}$A)')
plt.title('Counts vs Bias')
ax1.legend(['DCR', 'PCR'], loc=2)
#ax2.legend(['Eff'], loc=3)
#plt.grid()
plt.show()
               
fig2, ax3=plt.subplots()
ax3.plot(bias_array, eff_arr, 'o', markersize=3)
ax3.set_ylabel('Efficiency')
ax3.set_xlabel('Bias ($\mathrm{\mu}$A)')
#plt.grid()
plt.show()
