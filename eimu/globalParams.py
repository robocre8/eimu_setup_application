
class g():
  app = None
  eimu = None
  port = "None"

  gravity = 9.80665

  i2cAddress = None
  filterGain = None
  frameId = None
  frameList = ["NWU", "ENU", "NED"]

  accFilterCF = None
  coordList = ["x", "y", "z"]
  coordNum = 0