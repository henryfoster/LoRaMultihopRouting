#Script zur Steuerung des programms
#Author: Eduard Andreev

from connection.lora_connection import *


def command_line():
    while 1:
        eingabe = input("[1] send message\n"
                        "[0] exit\n"
                        "Einagbe: ")
        if eingabe == "0":
            break
        elif eingabe == "1":
            message = input("message: ")
            send_message(message)


command_line()