
def send_to_main_log(messages, msg):
    messages.main_log.append(msg)

def log_msg(msg, world):
    world.messages.log_msg = msg
