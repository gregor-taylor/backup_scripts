import HydraHarp_lib as HH
import thorlabs_apt as apt

###SETUP###
dwell_time = 20 #ms
tgt_area_height = 500 #mm
tgt_area_width = 500 #mm
inter_dwell_dist = 1.5 #mm
hh_dev_no = 0
sync_level = 500
sync_xcross = 10
ip_level = 50
ip_xcross = 10
channel = 0
motor_1_ID = 27504591
motor_2_ID = 27504633
hist_len_code = 6
####

###Initialise devices###
hh = HH.HydraHarp(hh_dev_no)
hh.initialise(0,0)
hh.calibrate()
hh.set_histo_length(hist_len_code)
hh.set_sync_cfd(sync_level,sync_xcross)
hh.set_input_cfd(channel,ip_level,ip_xcross)

motor_x = apt.Motor(motor_1_ID)
motor_y = apt.Motor(motor_2_ID)
motor_x.move_home(True)
motor_y.move_home(True)
####

###move and take data###
x_points = tgt_area_width/inter_dwell_dist
y_points = tgt_area_height/inter_dwell_dist
x_pos = 0
y_pos = 0
while y_pos < y_points:
    while x_pos < x_points:
        hh.start_meas(dwell_time)
        hh.CTC_status()
        while hh.ctcStatus.value == 0:
	        hh.CTC_status()
        hh.stop_meas()
        hh.get_histogram(channel, 1)
        point_no = str(y_pos)+'_'+str(x_pos)+'.txt'
        with open(point_no, 'w+') as op_file:
            for i in range(0,hh.histoLen.value):
                op_file.write(str(hh.histoBuffer[i]))
                op_file.write('\n')
        motor_x.move_by(inter_dwell_dist)        
        x_pos += 1
    motor_y.move_by(inter_dwell_dist)
    motor_x.move_home(True)
    y_pos += 1
    x_pos = 0
