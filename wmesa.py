# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:51:03 2017

@author: felipenanini
"""

import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSplashScreen, QGridLayout, QComboBox,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp, QLineEdit, QAction)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator, QPainter, QColor, QFont, QPen
import time

import comconfig
import pyqtmesa

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler
    
from multiprocessing import Process
import mesaxmlrpc

class Welcome(QMainWindow):
    """Classe implementada a partir da classe QMainWindow e gera a tela inicial,
    responsavel pela configuracao inicial dos argumentos utilizados pelo XMLRPC"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        
        super().__init__(parent)
        self.setWindowTitle("Configurações Iniciais")
        self.setGeometry(50, 50, 350, 400)
        
        self.widget = comconfig.COMConfig(True, "COM1", baud=9600, size=8, parity='N', stop=1) #client_setting()
        self.setCentralWidget(self.widget)
        
        self.widget.button_conf.clicked.connect(self.configurar)
        self.widget.button_end.clicked.connect(self.sair)
        quit = QAction("Quit", self)
        quit.triggered.connect(self.sair)
        
        self.setWindowIcon(QIcon('ipt.jpg'))
        self.mesa = None
        self.show()

    def configurar(self):
        """Essa funcao e chamada pelo botao *Configurar* e toma os valores das entradas de texto
        como os novos valores de endereco e porta"""
        self.port = self.widget.comboport.currentText()
        self.baud = int(self.widget.combobaud.currentText())
        self.size = int(self.widget.combosize.currentText())
        self.parity = str(self.widget.comboparity.currentText())
        self.stop = int(self.widget.combostop.currentText())
        self.initUI(self.port, self.baud, self.size, self.parity, self.stop)
        

    def initUI(self, port="COM1", baud=9600, size=8, parity='N', stop=1):
        """initUI fecha a janela atual e abre a interface reponsável pelos comandos ao robo,
        definindo a nova comunicação com o servidor"""
        #print(port)
        port = "\\\\.\\" + port
        global pr
        if pr:
            pr.terminate()
        ip = 'localhost' #"192.168.0.100"
        iport = 9596
        pr = Process(target=mesaxmlrpc.start_server, args=(ip, iport, port, baud, size, parity, stop))
        pr.start()
        self.mesa = xmlrpc.client.ServerProxy("http://{}:{}".format(ip, iport))
        self.new_wind()
        #self.mesa = mesa.Robo(port = port, baudrate = baud, bytesize = size, parity = parity, stopbits = stop)
        #self.new_wind()
        
    def new_wind(self):
        """Fecha a janela de boas vindas e inicia a janela principal"""
        self.close()
        self.win = pyqtmesa.MainWindow(self.mesa)
        self.win.show()
    
    def sair(self):
        """Finaliza o processo de comunicação e encerra o aplicativo"""
        print("CHEGOU 1")
        if self.mesa:
            self.mesa.disconnect()
        if pr:
            pr.terminate()
            
        qApp.quit()


if __name__ == '__main__':  
    #robo = roboteste.mesa()
    app = QApplication(sys.argv)
    global inicial
    inicial = True
    global pr
    pr = ''
    
    # Create and display the splash screen
    splash_pix = QPixmap('ipt.jpg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    
    win = Welcome()
    win.show()
    splash.finish(win)

    sys.exit(app.exec_())
