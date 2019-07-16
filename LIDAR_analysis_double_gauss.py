#Two hydra files, plot both, compare peaks
#Select data range

#Takes input from channel 1 currently

import numpy as np
import csv
import matplotlib.pyplot as plt
from  matplotlib import style
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
import statistics
from scipy import optimize
import peakutils
style.use('fivethirtyeight_V2')

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

def dbl_gauss(B,x):
    #B is a list of m, stddev, max, offset
    #for each peak
    #constants worked out first for clarity
    c1 = B[3]+B[2]/(B[1]*(np.sqrt(2*np.pi)))
    mu1 = B[0]
    sig1 = B[1]
    c2 = B[7]+B[6]/(B[5]*(np.sqrt(2*np.pi)))
    mu2 = B[4]
    sig2 = B[5]

    y = ( c1*np.exp(-(x-mu1)**2/(2*sig1**2)) ) + ( c2*np.exp(-(x-mu2)**2/(2*sig2**2)) )
    return y 

def errorfunc(B, x, y):
    return y-dbl_gauss(B,x)

def get_peaks(data_array):
    peak_dict = {}
    pk = peakutils.indexes(data_array, min_dist=50)
    for i in pk:
        peak_dict[data_array[i]]=i
    temp = sorted(peak_dict, reverse=True)
    peak_1 = temp[0], peak_dict[temp[0]] 
    peak_2 = temp[1], peak_dict[temp[1]]
    return peak_1, peak_2

def fit_it(array, peak_1, peak_2):
    x = np.arange(1,len(array)+1)
    p0 = [peak_1[1],1.,peak_1[0],1.,peak_2[1],1.,peak_2[0],1.]
    #p0 = [3818.0,1.,278.0,1.,3598.0,1.,230.0,1.]
    fit = optimize.leastsq(errorfunc, p0, args=(x,array))
    fitted_curve = dbl_gauss(fit[0], x)
    return x, fitted_curve ,fit

def process_files_for_means(directory, start_p, end_p, channel_used):
    files_list = os.listdir(directory)
    std_dev_list = []
    max_id_list = []
    for file_name in files_list:
        filename = directory+'\\'+file_name
        data_array, meta_d, ns_per_bin = extract_data(filename, start_p, end_p, channel_used)
        arr_proc = np.copy(data_array)
        #arr_proc[arr_proc<40] = 0.0 #remove DCR
        peak_1, peak_2 = get_peaks(arr_proc)
        x, fit_x, fit_data = fit_it(arr_proc, peak_1, peak_2)
        std_dev_list.append(fit_data[0][1]) #of first peak, ignore second
        max_id_list.append(fit_data[0][0])
        delta_t = fit_data[0][0]-fit_data[0][4] #time difference btween fitted peaks
        print (delta_t)
        #dist = round(abs(delta_t*1e-12*299792458),4) #ps so -12 needed
        #if plot desired for each one
        fig, ax1 = plt.subplots()
        ax1.plot(data_array, 'bo', markersize=1)
        ax1.plot(x, fit_x,'r-')
        plt.show()

    return std_dev_list, max_id_list

root = tk.Tk()
hydra_file_initial = askopenfilename(initialdir="Z:\\", title="Choose first file")
#directory = askdirectory(initialdir="Z:\\", title="Choose directory")
root.withdraw()

#Setup
channel_used = 1

#Select data range, end to 0 for all
start_point = 5000
end_point = 14000
array_1, meta_1, ns_per_bin_1 = extract_data(hydra_file_initial, start_point, end_point, channel_used)

#fit
arr_proc = np.copy(array_1)
#arr_proc[arr_proc<40] = 0.0 #remove DCR
peak_1, peak_2 = get_peaks(arr_proc)

x, fit_x, fit = fit_it(arr_proc, peak_1, peak_2)
delta_t = fit[0][0]-fit[0][4] #time difference btween fitted peaks
dist = round(abs(delta_t*1e-12*299792458),4) #ps so -12 needed
print(peak_1, peak_2)
print(fit)

#quick plot
plt.plot(array_1, 'bo', markersize=1)
plt.plot(x, fit_x,'r-')
plt.legend(['Data', 'Fit'])
plt.ylabel('Counts')
plt.xlabel('Bin (ps)')
plt.text(0, peak_1[0]-100, 'Peak 1 = '+str(fit[0][0])+'\nPeak 2 = '+str(fit[0][4])+'\nDistance = '+str(dist/2)+'m', size=10)
plt.show()

'''
std_dev_list, max_id_list = process_files_for_means(directory, start_point, end_point, channel_used)
jitter_list  = []
for i in std_dev_list:
    jitter_list.append(2.354820045*i)
print('Mean jitter = '+str(statistics.mean(jitter_list)))
print('Std Dev jitter = '+str(statistics.pstdev(jitter_list)))
print('Mean max_id = '+str(statistics.mean(max_id_list)))
print('Std Dev max_id = '+str(statistics.pstdev(max_id_list)))

max_arr = np.asarray(max_id_list, dtype='float')
plt.plot (max_arr)
plt.show()
'''