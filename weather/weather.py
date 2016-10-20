import subprocess
import xml.etree.ElementTree as ET
import requests as req
exc = subprocess.getoutput

def getWeather():
    # получаем текущую дату - день.
    day = int(exc('date +%d'))
    url = 'http://www.yr.no/place/Russia/Yaroslavl/Rybinsk/forecast_hour_by_hour.xml'
    # Берём данные xml.  weatherdata.forecast.tabular .time
    try:
        res = req.get(url)
        frc = ET.fromstring(res.text)
        fore = frc.find('forecast').find('tabular').findall('time') 
    except:
        print("Что-то пошло не так")
        return (0,0,0)
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
    if periods == 0: return (0,0,0)
    avgTemp = avgTemp / periods
    wind /= periods
    return (avgTemp, perc, wind)

if __name__ == '__main__':
    print(getWeather())
