import os, sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import numpy as np

import tkinter as tk

import json
import glob
from matplotlib import pyplot as plt
from datetime import datetime
from time import time

import visor  

np.set_printoptions( suppress = True )  # Para que la notacion no sea la cientifica

class Ventana( QWidget ) :
    def __init__( self ) :
        super( Ventana, self ).__init__()

        self.visor = visor.Visor()
        self.visor.recibirVentana( self )

        # Con estos dos ya estaría
        # self.setWindowFlags( Qt.WindowStaysOnTopHint )  # Para que se mantenga en top
        # self.setWindowFlags( Qt.FramelessWindowHint )

        # Para que se mantenga en top y para ventana sin bordes.
        self.setWindowFlags( Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )  

        self.setAttribute( Qt.WA_TranslucentBackground, True )  # Hace transparente el color gris de los widgets
        self.visor.setAttribute( Qt.WA_TransparentForMouseEvents, True )  # El Clic atraviesa esta ventana
        self.setAttribute( Qt.WA_TransparentForMouseEvents, True )  # El Clic atraviesa esta ventana
        

        # self.setWindowFlags( Qt.FramelessWindowHint | Qt.Popup )
        # self.setWindowFlags( Qt.Popup )

        self.visor.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        grid = QGridLayout()
        grid.setContentsMargins( 0, 0, 0, 0 )
        grid.addWidget( self.visor, 0, 0, 9, 10 )
        self.setLayout( grid )
 
        self.setWindowTitle( 'Chroma Keying' )

        # A continuación los valores para hacer el Chroma Keying
        self.up_canal1 = 104
        self.up_canal2 = 153
        self.up_canal3 = 70
        self.down_canal1 = 30
        self.down_canal2 = 30
        self.down_canal3 = 0

        self.down_canal1 = 0
        self.down_canal2 = 90
        self.down_canal3 = 0
        self.up_canal1 = 255
        self.up_canal2 = 180
        self.up_canal3 = 255


        self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                     self.down_canal1, self.down_canal2, self.down_canal3 )


    def slot_capturar( self ) :
        self.visor.capturarParaCSV( cuantos = 50 )

    @Slot( int )
    def slot_gestoDetectado( self, label_gesto_detectado ) :
        print( 'slot_gestoDetectado()', label_gesto_detectado )

    def keyPressEvent( self, e ) :

        if e.key() == Qt.Key_Escape :
            self.close()

        elif e.key() == Qt.Key_N :
            event = QMouseEvent( QEvent.MouseButtonPress, QCursor.pos(), 
                                 Qt.LeftButton, Qt.LeftButton, Qt.NoModifier )
            QCoreApplication.sendEvent( self, event )

        elif e.key() == Qt.Key_C :
            self.slot_capturar()

        elif e.key() == Qt.Key_Q :
            self.down_canal1 += 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_A :
            self.down_canal1 -= 1   
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_W :
            self.down_canal2 += 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_S :
            self.down_canal2 -= 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_E :
            self.down_canal3 += 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_D :
            self.down_canal3 -= 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )

        elif e.key() == Qt.Key_R :
            self.up_canal1 += 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_F :
            self.up_canal1 -= 1            
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_T :
            self.up_canal2 += 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_G :
            self.up_canal2 -= 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_Y :
            self.up_canal3 += 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )
        elif e.key() == Qt.Key_H :
            self.up_canal3 -= 1
            self.visor.setValues_chroma( self.up_canal1, self.up_canal2, self.up_canal3, 
                                         self.down_canal1, self.down_canal2, self.down_canal3 )

            

    def closeEvent( self, e ) :
        self.visor.detener()        
        qApp.quit()        

if __name__ == '__main__':
    app = QApplication( sys.argv )

    # Aquí detectamos el archivo .py que estamos ejecutando, leemos su directorio y la seteamos como
    # carpeta de trabajo. Esto es para que independientemente desde dónde se ejecute este .py, que la
    # carpeta de trabajo sea la misma donde se encuentra el .py ejecutado.
    os.chdir( os.path.dirname( os.path.abspath( __file__ ) ) )

    root = tk.Tk()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()  

    with open( 'config.json' ) as json_file: 
        config = json.load( json_file ) 

    ventana = Ventana()

    ancho_imagen_camara = config[ 'ancho_imagen_camara' ]
    alto_imagen_camara = config[ 'alto_imagen_camara' ]
    ventana.resize( ancho_imagen_camara, alto_imagen_camara )

    if config[ 'posicion_ventana' ] == 'centro' :
        ventana.move( screen_w / 2 - ancho_imagen_camara / 2, screen_h / 2 - alto_imagen_camara / 2 )
    elif config[ 'posicion_ventana' ] == 'abajo_der' :        
        ventana.move( screen_w - ancho_imagen_camara, screen_h - alto_imagen_camara )
    elif config[ 'posicion_ventana' ] == 'arriba_izq' :        
        ventana.move( 0, 0 )

    if config[ 'posicion_ventana' ] == 'max' :        
        ventana.showMaximized()
    else :
        ventana.show()

    sys.exit( app.exec_() )