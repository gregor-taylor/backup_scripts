#####################################################################
#                                                                   #
#  Name         :   I-V-Rankinator                                  #
#  Author       :   Gavin Orchin                                    #
#  Description  :   I-Vs measured until Temp exceeds a value        #                                                                
#                                                                   #
#   The SIM900 is run in triggered mode. This ensures that the      #
#   values of V1 and V2 are recorded at the same time and allows    #
#   much faster readings (10Hz vs 1Hz).                             #
#   It seems there are 2 small bugs:                                #
#   1) The mode of the SIM900 takes a long time to change so the    #
#   1st IV usually has an error at the start.                       #
#   2) About half the time the mode doesn't change from its default #
#   value. Run the code again and the problem should disappear.     #
#                                                                   #
#   The mode of the voltmeter is printed each IV run. It should     #
#   read: AUTO=0, SCAL=200, DVDR=2, CHOP=0, FLTR=0. Descriptions    #
#   of these terms are given in the code when they are changed.     #
#                                                                   #
#####################################################################

import visa as vi
import time
import numpy as np
import os
import Diode_Conversions as DC
#Change me. Don't let the first character be a number.
yourName        = 'Kleanthis'
chipName        = '2p3um'
deviceName      = 'F4'
smaNumber       = '8'
temperature     = '5K'
shunt           = '50' #In Ohms
comment         = 'cooldown,75 steps ,0.1s'
StopTemp        = 7.00
resistor        = 100000
dateAndTime     = time.strftime('%d_%m_%y_%H%M')
sleepTime       = 0.1 #between data points
delay           = 0 #between IVs
#Set you Voltage path
maxBias = 1.5
steps = 75


#At start of file:
#smaNumber, temperature, shunt, resistor



#################################################################
#                                                               #
#   DON'T VENTURE FORTH                                         #
#                                                               #
#################################################################

#-----DATA------------------------------------------------------#

#data = []





#-----CONNECTIONS-----------------------------------------------#

#SIM900
SIM900_port = 'ASRL1'
SIM900      = vi.instrument(SIM900_port)

SIM900_port_T         = 'GPIB0::2::INSTR'
SIM900_T = vi.instrument(SIM900_port_T)

#Check SIM900 Connection
try:
    SIM900.clear()
    SIM900.write("*CLS")
    SIM900Check = SIM900.ask('*IDN?')[:1]
    if SIM900Check is 'S':
        print "SIM900 Mainframe:\t\t Connected"
    else:
        print "SIM900 Mainframe:\t\t Not Connected"
except:
    print "SIM900 Mainframe:\t\t Not Connected"

    #Check SIM900_T Connection
try:
    SIM900_T.clear()
    SIM900_T.write('*CLS')
    SIM900_T_Check = SIM900_T.ask('*IDN?')[:1]
    if SIM900_T_Check is 'S':
        print "SIM900_T Mainframe:\t\t Connected"
    else:
        print "SIM900_T Mainframe:\t\t Not Connected"
except:
    print "SIM900_T Mainframe:\t\t Not Connected"
time.sleep(1)



#-----PROGRAM---------------------------------------------------#

SIM900.write('CONN 2, "xyx"')
#reset voltmeter settings
SIM900.write('*CLS')
time.sleep(0.5)
SIM900.write('*RST')
time.sleep(0.5)

# Set triggering to remote using TMOD command. This is reset to dafault(0) at end of progrsm.
# 0 = LOCAL = continuous unsynchonized measurements
# 1 = EXTERNAL = Take measurement of all 4 inputs when the trigger coax goes LOW
# 2 = REMOTE =  Take measurement of all 4 inputs when *TRG command is issued
SIM900.write('TMOD 2')
time.sleep(0.5)

#Turn off automatic changing of: SCALE, DIVIDER, CHOP and FILTER.
#SCALE - decimal position on display
#DIVIDER - attuates signal by factor of 10 if on. Needs to be on if voltage > 2V or else protection circuitry triggered but it can cause gain errors
#CHOP - corrects for offset and gain errors in measurements (reduces measurement rate)
#FILTER - applies a low pass filter to measurements with a time period of 8 measurements. Is automatically turned off if measurements are detected to be changing quickly. I think this is what leads to voltage jumps in some IVs

SIM900.write('AUTO 1, 0') #This number (0-15) is interpreted as a 4 digit bitstream where 1=ON, 0=OFF. Therefore, 15=ALL ON and 0=All OFF 
time.sleep(0.5)
SIM900.write('AUTO 2, 0')
time.sleep(0.5)
SIM900.write('AUTO 3, 0')
time.sleep(0.5)
SIM900.write('AUTO 4, 0')
time.sleep(0.5)

SIM900.write('SCAL 1, 20')  #scale set to max of 20V
time.sleep(0.5)
SIM900.write('SCAL 2, 200') #scale set to max of 200mV
time.sleep(0.5)
SIM900.write('SCAL 3, 20')
time.sleep(0.5)
SIM900.write('SCAL 4, 20')
time.sleep(0.5)

SIM900.write('DVDR 1, 1') #Attenuator ON
time.sleep(0.5)
SIM900.write('DVDR 2, 2') #Attenuator OUT = OFF but with high input impedance
time.sleep(0.5)
SIM900.write('DVDR 3, 1')
time.sleep(0.5)
SIM900.write('DVDR 4, 1')
time.sleep(0.5)

#Set the autocalibration regime for each channel
# 0 = NONE - Correct for a offset error and a gain error only at the start of the measurement sequence (once per program run)
# 1 = GND - Correct for an offset error continuously and a gain error only at the start of the sequence
# 2 = GNDREF4(default) - Correct for both errors continuously, measure the input twice
# 3 = GNDREF3 - Correct for both errors continuously

