import os
pipe_name = '/home/ksi/pipe'
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)  
pipeout = os.open(pipe_name, os.O_WRONLY)
os.write(pipeout, b'Number')
