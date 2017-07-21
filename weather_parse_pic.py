#! /usr/bin/env python3
# coding=utf-8
__author__ = 'Dasha', 'danilcha'
# Change history
# 2015-11-16 Add note about new API method after VK_module update.

import vk
import urllib.request
import lxml.html
import facebook
import random
from time import gmtime, strftime, sleep
from PIL import Image, ImageDraw, ImageFont
import requests

# Config date:
curr_date = strftime("%Y-%m-%d")
curr_time = strftime("%H:%M")
date = strftime("%Y""-""%m""-""%d", gmtime())
date = str(date)

# Debug settings:
debug = 1
if debug == 1:
    weather_forecast_pic = "E:\\Pictures\\Works\\Типичный\\Графика группы\\PSD\\banners\\weather\\"
    weather_icons = "E:\\Pictures\\Works\\Типичный\\Графика группы\\PSD\\banners\\weather\\weather_icons\\"
    font = "E:\\Pictures\\Works\\Типичный\\Графика группы\\PSD\\banners\\weather\\weather_icons\\impact.ttf"
    post_to = "13147598"
elif debug == 0:
    weather_forecast_pic = "/var/www/python-lab/weather_icons/"
    weather_icons = "/var/www/python-lab/weather_icons/"
    font = "/var/www/python-lab/weather_icons/impact.ttf"
    post_to = "-46631810"
else:
    weather_forecast_pic = ""
    weather_icons = ""
    font = ""
    post_to = ""

im = Image.open(weather_forecast_pic+"weather_forecast.png")
copy_im = im.copy()
draw = ImageDraw.Draw(copy_im)
font_status = ImageFont.truetype(font, 45, encoding='utf-8')
font_temp = ImageFont.truetype(font, 50, encoding='utf-8')
font_forecast = ImageFont.truetype(font, 40, encoding='utf-8')
font_copyright = ImageFont.truetype(font, 25, encoding='utf-8')


current_coordinates = (120, 135)
morning_coordinates = (250, 265)
day_coordinates =     (380, 395)
evening_coordinates = (510, 525)
night_coordinates =   (640, 655)

date_txt = draw.text((25, 15), date, fill='white', font=ImageFont.truetype(font, 29, encoding='utf-8'))
time_txt = draw.text((50, 45), curr_time, fill='white', font=ImageFont.truetype(font, 29, encoding='utf-8'))

def weather_pictures(weather_tuple, coordinates):
    '''
    :param weather_tuple:  ('-7', '-6', 'overcast', 'хмарно', 'nw', '8.5', '75', '744', '992')
    :param coordinates: (280, 360)
    :return:
    '''
    from_left_x = 165
    status_txt_x = 285
    temp_from_x = 670
    temp_to_x = 730
    pressure_x = 830
    wind_x = 935
    wind_dir_x = 990
    humidity_x = 1080

    status = weather_tuple[3]
    if "," in status:
        draw.text((status_txt_x, coordinates[1]-25), status.replace(",",", \n"), fill='white', font=font_status)
    elif "із" in status:
        draw.text((status_txt_x, coordinates[1]-25), status.replace("із","із\n"), fill='white', font=font_status)
    else:
        draw.text((status_txt_x, coordinates[1]), status, fill='white', font=font_status)

    temperature_from = weather_tuple[0]
    if "-" not in temperature_from:
        draw.text((temp_from_x+15, coordinates[1]), str(temperature_from), fill='white', font=font_temp)
    else:
        draw.text((temp_from_x, coordinates[1]), str(temperature_from), fill='white', font=font_temp)

    temperature_to = weather_tuple[1]
    if "-" not in temperature_to:
        draw.text((temp_to_x+15, coordinates[1]), str(temperature_to), fill='white', font=font_temp)
    else:
        draw.text((temp_to_x, coordinates[1]), str(temperature_to), fill='white', font=font_temp)

    pressure = weather_tuple[7]
    draw.text((pressure_x, coordinates[1]), str(pressure), fill='white', font=font_forecast)
    wind_speed = weather_tuple[5]
    wind_direction = weather_tuple[4]
    if wind_speed == "0.0":
        draw.text((wind_x, coordinates[1]), str("штиль"), fill='white', font=font_forecast)
    else:
        draw.text((wind_x, coordinates[1]), str(wind_speed), fill='white', font=font_forecast)
        draw.text((wind_dir_x, coordinates[1]), wind_direction, fill='white', font=font_forecast)
    humidity = weather_tuple[6]
    draw.text((humidity_x, coordinates[1]), str(humidity+" %"), fill='white', font=font_forecast)

    if weather_tuple[2] == "clear":
        weather_icon = Image.open(weather_icons+"clear.png")
    elif weather_tuple[2] == "partly-cloudy":
        weather_icon = Image.open(weather_icons+"partly-cloudy.png")
    elif weather_tuple[2] == "cloudy":
        weather_icon = Image.open(weather_icons+"cloudy.png")
    elif weather_tuple[2] == "overcast":
        weather_icon = Image.open(weather_icons+"overcast.png")
    elif weather_tuple[2] == "cloudy-and-rain":
        weather_icon = Image.open(weather_icons+"cloudy-and-rain.png")
    elif weather_tuple[2] == "overcast-and-rain":
        weather_icon = Image.open(weather_icons+"overcast-and-rain.png")
    elif weather_tuple[2] == "overcast-thunderstorms-with-rain":
        weather_icon = Image.open(weather_icons+"overcast-thunderstorms-with-rain.png")
    elif weather_tuple[2] == "overcast-and-light-rain":
        weather_icon = Image.open(weather_icons+"overcast-and-light-rain.png")
    elif weather_tuple[2] == "overcast-and-snow":
        weather_icon = Image.open(weather_icons+"overcast-and-snow.png")
    elif weather_tuple[2] == "overcast-and-light-snow":
        weather_icon = Image.open(weather_icons+"overcast-and-light-snow.png")
    else:
        weather_icon = Image.open(weather_icons+"unknown.png")
    copy_im.paste(weather_icon, (from_left_x, coordinates[0],), weather_icon)
    return copy_im

