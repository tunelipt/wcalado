# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:35:10 2017

@author: felipenanini
"""

#import mesateste as mesa

from xmlrpc.server import SimpleXMLRPCServer

def start_server(test=False, ip='localhost', port=9596, porta='COM1', baud=9600, size=8, parity='N', stop=1):
    """Inicializa o servidor relacionando-o a uma instancia importada de um arquivo externo
    
    Keyword arguments:
    ip -- endereco do servidor
    port -- porta do servidor"""
    if test:
        import mesateste as mesa
    else:
        import mesa
    
    m = mesa.Robo(port = porta, baudrate = baud, bytesize = size, parity = parity, stopbits = stop)
    print("Connecting to Serial...")
    m.connect()
    print("Starting XML-RPC server...")
    srvr = MesaServer(ip, port, m)
    srvr.start()

class MesaServer:
    """Cria a instancia do servidor responsavel pela comunicacao XML-RPC com o robo"""
    def __init__(self, ip, port, mesa):
        self.mesa=mesa
        self.ip=ip
        self.port=int(port)
    def start(self):
        print("Starting XML-RPC Server...")
        #self.server = SimpleXMLRPCServer(("192.168.129.7", 8000), allow_none=True)
        self.server = SimpleXMLRPCServer((self.ip, self.port), allow_none=True)
        self.server.register_instance(self.mesa)
        print("Serving XML-RPC...")
        self.server.serve_forever()


if __name__ == "__main__":
    print("Creating interface ...")
    start_server()
