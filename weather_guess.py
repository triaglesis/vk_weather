#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history
# 2015-11-16 Add note about new API method after VK_module update.

import vk
import urllib.request
import lxml.html
import random
import datetime
from time import gmtime, strftime, sleep

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)
curr_date = strftime("%Y-%m-%d")
date = strftime("%Y""-""%m""-""%d", gmtime())
date = str(date)

today = datetime.date.today()
tomorrow_date = today + datetime.timedelta(days=1)
tomorrow = str(tomorrow_date)

print("Today is - " + curr_date + " date")
print("Tomorrow is - " + tomorrow + " date")

# This gather information from Yandex weather service by url with xml data
local = "file:///D:/Projects/PycharmProjects/Test/Working/vk_weather/PIC/33711.xml"
live = "http://export.yandex.ua/weather-ng/forecasts/33711.xml"

weather_xml = ''
try:
    weather_xml = urllib.request.urlopen(live)
except:
    print("Weather link is not working")

xmldoc = ''
if weather_xml:
    data = weather_xml.read()
    weather_xml.close()
    xmldoc = lxml.html.document_fromstring(data)
else:
    print("No access to Yandex weather xml")

while len(xmldoc) < 1:
    try:
        weather_xml = urllib.request.urlopen(live)
        data = weather_xml.read()
        weather_xml.close()
        xmldoc = lxml.html.document_fromstring(data)
        print("xmldoc is TRUE - continue")
    except:
        print("xmldoc is FALSE - looping")
        sleep(1)

