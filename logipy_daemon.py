"""
logipy_daemon, a daemon to control logitech keyboard lighting!
Example of sending commands:

from multiprocessing.connection import Client
address = ('localhost', 6001)
conn = Client(address, authkey=b'LogiLed')
conn.send("'SetLighting',(100,0,0)")
"""
import os
import ctypes
import logi_lib as lib
import atexit
import struct
import time
from multiprocessing.connection import Listener
import traceback
import configparser

logipydir = os.getcwd() #Make sure to set this!

#TODO: Still working on this
config = configparser.ConfigParser()

if os.path.exists('config.ini'):   #Detect whether config file exists, if so loads values from config
    config.read('config.ini')
    dll_path = config['SETTINGS']['DLLPath']
    port = int(config['SETTINGS']['Port'])
    print(port)

#Determine whether system is 32 or 64 bit, and set the dll_path accordingly
else:
    if 8 * struct.calcsize('P') == 64:
        dll_path = logipydir + "\\Led\\Lib\\LogitechLedEnginesWrapper\\x64\\LogitechLedEnginesWrapper.dll"
    else:
        dll_path = logipydir + "\\Led\\Lib\\LogitechLedEnginesWrapper\\x86\\LogitechLedEnginesWrapper.dll"
    
#Create config file with default values
    config['SETTINGS'] = {
        'DLLPath': dll_path,
        'Port': 6001,
        'PrimaryColor': '0,56,88'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

led = ctypes.WinDLL(dll_path)
led.LogiLedInit()
led.LogiLedSetTargetDevice(ctypes.c_int(4)) #Sets device to keyboard

#TODO: This is a specific fix for my computer. Edit this out before public release
led.LogiLedSetLighting(0,56,88)
time.sleep(1)
led.LogiLedShutdown()
time.sleep(1)
led.LogiLedInit()
led.LogiLedSaveCurrentLighting()


def parse_and_execute(run_command, *args):
    """
    This function parses and executes the command. Not intended to be called directly, only called by other functions.
    """
    if args == ():
        exec(f"{run_command})")
        print(f"Executed {run_command})")
        return
    for a in args:
        print(a)
        print(type(a))
        if type(a) == type("A"):
            if " " in a:
                arg = a.split(" ")
                print(arg)
                if hasattr(lib, arg[0]):
                    arg[1] = "[\'" + arg[1] + "\']"
                    run_command += "ctypes.c_int(" + f"lib.{arg[0]}{arg[1]}" + "),"
                    print(run_command)
                else:
                    print(f"Encountered string {arg[0]}, which isn't an attribute of logi_lib.py. This is probably a bug.")
                    return
            else:
                a = "[\'" + a + "\']"
                run_command += "ctypes.c_int(" + str(lib.KeyName[str(a).strip("'[]'")]) + "),"
                print("String with no dictionary detected. Assuming dictionary KeyName.")
            print(run_command)
        if type(a) == type(1):
            run_command += str(f"ctypes.c_int({a})") + ","
    run_command = run_command[:-1] + ")"
    try:
        exec(run_command)
    except Exception:
        print(f"An Error has occured. The script attempted to run the command {run_command}. Origin: parse_and_execute")
        return
    print(f"Command succesfully executed: {run_command}")


def exit_handler():
    """
    Exit Function, shuts down Logitech Illumination SDK so that it doesn't interfere with other programs.
    """
    exec("led.LogiLedSetLighting(0,66,100)") #Workaround for my \ lighting weirdly after closing the SDK.
    time.sleep(0.1)
    exec("led.LogiLedShutdown()")
    try:
        listener.close()
    except Exception:
        print("listener close except")
atexit.register(exit_handler)


if __name__ == "__main__":
    listen = False
    address = ('localhost', port)
    while True:
        try:
            listener = Listener(address, authkey=b'LogiLed')
            conn = listener.accept()
            print('connection accepted from', listener.last_accepted)
            listen = True
        except OSError:
            print(traceback.format_exc())
            print("Connection could not be made. Trying again in 10 seconds.")
            listener.close()
            time.sleep(10)    
        while listen == True:
            try:
                msg = conn.recv()
                if msg == 'close':
                    conn.close()
                    break
                msg = eval(msg)
                run_command = f"led.LogiLed{msg[0]}("
                args = msg[1]
                parse_and_execute(run_command,*args)
            except ConnectionResetError:
                time.sleep(1)
                listen = False
                listener.close()
            except EOFError:
                time.sleep(1)
                listen = False
                listener.close()
    listener.close()