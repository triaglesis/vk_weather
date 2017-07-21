#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history
# 2015-11-16 Add note about new API method after VK_module update.

import vk
import urllib.request
import lxml.html
import facebook
import random
from time import gmtime, strftime

# This gather information from Yandex weather service by url with xml data
local = "file:///C:/Users/danilcha/PycharmProjects/weather/33711.xml"
live = "http://export.yandex.com/weather-ng/forecasts/33711.xml"
weather_xml = urllib.request.urlopen(live)

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)

# Expiration Time	1452240387 (Fri Jan 08 2016 10:06:27 GMT+0200 (FLE Standard Time))
fb_access_token = \
    'TOKEN'
fb_access_token_2 = \
    'TOKEN'
graph = facebook.GraphAPI(fb_access_token_2)
graph2 = facebook.GraphAPI(fb_access_token)

data = weather_xml.read()
weather_xml.close()
xmldoc = lxml.html.document_fromstring(data)

if xmldoc is not None:
    print("Yandex xml found - parsing")
else:
    print("Weather xml is not available")


# Part 1
# Extracting weather condition for further usage in message compose.
# Known weather types are:
# clear, partly-cloudy, cloudy, overcast, cloudy-and-rain,
# overcast-and-rain, overcast-thunderstorms-with-rain,
# overcast-and-light-rain

# At first - current weather condition
weather_condition = xmldoc.xpath('//weather_condition[1]/@code')
weather_condition = weather_condition[0]

# Then weather conditions for each day period
weather_condition_morning = xmldoc.xpath('//forecast/day/day_part[@typeid="1"]/weather_condition/@code')
weather_condition_day = xmldoc.xpath('//forecast/day/day_part[@typeid="2"]/weather_condition/@code')
weather_condition_evening = xmldoc.xpath('//forecast/day/day_part[@typeid="3"]/weather_condition/@code')
weather_condition_night = xmldoc.xpath('//forecast/day/day_part[@typeid="4"]/weather_condition/@code')

weather_condition_morning = weather_condition_morning[0]
weather_condition_day = weather_condition_day[0]
weather_condition_evening = weather_condition_evening[0]
weather_condition_night = weather_condition_night[0]

if weather_condition \
        and weather_condition_morning \
        and weather_condition_day \
        and weather_condition_evening \
        and weather_condition_night is not None:
    print("weather_conditions are found! They are: -"
          " morning: "
          + weather_condition_morning +
          "| daily: "
          + weather_condition_day +
          "| evening: "
          + weather_condition_evening +
          "| night: "
          + weather_condition_night)
else:
    print("weather_condition is not available")


# Part 2
# Extracting weather data for current time
# Current time is that time when xml data was gathered from server
observation_time = xmldoc.xpath('//forecast/fact/observation_time/text()')
uptime = xmldoc.xpath('//forecast/fact/uptime/text()')
weather_type_ua = xmldoc.xpath('//forecast/fact/weather_type_ua/text()')
wind_direction = xmldoc.xpath('//forecast/fact/wind_direction/text()')
wind_speed = xmldoc.xpath('//forecast/fact/wind_speed/text()')
humidity = xmldoc.xpath('//forecast/fact/humidity/text()')
pressure = xmldoc.xpath('//forecast/fact/pressure/text()')
mslp_pressure = xmldoc.xpath('//forecast/fact/mslp_pressure/text()')

if observation_time:
    print("Time is " + str(observation_time) + " will parse xml further")
else:
    print("parsing interrupted on line 72")

# going to string
observation_time = ''.join(observation_time)
uptime = ''.join(uptime)
weather_type_ua = ''.join(weather_type_ua)
wind_direction = ''.join(wind_direction)
wind_speed = ''.join(wind_speed)
humidity = ''.join(humidity)
pressure = ''.join(pressure)
mslp_pressure = ''.join(mslp_pressure)

# from Part 1
curr_emoji = ''
curr_emoji_fb = ''
if weather_condition == "clear":
    curr_emoji = "&#9728;"
