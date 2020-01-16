# route class
# Author: Eduard Andreev
import time


class Route:

    def __init__(self, adress, hop_count, next_hop):
        super(Route, self).__init__()
        self.adress = adress
        self.hop_count = hop_count
        self.next_hop = next_hop
        self.timestamp = time.time()

    def set_timestamp(self):
        self.timestamp = time.time()

    def get_time(self):
        return self.timestamp

    def __eq__(self, other):
        return self.adress == other.adress and self.hop_count == other.hop_count and self.next_hop == other.next_hop

    def __repr__(self):
        return f"{self.adress} | {self.hop_count} | {self.next_hop}"