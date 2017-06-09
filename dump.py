#!/usr/bin/python3
#TODO frequency analyze for delimeters
#TODO format of fields
import csv
# if not exist(dest_path):
# sudo mkdir /run/fio/
# sudo chown user:group /run/fio
data = dict()
intersect = 0
count = 0
prefix = '/run/fio/'
#prefix = '/home/ksi/Downloads/fio/2017/'
resultpath = '/run/fio/result_201705.csv'
#rpgu = 'person-rpgu-20170517u.csv'
#dobro = 'person-dobrodel-20170517.csv'
#zdrav = 'person-zdrav-20170518.csv' 
#obr = 'person-obr_20170517.csv'

rpgu = 'person_rpgu_20160101.csv'
dobro = 'person_dobrodel_20160101.csv'
zdrav = 'person_zdrav_20160101.csv' 
obr = 'person_obr_20160101.csv'

rpgu = 'userstill20170526.csv'
dobro = 'person_dobrodel_20170530.csv'
zdrav = 'person_zdrav_20170530.csv' 
obr = 'person_obr_20170529.csv'

# Write
def save():
    print('saving')
    with open(resultpath, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['FirstName', 'Name', 'LastName', 'Email', 'Date', 'Sex', 'Phone', 'snils', 'Inn'])


        keylist = data.keys()
        keylist = sorted(keylist)
        #for k, v in data.items():
        for key in keylist:
            v = data[key]
            phone = v.get('phone', '')
            email = v.get('email', '')
            sex = v.get('sex', '')
            date = v.get('date', '')
            snils = v.get('snils', '')
            name = v.get('name', '')
            fio = v.get('fio', '')
            inn = v.get('inn', '')
            writer.writerow([v['f'], v['i'], v['o'], email, date, sex, phone, snils, inn])
            #writer.writerow([v['f'], v['i'], v['o'], email, date, sex, phone, snils, name])

def add_data(fio, f, i, o, email='', phone='', sex='', date='', snils='', name='', inn=''):
    global intersect, data, count
    count += 1
    if fio in data:
        if data[fio].get('email','') == email:
            intersect += 1
            return
    data[fio] = {'fio': fio,
            'email': email,
            'phone': phone,
            'f': f,
            'i': i,
            'o': o,
            'name': name,
            'snils':snils,
            'sex':sex,
            'date':date,
            'inn':inn,
            }

def proc_file(desc):
    name = prefix + desc['name']
    field_f = desc['f']
    field_i = desc['i']
    field_o = desc['o']
    field_fio = desc['fio']
    field_phone = desc['phone']
    field_email = desc['email']
    field_snils = desc['snils']
    delimiter = desc['delimiter']
    quotechar = desc['quotechar']
    with open(name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            if field_fio:
                pass #TODO
            else:
                fio = (row[field_f] + ' ' + row[field_i] + ' ' + row[field_o]).strip().upper()
            f = row[field_f].capitalize()
            i = row[field_i].capitalize()
            o = row[field_o].capitalize()
            email = row[field_email]
            phone = row[field_phone]
            snils = row[field_snils]
            add_data(fio, f, i, o, email, phone, snils=snils, name=name)
    print(name, 'ok')

name = prefix + rpgu
field_f = 1
field_i = 2
field_o = 3
field_phone = 6
field_email = 7
field_snils = 5
field_inn = 4
field_date = 0
with open(name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        fio = (row[field_f] + ' ' + row[field_i] + ' ' + row[field_o]).strip().upper()
        f = row[field_f].capitalize()
        i = row[field_i].capitalize()
        o = row[field_o].capitalize()
        email = row[field_email]
        phone = row[field_phone]
        snils = row[field_snils]
        date = row[field_date]
        inn = row[field_inn]
        add_data(fio, f, i, o, email, phone, snils=snils, name='rpgu', date=date, inn=inn)

print(name, 'ok')

name = prefix + dobro
field_fio = 0
field_phone = 2
field_email = 1
with open(name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        fio = (row[field_fio]).strip().upper()
        if fio == 'ФИО':
            continue
        email = row[field_email]
        phone = row[field_phone]
        fiolst = [s for s in fio.split() if s.strip() != '']
        if len(fiolst) == 0:
            continue
        if len(fiolst) == 1:
            i = fiolst[0].capitalize() 
            o = ''
            f = ''
        else:
            i = fiolst[0].capitalize() if len(fiolst) > 0 else ''
            f = fiolst[1].capitalize() if len(fiolst) > 1 else ''
            o = fiolst[2].capitalize() if len(fiolst) > 2 else ''
            fio = f + ' ' + i + ' ' + o
        add_data(fio, f, i, o, email, phone, name='dobro')

print(name, 'ok')

name = prefix + zdrav
field_f = 0
field_i = 1
field_o = 2
field_date = 3
field_sex = 4
field_phone = 7
field_email = 6
field_snils = 5
with open(name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        fio = (row[field_f] + ' ' + row[field_i] + ' ' + row[field_o]).strip()
        email = row[field_email]
        phone = row[field_phone]
        snils = row[field_snils]
        sex = "Ж" if row[field_sex] == '0' else "М"
        date = row[field_date]
        f = row[field_f].capitalize()
        i = row[field_i].capitalize()
        o = row[field_o].capitalize()
        add_data(fio, f, i, o, email, phone, snils=snils, sex=sex, date=date, name='zdrav')

print(name, 'ok')

name = prefix + obr
field_i = 'UserNameFirst'
field_o = 'UserNameMiddle'
field_f = 'UserNameLast'
field_date = 'BirthDate'
field_sex = 'Sex'
field_phone = 'Phone'
field_email = 'Email'
field_snils = 'snilsNumber'
field_role = 'Role'
with open(name, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
    for row in reader:
        fio = (row[field_f] + ' ' + row[field_i] + ' ' + row[field_o]).strip().upper()
        email = row[field_email]
        phone = row[field_phone]
        snils = row[field_snils]
        sex = row[field_sex]
        date = row[field_date]
        #role = row[field_role]
        f = row[field_f].capitalize()
        i = row[field_i].capitalize()
        o = row[field_o].capitalize()
        add_data(fio, f, i, o, email, phone, snils=snils, sex=sex, date=date, name='obr')

print(name, 'ok')
print('all records', count)
print('uniq records', len(data))
print('intersected', intersect)
save()

