import requests

def load_file_from_file(fn):
    with open(fn) as fin:
        name = fin.read().strip()
    return name

def url_line_count(url):
    text = requests.get(url).text
    n = len(text.splitlines())
    print(n)

url_line_count(load_file_from_file('input'))

