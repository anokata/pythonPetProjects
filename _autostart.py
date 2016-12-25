#!/usr/bin/python3
#TODO: проверять первый запуск. записывать ежедневный файл, поставить в авто запуск и смотреть есть ли запись за сегодня и предлагать уже в зависимости.
import os
import time
import subprocess
exc = subprocess.getoutput
import sys
work_dir = sys.path[0]
lib_dir = os.path.join(work_dir, './lib')
sys.path.append('./weather')
sys.path.append(lib_dir)
import currency
import weather
test = len(sys.argv) > 1
#TODO if atel is off - turn. If time of statistic is not nowday then open, and weather simily

def atel_status():
    status = exc('nmcli connection show atel | grep GENERAL.STATE | cut -d: -f2 | tr -d [:blank:]')
    return status == 'activated'

def inet_on():
    if not atel_status():
        print('Подключаем интернет #1')
        #exc('inet.sh')
        exc('nmcli connection up atel')

def is_new(filename):
    now_day = time.localtime().tm_mday
    file_day = time.localtime(os.path.getmtime('.')).tm_mday
    return file_day == nowday

def show_weather():
    if not is_new('avansert_meteogram.png'):
        pogoda()
    #TODO

def pogoda():
    if (0,0,0) == weather.getWeather(weather.place):
        print("Нет погоды")
        return
    temp, perc, wind = weather.getWeather(weather.place)
    print("Сегодняшняя средняя погда: T: %.1f  Осадки: %.1f  Ветер: %.1f м/c" % (temp, perc, wind))
    print("Запишу погоду на сегодня для статистики в ~/weather.cvs")
    dmy = exc('date +%d.%m.%Y')
    with open('/home/ksi/weather.cvs', 'at') as fout:
        fout.write(dmy + "|%.1f|%.1f|%.1f\n" % (temp, perc, wind))

def greating():
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
    return daypart

daypart = greating()

def qry():
    yn = '[y/n]:'
    r = input('Выполнить автозапуск? [y/n]')
    if r[0] != 'y':
        print('Ну ладно...')
        exit()
    print('Поехали!')

#TODO: сканирование всех разделов и монтирование в созданные каталоги
#print('Монтируем раздел данных...')
#exc('datamount.sh')
inet_on()
if not test:
    print('Подождём сек...')
    exc('sleep 1')
    pogoda()
    print('Текущий курс доллара: {}'.format(currency.getUSD_RUB()))
    print('Смотри какая сегодня погода! :)')
    exc('weather.sh')
    print('Запишем статистику')
    statistic = '?.gnumeric'
    exc('gnumeric')


#print('Установим обои')
#exc('wallpaperText.py --file "/home/ksi/txthub/doings.txt" \
    #--bg "/home/ksi/Downloads/bg1.png" --fontsize 17 \
    #--fontcolor "(10,100,0)"')
#exc('qiv -z /usr/local/share/backgrounds/black-and-white-city-skyline-buildings.jpg') 

exc('pday.py start')

print('Удачного %s! vim txthub/live.org' % daypart)
