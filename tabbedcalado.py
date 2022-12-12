# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:35:00 2017

@author: felipenanini
"""

import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QSplashScreen, QAction,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator
import time



class RelativeMove(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pelos botoes
    de movimentacao relativa"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(RelativeMove, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para o movimento relativo e define como serao 
        dispostos de acordo com um *grid layout* dentro do *group box* criado"""
    
        relgroup = QGroupBox('Movimento Relativo')
        
        box = QHBoxLayout() 

        self.buttoncw = QPushButton('CW')
        self.buttonccw = QPushButton('CCW')
        
        self.buttoncw.setMaximumWidth(50)
        self.buttonccw.setMaximumWidth(50)
        self.buttoncw.setMaximumHeight(50)
        self.buttonccw.setMaximumHeight(50)
        
        box.addWidget(self.buttoncw)
        box.addWidget(self.buttonccw)

        relgroup.setLayout(box)
        
        return relgroup
    
class StepMove(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pelo passo da
    movimentacao relativa"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(StepMove, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para o passo do movimento relativo e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        
        Os passos são definidos pelos valores dos *sliders* associados a cada uma das coordenadas
        """
            
        stepgroup = QGroupBox('Step')
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
 
        self.btn_motor = QPushButton('Passo do motor')
        self.btn_motor.setStyleSheet("background-color:darkCyan;  border-style: outset; border-width: 2px; border-radius: 10px; border-color: blue;")
        self.btn_encoder = QPushButton('Passo do encoder')
        self.btn_motor.setMinimumHeight(50)
        self.btn_encoder.setMinimumHeight(50)

       #Definicao do sliderx
        self.sliderx = QSlider(Qt.Horizontal, self)
        self.sliderx.setFocusPolicy(Qt.StrongFocus)

        self.sliderx.setTickPosition(QSlider.TicksBothSides)
        self.sliderx.setTickInterval(10)
        self.sliderx.setSingleStep(1)
        self.sliderx.setValue(10)
        self.sliderx.setMinimum(0)
        self.sliderx.setMaximum(180)

        self.labelx = QLabel('10')
        self.labelx.setMinimumHeight(40)
        self.labelx.setAlignment(Qt.AlignCenter)
        stepx = QLabel("Ângulo")
        
        self.entrada_x = QLineEdit(self)
        self.entrada_x.setText('10')
        regex = QRegExp("\d{0,3}(\.\d{0,3})?")
        validator=QRegExpValidator(regex, self.entrada_x)
        
        self.entrada_x.setValidator(validator)
        
        vbox.addLayout(hbox2)
        vbox.addWidget(self.labelx)
        vbox.addLayout(hbox1)
        hbox2.addWidget(self.btn_motor)
        hbox2.addWidget(self.btn_encoder)
        hbox1.addWidget(stepx,0.5)
        hbox1.addWidget(self.sliderx,6)
        hbox1.addWidget(self.entrada_x,1)
        
        self.entrada_x.textChanged[str].connect(lambda text: self.changeCursor(text, self.sliderx))
        self.sliderx.valueChanged[int].connect(lambda value: self.changeValue(value, self.labelx))
        self.sliderx.setMinimumHeight(40)

        stepgroup.setLayout(vbox)
        self.resize(150, 250)
        return stepgroup
    
    
    def changeCursor(self, text, sliders):
        """changeValue toma os valores dos *line edits* a cada alteracao feita e repassa para o valor
        dos *sliders* respectivas.
        
        Keyword arguments:
        value -- o valor referente ao *line edit* alterado
        sliders -- o *slider* a ser modificado
        """
        
        slider = sliders
        if text:
            slider.setValue(float(text))
        
    def changeValue(self, value, labels):
        """changeValue toma os valores dos *sliders* a cada alteracao feita e repassa para o texto
        das *labels* respectivas.
        
        Keyword arguments:
        value -- o valor referente ao *slider* alterado
        lables -- o *label* a ser modificado
        """
        
        label = labels
        label.setText(str(value))
        
class Reference(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela definicao
    das referencias do robo"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Reference, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para a definicao da referencia do robo e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        """
        
        refgroup = QGroupBox('Referencia')
        
        vbox = QVBoxLayout()
        
        self.buttonref = QPushButton("Ponto atual como referencia")
        self.buttonabsref = QPushButton("Referencia absoluta")
        vbox.addWidget(self.buttonref)
        vbox.addWidget(self.buttonabsref)
        refgroup.setLayout(vbox)
        
        return refgroup


class Home(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel por ordenar o robo
    a tomar a posição de referencia"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Home, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
    def interface(self):        
        """interface gera os botoes para enviar o robo para a posição de referencia e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        """
        
        homegroup = QGroupBox('Home')
        vbox = QVBoxLayout()
        
        self.buttonxp = QPushButton("Home +")
        self.buttonxm = QPushButton("Home -")
        vbox.addWidget(self.buttonxp)
        vbox.addWidget(self.buttonxm)
        homegroup.setLayout(vbox)
        
        return homegroup


class Move(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela
    movimentação do robo para um ponto específico"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Move, self).__init__(parent) 
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para enviar o robo para uma posição específica e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        
        Os valores dessa posição são definidos por *sliders* referentes a cada coordenada.
        """
        
        movegroup = QGroupBox("Movimento")
        
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        
        self.button = QPushButton("Mover")
        self.button.setMinimumHeight(50)
        vbox.addWidget(self.button)

        #Definicao do sliderx
        self.slidermx = QSlider(Qt.Horizontal, self)
        self.slidermx.setFocusPolicy(Qt.StrongFocus)
        self.slidermx.setSingleStep(1)
        self.slidermx.setValue(0)
        self.slidermx.setMinimum(-180)
        self.slidermx.setMaximum(180)
        
        self.move_x = QLineEdit(self)
        self.move_x.setText('0')
        regex = QRegExp("-?\d{0,3}(\.\d{0,3})?")
        validator=QRegExpValidator(regex, self.move_x)
        
        self.move_x.setValidator(validator)
        
        self.posx = QLabel('0')
        self.posx.setAlignment(Qt.AlignCenter)
        labelx = QLabel("Ângulo")
        labelx.setMinimumHeight(40)

        vbox.addWidget(self.posx)
        vbox.addLayout(hbox1)
        hbox1.addWidget(labelx,1)
        hbox1.addWidget(self.slidermx,7)
        hbox1.addWidget(self.move_x,1)
        
        self.move_x.textChanged[str].connect(lambda text: self.changeCursor(text, self.slidermx))
        self.slidermx.valueChanged[int].connect(lambda value: self.changeValue(value, self.posx))
        self.slidermx.setMinimumHeight(40)
        
        movegroup.setLayout(vbox)
        
        return movegroup
    
    def changeCursor(self, text, sliders):
        """changeValue toma os valores dos *line edits* a cada alteracao feita e repassa para o valor
        dos *sliders* respectivas.
        
        Keyword arguments:
        value -- o valor referente ao *line edit* alterado
        sliders -- o *slider* a ser modificado
        """
        
        slider = sliders
        if text:
            if text[0] == '-' and len(text) >= 2:
                slider.setValue(-float(text[1:]))
            elif text[0] != '-':
                slider.setValue(float(text))
    
    def changeValue(self, value, labels):
        """changeValue toma os valores dos *sliders* a cada alteracao feita e repassa para o texto
        das *labels* respectivas.
        
        Keyword arguments:
        value -- o valor referente ao *slider* alterado
        lables -- o *label* a ser modificado
        """
        
        label = labels
        label.setText(str(value))


class Position(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela
    verificação da posição do robo"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Position, self).__init__(parent)    
        #groupbox de posicao
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para verificar a posição do robo e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        """
        
        posgroup = QGroupBox('Posicao')
        
        vbox = QVBoxLayout()
        
        self.buttonpos = QPushButton("Posicao")
        self.buttonpos.setMinimumHeight(35)
        self.labelp = QLabel('')
        self.labelp.setAlignment(Qt.AlignCenter)
        
        self.buttonabspos = QPushButton("Posicao absoluta")
        self.buttonabspos.setMinimumHeight(35)
        self.labelabsp = QLabel('')
        self.labelabsp.setAlignment(Qt.AlignCenter)

        vbox.addWidget(self.buttonpos)
        vbox.addWidget(self.labelp)
        vbox.addWidget(self.buttonabspos)
        vbox.addWidget(self.labelabsp)
        posgroup.setLayout(vbox)

        return posgroup

class Stop(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela
    parada de emergencia"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Stop, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera o botao para parada de emergencia e define as caracteristicas
        do botao, colocando-o dentro do *group box*.
        """
        
        stopgroup = QGroupBox("Parada")
        
        vbox = QVBoxLayout()
        
        self.buttons = QPushButton("PARADA IMEDIATA")
        self.buttons.setMinimumHeight(70)
        self.buttons.setStyleSheet("background-color: red; border-style: outset; border-width: 2px; border-radius: 10px; border-color: black;")
        
        
        vbox.addWidget(self.buttons)
        stopgroup.setLayout(vbox)
    
        return stopgroup
    
class Clear(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela
    limpeza dos dados"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Clear, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):        
        """interface gera o botao para limpar os dados e define as caracteristicas
        do botao, colocando-o dentro do *group box*.
        """
        
        cleargroup = QGroupBox("Limpar")
        
        vbox = QVBoxLayout()
        
        self.buttonc = QPushButton("Limpar")
        vbox.addWidget(self.buttonc)
        cleargroup.setLayout(vbox)
        
        return cleargroup

class Tab1(QWidget):
    """Tab1 e responsavel pela juncao e disposicao das *Group Boxes* necessarias na primeira
    aba da interface final"""
    
    def __init__(self):
        """Funcao __init__ para definir o layout geral"""
        
        super().__init__()
        
        column1 = QVBoxLayout()
        self.relativo = RelativeMove()
        self.step = StepMove()
        self.position = Position()
        self.stop = Stop()
        
        column1.addWidget(self.relativo,1)
        column1.addWidget(self.step,2)
        column1.addWidget(self.stop,1)
        column1.addWidget(self.position,1)
        
        
        self.setLayout(column1)

class Tab2(QWidget):
    """Tab2 e responsavel pela juncao e disposicao das *Group Boxes* necessarias na segunda
    aba da interface final"""
    
    def __init__(self):
        """Funcao __init__ para definir o layout geral"""
        
        super().__init__()
        column2 = QVBoxLayout()
        self.home = Home()
        self.position = Position()
        self.stop = Stop()
        self.clear = Clear()
        
        column2.addWidget(self.home)
        column2.addWidget(self.stop)
        column2.addWidget(self.clear)
        column2.addWidget(self.position)
        

        self.setLayout(column2)
    
class Tab3(QWidget):
    """Tab3 e responsavel pela juncao e disposicao das *Group Boxes* necessarias na terceira
    aba da interface final"""
    
    def __init__(self):
        """Funcao __init__ para definir o layout geral"""
        
        super().__init__()
        
        column3 = QVBoxLayout()
        self.move = Move()
        self.position = Position()
        self.stop = Stop()
        self.clear = Clear()
                
        column3.addWidget(self.move)
        column3.addWidget(self.stop)
        column3.addWidget(self.clear)
        column3.addWidget(self.position)
        
        self.setLayout(column3)
        
class Tab4(QWidget):
    """Tab4 e responsavel pela juncao e disposicao das *Group Boxes* necessarias na quarta
    aba da interface final"""
    
    def __init__(self):
        """Funcao __init__ para definir o layout geral"""
        
        super().__init__()
    
        column4 = QVBoxLayout()
        self.ref = Reference()
        self.position = Position()
        self.stop = Stop()
        self.clear = Clear()
        
        column4.addWidget(self.ref)
        column4.addWidget(self.stop)
        column4.addWidget(self.clear)
        column4.addWidget(self.position)
        
        self.setLayout(column4)
    
class client_setting(QWidget):
    """client_setting exibe as entradas de texto para a definicao do endereço e porta utilizados
    pela comunicação XMLRPC"""
    
    def __init__(self, inicial=False):
        """Funcao __init__ para definir o layout geral"""
        
        self.inicial = inicial
        super().__init__()
        self.title = "Configuracoes da serial"
        
        self.comboport = QLineEdit(self)
        self.comboport.setText('COM1')
        self.comboport.setMaximumWidth(150)
        self.labelport = QLabel('Porta:')
        
        self.combobaud = QComboBox(self)
        self.combobaud.addItem('9600')
        self.combobaud.setMaximumWidth(150)
        self.labelbaud = QLabel('Baud Rate:')

        self.combosize = QComboBox(self)
        self.combosize.addItem('8')
        self.combosize.addItem('7')
        self.combosize.addItem('6')
        self.combosize.addItem('5')
        self.combosize.setMaximumWidth(150)
        self.labelsize = QLabel('Tamanho do Byte:')
        
        self.comboparity = QComboBox(self)
        self.comboparity.addItem('N')
        self.comboparity.addItem('E')
        self.comboparity.addItem('O')
        self.comboparity.addItem('M')
        self.comboparity.addItem('S')
        self.comboparity.setMaximumWidth(150)
        self.labelparity = QLabel('Paridade:')
        
        self.combostop = QComboBox(self)
        self.combostop.addItem('1')
        self.combostop.addItem('2')
        self.combostop.setMaximumWidth(150)
        self.labelstop = QLabel('Bit de Parada:')
        
        self.button_end = QPushButton('Sair')
        self.button_conf = QPushButton('Configurar')
        
        column = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()

        column.addLayout(row1)
        row1.addWidget(self.labelport)
        row1.addWidget(self.comboport)
        
        column.addLayout(row2)
        row2.addWidget(self.labelbaud)
        row2.addWidget(self.combobaud)
        
        column.addLayout(row3)
        row3.addWidget(self.labelsize)
        row3.addWidget(self.combosize)
        
        column.addLayout(row4)
        row4.addWidget(self.labelparity)
        row4.addWidget(self.comboparity)
        
        column.addLayout(row5)
        row5.addWidget(self.labelstop)
        row5.addWidget(self.combostop)
        
        column.addWidget(self.button_conf)
 
        column.addStretch(1)
        column.addWidget(self.button_end)
       
        self.setLayout(column)
        
class Welcome(QMainWindow):
    """Classe implementada a partir da classe QMainWindow e gera a tela inicial,
    responsavel pela configuracao inicial dos argumentos utilizados pelo XMLRPC"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        self.inicial = True

        super().__init__(parent)
        self.setWindowTitle("Configurações Iniciais")
        self.setGeometry(50, 50, 350, 400)
        
        self.widget = client_setting()
        self.setCentralWidget(self.widget)
        
        self.widget.button_conf.clicked.connect(self.configurar)
        self.widget.button_end.clicked.connect(self.sair)
        
        self.setWindowIcon(QIcon('ipt.jpg'))
        
        self.show()

    def configurar(self):
        """Essa funcao e chamada pelo botao *Configurar* e toma os valores das entradas de texto
        como os novos valores de endereco e porta"""     
        self.port = self.widget.comboport.text()
        self.baud = int(self.widget.combobaud.currentText())
        self.size = int(self.widget.combosize.currentText())
        self.parity = str(self.widget.comboparity.currentText())
        self.stop = int(self.widget.combostop.currentText())
        self.initUI(self.port, self.baud, self.size, self.parity, self.stop)

    def initUI(self, port, baud, size, parity, stop):
        """initUI fecha a janela atual e abre a interface reponsável pelos comandos ao robo,
        definindo a nova comunicação com o servidor"""
        self.calado = calado.Robo(port = port, baudrate = baud, bytesize = size, parity = parity, stopbits = stop)
        self.new_wind()
        
    def new_wind(self):
        """Fecha a janela de boas vindas e inicia a janela principal"""
        self.close()
        self.win = MainWindow(self.calado)
        self.win.show()
        
    def sair(self):
        qApp.quit()
        
class MainWindow(QMainWindow):
    """Classe implementada sobre a partir da classe QMainWindow e gera a tela de comandos,
    responsavel pela disposicao final das guias"""
    
    def __init__(self, calado, parent=None):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        
        self.calado = calado
        
        super().__init__(parent)
        self.setWindowTitle("Movimentador do Tunel")
        self.setGeometry(50, 50, 500, 550)
        
        self.table_widget = MyTableWidget(self.calado, self)
        self.setCentralWidget(self.table_widget)
        
        exitAct = QAction(QIcon('exit.png'), '&Sair', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Sair do Programa')
        exitAct.triggered.connect(self.sair)
        
        configAct = QAction(QIcon('configura.jpg'), '&Configurar', self)
        configAct.setStatusTip('Configurar endereço')
        configAct.triggered.connect(self.new_wind)
       
        menubar = self.menuBar()
        configMenu = menubar.addMenu('&Configurações')
        configMenu.addAction(configAct)
        configMenu.addAction(exitAct)
        
        self.setWindowIcon(QIcon('ipt.jpg'))
        self.show()
        
    def new_wind(self):
        """Fecha a janela de boas vindas e inicia a janela principal"""
        self.close()
        self.win = Welcome()
        self.win.show()
        
    def sair(self):
        """Finaliza o processo de comunicação e encerra o aplicativo"""
        self.calado.disconnect()
        qApp.quit()

class MyTableWidget(QWidget):        
    """Classe que cria o *layout* de guias e preenche com as classes anteriores,
    definindo tambem a funcionalidade de cada um dos botoes"""
    
    def __init__(self, calado, parent):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        
        self.calado = calado
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
                
        self.tabs = QTabWidget()
        self.tab1 = Tab1()
        self.tab2 = Tab2()
        self.tab3 = Tab3()
        self.tab4 = Tab4()
        self.tabs.resize(350,300)  
 
        # Add tabs
        self.tabs.addTab(self.tab1,"Relativo")
        self.tabs.addTab(self.tab2,"Home")
        self.tabs.addTab(self.tab3,"Movimento")
        self.tabs.addTab(self.tab4,"Referência")
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        self.tab1.relativo.buttoncw.clicked.connect(self.rmoveClicked)
        self.tab1.relativo.buttonccw.clicked.connect(self.rmoveClicked)
        self.tab1.step.btn_encoder.clicked.connect(self.stepEncoderClicked)
        self.tab1.step.btn_motor.clicked.connect(self.stepMotorClicked)
        self.tab4.ref.buttonref.clicked.connect(self.refClicked)
        self.tab4.ref.buttonabsref.clicked.connect(self.absrefClicked)
        
        self.tab2.home.buttonxp.clicked.connect(self.homexClicked)
        self.tab2.home.buttonxm.clicked.connect(self.homexClicked)
        self.tab3.move.button.clicked.connect(self.moveClicked)

        select = [self.tab1, self.tab2, self.tab3, self.tab4]
        for tab in select:
            tab.position.buttonpos.clicked.connect(self.posClicked)
            tab.position.buttonabspos.clicked.connect(self.absposClicked)
            tab.stop.buttons.clicked.connect(self.stopClicked)
            if tab != self.tab1:
                tab.clear.buttonc.clicked.connect(self.clearClicked)  
    
    def rmoveClicked(self):
        """Utiliza o metodo sender dos botoes para a movimentacao relativa de cada uma das coordenadas,
        levando os valores do respectivo passo em consideração.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        clickedButton = self.sender()
        digitFunction = clickedButton.text()
        p = self.calado.position()['x']
        print (p)
        if digitFunction[1] == 'W':
            x = (-1)*float(self.tab1.step.labelx.text())
            if x+p>180 or x+p<-180:
                x = x + 360          
            self.calado.rmove(x)
        
        elif digitFunction[1] == "C":
            x = float(self.tab1.step.labelx.text())
            if x+p>180 or x+p<-180:
                x = x - 360
            self.calado.rmove(x)
        x=0
        self.posClicked(True)
        self.absposClicked(True)
        
    def moveClicked(self):
        """Envia o robo a posição indicada pelos *sliders* da classe Move.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        x = float(self.tab3.move.posx.text())
        
        y = x%360
        if y:
            x = x - 360*y 
        
        if x%180:
            x = x - 360
        
        self.calado.move(x)
        self.posClicked(True)
        self.absposClicked(True)
        
    def homexClicked(self):
        """Envia o robo a posição de referencia em X.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        clickedButton = self.sender()
        sign = clickedButton.text()[-1]
        self.calado.home(sign)
        self.posClicked(True)
        self.absposClicked(True)
        
    def posClicked(self, changed = False):
        """Obtem a posicao do robo e a imprime.
        
        Chamando o comando por meio do arquivo passado por *self.calado*
        
        Keyword arguments:
        changed -- indica alteracao na posicao, para valor verdadeiro apaga a posicao da interface"""
        
        p = self.calado.position()['x']
        if changed:
            self.text1 = ''
            self.changed = False
        else:
            if p < 0:
                p += 360*abs(p//360)
            p = p%360
            self.text1 = "Ângulo = {}".format(format(p, '.3f'))
        select = [self.tab1, self.tab2, self.tab3, self.tab4]
        for tab in select:
            tab.position.labelp.setText(self.text1)
        
    def absposClicked(self, changed = False):
        """Obtem a posicao absoluta do robo e a imprime.
        
        Chamando o comando por meio do arquivo passado por *self.calado*
        
        Keyword arguments:
        changed -- indica alteracao na posicao, para valor verdadeiro apaga a posicao da interface"""
        
        p = self.calado.abs_position()['x']
        if changed:
            self.text2 = ''
            self.changed = False
        else:
            if p < 0:
                p += 360*abs(p//360)
            p = p%360
            self.text2 = "Ângulo = {}".format(format(p, '.3f'))
        select = [self.tab1, self.tab2, self.tab3, self.tab4]
        for tab in select:
            tab.position.labelabsp.setText(self.text2)
        
    def refClicked(self):
        """Define a posicao atual como referencia para o robo.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        self.posClicked(True)
        self.absposClicked(True)
        self.calado.set_reference()
        
    def absrefClicked(self):
        """Define a posicao atual como referencia absoluta para o robo.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        self.posClicked(True)
        self.absposClicked(True)
        self.calado.set_abs_reference()
        
    def stopClicked(self):
        """Parada emergencial da movimentacao.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        self.calado.stop()
        print("Funcionando ate aqui")
        self.posClicked(True)
        self.absposClicked(True)
        
    def clearClicked(self):
        """Limpa os dados enviados.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        self.calado.clear()
        self.posClicked(True)
        self.absposClicked(True)
        
    def stepMotorClicked(self):
        """Muda o metodo de passos enviados do controlador para o valor de passos 
        calibrados para o motor."""
        
        self.calado.step_motor()
        self.tab1.step.btn_motor.setStyleSheet("background-color:darkCyan;  border-style: outset; border-width: 2px; border-radius: 10px; border-color: blue;")
        self.tab1.step.btn_encoder.setStyleSheet("")
        
    def stepEncoderClicked(self):
        """Muda o metodo de passos enviados do controlador para o valor de passos 
        calibrados pelo encoder."""
        
        self.calado.step_encoder()
        self.tab1.step.btn_encoder.setStyleSheet("background-color:darkCyan;  border-style: outset; border-width: 2px; border-radius: 10px; border-color: blue;")
        self.tab1.step.btn_motor.setStyleSheet("")
        
import calado

if __name__ == '__main__':  
    app = QApplication(sys.argv)
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
