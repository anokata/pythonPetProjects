import threading

def p(x):
    for i in range(10):
        print(x)

t1 = threading.Thread(target=p, args=(0,))
t2 = threading.Thread(target=p, args=(1,))
t1.start()
t2.start()
t1.join()
t2.join()
