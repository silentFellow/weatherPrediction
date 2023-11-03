import numpy as np
import requests
from time import sleep
import polars as pl

""" years = np.arange(2015, 2024)
months = np.arange(1, 13)
endDates = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]) """

years = np.array([2023])
months = np.arange(8, 11)
endDates = np.array([31, 30, 31])

try:
  df = pl.read_csv("rawData.csv")
except:
  df = pl.DataFrame({
    'cityName': [], 
    'temp': [], 
    'feelsLike': [], 
    'pressure': [], 
    'humidity': [], 
    'clouds': [], 
    'windSpeed': [], 
    'windDir': [], 
    'gustSpeed': [], 
    'result': []
  }, schema = {
    'cityName': str, 
    'temp': float, 
    'feelsLike': float, 
    'pressure': float, 
    'humidity': float, 
    'clouds': float, 
    'windSpeed': float, 
    'windDir': float, 
    'gustSpeed': float, 
    'result': str
  })

GEO_ENCODING_API_KEY = "69a1dcf5b06f61a63bbf2d30ee3651a1"
WEATHER_BIT_API_KEY = "30ce3b09c6a54e5abcc7fc107d23f767"

cities = np.array(['Erode', 'Coimbatore', 'Chennai', 'Tiruppur', 'Karur', 'Namakkal', 'Nilgiris', 'Thanjavur', 'Vellore', 'Dharmapuri'])

count = 0

for city in cities:
  res = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={GEO_ENCODING_API_KEY}")
  if res.status_code != 200:
    continue
  
  res = res.json()
  
  filteredRes = np.array(list(filter(lambda fromTN: fromTN['name'].lower() == city.lower() and fromTN['state'].lower() == 'tamil nadu', res)))
  if len(filteredRes) == 0:
    continue
  lat = filteredRes[0]['lat']
  lon = filteredRes[0]['lon']

  for year in years:
    for month, endDate in zip(months, endDates):
      response = requests.get(f"https://api.weatherbit.io/v2.0/history/hourly?lat={lat}&lon={lon}&start_date={year}-{month}-01&end_date={year}-{month}-{endDate}&key={WEATHER_BIT_API_KEY}")
      if response.status_code != 200:
        response = response.json()
        print(response)
        sleep(15)
        break
      response = response.json()
      for res in response['data']:
        info = pl.DataFrame({
        'cityName': city, 
        'temp': float(res['temp']), 
        'feelsLike': float(res['app_temp']), 
        'pressure': float(res['pres']), 
        'humidity': float(res['rh']), 
        'clouds': float(res['clouds']), 
        'windSpeed': float(res['wind_spd']), 
        'windDir': float(res['wind_dir']), 
        'gustSpeed': float(res['wind_gust_spd']), 
        'result': res['weather']['description']
      })

        df = pl.concat([df, info])

      count += 1
      print(f'completed {count}...')
      sleep(15)

df.write_csv("rawData.csv")