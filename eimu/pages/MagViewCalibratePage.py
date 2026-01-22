import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from eimu.globalParams import g



class MagViewCalibrationFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.b = np.zeros([3, 1])
    self.A_1 = np.eye(3)
    self.F = 1

    self.magArray = []
    self.mag_x = []
    self.mag_y = []
    self.mag_z = []

    self.anim = None
    self.stop = False
    self.calibrated = False
    self.HISTORY_SIZE = 10000

    g.imu.setWorldFrameId(1)

    self.fig, self.ax = None, None

    self.label = tb.Label(self, text="VIEW MAG CALIBRATION", font=('Monospace',16, 'bold') ,bootstyle="dark")
    self.frame = tb.Frame(self)
    
    #create widgets to be added to frame1
    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',10,'bold'))
    self.calMagButton = tb.Button(self.frame, text="START",
                               style=buttonStyleName, padding=20,
                               command=self.runCalibration)
    
    #add framed widgets to frame
    self.calMagButton.pack(side='top', expand=True, fill="both")

    #add label and frame to CalibrateAccFrame
    self.label.pack(side='top', pady=(20,50))
    self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)



  def onClick(self,event):   
    if self.stop == False:
      self.anim.event_source.stop()
      self.stop = True
    # else:
    #   self.anim.event_source.start()
    #   self.stop = False

  def onClose(self,event): 
    plt.close()
    self.b = np.zeros([3, 1])
    self.A_1 = np.eye(3)
    self.F = 1

    self.magArray = []
    self.mag_x = []
    self.mag_y = []
    self.mag_z = []

    self.anim = None
    self.stop = False
    self.calibrated = False
    self.HISTORY_SIZE = 10000

    self.fig, self.ax = None, None 

      
  def animate(self,i):
    success, mx, my, mz = g.imu.readMag()
    
    if success:
      self.magArray.append([mx,my,mz])
      self.mag_x.append(mx)
      self.mag_y.append(my)
      self.mag_z.append(mz)

      # Clear all axis
      self.ax.cla()

      # Display the sub-plots
      self.ax.scatter(self.mag_x, self.mag_y, color='r')
      self.ax.scatter(self.mag_y, self.mag_z, color='g')
      self.ax.scatter(self.mag_z, self.mag_x, color='b')
      
    if len(self.mag_x) == self.HISTORY_SIZE:
      self.anim.event_source.stop()
    

  def runCalibration(self):
    self.fig, self.ax = plt.subplots(1, 1)
    self.ax.set_aspect(1)

    self.fig.canvas.mpl_connect('close_event', self.onClose)
    self.fig.canvas.mpl_connect('button_press_event', self.onClick)    
    self.anim = FuncAnimation(self.fig, self.animate, frames = np.arange(0, 10000, 1), interval=50)
    plt.show()