def sky_status(sky_tuple):
    '''
    :param sky_tuple:
    :param coordinates:
    :return:
    '''
    sun_on = sky_tuple[0]
    sun_on_x = 510
    sun_on_y = 790
    sun_off = sky_tuple[1]
    sun_off_x = 1010
    sun_off_y = 790
    moon_on = sky_tuple[2]
    moon_on_x = 510
    moon_on_y = 875
    moon_off = sky_tuple[3]
    moon_off_x = 1010
    moon_off_y = 875
    moon_phase = sky_tuple[4]
    moon_phase_x = 510
    moon_phase_y = 965
    moon_phase_icon_x = 550
    moon_phase_y_icon = 945
    copyright_x = 840
    copyright_y = 970
    copyright_txt = "\"Weather Bot\" made by trianglesis\non python3 and pillow"

    draw.text((sun_on_x, sun_on_y), sun_on, fill='white', font=font_status)
    draw.text((sun_off_x, sun_off_y), sun_off, fill='white', font=font_status)
    draw.text((moon_on_x, moon_on_y), moon_on, fill='white', font=font_status)
    draw.text((moon_off_x, moon_off_y), moon_off, fill='white', font=font_status)
    draw.text((moon_phase_x, moon_phase_y), moon_phase, fill='white', font=font_status)
    draw.text((copyright_x, copyright_y), copyright_txt, fill='white', font=font_copyright)

    # http://home.hiwaay.net/~krcool/Astro/moon/moonphase/
    if sky_tuple[4] == "1":
        moon_icon = Image.open(weather_icons+"moon_1.png")
    elif sky_tuple[4] == "2":
        moon_icon = Image.open(weather_icons+"moon_2.png")
    elif sky_tuple[4] == "3":
        moon_icon = Image.open(weather_icons+"moon_3.png")
    elif sky_tuple[4] == "4":
        moon_icon = Image.open(weather_icons+"moon_4.png")
    elif sky_tuple[4] == "5":
        moon_icon = Image.open(weather_icons+"moon_5.png")
    elif sky_tuple[4] == "6":
        moon_icon = Image.open(weather_icons+"moon_6.png")
    elif sky_tuple[4] == "7":
        moon_icon = Image.open(weather_icons+"moon_7.png")
    elif sky_tuple[4] == "8":
        moon_icon = Image.open(weather_icons+"moon_8.png")
    elif sky_tuple[4] == "9":
        moon_icon = Image.open(weather_icons+"moon_1.png")
    elif sky_tuple[4] == "10":
        moon_icon = Image.open(weather_icons+"moon_2.png")
    elif sky_tuple[4] == "11":
        moon_icon = Image.open(weather_icons+"moon_3.png")
    elif sky_tuple[4] == "12":
        moon_icon = Image.open(weather_icons+"moon_4.png")
    elif sky_tuple[4] == "13":
        moon_icon = Image.open(weather_icons+"moon_5.png")
    elif sky_tuple[4] == "14":
        moon_icon = Image.open(weather_icons+"moon_6.png")
    elif sky_tuple[4] == "15":
        moon_icon = Image.open(weather_icons+"moon_7.png")
    elif sky_tuple[4] == "16":
        moon_icon = Image.open(weather_icons+"moon_8.png")
    else:
        moon_icon = Image.open(weather_icons+"moon_else.png")
    copy_im.paste(moon_icon, (moon_phase_icon_x, moon_phase_y_icon), moon_icon)

    return copy_im

