laser_rr = 1 #Laser rep rate
power_at_end_fibre = 40e-6 #Power after optical setup
filter_list = [6.5,6.6,6.7,6.8,6.9,7,7.7,7.8,7.9,8, 8.9,9, 9.1,9.2, 9.3,\
               8.1,8.2,8.3,8.4,8.5,8.6,7.6,7.5,7.4,7.3,7.2,7.1,9.4,9.5,9.6,9.7] #OD values
laser_wlength = 0.83e-6 
#constants
h=6.626e-34
c=2.998e8


#Photon numbers for given filter
energy_per_photon = h*(c/laser_wlength)
print (energy_per_photon)
no_photons_pp_dict ={}
for i in filter_list:
    DB_value = 10*i
    photons_per_pulse = ((power_at_end_fibre*10**(-(DB_value/10))/energy_per_photon)*(1/laser_rr))
    no_photons_pp_dict[str(i).replace('.','')]=photons_per_pulse
print(power_at_end_fibre)
for k in no_photons_pp_dict:
    print (k, no_photons_pp_dict[k])
 
