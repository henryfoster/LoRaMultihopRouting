# Module for handling communication between LoRa modules
# Author: Eduard Andreev

from connection.serial_connection import *
from config.ConfigReader import get_config


# setting up LoRa Connection
def load_lora_config(lora_config):
    send_at_command(f"AT+CFG="
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
                    f"\r\n")


# loading config from ./resources/LoRaConfig.json as dict
config = get_config("resources/LoRaConfig.json")

# sending the loraconfig via serial
load_lora_config(config)

# Setting own adress (from LoRaConfig.json : freq) and sending via serial
send_at_command(f"AT+ADDR={config['freq']}\r\n")

# Setting default Targetadress to FFFF (Broadcast)
send_at_command(f"AT+DEST=FFFF\r\n")

# setting Receiver mode RX
send_at_command("AT+RX\r\n")

# send_message("hello from lora connection")