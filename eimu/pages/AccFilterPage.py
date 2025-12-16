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

    self.fig, self.axes = None, None

    self.ylim = [-2, 2]

    self.accRawDataList = []
    self.accFiltDataList = []

    self.dataPoints = 50
    
    g.eimu.setWorldFrameId(1)

    self.label = tb.Label(self, text="FILTER ACC DATA", font=('Monospace',16, 'bold') ,bootstyle="dark")

    g.coordNum = 0
    self.selectCoord = SelectValueFrame(self, keyTextInit=f"CO-ORDINATE: ", valTextInit=g.coordList[g.coordNum],
                                          initialComboValues=g.coordList, middileware_func=self.selectCoordFunc )
    
    success, accFilterCF = g.eimu.getAccFilterCF()
    if success:
      g.accFilterCF = accFilterCF
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

    success, ax, ay, az = g.eimu.readLinearAcc()
    if not success:
      print("Error Occured while reading Initial Linear Acceleration Data")

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
    if text:
      g.eimu.setAccFilterCF(float(text))
      success, accFilterCF = g.eimu.getAccFilterCF()
      if success:
        g.accFilterCF = accFilterCF
  
    return g.accFilterCF
  

  def selectCoordFunc(self, coord_val_str):
    if coord_val_str == g.coordList[0]:
      g.coordNum = 0
      
    elif coord_val_str == g.coordList[1]:
      g.coordNum = 1
    
    elif coord_val_str == g.coordList[2]:
      g.coordNum = 2

    return g.coordList[g.coordNum]


  def onClose(self,event): 
    plt.close()
    self.fig, self.ax = None, None 


  def animate(self,i):

    success0, ax_raw, ay_raw, az_raw = g.eimu.readLinearAccRaw()
    success1, ax, ay, az = g.eimu.readLinearAcc()

    if success0 and success1:

      self.axVal.configure(text=f"{ax}")
      self.ayVal.configure(text=f"{ay}")
      self.azVal.configure(text=f"{az}")

      if g.coordNum==0:
        self.accRawDataList.append(ax_raw)
        self.accFiltDataList.append(ax)
      elif g.coordNum==1:
        self.accRawDataList.append(ay_raw)
        self.accFiltDataList.append(ay)
      elif g.coordNum==2:
        self.accRawDataList.append(az_raw)
        self.accFiltDataList.append(az)

      # Fix the list size so that the animation plot 'window' is x number of points

      accRawDataList = self.accRawDataList[-self.dataPoints:]
      accFiltDataList = self.accFiltDataList[-self.dataPoints:]
      
      self.axes.clear()
      if g.coordNum==0:
        self.axes.plot(accRawDataList, color="darkcyan")
        self.axes.plot(accFiltDataList, color="red")
      elif g.coordNum==1:
        self.axes.plot(accRawDataList, color="darkorange")
        self.axes.plot(accFiltDataList, color="green")
      elif g.coordNum==2:
        self.axes.plot(accRawDataList, color="tomato")
        self.axes.plot(accFiltDataList, color="blue")
      
      # self.ax.plot(azDataList)
      
      self.axes.grid(which = "major", linewidth = 0.5)
      self.axes.grid(which = "minor", linewidth = 0.2)
      self.axes.minorticks_on()

      self.axes.set_ylim(self.ylim) # Set Y axis limit of plot
      self.axes.set_title(f'Linear Acceleration {g.coordList[g.coordNum]} Data') # Set title of figure
      self.axes.set_ylabel("linear acceleration in m/s^2") # Set title of y axis 
      self.axes.set_xlabel("number of data points") # Set title of z axis 
      self.axes.legend(["unfiltered", "filtered"], loc ="upper right")

        
        
    ##    # Pause the plot for INTERVAL seconds 
    ##    plt.pause(INTERVAL)


  def runVisualization(self):
    
    self.fig = plt.figure()
    self.axes = self.fig.add_subplot(111)

    self.axes.set_ylim(self.ylim) # Set Y axis limit of plot
    self.axes.set_title(f'Linear Acceleration {g.coordList[g.coordNum]} Data') # Set title of figure
    self.axes.set_ylabel("linear acceleration in m/s^2") # Set title of y axis 
    self.axes.set_xlabel("number of data points") # Set title of z axis 
    self.axes.legend(["unfiltered", "filtered"], loc ="upper right")

    self.fig.canvas.mpl_connect('close_event', self.onClose)
    self.anim = FuncAnimation(self.fig, self.animate, frames=100, interval=50)
    plt.show()