elif weather_condition == "partly-cloudy":
    curr_emoji = "&#9925;"
elif weather_condition == "cloudy":
    curr_emoji = "&#9925;"
elif weather_condition == "overcast":
    curr_emoji = "&#9729; &#9729;"
elif weather_condition == "cloudy-and-rain":
    curr_emoji = "&#9729; &#128166; &#9748;"
elif weather_condition == "overcast-and-rain":
    curr_emoji = "&#9729; &#9729; &#128166; &#9748"
elif weather_condition == "overcast-thunderstorms-with-rain":
    curr_emoji = "&#9729; &#9889; &#127744; &#9748;"
elif weather_condition == "overcast-and-light-rain":
    curr_emoji = "&#9729; &#128167; &#127746;"
elif weather_condition == "overcast-and-snow":
    curr_emoji = "&#9729; &#10052; &#127784;"
elif weather_condition == "overcast-and-light-snow":
    curr_emoji = "&#9729; &#10052; &#127784;"
else:
    curr_condition = "&#10067;"

current_msg = ("Погода станом на {0}\nЗараз на вулиці {1} {2}. \n"
               "Напрямок вітру - {3}, швидкість - {4} м\\с. \n"
               "Відносна вологість повітря - {5}%, \n"
               "Тиск - {6} кПа або - {7} мм рт. ст.".format(uptime,
                                                            weather_type_ua,
                                                            curr_emoji,
                                                            wind_direction,
                                                            wind_speed,
                                                            humidity,
                                                            mslp_pressure,
                                                            pressure))
current_msg_fb = ("Погода станом на {0}\nЗараз на вулиці {1} . \n"
                  "Напрямок вітру - {2}, швидкість - {3} м\\с. \n"
                  "Відносна вологість повітря - {4}%, \n"
                  "Тиск - {5} кПа або - {6} мм рт. ст.".format(uptime,
                                                               weather_type_ua,
                                                               wind_direction,
                                                               wind_speed,
                                                               humidity,
                                                               mslp_pressure,
                                                               pressure))

curr_date = strftime("%Y-%m-%d")
date = strftime("%Y""-""%m""-""%d", gmtime())
date = str(date)

# Part 3
# Extracting forecast for current date with details till day ends
# Starting from solar and moon cycles
sunrise = xmldoc.xpath('//forecast/day[@date="' + date + '"]/sunrise/text()')
sunset = xmldoc.xpath('//forecast/day[@date="' + date + '"]/sunset/text()')
moon_phase = xmldoc.xpath('//forecast/day[@date="' + date + '"]/moon_phase/text()')
moonrise = xmldoc.xpath('//forecast/day[@date="' + date + '"]/moonrise/text()')
moonset = xmldoc.xpath('//forecast/day[@date="' + date + '"]/moonset/text()')

if sunrise is not None:
    print("Solar is " + str(sunrise) + " will parse xml further")
else:
    print("parsing interrupted on line 180")

sunrise = ''.join(sunrise)
sunset = ''.join(sunset)
moon_phase = ''.join(moon_phase)
moonrise = ''.join(moonrise)
moonset = ''.join(moonset)

if moon_phase == "1":
    moon_emoji = "&#127761;"
elif moon_phase == "2":
    moon_emoji = "&#_127762;"
elif moon_phase == "3":
    moon_emoji = "&#_127763;"
elif moon_phase == "4":
    moon_emoji = "&#127764;"
elif moon_phase == "5":
    moon_emoji = "&#127765;"
elif moon_phase == "6":
    moon_emoji = "&#127766;"
elif moon_phase == "7":
    moon_emoji = "&#127767;"
elif moon_phase == "8":
    moon_emoji = "&#127768;"
else:
    moon_emoji = "&#127769;"

