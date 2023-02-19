#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
- ntc ve ptc verilerini doğrula
- log verilerine zaman ekle


"""

import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets,QtGui,QtCore
import pyqtgraph as pg
import numpy as np

class serialThreadClass(QtCore.QThread):  # Seri Porttan veri okuma iÅlemi iÃ§in QThread KullanÄ±ldÄ±.

    message = QtCore.pyqtSignal(str)
    def __init__(self,parent = None):

        super(serialThreadClass,self).__init__(parent)
        self.serialPort = serial.Serial()
        self.stopflag = False
    def stop(self):
        self.stopflag = True
    def run(self):
        while True:
            if (self.stopflag):
                self.stopflag = False
                break
            elif(self.serialPort.isOpen()): # eÄer seri Port baÄlÄ± deÄil iken veri okumayÄ± denersek hata verir.
                try:                        # bu hatayÄ± yakalayabilmek iÃ§in "try" bloÄu kullanÄ±ldÄ±.
                    self.data = self.serialPort.readline()
                except:
                    print("HATA\n")
                self.message.emit(str(self.data.decode()))
                print(str(self.data.decode()))
class Pencere(QtWidgets.QWidget):   
    
    def __init__(self):
        super().__init__()
        self.GulecGUI()
        self.show() 
        
    def GulecGUI(self): 

# com port        
        self.labelConstPort = QtWidgets.QLabel('<font color=blue>Please choose a serial port</font>')
        self.portCbox = QtWidgets.QComboBox()
        self.portlar = serial.tools.list_ports.comports()
        for i in self.portlar:
            self.portCbox.addItem(str(i))
            
        self.yenile = QtWidgets.QPushButton("")
        self.yenile.setStyleSheet("font: bold 14px; background-color : cyan; max-width: 1em; padding: 6px")        
        self.yenile.setIcon(QtGui.QIcon("update.png")) 
        
# baud rate
        self.labelConstBaud = QtWidgets.QLabel('<font color=blue>Please choose the baud rate of the device </font>')
        self.baudCbox = QtWidgets.QComboBox()
        baud = ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "74880", "115200", "230400", "250000",
                "500000", "1000000", "2000000"]
        for i in baud:
            self.baudCbox.addItem(i)
        self.baudCbox.setCurrentText(baud[4])
    
# baglan / baglanti kes        
        self.baglan = QtWidgets.QPushButton("Connect")
        self.baglan.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
# peltier ac / kapa
        self.peltier = QtWidgets.QPushButton("Peltier Disable")
        self.peltier.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")

        self.pump = QtWidgets.QPushButton("Pump Off")
        self.pump.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
        
        self.fan = QtWidgets.QPushButton("Fan Disable")
        self.fan.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
        
        self.cizdir = QtWidgets.QPushButton("Plot")
        self.cizdir.setStyleSheet("font: bold 14px; background-color : orange; max-width: 15em; padding: 6px")
        """
        self.cizdir2 = QtWidgets.QPushButton("Take A Snapshot")
        self.cizdir2.setStyleSheet("font: bold 14px; background-color : orange; max-width: 15em; padding: 6px")
        """
        self.onlineCizdir = False
        
        self.sicaklik = QtWidgets.QPushButton("Tank Temperature")
        self.sicaklik.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
        """
        self.sicaklik2 = QtWidgets.QPushButton("Fan Temperature")
        self.sicaklik2.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
        """
#
        self.pump.setEnabled(False)
        self.peltier.setEnabled(False)
        self.fan.setEnabled(False)
        self.sicaklik.setEnabled(False)
        self.cizdir.setEnabled(False)
        """
        self.sicaklik2.setEnabled(False)
        self.cizdir2.setEnabled(False)
        """
        
# 
        self.tempTank = QtWidgets.QLCDNumber()
        self.tempTank.setMinimumHeight(50)
        self.tempTank.setMinimumWidth(50)
        #self.tempTank.setStyleSheet("color:red ; background-color : yellow") 
        self.tempTank.setStyleSheet("color:red") 
        self.tempCooler = QtWidgets.QLCDNumber()
        self.tempCooler.setMinimumHeight(50)
        self.tempCooler.setMinimumWidth(50)
        self.tempCooler.setStyleSheet("color:blue") 
        self.labelTank = QtWidgets.QLabel('<font color=blue>Tank</font>')
        self.labelCooler = QtWidgets.QLabel('<font color=blue>Cooler</font>')
        self.labelC1 = QtWidgets.QLabel('Celcius')
        self.labelC2 = QtWidgets.QLabel('Celcius')
        

        self.graphicsView = pg.PlotWidget()
        pg.setConfigOption('background', 'w')      # sets background white
        pg.setConfigOption('foreground', 'k')      # sets axis color to black
        self.graphicsView.setTitle('TEMPERATURE-TIME GRAPH')
        self.graphicsView.setLabel('bottom', 'TIME')           	# x-label
        self.graphicsView.setLabel('left', 'TEMPERATURE [C]')             # y-label 

# bilgi alanı
        self.labelPort = QtWidgets.QLabel('<font color=black>Please select a serial port to connect device</font>')
        self.labelPump = QtWidgets.QLabel('<font color=black>Pump is closed </font>')
        self.labelPeltier = QtWidgets.QLabel('<font color=black> Peltier has not been enabled yet  </font>')
        self.labelFan = QtWidgets.QLabel('<font color=black> Fan has not been started yet </font>')
        self.labelSicaklik = QtWidgets.QLabel('<font color=black> Temperatures has not been enabled yet </font>')        
        self.labelCizdir = QtWidgets.QLabel('<font color=black> Graph has not been plotted yet</font>')
        """
        self.labelSicaklik2 = QtWidgets.QLabel('<font color=black> Cooler temperature measuring has not been enabled yet </font>')
        self.labelCizdir2 = QtWidgets.QLabel('<font color=black> graph not plotted </font>')
        """
        self.labelPort.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        self.labelPump.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        self.labelPeltier.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        self.labelFan.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        self.labelCizdir.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        """
        self.labelCizdir2.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        self.labelSicaklik2.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
        """
        self.labelSicaklik.setFont(QtGui.QFont("Arial",14,QtGui.QFont.Bold))
# message

        self.message = QtWidgets.QTextEdit()
        self.message.setReadOnly(True) # bu satÄ±rda text edit sadece okunabilir olarak ayarlandÄ±. Yani textedit'in iÃ§ine yazÄ± yazÄ±lamaz.
        self.messageTitle = QtWidgets.QLabel("Gelen Mesaj")
        
        
        self.dataTank = []
        self.dataFan = []
        """        
        self.dataTank = [i*i for i in range(150)]   
        self.dataFan = [i for i in range(150)]  
        """
        
        
        self.titleBaslik1 = QtWidgets.QLabel('<font color=blue>Peltier Cooler GUI</font>')
        self.titleBaslik1.setFont(QtGui.QFont("Arial",20,QtGui.QFont.Bold))
        self.titleYTU = QtWidgets.QLabel()
        self.titleBaslik2 = QtWidgets.QLabel("Sensors, Actuators and Interface Principles")
        self.titleBaslik2.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Normal))
        self.titleBaslik3 = QtWidgets.QLabel("Tufan GULEC")
        self.titleBaslik3.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Normal))
        self.titleBaslik4 = QtWidgets.QLabel("20567001")
        self.titleBaslik4.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Normal))
        
#ekran yerlesimi yap
        vBox00 = QtWidgets.QVBoxLayout()        
        vBox00.addWidget(self.titleBaslik1)
        vBox00.addStretch()

        vBox0 = QtWidgets.QVBoxLayout()  
        vBox0.addWidget(self.titleBaslik2)
        vBox0.addWidget(self.titleBaslik3)
        vBox0.addWidget(self.titleBaslik4)
        vBox0.addStretch()
        
        hBox0 = QtWidgets.QHBoxLayout() 
        hBox0.addLayout(vBox00)
        hBox0.addStretch()
        hBox0.addLayout(vBox0)
        
        hBoxConnect = QtWidgets.QHBoxLayout()
        hBoxConnect.addWidget(self.portCbox)
        hBoxConnect.addWidget(self.yenile)
        
        vBox1 = QtWidgets.QVBoxLayout()   
        vBox1.addWidget(self.labelConstPort)  
        vBox1.addLayout(hBoxConnect)   
        vBox1.addWidget(self.labelConstBaud)
        vBox1.addWidget(self.baudCbox)  
        vBox1.addStretch()
        vBox1.addWidget(self.baglan)
        vBox1.addStretch()
        vBox1.addWidget(self.pump)
        vBox1.addWidget(self.peltier)
        vBox1.addWidget(self.fan)
        vBox1.addWidget(self.sicaklik)        
        vBox1.addWidget(self.cizdir)
        """
        vBox1.addWidget(self.sicaklik2)
        vBox1.addWidget(self.cizdir2)
        """
        vBox1.addStretch()
        
        
        vBox2 = QtWidgets.QVBoxLayout()
        vBox2.addWidget(self.labelPort)
        vBox2.addWidget(self.labelPump)
        vBox2.addWidget(self.labelPeltier)      
        vBox2.addWidget(self.labelFan)
        vBox2.addWidget(self.labelSicaklik)
        vBox2.addWidget(self.labelCizdir)
        vBox2.addWidget(self.messageTitle)
        vBox2.addWidget(self.message)
        vBox2.addStretch()
        
        vBox4 = QtWidgets.QVBoxLayout()
        vBox4.addStretch()
        vBox4.addWidget(self.labelTank)
        vBox4.addWidget(self.tempTank)
        vBox4.addWidget(self.labelC1)
        vBox4.addStretch()
        vBox4.addWidget(self.labelCooler)
        vBox4.addWidget(self.tempCooler)
        vBox4.addWidget(self.labelC2)
        vBox4.addStretch()

        self.group1 = QtWidgets.QGroupBox("Control Panel")
        self.group1.setLayout(vBox1)
        
        self.group2 = QtWidgets.QGroupBox("Monitor")
        self.group2.setLayout(vBox2)
        
        self.group3 = QtWidgets.QGroupBox("Temperatures")
        self.group3.setLayout(vBox4)
        
        hBox = QtWidgets.QHBoxLayout()
        hBox.addWidget(self.group1)
        hBox.addWidget(self.group3)
        hBox.addWidget(self.group2)        
        
        vBox3 = QtWidgets.QVBoxLayout()
        vBox3.addWidget(self.graphicsView)
        
        self.group4 = QtWidgets.QGroupBox("Drawing")
        self.group4.setLayout(vBox3)
        
        vBox = QtWidgets.QVBoxLayout()
        vBox.addLayout(hBox0)
        vBox.addLayout(hBox)
        vBox.addWidget(self.group4)
        vBox.addStretch()

# ekranı calistir        
        self.setLayout(vBox)      
        self.setWindowTitle("TUFAN GULEC - Project : Peltier Cooler")
        self.setGeometry(10, 40, 1000, 1000) 
        self.setWindowIcon(QtGui.QIcon('yildiz.png'))
        self.mySerial = serialThreadClass()                    # pencere sinifinin icinde serialThreadClass nesnesi olusturuldu
        self.mySerial.message.connect(self.messageTextEdit)    # seri porttan mesaj geldiginde mesajTextEdit fonksitonuna dallan
        self.mySerial.start()                                  # thread islemi baslatildi.
        
        self.baglan.clicked.connect(self.serialConnect)
        self.pump.clicked.connect(lambda: self.funcs(self.pump))
        self.peltier.clicked.connect(lambda: self.funcs(self.peltier))     
        self.fan.clicked.connect(lambda: self.funcs(self.fan))  
        self.sicaklik.clicked.connect(lambda: self.funcs(self.sicaklik))       
        self.yenile.clicked.connect(lambda: self.funcs(self.yenile))
        self.cizdir.clicked.connect(lambda: self.funcs(self.cizdir))
        """
        self.sicaklik2.clicked.connect(lambda: self.funcs(self.sicaklik2))
        self.cizdir2.clicked.connect(lambda: self.funcs(self.cizdir2))
        """
        
    
#
    def serialConnect(self):
        if self.baglan.text() == "Connect":
            if (self.mySerial.serialPort.isOpen() == False):
                self.portText = self.portCbox.currentText()
                self.port = self.portText.split()
                self.baudrate = self.baudCbox.currentText()
                self.mySerial.serialPort.baudrate = int(self.baudrate) # seriport baudrate ayarÄ± tanÄ±mlandÄ±.
                self.mySerial.serialPort.port = self.port[0]
        
                try:
                    self.mySerial.serialPort.open()
                except:
                    self.message.append("Connection error!(on log)")
                if (self.mySerial.serialPort.isOpen()):
                    self.labelPort.setText('<font color=red> Conencted (on window) </font>')
                    self.message.append("Connectted (on log)")
                    self.baglan.setText("Disconnect")
                    self.baglan.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                    self.portCbox.setEnabled(False)
                    self.baudCbox.setEnabled(False)
                    self.pump.setEnabled(True)
                    self.peltier.setEnabled(True)
                    self.fan.setEnabled(True)
                    self.sicaklik.setEnabled(True)
                    self.cizdir.setEnabled(True)
                    """
                    self.sicaklik2.setEnabled(True)
                    self.cizdir2.setEnabled(True)
                    """
                    
        elif self.baglan.text() == "Disconnect":
            if self.mySerial.serialPort.isOpen():                
                # Pompa kapat ******************************************
                if self.pump.text() == "Pump On":
                    self.mySerial.serialPort.write("2".encode())  # seri porttan Arduino'ya 2 karakteri gonderildi
                    self.pump.setText("Pump Off")
                    self.pump.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px") 
                    self.labelPump.setText('<font color=red> Pump turned off </font>')
                self.pump.setEnabled(False)
                # peltier kapat ****************************************
                if self.peltier.text() == "Peltier Enable":
                    self.mySerial.serialPort.write("4".encode())  # seri porttan Arduino'ya 4 karakteri gonderildi
                    self.peltier.setText("Peltier Disable")
                    self.peltier.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px") 
                    self.labelPeltier.setText('<font color=red> Peltier is disabled </font>')
                self.peltier.setEnabled(False)
                # fan kapat ********************************************
                if self.fan.text() == "Fan Enable":
                    self.mySerial.serialPort.write("6".encode())  # seri porttan Arduino'ya 6 karakteri gonderildi
                    self.fan.setText("Fan Disable")
                    self.fan.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px") 
                    self.labelFan.setText('<font color=red> Fan is disabled </font>')
                self.fan.setEnabled(False)
                # sıcaklık okumayı kapat *******************************
                if self.sicaklik.text() == "Stop reading for tank":
                    self.mySerial.serialPort.write("8".encode())  # seri porttan Arduino'ya 8 karakteri gonderildi
                    self.sicaklik.setText("Tank Temperature")
                    self.sicaklik.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
                    self.labelSicaklik.setText('<font color=red> Tank temperature measuring was stopped </font>')
                self.sicaklik.setEnabled(False)
                """
                if self.sicaklik2.text() == "Stop reading for fan":
                    self.mySerial.serialPort.write("0".encode())  # seri porttan Arduino'ya 0 karakteri gonderildi
                    self.sicaklik2.setText("Fan Temperature")
                    self.sicaklik2.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
                    self.labelSicaklik2.setText('<font color=red> Fan temperature measuring was stopped (on window) </font>')
                    #self.message.append("GUI : ")
                self.sicaklik2.setEnabled(False)
                """           
                self.mySerial.serialPort.close()
                if self.mySerial.serialPort.isOpen() == False:
                    self.labelPort.setText('<font color=red> Disconnected (on log) </font>')
                    self.message.append("Disconnectted (on log)")
                    self.baglan.setText("Connect")
                    self.baglan.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")

                    self.portCbox.setEnabled(True)
                    self.baudCbox.setEnabled(True)
                    self.cizdir.setEnabled(False)
                    """
                    self.cizdir2.setEnabled(False)
                    """
            else:
                self.message.append("HATA KODU 1, baglan")

# 
    def messageTextEdit(self):  # seri porttan mesaj geldiginde bu fonksiyon calisacak
        self.incomingMessage = str(self.mySerial.data.decode())
        self.message.append(self.incomingMessage)
        # gelen verileri dizide sürekli güncelle        
        self.veri = self.mySerial.data.decode().split()
        #self.message.append(str(self.veri[1])
                            
        if (str(self.veri[0]) == "tank") and (str(self.veri[1]) != "okunamadi"):
            
            self.dataTankTut =  float(self.veri[1])
            self.dataFanTut = float(self.veri[3])
            
            # arduino verisini dirence cevirme
            self.R0Tank = 10000
            self.R2Tank = 9730
            # arduinouno  ile okursan 5V üzerinden okuyacağı için 
            self.R1Tank = ((self.R2Tank*(1023 - self.dataTankTut)) / (self.dataTankTut)) #Anlik NTC direci 
            
            # NTC icin denklem
            # self.betaTank = 3799 #Kelvin for 5K NTC
            self.betaTank = 3435 #Kelvin
            self.T0 = 298.15 #Kelvin -> 25 C
            self.TankK = 1/((1/self.T0)+((1/self.betaTank)*(np.log(self.R1Tank/self.R0Tank))))
            self.TankC = self.TankK - 273.15
            
            self.R0Cooler = 10000
            self.R2Cooler = 10000
            self.R1Cooler = ((self.R2Cooler*(1023 - self.dataFanTut)) / (self.dataFanTut)) #Anlik NTC direci 
            
            # NTC icin denklem
            self.betaCooler = 3435 #Kelvin
            self.T0 = 298.15 #Kelvin -> 25 C
            self.CoolerK = 1/((1/self.T0)+((1/self.betaCooler)*(np.log(self.R1Cooler/self.R0Cooler))))
            self.CoolerC = self.CoolerK - 273.15
            
            self.dataTank = self.dataTank + [self.TankC]
            self.dataFan = self.dataFan + [self.CoolerC]
            
            # LCD Displayda göster
            self.tempTank.display(self.TankC)
            self.tempCooler.display(self.CoolerC)
        
        if (self.onlineCizdir == True) and (len(self.dataTank) % 5 == 0):            
            self.graphicsView.plot(self.dataTank, pen="b")
            #self.graphicsView.plot(self.dataFan, pen="r")   

             
            
        """
        if (str(self.veri[0]) == "tank"):
            for k in range(149):
                self.dataTank[k] = self.dataTank[k+1]
                self.dataTank[149] = int(self.veri[1])
                self.dataFan[k] = self.dataFan[k+1]
                self.dataFan[149] = int(self.veri[3])
                #self.graphicsView.plot(self.dataTank)
                #self.graphicsView.plot(self.dataFan)
        """
    def funcs(self,func):  
        
        if func == self.yenile:
            self.portCbox.clear()
            self.portlar = serial.tools.list_ports.comports()
            for i in self.portlar:
                self.portCbox.addItem(str(i))
                
        if func == self.pump:
            if self.pump.text() == "Pump Off":
                if self.mySerial.serialPort.isOpen():
                    self.mySerial.serialPort.write("1".encode())  # seri porttan Arduino'ya 1 karakteri gonderildi
                    self.pump.setText("Pump On")
                    self.pump.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                    self.labelPump.setText('<font color=green> Pump turned on (on window) </font>')
                else:
                    self.message.append("GUI : bagli cihaz yok, pompayi acamasiniz")
            elif self.pump.text() == "Pump On":
                if self.mySerial.serialPort.isOpen():
                    self.mySerial.serialPort.write("2".encode())  # seri porttan Arduino'ya 2 karakteri gonderildi
                    self.pump.setText("Pump Off")
                    self.pump.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
                    self.labelPump.setText('<font color=red> Pump turned off (on window) </font>')
                else:
                    self.message.append("HATA KODU 2, pompa")
     
        if func == self.peltier:
            if self.peltier.text() == "Peltier Disable":  
                if self.mySerial.serialPort.isOpen():
                    self.peltier.setText("Peltier Enable")
                    self.peltier.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                    self.labelPeltier.setText('<font color=green> Peltier is working </font>')
                    self.mySerial.serialPort.write("3".encode())  # seri porttan Arduino'ya 3 karakteri gonderildi
                else:
                    self.message.append("GUI : Bagli cihaz yok, peltieri acamazsiniz")
            elif self.peltier.text() == "Peltier Enable":
                if self.mySerial.serialPort.isOpen():    
                    self.peltier.setText("Peltier Disable")
                    self.peltier.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px") 
                    self.labelPeltier.setText('<font color=red> Peltier is disabled </font>')
                    self.mySerial.serialPort.write("4".encode())  # seri porttan Arduino'ya 4 karakteri gonderildi
                else:
                    self.message.append("HATA KODU 3, peltier")
        if func == self.fan:
            if self.fan.text() == "Fan Disable":   
                if self.mySerial.serialPort.isOpen():
                    self.fan.setText("Fan Enable")
                    self.fan.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                    self.labelFan.setText('<font color=green> Fan is working </font>')
                    self.mySerial.serialPort.write("5".encode())  # seri porttan Arduino'ya 5 karakteri gonderildi
                else:
                    self.message.append("GUI : Bagli cihaz yok, fani acamazsiniz")
            elif self.fan.text() == "Fan Enable":
                if self.mySerial.serialPort.isOpen():
                    self.fan.setText("Fan Disable")
                    self.fan.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px") 
                    self.labelFan.setText('<font color=red> Fan is disabled </font>')
                    self.mySerial.serialPort.write("6".encode())  # seri porttan Arduino'ya 6 karakteri gonderildi
                else:
                    self.message.append("HATA KODU 4, fan")
                
        if func == self.sicaklik:
            if self.sicaklik.text() == "Tank Temperature":
                self.sicaklik.setText("Stop reading for tank")
                self.sicaklik.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                self.labelSicaklik.setText('<font color=green> Tank temperature is measuring (on window) </font>')
                self.mySerial.serialPort.write("7".encode())  # seri porttan Arduino'ya 5 karakteri gonderildi
            elif self.sicaklik.text() == "Stop reading for tank":
                self.sicaklik.setText("Tank Temperature")
                self.sicaklik.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
                self.labelSicaklik.setText('<font color=red> Tank temperature measuring was stopped (on window) </font>')
                self.mySerial.serialPort.write("8".encode())  # seri porttan Arduino'ya 6 karakteri gonderildi        
        
        """
        if func == self.sicaklik2:
            if self.sicaklik2.text() == "Fan Temperature":
                self.sicaklik2.setText("Stop reading for fan")
                self.sicaklik2.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                self.labelSicaklik2.setText('<font color=green> Fan temperature is measuring  </font>')
                self.mySerial.serialPort.write("9".encode())  # seri porttan Arduino'ya 5 karakteri gonderildi
            elif self.sicaklik2.text() == "Stop reading for fan":
                self.sicaklik2.setText("Fan Temperature")
                self.sicaklik2.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
                self.labelSicaklik2.setText('<font color=red> Fan temperature measuring was stopped (on window) </font>')
                self.mySerial.serialPort.write("0".encode())  # seri porttan Arduino'ya 6 karakteri gonderildi
                """
        if func == self.cizdir:
            if self.cizdir.text() == "Plot":
                self.onlineCizdir = True
                self.cizdir.setText("Stop Plotting")
                self.cizdir.setStyleSheet("font: bold 14px; background-color : green; max-width: 15em; padding: 6px")
                self.labelCizdir.setText('<font color=green> Online plotting started  </font>')
            elif self.cizdir.text() == "Stop Plotting":
                self.onlineCizdir = False
                self.cizdir.setText("Plot")
                self.cizdir.setStyleSheet("font: bold 14px; background-color : red; max-width: 15em; padding: 6px")
                self.labelCizdir.setText('<font color=red> Online plotting stopped  </font>')
                
# pop up olarak göster
# fonksiyon içerisinde tanımlama yaparsan popp up olarak açıyor
        """
        if func == self.cizdir2:   
            self.labelCizdir.setText('<font color=green> Tank temperature-time graph plotted </font>')
            self.message.append("Tank temperature-time graph plotted")  
            self.graphicsViewTank = pg.PlotWidget()
            self.graphicsView.plot(self.dataTank, pen="b")
            
            self.labelCizdir2.setText('<font color=green> Fan temperature-time graph plotted </font>')
            self.message.append("Fan temperature-time graph plotted")
            self.graphicsViewFan = pg.PlotWidget()
            #self.graphicsViewFan.plot(self.dataFan, pen="r")
        """      

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pen = Pencere()
    sys.exit(app.exec_())

            
        
        
        