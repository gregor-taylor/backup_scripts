# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 16:45:03 2018

Plots data from QE_auto_GT.py.

Rewritten end to plot DCR/EFF data onb one plot.

Also plots data taken with DataGatherSNSPD 

@author: 0901754T
"""
import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import matplotlib
from matplotlib import style
style.use('fivethirtyeight')

###SETUP
Tk().withdraw()
Filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
device_name = 'Dev6'
select_plot = 1 #select what plot to plot larger if desired, 0 for all of them
number_attens = 1

bias_list = []
efficiency_list = []
p_count_list=[]
DCR_list = []
flag = False
plot_dict ={}
select_plot_counter=0
for i in range(number_attens):
    plot_dict[411+i] = 'plot'+str(i)

###If all 4 plots desired
if select_plot == 0:
    subplot_pointer = 411
    plt.figure(1)
    with open(Filename) as csv_file:
        read_csv = csv.reader(csv_file)
        for row in read_csv:
            if len(row)>2:
                if flag == False: #First run through 
                    photon_flux =row[2]
                    
                    ###For first run where I didn't remember how to do sums
                    ###photon_flux = str(float(row[2])/1000)
                    ###If you don't know what this does, don't use it. If you do, remember to change the if clause in
                    ###to deal with more than 100% efficiencys as well to '-100< 1000*(float(row[3])) < 100:'
                    
                    atten_val = row[1]
                    flag = True
                else:
                    if row[0] == 'ATTENUATION': #After the 'next ATTEN line will plot and reset everything for next data set
                        bias_arr = np.asarray(bias_list, dtype='float')*10
                        eff_arr = np.asarray(efficiency_list, dtype='float')
                        
                        ###FOR first run where I didn't remember how to do sums
                        ###eff_arr = eff_arr*1000
        #Plot the fig
                        plt.subplot(subplot_pointer)
                        plot_dict[subplot_pointer] = plt.plot(bias_arr, eff_arr, '*')
                        plt.title(device_name)#+'\n tested at '+atten_val+'dB atten \n '+photon_flux+' photons/s', rotation='vertical', x=1.05,size='small' )
                        plt.ylabel('Efficiency (%)')                    
                        #Clear lists, increment counters, resets header data for next run.
                        photon_flux = row[2]
                        ###FOR first run where I didn't remember how to do sums
                        ###photon_flux = str(float(row[2])/1000)
                        atten_val = row[1]
                        bias_list = []
                        efficiency_list=[]
                        subplot_pointer+=1
                    else:
                        if -100< float(row[3]) <100: #deals with odd values.
                            bias_list.append(row[0])
                            efficiency_list.append(row[3])
                  #Once finished, plot the last one.
    bias_arr = np.asarray(bias_list, dtype='float')
    eff_arr = np.asarray(efficiency_list, dtype='float')
    plt.subplot(subplot_pointer)
    plot_dict[subplot_pointer] = plt.plot(bias_arr, eff_arr, '*')   
    plt.title(device_name)#+'\n tested at '+atten_val+'dB atten \n '+photon_flux+' photons/s', rotation='vertical', x=1.05,size='small' )
    plt.xlabel('Bias (uA)')
    plt.ylabel('Efficiency (%)')   
    plt.show()            

###else plot single plot
else:
    with open(Filename) as csv_file:
        read_csv = csv.reader(csv_file)
        for row in read_csv:
            if len(row)>2:
                if flag == False:
                    photon_flux = row[2]
                    ###FOR first run where I didn't remember how to do sums
                    ###photon_flux = str(float(row[2])/1000)     
                    atten_val = row[1]
                    flag = True
                else:
                    if row[0] == 'ATTENUATION':
                        select_plot_counter += 1
                        if select_plot == select_plot_counter:
                            bias_arr = np.asarray(bias_list, dtype='float')*10
                            eff_arr = np.asarray(efficiency_list, dtype='float')
                            ###FOR first run where I didn't remember how to do sums
                            ###eff_arr = eff_arr*1000
                            plt.plot(bias_arr, eff_arr, '*')
                            plt.title(device_name)#+'\n tested at '+atten_val+'dB atten \n '+photon_flux+' photons/s')
                            plt.xlabel('Bias (uA)')
                            plt.ylabel('Efficiency (%)')
                            plt.show()
                        else: #RESET ALL
                            photon_flux = row[2]
                            ###FOR first run where I didn't remember how to do sums
                            ###photon_flux = str(float(row[2])/1000)
                            atten_val = row[1]
                            bias_list = []
                            efficiency_list = []
                    else:
                        if -100< float(row[3]) <100: #deals with weird values.
                            bias_list.append(row[0])
                            efficiency_list.append(row[3])
                            DCR_list.append(row[1])
                            p_count_list.append(row[2])
                        
                #Again because no last 'ATTENUATION' line, need this if last plot desired.
        select_plot_counter += 1
        if select_plot == select_plot_counter:
            bias_arr = np.asarray(bias_list, dtype='float')*10
            eff_arr = np.asarray(efficiency_list, dtype='float')
            DCR_arr = np.asarray(DCR_list, dtype='float')
            p_count_array = np.asarray(p_count_list, dtype='float')
            fig, ax1 = plt.subplots()
            ax1.set_xlabel('Bias (uA)')
            ax1.set_ylabel('Efficiency (%)')
            ax1.plot(bias_arr, eff_arr,'rs', markersize=4)
            ax1.legend(['Efficiency'], loc="upper left")
            #ax1.set_yticks(range(0,110,10))#set ticks for efficiency from 0 to 100
            ax1.grid()#Grid on
            #ax1.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(10))

            ax2=ax1.twinx()
            ax2.set_ylabel('Counts (CPS)')
            ax2.semilogy(bias_arr, DCR_arr,'bs',markersize=4)
            ax2.legend(['DCR'], loc="lower right")
            #ax2.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(10))
            plt.title(device_name)#+'\n tested at '+atten_val+'dB atten \n '+photon_flux+' photons/s')

            fig2, ax3 = plt.subplots()
            ax3.set_xlabel('Bias (uA)')
            ax3.set_ylabel('Counts (cps)')
            ax3.semilogy(bias_arr, p_count_array, 'rs', markersize=4)
            ax3.semilogy(bias_arr, DCR_arr, 'bs', markersize=4)
            ax3.legend(['Photon Counts', 'Dark Count'])
            ax3.grid()


          
plt.show()
