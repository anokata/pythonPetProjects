#!/usr/bin/python3
#засекатель
import sys
import time
import subprocess
exc = subprocess.getoutput
arg = sys.argv

if len(arg) == 1 or not arg[1].isnumeric():
    print("Необходимо ввести агрумент - количество минут, и, возможно, сообщение.")
    exit()
minutes = int(sys.argv[1])
print("Я сообщу через: %d минут." % minutes)
time.sleep(minutes * 60)
msg = "Прошло %d минут!" % minutes
if len(arg) > 2:
    msg += '\n' + arg[2]
print(msg)
exc('zenity --info --text="' + msg + '"')
