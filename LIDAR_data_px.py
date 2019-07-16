###############################################################################
# G Taylor
#        February 2019
#              Code to take outputs of LIDAR_datagather.py and turn them into a mapping
#              using a variety of fitting/threshold techniques
#
###############################################################################

### Imports ###

import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm
from scipy import ndimage
import matplotlib.ticker as mticker

### Functions for threshold method ###

def process_files_for_thresholds(directory, files_list, start_p, end_p):
    image_dict = {}
    files_to_average_pixels=[]
    for file_name in files_list:
        data_conditioned = False
        filename = directory+'\\'+file_name
        data_array = extract_data(filename, start_p, end_p)
        max_val, max_indexes = get_maxes(data_array) #Gets the positions of the max values of the histo.
        if max_val == 1: #If no count bigger than 1 then note the pixel and can average it later.
            files_to_average_pixels.append(file_name[:-4])
            #average neighbouring pixels
        elif len(max_indexes) == 1: #If only one max value, take it as the pixel range.
            pixel_bin = max_indexes[0][0]
        else: #else, try and get a variance of 200ps meaning the signal is a signal rather than noise. If it fails then try to remove values to home in on the point.
            while data_conditioned == False:
                if np.var(max_indexes) < 200: #tune this paramater.
                    pixel_bin = np.mean(max_indexes)
                    data_conditioned = True
                else:
                    if len(max_indexes)>3: #remove values until variance decreases.
                        max_indexes = max_indexes[:-1]
                        max_indexes = max_indexes[1:]
                    else:
                        pixel_bin=np.mean(max_indexes) #if only 2 vals just average them and take that as answer.
                        data_conditioned = True
        image_dict[file_name[:-4]] = pixel_bin
    return image_dict, files_to_average_pixels

def extract_data(file, start_p, end_p):
    with open(file) as csv_file:
        data_list=[]
        read_csv_file = csv.reader(csv_file, delimiter='\t')
        for index, row in enumerate(read_csv_file):
            if end_p == 0:
                data_list.append(float(row[0]))
            else:
                if index in range((start_p+10), (end_p+10)):
                    data_list.append(float(row[0]))
    data_arr = np.asarray(data_list, dtype='float')
    return data_arr

def get_maxes(data_array):
    max_val = np.amax(data_array)
    max_indexes = np.argwhere(data_array == max_val)
    return max_val, max_indexes

### Functions for cross correlate method ###

def process_files_with_fit(directory, files_list, start_p, end_p):
    for file_name in files_list:
        data_conditioned = False
        filename = directory+'\\'+file_name
        data_array = extract_data(filename, start_p, end_p)
        max_val, max_indexes = get_maxes(data_array) #Gets the positions of the max values of the histo.
        max_mean_id = np.mean(max_indexes)

def extract_data_IRF(file, start_p, end_p, channel_used):
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

def cross_correlate(data_1, data_2):
    corr = np.fft.ifft(np.fft.fft(data_1)*np.conj(np.fft.fft(data_2)))
    return corr

def cross_correlate_all_files(directory, IRF_data,start_p, end_p):
    image_dict = {}
    files_to_average_pixels=[]
    files_list = os.listdir(directory)
    for file_name in files_list:
        filename = directory+'\\'+file_name
        data_array = extract_data(filename, start_p, end_p)
        corr = cross_correlate(data_array, IRF_data)
        max_val = np.argmax(corr)
        if max_val < lower_threshold_for_pixel:
            files_to_average_pixels.append(file_name[:-4])
        elif max_val > upper_threshold_for_pixel:
            files_to_average_pixels.append(file_name[:-4])
        image_dict[file_name[:-4]] = max_val
    return image_dict, files_to_average_pixels #files_to_average_pixels empty at moment, leaves room to average pixels if required


### Setup code to be edited ###

image_size_x = 86
image_size_y = 100
start_point=5000
end_point=12000
lower_threshold_for_pixel = 0 #come up with way of automatically determining this
upper_threshold_for_pixel = 20000

root = tk.Tk()
directory = askdirectory(initialdir="Z:\\", title="Choose directory")
root.withdraw()
files_list = os.listdir(directory)

### Threshold method ### 

#image_dict, files_to_average_pixels = process_files_for_thresholds(directory, files_list, start_point, end_point)


