# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:33:21 2017

@author: felipenanini
"""

import serial
import mesaxmlrpc
import time

class XException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class Robo:
    def __init__(self, port = "\\\\.\\COM1", baudrate = 9600, bytesize = serial.EIGHTBITS, 
                 parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, passoMotor=28100000, passoEncoder=2492):
        """Incializa a conexao com a porta serial
        
        Keyword arguments:
        passoMotor   Define o valor de passos do motor para uma volta completa
        passoEncoder Define o valor de passos do encoder para uma volta completa
        port         A porta serial conectada
        baudrate     Taxa em que os sinais da comunicacao variam
        bytesize     Numero de bits por caracter (5, 6, 7, 8)
        parity       Bit de verificacao de paridade (Nenhum-N, Par-E, Impar-O, Espaco-S, Marca-M)
        stopbits     Bit ou bits de parada no final do caracter (1 ou 2)"""
        self.ser = serial.Serial(port = port, baudrate = baudrate, bytesize = bytesize, parity = parity, stopbits = stopbits, timeout = 0.01)
        time.sleep(1)
        self._passoMotor = passoMotor/360
        self._passoEncoder = passoEncoder/360
        self.x0 = 0.0
        self.stopPress = False
        self.step = False
        self.connect()
        
        
    def connect(self):
        """Estabelece a conexao a partir do terminal e inicializa o canal pelo prompt do programa"""
        self.isconnected = True
        self.sendData("E")
        reply = self.get_reply()
        seq = ["LD3", "MN", "OSC1", "FSB1", "A5", "V5", "ER1"]
        for i in seq:
            self.sendData(i)
        self.step_encoder()        
        return reply
               
    def get_reply(self, wait=0.01):
        """Executa a leitura do terminal"""
        if not self.isconnected:
            raise XException("Python interface not connected")
        reply = ''
        while True:
            time.sleep(wait)
            tmp = self.ser.readline()
            tmp = str(tmp)

            if tmp == '' or tmp == 'b\'\'':
                break
            tmp = tmp.strip('b')
            tmp = tmp.strip('\'')
            tmp = tmp.strip(' ')
            tmp = tmp.replace("r", "")
            tmp = tmp.replace("\\", "")
            tmp = tmp.strip('n')
            reply += tmp
        return reply
    
    def move(self, x, y = None, z = None, a = False, r = False, sync = False):
        """Inicializa a movimentacao do robo verificando todos os eixos
        
        O parametro s define o comando incremental na linguagem X"""
        x = int(x)
        y = x//360
        if y:
            x = x%360 
        
        if x//180:
            x = x - 360
        step = self.step
        if not self.isconnected:
            raise XException("Python interface not connected")
        if a:
            x0 = 0
        else:
            x0 = self.x0
            x0 = float(x0)
        if step:
            if r:
                step = self.abs_position(pulses = True)
                pos = round(self.abs_position()['x'])
                msg = ["FSA0 \n", "D" + str(round(self._passoEncoder*(x + pos) - step)) + "\n", "G \n"]
            else:
                msg = ["FSA1 \n", "D" + str(round(x*self._passoEncoder + x0)) + "\n", "G \n"]
        else:
            if r:
                msg = ["MPI \n", "D" + str(round(x*self._passoMotor)) + "\n", "G \n"]
            else:
                msg = ["MPA \n", "D" + str(round(x*self._passoMotor + x0)) + "\n", "G \n"]
        for i in msg:
            self.sendData(i)
        rep = self.get_reply()
        if sync:
            self.waitUntilDone()
        return rep
    
    def rmove(self, x, y = None, z = None, sync = False):
        """Inicializa a movimentacao incremental do robo no eixo indicado"""
        p = self.position()['x']
        if p//180:
            p = p-360
        if x+p>180 or x+p<-180:
            if x > 0:
                x = x - 360
            else:
                x = x + 360                  
        self.move(x, r = True, sync = sync)
    
    def abs_position(self, pulses=False):
        """Indica a posicao atual absoluta do robo de acordo com os parametros de posicao definidos inicialmente"""
        if not self.isconnected:
            raise XException("Python interface not connected")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        char_found = True
        while char_found:
            try:
                self.sendData("1PR")
                r = self.get_reply()
                if len(r)>5:    
                    sign = r[4]
                    r = r[5:]
                    if r.isnumeric():
                        if sign == '-':
                            pts = -1*int(r)
                        else:
                            pts = int(r)
                    else:
                        continue
                    char_found = False
            except:
                while self.get_reply() != 'b\'\'' or self.get_reply != " ":
                    time.sleep(0.01)
                char_found = True
            
        if pulses:
            return pts
        else:
            if self.step:
                x=pts/self._passoEncoder
            else:    
                x=pts/self._passoMotor
            return dict(x=x)
            
    def position(self):
        """Indica a posicao atual do robo de acordo com os parametros de posicao definidos inicialmente"""
        p = self.abs_position()
        x=p['x']-self.x0
        return dict(x=x)
    
    def set_reference(self):
        """Define a posicao de referencia"""
        
        p = self.abs_position()
        self.x0 = p['x']
        
    def home(self, eixo, sinal):
        """Envia o comando para o controlador procurar o sensor de homing na direcao que deve seguir para se 
        percorrer o menor caminho"""
        if sinal == '+':
            self.sendData("GH1")
        else:
            self.sendData("GH-1")

    def set_abs_reference(self):
        """Define a posicao de referencia absoluta"""
        
        self.x0 = 0.0
        #self.sendData("PZ")
    
    def stop(self):
        """Para toda a movimentacao imediatamente"""
        self.stopPress = True
        self.sendData("S")
        time.sleep(0.5)
    
    def clear(self):
        self.sendData("Z")
        time.sleep(0.1)
        self.connect()
        
    def step_motor(self):
        self.sendData("FSB0")
        self.step = False
        
    def step_encoder(self):
        self.sendData("FSB1")
        self.step = True
    
    def waitUntilDone(self, wait=0.01):
        """Aguarda a execucao do comando ate a posicao """
        if not self.isconnected:
            raise XException("Python interface not connected")
        p1 = self.abs_position(pulses=True)
        while True:
            p2 = self.abs_position(pulses=True)
            if self.stopPress:
                self.sendData("S")
                self.stopPress = False
                break
            if p2 == p1:
                break
            p1 = p2
        return p2
    
    def sendData(self, data):
        """Envia os comandos para o controlador"""
        data += "\r\n"
        self.ser.write(data.encode())        
    
    def disconnect(self):
        """Desconecta o programa do terminal"""
        if self.isconnected:
            self.ser.close()

        return None

if __name__ == "__main__":
    print("Creating server ...")
    
    mesaxmlrpc.start_server(ip = 'localhost', port = '8080', porta = 'COM1', baud = 9600, parity = 'N', stop = serial.STOPBITS_ONE)
