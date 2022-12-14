# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:51:03 2017

@author: felipenanini
"""

import sys
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSplashScreen, QGridLayout, QComboBox,
                             QGroupBox, QPushButton, QApplication, QSlider, QMainWindow, qApp, QLineEdit, QAction, QCheckBox)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator, QDoubleValidator, QPainter, QColor, QFont, QPen
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
        
        box = QVBoxLayout() 

        self.buttonup = QPushButton('Subir')
        self.buttondo = QPushButton('Descer')
        
        self.buttonup.setMaximumWidth(85)
        self.buttondo.setMaximumWidth(85)
        self.buttonup.setMaximumHeight(50)
        self.buttondo.setMaximumHeight(50)
        
        box.addWidget(self.buttonup)
        box.addWidget(self.buttondo)

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
        
        Os passos s??o definidos pelos valores dos *sliders* associados a cada uma das coordenadas
        """
            
        stepgroup = QGroupBox('Step')
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
 
        self.btn_motor = QPushButton('Passo do motor')
        self.btn_encoder = QPushButton('Passo do encoder')
        self.btn_encoder.setStyleSheet("background-color:darkCyan;  border-style: outset; border-width: 2px; border-radius: 10px; border-color: blue;")
        self.btn_motor.setMinimumHeight(50)
        self.btn_encoder.setMinimumHeight(50)

        self.btn_motor.setEnabled(False)
        self.btn_encoder.setEnabled(False)
        
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
        stepx = QLabel("Passo (mm)")
        
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
        hbox1.addWidget(stepx, 1)
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
            slider.setValue(int(text))
        
    def changeValue(self, value, labels):
        """changeValue toma os valores dos *sliders* a cada alteracao feita e repassa para o texto
        das *labels* respectivas.
        
        Keyword arguments:
        value -- o valor referente ao *slider* alterado
        lables -- o *label* a ser modificado
        """
        
        label = labels
        label.setText(str(value))
        self.entrada_x.setText(str(value))
        
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
        
        refgroup = QGroupBox('Refer??ncia')
        
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        lab = QLabel("Refer??ncia")
        self.valref = QLineEdit(self)
        self.valref.setText("0")
        validator = QDoubleValidator()
        self.valref.setValidator(validator)
        hbox.addWidget(lab)
        hbox.addWidget(self.valref)
        
        self.buttonref = QPushButton("Ponto atual como refer??ncia")
        self.buttonabsref = QPushButton("Refer??ncia absoluta")

        vbox.addLayout(hbox)
        vbox.addWidget(self.buttonref)
        vbox.addWidget(self.buttonabsref)

        refgroup.setLayout(vbox)
        
        return refgroup