### Cross correlate method ###

IRF = askopenfilename(initialdir="Z:\\", title="Choose IRF file")
IRF_data, meta_IRF, ns_per_bin_IRF = extract_data_IRF(IRF, start_point, end_point, 1)
image_dict, files_to_average_pixels = cross_correlate_all_files(directory, IRF_data, start_point, end_point)

### Turns output of chosen method into data array of pixel ranges ###

img_arr = np.zeros((image_size_y, image_size_x))
for k, v in image_dict.items():
    x, y =k.split('_')[0], k.split('_')[1]
    x, y = int(x), int(y)
    try:
        img_arr[x,y] = v
    except:
        print('Outside image size')

### Averaging adjacent pixels if required ###

if files_to_average_pixels != []:
    print(str(len(files_to_average_pixels))+' pixels needing averaged')
    for pixel_needs_average in files_to_average_pixels:
        x, y = pixel_needs_average.split('_')[0], pixel_needs_average.split('_')[1]
        x, y = int(x), int(y)
        if x==0 and y==0:
            av_val = (img_arr[x+1,y]+img_arr[x,y+1])/2
        elif x==0 and y==image_size_y-1:
            av_val = (img_arr[x+1,y]+img_arr[x,y-1])/2
        elif x==image_size_x-1 and y==image_size_y-1:
            av_val = (img_arr[x-1,y]+img_arr[x,y-1])/2
        elif x==image_size_x-1 and y==0:
            av_val = (img_arr[x-1,y]+img_arr[x,y+1])/2
        elif x == 0:
            av_val = (img_arr[x+1,y]+img_arr[x,y+1]+img_arr[x,y-1])/3
        elif x == image_size_x-1:
            av_val = (img_arr[x-1,y]+img_arr[x,y+1]+img_arr[x,y-1])/3
        elif y == 0:
            av_val = (img_arr[x+1,y]+img_arr[x-1,y]+img_arr[x,y+1])/3
        elif y == image_size_y-1:
            av_val = (img_arr[x+1,y]+img_arr[x-1,y]+img_arr[x,y-1])/3
        else:
            av_val = (img_arr[x+1,y]+img_arr[x-1,y]+img_arr[x,y+1]+img_arr[x,y-1])/4
        #check if the average val is still big enough, deals with cases where the zero is surrounded by other zeroes.
        if av_val < lower_threshold_for_pixel:
            av_val = np.mean(img_arr)
        elif av_val > upper_threshold_for_pixel:
            av_val = np.mean(img_arr)
        img_arr[x,y] = av_val

### Smoothing ###


### Plotting ###

### Basic 2d plot ###

#plt.imshow(img_arr)
#plt.show()
def log_tick_formatter(val, pos=None):
    return "{:.2e}".format(10**val)
### 3-D plot ###

fig=plt.figure()
ax=fig.gca(projection='3d')
#Make some datasets from the array
x_data=np.arange(image_size_x)
y_data=np.arange(image_size_y)
'''
with open('data_op.txt', 'w+') as file:
    writer_csv=csv.writer(file)
    for i in range(len(x_data)):
        for j in range(len(y_data)):
            writer_csv.writerow(x_data[i], y_data[j], img_arr[i][j])
            '''
#img_arr[img_arr>9000]-=9000
img_arr[img_arr<2000]+=7000
x_data=x_data/2
y_data=y_data/2
x_data, y_data=np.meshgrid(x_data, y_data)
#img_arr[img_arr == '-inf'] = 0
#img_arr=np.nan_to_num(img_arr)
surf=ax.plot_surface(x_data, y_data, img_arr, cmap=cm.plasma)
#plasma best so far
#ax.set_zlim3d(8000, 10000)
#ax.zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
plt.show()

sig = [0.1, 0.5]
for i in sig:
    px_img_arr = ndimage.filters.gaussian_filter(img_arr, sigma=i)
    fig=plt.figure()
    ax=fig.gca(projection='3d')
    surf=ax.plot_surface(x_data, y_data, px_img_arr, cmap=cm.plasma)
    ax.set_zlim3d(6800, 7300)
    fig.colorbar(surf, shrink=0.5, aspect=10, orientation='horizontal')
    plt.xlabel('x pos (mm)', size=12)
    plt.ylabel('y pos (mm)', size=12)
    plt.show()
