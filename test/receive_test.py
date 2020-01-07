# Script for testing the recieve functionality of the Programm
import time

from serial import Serial
from config.ConfigReader import get_config

serial_config = get_config("../resources/SerialConfig.json")

# setting up the serial connection on COM Port 6 for testing purpose
ser = Serial("COM6",
                serial_config['baudrate'],
                serial_config['bytesize'],
                serial_config['parity'],
                serial_config['stopbits'],
                serial_config['timeout']
                );

# sends a command via the serial connection
# main purpose are AT commands
def send_at_command(command):
    ser.write(str.encode(command))
    time.sleep(1)


# used to send 'String' messages via AT+SEND
def send_message(message):
    send_at_command("AT+SEND=" + str(len(message)) + "\r\n")
    time.sleep(1)
    send_at_command(str(message) + "\r\n")


print("Ready to send data....")

def command_line():
    while 1:
        eingabe = input("[1] send message\n"
                        "[0] exit\n"
                        "Einagbe: ")
        if eingabe == "0":
            break
        elif eingabe == "1":
            message = input("message: ")
            send_message(message)


command_line()
