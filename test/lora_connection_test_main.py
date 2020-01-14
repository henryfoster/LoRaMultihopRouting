import time
from _thread import start_new_thread
from threading import Thread

import serial

serial_config = serial.Serial('COM6', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
print(serial_config)
def receive():
    for i in range(0,4):
        print("waiting for config")
        out = serial_config.readline().decode("utf-8")
        print(out)
        print("answering to config ...")
        serial_config.write(str.encode("AT+OK\r\n"))
    while True:
        out = serial_config.readline().decode("utf-8")
        if "AT," in out:
            print(f"Size = {out}")
            print("Answering with AT,OK to size of message ...")
            serial_config.write(str.encode("AT,OK\r\n"))
            out = serial_config.readline().decode("utf-8")
            print(f"Getting message: {out}")
            print(f"answering with AT,SENDING und AT,SENDED")
            serial_config.write(str.encode("AT,SENDING\r\n"))
            serial_config.write(str.encode("AT,SENDED\r\n"))
        elif "AT+DEST" in out:
            print(f"dest set to: {out}")
            serial_config.write(str.encode("AT,OK\r\n"))
        else:
            print(out)
            serial_config.write(str.encode("AT,OK\r\n"))
            out = serial_config.readline().decode("utf-8")
            message_type = ""
            if out.startswith("01"):
                message_type = "self propa: "
            elif out.startswith("02"):
                message_type = "routing table propa: "
            print(f"Getting message ({message_type}): {out}")
            print(f"answering with AT,SENDING und AT,SENDED")
            serial_config.write(str.encode("AT,SENDING\r\n"))
            serial_config.write(str.encode("AT,SENDED\r\n"))

receive_thread = Thread(target=receive)
receive_thread.start()


def command_line():
    while 1:
        eingabe = input("[1] send fake self Propagation\n"
                        "[2] send fake routing table Propagation\n"
                        "[3] send fake routing table Propagation hop-1\n"
                        "[4] send fake routing table Propagation longer route\n"
                        "[0] exit\n"
                        "Einagbe: ")
        if eingabe == "0":
            break
        elif eingabe == "1":
            serial_config.write(str.encode(f"LR,0016,12,01FFFF00160100\r\n"))
        elif eingabe == "2":
            serial_config.write(str.encode(f"LR,0016,12,02FFFF00160100001702\r\n"))
        elif eingabe == "3":
            serial_config.write(str.encode(f"LR,0016,12,02FFFF00160100001701\r\n"))
        elif eingabe == "4":
            serial_config.write(str.encode(f"LR,0016,12,02FFFF00160100001701001801\r\n"))

command_line()
