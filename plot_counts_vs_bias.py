# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:21:45 2017
Takes photon counts for various ND filter strengths and plots them against bais current
@author: G Taylor
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename

#root = tk.Tk()
#photon_count_file = askopenfilename(initialdir="Z:\\", title="Choose a photon count file")
#dark_count_file = askopenfilename(initialdir="Z:\\", title="Choose a dark count file")
#root.withdraw()
photon_count_files_dir="Z:\\User folders\\Gregor Taylor\\MIR work\\Scontel detectors\\545\\New attens\\2"
dark_count_file = ""
legends_list = []
DC_offset = 0
#DC
if dark_count_file == '':
    pass
else:
    with open(dark_count_file) as DC_csv:
        bias_list = []
        counts_list=[]
        read_DC_csv_file = csv.reader(DC_csv, delimiter='\t')
        for row in read_DC_csv_file:
            if len(row) >= 2:
                bias_list.append(row[0])
                counts_list.append(row[2])
        bias_array = np.asarray(bias_list, dtype='float')
        bias_array = bias_array*10 - DC_offset #uA
        counts_array = np.asarray(counts_list, dtype='float')
        plt.plot(bias_array, counts_array, '*')
    legends_list.append('DC')


#PC      
file_names = [fn for fn in os.listdir(photon_count_files_dir)if any(fn.endswith(ext) for ext in 'txt')]
for file_name in file_names:
    full_path = photon_count_files_dir+'\\'+file_name
    filter_stripped_name = file_name.split('_')[-1][:-4]
    filter_name = re.sub('[^0-9]','', filter_stripped_name)
    legends_list.append('PC')
    with open(full_path) as PC_csv:
        bias_list = []
        counts_list = []
        read_PC_csv = csv.reader(PC_csv, delimiter=',')
        for index,  row in enumerate(read_PC_csv):
            if len(row) >= 2:
                if index == 0:
                    pass
                else:
                    bias_list.append(row[2])
                    counts_list.append(row[3])
        bias_array=np.asarray(bias_list, dtype='float')
        bias_array=bias_array*1e6 - DC_offset #convert to uA and take away offset.
        counts_array=np.asarray(counts_list, dtype='float')
        plt.plot(bias_array, counts_array, 'o', markersize=3)


plt.yscale('log')
plt.ylabel('Counts (CPS)')
plt.xlabel('Bias (uA)')
plt.title('Counts vs Bias')
#plt.legend(legends_list)
plt.grid()
plt.show()
               
