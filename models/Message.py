# Class for handling message entries
# Author: Eduard Andreev
import time


class Message:
    def __init__(self, dest, src, ttl, seq, payload):
        super(Message, self).__init__()
        self.dest = dest
        self.src = src
        self.ttl = ttl
        self.seq = seq
        self.payload = payload
        # self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')


    # dest
    def set_dest(self, dest):
        self.dest = dest

    def get_dest(self):
        return self.dest

    # src
    def set_src(self, src):
        self.src = src

    def get_src(self):
        return self.src

    # ttl
    def set_ttl(self, ttl):
        self.ttl = ttl

    def get_ttl(self):
        return self.ttl

    # seq
    def set_seq(self, seq):
        self.seq = seq

    def get_seq(self):
        return self.seq

    # payload
    def set_payload(self, payload):
        self.payload = payload

    def get_payload(self):
        return self.payload

    # #timestamp
    # def get_timestamp(self):
    #     return self.timestamp

    # def __eq__(self, other):
    #     return self.dest == other.dest and self.src == other.src and self.payload == other.payload

    def __str__(self):
        return self.dest + " " + self.src + " " + str(self.ttl) + " " + str(self.seq) + " " + self.payload

    def __repr__(self):
        return self.dest + " " + self.src + " " + str(self.ttl) + " " + str(self.seq) + " " + self.payload