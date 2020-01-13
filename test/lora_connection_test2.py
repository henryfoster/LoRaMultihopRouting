import time
from _thread import start_new_thread

import serial

serial_config = serial.Serial('COM6', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
print(serial_config)
def receive():
    for i in range(0,4):
        print("Waiting for new line")
        out = serial_config.readline().decode("utf-8")
        print(out)
        print("Test task answering ...")
        serial_config.write(str.encode("AT+OK\r\n"))
    while True:
        print("Waiting for new line")
        out = serial_config.readline().decode("utf-8")
        print(out)
        print("Test task answering ...")
        serial_config.write(str.encode("AT,OK\r\n"))
        out = serial_config.readline().decode("utf-8")
        print(out)
        serial_config.write(str.encode("AT,SENDING\r\n"))

        serial_config.write(str.encode("AT,SENDED\r\n"))

receive()



