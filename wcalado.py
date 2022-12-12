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

from wcaladolib import comconfig
from wcaladolib import xmlrpcconfig
from wcaladolib import pyqtcalado

import xmlrpc.client
   
from multiprocessing import Process, freeze_support
import caladoxmlrpc
import argparse

import os.path

class WCaladoServer(QMainWindow):
    """Classe implementada a partir da classe QMainWindow e gera a tela inicial,
    responsavel pela configuracao inicial dos argumentos utilizados pelo XMLRPC"""
    
    def __init__(self, test=False,  srvip="localhost", srvport=9596, comport=None, initserver=True, client=False, parent=None):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        
        super(WCaladoServer, self).__init__(parent=parent)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.initvals = dict(test=test, ip=srvip, port=srvport, comport=comport, initserver=initserver, client=client)
        self.test = test
        self.client = client

        if client:
            self.initserver = False
        else:
            self.initserver = initserver
        
        self.draw_gui()
        #quit = QAction("Quit", self)
        #quit.triggered.connect(self.sair)
        
        self.process = None
        self.calado = None
        
        self.setWindowIcon(QIcon(os.path.join('wcaladolib', 'ipt.ico')))
        self.show()
    
    def draw_gui(self):
        self.setWindowTitle("Interface da calado giratória")
        #self.setGeometry(50, 50, 350, 400)
        vbox = QVBoxLayout()
        brow = QHBoxLayout()
        
        if not self.client:
            self.com = comconfig.COMConfig(True, self.initvals['comport'], baud=9600, size=8, parity='N', stop=1, parent=self)
        
            self.rpc = xmlrpcconfig.XMLRPCConfig(True, self.initvals['ip'], self.initvals['port'], parent=self)
            self.check_rpc = QCheckBox("Usar XML-RPC")
            self.check_rpc.stateChanged.connect(self.rpc_check_changed)
            if self.initserver:
                self.check_rpc.setChecked(True)
            else:
                self.check_rpc.setChecked(False)
            
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
        else: # cliente
            self.com = None
            self.check_rpc = None
            self.rpc = xmlrpcconfig.XMLRPCConfig(False, self.initvals['ip'], self.initvals['port'], parent=self)
            vbox.addWidget(self.rpc)
            
            self.config_button = QPushButton("Config")
            self.sair_button = QPushButton("Sair")
            vbox.addLayout(brow)
            brow.addWidget(self.config_button)
            brow.addWidget(self.sair_button)
            self.config_button.clicked.connect(self.init_client)
            self.sair_button.clicked.connect(self.sair)

            self.widget.setLayout(vbox)
                
        return
    
    def rpc_check_changed(self):
        if self.check_rpc.isChecked():
            self.rpc.setEnabled(True)
        else:
            self.rpc.setEnabled(False)
            
    def init_client(self):
        xaddr = self.rpc.ipaddr().strip()
        xport = self.rpc.port()
        time.sleep(1)
        serv = "http://{}:{}".format(xaddr, xport)
        m = xmlrpc.client.ServerProxy(serv)
        self.process = None
        err = False
        msg = "http://{}:{}".format(xaddr, xport)
        try:
            if m.ping() == 123:
                self.calado = m
                self.close()
                self.win = pyqtcalado.MainWindow(self.calado, msg, self.process)
                self.win.show()
                return
            else:
                err = True
        except:
            err = True

        if err:
            QMessageBox.warning(self, 'Erro', "Não foi possível encontrar o servidor XML-RPC. Tente outro IP ou porta", QMessageBox.Ok)
          
        
                
        
    def init_server(self):
        port = self.com.comport()
        baud = self.com.baudrate()
        size = self.com.bytesize()
        parity = self.com.parity()
        stopbits = self.com.stopbits()
        pr = None
        m = None
        self.process = None
        self.initserver = self.check_rpc.isChecked()
        msg = ''
        if self.initserver:
            xaddr = self.rpc.ipaddr().strip()
            xport = self.rpc.port()

            msg = "http://{}:{}".format(xaddr, xport)

            ntries = 0
            while True:
                ntries = ntries + 1
                pr = Process(target=caladoxmlrpc.start_server, args=(self.test, xaddr, xport, port, baud, size, parity, stopbits))
                pr.start()

                time.sleep(5)
                serv = "http://{}:{}".format(xaddr, xport)
                m = xmlrpc.client.ServerProxy(serv)
                try:
                    if m.ping() == 123:
                        break
                except:
                    pr.terminate()
                    QMessageBox.warning(self, 'Erro', "Não foi possível iniciar o servidor XML-RPC. Tentando novamente", QMessageBox.Ok)
                    if ntries > 4:
                        pr = None
                        m = None
                        break
                    time.sleep(4)
            
        else:
            #import caladoteste as calado
            if self.test:
                import wcaladolib.caladoteste as calado
                msg = "TESTE: {}".format(port)
            else:
                import wcaladolib.calado
                msg = "{}".format(port)
            
            m = calado.Robo(port, baud, size, parity, stopbits)
            time.sleep(3)
            try:
                if m.ping() != 123:
                    raise RuntimeError("Não comunicou")
            except:
                QMessage.critical(self, 'Erro', "Não foi possível iniciar o servidor XML-RPC",
                MessageBox.Ok)
                m = None
        self.process = pr
        self.calado = m
        if m is not None:
            self.close()
            self.win = pyqtcalado.MainWindow(self.calado, msg, self.process)
            self.win.show()
            return
        else:
            QMessage.critical(self, 'Erro', "Não foi possível criar uma interface com a Calado",
                              QMessageBox.Ok)
            
    def sair(self):
        """Finaliza o processo de comunicação e encerra o aplicativo"""
        qApp.quit()


if __name__ == '__main__':  
    freeze_support()
    
    parser = argparse.ArgumentParser(description="wcalado")
    parser.add_argument("-t", "--test", help="Interface teste da calado giratória", action="store_true")
    parser.add_argument("-i", "--ip", help="Endereço IP do servidor XML-RPC", default="localhost")
    parser.add_argument("-p", "--port", help="Porta XML-RPC do servidor XML-RPC", default=9596, type=int)
    parser.add_argument("-s", "--comport", help="Porta serial a ser utilizada", default="COM1")
    parser.add_argument("-n", "--serverless", help="Não inicie o servidor XML-RPC", action="store_true")
    parser.add_argument("-c", "--client", help="Criar interface para cliente de servidor XML-RPC", action="store_true")
    
    app = QApplication([]) # sys.argv

    args = parser.parse_args()
    
    # Create and display the splash screen
    splash_pix = QPixmap(os.path.join('wcaladolib', 'ipt.jpg'))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    
    win = WCaladoServer(args.test, args.ip, args.port, args.comport, not args.serverless, args.client)
    win.show()
    splash.finish(win)

    sys.exit(app.exec_())
