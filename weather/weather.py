
import subprocess
exc = subprocess.getoutput
# получаем текущую дату - день.
day = int(exc('date +%d'))

import requests as req
url = 'http://www.yr.no/place/Russia/Yaroslavl/Rybinsk/forecast_hour_by_hour.xml'
# Берём данные xml.  weatherdata.forecast.tabular .time
res = req.get(url)
import xml.etree.ElementTree as ET
frc = ET.fromstring(res.text)
fore = frc.find('forecast').find('tabular').findall('time') 
avgTemp = 0
periods = 0
perc = 0
wind = 0
# выбираем узлы time from для текущего дня.
for x in fore:
    foreDay = int(x.get('from').split('-')[2].split('T')[0])
    if foreDay == day:
        temp = float(x.find('temperature').get('value'))
        avgTemp += temp
        periods += 1
        perc += float(x.find('precipitation').get('value'))
        wind += float(x.find('windSpeed').get('mps'))
# из данных temperature value вычисляем среднее
avgTemp = avgTemp / periods
print(avgTemp)
print(perc)
print(wind/periods)
