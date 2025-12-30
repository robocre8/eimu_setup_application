import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import linalg
import time
from termcolor import colored

from eimu.globalParams import g



class AccCalibrateFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.b = np.zeros([3, 1])
    self.A_1 = np.eye(3)
    self.F = g.gravity

    self.accArray = []
    self.acc_x = []
    self.acc_y = []
    self.acc_z = []

    self.acc_cal_x = []
    self.acc_cal_y = []
    self.acc_cal_z = []

    self.start_process = False
    self.loop_count = 0
    self.no_of_samples = 500
    self.total_no_of_samples = 3000

    self.incrementBar = 0

    g.eimu.setWorldFrameId(1)

    self.label = tb.Label(self, text="CALIBRATE ACCELEROMETER SENSOR", font=('Monospace',16, 'bold') ,bootstyle="dark")
  
    #create widgets to be added to the Fame
    percent = 0.0
    self.textVal = tb.Label(self, text=f'{percent} %', font=('Monospace',20, 'bold'), bootstyle="primary")

    self.progressBar = []
    for i in range(6):
      self.progressBar.append( tb.Progressbar(self, bootstyle="danger striped", mode='determinate',
                                      maximum=100, length=200, value=0.0) )

    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',15,'bold'))
    self.pressButton = tb.Button(self, text="START", style=buttonStyleName,
                                 command=self.change_btn_state)
    
    self.canvasFrame = tb.Frame(self)
    
    #add created widgets to Frame
    self.label.pack(side='top', pady=(20,50))
    self.textVal.pack(side='top', expand=True, fill='y')

    for i in range(6):
      self.progressBar[i].pack(side='top', expand=True, fill='x', padx=10)

    self.pressButton.pack(side='top', fill='y')
    self.canvasFrame.pack(side='top', expand=True, fill='both', pady=(10,0))

    #create widgets to be added to the canvasFame
    self.canvas = tb.Canvas(self.canvasFrame, width=300, height=2, autostyle=False ,bg="#FFFFFF", relief='solid')

    #add created widgets to canvasFame
    self.canvas.pack(side='left', expand=True, fill='both', pady=(0,20))

    # start process
    self.read_data()


  def calibrate(self):

    if len(self.accArray) < self.total_no_of_samples:
      print("Not enough samples for accelerometer calibration, RETRY")
      return
      
    # ellipsoid fit
    s = np.array(self.accArray).T
    M, n, d = self.__ellipsoid_fit(s)
    
    # calibration parameters
    # note: some implementations of sqrtm return complex type, taking real
    M_1 = linalg.inv(M)
    self.b = -np.dot(M_1, n)
    self.A_1 = np.real(self.F / np.sqrt(np.dot(n.T, np.dot(M_1, n)) - d) * linalg.sqrtm(M))

    ################################################

    b_vect = np.zeros([3, 1])
    A_mat = np.eye(3)
    
    g.eimu.writeAccBiasVect(self.b[0][0], self.b[1][0], self.b[2][0])

    success, b_vect[0][0], b_vect[1][0], b_vect[2][0] = g.eimu.readAccBiasVect()
    if not success:
      print("Error Occured while reading Acc Bias Values")
    
    g.eimu.writeAccScaleMatR0(self.A_1[0][0], self.A_1[0][1], self.A_1[0][2])
    g.eimu.writeAccScaleMatR1(self.A_1[1][0], self.A_1[1][1], self.A_1[1][2])
    g.eimu.writeAccScaleMatR2(self.A_1[2][0], self.A_1[2][1], self.A_1[2][2])

    success0, A_mat[0][0], A_mat[0][1], A_mat[0][2] = g.eimu.readAccScaleMatR0()
    success1, A_mat[1][0], A_mat[1][1], A_mat[1][2] = g.eimu.readAccScaleMatR1()
    success2, A_mat[2][0], A_mat[2][1], A_mat[2][2] = g.eimu.readAccScaleMatR2()

    if not (success0 and success1 and success2):
      print("Error Occured while reading Acc Scale + Misalignment Values")
    

    ################################################
    
    print(colored("\nAcc Bias (b_vect)", 'green'))
    print(b_vect)
    
    print(colored("\nAcc Scale + Misalignment (A_mat):", 'green'))
    print(A_mat)




  def __ellipsoid_fit(self, s):
    ''' Estimate ellipsoid parameters from a set of points.

      Parameters
      ----------
      s : array_like
        The samples (M,N) where M=3 (x,y,z) and N=number of samples.

      Returns
      -------
      M, n, d : array_like, array_like, float
        The ellipsoid parameters M, n, d.

      References
      ----------
      .. [1] Qingde Li; Griffiths, J.G., "Least squares ellipsoid specific
          fitting," in Geometric Modeling and Processing, 2004.
          Proceedings, vol., no., pp.335-340, 2004
    '''

    # D (samples)
    D = np.array([s[0]**2., s[1]**2., s[2]**2.,
                  2.*s[1]*s[2], 2.*s[0]*s[2], 2.*s[0]*s[1],
                  2.*s[0], 2.*s[1], 2.*s[2], np.ones_like(s[0])])

    # S, S_11, S_12, S_21, S_22 (eq. 11)
    S = np.dot(D, D.T)
    S_11 = S[:6,:6]
    S_12 = S[:6,6:]
    S_21 = S[6:,:6]
    S_22 = S[6:,6:]

    # C (Eq. 8, k=4)
    C = np.array([[-1,  1,  1,  0,  0,  0],
                  [ 1, -1,  1,  0,  0,  0],
                  [ 1,  1, -1,  0,  0,  0],
                  [ 0,  0,  0, -4,  0,  0],
                  [ 0,  0,  0,  0, -4,  0],
                  [ 0,  0,  0,  0,  0, -4]])

    # v_1 (eq. 15, solution)
    E = np.dot(linalg.inv(C),
                S_11 - np.dot(S_12, np.dot(linalg.inv(S_22), S_21)))

    E_w, E_v = np.linalg.eig(E)

    v_1 = E_v[:, np.argmax(E_w)]
    if v_1[0] < 0: v_1 = -v_1

    # v_2 (eq. 13, solution)
    v_2 = np.dot(np.dot(-np.linalg.inv(S_22), S_21), v_1)

    # quadric-form parameters
    M = np.array([[v_1[0], v_1[3], v_1[4]],
                  [v_1[3], v_1[1], v_1[5]],
                  [v_1[4], v_1[5], v_1[2]]])
    n = np.array([[v_2[0]],
                  [v_2[1]],
                  [v_2[2]]])
    d = v_2[3]

    return M, n, d


  def validate_calibration(self):
    norms = []
    for a in self.accArray:
        a = np.array(a).reshape(3,1)
        a_cal = self.A_1 @ (a - self.b)
        norms.append(np.linalg.norm(a_cal))
        self.acc_cal_x.append(a_cal[0])
        self.acc_cal_y.append(a_cal[1])
        self.acc_cal_z.append(a_cal[2])
        
    print("Gravity norm mean:", np.mean(norms))
    print("Gravity norm std:", np.std(norms))


  def is_static(self):
    success, gx, gy, gz = g.eimu.readGyro()
    if success:
      w = np.sqrt(gx*gx + gy*gy + gz*gz)
      return w < 0.02  # rad/s
    else:
      return False


  def read_data(self):
    # for bar in self.progressBar:
    if self.start_process and self.incrementBar<len(self.progressBar):

      if self.is_static():
        # print("Device moving — calibration aborted")
        # percent = (self.loop_count*100)/self.no_of_samples
        # self.textVal.configure(text=f'{int(percent)} %')
        # self.progressBar[self.incrementBar]['value'] = percent
        # self.canvas.after(10, self.read_data)
      
        success, ax, ay, az = g.eimu.readAccRaw()

        if success:
          self.accArray.append([ax,ay,az])
          self.acc_x.append(ax)
          self.acc_y.append(ay)
          self.acc_z.append(az)

          self.loop_count += 1
          percent = (self.loop_count*100)/self.no_of_samples
          self.textVal.configure(text=f'{int(percent)} %')
          self.progressBar[self.incrementBar]['value'] = percent

          if self.loop_count >= self.no_of_samples:
            percent = 100.0
            self.textVal.configure(text=f'{percent} %')
            self.progressBar[self.incrementBar]['value'] = percent
            self.incrementBar += 1
            self.start_process = False
            self.loop_count = 0
            self.pressButton.configure(text='START')
            self.canvas.after(10, self.read_data)
            # self.plot_calibrated_data()
          
          else:
            self.canvas.after(10, self.read_data)
      else:
        self.canvas.after(10, self.read_data)

    elif self.incrementBar>=len(self.progressBar):
      self.calibrate()
      self.validate_calibration()
      self.plot_calibrated_data()
      return

    else:
      self.canvas.after(10, self.read_data)
  

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


  def reset_all_params(self):
    self.loop_count = 0
    
    self.accArray = []
    self.acc_x = []
    self.acc_y = []
    self.acc_z = []

    self.start_process = False
    self.loop_count = 0

    percent = 0
    self.textVal.configure(text=f'{percent} %')
    for i in range(6):
      self.progressBar[i]['value'] = percent


  def plot_calibrated_data(self):

    fig, (accUncal, accCal) = plt.subplots(nrows=2)

    # Clear all axis
    accUncal.cla()
    accCal.cla()

    t = np.linspace(0, len(self.acc_x), len(self.acc_x))

    # plot uncalibrated data
    accUncal.set_ylim([-10,10])
    accUncal.grid(which = "major", linewidth = 0.5)
    accUncal.grid(which = "minor", linewidth = 0.2)
    accUncal.minorticks_on()

    accUncal.plot(t, self.acc_x, color='r')
    accUncal.plot(t, self.acc_y, color='g')
    accUncal.plot(t, self.acc_z, color='b')
    accUncal.title.set_text("Uncalibrated Acc")
    accUncal.set(ylabel='m/s^2')

    # plot calibrated data
    accCal.set_ylim([-10,10])
    accCal.grid(which = "major", linewidth = 0.5)
    accCal.grid(which = "minor", linewidth = 0.2)
    accCal.minorticks_on()

    accCal.plot(t, [x for x in self.acc_x], color='r')
    accCal.plot(t, [y for y in self.acc_y], color='g')
    accCal.plot(t, [z for z in self.acc_z], color='b')
    accCal.title.set_text("Calibrated Acc")
    accCal.set(ylabel='m/s^2')

    fig.tight_layout()
    plt.show()