#TODO lines separate
def wrap_string(line, max_len):
    wraped_line = ''
    words = line.split(' ')
    line_len = 0
    last = 0
    for i, w in enumerate(words):
        if line_len >= max_len:
            wraped_line += ' '.join(words[last:i]) + '\n' 
            last = i
            line_len = 0
        line_len += len(w) + 1
    wraped_line += ' '.join(words[last:]) + '\n' 

    return wraped_line