phases_msg = ("Сонце зійде &#127773; о {0} год, захід &#127774; сонця о {1} год. \n"
              "Місяць вийде &#127771; о {2} год, заховається &#127772; о {3} год. \n"
              "Місяць знаходиться у {4}й фазі {5}.".format(sunrise,
                                                           sunset,
                                                           moonrise,
                                                           moonset,
                                                           moon_phase,
                                                           moon_emoji))
phases_msg_fb = ("Сонце зійде о {0} год, захід сонця о {1} год. \n"
                 "Місяць вийде о {2} год, заховається о {3} год. \n"
                 "Місяць знаходиться у {4}й фазі.".format(sunrise,
                                                              sunset,
                                                              moonrise,
                                                              moonset,
                                                              moon_phase))

# Extracting forecast for day periods: morning, day, evening, night
# Part 4
# MORNING
morning_temperature_current = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/temperature/text()')
morning_temperature_from = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/temperature_from/text()')
morning_temperature_to = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/temperature_to/text()')
morning_weather_type_ua = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/weather_type_ua/text()')
morning_wind_direction = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/wind_direction/text()')
morning_wind_speed = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/wind_speed/text()')
morning_humidity = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/humidity/text()')
morning_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/pressure/text()')
morning_mslp_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="1"]/mslp_pressure/text()')

if morning_temperature_from:
    print("Morning temp " + str(morning_temperature_from) +" to "+ str(morning_temperature_to)+ " will parse xml further")
else:
    morning_temperature_from,morning_temperature_to = morning_temperature_current
    print("Morning temperature have one value: "+str(morning_temperature_current))

morning_temperature_from = ''.join(morning_temperature_from)
morning_temperature_to = ''.join(morning_temperature_to)
morning_weather_type_ua = ''.join(morning_weather_type_ua)
morning_wind_direction = ''.join(morning_wind_direction)
morning_wind_speed = ''.join(morning_wind_speed)
morning_humidity = ''.join(morning_humidity)
morning_pressure = ''.join(morning_pressure)
morning_mslp_pressure = ''.join(morning_mslp_pressure)

# from Part 1
if weather_condition_morning == "clear":
    morning_emoji = "&#9728;"
elif weather_condition_morning == "partly-cloudy":
    morning_emoji = "&#9925;"
elif weather_condition_morning == "cloudy":
    morning_emoji = "&#9925;"
elif weather_condition_morning == "overcast":
    morning_emoji = "&#9729; &#9729;"
elif weather_condition_morning == "cloudy-and-rain":
    morning_emoji = "&#9729; &#128166; &#9748;"
elif weather_condition_morning == "overcast-and-rain":
    morning_emoji = "&#9729; &#9729; &#128166; &#9748"
elif weather_condition_morning == "overcast-thunderstorms-with-rain":
    morning_emoji = "&#9729; &#9889; &#127744; &#9748;"
elif weather_condition_morning == "overcast-and-light-rain":
    morning_emoji = "&#9729; &#128167; &#127746;"
elif weather_condition_morning == "overcast-and-snow":
    morning_emoji = "&#9729; &#10052; &#127784;"
elif weather_condition_morning == "overcast-and-light-snow":
    morning_emoji = "&#9729; &#10052; &#127784;"
else:
    morning_emoji = "&#10067;"

morning_msg = ("Зранку, &#128201; {0}° &#128200; {1}°. Загальний стан - {2} {3}.\n"
               "Напрямок вітру - {4}, швидкість - {5} м\\с, відносна вологість повітря - {6}%. \n"
               "Тиск - {7} кПа або - {8} мм рт. ст.".format(morning_temperature_from,
                                                            morning_temperature_to,
                                                            morning_weather_type_ua,
                                                            morning_emoji,
                                                            morning_wind_direction,
                                                            morning_wind_speed,
                                                            morning_humidity,
                                                            morning_pressure,
                                                            morning_mslp_pressure))

