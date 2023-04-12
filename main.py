from datetime import date, datetime
import time
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
#start_date = '2019-08-14'
start_date = '2022-10-31'
ending_date = '2023-07-01'
city0 = 'wuhan'
birthday1 = '10-13'
birthday2 = '11-18'

app_id = "wxa6908ef5cf77e676"
app_secret = "df5408b2d176032e45e98b73934883af"

user_id = ["okCU26Gxs7OSjbr9N12KwLmf2heg", "okCU26CyZAlox-Mrm9fQsmPhRa5I"]
template_id = "vbcMSv7sxlr2GrEuI9rQe-AHzlySGP6FoS7NaKho4F8"

weather_key = "08eb4100a73f4d2ab967c0bd5baed51e"


def get_weather():
  url_location = "https://geoapi.qweather.com/v2/city/lookup?location="+city0+"&key="+weather_key
  location_req = requests.get(url_location).json()["location"][8]
  location_id = str(location_req["id"])
  region = location_req["name"]
  city = location_req["adm2"]
  prov = location_req["adm1"]
  url_weather_now = "https://devapi.qweather.com/v7/weather/now?location="+location_id+"&key="+weather_key
  url_weather_daily = "https://devapi.qweather.com/v7/weather/3d?location="+location_id+"&key="+weather_key
  url_air_daily = "https://devapi.qweather.com/v7/air/5d?location="+location_id+"&key="+weather_key
  now_req = requests.get(url_weather_now).json()["now"]
  daily_req = requests.get(url_weather_daily).json()["daily"][0]
  air_req = requests.get(url_air_daily).json()["daily"][0]
  temp_now = now_req["temp"]
  text_now = now_req["text"]
  date = daily_req["fxDate"]
  temp_min = daily_req["tempMin"]
  temp_max = daily_req["tempMax"]
  day_wea = daily_req["textDay"]
  night_wea = daily_req["textNight"]
  sunrise = daily_req["sunrise"]
  sunset = daily_req["sunset"]
  moonrise = daily_req["moonrise"]
  moonset = daily_req["moonset"]
  air_qual = air_req["category"]
  return region, city, prov, date, text_now, temp_now, temp_min, \
          temp_max, day_wea, night_wea, sunrise, sunset, moonrise, \
          moonset, air_qual

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  ends = datetime.strptime(ending_date, "%Y-%m-%d") - today
  return delta.days, ends.days

def get_birthday():
  next1 = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  next2 = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next1 < datetime.now():
    next1 = next1.replace(year=next1.year + 1) 
  if next2 < datetime.now():
    next2 = next2.replace(year=next2.year + 1)
  return (next1 - today).days, (next2 - today).days

def get_weekday():
    day = today.weekday()
    if(day==0):   
        wday = "星期一"
    elif(day==1): 
        wday = "星期二"
    elif(day==2): 
        wday = "星期三"
    elif(day==3):
        wday = "星期四"
    elif(day==4):
        wday = "星期五"
    elif(day==5):
        wday = "星期六"
    elif(day==6):
        wday = "星期日"
    return wday

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
region,city,prov,data,text_now,temp_now,temp_min, \
    temp_max,day_wea,night_wea,sunrise,sunset,moonrise,moonset,air_qual = get_weather()
wm = WeChatMessage(client)
days_start, days_ends = get_count()
data = {"region":{"value":region, "color":get_random_color()},
        "city":{"value":city, "color":get_random_color()},
        "prov":{"value":prov, "color":get_random_color()},
        "date":{"value":data, "color":get_random_color()},
        "wday":{"value":get_weekday(), "color":get_random_color()},
        "wea_now":{"value":text_now, "color":get_random_color()}, 
        "temp_now":{"value":temp_now, "color":get_random_color()},
        "temp_min":{"value":temp_min, "color":get_random_color()},
        "temp_max":{"value":temp_max, "color":get_random_color()},
        "day_wea":{"value":day_wea, "color":get_random_color()},
        "night_wea":{"value":night_wea, "color":get_random_color()},
        "sunrise":{"value":sunrise, "color":get_random_color()},
        "sunset":{"value":sunset, "color":get_random_color()},
        "moonrise":{"value":moonrise, "color":get_random_color()},
        "moonset":{"value":moonset, "color":get_random_color()},
        "air_qual":{"value":air_qual, "color":get_random_color()},
        "love_days":{"value":days_start, "color":get_random_color()},
        "ends_days":{"value":days_ends, "color":get_random_color()},
        "birthday1_left":{"value":get_birthday()[0], "color":get_random_color()},
        "birthday2_left":{"value":get_birthday()[1], "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
for wechat_id in user_id:
    res = wm.send_template(wechat_id, template_id, data)
    print(res)
#print(days_ends)
