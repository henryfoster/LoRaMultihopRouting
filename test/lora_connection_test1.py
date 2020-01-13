from config.ConfigReader import get_config
from connection.lora_connection import load_lora_config
from connection.serial_connection import SerialConnection

serial_conn = SerialConnection()
serr = serial_conn.ser
lora_config = get_config("../resources/LoRaConfig.json")
load_lora_config(lora_config, serr)