morning_msg_fb = ("Зранку, {0}° -> {1}°. Загальний стан - {2}.\n"
                  "Напрямок вітру - {3}, швидкість - {4} м\\с, відносна вологість повітря - {5}%. \n"
                  "Тиск - {6} кПа або {7} мм рт. ст.".format(morning_temperature_from,
                                                               morning_temperature_to,
                                                               morning_weather_type_ua,
                                                               morning_wind_direction,
                                                               morning_wind_speed,
                                                               morning_humidity,
                                                               morning_pressure,
                                                               morning_mslp_pressure))

# Part 5
# DAY
day_temperature_current = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/temperature/text()')
day_temperature_from = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/temperature_from/text()')
day_temperature_to = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/temperature_to/text()')
day_weather_type_ua = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/weather_type_ua/text()')
day_wind_direction = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/wind_direction/text()')
day_wind_speed = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/wind_speed/text()')
day_humidity = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/humidity/text()')
day_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/pressure/text()')
day_mslp_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="2"]/mslp_pressure/text()')

if day_temperature_from:
    print("Day temp " + str(day_temperature_from) +" to "+ str(day_temperature_to)+ " will parse xml further")
else:
    day_temperature_from,day_temperature_to = day_temperature_current
    print("Day temperature have one value: "+str(day_temperature_current))

day_temperature_from = ''.join(day_temperature_from)
day_temperature_to = ''.join(day_temperature_to)
day_weather_type_ua = ''.join(day_weather_type_ua)
day_wind_direction = ''.join(day_wind_direction)
day_wind_speed = ''.join(day_wind_speed)
day_humidity = ''.join(day_humidity)
day_pressure = ''.join(day_pressure)
day_mslp_pressure = ''.join(day_mslp_pressure)

# from Part 1
day_emoji = ''
day_emoji_fb = ''
if weather_condition_day == "clear":
    day_emoji = "&#9728;"
elif weather_condition_day == "partly-cloudy":
    day_emoji = "&#9925;"
elif weather_condition_day == "cloudy":
    day_emoji = "&#9925;"
elif weather_condition_day == "overcast":
    day_emoji = "&#9729; &#9729;"
elif weather_condition_day == "cloudy-and-rain":
    day_emoji = "&#9729; &#128166; &#9748;"
elif weather_condition_day == "overcast-and-rain":
    day_emoji = "&#9729; &#9729; &#128166; &#9748"
elif weather_condition_day == "overcast-thunderstorms-with-rain":
    day_emoji = "&#9729; &#9889; &#127744; &#9748;"
elif weather_condition_day == "overcast-and-light-rain":
    day_emoji = "&#9729; &#128167; &#127746;"
elif weather_condition_day == "overcast-and-snow":
    day_emoji = "&#9729; &#10052; &#127784;"
elif weather_condition_day == "overcast-and-light-snow":
    day_emoji = "&#9729; &#10052; &#127784;"
else:
    weather_condition_day = "&#10067;"

day_msg = ("У день, &#128201; {0}° &#128200; {1}°. Загальний стан - {2} {3}.\n"
           "Напрямок вітру - {4}, швидкість - {5} м\\с, відносна вологість повітря - {6}%. \n"
           "Тиск - {7} кПа або {8} мм рт. ст.".format(day_temperature_from,
                                                      day_temperature_to,
                                                      day_weather_type_ua,
                                                      day_emoji,
                                                      day_wind_direction,
                                                      day_wind_speed,
                                                      day_humidity,
                                                      day_pressure,
                                                      day_mslp_pressure))

day_msg_fb = ("У день, {0}° -> {1}°. Загальний стан - {2}.\n"
                  "Напрямок вітру - {3}, швидкість - {4} м\\с, відносна вологість повітря - {5}%. \n"
                  "Тиск - {6} кПа або {7} мм рт. ст.".format(day_temperature_from,
                                                         day_temperature_to,
                                                         day_weather_type_ua,
                                                         day_wind_direction,
                                                         day_wind_speed,
                                                         day_humidity,
                                                         day_pressure,
                                                         day_mslp_pressure))

