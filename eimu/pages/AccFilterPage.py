import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from eimu.globalParams import g
from eimu.components.SetValueFrame import SetValueFrame
from eimu.components.SelectValueFrame import SelectValueFrame



class AccFilterFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.fig, self.ax = None, None

    self.ylim = [-2, 2]

    self.axDataList = []
    self.ayDataList = []
    self.azDataList = []

    self.dataPoints = 50
    
    isSuccessful = g.eimu.clearDataBuffer()
    isSuccessful = g.eimu.setWorldFrameId(1)

    self.label = tb.Label(self, text="FILTER ACC DATA", font=('Monospace',16, 'bold') ,bootstyle="dark")

    g.coordNum = 0
    self.selectCoord = SelectValueFrame(self, keyTextInit=f"CO-ORDINATE: ", valTextInit=g.coordList[g.coordNum],
                                          initialComboValues=g.coordList, middileware_func=self.selectCoordFunc )
    
    g.accFilterCF = g.eimu.getAccFilterCF()
    self.setAccFilterCFFrame = SetValueFrame(self, keyTextInit="ACC_LPF_CF: ", valTextInit=g.accFilterCF,
                                middleware_func=self.setAccFilterCFFunc)
    
    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',12,'bold'))

    self.button = tb.Button(self, text="READ ACC DATA", style=buttonStyleName,
                             padding=20, command=self.runVisualization)
    

    self.imuDisplayFrame = tb.Frame(self)

    self.accelerationValFrame = tb.Frame(self.imuDisplayFrame)
    self.axValFrame = tb.Frame(self.accelerationValFrame)
    self.ayValFrame = tb.Frame(self.accelerationValFrame)
    self.azValFrame = tb.Frame(self.accelerationValFrame)

    ax, ay, az = g.eimu.readLinearAcc()

    self.axText = tb.Label(self.axValFrame, text="AX:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.axVal = tb.Label(self.axValFrame, text=f'{ax}', font=('Monospace',10), bootstyle="dark")

    self.ayText = tb.Label(self.ayValFrame, text="AY:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.ayVal = tb.Label(self.ayValFrame, text=f'{ay}', font=('Monospace',10), bootstyle="dark")

    self.azText = tb.Label(self.azValFrame, text="AZ:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.azVal = tb.Label(self.azValFrame, text=f'{az}', font=('Monospace',10), bootstyle="dark")
    

    #add created widgets to displayFrame
    self.axText.pack(side='left', fill='both')
    self.axVal.pack(side='left', expand=True, fill='both')

    self.ayText.pack(side='left', fill='both')
    self.ayVal.pack(side='left', expand=True, fill='both')

    self.azText.pack(side='left', fill='both')
    self.azVal.pack(side='left', expand=True, fill='both')


    #add created widgets to Frame
    self.label.pack(side='top', pady=(20,20))
    self.selectCoord.pack(side='top', fill='y', pady=(30,0))
    self.setAccFilterCFFrame.pack(side='top', fill='y', pady=(30,0))
    self.button.pack(side='top', fill='y', pady=(50,0))
    self.imuDisplayFrame.pack(side='top', fill='x', pady=(50,0))

    self.accelerationValFrame.pack(side='left', expand=True, fill='both')

    self.axValFrame.pack(side='top', fill='x')
    self.ayValFrame.pack(side='top', fill='x')
    self.azValFrame.pack(side='top', fill='x')  
  
    ############################################
  

  def setAccFilterCFFunc(self, text):
    try:
      if text:
        isSuccessful = g.eimu.setAccFilterCF(float(text))
        g.accFilterCF = g.eimu.getAccFilterCF()
    except:
      pass
  
    return g.accFilterCF
  

  def selectCoordFunc(self, coord_val_str):
    try:
      if coord_val_str == g.coordList[0]:
        g.coordNum = 0
        
      elif coord_val_str == g.coordList[1]:
        g.coordNum = 1
      
      elif coord_val_str == g.coordList[2]:
        g.coordNum = 2

    except:
      pass

    return g.coordList[g.coordNum]


  def onClose(self,event): 
    plt.close()
    self.fig, self.ax = None, None 


  def animate(self,i):
    try:

      ax_raw, ay_raw, az_raw = g.eimu.readLinearAccRaw()
      ax, ay, az = g.eimu.readLinearAcc()

      self.axVal.configure(text=f"{ax}")
      self.ayVal.configure(text=f"{ay}")
      self.azVal.configure(text=f"{az}")

      if g.coordNum==0:
        self.axDataList.append(ax_raw)
        self.ayDataList.append(ax)
      elif g.coordNum==1:
        self.axDataList.append(ay_raw)
        self.ayDataList.append(ay)
      elif g.coordNum==2:
        self.axDataList.append(az_raw)
        self.ayDataList.append(az)

      # self.azDataList.append(az)

      # Fix the list size so that the animation plot 'window' is x number of points

      axDataList = self.axDataList[-self.dataPoints:]
      ayDataList = self.ayDataList[-self.dataPoints:]
      # azDataList = self.azDataList[-self.dataPoints:]
      
      self.ax.clear()
      if g.coordNum==0:
        self.ax.plot(axDataList, color="darkcyan")
        self.ax.plot(ayDataList, color="red")
      elif g.coordNum==1:
        self.ax.plot(axDataList, color="darkorange")
        self.ax.plot(ayDataList, color="green")
      elif g.coordNum==2:
        self.ax.plot(axDataList, color="tomato")
        self.ax.plot(ayDataList, color="blue")
      
      # self.ax.plot(azDataList)
      
      self.ax.grid(which = "major", linewidth = 0.5)
      self.ax.grid(which = "minor", linewidth = 0.2)
      self.ax.minorticks_on()

      self.ax.set_ylim(self.ylim) # Set Y axis limit of plot
      self.ax.set_title("Acceleration Data") # Set title of figure
      self.ax.set_ylabel("linear acceleration in m/s^2") # Set title of y axis 
      self.ax.set_xlabel("number of data points") # Set title of z axis 

      # self.ax.legend(["ax", "ay", "az"], loc ="upper right")
      self.ax.legend(["unfiltered", "filtered"], loc ="upper right")

        
        
    ##    # Pause the plot for INTERVAL seconds 
    ##    plt.pause(INTERVAL)
    except:
      print ("Error Readind Acc Data")
      pass


  def runVisualization(self):
    
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111)

    self.ax.set_ylim(self.ylim) # Set Y axis limit of plot
    self.ax.set_title("Acceleration Data") # Set title of figure
    self.ax.set_ylabel("linear acceleration in m/s^2") # Set title of y axis 
    self.ax.set_xlabel("number of data points") # Set title of z axis 

    self.ax.legend(["ax", "ay", "az"], loc ="upper right")

    self.fig.canvas.mpl_connect('close_event', self.onClose)
    self.anim = FuncAnimation(self.fig, self.animate, frames=100, interval=50)
    plt.show()