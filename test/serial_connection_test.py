from connection.serial_connection import SerialConnection

ser = SerialConnection()

ser.send_at_command("hallo\n")
out = ser.ser.readline().decode("utf-8")
print(out)