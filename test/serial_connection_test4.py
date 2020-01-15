import serial

from connection.serial_connection import SerialConnection

ser = serial.Serial('COM6', timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)



ser.write(str.encode("troll1\r\n"))
ser.write(str.encode("troll2\r\n"))
ser.write(str.encode("troll3\r\n"))
ser.write(str.encode("troll4\r\n"))
ser.write(str.encode("troll1\r\n"))
ser.write(str.encode("troll2\r\n"))
ser.write(str.encode("troll3\r\n"))
ser.write(str.encode("troll4\r\n"))