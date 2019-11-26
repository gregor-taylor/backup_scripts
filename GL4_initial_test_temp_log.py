#Log temp for new 1K fridge initial cooldowns.

from hardware import SIM900
import csv
import time

SIM_add='ASRL7'
Therm_slot='8'
AC_bridge_slot='5'
log_file='temp_log.txt'
time_const=5

SIM900 = SIM900(SIM_add)
start_time=time.time()
with open(log_file, 'a') as logging_file:
    writer_log = csv.writer(logging_file)
    writer_log.writerow(['timestamp(s)', 'c_head_temp(K)', 'film_burner_temp(K)', 'mainplate_temp(K)', 'he_pump_temp(K)', 'heat_sw_temp(K)'])

while True:
    timestamp=str(time.time()-start_time)
    c_head_temp =SIM900.ask(AC_bridge_slot, 'TVAL?') #Cold Head temp
    film_burner_temp = SIM900.ask(Therm_slot, 'TVAL? 1') #f_burner
    mainplate_temp =SIM900.ask(Therm_slot,'TVAL? 2')
    he_pump_temp = SIM900.ask(Therm_slot, 'TVAL? 3')
    heat_sw_temp = SIM900.ask(Therm_slot, 'TVAL? 4')

    temp_data_str = [timestamp, c_head_temp, film_burner_temp, mainplate_temp, he_pump_temp, heat_sw_temp]
    print(temp_data_str)

    with open(log_file, 'a') as logging_file:
        writer_log = csv.writer(logging_file)
        writer_log.writerow(temp_data_str)

    time.sleep(time_const)
