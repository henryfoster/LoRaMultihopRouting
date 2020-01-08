# from serial import Serial
# from config.ConfigReader import get_config
#
# serial_config = get_config("../resources/SerialConfig.json")
#
# # setting up the serial connection on COM Port 6 for testing purpose
# ser = Serial("COM6",
#                 serial_config['baudrate'],
#                 serial_config['bytesize'],
#                 serial_config['parity'],
#                 serial_config['stopbits'],
#                 serial_config['timeout']
#                 );
#
# print("Recieving data.....")
# # listening for incomming serial data and printing them on the console
# # for testing purpose
# def receive():
#     while 1:
#         try:
#             out = ser.readline().decode("utf-8")
#             print(out.strip("\n"))
#
#         except UnicodeDecodeError:
#             print("Error while decoding utf-8")
#
# receive()