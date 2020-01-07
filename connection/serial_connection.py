import time
from serial import Serial
from config.ConfigReader import get_config

serial_config = get_config("../resources/SerialConfig.json")

ser = Serial(f"{serial_config['port']}",
                serial_config['baudrate'],
                serial_config['bytesize']
                    );

def send_at_command(command):
    ser.write(str.encode(command))
    time.sleep(1)

def send_message(message):
    send_at_command("AT+SEND=" + str(len(message)) + "\r\n")
    time.sleep(1)
    send_at_command(str(message) + "\r\n")
    #print(message)

send_message("Test Message");