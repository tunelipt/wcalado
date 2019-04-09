
import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSplashScreen, QGridLayout, QComboBox,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp, QLineEdit, QAction)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator, QPainter, QColor, QFont, QPen
import time
import serial.tools.list_ports


import serial.tools.list_ports

class COMConfig(QWidget):
    """
    Janela para configurar a 
    client_setting exibe as entradas de texto para a definicao do endereço e porta utilizados
    pela comunicação XMLRPC
    """

    def __init__(self, scanports=True, port="COM1", baud=9600, size=8, parity='N', stop=1, parent=None):

        QWidget.__init__(self, parent=parent)


        self.comboport = QComboBox()
        self.labelport = QLabel('Porta:')
        if scanports:
            # Escanear as portas seriais disponíveis
            portlst = [x.device for x in serial.tools.list_ports.comports()]

            defaultport = None
            if port is not None:
                for dev in portlst:
                    if port in dev:
                        defaultport = dev
                        break
            
             
            for dev in portlst:
                self.comboport.addItem(dev)
            if defaultport is not None:
                self.comboport.setCurrentIndex(portlst.index(defaultport))

        else:
            self.comboport.addItem(port)
        xbaud = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 56000, 57600, 115200]
        xsize = [5, 6, 7, 8]
        xparity = ['N', 'E', 'O', 'M', 'S']
        xstop = [1, 1.5, 2]
        
        self.combobaud = QComboBox()
        for x in xbaud:
            self.combobaud.addItem(str(x))
        self.combobaud.setMaximumWidth(150)
        self.combobaud.setCurrentIndex(xbaud.index(baud))
        self.labelbaud = QLabel('Baud Rate:')

        self.combosize = QComboBox()
        for x in xsize:
            self.combosize.addItem(str(x))
        self.combosize.setCurrentIndex(xsize.index(size))
        self.combosize.setMaximumWidth(150)
        self.labelsize = QLabel('Tamanho do Byte:')
        
        self.comboparity = QComboBox()
        for x in xparity:
            self.comboparity.addItem(x)
        self.comboparity.setCurrentIndex(xparity.index(parity))
        self.comboparity.setMaximumWidth(150)
        self.labelparity = QLabel('Paridade:')
        
        self.combostop = QComboBox()
        for x in xstop:
            self.combostop.addItem(str(x))
        self.combostop.setCurrentIndex(xstop.index(stop))
        self.combostop.setMaximumWidth(150)
        self.labelstop = QLabel('Bit de Parada:')
        
        column = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()

        column.addLayout(row1)
        column.addLayout(row2)
        column.addLayout(row3)
        column.addLayout(row5)
        column.addLayout(row4)
        col0 = QVBoxLayout()

        row1.addWidget(self.labelport)
        row1.addWidget(self.comboport)
        
        row2.addWidget(self.labelbaud)
        row2.addWidget(self.combobaud)
        
        row3.addWidget(self.labelsize)
        row3.addWidget(self.combosize)
        
        row4.addWidget(self.labelparity)
        row4.addWidget(self.comboparity)
        
        row5.addWidget(self.labelstop)
        row5.addWidget(self.combostop)


        groupbox = QGroupBox("Config. COM")
        
        groupbox.setLayout(column)
        col0.addWidget(groupbox)
        self.setLayout(col0)
        
    def comport(self):
        return self.comboport.currentText()
    def baudrate(self):
        return int(self.combobaud.currentText())
    def bytesize(self):
        return int(self.combosize.currentText())
    def parity(self):
        return self.comboparity.currentText()
    def stopbits(self):
        x = self.combostop.currentText()
        if x=='2':
            return 2
        elif x=='1.5':
            return 1.5
        else:
            return 1
    
        
            
if __name__ == '__main__':  
    #robo = roboteste.mesa()
    app = QApplication(sys.argv)
    
    win = COMConfig(False, port="COM1", baud=9600, size=8, parity='N', stop=1)
    win.show()

    sys.exit(app.exec_())

