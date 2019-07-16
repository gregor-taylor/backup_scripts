# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:23:01 2018
Takes a ouput csv from a THORLABS OSA and plots it.
@author: 0901754T
"""

import matplotlib.pyplot as plt
import numpy as np
from  matplotlib import style
import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename
style.use('fivethirtyeight')

root = tk.Tk()
filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
root.withdraw()
wlength_list =[]
power_list = []
data_start_flag = False
with open(filename) as csv_file:
    csv_read = csv.reader(csv_file, delimiter=';')
    for row in csv_read:
        if data_start_flag == True:
            if row[0] == '[EndOfFile]':
                break
            else:
                wlength_list.append(row[0])
                power_list.append(row[1])
        elif data_start_flag == False:
            if row[0] == '[Data]':
                data_start_flag = True
        
wlength_array=np.asarray(wlength_list, dtype='float')
power_array=np.asarray(power_list, dtype='float')

plt.plot(wlength_array, power_array, 'o', markersize=2)
plt.title('Spectrum')
plt.xlabel('wlength (nm)')
plt.ylabel('Power (mW)')
plt.show()