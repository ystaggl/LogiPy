# LogiPy
An up-to-date Logitech Illumination SDK Wrapper for python!

# Requirements
Logitech G Hub
[Logitech Illumination SDK](https://www.logitechg.com/en-us/innovation/developer-lab.html)


# Install
Download logi.py and logi_lib.py from this repo

Place the LED folder from the Logitech Illumination SDK into the same folder as logi.py and logi_lib.py

# Use
There are two ways to use this Wrapper. The first is straight from the Terminal. Simply open Windows Terminal up in the same folder as logi.py, open up python and type `import logi`. Now, you can use any command from the Logitech Illumination SDK.

The other way is to run it from a different location using the colour_control.py script. Set the location of LogiPy in colour_control.py, and then execute commands with the following syntax:

`python colour_control.py Function arguments`

For example:
`python colour_control.py LightSingleKey F7 100 0 0`

Note that because of limitations of argv, by default any arguments that can be converted to int, will be. For example "1" will be converted to 1. To force the argument
to be processed as a string. prepend "str" to the argument. For example, "1" would become "str1".

# Syntax
The syntax is best shown with an example:

To call the function `LogiLedSetLighting(int redPercentage, int greenPercentage, int bluePercentage)`, all you need to do is run `logi.SetLighting(red,green,blue)`, where red, green, and blue are integers from 1-100 representating the percentage of each value in the colour.

To use commands with Key names, you need only write the key name as a string, for example `logi.SetLightingForKeyWithKeyName["F7",100,0,0]`.

To see the rest of the functions you can use, look at the Logitech Illumination SDK Docs, LogiPy supports all functions in the Logitech Illumination SDK.

# Custom Aliases
Some of the functions in the Logitech Illumination SDK have very long and cumbersome names. LogiPy let's you easily add custom Aliases. There is a sample Alias (LightSingleKey) already in the logi.py file which should show you what to do.
