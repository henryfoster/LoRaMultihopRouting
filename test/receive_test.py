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
    time.sleep(0.1)


# used to send 'String' messages via AT+SEND
def send_message(message):
    send_at_command("AT+SEND=" + str(len(message)) + "\r\n")
    time.sleep(0.1)
    send_at_command(str(message) + "\r\n")


print("Ready to send data....")

def command_line():
    while 1:
        eingabe = input("[1] send hallo message\n"
                        "[2] send routingtable\n"
                        "[3] send chat message\n"
                        "[0] exit\n"
                        "Einagbe: ")
        if eingabe == "0":
            break
        elif eingabe == "1":
            send_message("LR,0505,13,01FFFF05050100Hello")
        elif eingabe == "2":
            send_message("LR,0505,13,02FFFF05050100444455666677")
        elif eingabe == "3":
            send_message("LR,0505,13,00001505050100Hallohallohallo")


command_line()
