#Script zur Steuerung des programms
#Author: Eduard Andreev
import time
from _thread import start_new_thread
from threading import Lock, Thread
from config.ConfigReader import get_config
from connection.lora_connection import load_lora_config
from connection.serial_connection import SerialConnection
from models.Message import Message
from models.Route import Route

lock = Lock()

print("Main: laoding SerialConfig ...")
ser_con = SerialConnection() # "../resources/SerialConfig.json"
ser = ser_con.ser
print("Main: Serial connection established")
time.sleep(0.5)

print("Main: laoding LoRa Config ...")
# loading config from ./resources/LoRaConfig.json as dict
lora_config = get_config("../resources/LoRaConfig.json")
load_lora_config(lora_config, ser)
print("Main: LoRa Config fully loaded ...")
time.sleep(0.5)

buffer_list = []
liste = []
message_box = []
######example_route = Route("0014",1,"0014")
routing_table = {} # "0014" : example_route


def change_dest(addr):
    ser.write(str.encode(f"AT+DEST={addr}\r\n"))
    trys = 0
    while trys < 10:
        time.sleep(0.5)
        for i in buffer_list:
            if "AT,OK" in i:
                buffer_list.remove(i)
                print(f"change_dest to ({addr}): removing AT,OK from bufferlist")
                trys = 10
                break
        trys += 1

# used to send 'String' messages via AT+SEND
def send_message(message):
    lock.acquire()
    ser.write(str.encode("AT+SEND=" + str(len(message)) + "\r\n"))
    trys = 0
    while trys < 10:
        time.sleep(0.5)
        for i in buffer_list:
            if "AT,OK" in i:
                buffer_list.remove(i)
                print("send_message(): removing AT,OK from bufferlist")
                ser.write(str.encode(str(message) + "\r\n"))
                trys = 10
                break
        trys += 1
    trys = 0
    while trys < 10:
        time.sleep(0.5)
        for i in buffer_list:
            if "AT,SENDING" in i:
                print("send_message(): removing AT,SENDING from bufferlist")
                buffer_list.remove(i)
                trys = 10
                break
        trys +=1
    trys = 0
    while trys < 10:
        time.sleep(0.5)
        for i in buffer_list:
            if "AT,SENDED" in i:
                print("send_message(): removing AT,SENDED from bufferlist")
                buffer_list.remove(i)
                trys = 10
                break
        trys +=1
    lock.release()

def receive():
    while 1:
        try:
            out = ser.readline().decode("utf-8")
            # print("Recieved: " + out)
            buffer_list.append(out)
            # print("Recieved buffer: ")
            # print(buffer_list)

            #print("out: "+ out)
            #if "LR" in out:
            #    handle_incomming_message(out)
            #elif "AT" in out:
            #    print("KRRRRASS: " + out)
            #debug-------------------------------------------------------------
            #if not 'AT' in out:
            #    mmessage = out
            #    write_log(mmessage, "../resources/receive.log")
        except UnicodeDecodeError:
            print("Error while decoding utf-8")


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
    while True:
        time.sleep(100)
        message_string = f"01FFFF{lora_config['freq']}0100"
        send_message(message_string)


# Protocol: Routing Table Propagation (outgoing)
# Type: 02
def routing_table_propagation():
    message_string = f"02FFFF{lora_config['freq']}0100"
    for key in routing_table.keys():
        message_string += key
        message_string += str(routing_table[key])
    send_message(message_string)
    print("sending Routing table propagation: " + message_string)


# Protocol: Acknowledgement (outgoing)
# Type: 05
def send_acknowledgement(destination):
    ttl = routing_table.get(destination)
    ttl = add_leading_zero(ttl)
    message_string = f"05{destination}{lora_config['freq']}{ttl}00"


def check_buffer():
    while True:
        time.sleep(0.3)
        if len(buffer_list) > 0:
            output = buffer_list[0]
            print("Buffer[0] calling handle: " + output)
            handle_incomming_message(output)


def handle_incomming_message(message):                                                 #in einzelne funktionen auslagern
    if "LR" in message:
        print("handle detected LR message: " + message)
        buffer_list.pop(0)
        print("Buffer after LR pop: " )
        print(buffer_list)
        #message = message.replace(' ', '')
        message = message.replace('\r', '')
        message = message.replace('\n', '')
        # LR,0016,0E,01FFFF00160100
        real_src =  message[3:7]
        print("Real Adress: " + real_src)
        message = message[11:]
        flag = message[:2]
        dest = message[2:6]
        src = message[6:10]
        ttl = int(message[10:12])
        seq = int(message[12:14])
        payload = message[14:]
        print(flag + " " + dest + " " + src + " " + str(ttl) + " " + str(seq) + " " + payload)
        if flag == '00':
            print("incomming chat message")
            temp_message = Message(dest, src, ttl, seq, payload)                            #ÜBERARBEITEN!!!!!!!!!!!!!!!!!!
            message_box.append(temp_message)
            print(message_box)
            #temp_message = None
            #send_acknowledgement(dest)                                                      #TTL SEQ ??????? 2 mal was versuchen???
            # if dest == config['freq']:
            #     print("juhu ich hab meine nachricht bekommen: " + message)
            #     return
            # if dest in routing_table and routing_table[dest] > 1:
            #     print("forwarding message...")
            #     forward_chat_message(dest, src, ttl, seq, payload)                          #Wie soll das funktionieren????
        elif flag == '01':
            print("incomming self_propagation message")
            change = False
            if src not in routing_table:
                routing_table[src] = 1
                change = True
            if change:
                routing_table_propagation()
            print("printing routingtable :")
            print(routing_table)
        elif flag == '06':
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
    elif "AT," in message:
        #print("Handle: AT-message detected: " + message)
        #print("Buffer : ")
        #print(buffer_list)
        xyz = 1

    else:
        print("popping : " + message)
        print(buffer_list)
        buffer_list.pop(0)
        print("Buffer after wrong message pop: ")
        print(buffer_list)



# empfange Daten
# receive()
#start_new_thread(receive, ())
#start_new_thread(check_buffer, ())
#start_new_thread(self_propagation, ())

# New threading module
receive_thread = Thread(target=receive)
check_buffer_thread = Thread(target=check_buffer)
selfpropagation_thread = Thread(target=self_propagation)


receive_thread.start()
check_buffer_thread.start()
selfpropagation_thread.start()



def command_line():
    while 1:
        eingabe = input("[1] send message\n"
                        "[2] show Routing-Table\n"
                        "[3] show Buffer-List\n"
                        "[4] show Message Box"
                        "[0] exit\n"
                        "Einagbe: ")
        if eingabe == "0":
            break
        elif eingabe == "1":
            addr = input("adresse: ")
            change_dest(addr)
            message = input("message: ")
            send_message(message)
            change_dest("ffff")
        elif eingabe == "2":
            print(routing_table)
        elif eingabe == "3":
            print(buffer_list)
        elif eingabe == "4":
            print(message_box)

command_line()