def weather_for_day_part(date,day_part):
    weather_condition = xmldoc.xpath('//forecast/day/day_part[@typeid="'+str(day_part)+'"]/weather_condition/@code')
    temperature_from = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/temperature_from/text()')
    temperature_to = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/temperature_to/text()')
    temperature_current = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/temperature/text()')
    weather_type_ua = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/weather_type_ua/text()')
    wind_direction = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/wind_direction/text()')
    wind_speed = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/wind_speed/text()')
    humidity = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/humidity/text()')
    pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/pressure/text()')
    mslp_pressure = xmldoc.xpath('//forecast/day[@date="' + date + '"]/day_part[@typeid="'+str(day_part)+'"]/mslp_pressure/text()')
    if not temperature_from:
        temperature_from = temperature_current
        temperature_to = temperature_current
    return (temperature_from[0],temperature_to[0],weather_condition[0],weather_type_ua[0],wind_direction[0],
            wind_speed[0],humidity[0],pressure[0],mslp_pressure[0])

def msg_for_all_vk (day,forecast):
    msg_vk = (day +", &#128201; {0}° &#128200; {1}°. Загальний стан - {3}.\n"
               "Напрямок вітру - {4}, швидкість - {5} м\\с, відносна вологість повітря - {6}%. \n"
               "Тиск - {8} гПа або {7} мм рт. ст.".format(*forecast))
    return msg_vk

