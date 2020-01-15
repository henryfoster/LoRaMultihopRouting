import time

import serial

ser = serial.Serial('COM5', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)


time.sleep(20)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)
out = ser.readline().decode("utf-8")
print(out)