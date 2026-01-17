# REFERENCE: https://learn.adafruit.com/adafruit-sensorlab-gyroscope-calibration/gyro-calibration-with-jupyter
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import matplotlib.pyplot as plt
from collections import deque
import numpy as np
from termcolor import colored

from eimu.globalParams import g


class GyroCalibrateFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    # intialize parameter
    self.start_process = False
    self.loop_count = 0
    self.no_of_samples = 1000

    g.imu.setWorldFrameId(1)

    self.gyro_x = deque(maxlen=self.no_of_samples)
    self.gyro_y = deque(maxlen=self.no_of_samples)
    self.gyro_z = deque(maxlen=self.no_of_samples)

    self.label = tb.Label(self, text="CALIBRATE GYROSCOPE SENSOR", font=('Monospace',16, 'bold') ,bootstyle="dark")

    self.gxValFrame = tb.Frame(self)
    self.gyValFrame = tb.Frame(self)
    self.gzValFrame = tb.Frame(self)

    success, gx, gy, gz = g.imu.readGyroOffset()
    if not success:
      print("Error Occured while reading Initial Gyro Offset Values")

    self.gxText = tb.Label(self.gxValFrame, text="GX-OFFSET:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.gxVal = tb.Label(self.gxValFrame, text=f'{gx}', font=('Monospace',10), bootstyle="dark")

    self.gyText = tb.Label(self.gyValFrame, text="GY-OFFSET:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.gyVal = tb.Label(self.gyValFrame, text=f'{gy}', font=('Monospace',10), bootstyle="dark")

    self.gzText = tb.Label(self.gzValFrame, text="GZ-OFFSET:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.gzVal = tb.Label(self.gzValFrame, text=f'{gz}', font=('Monospace',10), bootstyle="dark")
  
    #create widgets to be added to the Fame
    percent = 0.0
    self.textVal = tb.Label(self, text=f'{percent} %', font=('Monospace',20, 'bold'), bootstyle="primary")
    self.progressBar = tb.Progressbar(self, bootstyle="danger striped", mode='determinate',
                                      maximum=100, length=200, value=0.0)

    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',15,'bold'))
    self.pressButton = tb.Button(self, text="START", style=buttonStyleName,
                                 command=self.change_btn_state)
    
    self.canvasFrame = tb.Frame(self)
    

    #add created widgets to displayFrame
    self.gxText.pack(side='left', fill='both')
    self.gxVal.pack(side='left', expand=True, fill='both')

    self.gyText.pack(side='left', fill='both')
    self.gyVal.pack(side='left', expand=True, fill='both')

    self.gzText.pack(side='left', fill='both')
    self.gzVal.pack(side='left', expand=True, fill='both')
    
    #add created widgets to Frame
    self.label.pack(side='top', pady=(20,50))
    self.textVal.pack(side='top', expand=True, fill='y')
    self.progressBar.pack(side='top', expand=True, fill='x', padx=50)
    self.pressButton.pack(side='top', fill='y')
    self.canvasFrame.pack(side='top', expand=True, fill='both', pady=(10,0))

    #create widgets to be added to the canvasFame
    self.canvas = tb.Canvas(self.canvasFrame, width=300, height=2, autostyle=False ,bg="#FFFFFF", relief='solid')

    #add created widgets to canvasFame
    self.canvas.pack(side='left', expand=True, fill='both', pady=(0,20))

    self.gxValFrame.pack(side='top', fill='x')
    self.gyValFrame.pack(side='top', fill='x')
    self.gzValFrame.pack(side='top', fill='x')

    # start process
    self.calibrate_imu()

  def reset_all_params(self):
    self.loop_count = 0
    
    self.gyro_x = deque(maxlen=self.no_of_samples)
    self.gyro_y = deque(maxlen=self.no_of_samples)
    self.gyro_z = deque(maxlen=self.no_of_samples)

    percent = 0.0
    self.textVal.configure(text=f'{int(percent)} %')
    self.progressBar['value'] = percent

  def read_data(self):
    if self.start_process:

      self.gxVal.configure(text="0.0")
      self.gyVal.configure(text="0.0")
      self.gzVal.configure(text="0.0")

      success, gx, gy, gz = g.imu.readGyroRaw()

      if success:
        self.gyro_x.append(gx)
        self.gyro_y.append(gy)
        self.gyro_z.append(gz)

        self.loop_count += 1
        percent = (self.loop_count*100)/self.no_of_samples
        self.textVal.configure(text=f'{int(percent)} %')
        self.progressBar['value'] = percent

        if self.loop_count >= self.no_of_samples:
          percent = 100.0
          self.textVal.configure(text=f'{int(percent)} %')
          self.progressBar['value'] = percent
          self.plot_calibrated_data()
        else:
          self.canvas.after(10, self.read_data)

    else:
      self.reset_all_params()
      self.canvas.after(10, self.calibrate_imu)

  def plot_calibrated_data(self):

    gx_offset = self.average(self.gyro_x)
    gy_offset = self.average(self.gyro_y)
    gz_offset = self.average(self.gyro_z)

    g.imu.writeGyroOffset(gx_offset, gy_offset, gz_offset)

    success, gx_offset, gy_offset, gz_offset = g.imu.readGyroOffset()

    if not success:
      print("Error Occured while reading Final Gyro Offset Values")

    self.gxVal.configure(text=f'{gx_offset}')
    self.gyVal.configure(text=f'{gy_offset}')
    self.gzVal.configure(text=f'{gz_offset}')

    gyro_calibration = [ gx_offset, gy_offset, gz_offset ]

    print(colored("\ngyro offsets in rad/s:", 'green'))
    print(gyro_calibration)

    fig, (gyroUncal, gyroCal) = plt.subplots(nrows=2)

    # Clear all axis
    gyroUncal.cla()
    gyroCal.cla()

    t = np.linspace(0, len(self.gyro_x), len(self.gyro_x))

    # plot uncalibrated data
    gyroUncal.set_ylim([-1,1])
    gyroUncal.grid(which = "major", linewidth = 0.5)
    gyroUncal.grid(which = "minor", linewidth = 0.2)
    gyroUncal.minorticks_on()

    gyroUncal.plot(t, self.gyro_x, color='r')
    gyroUncal.plot(t, self.gyro_y, color='g')
    gyroUncal.plot(t, self.gyro_z, color='b')
    gyroUncal.title.set_text("Uncalibrated Gyro")
    gyroUncal.set(ylabel='rad/s')

    # plot calibrated data
    gyroCal.set_ylim([-1,1])
    gyroCal.grid(which = "major", linewidth = 0.5)
    gyroCal.grid(which = "minor", linewidth = 0.2)
    gyroCal.minorticks_on()

    gyroCal.plot(t, [x - gyro_calibration[0] for x in self.gyro_x], color='r')
    gyroCal.plot(t, [y - gyro_calibration[1] for y in self.gyro_y], color='g')
    gyroCal.plot(t, [z - gyro_calibration[2] for z in self.gyro_z], color='b')
    gyroCal.title.set_text("Calibrated Gyro")
    gyroCal.set(ylabel='rad/s')

    fig.tight_layout()
    plt.show()

  def calibrate_imu(self):
    if self.start_process:
      self.reset_all_params()
      self.read_data()
    else:
      self.reset_all_params()
      self.canvas.after(10, self.calibrate_imu)

  def change_btn_state(self):
    if self.start_process:
      self.start_process = False
      self.pressButton.configure(text='START')

    else:
      self.start_process = True
      self.pressButton.configure(text='STOP')

  def average(self, val):
      ans = 0
      for i in val:
        ans= ans + i
      
      ans = ans/len(val)
      
      return ans