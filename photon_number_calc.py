def calculate_photon_number(laser_r, wav, power, atten): #wav in nm, rr in Hz, power in W, atten in dB
        h = 6.626070040e-34
        c = 2.99792458e8
        ppp = []
        laser_rr=float(laser_r)
        energy_per_photon = h*(c/(float(wav)/1e9))
        ph_p_pul = (float(power)*10**(-(float(atten)/10))/energy_per_photon)*(1/laser_rr)
        ph_p_sec = round(ph_p_pul*laser_r)
        return ph_p_pul, ph_p_sec


print(calculate_photon_number(110e6, 2600, 1e-6, 41.6))
        