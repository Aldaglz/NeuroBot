#cód1go principal 
#Nyaaaa

import sys
from Diseño import * 

from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore , QtGui , QtWidgets
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, QThread, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cv2
import mediapipe as mp
import numpy as np
import os
import math
import time
import threading


import serial


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

degrees=math.degrees
acos=math.acos




mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)



class MiApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		#eliminar barra y de titulo - opacidad
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setWindowOpacity(1)

		#SizeGrip
		self.gripSize = 10
		self.grip = QtWidgets.QSizeGrip(self)
		self.grip.resize(self.gripSize, self.gripSize)

		#Mover ventana
		self.ui.frameSuperior.mouseMoveEvent = self.mover_ventana

		#Acceder a las paginas
		self.ui.btn_Inicio.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_Inicio))
		self.ui.btn_Pacientes.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_Pacientes))
		self.ui.btn_Terapias.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_Interfaz_de_Terapia))

		#control barra de titulos
		self.ui.btn_Maximizar.clicked.connect(self.control_btn_Maximizar)
		self.ui.btn_Minimizar.clicked.connect(self.control_btn_Minimizar)
		self.ui.btn_Restaurar.clicked.connect(self.control_btn_Restaurar)
		self.ui.btn_Cerrar.clicked.connect(lambda: self.close())

		self.ui.btn_Restaurar.hide()

		#menu lateral
		self.ui.btn_Menu.clicked.connect(self.mover_menu)

		#Video
		self.ui.btn_Encender.clicked.connect(self.start_video)
		self.ui.btn_Apagar.clicked.connect(self.cancel)
				

	def start_video(self):
		bd=0

		if self.ui.rb_Skeleto.isChecked()==True:
			self.Streaming = Skeleton()
			bd=3
		elif self.ui.rb_both.isChecked()==True:
			self.Streaming = Streaming()
			bd=2

	

		if bd==1:
			self.ui.lb_StateVideo.setText("Encendiendo...")
			
			#Se conectan con las imagenes generadas
			self.Streaming.ImageEmotion.connect(self.Imageupd_slot_Emotions)
			self.Streaming.ImageSkeleton.connect(self.Imageupd_slot_Skeleton)
			self.Streaming.PNG_Emoji.connect(self. Imageupd_slot_emoji)
			
			#Se conectan con los angulos tomados
			self.Streaming.Shoulder_Right.connect(self.Angulo_Shoulder_Derecho)
			self.Streaming.Shoulder_Left.connect(self.Angulo_Shoulder_izquierdo)
			self.Streaming.Elbow_Right.connect(self.Angulo_Elbow_Derecho)
			self.Streaming.Elbow_Left.connect(self.Angulo_Elbow_izquierdo)
			self.Streaming.Wrist_Right.connect(self.Angulo_Wrist_Derecho)
			self.Streaming.Wrist_Left.connect(self.Angulo_Wrist_izquierdo)
			self.Streaming.Cuello.connect(self.Angulo_Cuello)			
			self.Streaming.Cabeza.connect(self.Angulo_Cabeza)
			
			#Pantalla LCD
			self.Streaming.Expresion.connect(self.Expresion)
			self.Streaming.start()

		elif bd==2:
			self.ui.lb_StateVideo.setText("Encendiendo...")
			self.Streaming.Imageupd.connect(self.Imageupd_slot_video)
			self.Streaming.start()

		elif bd==3:
			self.ui.lb_StateVideo.setText("Encendiendo...")
			self.Streaming.Imageupd.connect(self.Imageupd_slot_videoSkele)
			self.Streaming.start()
	


		else:
			mg_box = QMessageBox()
			mg_box.setWindowTitle("ERROR")
			mg_box.setText('Seleccione una opcion de abajo')
			mg_box.setIcon(QMessageBox.Information)
			mg_box.exec_()



	#Funciones que colocan las imagenes generadas en el hilo


	def Imageupd_slot_Skeleton(self, ImageSkeleton):
		self.ui.lb_VideoSkeleto.setPixmap(QPixmap.fromImage(ImageSkeleton))
		self.ui.lb_StateVideo.setText("Captura del cuerpo activado") 

	def Imageupd_slot_emoji(self, PNG_Emoji):
		self.ui.label_4.setPixmap(PNG_Emoji)



	def Imageupd_slot_video(self,Imageupd):
		self.ui.lb_Video.setPixmap(QPixmap.fromImage(Imageupd))
	
	def Imageupd_slot_videoSkele(self,Imageupd):
		self.ui.lb_VideoSkeleto.setPixmap(QPixmap.fromImage(Imageupd))


	

	
	def cancel(self, Image):
		self.ui.lb_VideoSkeleto.clear()
		self.ui.lb_Video.clear()
		self.ui.label_4.clear()
		self.Streaming.stop()
		self.ui.lb_StateVideo.setText("Apagado")


	def control_btn_Minimizar(self):
		self.showMinimized()

	def control_btn_Restaurar(self):
		self.showNormal()
		self.ui.btn_Restaurar.hide()
		self.ui.btn_Maximizar.show()
		
	def control_btn_Maximizar(self):
		self.showMaximized()		
		self.ui.btn_Maximizar.hide()
		self.ui.btn_Restaurar.show()
		

	
	def mover_menu(self):
		if True:
			width = self.ui.frameLateral.width()
			normal = 0
			if width==0:
				extender = 200
			else: 
				extender= normal
			self.animacion=QPropertyAnimation(self.ui.frameLateral, b'minimumWidth')
			self.animacion.setDuration(300)
			self.animacion.setStartValue(width)
			self.animacion.setEndValue(extender)
			self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
			self.animacion.start()

			
 	##SizeGrip
	def resizeEvent(self, event):
		rect = self.rect()
		self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)


	##Mover ventana
	def mousePressEvent(self, event):
		self.clickPosition=event.globalPos()

	def mover_ventana(self, event):
		if self.isMaximized()==False:
			if event.buttons() == Qt.LeftButton:
				self.move(self.pos()+event.globalPos()-self.clickPosition)
				self.clickPosition =event.globalPos()
				event.accept()

		if event.globalPos().y() <=20:
			self.showMaximized()
		else:
			self.showNormal()
			

