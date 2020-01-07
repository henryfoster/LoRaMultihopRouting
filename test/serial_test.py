from serial import Serial
from config.ConfigReader import get_config

serial_config = get_config("../resources/SerialConfig.json")

ser = Serial("COM6",
                serial_config['baudrate'],
                serial_config['bytesize']
                    );
print("Recieving data.....")
def receive():
    while 1:
        try:
            out = ser.readline().decode("utf-8")
            print(out.strip("\n"))

        except UnicodeDecodeError:
            print("Error while decoding utf-8")

receive()