# Part 6
# EVENING
evening_temperature_current = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/temperature/text()')
evening_temperature_from = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/temperature_from/text()')
evening_temperature_to = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/temperature_to/text()')
evening_weather_type_ua = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/weather_type_ua/text()')
evening_wind_direction = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/wind_direction/text()')
evening_wind_speed = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/wind_speed/text()')
evening_humidity = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/humidity/text()')
evening_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/pressure/text()')
evening_mslp_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="3"]/mslp_pressure/text()')

if evening_temperature_from:
    print("Evening temp " + str(evening_temperature_from) +" to "+ str(evening_temperature_to)+ " will parse xml further")
else:
    evening_temperature_from,evening_temperature_to = evening_temperature_current
    print("Evening temperature have one value: "+str(evening_temperature_current))

evening_temperature_from = ''.join(evening_temperature_from)
evening_temperature_to = ''.join(evening_temperature_to)
evening_weather_type_ua = ''.join(evening_weather_type_ua)
evening_wind_direction = ''.join(evening_wind_direction)
evening_wind_speed = ''.join(evening_wind_speed)
evening_humidity = ''.join(evening_humidity)
evening_pressure = ''.join(evening_pressure)
evening_mslp_pressure = ''.join(evening_mslp_pressure)

# from Part 1
if weather_condition_evening == "clear":
    evening_emoji = "&#9728;"
elif weather_condition_evening == "partly-cloudy":
    evening_emoji = "&#9925;"
elif weather_condition_evening == "cloudy":
    evening_emoji = "&#9925;"
elif weather_condition_evening == "overcast":
    evening_emoji = "&#9729; &#9729;"
elif weather_condition_evening == "cloudy-and-rain":
    evening_emoji = "&#9729; &#128166; &#9748;"
elif weather_condition_evening == "overcast-and-rain":
    evening_emoji = "&#9729; &#9729; &#128166; &#9748"
elif weather_condition_evening == "overcast-thunderstorms-with-rain":
    evening_emoji = "&#9729; &#9889; &#127744; &#9748;"
elif weather_condition_evening == "overcast-and-light-rain":
    evening_emoji = "&#9729; &#128167; &#127746;"
elif weather_condition_evening == "overcast-and-snow":
    evening_emoji = "&#9729; &#10052; &#127784;"
elif weather_condition_evening == "overcast-and-light-snow":
    evening_emoji = "&#9729; &#10052; &#127784;"
else:
    evening_emoji = "&#10067;"

evening_msg = ("Ввечері, &#128201; {0}° &#128200; {1}°. Загальний стан - {2} {3}.\n"
               "Напрямок вітру - {4}, швидкість - {5} м\\с, відносна вологість повітря - {6}%. \n"
               "Тиск - {7} кПа або {8} мм рт. ст.".format(evening_temperature_from,
                                                          evening_temperature_to,
                                                          evening_weather_type_ua,
                                                          evening_emoji,
                                                          evening_wind_direction,
                                                          evening_wind_speed,
                                                          evening_humidity,
                                                          evening_pressure,
                                                          evening_mslp_pressure))

evening_msg_fb = ("Ввечері, {0}° -> {1}°. Загальний стан - {2}.\n"
                  "Напрямок вітру - {3}, швидкість - {4} м\\с, відносна вологість повітря - {5}%. \n"
                  "Тиск - {6} кПа або {7} мм рт. ст.".format(evening_temperature_from,
                                                             evening_temperature_to,
                                                             evening_weather_type_ua,
                                                             evening_wind_direction,
                                                             evening_wind_speed,
                                                             evening_humidity,
                                                             evening_pressure,
                                                             evening_mslp_pressure))

# Part 7
# NIGHT
night_temperature_current = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/temperature/text()')
night_temperature_from = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/temperature_from/text()')
night_temperature_to = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/temperature_to/text()')
night_weather_type_ua = xmldoc.xpath(
    '//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/weather_type_ua/text()')
