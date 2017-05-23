#!/usr/bin/python3
import csv
# sudo mkdir /run/fio/
# sudo chown user:group /run/fio
prefix = '/run/fio/'
data = dict()
fios = set()
intersect = 0
count = 0

# Write
def save():
    print('saving')
    with open('result.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['FirstName', 'Name', 'LastName', 'Email', 'Date', 'Sex', 'Phone', 'snils'])


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
            writer.writerow([v['f'], v['i'], v['o'], email, date, sex, phone, snils, ])
            #writer.writerow([v['f'], v['i'], v['o'], email, date, sex, phone, snils, name])

def add_data(fio, f, i, o, email='', phone='', sex='', date='', snils='', name=''):
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
            }


name = prefix + 'person-rpgu-20170517u.csv'
field_f = 0
field_i = 1
field_o = 2
field_phone = 4
field_email = 5
field_snils = 3
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
        add_data(fio, f, i, o, email, phone, snils=snils, name='rpgu')

print(name, 'ok')

name = prefix + 'person-dobrodel-20170517.csv'
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

name = prefix + 'person-zdrav-20170518.csv' # ok
field_f = 0
field_i = 1
field_o = 2
field_date = 3
field_sex = 4
field_phone = 7
field_email = 6
field_snils = 5
with open(name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
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

name = prefix + 'person-obr_20170517.csv'
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

