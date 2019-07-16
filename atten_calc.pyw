from PyQt5 import QtGui, QtCore, QtWidgets
import sys


class AttenCalc(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(AttenCalc, self).__init__()
        self.initUi()
        
    def initUi(self):
        self.setGeometry(50, 50, 250, 170)
        self.setWindowTitle('Attenuation Calculator')
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        laser_rr_lab = QtWidgets.QLabel(self)
        laser_rr_lab.setText('Laser rep rate (Hz):')
        self.grid.addWidget(laser_rr_lab,0,0)
        self.laser_rr_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.laser_rr_ip,0,1)

        wav_lab = QtWidgets.QLabel(self)
        wav_lab.setText('Wavelength (nm):')
        self.grid.addWidget(wav_lab,1,0)
        self.wav_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.wav_ip,1,1)

        pwr_lab = QtWidgets.QLabel(self)
        pwr_lab.setText('Power at fibre end (W):')
        self.grid.addWidget(pwr_lab,2,0)
        self.pwr_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.pwr_ip,2,1)

        ppp_lab = QtWidgets.QLabel(self)
        ppp_lab.setText('Photons per pulse?:')
        self.grid.addWidget(ppp_lab,3,0)
        self.ppp_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.ppp_ip,3,1)

        calc_ip = QtWidgets.QPushButton('Calculate', self)
        calc_ip.clicked.connect(self.calc)
        self.grid.addWidget(calc_ip,4,0)

        self.atten_val = QtWidgets.QLabel(self)
        self.atten_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.atten_val.setLineWidth(1)
        self.grid.addWidget(self.atten_val,4,1)

        self.photons_per_sec = QtWidgets.QLabel(self)
        self.grid.addWidget(self.photons_per_sec,5,1)

        self.show()

    def calc(self):
        try:
            laser_r = float(self.laser_rr_ip.text())
            wav = float(self.wav_ip.text())
            pwr = float(self.pwr_ip.text())
            ppp = float(self.ppp_ip.text())
            atten, ph_p_pul = calculate_atten(laser_r, wav, pwr, ppp)
            ph_p_sec = round(ph_p_pul*laser_r)
            self.photons_per_sec.setText(str(ph_p_sec)+' photons per sec')
            self.atten_val.setText(str(atten)+ 'dB')
        except ValueError:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("Error with one of the entries!")
            self.msg.setWindowTitle("Error")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.show()
        


def calculate_atten(laser_r, wav, power, ideal_num):
        h = 6.626070040e-34
        c = 2.99792458e8
        ppp = []
        laser_rr=float(laser_r)
        energy_per_photon = h*(c/(float(wav)/1e9))
        for i in range(0,180):    #Goes through 0to180dB attenuations and calculates photons per pulse for each
            ph_p_pul = (float(power)*10**(-(float(i)/10))/energy_per_photon)*(1/laser_rr)
            ppp.append(ph_p_pul)
        nearest = min(ppp, key=lambda x:abs(x-ideal_num))    #Finds nearest value to ideal value
        return ppp.index(nearest), nearest

app = QtWidgets.QApplication(sys.argv)
GUI=AttenCalc()
sys.exit(app.exec_())