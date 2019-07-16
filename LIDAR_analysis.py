#Two hydra files, plot both, compare peaks
#Select data range

#Takes input from channel 1 currently

import numpy as np
import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from scipy import optimize
import os
import statistics


def extract_data(file, start_p, end_p, channel_used):
    with open(file) as csv_file:
        data_list=[]
        read_csv_file = csv.reader(csv_file, delimiter='\t')
        for index, row in enumerate(read_csv_file):
            if index == 0:
                metadata = row
            elif index == 8:
                ns_per_bin = float(row[channel_used-1])
            elif index in range(1,10):
                pass
            else:
                if end_p == 0:
                    data_list.append(float(row[channel_used-1]))
                else:
                    if index in range((start_p+10), (end_p+10)):
                        data_list.append(float(row[channel_used-1]))
    data_arr = np.asarray(data_list, dtype='float')
    return data_arr, metadata, ns_per_bin

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

def get_max(data_array):
    index_max = np.argmax(data_array, axis=0)
    max_val = data_array[index_max]
    return index_max, max_val

def fit_it(m, max_val, array):
    B = [m, 0.55,max_val, 0]
    x = np.arange(1,len(array)+1)
    p0 = [m,1.,max_val,1.]
    fit = optimize.leastsq(errorfunc, p0, args=(x,array))
    fitted_curve = gauss(fit[0], x)
    return x, fitted_curve, fit

def process_files_for_means(directory, start_p, end_p, channel_used):
    files_list = os.listdir(directory)
    std_dev_list = []
    max_id_list = []
    for file_name in files_list:
        filename = directory+'\\'+file_name
        data_array, meta_d, ns_per_bin = extract_data(filename, start_p, end_p, channel_used)
        m, max_val = get_max(data_array)
        if subtract_bg == True:
            arr_proc = np.copy(data_array)
            arr_proc[arr_proc<(max_val/2)] = 0.0
            x1, fit_1, fit_data = fit_it(m, max_val, arr_proc)
        else:
             x1, fit_1, fit_data = fit_it(m, max_val, data_array)
        std_dev_list.append(fit_data[0][1])
        max_id_list.append(fit_data[0][0])
        #if plot desired for each one
        fig, ax1 = plt.subplots()
        ax1.plot(data_array, 'bo', markersize=1)
        ax1.plot(x1, fit_1,'b-')
        plt.show()

    return std_dev_list, max_id_list


root = tk.Tk()
#hydra_file_initial = askopenfilename(initialdir="Z:\\", title="Choose first file")
directory = askdirectory(initialdir="Z:\\", title="Choose directory")
#hydra_file_2 = askopenfilename(initialdir="Z:\\", title="Choose second file")
root.withdraw()

#Setup
channel_used = 1
subtract_bg = True
#Select data range, end to 0 for all
start_point = 6000
end_point = 14000
'''
array_1, meta_1, ns_per_bin_1 = extract_data(hydra_file_initial, start_point, end_point, channel_used)
#array_2, meta_2, ns_per_bin_2 = extract_data(hydra_file_2, start_point, end_point, channel_used)
#fit
m, max_val = get_max(array_1)
####TRIAL subtract all of the shit around the peak
if subtract_bg == True:
    arr_proc = np.copy(array_1)
    arr_proc[arr_proc<(max_val/2)] = 0.0
    x1, fit_1, fit_data = fit_it(m, max_val, arr_proc)
else:
	x1, fit_1, fit_data = fit_it(m, max_val, array_1)
print(fit_data)

#m_2, max_val_2 = get_max(array_2)
#x2, fit_2 = fit_it(m_2, max_val_2, array_2)

#print(str(m_2-m)+' ps')
#dist = ((m_2-m)*  1e-12)*3e8
#print(str(dist)+' m')

#quick plot
plt.plot(array_1, 'bo', markersize=1)
#plt.plot(array_2, 'ro', markersize=1)
plt.plot(x1, fit_1,'b-')
#plt.plot(x2, fit_2,'r-')
plt.show()

'''
 #means of various histos
std_dev_list, max_id_list = process_files_for_means(directory, start_point, end_point, channel_used)
jitter_list  = []
for i in std_dev_list:
	jitter_list.append(2.354820045*i)
print('Mean jitter = '+str(statistics.mean(jitter_list)))
print('Std Dev jitter = '+str(statistics.pstdev(jitter_list)))
print('Mean max_id = '+str(statistics.mean(max_id_list)))
print('Std Dev max_id = '+str(statistics.pstdev(max_id_list)))

max_arr = np.asarray(max_id_list, dtype='float')
dist = (max_arr*1e-12*299792458)/2 #ps so -12 needed
rel_dist = dist - dist[0]
print(dist)
print(rel_dist)
plt.plot (max_arr, 'o')
plt.show()  
