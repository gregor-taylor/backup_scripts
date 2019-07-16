# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:46:37 2017
Takes photon count files for varying ND filter sterngths and plots them.

Fill in all parameters under 'Setup'

@author: G Taylor
"""

###TO BE DONE###
#Configure so filter values are fetched automatically from file names

#import
import csv
import matplotlib.pyplot as plt
import numpy as np
import re
import os

###Setup 
save_to_txt = 'n'
output_folder = "Z:\\Ramanator-PC\\Kleanthis\\measurements\\2017-10-30 2p3um NICT F4\\Photon counts\\output_from_py\\"
laser_rr = 110e6 #Laser rep rate
power_at_end_fibre = 3.2e-3 #Power after optical setup
filter_list = [6, 6.3, 6.6, 7, 7.3, 7.6, 8, 8.3] #OD values
laser_wlength = 2.3e-6 
photon_count_files_dir="Z:\\Ramanator-PC\\Kleanthis\\measurements\\1550DBR\\photon counts"
dark_count_file = "Z:\\Ramanator-PC\Kleanthis\\measurements\\1550DBR\\dark counts\\1A__SMA3_I_V_50 Ohm Shunt_2.2K_100Kohmdark_counts_blocked_at_box.txt"
bias_points = [0.7,0.75,0.8,0.85,0.9,0.95,1.0,1.05] #microamps

#constants
h=6.626e-34
c=2.998e8


###sort out the files for processing from given directory
def sorting_func(fname):
    filter_stripped_name = fname.split('_')[-1][:-4]
    filter_name = re.sub('[^0-9]','', filter_stripped_name)
    return filter_name
file_names = [fn for fn in os.listdir(photon_count_files_dir)if any(fn.endswith(ext) for ext in 'txt')]
photon_count_files_list_unsorted = []
photon_count_files_list = []
for file_name in file_names:
    photon_count_files_list_unsorted.append(photon_count_files_dir+'\\'+file_name)
photon_count_files_list=sorted(photon_count_files_list_unsorted, key=sorting_func)


###Photon numbers for given filter
energy_per_photon = h*(c/laser_wlength)
no_photons_pp_dict ={}
for i in filter_list:
    DB_value = 10*i
    photons_per_pulse = ((power_at_end_fibre*10**(-(DB_value/10))/energy_per_photon)*(1/laser_rr))
    no_photons_pp_dict[str(i).replace('.','')]=photons_per_pulse
    
    
###DC values for given bias
bias_point_value_dicts={}
with open(dark_count_file) as DC_csv_file:
    read_DC_csv_file = csv.reader(DC_csv_file, delimiter='\t')
    for bias_point in bias_points:
        sum_of_rows = 0
        for row in read_DC_csv_file:
            if len(row) >= 2: #Odd empty lines in output file to be dealt with
                if round(float(row[0]),2) == bias_point:
                    sum_of_rows += float(row[2])
        DC_csv_file.seek(0) #resets file pointer for next bias point
        averaged_count = sum_of_rows/2
        bias_point_value_dicts[bias_point]={}     
        bias_point_value_dicts[bias_point]["DC"]=averaged_count
                    
        
###PCs for given bias
for PC_file_name in photon_count_files_list:
    filter_stripped_name = PC_file_name.split('_')[-1][:-4]
    filter_name = re.sub('[^0-9]','', filter_stripped_name)
    with open(PC_file_name) as PC_csv_file:
        read_PC_csv_file = csv.reader(PC_csv_file, delimiter='\t')
        for bias_point in bias_points:
            sum_of_rows = 0
            for row in read_PC_csv_file:
                if len(row) >= 2: #Odd empty lines in output file to be dealt with
                    if round(float(row[0]),2) == bias_point:
                        sum_of_rows += float(row[2])                                     
            PC_csv_file.seek(0)
            averaged_count = sum_of_rows/2
            bias_point_value_dicts[bias_point][filter_name]=averaged_count

###Plot data            
col1_list = []
legend_list=[]
plt.figure(figsize=(8,6), dpi=80)
plt.subplot(1,1,1)
for k in no_photons_pp_dict:
    col1_list.append(no_photons_pp_dict[k])
col1_array = np.asarray(col1_list, dtype='float')
for bias_point in bias_points:
    col2_list = []
    for k in bias_point_value_dicts[bias_point]:
        if k == 'DC':
            pass
        else:
            adjusted_count = bias_point_value_dicts[bias_point][k] - bias_point_value_dicts[bias_point]['DC']
            col2_list.append(adjusted_count)
            #col2_list.append(bias_point_value_dicts[bias_point][k]) ###SWAP WITH ABOVE LINE TO NOT SUBTRACT DC
    col2_array = np.asarray(col2_list, dtype='float')
    
    #fit
  #  coefficients = np.polyfit(np.log10(col1_array), np.log10(col2_array), 1)
  #  polynomial = np.poly1d(coefficients)
  #  y_fit = polynomial(np.log10(col1_array))
    
    #plot
    plt.plot(col1_array, col2_array,'')
#    plt.plot(col1_array, (10**y_fit), '-')
    legend_list.append(bias_point)
 #   legend_list.append(str(bias_point)+' fit: m=' +str(coefficients[0]))
    
    #punt out to txt if required
    if save_to_txt == 'y':
        file_path = output_folder + str(bias_point) + '.txt'
        np.savetxt(file_path, np.column_stack((col1_array,col2_array)), delimiter='\t', newline='\r\n')
        
###format plot
plt.legend(legend_list)       
plt.yscale('log')
plt.ylabel('Photon counts (cps)')
plt.xscale('log')
plt.xlabel('Photons per pulse')
plt.show()
    
