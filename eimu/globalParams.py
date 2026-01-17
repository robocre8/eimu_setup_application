
class g():
  app = None
  imu = None
  port = "None"

  i2cAddress = None
  filterGain = None
  frameId = None
  frameList = ["NWU", "ENU", "NED"]

  accFilterCF = None
  coordList = ["x", "y", "z"]
  coordNum = 0