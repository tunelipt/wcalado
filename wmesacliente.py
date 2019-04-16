# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:51:03 2017

@author: felipenanini
"""

import sys

from PyQt5.QtWidgets import (QSplashScreen, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import argparse
import time
import wmesa


if __name__ == '__main__':  
    
    parser = argparse.ArgumentParser(description="wmesa")
    parser.add_argument("-i", "--ip", help="Endereço IP do servidor XML-RPC", default="localhost")
    parser.add_argument("-p", "--port", help="Porta XML-RPC do servidor XML-RPC", default=9596, type=int)

    app = QApplication([]) # sys.argv
    
    args = parser.parse_args()
    
    # Create and display the splash screen
    splash_pix = QPixmap('ipt.jpg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    
    win = wmesa.WMesaServer(False, args.ip, args.port, "COM1", False, True)
    win.show()
    splash.finish(win)

    sys.exit(app.exec_())
