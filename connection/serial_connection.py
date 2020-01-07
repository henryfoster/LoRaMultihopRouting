# Module for dealing with Serial connection and serial data
# Author: Eduard Andreev
import time
from serial import Serial
from config.ConfigReader import get_config


# setting up the serial connection
# loading config from ./resources/SerialConfig.json
def load_serial_config(file_name):
    serial_config = get_config(file_name)
    ser = Serial(f"{serial_config['port']}",
                 serial_config['baudrate'],
                 serial_config['bytesize'],
                 serial_config['parity'],
                 serial_config['stopbits'],
                 serial_config['timeout']
                 );
    return ser


# Init: serlial
ser = load_serial_config("resources/SerialConfig.json")


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




#send_message("Test Message");
