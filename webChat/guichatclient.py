import tkinter as tk
main = tk.Tk()
def keyPress(k):
    print(k.char, k.keycode)
    if k.keycode == 1:
        exit()
main.bind('<Key>', keyPress)
main.bind('<Escape>', exit)

def sendmsg():
    print(e.get())

e = tk.Entry(main)
e.insert(0, "defval")
#e.get()
e.focus_set()
b = tk.Button(main, text='Отправить...', width = 20, command=sendmsg)
l = tk.Label(main, text='chat...->', width = 100, height = 300)
b.pack()
e.pack()
l.pack()

main.mainloop()
