# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 12:53:09 2018

@author: 0901754T
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename

root = tk.Tk()
filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
root.withdraw()
current_list = []
voltage_list = []

def find_Ic(v_arr, i_arr):
    #get index of points that cross a 1.5mV threshold
    threshold_upper = v_arr[0] + 15e-5
    threshold_lower = v_arr[0] - 15e-5
    for index, val in enumerate(v_arr):
        if val > threshold_upper:
            max_ind = index
            break
    for index, val in enumerate(v_arr):
        if val < threshold_lower:
            min_ind = index
            break
    #take those indexes and get corresponding currents, average them and return
    print(max_ind, min_ind)
    min_val = i_arr[min_ind]
    max_val = i_arr[max_ind]
    av_val = (abs(max_val)+abs(min_val))/2
    return round(av_val,1)

def calc_current_over_dev(bias_resist, shunt_resist, V1, V2):
    current = ((V1-V2)/bias_resist)-(V2/shunt_resist)
    current_micro = current * 1000000 #in microamps
    return current_micro

with open(filename) as csv_file:
    read_csv = csv.reader(csv_file, delimiter=',')
    for index, row in enumerate(read_csv):
        if len(row)>0:
            if index<30:
                if index == 2:
                    bias_resistor = float(row[1])
                elif index == 6:
                    date_time = row[1]
                elif index == 8:
                    dev_id = row[1]
                elif index == 18:
                    shunt_resistor = float(row[1])
                else:
                    pass
            else:            
                v1 = float(row[0])
                v2 = float(row[1])
                current_over_dev = calc_current_over_dev(bias_resistor, shunt_resistor, v1, v2)
                current_list.append(current_over_dev)
                voltage_list.append(v2)
           

current_array = np.asarray(current_list, dtype='float')
voltage_array = np.asarray(voltage_list, dtype='float')

plt.plot(voltage_array,current_array, '-')
plt.title('Device '+dev_id+': '+date_time+'. Bias R = '+str(bias_resistor)+', Shunt R = '+str(shunt_resistor))
plt.xlabel('Voltage over device(V)')
plt.ylabel('Current through device(uA)')
plt.text(min(voltage_array),0,'$I_c$ = '+str(find_Ic(voltage_array,current_array))+'uA')
plt.show()

        