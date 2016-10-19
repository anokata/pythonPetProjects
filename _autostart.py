#!/usr/bin/python3
#TODO: проверять первый запуск. записывать ежедневный файл, поставить в авто запуск и смотреть есть ли запись за сегодня и предлагать уже в зависимости.
import os
import subprocess
import sys
sys.path.append('./weather')
import weather
exc = subprocess.getoutput

def pogoda():
    temp, perc, wind = weather.getWeather()
    print("Сегодняшняя средняя погда: T: %.1f  Осадки: %.1f  Ветер: %.1f м/c" % weather.getWeather())
    print("Запишу погоду на сегодня для статистики в ~/weather.cvs")
    dmy = exc('date +%d.%m.%Y')
    with open('/home/ksi/weather.cvs', 'at') as fout:
        fout.write(dmy + "|%.1f|%.1f|%.1f\n" % (temp, perc, wind))

name = subprocess.getoutput('whoami')
hour = int(exc('date +%H'))
if 0 < hour < 6:
    daypart = 'ночуемс'
elif 6 < hour < 12:
    daypart = 'утра'
elif 12 < hour < 18:
    daypart = 'дня'
elif 18 < hour < 23:
    daypart = 'вечера'
else:
    daypart = 'времени суток'
print("Доброго %s %s!"%(daypart, name))


yn = '[y/n]:'
r = input('Выполнить автозапуск? [y/n]')
if r[0] != 'y':
    print('Ну ладно...')
    exit()
print('Поехали!')

#TODO: сканирование всех разделов и монтирование в созданные каталоги
print('Подключаем интернет #1')
#exc('inet.sh')
exc('nmcli connection up atel')
#print('Монтируем раздел данных...')
#exc('datamount.sh')
#print('Подождём сек...')
#exc('sleep 2')
#print('Подождём сек...')
#exc('sleep 2')
#print('Подключаем интернет #2')
#exc('inet.sh')
pogoda()
print('Смотри какая сегодня погода! :)')
exc('weather.sh')
print('Запишем статистику')
statistic = '?.gnumeric'
exc('gnumeric')

#exc('pcmanfm&')
#r = input('Запустим браузер? [y/n]:')
#if r[0] == 'y':
#    exc('midori&')

#exc('qiv -z /usr/local/share/backgrounds/black-and-white-city-skyline-buildings.jpg') 

print('Удачного %s!' % daypart)