night_wind_direction = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/wind_direction/text()')
night_wind_speed = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/wind_speed/text()')
night_humidity = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/humidity/text()')
night_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/pressure/text()')
night_mslp_pessure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="4"]/mslp_pressure/text()')

if night_temperature_from:
    print("Night temp " + str(night_temperature_from) +" to "+ str(night_temperature_to)+ " will parse xml further")
else:
    night_temperature_from,night_temperature_to = night_temperature_current
    print("Night temperature have one value: "+str(night_temperature_current))

night_temperature_from = ''.join(night_temperature_from)
night_temperature_to = ''.join(night_temperature_to)
night_weather_type_ua = ''.join(night_weather_type_ua)
night_wind_direction = ''.join(night_wind_direction)
night_wind_speed = ''.join(night_wind_speed)
night_humidity = ''.join(night_humidity)
night_pressure = ''.join(night_pressure)
night_mslp_pessure = ''.join(night_mslp_pessure)

# from Part 1
night_emoji = ''
night_emoji_fb = ''
if weather_condition_night == "clear":
    night_emoji = "&#9728;"
elif weather_condition_night == "partly-cloudy":
    night_emoji = "&#9925;"
elif weather_condition_night == "cloudy":
    night_emoji = "&#9925;"
elif weather_condition_night == "overcast":
    night_emoji = "&#9729; &#9729;"
elif weather_condition_night == "cloudy-and-rain":
    night_emoji = "&#9729; &#128166; &#9748;"
elif weather_condition_night == "overcast-and-rain":
    night_emoji = "&#9729; &#9729; &#128166; &#9748"
elif weather_condition_night == "overcast-thunderstorms-with-rain":
    night_emoji = "&#9729; &#9889; &#127744; &#9748;"
elif weather_condition_night == "overcast-and-light-rain":
    night_emoji = "&#9729; &#128167; &#127746;"
elif weather_condition_night == "overcast-and-snow":
    night_emoji = "&#9729; &#10052; &#127784;"
elif weather_condition_night == "overcast-and-light-snow":
    night_emoji = "&#9729; &#10052; &#127784;"
else:
    weather_condition_night = "&#10067;"

night_msg = ("Вночі, &#128201; {0}° &#128200; {1}°. Загальний стан - {2} {3}.\n"
             "Напрямок вітру - {4}, швидкість - {5} м\\с, відносна вологість повітря - {6}%. \n"
             "Тиск - {7} кПа або {8} мм рт. ст.".format(night_temperature_from,
                                                        night_temperature_to,
                                                        night_weather_type_ua,
                                                        night_emoji,
                                                        night_wind_direction,
                                                        night_wind_speed,
                                                        night_humidity,
                                                        night_pressure,
                                                        night_mslp_pessure))

night_msg_fb = ("Вночі, {0}° -> {1}°. Загальний стан - {2}.\n"
                "Напрямок вітру - {3}, швидкість - {4} м\\с, відносна вологість повітря - {5}%. \n"
                "Тиск - {6} кПа або {7} мм рт. ст.".format(night_temperature_from,
                                                           night_temperature_to,
                                                           night_weather_type_ua,
                                                           night_wind_direction,
                                                           night_wind_speed,
                                                           night_humidity,
                                                           night_pressure,
                                                           night_mslp_pessure))

# Part 8
# Vk message format:
vk_disclaimer = "Пропонуйте ваші варіанти музичних композицій до варіантів прогнозів, ваші варіанти додавайте в коментарі! \n" \
                "\n\n #ВождьБот Powered by #Python made by #trianglesis"
vk_tags = "#weather@typical_kirovohrad, #weather, #forecast, #weatherbot, #forecastbot, #kirovohrad, #kirovograd, #кировоград, #кіровоград, #ПогодавКировограде, #КировоградПогода"
fb_tags =                              "#weather, #forecast, #weatherbot, #forecastbot, #kirovohrad, #kirovograd, #кировоград, #кіровоград, #ПогодавКировограде, #КировоградПогода" \
                                       "\n\n #ВождьБот Powered by #Python made by #trianglesis"