class Skeleton(QThread):
    Imageupd = pyqtSignal(QImage)
    def run(self):
        self.hilo_corriendo = True
        cap = cv2.VideoCapture(1)
        with mp_pose.Pose(static_image_mode=False) as pose:
            while self.hilo_corriendo:
                ret, frame = cap.read() 
                if ret:
                    Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    flip = cv2.flip(Image, 1)

                    results=pose.process(flip)
                    if results.pose_landmarks is not None:
                        mp_drawing.draw_landmarks(flip,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,mp_drawing.DrawingSpec(color=(128,0,250),thickness=5,circle_radius=3),mp_drawing.DrawingSpec(color=(255,255,0),thickness=10))   
                        convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                        if self.hilo_corriendo:
                            pic = convertir_QT.scaled(600, 621, Qt.KeepAspectRatio)

                            self.Imageupd.emit(pic)
    def stop(self):
        self.hilo_corriendo = False
        self.quit()



class Streaming(QThread):
	Imageupd = pyqtSignal(QImage)
	def run(self):
		self.hilo_corriendo  = True
		cap = cv2.VideoCapture(1)
		while self.hilo_corriendo:
			ret, frame = cap.read() 
			if ret:
				Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				flip = cv2.flip(Image, 1)
				convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
				if self.hilo_corriendo:
					pic = convertir_QT.scaled(471, 321, Qt.KeepAspectRatio)
					self.Imageupd.emit(pic)
		
	def stop(self):
		self.hilo_corriendo = False
		self.quit()




if __name__ == "__main__":
	app = QApplication(sys.argv) 
	mi_app = MiApp()
	mi_app.show()
	sys.exit(app.exec_())



