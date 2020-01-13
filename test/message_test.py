from models.Message import Message

message1 = Message("0014", "0016", 1, 2, "hallo")
message3 = Message("0014", "0016", 1, 2, "hallo")
message2 = Message("0015", "0014", 1, 3, "hallo Welt")
message4 = Message("0015", "0014", 1, 3, "hallo Welt!")

print(message1)
print(message2)
print(message3)
print(message4)

print(message1 == message2)     #False
print(message1 == message3)     #True
print(message2 == message4)     #False