if len(xmldoc) > 0:
    weather_condition_morning = \
        xmldoc.xpath('//forecast/day[@date="' + tomorrow + '"]/day_part[@typeid="1"]/weather_condition[1]/@code')
    weather_condition_day = \
        xmldoc.xpath('//forecast/day[@date="' + tomorrow + '"]/day_part[@typeid="2"]/weather_condition[1]/@code')
    weather_condition_evening = \
        xmldoc.xpath('//forecast/day[@date="' + tomorrow + '"]/day_part[@typeid="3"]/weather_condition[1]/@code')
    weather_condition_night = \
        xmldoc.xpath('//forecast/day[@date="' + tomorrow + '"]/day_part[@typeid="4"]/weather_condition[1]/@code')

    weather_condition_morning = weather_condition_morning[0]
    weather_condition_day = weather_condition_day[0]
    weather_condition_evening = weather_condition_evening[0]
    weather_condition_night = weather_condition_night[0]

    if weather_condition_morning \
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
    if weather_condition_morning == "clear":
        vk_audio_morning = vk_audio_clear
    elif weather_condition_morning == "partly-cloudy":
        vk_audio_morning = vk_audio_p_cloudy
    elif weather_condition_morning == "cloudy":
        vk_audio_morning = vk_audio_cloudy
    elif weather_condition_morning == "overcast":
        vk_audio_morning = vk_audio_overcast
    elif weather_condition_morning == "cloudy-and-rain":
        vk_audio_morning = vk_audio_cloudy_rain
    elif weather_condition_morning == "overcast-and-rain":
        vk_audio_morning = vk_audio_overcast_rain
    elif weather_condition_morning == "overcast-thunderstorms-with-rain":
        vk_audio_morning = vk_audio_overcast_thund_rain
    elif weather_condition_morning == "overcast-and-light-rain":
        vk_audio_morning = vk_audio_overcast_light_rain
    elif weather_condition_morning == "overcast-and-snow":
        vk_audio_morning = vk_audio_overcast_and_snow
    elif weather_condition_morning == "overcast-and-light-snow":
        vk_audio_morning = vk_audio_overcast_and_light_snow
    else:
        vk_audio_morning = vk_audio_other

    if weather_condition_day == "clear":
        vk_audio_day = vk_audio_clear
    elif weather_condition_day == "partly-cloudy":
        vk_audio_day = vk_audio_p_cloudy
    elif weather_condition_day == "cloudy":
        vk_audio_day = vk_audio_cloudy
    elif weather_condition_day == "overcast":
        vk_audio_day = vk_audio_overcast
    elif weather_condition_day == "cloudy-and-rain":
        vk_audio_day = vk_audio_cloudy_rain
    elif weather_condition_day == "overcast-and-rain":
        vk_audio_day = vk_audio_overcast_rain
    elif weather_condition_day == "overcast-thunderstorms-with-rain":
        vk_audio_day = vk_audio_overcast_thund_rain
    elif weather_condition_day == "overcast-and-light-rain":
        vk_audio_day = vk_audio_overcast_light_rain
    elif weather_condition_morning == "overcast-and-snow":
        vk_audio_day = vk_audio_overcast_and_snow
    elif weather_condition_morning == "overcast-and-light-snow":
        vk_audio_day = vk_audio_overcast_and_light_snow
    else:
        vk_audio_day = vk_audio_other

    if weather_condition_evening == "clear":
        vk_audio_evening = vk_audio_clear
    elif weather_condition_evening == "partly-cloudy":
        vk_audio_evening = vk_audio_p_cloudy
    elif weather_condition_evening == "cloudy":
        vk_audio_evening = vk_audio_cloudy
    elif weather_condition_evening == "overcast":
        vk_audio_evening = vk_audio_overcast
    elif weather_condition_evening == "cloudy-and-rain":
        vk_audio_evening = vk_audio_cloudy_rain
    elif weather_condition_evening == "overcast-and-rain":
        vk_audio_evening = vk_audio_overcast_rain
    elif weather_condition_evening == "overcast-thunderstorms-with-rain":
        vk_audio_evening = vk_audio_overcast_thund_rain
    elif weather_condition_evening == "overcast-and-light-rain":
        vk_audio_evening = vk_audio_overcast_light_rain
    elif weather_condition_morning == "overcast-and-snow":
        vk_audio_evening = vk_audio_overcast_and_snow
    elif weather_condition_morning == "overcast-and-light-snow":
        vk_audio_evening = vk_audio_overcast_and_light_snow
    else:
        vk_audio_evening = vk_audio_other

    if weather_condition_night == "clear":
        vk_audio_night = vk_audio_clear
    elif weather_condition_night == "partly-cloudy":
        vk_audio_night = vk_audio_p_cloudy
    elif weather_condition_night == "cloudy":
        vk_audio_night = vk_audio_cloudy
    elif weather_condition_night == "overcast":
        vk_audio_night = vk_audio_overcast
    elif weather_condition_night == "cloudy-and-rain":
        vk_audio_night = vk_audio_cloudy_rain
    elif weather_condition_night == "overcast-and-rain":
        vk_audio_night = vk_audio_overcast_rain
    elif weather_condition_night == "overcast-thunderstorms-with-rain":
        vk_audio_night = vk_audio_overcast_thund_rain
    elif weather_condition_night == "overcast-and-light-rain":
        vk_audio_night = vk_audio_overcast_light_rain
    elif weather_condition_morning == "overcast-and-snow":
        vk_audio_night = vk_audio_overcast_and_snow
    elif weather_condition_morning == "overcast-and-light-snow":
        vk_audio_night = vk_audio_overcast_and_light_snow
    else:
        vk_audio_night = vk_audio_other

    vk_picture = "photo-46631810_395132739"

    # Choose 3 songs from list randomly and convert them to a comma-sep string
    vk_audio_lst_morning = random.sample(set(vk_audio_morning), 1)
    vk_audio_str_morning = ','.join(vk_audio_lst_morning)

    vk_audio_lst_day = random.sample(set(vk_audio_day), 1)
    vk_audio_str_day = ','.join(vk_audio_lst_day)

    vk_audio_lst_evening = random.sample(set(vk_audio_evening), 1)
    vk_audio_str_evening = ','.join(vk_audio_lst_evening)

    vk_audio_lst_night = random.sample(set(vk_audio_night), 1)
    vk_audio_str_night = ','.join(vk_audio_lst_night)

    vk_attachment = vk_audio_str_morning + "," \
                    + vk_audio_str_day + "," \
                    + vk_audio_str_evening + "," \
                    + vk_audio_str_night + "," \
                    + vk_picture

    forecast_vk_format = "Угадай погоду!" \
                         "\n Расположение музыкальных треков соответствует времени суток:" \
                         "\n 1я - утро, 2я - день, 3я - вечер, 4я - ночь" \
                         "\n" \
                         "\n Предлагайте ваши варианты песен для прогнозов погоды в vk.com/topic-46631810_32371854" \
                         "\n" \
                         "#weather@typical_kirovohrad, #weather, #forecast, #weatherbot, #forecastbot," \
                         " #kirovohrad, #kirovograd, #кировоград, #кіровоград, #ПогодавКировограде" \
                         "\n\n #ВождьБот Powered by #Python made by #trianglesis"

    typical_kirovohrad = "-46631810"
    typical_kirovohrad_boss = "13147598"

    wall_post = vkapi('wall.post',
                      owner_id=typical_kirovohrad,
                      from_group='1',
                      message=forecast_vk_format,
                      attachments=vk_attachment,
                      signed='0')

    # print(forecast_vk_format)
    print("Message has been posted!")
else:
    print("Weather xml is not available")