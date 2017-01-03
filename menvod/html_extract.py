from lxml import html
import glob
import os
import re
def file_to_html(filename):
    if os.path.exists(filename):
        with open(filename, 'rt') as fin:
            content = fin.read()
            html_doc = html.fromstring(content)
    return html_doc

def get_all_tags(ht, tag):
    return ht.xpath('//%s'%tag)

def extract_text(elements):
    text = list()
    for e in elements:
        text.append(e.text_content())
        text.append('\n')
    return ''.join(text)

def save_text(filename, text):
    with open(filename, 'wt') as fout:
        fout.write(text)

def get_star_files(path):
    return glob.glob(path + '*', recursive=True)

def extract_new_name(path, extension=None):
    if extension == None:
        extension = re.search('\.[a-zA-Z]*', path).group()
    numbers = re.search('\d+', path).group()
    part1 = ''.join(re.findall('/[a-zA-Z]', path)).replace('/', '')
    real_name = os.path.split(path)[1]
    name = re.sub('[:|\s\.\,]', '', real_name)[::4]
    pth = os.path.split(path)[0] + os.path.sep
    end_name = pth + name + part1 + numbers + extension
    if os.path.exists(end_name):
        return None
    return end_name

def html_p_texts(pattern):
    files = get_star_files(path)
    for fn in files:
        htm = file_to_html(fn)
        tags = get_all_tags(htm, 'p')
        text = extract_text(tags)
        name = extract_new_name(fn, '.txt')
        if name != None:
            save_text(name, text)
        else:
            print('sorry')
        pass



#if __name__=='__main__':

path = '/home/ksi/Downloads/html/Mother of Learning Chapter'
f = file_to_html('/home/ksi/Downloads/html/Mother of Learning Chapter 58: Questions and Answers, a fantasy fiction | FictionPress.html')
t = get_all_tags(f, 'p')
x = extract_text(t)
#save_text('/home/ksi/Downloads/mol58.txt', x)
html_p_texts(path)