def msg_for_all_fb (day,forecast):
    msg_fb = (day + " {0}° -> {1}°. Загальний стан - {3}.\n"
                  "Напрямок вітру - {4}, швидкість - {5} м\\с, відносна вологість повітря - {6}%. \n"
                  "Тиск - {8} гПа або {7} мм рт. ст.".format(*forecast))
    return msg_fb

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
    print("Yandex xml found - parsing")
    weather_condition = xmldoc.xpath('//forecast/fact/weather_condition/@code')
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
              " current: "
              + weather_condition[0] +
              "| morning: "
              + weather_condition_morning +
              "| daily: "
              + weather_condition_day +
              "| evening: "
              + weather_condition_evening +
              "| night: "
              + weather_condition_night)
    else:
        print("weather_condition is not available")

    # Extracting weather data for current time
    observation_time = (xmldoc.xpath('//forecast/fact/observation_time/text()'))
    uptime = xmldoc.xpath('//forecast/fact/uptime/text()')
    uptime = (uptime[0].replace("T"," "))
    weather_type_ua = xmldoc.xpath('//forecast/fact/weather_type_ua/text()')

    temperature_from = xmldoc.xpath('//forecast/fact/temperature/text()')
    temperature_to = xmldoc.xpath('//forecast/fact/temperature/text()')
    temperature_current = xmldoc.xpath('//forecast/fact/temperature/text()')
    if not temperature_from:
        temperature_from = temperature_current
        temperature_to = temperature_current
    wind_direction = xmldoc.xpath('//forecast/fact/wind_direction/text()')
    wind_speed = xmldoc.xpath('//forecast/fact/wind_speed/text()')
    humidity = xmldoc.xpath('//forecast/fact/humidity/text()')
    pressure = xmldoc.xpath('//forecast/fact/pressure/text()')
    mslp_pressure = xmldoc.xpath('//forecast/fact/mslp_pressure/text()')
    current_tuple = (temperature_from[0],temperature_to[0],weather_condition[0],weather_type_ua[0],wind_direction[0],
                wind_speed[0],humidity[0],pressure[0],mslp_pressure[0])

    if observation_time:
        print("Time is " + str(observation_time) + " will parse xml further")
    else:
        print("parsing interrupted on line 72")

    current_msg = ("Погода станом на {0}\nЗараз на вулиці {1}. \n"
                   "Напрямок вітру - {2}, швидкість - {3} м\\с. \n"
                   "Відносна вологість повітря - {4}%, \n"
                   "Тиск - {5} гПа або - {6} мм рт. ст.".format(uptime,
                                                                weather_type_ua[0],
                                                                wind_direction[0],
                                                                wind_speed[0],
                                                                humidity[0],
                                                                mslp_pressure[0],
                                                                pressure[0]))

    current_msg_fb = ("Погода станом на {0}\nЗараз на вулиці {1} . \n"
                      "Напрямок вітру - {2}, швидкість - {3} м\\с. \n"
                      "Відносна вологість повітря - {4}%, \n"
                      "Тиск - {5} гПа або - {6} мм рт. ст.".format(uptime,
                                                                   weather_type_ua[0],
                                                                   wind_direction[0],
                                                                   wind_speed[0],
                                                                   humidity[0],
                                                                   mslp_pressure[0],
                                                                   pressure[0]))

    # Extracting forecast for current date with details till day ends
    sunrise = xmldoc.xpath('//forecast/day[@date="' + date + '"]/sunrise/text()')
    sunset = xmldoc.xpath('//forecast/day[@date="' + date + '"]/sunset/text()')
    moon_phase = xmldoc.xpath('//forecast/day[@date="' + date + '"]/moon_phase/text()')
    moonrise = xmldoc.xpath('//forecast/day[@date="' + date + '"]/moonrise/text()')
    moonset = xmldoc.xpath('//forecast/day[@date="' + date + '"]/moonset/text()')

    sky_tuple = (sunrise[0],sunset[0],moonrise[0],moonset[0],moon_phase[0])
    sky_status(sky_tuple)
    print(sky_tuple)

    if sunrise is not None:
        print("Solar is " + str(sunrise) + " will parse xml further")
    else:
        print("parsing interrupted on line 180")

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
                  "Місяць знаходиться у {4}й фазі {5}.".format(sunrise[0],
                                                               sunset[0],
                                                               moonrise[0],
                                                               moonset[0],
                                                               moon_phase[0],
                                                               moon_emoji))
    phases_msg_fb = ("Сонце зійде о {0} год, захід сонця о {1} год. \n"
                     "Місяць вийде о {2} год, заховається о {3} год. \n"
                     "Місяць знаходиться у {4}й фазі.".format(sunrise[0],
                                                                  sunset[0],
                                                                  moonrise[0],
                                                                  moonset[0],
                                                                  moon_phase[0]))

    # CURRENT
    weather_pictures(current_tuple,current_coordinates)
    # print(str(current_tuple))
    # MORNING
    morning_forecast = (weather_for_day_part(date,1))
    morning_msg = (msg_for_all_vk("Зранку", morning_forecast))
    morning_msg_fb = (msg_for_all_fb("Зранку", morning_forecast))
    weather_pictures(morning_forecast,morning_coordinates)
    # DAY
    day_forecast = (weather_for_day_part(date,2))
    day_msg = (msg_for_all_vk("У день", day_forecast))
    day_msg_fb = (msg_for_all_fb("У день", day_forecast))
    weather_pictures(day_forecast,day_coordinates)
    # EVENING
    evening_forecast = (weather_for_day_part(date,3))
    evening_msg = (msg_for_all_vk("Ввечері", evening_forecast))
    evening_msg_fb = (msg_for_all_fb("Ввечері", evening_forecast))
    weather_pictures(evening_forecast,evening_coordinates)
    # NIGHT
    night_forecast = (weather_for_day_part(date,4))
    night_msg = (msg_for_all_vk("Вночі", night_forecast))
    night_msg_fb = (msg_for_all_fb("Вночі", night_forecast))
    weather_pictures(night_forecast,night_coordinates)

    # Vk message format:
    vk_disclaimer = "Пропонуйте ваші варіанти музичних композицій до варіантів прогнозів, ваші варіанти додавайте в коментарі! \n" \
                    "\n\n #ВождьБот Powered by #Python made by #trianglesis"
    vk_tags = "#weather@typical_kirovohrad, #weather, #forecast, #weatherbot, #forecastbot, #kirovohrad, #kirovograd, #кировоград, #кіровоград, #ПогодавКировограде, #КировоградПогода"
    fb_tags = "#weather, #forecast, #weatherbot, #forecastbot, #kirovohrad, #kirovograd, #кировоград, #кіровоград, #ПогодавКировограде, #КировоградПогода" \
              "\n\n#ВождьБот Powered by #Python made by #trianglesis"

    forecast_vk_format = (
        current_msg + "\n\n"
        + morning_msg + "\n\n"
        + day_msg + "\n\n"
        + evening_msg + "\n\n"
        + night_msg + "\n\n"
        + phases_msg + "\n\n"
        + vk_disclaimer + "\n\n"
        + vk_tags + "\n\n")

    forecast_fb_format = (
        current_msg_fb + "\n\n"
        + morning_msg_fb + "\n\n"
        + day_msg_fb + "\n\n"
        + evening_msg_fb + "\n\n"
        + night_msg_fb + "\n\n"
        + phases_msg_fb + "\n\n"
        + fb_tags + "\n\n")

    # Making list of different music tracks for different weather conditions
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

    weather_condition = weather_condition[0]
    if weather_condition == "clear":
        vk_audio = vk_audio_clear
    elif weather_condition == "partly-cloudy":
        vk_audio = vk_audio_p_cloudy
    elif weather_condition == "cloudy":
        vk_audio = vk_audio_cloudy
    elif weather_condition == "overcast":
        vk_audio = vk_audio_overcast
    elif weather_condition == "cloudy-and-rain":
        vk_audio = vk_audio_cloudy_rain
    elif weather_condition == "overcast-and-rain":
        vk_audio = vk_audio_overcast_rain
    elif weather_condition == "overcast-thunderstorms-with-rain":
        vk_audio = vk_audio_overcast_thund_rain
    elif weather_condition == "overcast-and-light-rain":
        vk_audio = vk_audio_overcast_light_rain
    elif weather_condition_morning == "overcast-and-snow":
        vk_audio = vk_audio_overcast_and_snow
    elif weather_condition_morning == "overcast-and-light-snow":
        vk_audio = vk_audio_overcast_and_light_snow
    else:
        vk_audio = vk_audio_other

    vk_audio_lst = random.sample(set(vk_audio), 3)
    vk_audio_str = ','.join(vk_audio_lst)
    # print(vk_audio_str)

    copy_im.save("weather_ready.png")
    weather_pic = ("weather_ready.png")
    weather_pic_open = Image.open("weather_ready.png")

    # VKONTAKTE
    token = 'TOKEN'
    vkapi = vk.API(access_token=token)

    typical_kirovohrad_id = "46631810"
    typical_kirovohrad = "-46631810"
    #debug
    typical_kirovohrad_boss = "13147598"
    group_id = "75140438"
    owner_id = "-75140438"
    user_id = "13147598"
    #FACEBOOK
    # Expiration Time NEVER
    fb_access_token_TypicalKirovohrad = \
        'TOKEN'
    graph = facebook.GraphAPI(access_token='fb_access_token_TypicalKirovohrad', version='2.2')

    photo_id = ""
    request_server = requests.post('https://api.vk.com/method/photos.getWallUploadServer?group_id='+typical_kirovohrad_id+'&access_token='+token)
    if request_server:
        response_data = request_server.json()
        upload_url = response_data['response']['upload_url']
        post_pic = requests.post(upload_url, files={'photo': open(weather_pic,"rb")})
        response_pic = post_pic.json()
        server = str(response_pic['server'])
        photo = str(response_pic['photo'])
        hash_str = str(response_pic['hash'])
        wallphoto = requests.post('https://api.vk.com/method/photos.saveWallPhoto?group_id='
                                  +typical_kirovohrad_id+'&photo='+photo+'&server='+server+'&hash='+hash_str+'&access_token='+token)
        response_wallphoto = wallphoto.json()
        resp = response_wallphoto['response'][0]
        photo_id = resp['id']
        print("Weather pic has been created and uploaded: "+photo_id)
    else:
        print("No response")

    # POST on VK Wall
    vk_attachment = vk_audio_str+","+photo_id
    wall_post = vkapi('wall.post',
                      owner_id=post_to,
                      from_group='1',
                      message=forecast_vk_format,
                      attachments=vk_attachment,
                      signed='0')
    print("Message has been posted to VK!\n")

    # # Post on FB public Page
    if debug == 0:
        url = 'https://graph.facebook.com/318878038180954/photos?access_token='+str(fb_access_token_TypicalKirovohrad)
        flag = requests.post(url, files={'file':open(weather_pic,'rb')}).text
    else:
        pass

    # print(forecast_vk_format)
    # print(forecast_fb_format)
    # print("Messages has been posted!")
else:
    print("Weather xml is not available")