import sys, tty, termios
def main():
    i = sys.stdin
    o = sys.stdout
    o.write('a\nb')
    o.write('.')
    #o.seek(1)
    o.write('.')

def rawmain():
    fdi = sys.stdin.fileno()
    fdo = sys.stdout.fileno()
    old_settingsI = termios.tcgetattr(fdi)
    old_settingsO = termios.tcgetattr(fdo)
    try:
        print('start')
        #tty.setraw(fdi)
        #tty.setraw(fdo)
        main()
    finally:
        termios.tcsetattr(fdi, termios.TCSADRAIN, old_settingsI)
        termios.tcsetattr(fdo, termios.TCSADRAIN, old_settingsO)
        print('end')

rawmain()
