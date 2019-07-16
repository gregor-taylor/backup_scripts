from visa import *
import time as t
import math as m
import os as f
import Diode_Conversions as DC
#import matplotlib.pyplot as plt

#-----PRESETS-----#
iSourceRange    = 0.2e-04 #Max current in Amps
stepsUp         = 100 #200 points maximum before the Keithley wigs out
delay           = 20 #20ms minimum
StopTemp        = 10 #Temperature to stop taking IVs at
SleepTime       = 1 #Sleep time between IVs
Device = 'Device_F4_'
#-----SETUP-----#
data = []
temp = 0
dataHolderX = 0
dataHolderY = 0

keithley238_port    = 'GPIB1::17::INSTR'
SIM900_port         = 'GPIB0::2::INSTR'
keithley238 = instrument(keithley238_port)
SIM900 = instrument(SIM900_port)

#Check SIM900 Connection
try:
    SIM900.clear()
    SIM900.write('*CLS')
    SIM900Check = SIM900.ask('*IDN?')[:1]
    if SIM900Check is 'S':
        print "SIM900 Mainframe:\t\t Connected"
    else:
        print "SIM900 Mainframe:\t\t Not Connected"
except:
    print "SIM900 Mainframe:\t\t Not Connected"
t.sleep(1)

keithley238.clear()

#Get a value for the step amount
def round_to_1(x):
	return round(x, -int(m.floor(m.log10(abs(x))) - 2))
iSourceSteps = round_to_1(iSourceRange/stepsUp)
print iSourceSteps
#What's the smallest value of steps size? 100fA?

#-----PROGRAMSETUP-----#

#I Source, V Measure
keithley238.write('F1,1X')

def Keithley238Sweep(start, end, stepSci, stepNum, delay):
    keithley238.write('Q1,' + str(start) + ',' + str(end) + ',' + str(stepSci)
               + ',0,' + str(delay) + 'X')
    keithley238.write('N1X')
    keithley238.write('H0X')
    on = True
    while (on):
        t.sleep(0.2)
        stepCheck = int(keithley238.ask('U11X').strip()[3:])
        print str(stepCheck) + ' - ' + str(stepNum)
        if (stepCheck >= (stepNum)):
            on = False

#-----PROGRAM-----#          
TempLow=True
q=0
while TempLow :
    #Get Temperature
    print 'Run ' + str(q + 1)
    try:
        SIM900.write('CONN 1, "xyx"')
        Resi_SIM921_X = SIM900.ask('RVAL?').strip() #Which reading is the He3 head?
        SIM900.write('xyx')
    except:
        print "Failed to collect voltage reading."
        SIM900.clear()
    temp       = round(DC.RuO2Converter(float(Resi_SIM921_X)), 3)

    #Reading up
   # t.sleep(0.1)
    print 'From 0A to ' + str(iSourceRange) + 'A'
    Keithley238Sweep(0, iSourceRange, iSourceSteps, stepsUp, delay)
    stringUp = keithley238.ask('G5,2,2')
    stringUp = stringUp.split(',')
    #Reading Up Again
    #t.sleep(0.1)#2
    print 'From 0A to ' + str(iSourceRange) + 'A'
    Keithley238Sweep(0, iSourceRange, iSourceSteps, stepsUp, delay)
   # t.sleep(0.1)#2
    stringUp = keithley238.ask('G5,2,2')
    #print stringUp
    stringUp = stringUp.split(',')
    #Reading down
    print 'From ' + str(iSourceRange) + 'A to 0A'
    Keithley238Sweep(iSourceRange, 0, iSourceSteps, stepsUp, delay)
  #  t.sleep(0.1)#2
    stringDown = keithley238.ask('G5,2,2')
    stringDown = stringDown.split(',')
    #Reading down again
    print 'From 0A to -' + str(iSourceRange) + 'A'
    Keithley238Sweep(0, -iSourceRange, iSourceSteps, stepsUp, delay)
  #  t.sleep(0.1)#2
    stringDown2 = keithley238.ask('G5,2,2')
    stringDown2 = stringDown2.split(',')
    #Reading return
    print 'From -' + str(iSourceRange) + 'A to 0A'
    Keithley238Sweep(-iSourceRange, 0, iSourceSteps, stepsUp, delay)
  #  t.sleep(0.1)#2
    stringReturn = keithley238.ask('G5,2,2')
    stringReturn = stringReturn.split(',')

    stringAll = stringUp + stringDown + stringDown2 + stringReturn

   # print stringAll

    for i in range(len(stringAll)):
        if i%2 == 0 and i != 0:
            data.append([dataHolderX, dataHolderY])
        if i%2 == 0 and i != 0:
            dataHolderX = float(stringAll[i].split()[-1])
        elif i%2 != 0:
            dataHolderY = float(stringAll[i].split()[-1])

    fileHandle = open ('S:\\QSG\\Rankinator-PC\\Kleanthis\\Measurements\\Devices\\2p3um\\IV' + str(Device) + str(temp) + 'K_' + str(q) + '.txt', 'a' )
    for i in range(len(data)):
        fileHandle.write (str(data[i][0]) + '\t' + str(data[i][1]) + '\n')
    fileHandle.close()

    if temp>StopTemp:
        TempLow=False
    else:
        t.sleep(SleepTime)
            
    q=q+1
    '''
    #-----MATPLOT-----#
    dataX = []
    dataY = []

    for i in range(len(data)):
        dataX.append(data[i][0])
        dataY.append(data[i][1])

    plt.plot(dataX, dataY, 'b-')
    plt.xlabel('Source Current, A')
    plt.ylabel('Measured Voltage, V')
    plt.show()
    '''

    #Reset all the figures
    del data[:]
    

