# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:16:16 2017
Reads hydraharp .dat file, plots it, finds the peak and computes the FWHM.
@author: G Taylor
"""


import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import style

###SETUP###
root = tk.Tk()
file_to_px = askopenfilename(initialdir="Z:\\", title="Choose a file")
root.withdraw()
number_of_channels = 1
channel_used = 1
style.use('fivethirtyeight_V2')
TCSPC_type = 'HH' #'BH'=Beckr+Hickl 'HH'=Hydraharp
remove_start_vals = 300 #number of vals to be cut from start of data file as B&H has a lot of shit at start sometimes.
cut_off = 15000 #use to cut end off data
def get_max(data_array):
    index_max = np.argmax(data_array, axis=0)
    max_val = data_array[index_max]
    return index_max, max_val

def gauss(B,x):
    #B is a list of m, stddev, max, offset
    #constants worked out first for clarity
    a = B[3]+B[2]/(B[1]*np.sqrt(2*np.pi))
    b = B[0]
    c = B[1]
    y = a*np.exp(-(x-b)**2/(2*c**2))
    return y 

def errorfunc(B, x, y):
    return y-gauss(B,x)

channel_1_list=[]
channel_2_list=[]
time_list = []
if TCSPC_type == 'HH':
    with open(file_to_px) as csv_file:
        read_csv_file = csv.reader(csv_file, delimiter='\t')
        for index, row in enumerate(read_csv_file):
            if index == 0:
                metadata = row
            elif index == 8:
                ns_per_bin = float(row[channel_used-1])
            elif index in range(1,10):
                pass
            elif index > cut_off:
                pass
            else:
                if number_of_channels == 1:
                    channel_1_list.append(float(row[channel_used-1]))
                elif number_of_channels == 2:
                    channel_1_list.append(float(row[channel_used-1]))
                    channel_2_list.append(float(row[channel_used]))

elif TCSPC_type == 'BH':
    with open(file_to_px) as csv_file:
        read_csv_file = csv.reader(csv_file, delimiter='\t')
        for index, row in enumerate(read_csv_file):
            if index in range(0,10):
                pass
            elif index in range(10,remove_start_vals):
                pass
            elif row[0] == '*END':
                pass
            else:
                row_pxed = row[0].strip().split()
                #time_list.append(float(row_pxed[0])) 
                #removed above as no time just counts in this file???
                channel_1_list.append(float(row_pxed[0]))
    #ns_per_bin = float(time_list[5])-float(time_list[4])
    ns_per_bin = 0.000203


channel_1_array = np.asarray(channel_1_list)
m, max_val = get_max(channel_1_array)
B = [m, 0.55,max_val, 0]
x = np.arange(1,len(channel_1_array)+1)

p0 = [m,1.,max_val,1.]
fit = optimize.leastsq(errorfunc, p0, args=(x,channel_1_array))
fitted_curve = gauss(fit[0], x)

print(fit)

plt.plot(channel_1_array, 'b.')
plt.plot(x, fitted_curve,'r-')
print(fit[0][1])
FWHM = (2.354820045*fit[0][1]) * (ns_per_bin*1e3) #ps #DOESN'T WORK
print(FWHM)
if TCSPC_type == 'HH':
    plt.title('Jitter - '+metadata[3])
elif TCSPC_type == 'BH':
    plt.title('IRF')
plt.xlabel('Time ('+str(round(ns_per_bin, 6))+'ns per bin)')
plt.ylabel('Counts')
plt.show()



###Below section to be added if two channels required.
if channel_2_list == []:
    pass
else:
    channel_2_array = np.asarray(channel_2_list)
    max_value_ch2_index = np.argmax(channel_2_array, axis=0)

