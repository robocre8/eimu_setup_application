import serial
import struct
from typing import Tuple
from enum import Enum
from time import sleep

# class EIMUSerialError(Exception):
#     """Custom exception for for EIMU Comm failure"""
#     pass

#------------------------------------------------
START_BYTE = 0xBB
READ_QUAT = 0x01
READ_RPY = 0x02
READ_RPY_VAR = 0x03
WRITE_RPY_VAR = 0x04
READ_ACC = 0x05
READ_ACC_RAW = 0x06
READ_ACC_OFF = 0x07
WRITE_ACC_OFF = 0x08
READ_ACC_VAR = 0x09
WRITE_ACC_VAR = 0x0A
READ_GYRO = 0x0B
READ_GYRO_RAW = 0x0C
READ_GYRO_OFF = 0x0D
WRITE_GYRO_OFF = 0x0E
READ_GYRO_VAR = 0x0F
WRITE_GYRO_VAR = 0x10
READ_MAG = 0x11
READ_MAG_RAW = 0x12
READ_MAG_H_OFF = 0x13
WRITE_MAG_H_OFF = 0x14
READ_MAG_S_OFF0 = 0x15
WRITE_MAG_S_OFF0 = 0x16
READ_MAG_S_OFF1 = 0x17
WRITE_MAG_S_OFF1 = 0x18
READ_MAG_S_OFF2 = 0x19
WRITE_MAG_S_OFF2 = 0x1A
SET_I2C_ADDR = 0x1B
GET_I2C_ADDR = 0x1C
SET_FILTER_GAIN = 0x1D
GET_FILTER_GAIN = 0x1E
SET_FRAME_ID = 0x1F
GET_FRAME_ID = 0x20
RESET_PARAMS = 0x21
READ_QUAT_RPY = 0x22
READ_ACC_GYRO = 0x23
CLEAR_DATA_BUFFER = 0x27
READ_IMU_DATA = 0x28
SET_ACC_LPF_CUT_FREQ = 0x29
GET_ACC_LPF_CUT_FREQ = 0x2A
READ_LIN_ACC_RAW = 0x2B
READ_LIN_ACC = 0x2C
#---------------------------------------------

