
def send_to_main_log(messages, msg):
    for line in msg.split('\n'):
        if line.strip():
            messages.main_log.append(line)

def log_msg(msg, world):
    world.messages.log_msg = msg

def set_main_log(messages):
    global main_log
    main_log = messages

def log_main(msg):
    send_to_main_log(main_log, msg)
