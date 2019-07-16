#plot GL theory Ic density with respect to temp (t=T/Tc)
#uses expression Ic(t)=(1-t^2)^(3/2)x(1+t^2)^(1/2)

import numpy as np
import matplotlib.pyplot as plt

def calc_jc(t):
	j_c = (1-(t**2)**(2/3))*(1+(t**2)**(1/2))
	return j_c

Tc = 8.6
t_arr = np.arange(0.0, 1.01, 0.01, dtype=float)
T_arr = t_arr*Tc

jc_list=[]
for i in t_arr:
	j_c = calc_jc(i)
	jc_list.append(j_c)

jc_arr = np.asarray(jc_list)

plt.plot(T_arr, jc_arr, 'o')
plt.xlabel('T(k)')
plt.grid()
plt.show()

