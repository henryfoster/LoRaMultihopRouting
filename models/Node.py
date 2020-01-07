# Class for handling routingtable entries
# Author: Eduard Andreev


class Node:

    def set_addr(self, addr):
        self.addr = addr

    def getAddr(self):
        return self.addr

    def set_hops(self, hops):
        self.hops = hops

    def get_hops(self):
        return self.hops

    def set_sequence(self, sequence):
        self.sequence = sequence

    def get_sequence(self):
        return self.sequence

    def __str__(self):
        return str(self.addr) + " " + str(self.hops)

    def __repr__(self):
        return str(self.addr) + " " + str(self.hops)