# Max measurement rate for each setting is:
# 0 - 6/s
# 1 - 3/s
# 2 - 3/s
# 3 - 2/s

SIM900.write('CHOP 1, 0')
time.sleep(0.5)
SIM900.write('CHOP 2, 0')
time.sleep(0.5)
SIM900.write('CHOP 3, 0')
time.sleep(0.5)
SIM900.write('CHOP 4, 0')
time.sleep(0.5)

SIM900.write('FLTR 1, 0')
time.sleep(0.5)
SIM900.write('FLTR 2, 0')
time.sleep(0.5)
SIM900.write('FLTR 3, 0')
time.sleep(0.5)
SIM900.write('FLTR 4, 0')
time.sleep(0.5)



TempLow=True
q=0
while TempLow :
    #Get Temperature
    print 'Run ' + str(q + 1)
    try:
        SIM900_T.write('CONN 1, "xyx"')
        Resi_SIM921_X = SIM900_T.ask('RVAL?').strip() #Which reading is the He3 head?
        SIM900_T.write('xyx')
    except:
        print "Failed to collect voltage reading."
        SIM900_T.clear()
    temp       = round(DC.RuO2Converter(float(Resi_SIM921_X)), 3)
    
    fileName        = ('S:\QSG\\Rankinator-PC\\' + str(yourName) + '\Measurements\Devices\\' + str(chipName) + '\Feb_18\\IVTemp\\'
                                 + 'F4_run_1'  + '_' + str(q) + '.txt')
    
    print str(temp)
    #-----FILES-----------------------------------------------------#

    #If the directed doesn't exist, create it
    try:
        os.makedirs(os.path.dirname(fileName))
        print 'Directory',os.path.dirname(fileName),'created'
    except OSError:
        print 'Directory',os.path.dirname(fileName),'exists'
    
    #Create the Bias order
    biasprimitive = np.linspace((-maxBias),maxBias,steps+1)
    biases = list(biasprimitive) + list(biasprimitive[::-1])[1:]

    #Set the Bias to Zero and turn on the module
    SIM900.write('CONN 1, "xyx"')
    SIM900.write('VOLT 0.0')
    SIM900.write('OPON')
    SIM900.write('xyx')

    #Main Loop

    #reset chop to correct for errors
    SIM900.write('CONN 2, "xyx"')
    SIM900.write('CHOP 1, 0')
    time.sleep(0.5)
    SIM900.write('CHOP 2, 0')
    time.sleep(0.5)
    SIM900.write('CHOP 3, 0')
    time.sleep(0.5)
    SIM900.write('CHOP 4, 0')
    time.sleep(0.5)

    #check its in the right state, 
    state_auto = SIM900.ask('AUTO? 2')
    time.sleep(0.5)
    state_scal = SIM900.ask('SCAL? 2')
    time.sleep(0.5)
    state_dvdr = SIM900.ask('DVDR? 2')
    time.sleep(0.5)
    state_chop = SIM900.ask('CHOP? 2')
    time.sleep(0.5)
    state_fltr = SIM900.ask('FLTR? 2')
    time.sleep(0.5)
    SIM900.write('xyx')

    print "AUTO = ", str(state_auto)
    print "SCAL = ", str(state_scal)
    print "DVDR = ", str(state_dvdr)
    print "CHOP = ", str(state_chop)
    print "FLTR = ", str(state_fltr)
    
    for bias in biases:
        #Change Bias
        try:
            SIM900.write('CONN 1, "xyx"')
            SIM900.write('VOLT ' + str('%.3f' % bias))
            SIM900.write('xyx')
        except:
            print "Failed to change bias."

        #Sleep time
        time.sleep(sleepTime/2)

        #Read Voltage
        try:
            SIM900.write('CONN 2, "xyx"')
            SIM900.write('*TRG')
            time.sleep(sleepTime/2)
            volt1 = SIM900.ask('VOLT? 1,1')
            volt2 = SIM900.ask('VOLT? 2,1')
            SIM900.write('xyx')
        except:
            print "Failed to collect Voltage reading."



        #Sort data
        iSource = ((float(volt1.strip()) - float(volt2.strip()))/resistor) #- (float(volt2.strip())/float(shunt))
       # data.append([str('%.3f' % bias), float(volt1), float(volt2), iSource])
        fileHandle = open(fileName, 'a')
        fileHandle.write(str('%.3f' % bias) + '\t' + str(float(volt1)) + '\t' + str(float(volt2)) + '\t' + str(iSource) + '\t' + str(temp)+ '\n')
    
    fileHandle.close()

    if temp>StopTemp:
        TempLow=False
    else:
        time.sleep(delay)
            
    q=q+1



#Turn off Voltage Source
SIM900.write('CONN 1, "xyx"')
SIM900.write('OPOF')
SIM900.write('xyx')


#reset voltmeter settings
SIM900.write('CONN 2, "xyx"')
time.sleep(0.5)

SIM900.write('TMOD 0')
time.sleep(0.5)

SIM900.write('AUTO 1, 15')
time.sleep(0.5)
SIM900.write('AUTO 2, 15')
time.sleep(0.5)
SIM900.write('AUTO 3, 15')
time.sleep(0.5)
SIM900.write('AUTO 4, 15')
time.sleep(0.5)

SIM900.write('*CLS')
time.sleep(0.5)
SIM900.write('*RST')
time.sleep(0.5)

SIM900.write('xyx')
time.sleep(0.5)


    
