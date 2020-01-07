import connection.commands

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