class EIMUSerialClient:
    """Python client for EIMU serial communication."""

    def __init__(self):
        self.ser: serial.Serial | None = None

    def connect(self, port: str, baud: int = 115200, timeout: float = 0.1):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        sleep(3.0)

        for _ in range(10):
            success, id = self.getWorldFrameId()
            if success:
                print("EIMU Connected Successfully")
                return
            sleep(0.1)

        self.disconnect()
        raise RuntimeError("EIMU could not connect, Please check connection and Try Again")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.ser = None
    
    # ------------------ Packet Helpers ------------------

    def _flush_rx(self):
        """Flush any unread bytes in RX buffer"""
        if self.ser is None:
            return
        try:
            self.ser.reset_input_buffer()
        except serial.SerialException:
            pass


    def _flush_tx(self):
        """Flush TX buffer"""
        if self.ser is None:
            return
        try:
            self.ser.reset_output_buffer()
        except serial.SerialException:
            pass


    def _send_packet(self, cmd: int, payload: bytes = b""):
        if self.ser is None:
            raise RuntimeError("Serial port is not connected")
        self._flush_rx()
        length = len(payload)
        packet = bytearray([START_BYTE, cmd, length]) + payload
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)
        self.ser.flush()

    
    def _read_floats(self, count: int) -> Tuple[bool, tuple]:
        if self.ser is None:
            raise RuntimeError("Serial port is not connected")

        try:
            payload = self.ser.read(4 * count)

            if len(payload) != 4 * count:
                # partial frame → stream is now misaligned
                self._flush_rx()
                return False, tuple([0.0] * count)

        except (serial.SerialTimeoutException,
                serial.SerialException,
                Exception):
            # Any read-related failure → resync stream
            self._flush_rx()
            return False, tuple([0.0] * count)
        
        return True, struct.unpack("<" + "f" * count, payload)
    
    # ------------------ Generic Data ------------------

    def write_data1(self, cmd: int, val: float, pos: int = 0):
        payload = struct.pack("<Bf", pos, val)
        self._send_packet(cmd, payload)

    def read_data1(self, cmd: int, pos: int = 0) -> Tuple[bool, float]:
        payload = struct.pack("<Bf", pos, 0.0)
        self._send_packet(cmd, payload)
        success, (val,) = self._read_floats(1)
        return success, val

    def write_data3(self, cmd: int, a: float, b: float, c: float):
        payload = struct.pack("<fff", a, b, c)
        self._send_packet(cmd, payload)

    def read_data3(self, cmd: int) -> Tuple[bool, float, float, float]:
        self._send_packet(cmd)
        success, vals = self._read_floats(3)
        return success, *vals

    def read_data4(self, cmd: int) -> Tuple[bool, float, float, float, float]:
        self._send_packet(cmd)
        success, vals = self._read_floats(4)
        return success, *vals
    
    def read_data6(self, cmd: int) -> Tuple[bool, float, float, float, float, float, float]:
        self._send_packet(cmd)
        success, vals = self._read_floats(6)
        return success, *vals
    
    def read_data9(self, cmd: int) -> Tuple[bool, float, float, float, float, float, float, float, float, float]:
        self._send_packet(cmd)
        success, vals = self._read_floats(9)
        return success, *vals
    
    #---------------------------------------------------------------------
        
    def clearDataBuffer(self):
        success, _ = self.read_data1(CLEAR_DATA_BUFFER)
        return success
    
    def setWorldFrameId(self, frame_id: int):
        self.write_data1(SET_FRAME_ID, float(frame_id))
    
    def getWorldFrameId(self):
        success, frame_id = self.read_data1(GET_FRAME_ID)
        return success, int(frame_id)
    
    def getFilterGain(self):
        success, gain = self.read_data1(GET_FILTER_GAIN)
        return success, round(gain, 3)
    
    def readQuat(self):
        success, qw, qx, qy, qz = self.read_data4(READ_QUAT)
        return success, round(qw, 6), round(qx, 6), round(qy, 6), round(qz, 6)
    
    def readRPY(self):
        success, r, p, y = self.read_data3(READ_RPY)
        return success, round(r, 6), round(p, 6), round(y, 6)
    
    def readRPYVariance(self):
        success, r, p, y = self.read_data3(READ_RPY_VAR)
        return success, round(r, 6), round(p, 6), round(y, 6)
    
    def readAcc(self):
        success, ax, ay, az = self.read_data3(READ_ACC)
        return success, round(ax, 6), round(ay, 6), round(az, 6)
    
    def readAccVariance(self):
        success, ax, ay, az = self.read_data3(READ_ACC_VAR)
        return success, round(ax, 6), round(ay, 6), round(az, 6)
    
    def readGyro(self):
        success, gx, gy, gz = self.read_data3(READ_GYRO)
        return success, round(gx, 6), round(gy, 6), round(gz, 6)
    
    def readGyroVariance(self):
        success, gx, gy, gz = self.read_data3(READ_GYRO_VAR)
        return success, round(gx, 6), round(gy, 6), round(gz, 6)
    
    def readMag(self):
        success, mx, my, mz = self.read_data3(READ_MAG)
        return success, round(mx, 6), round(my, 6), round(mz, 6)
    
    def readAccGyro(self):
        success, ax, ay, az, gx, gy, gz = self.read_data6(READ_ACC_GYRO)
        return success, round(ax, 6), round(ay, 6), round(az, 6), round(gx, 6), round(gy, 6), round(gz, 6)
    
    def readImuData(self):
        success, r, p, y, ax, ay, az, gx, gy, gz = self.read_data9(READ_IMU_DATA)
        return success, round(r, 6), round(p, 6), round(y, 6), round(ax, 6), round(ay, 6), round(az, 6), round(gx, 6), round(gy, 6), round(gz, 6)

    def readLinearAccRaw(self):
        success, ax, ay, az = self.read_data3(READ_LIN_ACC_RAW)
        return success, round(ax, 6), round(ay, 6), round(az, 6)
    
    def readLinearAcc(self):
        success, ax, ay, az = self.read_data3(READ_LIN_ACC)
        return success, round(ax, 6), round(ay, 6), round(az, 6)
    #---------------------------------------------------------------------

    def setI2cAddress(self, i2cAddress: int):
        self.write_data1(SET_I2C_ADDR, float(i2cAddress))
    
    def getI2cAddress(self):
        success, i2cAddress = self.read_data1(GET_I2C_ADDR)
        return success, int(i2cAddress)

    def setFilterGain(self, gain: float):
        self.write_data1(SET_FILTER_GAIN, gain)
    
    def setAccFilterCF(self, cf: float):
        self.write_data1(SET_ACC_LPF_CUT_FREQ, cf)
    
    def getAccFilterCF(self):
        success, cf = self.read_data1(GET_ACC_LPF_CUT_FREQ)
        return success, round(cf, 3)
    
    def writeRPYVariance(self, r: float, p: float, y: float):
        self.write_data3(WRITE_RPY_VAR, r, p, y)
    
    def readAccRaw(self):
        success, ax, ay, az = self.read_data3(READ_ACC_RAW)
        return success, round(ax, 6), round(ay, 6), round(az, 6)
    
    def readAccOffset(self):
        success, ax, ay, az = self.read_data3(READ_ACC_OFF)
        return success, round(ax, 6), round(ay, 6), round(az, 6)
    
    def writeAccOffset(self, ax: float, ay: float, az: float):
        self.write_data3(WRITE_ACC_OFF, ax, ay, az)
    
    def writeAccVariance(self, ax: float, ay: float, az: float):
        self.write_data3(WRITE_ACC_VAR, ax, ay, az)
    
    def readGyroRaw(self):
        success, gx, gy, gz = self.read_data3(READ_GYRO_RAW)
        return success, round(gx, 6), round(gy, 6), round(gz, 6)
    
    def readGyroOffset(self):
        success, gx, gy, gz = self.read_data3(READ_GYRO_OFF)
        return success, round(gx, 6), round(gy, 6), round(gz, 6)
    
    def writeGyroOffset(self, gx: float, gy: float, gz: float):
        self.write_data3(WRITE_GYRO_OFF, gx, gy, gz)
    
    def writeGyroVariance(self, gx: float, gy: float, gz: float):
        self.write_data3(WRITE_GYRO_VAR, gx, gy, gz)
    
    def readMagRaw(self):
        success, mx, my, mz = self.read_data3(READ_MAG_RAW)
        return success, round(mx, 6), round(my, 6), round(mz, 6)
    
    def readMagHardOffset(self):
        success, mx, my, mz = self.read_data3(READ_MAG_H_OFF)
        return success, round(mx, 6), round(my, 6), round(mz, 6)
    
    def writeMagHardOffset(self, mx: float, my: float, mz: float):
        self.write_data3(WRITE_MAG_H_OFF, mx, my, mz)
    
    def readMagSoftOffset0(self):
        success, mx, my, mz = self.read_data3(READ_MAG_S_OFF0)
        return success, round(mx, 6), round(my, 6), round(mz, 6)
    
    def writeMagSoftOffset0(self, mx: float, my: float, mz: float):
        self.write_data3(WRITE_MAG_S_OFF0, mx, my, mz)
    
    def readMagSoftOffset1(self):
        success, mx, my, mz = self.read_data3(READ_MAG_S_OFF1)
        return success, round(mx, 6), round(my, 6), round(mz, 6)
    
    def writeMagSoftOffset1(self, mx: float, my: float, mz: float):
        self.write_data3(WRITE_MAG_S_OFF1, mx, my, mz)
    
    def readMagSoftOffset2(self):
        success, mx, my, mz = self.read_data3(READ_MAG_S_OFF2)
        return success, round(mx, 6), round(my, 6), round(mz, 6)
    
    def writeMagSoftOffset2(self, mx: float, my: float, mz: float):
        self.write_data3(WRITE_MAG_S_OFF2, mx, my, mz)

    def resetAllParams(self):
        success, _ = self.read_data1(RESET_PARAMS)
        return success
    
    #---------------------------------------------------------------------