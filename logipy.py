"""
Logipy import to control logipy_daemon easily

Example Usage:
logipy.run("'SetLighting',(100,0,0)")
"""

import configparser
import os
config = configparser.ConfigParser()
if os.path.exists('config.ini'):
    config.read('config.ini')
    port = int(config['SETTINGS']['Port'])
else:
    port = 6001

from multiprocessing.connection import Client
address = ('localhost', port)
conn = Client(address, authkey=b'LogiLed')
run = conn.send
def close():
    global conn
    conn.close()
    return

def connect():
    global conn
    conn = Client(address, authkey=b'LogiLed')
    return