from hardware import SIM900

SIM900_mf=SIM900('ASRL/dev/ttyUSB0::INSTR')
SIM900_mf.write(8, 'CURV 0, USER')
