# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSplashScreen, QGridLayout, QComboBox,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp, QLineEdit, QAction)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator, QIntValidator, QPainter, QColor, QFont, QPen
import time


def ip4addr():
    import netifaces

    xinterf = netifaces.interfaces()
    
    addr = []

    for x in xinterf:
        net = netifaces.ifaddresses(x)
        if 2 in net:
            ip = net[2][0]['addr']
            addr.append(ip)

    return addr

        
    

class XMLRPCConfig(QWidget):
    """
    Janela para configurar um servidor XML-RPC server

    Basically sets an IP and a port number
    """
    
    def __init__(self, server=False, ip=None, port=9500, parent=None):
        super(XMLRPCConfig, self).__init__(parent=parent)

        if server:
            import netifaces
            addr = ip4addr()
            self.iptext = QComboBox(self)
            for a in addr:
                self.iptext.addItem(a)
            if ip is not None:
                if 'localhost' in ip:
                    ip = '127.0.0.1'
                if ip in addr:
                    self.iptext.setCurrentIndex(addr.index(ip))
        else:

            self.iptext = QLineEdit()

            ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
            ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
            ipValidator = QRegExpValidator(ipRegex, self.iptext)

            self.iptext.setValidator(ipValidator)
            
            if ip is not None:
                self.iptext.setText(ip)
        
        iplab = QLabel("IP:")

        
        self.porttext = QLineEdit(self)
        self.porttext.setValidator(QIntValidator(1000, 65535, self.porttext))
        self.porttext.setText(str(port))
        portlab = QLabel("Porta: ")

        r1 = QHBoxLayout()
        r2 = QHBoxLayout()

        r1.addWidget(iplab)
        r1.addWidget(self.iptext)

        r2.addWidget(portlab)
        r2.addWidget(self.porttext)

        ver = QVBoxLayout()
        ver.addLayout(r1)
        ver.addLayout(r2)
                
        col0 = QVBoxLayout()
        group = QGroupBox("XML-RPC")
        group.setLayout(ver)
        col0.addWidget(group)
        self.setLayout(col0)
        
    def ipaddr(self):
        ip = self.iptext.currentText()
        return ip
    def port(self):
        return self.porttext.text()




if __name__ == '__main__':  
    #robo = roboteste.mesa()
    app = QApplication(sys.argv)
    
    win = XMLRPCConfig(False, "localhost")
    win.show()

    sys.exit(app.exec_())