forecast_vk_format = (
    current_msg + "\n\n"
    + morning_msg + "\n\n"
    + day_msg + "\n\n"
    + evening_msg + "\n\n"
    + night_msg + "\n\n"
    + phases_msg + "\n\n"
    + vk_disclaimer + "\n\n"
    + vk_tags )

forecast_fb_format = (
    current_msg_fb + "\n\n"
    + morning_msg_fb + "\n\n"
    + day_msg_fb + "\n\n"
    + evening_msg_fb + "\n\n"
    + night_msg_fb + "\n\n"
    + phases_msg_fb + "\n\n"
    + fb_tags )

# Part 9
# Making list of different music tracks for different weather conditions
# Add getRandom later
vk_audio_clear = ['audio13147598_392892048', 'audio13147598_393731431', 'audio13147598_393731431','audio13147598_393730840', 'audio13147598_393731054', 'audio13147598_393731061','audio13147598_393731137', 'audio13147598_393731156', 'audio13147598_392892048','audio13147598_392891949', 'audio13147598_392891903', 'audio13147598_354809708','audio13147598_203213779']
vk_audio_p_cloudy = ['audio13147598_392891892', 'audio13147598_393730999', 'audio13147598_393731643','audio13147598_168702183', 'audio10104114_40465220', 'audio16440592_105091724','audio21473615_86627846', 'audio17010609_89910003', 'audio2262816_72319015','audio13147598_392891899', 'audio13147598_393777946']
vk_audio_cloudy = ['audio13147598_392891899', 'audio13147598_393731112', 'audio13147598_393730794','audio13147598_392891899', 'audio13147598_392891892', 'audio13147598_80752804','audio45289745_278972615', 'audio998400_106233375', 'audio2000002889_303369728','audio13147598_393777946']
vk_audio_overcast = ['audio13147598_392891903', 'audio13147598_393730862', 'audio12210495_123874930','audio58719920_163228135', 'audio20402318_354055585', 'audio122240028_212211793','audio7822288_90974312', 'audio83697245_92452562', 'audio13147598_393777946','audio2000002889_303369728', 'audio13147598_392891899']
vk_audio_cloudy_rain = ['audio13147598_392891909', 'audio13147598_393730710', 'audio13147598_393730714','audio13147598_393731076', 'audio13147598_393730937', 'audio13147598_254268328','audio13147598_230573116', 'audio16877413_96623057', 'audio13147598_393775882','audio13147598_393777946', 'audio2000204170_389472212', 'audio2000411568_353476605','audio21417336_163050397']
vk_audio_overcast_rain = ['audio13147598_392891918', 'audio2000505299_365265705', 'audio13147598_393731092','audio13147598_393730999', 'audio13147598_393730918', 'audio13147598_392891918','audio13147598_392882916', 'audio13147598_230573116', 'audio13147598_393775882','audio2000197117_270072237', 'audio955704_393593734', 'audio2000411568_353476605','audio92283068_170181592', 'audio2000204170_389472212', 'audio21417336_163050397']
vk_audio_overcast_thund_rain = ['audio13147598_392891921', 'audio13147598_393730965', 'audio13147598_393731040','audio13147598_393731170', 'audio13147598_393730899', 'audio13147598_393730878','audio13147598_392891921', 'audio13147598_392883215', 'audio13147598_176207568','audio3886954_63980227', 'audio147062527_369796624', 'audio2000203634_390237740','audio2000190996_387787540', 'audio162092922_359025590', 'audio2000165334_385287467']
vk_audio_overcast_light_rain = ['audio13147598_392891927', 'audio13147598_393730746', 'audio13147598_393730721','audio13147598_393730714', 'audio13147598_393730710', 'audio13147598_392891927','audio54138656_122366296', 'audio196268_239878470', 'audio2000482308_367227725','audio2000197117_270072237', 'audio955704_393593734', 'audio2000411568_353476605','audio92283068_170181592', 'audio2000204170_389472212']
vk_audio_overcast_and_snow = ['audio27532861_92074400', 'audio-13315679_71499717', 'audio10906876_70273079', 'audio-80882763_323781067', 'audio-107257502_423300450', 'audio-91215428_372335804', 'audio-101350019_398280381', 'audio4744443_187366711', 'audio4744443_428049163', 'audio-80611218_323380240']
vk_audio_overcast_and_light_snow = ['audio27532861_92074400', 'audio-13315679_71499717', 'audio10906876_70273079', 'audio-80882763_323781067', 'audio-107257502_423300450', 'audio-91215428_372335804', 'audio-101350019_398280381', 'audio4744443_187366711', 'audio4744443_428049163', 'audio-80611218_323380240']
vk_audio_other = ['audio13147598_392758605', 'audio2925497_45647607', 'audio10383013_68094242','audio115055933_106584596', 'audio3454267_66518906']


