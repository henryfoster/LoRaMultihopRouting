# Script for writing a logfile
# Author: Eduard Andreev

import time


#"resources/receive.log"
def write_log(message, filename):
    f = open(filename, "a")
    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} : {message}\n")
    f.close()