import csv
import pprint
from collections import OrderedDict 
#TODO Tests, Gui?

data = dict()
alldata = dict()
n = 0
intersect = 0
prefix = '/run/fio/' #input
resultpath = '/run/fio/result.csv' #input

def save(order, **kwargs):
    print('*** saving')
    with open(resultpath, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        titles = list()
        for name in order:
            titles.append(kwargs.get(name, ''))
        writer.writerow(titles)

        #name = kwargs.get(name, name)
        keylist = alldata.keys()
        keylist = sorted(keylist)

        for key in keylist:
            val = alldata[key]
            row = list()
            for name in order:
                value = val.get(name, '')
                row.append(value)
            writer.writerow(row)

def fio_extract(s):
    result = {}
    fio = s.strip().upper()
    fiolst = [s for s in fio.split() if s.strip() != '']
    if len(fiolst) == 0:
        return {'key':''} #EMAIL uniq
    if len(fiolst) == 1:
        result['i'] = fiolst[0].capitalize() 
        result['o'] = ''
        result['f'] = ''
        result['key'] = result['i']
    else:
        result['i'] = fiolst[0].capitalize() if len(fiolst) > 0 else ''
        result['f'] = fiolst[1].capitalize() if len(fiolst) > 1 else ''
        result['o'] = fiolst[2].capitalize() if len(fiolst) > 2 else ''
        result['fio'] = result['f'] + ' ' + result['i'] + ' ' + result['o']
        result['key'] = result['fio']
    return result

def id(x): return x;
def cap(x): return x.capitalize();

class Model:
    fields = None
    special = False

    # kwargs - description of fields = name:position
    # if __special is specified then it store pos and func
    #   for parse value to dict of fields
    def __init__(self, **kwargs):
        self.fields = OrderedDict()
        for name, position in kwargs.items():
            if name != '__special':
                self.fields[name] = position
            else:
                self.special = position # = (pos, func)

    def get_spec(self, row):
        if self.special:
            pos, fun = self.special
            return fun(row[pos])
        return {}

def check(d, name):
    print("===============")
    print('sample data of ' + name)
    for name, value in d.items():
        print(name + ' : ' + value)
    print("===============")

def make_key(row, pos):
    val = ''
    for i in pos:
        val += row[i].capitalize() + ' '
    return val.strip()


def add(row, model):
    global intersect, data, alldata
    drow = dict()
    for name, pos in model.fields.items():
        if name == 'key2':
            key2 = row[pos]
        if name == 'key':
            key = make_key(row, pos)
            drow[name] = key
        else:
            if type(pos) is tuple:
                pos, fun = pos
            else:
                fun = id
            drow[name] = fun(row[pos])

    for name, val in model.get_spec(row).items():
        drow[name] = val
        if name == 'key':
            key = val

    if key in data:
        #print(key, data[key].get('key2'), key2)
        if data[key].get('key2','') == key2:
            intersect += 1
            return
    alldata[key+key2] = drow
    data[key] = drow

def proc_file(name, model):
    print("*** process ", name)
    global data, n
    start = n
    first = True
    with open(name, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())
        header = csv.Sniffer().has_header(csvfile.readline())
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        if header:
            pass
        for row in reader:
            if first and header:
                first = False
                continue
            add(row, model)
            n += 1
    #middle = (n - start) // 4
    #check(list(data.values())[middle], name)
    print("*** ok")

def proc_files(files):
    for name, model in files.items():
        proc_file(prefix + name, model)

files = {
        'sample1.csv' : Model(
            email=1, 
            key2=1, 
            phone=2, 
            __special=(0, fio_extract)),

        'person_obr_20170529.csv' : Model(
            email=6, 
            key2=6, 
            snils=7, 
            date=4,
            sex=5,
            key=[1,2,3],
            f=(3, cap),
            i=(1, cap),
            o=(2, cap),),
        'person_zdrav_20170530.csv' : Model(
            email=6, 
            key2=5, 
            phone=5, 
            date=3,
            sex=4,
            key=[0,1,2],
            f=(0, cap),
            i=(1, cap),
            o=(2, cap),),
        }

#TODO read files, order and names from config
order = ['f', 'i','o', 'email', 'phone'] 
names = {
        'email':'Email', 
        'phone':"Phone",
        'f':"FirstName",
        'i':"MiddleName",
        }
proc_files(files)
#pprint.pprint(data)
#pprint.pprint(alldata)
print('uniq records without key2', len(data))
print('uniq records all', len(alldata))
print('intersected', intersect)
save(order, **names)
    
