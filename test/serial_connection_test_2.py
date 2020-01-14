import time

import serial

ser = serial.Serial('COM10', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
print(ser)
while 1:
    out = ser.readline().decode("utf-8")
    print(out)
    time.sleep(0.3)
    out = ser.write(str.encode(out))
