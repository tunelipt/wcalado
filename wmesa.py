# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:51:03 2017

@author: felipenanini
"""

import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSplashScreen, QGridLayout, QComboBox,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp,
                             QLineEdit, QAction, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator, QPainter, QColor, QFont, QPen
import time

import comconfig
import xmlrpcconfig

import pyqtmesa

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler
    
from multiprocessing import Process
import mesaxmlrpc

class WMesaServer(QMainWindow):
    """Classe implementada a partir da classe QMainWindow e gera a tela inicial,
    responsavel pela configuracao inicial dos argumentos utilizados pelo XMLRPC"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        
        super(WMesaServer, self).__init__(parent=parent)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        
        self.draw_gui()
        #quit = QAction("Quit", self)
        #quit.triggered.connect(self.sair)
        
        self.process = None
        self.mesa = None
        
        self.setWindowIcon(QIcon('ipt.jpg'))
        self.show()
    
    def draw_gui(self):
        self.setWindowTitle("Interface da mesa giratória")
        #self.setGeometry(50, 50, 350, 400)
        vbox = QVBoxLayout()
        brow = QHBoxLayout()

        self.com = comconfig.COMConfig(True, "COM1", baud=9600, size=8, parity='N', stop=1, parent=self)
        
        self.rpc = xmlrpcconfig.XMLRPCConfig(True, "localhost", 9596, parent=self)
        self.check_rpc = QCheckBox("Usar XML-RPC")
        self.check_rpc.stateChanged.connect(self.rpc_check_changed)
        self.check_rpc.setChecked(True)
        vbox.addWidget(self.com)
        vbox.addWidget(self.check_rpc)
        vbox.addWidget(self.rpc)
        
        self.config_button = QPushButton("Config")
        self.sair_button = QPushButton("Sair")
        vbox.addLayout(brow)
        brow.addWidget(self.config_button)
        brow.addWidget(self.sair_button)
        self.config_button.clicked.connect(self.init_server)
        self.sair_button.clicked.connect(self.sair)

        self.widget.setLayout(vbox)
        return
    
    def rpc_check_changed(self):
        if self.check_rpc.isChecked():
            self.rpc.setEnabled(True)
        else:
            self.rpc.setEnabled(False)
            
        
    def init_server(self):
        port = self.com.comport()
        baud = self.com.baudrate()
        size = self.com.bytesize()
        parity = self.com.parity()
        stopbits = self.com.stopbits()
        pr = None
        m = None
        self.process = None
        if self.check_rpc.isChecked():
            xaddr = self.rpc.ipaddr().strip()
            xport = self.rpc.port()

            ntries = 0
            while True:
                ntries = ntries + 1
                pr = Process(target=mesaxmlrpc.start_server, args=(xaddr, xport, port, baud,
                                                                   size, parity, stopbits))
                pr.start()

                time.sleep(5)

                m = xmlrpc.client.ServerProxy("http://{}:{}".format(xaddr, xport))
                try:
                    if m.ping() == 123:
                        break
                except:
                    pr.terminate()
                    QMessageBox.warning(self, 'Erro', "Não foi possível inicial o servidor XML-RPC. Tentando novamente", QMessageBox.Ok)
                    if ntries > 4:
                        pr = None
                        m = None
                        break
                    time.sleep(4)

        else:
            #import mesateste as mesa
            import mesa

            m = mesa.Robo(port, baud, size, parity, stopbits)
            time.sleep(3)
            try:
                if m.ping() != 123:
                    raise RuntimeError("Não comunicou")
            except:
                QMessage.critical(self, 'Erro', "Não foi possível iniciar o servidor XML-RPC",
                MessageBox.Ok)
                m = None
        self.process = pr
        self.mesa = m
        if m is not None:
            self.close()
            self.win = pyqtmesa.MainWindow(self.mesa, self.process)
            self.win.show()
            return
        else:
            QMessage.critical(self, 'Erro', "Não foi possível criar uma interface com a Mesa",
                              QMessageBox.Ok)
            
    def sair(self):
        """Finaliza o processo de comunicação e encerra o aplicativo"""
        qApp.quit()


if __name__ == '__main__':  
    #robo = roboteste.mesa()
    app = QApplication(sys.argv)
    
    # Create and display the splash screen
    splash_pix = QPixmap('ipt.jpg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    #time.sleep(1)
    
    win = WMesaServer()
    win.show()
    splash.finish(win)

    sys.exit(app.exec_())
