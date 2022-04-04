# LogiPy
A Logitech Illumination SDK Wrapper for python!

# Install
Download Logi.py, LogiLib.py and the DLL file that matches your python installation and put them in the same directory. That's all. (If unsure which DLL to use, you can just download both, the program will detect which one to use),

# Use
There are two ways to use this Wrapper. The first is straight from the Terminal. Simply open Windows Terminal up in the same folder as Logi.py, open up python and type `import logi`. Now, you can use any command from the Logitech Illumination SDK.

The other way is in another python script. To do this, either put that script in the same directory as LogiPy, or include this at the beginning of the py file:
```
import sys
sys.path.append('C:\Example\Logi\Path') #Make sure to replace this line with the directory that you put LogiPy in.
import Logi
```

# Syntax
The syntax is best shown with an example:

To call the function `LogiLedSetLighting(int redPercentage, int greenPercentage, int bluePercentage)`, all you need to do is run `logi.SetLighting(red,green,blue)`, where red, green, and blue are integers from 1-100 representating the percentage of each value in the colour.

To use commands with Key names, you need only write the key name as a string, for example `logi.SetLightingForKeyWithKeyName["F7",100,0,0]`.

To see the rest of the functions you can use, look at the Logitech Illumination SDK Docs, LogiPy supports all functions in the Logitech Illumination SDK.

# Custom Aliases
Some of the functions in the Logitech Illumination SDK have very long and cumbersome names. LogiPy let's you easily add custom Aliases. There is a sample Alias (LightSingleKey) already in the Logi.py file which should show you what to do.
