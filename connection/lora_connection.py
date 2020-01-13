# Module for handling communication between LoRa modules
# Author: Eduard Andreev

from connection.serial_connection import *
from config.ConfigReader import get_config

# setting up LoRa Connection
def load_lora_config(lora_config, ser):
    ser.write(str.encode(f"AT+CFG="
                    f"{lora_config['carrierfrequency']},"
                    f"{lora_config['transmissionpower']},"
                    f"{lora_config['modulationbandwidth']},"
                    f"{lora_config['spread']},"
                    f"{lora_config['errorcorrection']},"
                    f"{lora_config['crc']},"
                    f"{lora_config['implicidheader']},"
                    f"{lora_config['onetimereception']},"
                    f"{lora_config['frequencymodulation']},"
                    f"{lora_config['frequencymodulationperiod']},"
                    f"{lora_config['receptiontimelimittime']},"
                    f"{lora_config['userdatalength']},"
                    f"{lora_config['preamblelength']}"
                    f"\r\n"))
    #print("waiting for at+ok")
    # sending the loraconfig via serial
    # load_lora_config(config)
    output = ser.readline().decode("utf-8")
    print("LoraConfig: " + output)

    # Setting own adress (from LoRaConfig.json : freq) and sending via serial
    ser.write(str.encode(f"AT+ADDR={lora_config['freq']}\r\n"))
    var = ser.readline().decode("utf-8")
    print(f"Setting Address to {lora_config['freq']}: " + var)

    # Setting default Targetadress to FFFF (Broadcast)
    ser.write(str.encode(f"AT+DEST=FFFF\r\n"))
    var = ser.readline().decode("utf-8")
    print("Default target = ffff: " + var)

    # setting Receiver mode RX
    ser.write(str.encode("AT+RX\r\n"))
    var = ser.readline().decode("utf-8")
    print("Setting RX: " + var)











