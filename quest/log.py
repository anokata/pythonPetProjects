
def send_to_main_log(messages, msg):
    for line in msg.split('\n'):
        if line.strip():
            messages.main_log.append(line)

def log_msg(msg, world):
    world.messages.log_msg = msg
