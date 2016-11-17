#!/usr/bin/python3
#TODO: проверять первый запуск. записывать ежедневный файл, поставить в авто запуск и смотреть есть ли запись за сегодня и предлагать уже в зависимости.
import os
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

def pogoda():
    if (0,0,0) == weather.getWeather():
        print("Нет погоды")
        return
    temp, perc, wind = weather.getWeather()
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
if not test:
    print('Подождём сек...')
    exc('sleep 2')
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

print('Удачного %s!' % daypart)
