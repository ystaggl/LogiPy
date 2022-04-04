"""
Logipy: An up-to-date Logitech Illumination SDK Wrapper for python!
"""

import os
import ctypes
import LogiLib as Lib
import atexit
import struct
import time
DLLPath = os.getcwd() + f"\\LogitechLedEnginesWrapper{(8 * struct.calcsize('P'))}.dll" #Decides which DLL to use
Led = ctypes.WinDLL(DLLPath)
Led.LogiLedInit()
Led.LogiLedSetTargetDevice(ctypes.c_int(4)) #Sets device to keyboard

def LightSingleKey(*args):
    """
    Alias for LogiLedSetLightForKeyWithKeyName
    Syntax: 
        LightSingleKey("keyName",red,green,blue)
        where keyName is the name of the Key, and red, green, and blue are RGB values out of 100
    """

    runcommand = "Led.LogiLedSetLightingForKeyWithKeyName("
    parse_and_execute(runcommand, *args)
    return

#Add New Aliases Here


def __getattr__(command):
    """
    Main Function, Allows all LogiLed commands to be run directly from this module.
    """

    def method(*args):
        nonlocal command
        if not args:
            if command[-1] != ")":
                if "(" in command:
                    return "Error: Missing end bracket"
                command += "()"
            exec("Led.LogiLed" + command)
            return "Ran Command with no args"
        runcommand = "Led.LogiLed" + command + "("
        parse_and_execute(runcommand, *args)
    return method

def parse_and_execute(runcommand, *args):
    """
    This function parses and executes the command. Not intended to be called directly, only called by other functions.
    """

    for a in enumerate(args):
        if type(a) == type("A"):
            if " " in a:
                arg = a.split(" ")
                if hasattr(Lib, arg[0]):
                    arg[1] = "[\'" + arg[1] + "\']"
                    runcommand += "ctypes.c_int(" + f"Lib.{arg[0]}{arg[1]}" + "),"
                else:
                    print(f"Encountered string {arg[0]}, which isn't an attribute of LogiLib.py. This is probably a bug.")
                    return
            else:
                a = "[\'" + a + "\']"
                runcommand += "ctypes.c_int(" + f"Lib.KeyName{a}" + "),"
                print("String with no dictionary detected. Assuming dictionary KeyName.")
        if type(a) == type(1):
            runcommand += str(f"ctypes.c_int({a})") + ","
    runcommand = runcommand[:-1] + ")"
    try:
        exec(runcommand)
    except Exception:
        print(f"An Error has occured. The script attempted to run the command {runcommand}. Origin: parse_and_execute")
    return

def exit_handler():
    """
    Exit Function, shuts down Logitech Illumination SDK so that it doesn't interfere with other programs.
    """
    exec("Led.LogiLedSetLighting(0,66,100)") #Workaround for my \ lighting weirdly after closing the SDK.
    time.sleep(0.1)
    exec("Led.LogiLedShutdown()")

atexit.register(exit_handler)