import vk_api
from datetime import datetime

#birth_month
#religion interests about
#fields last_seen movies music online
#personal - 
    # people_main 1 2 !3 !4 5 ?6
    # life_main !1 !2 !3 4 5 6 !7 !8
    # smoking 1 2 not 3 4 5
    # alcohol 1 2 not 3 4 5
# relation 0 1 6 not 2-5 7 8
#city=121 rybinsk
#country=1
#sex=1
#status not 2 3 4 5 7 8
#sex 1=W 2=M
# groups - not Порно секс мамы маме Дискотека 
password = open('/home/ksi/password').read().strip()
vk_session = vk_api.VkApi('ksilenomen@gmail.com', password)
vk_session.auth()
vk = vk_session.get_api()

age = 25
current_year = 2019

def vk_get_users(age, sex=1):
    city=121 # rybinsk
    users = []
    a = 0
    for birth_month in range(1, 13):
        r = vk.users.search(count=1000, sex=sex, birth_month=birth_month, age_from=age, age_to=age, fields='about, books, interests, personal, relation, last_seen')
        #r = vk.users.search(count=1000, city=city, sex=sex, birth_month=birth_month, age_from=age, age_to=age, fields='about, books, interests, personal, relation, last_seen')
        print('count: ', r['count'])
        a += r['count']
        users.extend(r['items'])
    print('a count: ', a)
    return vk_filter_(users)

def vk_filter_(users):
    filtred = list()
    for user in users:
        if not user.get('personal', False):
            continue
        if not user.get('relation', False):
            continue
        # Только свободные
        if not user['relation'] in [0, 1]: #6 - в активном
            continue
        if not user['personal'].get('smoking', 1) in [1, 2]:
            continue
        if not user['personal'].get('alcohol', 1) in [1, 2]:
            continue
        if not user['personal'].get('people_main', 0) in [1, 2, 5, 6]:
            continue
        if not user['personal'].get('life_main', 0) in [4, 5, 6]:
            continue

        ts = int(user.get('last_seen').get('time'))
        tm = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        year = int(datetime.utcfromtimestamp(ts).strftime('%Y'))
        if year != current_year:
            continue

        filtred.append(user)
    return filtred

def vk_users_agefromto(f, t):
    users = list()
    for age in range(f, t+1):
        users.extend(vk_get_users(age))
    return users

def vk_print_user(user, full=False):
    print('http://vk.com/id{}  {} {}'.format(
        user['id'],
        user['first_name'],
        user['last_name'],
        ))
    if full:
        print("     {}    {}    {} ".format(
            user.get('interests'),
            user.get('books'),
            user.get('about'),
            ))

users = vk_users_agefromto(27, 29)
print('all: ', len(users))
#users = vk_filter_(users)
print(len(users))
for u in users:
    vk_print_user(u)
vk_print_user(users[0], True)
