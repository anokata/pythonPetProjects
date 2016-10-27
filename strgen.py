import random
nouns = ["дождь",'снег','солнце','туча','облоко','земля','небо','дерево','дорога','звук','свет','ветер',]
pril = ['красивый', 'вечерний', 'лазурный', 'морской', 'тёплый', 'нежный', 'суровый', 'сильный' ]
timed = "Сегодня Завтра Тогда Всегда Иногда".split()
nar = "медленно быстро спокойно яростно небрежно аккуратно".split()
verbs = "идёт ползёт летит бежит стучит поёт сидит грузит течёт".split()
def genstr0(end='.'):
    s = ''
    s += random.choice(timed) + ' '
    s += random.choice(pril) + ' '
    s += random.choice(nouns) + ' '
    if random.randint(0,1) == 1:
        s += random.choice(nar) + ' '
    s += random.choice(verbs) + end
    return s
random.seed()

def genpoem(n=4):
    s = ''
    for i in range(n):
        s += genstr0(',\n')
    s += genstr0('.')
    return s

print(genpoem())