# from Part 1
if weather_condition == "clear":
    vk_audio = vk_audio_clear
    vk_picture = "photo-46631810_378522420"
elif weather_condition == "partly-cloudy":
    vk_audio = vk_audio_p_cloudy
    vk_picture = "photo-46631810_378522454"
elif weather_condition == "cloudy":
    vk_audio = vk_audio_cloudy
    vk_picture = "photo-46631810_378522423"
elif weather_condition == "overcast":
    vk_audio = vk_audio_overcast
    vk_picture = "photo-46631810_378557770"
elif weather_condition == "cloudy-and-rain":
    vk_audio = vk_audio_cloudy_rain
    vk_picture = "photo-46631810_378522428"
elif weather_condition == "overcast-and-rain":
    vk_audio = vk_audio_overcast_rain
    vk_picture = "photo-46631810_378522444"
elif weather_condition == "overcast-thunderstorms-with-rain":
    vk_audio = vk_audio_overcast_thund_rain
    vk_picture = "photo-46631810_378522447"
elif weather_condition == "overcast-and-light-rain":
    vk_audio = vk_audio_overcast_light_rain
    vk_picture = "photo-46631810_378522436"
elif weather_condition_morning == "overcast-and-snow":
    vk_audio = vk_audio_overcast_and_snow
    vk_picture = "photo-46631810_395154137"
elif weather_condition_morning == "overcast-and-light-snow":
    vk_audio = vk_audio_overcast_and_light_snow
    vk_picture = "photo-46631810_395154132"
else:
    vk_audio = vk_audio_other
    vk_picture = "photo-46631810_378523077"
    fb_picture = "http://typical-kirovohrad.org.ua/Files/Images/weather/other.png"


# Choose 3 songs from list randomly and convert them to a comma-sep string
vk_audio_lst = random.sample(set(vk_audio), 3)
vk_audio_str = ','.join(vk_audio_lst)

vk_attachment = vk_audio_str + "," + vk_picture

# Part 10
# Making post
typical_kirovohrad = "-46631810"
typical_kirovohrad_boss = "13147598"

wall_post = vkapi('wall.post',
                  owner_id=typical_kirovohrad,
                  from_group='1',
                  message=forecast_vk_format,
                  attachments=vk_attachment,
                  signed='0')
print("Message has been posted to VK!\n")

post = graph.put_wall_post(forecast_fb_format,
                           attachment={
                               'caption': 'Погода від "ТК"',
                               'description': 'Прогноз погоди від спільноти "ТК"',
                           },
                           profile_id='318878038180954')
print("Message has been posted to FB 1st!\n")

post2 = graph2.put_wall_post(forecast_fb_format,
                            attachment = {
                                'caption': 'Погода від "ТК"',
                                'description': 'Прогноз погоди від спільноти "ТК"',
                            },
                            profile_id='931178533576777')
print("Message has been posted to FB 2nd!\n")

print(forecast_vk_format)
# print(forecast_fb_format)
print("Messages has been posted!")