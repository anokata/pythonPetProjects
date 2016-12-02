import sys
sys.path.append('../')
from mega import Mega
import yaml

urls = Mega()
urls.name = 'url root'

def add_dir(root, dir_name):
    dr = Mega()
    dr.name = dir_name
    root.add_attr(dir_name, dr)
    return dr

def del_dir(root, dir_name):
    pass

def add_url(root, name, val):
    setattr(root, name, val)

def get_yaml(root):
    return yaml.dump(root)

def get():
    return yaml.dump(urls)

def save():
    with open('url_data.yaml', 'wt') as fout:
        fout.write(get())

def load():
    global urls
    urls = yaml.load(open('url_data.yaml'))


if __name__=='__main__':
    load()
    #d = add_dir(urls, 'dir1')
    d = urls.dir1
    add_url(urls, 'py', 'py.org')
    add_url(d, 'u0', 'http://u.uk')
    print(urls)
    save()

