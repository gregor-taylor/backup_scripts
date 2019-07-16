# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:34:45 2018
Collection of useful funcs
@author: 0901754T
"""

def calc_photon_flux(laser_wlength,power_at_end_fibre, atten, laser_rr):
    h = 6.626070040e-34
    c = 2.99792458e8
    energy_per_photon = h*(c/laser_wlength)
    photons_per_pulse = ((power_at_end_fibre*10**(-(atten/10))/energy_per_photon)*(1/laser_rr))
    return photons_per_pulse

#write to local file if network write fails as it often does in the middle of the night
def write_local(data_to_write):
	local_filename = 'C:/temp_local_data_buffer.txt'
	with open(local_filename, 'w+') as fname:
		writer_csv =  csv.writer(fname, delimiter=',')
        writer_csv.writerow(data_to_write)


