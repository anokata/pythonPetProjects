# выбираем узлы time from для текущего дня.
# из данных temperature value вычисляем среднее

import subprocess
exc = subprocess.getoutput
# получаем текущую дату - день.
day = int(exc('date +%d'))

import requests as req
url = 'http://www.yr.no/place/Russia/Yaroslavl/Rybinsk/forecast_hour_by_hour.xml'
# Берём данные xml.  weatherdata.forecast.tabular
req.get(url)
frc = req.xml()

