#Через adb ... tap сделать возможность печатать сообщения.
#Разрешение: H=854 W=480
import subprocess
cmd = 'adb shell input '
swipe_cmd = cmd + 'swipe '
unlock_cmd = cmd + 'keyevent 26'
tap_cmd = cmd + 'tap '

LINE_ONE_Y = 600
phone_keyboard = dict()
line1 = 'йцукенгшщзхъ'
keyboard_line1 = dict()
for i in range(12):
    keyboard_line1[line1[i]] = (i*40+30, LINE_ONE_Y)
print(keyboard_line1)

def tapChar(c):
    if c in line1:
        x, y = keyboard_line1[c]
        phone_tap(x, y)

def tapStr(s):
    for c in s:
        tapChar(c)

def viber_start():
    return _exec_cmd(' adb shell am start -a android.intent.action.Main -n com.viber.voip/.WelcomeActivity')

def _exec_cmd(cmd):
    return subprocess.getoutput(cmd)

def phone_tap(x, y):
    cmd = "{} {} {}".format(tap_cmd, x, y)
    print(cmd)
    return _exec_cmd(cmd)

def phone_swipe(sx, sy, ex, ey):
    cmd = "{} {} {} {} {}".format(swipe_cmd, sx, sy, ex, ey)
    print(cmd)
    return _exec_cmd(cmd)

def phone_unlock():
    #_exec_cmd(unlock_cmd)
    phone_swipe(0,0, 0,50)

#print(phone_unlock())
#phone_tap(0,0)
#viber_start()
tapStr("йцукенгшщзхъ")
