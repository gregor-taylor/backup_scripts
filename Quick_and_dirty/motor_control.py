#requires thorlabs_apt library and 64 bit Thorlabs software.
####
#From github repo:
'''

    Install thorlabs_apt using setup.py

    Check whether your python is a 32 bit or 64 bit version and install the corresponding Thorlabs' APT software

    Copy APT.dll from the "APT installation path APT Server" directory to one of the following locations:
        Windows System32
        into the "thorlabs_apt" folder
        your python application directory
'''
#Also add "from ctypes import util" to the thorlabs_apt core.py
######

import thorlabs_apt as apt

motor_list = apt.list_available_devices()
motor_1 = apt.Motor(motor_list[0][1])
motor_2 = apt.Motor(motor_list[1][1])

#home both
motor_1.move_home(True)
motor_2.move_home(True)

motor_1.move_by(5)
motor_2.move_by(5)






