import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from globalParams import g

from vpython import *
import numpy as np
import math as m

from components.SetValueFrame import SetValueFrame
from components.SelectValueFrame import SelectValueFrame


class GainSetupVizFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    ##############################
    self.scene=None
    self.xAxis=None
    self.yAxis=None
    self.zAxis=None
    self.xArrow=None
    self.yArrow=None
    self.zArrow=None
    self.myBox=None
    self.myObj=None
    ##############################

    self.label = tb.Label(self, text="SET FILTER GAIN", font=('Monospace',16, 'bold') ,bootstyle="dark")
  
    #create widgets to be added to the Fame
    g.frameId = int(g.serClient.get("/frame-id"))
    self.selectFrameId = SelectValueFrame(self, keyTextInit=f"REFERENCE_FRAME: ", valTextInit=g.frameList[g.frameId],
                                          initialComboValues=g.frameList, middileware_func=self.selectFrameIdFunc)
    
    g.filterGain = g.serClient.get("/gain")
    self.setFilterGain = SetValueFrame(self, keyTextInit="FILTER_GAIN: ", valTextInit=g.filterGain,
                                middleware_func=self.setFilterGainFunc)
    
    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',12,'bold'))

    self.button = tb.Button(self, text="VIEW IMU", style=buttonStyleName,
                             padding=20, command=self.start_imu_viz)
    
    
    # self.rpyDisplayFrame = tb.Frame(self)

    self.rollValFrame = tb.Frame(self)
    self.pitchValFrame = tb.Frame(self)
    self.yawValFrame = tb.Frame(self)

    roll, pitch, yaw = g.serClient.get('/rpy')

    self.rollText = tb.Label(self.rollValFrame, text="ROLL:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.rollVal = tb.Label(self.rollValFrame, text=f'{roll}', font=('Monospace',10), bootstyle="dark")

    self.pitchText = tb.Label(self.pitchValFrame, text="PITCH:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.pitchVal = tb.Label(self.pitchValFrame, text=f'{pitch}', font=('Monospace',10), bootstyle="dark")

    self.yawText = tb.Label(self.yawValFrame, text="YAW:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.yawVal = tb.Label(self.yawValFrame, text=f'{yaw}', font=('Monospace',10), bootstyle="dark")

    self.canvasFrame = tb.Frame(self)
    

    #add created widgets to displayFrame
    self.rollText.pack(side='left', fill='both')
    self.rollVal.pack(side='left', expand=True, fill='both')

    self.pitchText.pack(side='left', fill='both')
    self.pitchVal.pack(side='left', expand=True, fill='both')

    self.yawText.pack(side='left', fill='both')
    self.yawVal.pack(side='left', expand=True, fill='both')

    #add created widgets to Frame
    self.label.pack(side='top', pady=(20,20))
    self.selectFrameId.pack(side='top', fill='y', pady=(30,0))
    self.setFilterGain.pack(side='top', fill='y', pady=(30,0))
    self.button.pack(side='top', fill='y', pady=(50,0))

    self.rollValFrame.pack(side='top', fill='x')
    self.pitchValFrame.pack(side='top', fill='x')
    self.yawValFrame.pack(side='top', fill='x')
  
    self.canvasFrame.pack(side='top', expand=True, fill='both', pady=(10,0))

    #create widgets to be added to the canvasFame
    self.canvas = tb.Canvas(self.canvasFrame, width=300, height=10, autostyle=False ,bg="#FFFFFF", relief='solid')

    #add created widgets to canvasFame
    self.canvas.pack(side='left', expand=True, fill='both')
    ############################################


  def setFilterGainFunc(self, text):
    try:
      if text:
        isSuccessful = g.serClient.send("/gain", float(text))
        val = g.serClient.get("/gain")
        g.filterGain = val
    except:
      pass
  
    return g.filterGain
  

  def selectFrameIdFunc(self, frame_val_str):
    try:
      if frame_val_str:
        
        if frame_val_str == g.frameList[0]:
          isSuccessful = g.serClient.send("/frame-id", 0)
          
        elif frame_val_str == g.frameList[1]:
          isSuccessful = g.serClient.send("/frame-id", 1)
        
        elif frame_val_str == g.frameList[2]:
          isSuccessful = g.serClient.send("/frame-id", 2)

    except:
      pass

    g.frameId = int(g.serClient.get("/frame-id"))
    return g.frameList[g.frameId]
  

  def start_imu_viz(self):
    ##----------------------------------------------------------------##
    self.scene = scene
    self.scene.range=5
    self.scene.forward=vector(-1,-1,-1)
    self.scene.width=500
    self.scene.height=500

    self.xAxis = arrow(length=1.25, shaftwidth=.08, color=color.red,
                  axis=vector(0,0,1), opacity=1.0) # (y,z,x)
    self.yAxis = arrow(length=1.25, shaftwidth=.08, color=color.green,
                  axis=vector(1,0,0), opacity=1.0) # (y,z,x)
    self.zAxis = arrow(length=1.25, shaftwidth=.08, color=color.blue,
                  axis=vector(0,1,0), opacity=1.0) # (y,z,x)

    self.xArrow = arrow(length=3, shaftwidth=.1, color=color.red,
                    axis=vector(0,0,1), opacity=.3) # (y,z,x)
    self.yArrow = arrow(length=3, shaftwidth=.1, color=color.green,
                  axis=vector(1,0,0), opacity=.3) # (y,z,x)
    self.zArrow = arrow(length=3, shaftwidth=.1, color=color.blue,
                  axis=vector(0,1,0), opacity=.3) # (y,z,x)
    
    self.myBox = box()
    self.myBox.length = 1.5
    self.myBox.width = 1.5
    self.myBox.height = 0.25
    self.myBox.opacity = 0.3 

    # # g.frameId = int(g.serClient.get("/frame-id"))

    # # if g.frameList[g.frameId] == "ENU":    
    # #   self.myBox.length = 1.5
    # #   self.myBox.width = 3.5
    
    self.myObj = compound([self.myBox])

    self.vizualize_imu()


  def vizualize_imu(self):
    try:
      roll, pitch, yaw = g.serClient.get('/rpy')
      self.rollVal.configure(text=f"{roll}")
      self.pitchVal.configure(text=f"{pitch}")
      self.yawVal.configure(text=f"{yaw}")

      ##### perform axis computations #####################
      up=np.array([0,0,1]) # (x,y,z)
      x_vect=np.array([m.cos(yaw)*m.cos(pitch), m.sin(yaw)*m.cos(pitch), -1.00*m.sin(pitch)]) # (x,y,z)
      y_vect = np.cross(up,x_vect) # (x,y,z)
      z_vect = np.cross(x_vect,y_vect) # (x,y,z)

      z_rot = z_vect*m.cos(roll)+(np.cross(x_vect,z_vect))*m.sin(roll)

      y_rot = np.cross(z_rot, x_vect)

      ######### draw axis in vpyton ########################
      self.xArrow.axis = vector(x_vect[1], x_vect[2], x_vect[0])# (y,z,x)
      self.xArrow.length = 3

      self.yArrow.axis = vector(y_rot[1], y_rot[2], y_rot[0])# (y,z,x)
      self.yArrow.length = 2

      self.zArrow.axis = vector(z_rot[1], z_rot[2], z_rot[0])# (y,z,x)
      self.zArrow.length = 1.5

      self.myObj.axis = vector(x_vect[1], x_vect[2], x_vect[0]) # (y,z,x)
      self.myObj.up = vector(z_rot[1], z_rot[2], z_rot[0]) # (y,z,x)

      self.canvas.after(10, self.vizualize_imu)
    except:
      pass