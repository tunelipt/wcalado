# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSplashScreen, QGridLayout, QComboBox,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp, QLineEdit, QAction)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator, QIntValidator, QPainter, QColor, QFont, QPen
import time


def ip4addr(addlocalhost=True):
    import netifaces

    xinterf = netifaces.interfaces()
    
    addr = []

    for x in xinterf:
        net = netifaces.ifaddresses(x)
        if 2 in net:
            ip = net[2][0]['addr']
            addr.append(ip)
    if addlocalhost:
        if "localhost" not in addr and "127.0.0.1" not in addr:
            addr.append("localhost")
    
    return addr

        
    

class XMLRPCConfig(QWidget):
    """
    Janela para configurar um servidor XML-RPC server

    Basically sets an IP and a port number
    """
    
    def __init__(self, server=False, ip=None, port=9500, parent=None):
        super(XMLRPCConfig, self).__init__(parent=parent)

        self.server = server
        #if server:
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

        if not server:
            self.iptext.setEditable(True)
        
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
        return self.iptext.currentText()
    def port(self):
        return self.porttext.text()




if __name__ == '__main__':
    
    #robo = roboteste.mesa()
    import argparse
    parser = argparse.ArgumentParser(description="xmlrpcconfig")
    parser.add_argument("-i", "--ip", help="Endereço IP do servidor XML-RPC", default="localhost")
    parser.add_argument("-p", "--port", help="Porta XML-RPC do servidor XML-RPC", default=9596, type=int)
    parser.add_argument("-s", "--server", help="Porta XML-RPC do servidor XML-RPC", action="store_true")
    args = parser.parse_args()

    app = QApplication([])
    
    win = XMLRPCConfig(args.server, args.ip, args.port)
    win.show()
    r = app.exec_()

    print(win.ipaddr())
    print(win.port())
    sys.exit(r)

