from lxml import html
import os
def file_to_html(filename):
    if os.path.exists(filename):
        with open(filename, 'rt') as fin:
            content = fin.read()
            html_doc = html.fromstring(content)
    return html_doc

def get_all_tags(ht, tag):
    return ht.xpath('//%s'%tag)

f = file_to_html('/home/ksi/Downloads/html/Mother of Learning Chapter 58: Questions and Answers, a fantasy fiction | FictionPress.html')
t = get_all_tags(f, 'p')

