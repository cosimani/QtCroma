import os, sys

import cv2 

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import json
import numpy as np
import tkinter as tk

from matplotlib import pyplot as plt

import ventana

np.set_printoptions( suppress = True )  # Para que la notacion no sea la cientifica

class Visor( QLabel ) :

    def __init__( self ) :
        super( Visor, self ).__init__()

        self.ventana = 0

        # A continuación los valores para hacer el Chroma Keying
        self.up_canal1 = 0
        self.up_canal2 = 0
        self.up_canal3 = 0
        self.down_canal1 = 0
        self.down_canal2 = 0
        self.down_canal3 = 0

        # Aquí leemos el archivo config.json para traer las variables de configuración
        # Podemos acceder así: config[ 'max_num_hands' ]
        # Al usar dentro del with el archivo se cierra autmáticamente al salir del with
        with open( 'config.json' ) as json_file: 
            self.config = json.load( json_file ) 

        self.videoCapture = cv2.VideoCapture( self.config[ 'camara_o_mp4' ] )

        self.timer = QTimer()

        # Connecting the signal
        QObject.connect( self.timer, SIGNAL( "timeout()" ), self.slot_procesar )
        self.timer.start( self.config[ 'tiempo_para_timer_procesar' ] )

        
        root = tk.Tk()
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        print( 'Resolución de la pantalla: %d x %d' % ( self.screen_w, self.screen_h ) )


    def recibirVentana( self, ventana ) :
        self.ventana = ventana

    def setValues_chroma( self, up_canal1, up_canal2, up_canal3, down_canal1, down_canal2, down_canal3 ) :
        self.up_canal1 = up_canal1
        self.up_canal2 = up_canal2
        self.up_canal3 = up_canal3
        self.down_canal1 = down_canal1
        self.down_canal2 = down_canal2
        self.down_canal3 = down_canal3
        print( 'down[', self.down_canal1, self.down_canal2, self.down_canal3, 
               '] - up[', self.up_canal1, self.up_canal2, self.up_canal3, ']' )
        
    @Slot()
    def slot_procesar( self ) :

        if self.videoCapture.isOpened() :

            success, frame = self.videoCapture.read()

            if success != True :
                return

            h, w, ch = frame.shape
            bytesPerLine = ch * w
            
            frame = cv2.cvtColor( cv2.flip( frame, 1 ), cv2.COLOR_BGR2RGB )

            if self.config[ 'deshabilitar_chroma_keying' ] == False :

                u_green = np.array( [ self.up_canal1, self.up_canal2, self.up_canal3 ] ) 
                l_green = np.array( [ self.down_canal1, self.down_canal2, self.down_canal3 ] ) 

                frame = cv2.cvtColor( frame, cv2.COLOR_BGR2LAB )

                mask = cv2.inRange( frame, l_green, u_green ) 
                # frame = cv2.bitwise_and( frame, frame, mask = mask ) 

                kernel = np.ones( ( 3, 3 ) )
                # mask = cv2.dilate(mask, kernel, iterations=1)
                mask = cv2.erode( mask, kernel, iterations = 1 )
               
                kernel = np.ones( ( 8, 8 ), np.float32 ) / 35
                mask = cv2.filter2D( mask, -1, kernel )

                # cv2.imshow('window_name', mask)

                frame = cv2.cvtColor( frame, cv2.COLOR_LAB2BGR )
            
            convertToQtFormat = QImage( frame.data, w, h, bytesPerLine, QImage.Format_RGB888 )
            im = convertToQtFormat.scaled( self.width(), self.height() )

            im = im.convertToFormat( QImage.Format_ARGB32 )

            if self.config[ 'deshabilitar_chroma_keying' ] == False :

                alpha_mask = QImage( mask.data, w, h, w, QImage.Format_Alpha8 )
                im.setAlphaChannel( alpha_mask );

            alpha = QImage( im.width(), im.height(), QImage.Format_Alpha8 )
            alpha.fill( self.config[ 'alpha_camara' ] )
            im.setAlphaChannel( alpha );

            pixmap = QPixmap.fromImage( im )
            self.setPixmap( pixmap );

    def detener( self ) : 

        self.timer.stop()
        self.videoCapture.release()

        if self.videoCapture.isOpened() == False :
            print( 'Cámara apagada' )

