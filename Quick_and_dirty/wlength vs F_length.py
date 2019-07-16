# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:12:02 2018
Plot wavelength vs focal length
@author: 0901754T

NOTE: Assumed that the numbers given on ocean optics for focal length were at the minimum wavelength quoted (350nm), this might be 
bollocks. I've worked out the radius of curvature from those numbers and scaled from there.
"""
import numpy as np
import matplotlib.pyplot as plt

n_dict = {365.02:1.53626, 404.66:1.53024, 435.84:1.52669, 546.706:1.51872, 706.52:1.51289, 852.11:1.50981, 1013.98:1.50731,
          1529.52:1.50094, 1970.09:1.49500, 2325.42:1.48929}

def calc_f_length(n):
    R = 5.3626 #mm
    f = R/(n-1)
    return f

wlength_list=[]
f_list=[]
for k in n_dict:
    wlength_list.append(k)
    f_list.append(calc_f_length(n_dict[k]))
    
wlength_arr = np.asarray(wlength_list)
f_arr = np.asarray(f_list)

plt.plot(wlength_arr, f_arr)
plt.title('F_length vs wavelength - BK7 Glass')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Focal length (mm)')
