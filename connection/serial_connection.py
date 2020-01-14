# Module for dealing with Serial connection and serial data
# Author: Eduard Andreev
import time
#from serial import Serial
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
        # self.ser = serial.Serial('COM5', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

    # sends a command via the serial connection
    # main purpose are AT commands
    def send_at_command(self, command):
        self.ser.write(str.encode(command))
        time.sleep(0.1)



    #     self.ser = self.load_serial_config(config_file_path) #"../resources/SerialConfig.json"
    #
    # # setting up the serial connection
    # # loading config from ./resources/SerialConfig.json
    # def load_serial_config(self, file_name):
    #
    #        ser = Serial(f"{serial_config['port']}",
    #                     serial_config['baudrate'],
    #                     serial_config['bytesize'],
    #                     serial_config['parity'],
    #                     serial_config['stopbits'],
    #                     serial_config['timeout']
    #                     );
    #     ser = serial.Serial('COM5', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
    #                         bytesize=serial.EIGHTBITS)
    #     return ser