class Home(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel por ordenar o robo
    a tomar a posi????o de referencia"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Home, self).__init__(parent)
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
    def interface(self):        
        """interface gera os botoes para enviar o robo para a posi????o de referencia e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        """
        
        homegroup = QGroupBox('Home')
        vbox = QVBoxLayout()
        
        self.buttonxp = QPushButton("Home +")
        self.buttonxm = QPushButton("Home -")
        vbox.addWidget(self.buttonxp)
        vbox.addWidget(self.buttonxm)
        homegroup.setLayout(vbox)
        homegroup.setEnabled(False)
        return homegroup


class Move(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela
    movimenta????o do robo para um ponto espec??fico"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Move, self).__init__(parent) 
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para enviar o robo para uma posi????o espec??fica e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        
        Os valores dessa posi????o s??o definidos por *sliders* referentes a cada coordenada.
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
        self.slidermx.setMinimum(-360)
        self.slidermx.setMaximum(360)
        self.slidermx.setMinimumWidth(120)
        
        self.move_x = QLineEdit(self)
        self.move_x.setText('0')
        regex = QRegExp("-?\d{0,3}(\.\d{0,3})?")
        validator=QRegExpValidator(regex, self.move_x)
        
        self.move_x.setValidator(validator)
        
        self.posx = QLabel('0')
        self.posx.setAlignment(Qt.AlignCenter)
        labelx = QLabel("Posi????o")
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
                slider.setValue(-int(text[1:]))
            elif text[0] != '-':
                slider.setValue(int(text))
    
    def changeValue(self, value, labels):
        """changeValue toma os valores dos *sliders* a cada alteracao feita e repassa para o texto
        das *labels* respectivas.
        
        Keyword arguments:
        value -- o valor referente ao *slider* alterado
        lables -- o *label* a ser modificado
        """
        
        label = labels
        label.setText(str(value))
        self.move_x.setText(str(value))


class Position(QWidget):
    """Classe criada a partir da classe QWidget, 
    para gerar a interface responsavel pela
    verifica????o da posi????o do robo"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral"""
        
        super(Position, self).__init__(parent)    
        #groupbox de posicao
        column = QVBoxLayout()
        column.addWidget(self.interface())
        
        self.setLayout(column)
        
        
    def interface(self):
        """interface gera os botoes para verificar a posi????o do robo e define como serao 
        dispostos de acordo com *Box Layouts* dentro do *group box* criado.
        """
        
        posgroup = QGroupBox('Posi????o')
        
        vbox = QVBoxLayout()
        
        self.buttonpos = QPushButton("Posi????o")
        self.buttonpos.setMinimumHeight(35)
        self.labelp = QLabel('')
        self.labelp.setAlignment(Qt.AlignCenter)
        
        self.buttonabspos = QPushButton("Posi????o absoluta")
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
        self.buttons.setMinimumWidth(150)
        self.buttons.setMinimumHeight(400)
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
        
        self.button = QPushButton("Limpar")
        vbox.addWidget(self.button)
        cleargroup.setLayout(vbox)
        
        return cleargroup


class help_text(QWidget):
    """Implementa os textos da tela de ajuda"""
    
    def __init__(self, inicial=False):
        """Funcao __init__ para definir o layout geral"""
        super().__init__()
        
        self.texto1 = "Movimento relativo:"
        self.texto2 = """Para a mudan??a do caladoem rela????o ?? posi????o atual, devem ser utilizados os"""
        self.texto3 = """bot??es 'Subir' e 'Descer',os quais tomam os valores do slider do grupo"""
        self.texto4 = """'Step' como o valor a ser adicionado ou subtra??do da posi????o de partida."""
        
        self.texto5 = "Movimento absoluto:"
        self.texto6 = """Para a mudan??a do calado em rela????o ?? refer??ncia absoluta,"""
        self.texto7 = """o bot??o'Mover' deve ser utilizado, tal bot??o utiliza o valor do slider""" 
        self.texto8 = """ no grupo 'Movimento' como o ??ngulo referente ?? posi????o final do movimento."""
        self.texto9 = "Posi????o:"
        self.texto10 = """Para obter a posi????o atual do calado utiliza-se os bot??es 'Posi????o' e""" 
        self.texto11 = """'Posi????o Absoluta', que se referem ??s posi????es relativas ao que ?? estabelecido"""
        self.texto12 = """pelos bot??es 'Ponto atual como refer??ncia' e 'Refer??ncia absoluta', respectivamente."""
        self.texto13 = "Homing:"
        self.texto14 = """Para levar o calado ao ponto de refer??ncia definido pelo sensor usam-se os"""
        self.texto15 = """bot??es 'Home +' e 'Home -', em que os sinais s??o referentes ?? dire????o do movimento."""            
        self.textos = [self.texto1, self.texto2, self.texto3, self.texto4, self.texto5, self.texto6, self.texto7,
                       self.texto8, self.texto9, self.texto10, self.texto11, self.texto12, self.texto13, self.texto14, self.texto15]
    
        self.button_fechar = QPushButton('Fechar')
        self.button_fechar.setMaximumWidth(50)
        self.button_fechar.move(550, 385)

    def paintEvent(self, event):
            qp = QPainter()
            qp.begin(self)
            self.drawText(event,qp)
            qp.end()
            
    def drawText(self, event, qp):
        for index, texto in enumerate(self.textos):
            if index in [0, 4, 8, 12]:
                pen = QPen(Qt.black, 2, Qt.SolidLine)
                qp.setPen(pen)
                qp.drawLine(20, index*25 + 22, 650, index*25 + 22)
                qp.setPen(QColor(177, 34, 3))
                qp.setFont(QFont('Decorative', 14))
            else:
                qp.setPen(QColor(0, 0, 0))
                qp.setFont(QFont('Decorative', 12))
            qp.drawText(20, index*25 + 20, texto)

class Help(QWidget):
    """Classe implementada a partir da classe QMainWindow e gera a tela de ajuda"""
    
    def __init__(self, parent=None):
        """Funcao __init__ para definir o layout geral
        """
        
        super().__init__(parent)
        self.setWindowTitle("Descri????o das fun????es")
        self.setGeometry(50, 50, 660, 420)
        
        self.texto1 = "Movimento relativo:"
        self.texto2 = """Para a movimenta????o da mesa em rela????o ?? posi????o atual, devem ser utilizados os"""
        self.texto3 = """bot??es 'Hor??rio' e 'Anti-hor??rio',os quais tomam os valores do slider do grupo"""
        self.texto4 = """'Step' como o ??ngulo a ser adicionado ou subtra??do da posi????o de partida."""
        
        self.texto5 = "Movimento absoluto:"
        self.texto6 = """Para a movimenta????o da mesa em rela????o ?? refer??ncia absoluta da mesa,"""
        self.texto7 = """o bot??o'Mover' deve ser utilizado, tal bot??o utiliza o valor do slider""" 
        self.texto8 = """ no grupo 'Movimento' como o ??ngulo referente ?? posi????o final do movimento."""
        self.texto9 = "Posi????o:"
        self.texto10 = """Para obter a posi????o atual da mesa utiliza-se os bot??es 'Posi????o' e""" 
        self.texto11 = """'Posi????o Absoluta', que se referem ??s posi????es relativas ao que ?? estabelecido"""
        self.texto12 = """pelos bot??es 'Ponto atual como refer??ncia' e 'Refer??ncia absoluta', respectivamente."""
        self.texto13 = "Homing:"
        self.texto14 = """Para levar a mesa ao ponto de refer??ncia definido pelo sensor usam-se os"""
        self.texto15 = """bot??es 'Home +' e 'Home -', em que os sinais s??o referentes ?? dire????o do movimento."""            
        self.textos = [self.texto1, self.texto2, self.texto3, self.texto4, self.texto5, self.texto6, self.texto7,
                       self.texto8, self.texto9, self.texto10, self.texto11, self.texto12, self.texto13, self.texto14, self.texto15]
        
        self.button_fechar = QPushButton('Fechar', self)
        self.button_fechar.setMaximumWidth(50)
        self.button_fechar.move(550, 385)
   
    def paintEvent(self, event):
            qp = QPainter()
            qp.begin(self)
            self.drawText(event,qp)
            qp.end()
            
    def drawText(self, event, qp):
        for index, texto in enumerate(self.textos):
            if index in [0, 4, 8, 12]:
                pen = QPen(Qt.black, 2, Qt.SolidLine)
                qp.setPen(pen)
                qp.drawLine(20, index*25 + 22, 650, index*25 + 22)
                qp.setPen(QColor(177, 34, 3))
                qp.setFont(QFont('Decorative', 14))
            else:
                qp.setPen(QColor(0, 0, 0))
                qp.setFont(QFont('Decorative', 12))
            qp.drawText(20, index*25 + 20, texto)
        
        self.button_fechar.clicked.connect(self.fechar)
        
        self.setWindowIcon(QIcon('ipt-wmesa.ico'))
        
        self.show()
        
    def fechar(self):
        """Fecha a janela de ajuda"""
        self.close()


class MainWindow(QMainWindow):
    """Classe implementada sobre a partir da classe QMainWindow e gera a tela de comandos,
    responsavel pela disposicao final das guias"""
    
    def __init__(self, mesa, msg=None, process=None, parent=None):
        """Funcao __init__ para definir o layout geral
        
        Keyword argumets:
        robo -- arquivo do qual chamam-se os comandos enviados ao robo
        """
        super(MainWindow, self).__init__(parent)
        
        self.calado = mesa
        titulo = "Movimentador do Tunel"
        if msg is not None:
            titulo += " - " + msg
        
        self.setWindowTitle(titulo)
        self.setGeometry(50, 50, 500, 550)
        
        self.table_widget = MyTableWidget(self.calado, process, self)
        self.setCentralWidget(self.table_widget)

        exitAct = QAction(QIcon('exit.png'), '&Sair', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Sair do Programa')
        exitAct.triggered.connect(self.table_widget.sair)
        
        #configAct = QAction(QIcon('configura.jpg'), '&Configurar', self)
        #configAct.setStatusTip('Configurar endere??o')
        #configAct.triggered.connect(self.new_wind)
        
        helpAct = QAction(QIcon('help.jpg'), '&Ajuda', self)
        helpAct.setShortcut('Ctrl+H')
        helpAct.setStatusTip('Ajuda')
        helpAct.triggered.connect(self.ajuda)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.table_widget.sair)

        menubar = self.menuBar()
        configMenu = menubar.addMenu('&Configura????es')
        #configMenu.addAction(configAct)
        configMenu.addAction(helpAct)
        configMenu.addAction(exitAct)

        self.setWindowIcon(QIcon('ipt-wmesa.ico'))

        self.show()
        
    def new_wind(self):
        """Fecha a janela de boas vindas e inicia a janela principal"""
        self.close()
        self.calado.disconnect()
        self.win = Welcome()
        self.win.show()
        
    def ajuda(self):
        """Abre a janela de ajuda"""
        self.win2 = Help()
        self.win2.show()

class MyTableWidget(QWidget):        
    """Classe implementada a partir da classe QWidget, gera a tela inicial dispondo
    os grupos criados em um *grid layout*"""
    
    def __init__(self, calado, process=None, parent=None):
        """Define os grupos dentro do *grid layout*"""
        
        self.calado = calado
        self.process = process
        super(MyTableWidget, self).__init__(parent)
        
        #Layout Geral
        grid = QGridLayout()
        
        self.relativo = RelativeMove()
        self.step = StepMove()
        self.reference = Reference()
        self.home = Home()
        self.move = Move()
        self.position = Position()
        self.stop = Stop()
        self.clear = Clear()
        
        grid.addWidget(self.relativo, 0, 0)
        grid.addWidget(self.step, 1, 0)
        grid.addWidget(self.reference, 2, 0)
        grid.addWidget(self.home, 0, 1)
        grid.addWidget(self.move, 1, 1)
        grid.addWidget(self.position, 2, 1)
        grid.addWidget(self.stop, 0, 2, 2, 1)
        grid.addWidget(self.clear, 2, 2)
        self.setLayout(grid)
        
        self.relativo.buttondo.clicked.connect(self.rmoveClicked)
        self.relativo.buttonup.clicked.connect(self.rmoveClicked)
        self.step.btn_encoder.clicked.connect(self.stepEncoderClicked)
        self.step.btn_motor.clicked.connect(self.stepMotorClicked)
        self.reference.buttonref.clicked.connect(self.refClicked)
        self.reference.buttonabsref.clicked.connect(self.absrefClicked)
        self.home.buttonxp.clicked.connect(self.homexClicked)
        self.home.buttonxm.clicked.connect(self.homexClicked)
        self.move.button.clicked.connect(self.moveClicked)
        self.position.buttonpos.clicked.connect(self.posClicked)
        self.position.buttonabspos.clicked.connect(self.absposClicked)
        self.stop.buttons.clicked.connect(self.stopClicked)
        self.clear.button.clicked.connect(self.clearClicked)
        
    def sair(self):
        """Finaliza o processo de comunica????o e encerra o aplicativo"""
        self.calado.disconnect()
        if self.process is not None:
            self.process.terminate()
        qApp.quit()

            
        
    def rmoveClicked(self):
        """Utiliza o metodo sender dos botoes para a movimentacao relativa de cada uma das coordenadas,
        levando os valores do respectivo passo em considera????o.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        clickedButton = self.sender()
        digitFunction = clickedButton.text()
        
        if digitFunction[0] == 'S':
            x = float(self.step.sliderx.value())
            self.calado.rmove(x)
        
        elif digitFunction[0] == "D":
            x = -float(self.step.sliderx.value())
            self.calado.rmove(x)
        self.posClicked(True)
        self.absposClicked(True)
        
    def moveClicked(self):
        """Envia o robo a posi????o indicada pelos *sliders* da classe Move.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        x = float(self.move.slidermx.value())
        
        
        self.calado.move(x)
        self.posClicked(True)
        self.absposClicked(True)
        
    def homexClicked(self):
        """Envia o robo a posi????o de referencia em X.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        
        clickedButton = self.sender()
        sign = clickedButton.text()[-1]
        self.calado.home('x',sign)
        self.posClicked(True)
        self.absposClicked(True)
        
    def posClicked(self, changed = False):
        """Obtem a posicao do robo e a imprime.
        
        Chamando o comando por meio do arquivo passado por *self.calado*
        
        Keyword arguments:
        changed -- indica alteracao na posicao, para valor verdadeiro apaga a posicao da interface"""
        
        if changed:
            self.text1 = ''
            self.changed = False
        else:
            p = self.calado.position()
            self.text1 = "Posi????o = {}".format(format(p, '.3f'))
        self.position.labelp.setText(self.text1)
        
    def absposClicked(self, changed = False):
        """Obtem a posicao absoluta do robo e a imprime.
        
        Chamando o comando por meio do arquivo passado por *self.calado*
        
        Keyword arguments:
        changed -- indica alteracao na posicao, para valor verdadeiro apaga a posicao da interface"""
        
        if changed:
            self.text2 = ''
            self.changed = False
        else:
            p = self.calado.abs_position()
            self.text2 = "Posi????o = {}".format(format(p, '.3f'))
        self.position.labelabsp.setText(self.text2)
        
    def refClicked(self):
        """Define a posicao atual como referencia para o robo.
        
        Chamando o comando por meio do arquivo passado por *self.calado*"""
        xref = float(self.reference.valref.text())
        self.posClicked(True)
        self.absposClicked(True)
        self.calado.set_reference(xref)
        self.reference.valref.setText("0")
        
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
        self.step.btn_motor.setStyleSheet("background-color:darkCyan;  border-style: outset; border-width: 2px; border-radius: 10px; border-color: blue;")
        self.step.btn_encoder.setStyleSheet("")
        
    def stepEncoderClicked(self):
        """Muda o metodo de passos enviados do controlador para o valor de passos 
        calibrados pelo encoder."""
        
        self.calado.step_encoder()
        self.step.btn_encoder.setStyleSheet("background-color:darkCyan;  border-style: outset; border-width: 2px; border-radius: 10px; border-color: blue;")
        self.step.btn_motor.setStyleSheet("")
        
#import mesa

