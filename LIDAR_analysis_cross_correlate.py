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
    #constants worked out fIRFt for clarity
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

def cross_correlate(data_1, data_2):
    corr = np.fft.ifft(np.fft.fft(data_1)*np.conj(np.fft.fft(data_2)))
    return corr

def cross_correlate_all_files(directory, IRF_data,start_p, end_p, channel_used):
    files_list = os.listdir(directory)
    max_id_list = []
    for file_name in files_list:
        filename = directory+'\\'+file_name
        data_array, meta_d, ns_per_bin = extract_data(filename, start_p, end_p, channel_used)
        corr = cross_correlate(data_array, IRF_data)
        max_val = np.argmax(corr)
        max_id_list.append(max_val)
        #plt.plot(corr)
        #plt.show()
    return max_id_list



    return std_dev_list, max_id_list
root = tk.Tk()
IRF = askopenfilename(initialdir="Z:\\", title="Choose IRF file")
directory = askdirectory(initialdir="Z:\\", title="Choose directory")
#hydra_file = askopenfilename(initialdir="Z:\\", title="Choose data file")
root.withdraw()

#Setup
channel_used = 1
subtract_bg = True
#Select data range, end to 0 for all
start_point = 6000
end_point = 14000

IRF_data, meta_IRF, ns_per_bin_IRF = extract_data(IRF, start_point, end_point, channel_used)

'''
array_1, meta_1, ns_per_bin_1 = extract_data(hydra_file, start_point, end_point, channel_used)
corr = cross_correlate(IRF_data, array_1)
print(np.argmax(corr))

#quick plot
plt.plot(corr, 'bo', markersize=1)

plt.show()
'''
max_points = cross_correlate_all_files(directory, IRF_data, start_point, end_point, channel_used)
print(max_points)
plt.plot(max_points, 'bo')
plt.show()