


import matplotlib.pyplot as plt
import numpy as np
import csv
import os

folder = 'Z:\\User folders\\Gregor Taylor\\MIR work\\OPO\\Spectra\\Fluctuating power spectra'
wlength_dict = {}
power_dict = {}
files_list = os.listdir(folder)

for file_name in files_list:
    filename = folder+'\\'+file_name
    data_start_flag = False
    wlength_list =[]
    power_list = []
    with open(filename) as csv_file:
        csv_read = csv.reader(csv_file, delimiter=';')
        for row in csv_read:
            if data_start_flag == True:
                if row[0] == '[EndOfFile]':
                    break
                else:
                    if 2000<float(row[0])<5000:#Change these values to change wavelength of interest - time consuming to do all of the spectrum
                        wlength_list.append(row[0])
                        power_list.append(row[1])
                    else:
                        pass
            elif data_start_flag == False:
                if row[0] == '[Data]':
                    data_start_flag = True
   
#Plots and saves all figures if desired for every file (TAKES TIME)
#    plt.plot(np.asarray(wlength_list, dtype='float'), np.asarray(power_list, dtype='float'))
#    plt.title('Spectrum')
#    plt.xlabel('wlength (nm)')
#    plt.ylabel('Power (mW)')
#    fname = folder+'\\'+'graph_'+file_name[19:21]
#    plt.savefig(fname)
#    plt.close()

        
#    wlength_dict["spect_"+file_name[19:21]]=np.asarray(wlength_list, dtype='float')
#    power_dict["spect_"+file_name[19:21]]=np.asarray(power_list, dtype='float')

#plt.plot(wlength_array, power_array, '-')
#plt.title('Spectrum')
#plt.xlabel('wlength (nm)')
#plt.ylabel('Power (mW)')

#Do stuff with the data
#Get the power of index 2618 (2320.66nm) and plot it over time
    '''
ind = 0
P_list = []

while ind <= 97:
    if ind <10:
        changed_str = '0'+str(ind)
        P_list.append(power_dict['spect_'+changed_str][2618]*1000000)#convert to uW
    else:
        P_list.append(power_dict['spect_'+str(ind)][2618]*1000000)
    
    ind+=1
    
plt.plot(P_list)
plt.xlabel('Time(mins)')
plt.ylabel('Power (uW)')
    

    '''