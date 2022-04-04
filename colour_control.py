"""
Colour Control interface for autohotkey/CLI:
Syntax: python colour_control.py "Function" args
Automatically assigns types based on if they can be converted to ints. If you need an argument that can be converted to int to be interpreted as a string,
append "str" to it, for example "str1"
"""

import sys
sys.path.append('C:\Workspace\Python\LogiPy')
argv = sys.argv
import logi
run_command = "logi." + argv[1] + "("
for a in argv[2:]:
    if a[0:3] == 'str':
        a = str(a[3:])
    else:
        try:
            a = int(a)
        except ValueError:
            pass

    if type(a) == type("a"):
        run_command += f"'{a}',"
    else: run_command += str(a) + ","
run_command = run_command[:-1] + ")"
exec(run_command)
