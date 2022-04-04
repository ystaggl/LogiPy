"""
Logipy: An up-to-date Logitech Illumination SDK Wrapper for python!
"""

import os
import ctypes
import logi_lib as lib
import atexit
import struct
import time
if 8 * struct.calcsize('P') == 64:
    dll_path = os.getcwd() + "\\Led\\Lib\\LogitechLedEnginesWrapper\\x64\\LogitechLedEnginesWrapper.dll"
else:
    dll_path = os.getcwd() + "\\Led\\Lib\\LogitechLedEnginesWrapper\\x86\\LogitechLedEnginesWrapper.dll"
led = ctypes.WinDLL(dll_path)
led.LogiLedInit()
led.LogiLedSetTargetDevice(ctypes.c_int(4)) #Sets device to keyboard

#Sample Alias

def LightSingleKey(*args): #Name the Alias
    """
    Alias for LogiLedSetLightForKeyWithKeyName
    Syntax: 
        LightSingleKey("keyName",red,green,blue)
        where keyName is the name of the Key, and red, green, and blue are RGB values out of 100
    """

    run_command = "LogiLedSetLightingForKeyWithKeyName" #Define run_command as the function as given by the SDK documentation
    parse_and_execute(run_command, *args)
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
            exec("led.LogiLed" + command)
            return "Ran Command with no args"
        run_command = "led.LogiLed" + command + "("
        parse_and_execute(run_command, *args)
    return method

def parse_and_execute(run_command, *args):
    """
    This function parses and executes the command. Not intended to be called directly, only called by other functions.
    """
    #For Custom Aliases
    if run_command[-1] != "(":
        run_command = "led." + run_command + "("

    for a in args:
        print(a)
        print(type(a))
        if type(a) == type("A"):
            print("Reached Line 65")
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

atexit.register(exit_handler)
