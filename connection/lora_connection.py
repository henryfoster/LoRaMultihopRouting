# Module for handling communication between LoRa modules
# Author: Eduard Andreev

from _thread import start_new_thread
from connection.serial_connection import *
from config.ConfigReader import get_config
from config.LogWriter import write_log
from models.Message import Message


liste = []
message_box = []
routing_table = {"0014": 1}


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


def receive():
    while 1:
        try:
            out = ser.readline().decode("utf-8")
            if out.startswith("LR"):
                handle_incomming_message(out)
            #debug-------------------------------------------------------------
            if not 'AT+SEND' in out:
                message = out.replace("\n", "").rstrip("\r")
                write_log(message, "../resources/receive.log")
        except UnicodeDecodeError:
            print("Error while decoding utf-8")


# loading config from ./resources/LoRaConfig.json as dict
config = get_config("../resources/LoRaConfig.json")

# sending the loraconfig via serial
load_lora_config(config)

# Setting own adress (from LoRaConfig.json : freq) and sending via serial
send_at_command(f"AT+ADDR={config['freq']}\r\n")

# Setting default Targetadress to FFFF (Broadcast)
send_at_command(f"AT+DEST=FFFF\r\n")

# setting Receiver mode RX
send_at_command("AT+RX\r\n")


# makes sure to add a leading zero if needed and casts int to string
def add_leading_zero(number):
    if number < 10:
        number = f"0{number}"
    return f"{number}"


# Protocol: sending a message (outgoing)
# Type: 00
def send_chat_message(destination, source, message):
    ttl = routing_table.get(destination)
    ttl = add_leading_zero(ttl)
    message_string = f"00{destination}{source}{ttl}00{message}"
    send_message(message_string)

# Protocol: forwarding message (reactive)
# Type: 00
def forward_chat_message(destination, source, ttl, seq, payload):
    message_string = f"00{destination}{source}{ttl-1}{seq+1}{payload}"
    send_message(message_string)


# Protocol: Self Propagation (outgoing)
# Type: 01
def self_propagation():
    message_string = f"01FFFF{config['freq']}0100"
    send_message(message_string)


# Protocol: Routing Table Propagation (outgoing)
# Type: 02
def routing_table_propagation():
    message_string = f"02FFFF{config['freq']}0100"
    for key in routing_table.keys():
        message_string += key
        message_string += str(routing_table[key])
    send_message(message_string)


# Protocol: Acknowledgement (outgoing)
# Type: 05
def send_acknowledgement(destination):
    ttl = routing_table.get(destination)
    ttl = add_leading_zero(ttl)
    message_string = f"05{destination}{config['freq']}{ttl}00"


def handle_incomming_message(message):                                                 #in einzelne funktionen auslagern
    message = message.replace(' ', '')
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    message = message[11:]
    flag = message[:2]
    dest = message[2:6]
    src = message[6:10]
    ttl = int(message[10:12])
    seq = int(message[12:14])
    payload = message[14:]
    #print(flag + " " + dest + " " + src + " " + str(ttl) + " " + str(seq) + " " + payload)
    if flag == '00':
        print("incomming chat message")
        temp_message = Message(dest, src, ttl, seq, payload)                            #ÜBERARBEITEN!!!!!!!!!!!!!!!!!!
        if len(message_box) == 0:
            message_box.append(temp_message)
        else:
            for m in message_box:
                if m == temp_message:
                    print("The same message was aready processed!")
                    print(m)
                else:
                    message_box.append(temp_message)

        #send_acknowledgement(dest)                                                      #TTL SEQ ??????? 2 mal was versuchen???
        if dest == config['freq']:
            print("juhu ich hab meine nachricht bekommen")
            print(message)
            return
        if dest in routing_table and routing_table[dest] > 1:
            print("forwarding message...")
            forward_chat_message(dest, src, ttl, seq, payload)                          #Wie soll das funktionieren????
    elif flag == '01':
        print("incomming self_propagation message")
        change = False
        if src not in routing_table:
            routing_table[src] = 1
            change = True
        if change:
            routing_table_propagation()
        print(routing_table)
    elif flag == '02':
        print('incomming routing_table_propagation')
        change = False
        for i in range(0,len(payload), 6):
            addr = payload[i:i+4]
            hop = payload[i+4:i+6]
            print(addr + " " + hop)
            if addr not in routing_table:
                routing_table[addr] = hop
                print(routing_table)
                change = True
        if change:
            routing_table_propagation()
    elif flag == '05':
        print('incomming acknowlagement message')
    else:
        print('wrong message')

# empfange Daten
receive()
#start_new_thread(receive, ())
# send_message("hello from lora connection")
