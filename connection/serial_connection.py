# Module for dealing with Serial connection and serial data
# Author: Eduard Andreev
import time
import serial
from config.ConfigReader import get_config


class SerialConnection:
    def __init__(self):
        serial_config = get_config("../resources/SerialConfig.json")
        self.ser = serial.Serial(f"{serial_config['port']}",
                     serial_config['baudrate'],
                     serial_config['bytesize'],
                     serial_config['parity'],
                     serial_config['stopbits'],
                     serial_config['timeout']
                     );
        print(self.ser)


    # sends a command via the serial connection
    # main purpose are AT commands
    def send_at_command(self, command):
        self.ser.write(str.encode(command))
        time.sleep(0.1)


# Default Example:  self.ser = serial.Serial('COM5', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
