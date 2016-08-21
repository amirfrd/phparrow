#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import util
import sys
import json
import os
import random
import wikipedia
import base64
import urllib
import urllib2
import redis
import requests as req
reload(sys)
wikipedia.set_lang("fa")
sys.setdefaultencoding("utf-8")

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)
is_sudo = 'ADMIN ID'
rediss = redis.StrictRedis(host='localhost', port=6379, db=0)

@bot.message_handler(commands=['start'])
def start(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        ids = m.chat.id
        bot.send_message(m.chat.id, '\xF0\x9F\x98\x85 ok welcome send /help')
        rediss.sadd('member', '{}'.format(m.from_user.id))
    if str(banlist) == 'True':
        bot.send_message(m.chat.id, 'You Are Banned')

@bot.message_handler(commands=['help'])
def welcome(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        print 'Send /help'
        rediss.sadd('member', '{}'.format(m.from_user.id))
        bot.send_chat_action(m.chat.id, 'typing')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Next \xE2\x96\xB6\xEF\xB8\x8F', callback_data='next'))
        markup.add(types.InlineKeyboardButton('Inline \xF0\x9F\x93\x9D', switch_inline_query=''))
        bot.send_message(m.chat.id,
        """
<i>Hello Welcome
arrow bot Fun Telegram bot</i>
commands list :
<code>
/arrow
/help
/ping
/echo [Text]  (Support Markdown *bold* _italic_ `code`)
/time     (Get Time Iran)
/dog [text]  (fun dogify)
/qr [text]    (Qr code)
/pic        (Get Random wallpaper)
/wallpaper    (Get Random wallpaper hd)
/calc [text]   (Calc)
/calc [2*2]
/sticker [text]    (Text To sticker)
/food           (Send food sticker)
/tr [text]      (Google translate)
/voice [text]      (Text to voice)
/webshot [url]
/info             (Send Your Info)
/bold [text]      (Your Text to bold)
/italic [text]    (Your Text to italic)
/mean [text]      (Mean Your Text (persian))
/ip [url,ip]
/github [username][repo]   ( Get info github)
/git [username]      (github search username)
/logo [url]          (Get Logo website)
/imdb [name]      (Get Film / Movie)
/cap            (Caption file)
/whois [domain name]       (whois)
/wiki [text]      (wikipedia)
/tophoto        (Sticker To photo by reply)
/tosticker      (Photo To Sticker By reply)
/map [City]     (Map screen)
/code base64 [text]
/decode base64 [text]
/news             (Get Iran News)
/spotify [Name Track]     (Get mp4)
/loc [City]      (send location)
/weather [City]
/arz            (Arz And tala)
/short [url]    (shorten link)
/sc [url soundcloud]       (Download Music sound cloud)
</code>

forward mode :
forward msg to private Me


<b>inline mode</b> :
<code>@Arrow_robot</code>
<b>Menu Inline</b>


\xD8\xAE\xD9\x88\xD8\xB4\x20\xD8\xA7\xD9\x85\xD8\xAF\xDB\x8C\xD8\xAF

برای دریافت راهنمای فارسی بنویس
/helpfa
سازنده
@negative
        """, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['helpfa'])
def helpfa(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        print 'Send /helpfa'
        text = """
دستورات :
/arrow
معرفی
/help
دستور راهنما
/ping
دستور انلاین بودن ربات
/echo [متن]
اکو یک متن
/time
دریافت ساعت ایران
/dog [متن]
نوشتن متن شما روی عکس سگ
/qr [متن]
تبدیل متن شما به کد کی ار
/pic
ارسال عکس تصادفی
/wallpaper
ارسال والپیپر تصادفی
/calc [معادله]
ماشین حساب
/sticker [متن]
ارسال متن استیکر
/food
ارسال استیکر غذا
/tr [متن]
ترجمه متن از انگلیسی به فارسی
/voice [متن]
تبدیل متن شما به صدا
/webshot [ادرس سایت]
اسکرین شات از ادرس سایت
/info
دریافت مشخصات شما
/bold [متن]
پررنگ نویسی متن شما
/italic [متن]
نوشتن متن شما با فونت شکسته
/mean [متن]
معنی کلمه
/ip [ادرس سایت]
دریافت ایپی ادرس سایت
/github [نام سورس]
دریافت مشخصات سورس در گیت هاب
/git [یوزر نیم]
دریافت مشخصات یک کاربر در گیت هاب
/logo [ادرس سایت]
دریافت لوگو ادرس سایت
/imdb [نام فیلم]
دریافت مشخصات فیلم
/cap
درج زیرنویس بر روی فایل
/whois [ادرس سایت]
دریافت مشخصات ادرس دامنه
/wiki [متن]
سرچ کردن یک متن در ویکی پدیا
/tophoto (ریپلی)
تبدیل استیکر به عکس
/tosticker (ریپلی)
تبدیل عکس به استیکر
/code base64 [متن]
تبدیل متن به کد
/decode base64 [متن]
تبدیل کد به متن
/news
دریافت اخبار فارسی
/spotify [نام اهنگ]
دریافت اهنگ
/loc [شهر]
دریافت نقشه
/map [شهر]
دریافت عکس نقشه یک شهر
/weather [نام شهر]
دریافت اب و هوای شهر
/arz
دریافت قیمت روز ارز
/short [ادرس سایت]
کوتاه کننده لینک
/sc [لینک ساد کلاد]
دریافت اهنگ از ساند کلاد

        """
        bot.send_message(m.chat.id, text)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "next":
            markup = types.InlineKeyboardMarkup()
            arrow = types.InlineKeyboardButton('Arrow\xE2\xAD\x95\xEF\xB8\x8F', callback_data='send_arrow')
            helpp = types.InlineKeyboardButton('Help\xE2\xAD\x95\xEF\xB8\x8F', callback_data='send_help')
            admin = types.InlineKeyboardButton('Admin arrow\xE2\x9A\xA0\xEF\xB8\x8F', callback_data="admin")
            back = types.InlineKeyboardButton('\xE2\x97\x80\xEF\xB8\x8FBack', callback_data='back')
            markup.add(arrow, helpp)
            markup.add(admin)
            markup.add(back)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="commands : list", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Next!")
    if call.message:
        if call.data == "send_arrow":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('\xE2\x97\x80\xEF\xB8\x8FBack', callback_data='next2'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="/arrow", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Commands : \n /arrow")
    if call.message:
        if call.data == "send_help":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('\xE2\x97\x80\xEF\xB8\x8FBack', callback_data='next2'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="/help", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Commands : \n /help")
    if call.message:
        if call.data == "admin":
            markupp = types.InlineKeyboardMarkup()
            markupp.add(types.InlineKeyboardButton('\xF0\x9F\x94\xB0Negative\xF0\x9F\x94\xB0', url='https://telegram.me/negative_officiall'))
            markupp.add(types.InlineKeyboardButton('\xE2\x97\x80\xEF\xB8\x8FBack', callback_data='next2'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Admins list \xF0\x9F\x94\xB1", reply_markup=markupp)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Admin Arrow Bot")
    if call.message:
        if call.data == "next2":
            markup = types.InlineKeyboardMarkup()
            arrow = types.InlineKeyboardButton('Arrow\xE2\xAD\x95\xEF\xB8\x8F', callback_data='send_arrow')
            helpp = types.InlineKeyboardButton('Help\xE2\xAD\x95\xEF\xB8\x8F', callback_data='send_help')
            admin = types.InlineKeyboardButton('Admin arrow\xE2\x9A\xA0\xEF\xB8\x8F', callback_data="admin")
            back = types.InlineKeyboardButton('\xE2\x97\x80\xEF\xB8\x8FBack', callback_data='back')
            markup.add(arrow, helpp)
            markup.add(admin)
            markup.add(back)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="commands : list", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Welcome Main Menu")
    if call.message:
        if call.data == 'more':
            markup = types.InlineKeyboardMarkup()
            wl = types.InlineKeyboardButton('Wallpaper \xE2\x9A\xA0\xEF\xB8\x8F', callback_data='send_wallpaper')
            time = types.InlineKeyboardButton('Time \xE2\x9A\xA0\xEF\xB8\x8F', callback_data='send_time')
            food = types.InlineKeyboardButton('Food \xE2\x9A\xA0\xEF\xB8\x8F', callback_data='send_food')
            back = types.InlineKeyboardButton('\xF0\x9F\x94\x99Back', callback_data='next2')
            markup.add(wl, food)
            markup.add(time)
            markup.add(back)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Welcome More Menu', reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="More Menu")
    if call.message:
        if call.data == 'send_wallpaper':
            urllib.urlretrieve("https://source.unsplash.com/1600x900", "wallpaper.jpg")
            bot.send_photo(call.message.chat.id, open('wallpaper.jpg'))
    if call.message:
        if call.data == 'send_time':
            url = "http://api.gpmod.ir/time/"
            response = urllib.urlopen(url)
            data = response.read()
            parsed_json = json.loads(data)
            ENtime = (parsed_json['ENtime'])
            bot.send_message(call.message.chat.id, '{}'.format(ENtime))
    if call.inline_message_id:
        if call.data == '!timee':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Back', callback_data='!backkk'))
            url = "http://api.gpmod.ir/time/"
            response = urllib.urlopen(url)
            data = response.read()
            parsed_json = json.loads(data)
            ENtime = (parsed_json['ENtime'])
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Time : {}".format(ENtime), reply_markup=markup)
    if call.inline_message_id:
        if call.data == '!backkk':
            markupp = types.InlineKeyboardMarkup()
            timee = types.InlineKeyboardButton('Time\xE2\x9A\xA0', callback_data='!timee')
            markupp.add(timee)
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Fun list \n Update #Soon", reply_markup=markupp)
    if call.message:
        if call.data == 'send_food':
            urllib.urlretrieve("https://source.unsplash.com/category/food", "food.jpg")
            bot.send_sticker(call.message.chat.id, open('food.jpg'))
    if call.message:
        if call.data == '!admins':
            bot.send_message(call.message.chat.id, 'Channel : @taylor_team')
            bot.send_message(call.message.chat.id, 'Admin : @Negative_officiall')
            bot.send_message(call.message.chat.id, 'github : https://github.com/taylor-team')
    if call.message:
        if call.data == "back":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Next \xE2\x96\xB6\xEF\xB8\x8F', callback_data='next'))
            markup.add(types.InlineKeyboardButton('Inline \xF0\x9F\x93\x9D', switch_inline_query=''))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
<i>Hello Welcome
arrow bot Fun Telegram bot</i>
commands list :
<code>
/arrow
/help
/ping
/echo [Text]  (Support Markdown *bold* _italic_ `code`)
/time     (Get Time Iran)
/dog [text]  (fun dogify)
/qr [text]    (Qr code)
/pic        (Get Random wallpaper)
/wallpaper    (Get Random wallpaper hd)
/calc [text]   (Calc)
/calc [2*2]
/sticker [text]    (Text To sticker)
/food           (Send food sticker)
/tr [text]      (Google translate)
/voice [text]      (Text to voice)
/webshot [url]
/info             (Send Your Info)
/bold [text]      (Your Text to bold)
/italic [text]    (Your Text to italic)
/mean [text]      (Mean Your Text (persian))
/ip [url,ip]
/github [username][repo]   ( Get info github)
/git [username]      (github search username)
/logo [url]          (Get Logo website)
/imdb [name]      (Get Film / Movie)
/cap            (Caption file)
/whois [domain name]       (whois)
/wiki [text]      (wikipedia)
/tophoto        (Sticker To photo by reply)
/tosticker      (Photo To Sticker By reply)
/map [City]     (Map screen)
/code base64 [text]
/decode base64 [text]
/news             (Get Iran News)
/spotify [Name Track]     (Get mp4)
/loc [City]      (send location)
/weather [City]
/arz            (Arz And tala)
/short [url]    (shorten link)
/sc [url soundcloud]       (Download Music sound cloud)
</code>

forward mode :
forward msg to private Me


<b>inline mode</b> :
<code>@Arrow_robot</code>
<b>Menu Inline</b>


\xD8\xAE\xD9\x88\xD8\xB4\x20\xD8\xA7\xD9\x85\xD8\xAF\xDB\x8C\xD8\xAF

برای دریافت راهنمای فارسی بنویس
/helpfa
سازنده
@negative
            """, parse_mode='HTML', reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Backed!")
            return

@bot.message_handler(commands=['send'])
def gif(m):
    idd = m.from_user.id
    if str(idd) not in is_sudo:
        bot.send_message(m.chat.id, 'Just Sudo @negative_officiall')
        return
    if str(m.from_user.id) == is_sudo:
        taylor_team = '@taylor_team'
        text = m.text.replace('/send', '')
        bot.send_message(taylor_team, '{}'.format(text), parse_mode="Markdown")
        bot.send_message(is_sudo, 'ok')

@bot.message_handler(commands=['weather'])
def wt(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            icons = {'01d': '🌞',
             '01n': '🌚',
             '02d': '⛅️',
             '02n': '⛅️',
             '03d': '☁️',
             '03n': '☁️',
             '04d': '☁️',
             '04n': '☁️',
             '09d': '🌧',
             '09n': '🌧',
             '10d': '🌦',
             '10n': '🌦',
             '11d': '🌩',
             '11n': '🌩',
             '13d': '🌨',
             '13n': '🌨',
             '50d': '🌫',
             '50n': '🌫',
             }
            icons_file = {
            '01d': '01d',
            '01n': '01n',
            '02d': '02d',
            '02n': '02n',
            '03d': '03d',
            '03n': '03n',
            '04d': '04d',
            '04n': '04n',
            '09d': '09d',
            '09n': '09n',
            '10d': '10d',
            '10n': '10n',
            '11d': '11d',
            '11n': '11n',
            '13d': '13d',
            '13n': '13n',
            '50d': '50d',
            '50n': '50n',
            }
            text = m.text.split(' ',1)[1]
            url = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q={}&appid=269ed82391822cc692c9afd59f4aabba'.format(text))
            d = url.read()
            data = json.loads(d)
            wt = data['main']['temp']
            feshar = data['main']['pressure']
            wind = data['wind']['speed']
            icon = data['weather'][0]['icon']
            texttt = icons[icon]
            wt_data = int(wt)-273.15
            bot.send_message(m.chat.id, '\xD8\xAF\xD9\x85\xD8\xA7 : {}\n\n\xD8\xB3\xD8\xB1\xD8\xB9\xD8\xAA\x20\xD8\xA8\xD8\xA7\xD8\xAF : {}/s\n\n\xD9\x81\xD8\xB4\xD8\xA7\xD8\xB1\x20\xD9\x87\xD9\x88\xD8\xA7 : {}\n\n {}'.format(wt_data,wind,feshar,texttt))
            texty = icons_file[icon]
            files = open('./weather/'+texty+'.png')
            bot.send_sticker(m.chat.id, files)
        except (IndexError):
            bot.send_message(m.chat.id, 'Error\n/weather tehran')
        except IOError:
            print 'not send sticker weather'

@bot.message_handler(commands=['short'])
def short(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            text = m.text.split(' ',1)[1]
            url = urllib.urlopen('http://gs2.ir/api.php?url='+text)
            bot.send_message(m.chat.id, url.read())
        except IndexError:
            bot.send_message(m.chat.id, 'Error \n فرمت : \n /short [ادرس سایت]')

@bot.message_handler(commands=['save'])
def save(m):    
    try:
        if str(m.from_user.id) == is_sudo:
            if m.reply_to_message.document:
                f_id = m.reply_to_message.document.file_id
                f = bot.get_file(f_id)
                downloaded_file = bot.download_file(f.file_path)
                text = m.text.replace('save','')
                with open('{}'.format(text), 'wb') as new_file:
                    new_file.write(downloaded_file)
    except:
        bot.send_message(m.chat.id, 'Error')

@bot.message_handler(commands=['map'])
def map(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            text = m.text.split(" ", 1)[1]
            data = text.encode('utf-8')
            urllib.urlretrieve('https://maps.googleapis.com/maps/api/staticmap?center={}&zoom=14&size=400x400&maptype=hybrid&key=AIzaSyBmZVQKUXYXYVpY7l0b2fNso4z82H5tMvE'.format(data), 'map.png')
            bot.send_sticker(m.chat.id, open('map.png'))
            os.remove('map.png')
        except IndexError:
            bot.send_message(m.chat.id, '<b>Error</b>',parse_mode='HTML')

@bot.message_handler(commands=['arz'])
def arz(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        url = urllib.urlopen('http://exchange.nalbandan.com/api.php?action=json')
        data = url.read()
        js = json.loads(data)
        dollar = js['dollar']['value']
        euro = js['euro']['value']
        gold_per_geram = js['gold_per_geram']['value']
        pond = js['pond']['value']
        text = '\xD8\xAF\xD9\x84\xD8\xA7\xD8\xB1 : '+dollar+'\n\xDB\x8C\xD9\x88\xD8\xB1\xD9\x88 : '+euro+'\n\xD8\xB7\xD9\x84\xD8\xA7\xDB\x8C\x20\x31\x38\x20\xD8\xB9\xDB\x8C\xD8\xA7\xD8\xB1 : '+gold_per_geram+'\n\xD9\xBE\xD9\x88\xD9\x86\xD8\xAF : '+pond
        bot.send_message(m.chat.id, text)

#@bot.message_handler(commands=['aparat'])
#def aparat(m):
    #text = m.text.split(' ',1)[1]
    #url = urllib.urlopen('http://www.aparat.com/etc/api/videoBySearch/text/'+text)
    #data = url.read()
    #js = json.loads(data)
    #title1 = js['videobysearch'][0]['title']
    #poster1 = js['videobysearch'][0]['big_poster']
    #uid1 = js['videobysearch'][0]['uid']
    #urllib.urlretrieve(poster1,'poster.png')
    #bot.send_photo(m.chat.id, open('poster.png'), caption='Title : '+title1+'\nLink : http://www.aparat.com/v/'+uid1)
    #os.remove('poster.png')

@bot.message_handler(commands=['spotify'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            url = urllib.urlopen("https://api.spotify.com/v1/search?limit=1&type=track&q={}".format(m.text.replace('/spotify','')))
            data = url.read()
            js = json.loads(data)
            files = js['tracks']['items'][0]['preview_url']
            name = js['tracks']['items'][0]['name']
            pic = js['tracks']['items'][0]['album']['images'][1]['url']
            art = js['tracks']['items'][0]['artists'][0]['name']
            bot.send_message(m.chat.id, '<b>Name</b> : {}\n<b>Artist : </b>{}'.format(name,art),parse_mode='HTML')
            bot.send_chat_action(m.chat.id, 'record_audio')
            urllib.urlretrieve(files,'spotify.mp3')
            urllib.urlretrieve(pic,'spotify.png')
            bot.send_audio(m.chat.id, open('spotify.mp3'), title=name)
            bot.send_sticker(m.chat.id, open('spotify.png'))
            hash = 'spotify'
            now = rediss.get(hash)
            new = int(now) + 1
            rediss.set(hash,new)
            os.remove('spotify.mp3')
            os.remove('spotify.png')
            print ' send /spotify'
        except KeyError:
            bot.send_message(m.chat.id, 'Error')
        except IndexError:
            bot.send_message(m.chat.id, 'Error')
        except IOError:
            bot.send_message(m.chat.id, 'Error')

@bot.message_handler(commands=['sc'])
def s(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            text = m.text.split(' ',1)[1]
            url = urllib.urlopen('http://api.soundcloud.com/resolve?url={}&client_id=68e2dd5ffc581ee86f6e17f21637455a'.format(text))
            d = url.read()
            data = json.loads(d)
            tag_list = data['tag_list']
            title = data['title']
            stream_url = data['stream_url']
            urllib.urlretrieve('{}?client_id=68e2dd5ffc581ee86f6e17f21637455a'.format(stream_url),'soundcloud.mp3')
            bot.send_chat_action(m.chat.id, 'record_audio')
            bot.send_message(m.chat.id, 'Title : '+title+'\n\nTag list : '+tag_list)
            bot.send_audio(m.chat.id, open('soundcloud.mp3'), title=title)
            hash = 'music'
            now = rediss.get(hash)
            new = int(now) + 1
            rediss.set(hash,new)
            os.remove('soundcloud.mp3')
        except KeyError:
            bot.send_message(m.chat.id, 'Error')
        except IndexError:
            bot.send_message(m.chat.id, 'Error')

@bot.message_handler(commands=['news'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        url = urllib.urlopen('http://api.khabarfarsi.net/api/news/latest/1?tid=*&output=json')
        data = url.read()
        pa = json.loads(data)
        title = pa['items'][0]['title']
        link = pa['items'][0]['link']
        title2 = pa['items'][1]['title']
        link2 = pa['items'][1]['link']
        title3 = pa['items'][2]['title']
        link3 = pa['items'][2]['link']
        bot.send_message(m.chat.id, '<b>Title</b> : {}\n\n<b>Link</b> {}\n\n\n<b>Title</b> : {}\n\n<b>Link</b> : {}\n\n\n<b>Title</b> : {}\n\n<b>Link</b> : {}'.format(title,link,title2,link2,title3,link3), parse_mode='HTML')

#@bot.message_handler(regexp='^(/gif)')
#def gif(m):
    #r = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC')
    #json_data = r.json()
    #textx = json_data['data']['image_original_url']
    #urllib.urlretrieve("{}".format(textx), "gif.gif")
    #bot.send_document(m.chat.id, open('gif.gif'))

@bot.message_handler(regexp='^(/logo) (.*)')
def log(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if m.text.split()[1]:
            text = m.text.split()[1]
            urllib.urlretrieve("http://logo.clearbit.com/{}?size=500&".format(text), "logo.png")
            bot.send_sticker(m.chat.id, open('logo.png'))

@bot.message_handler(regexp='^(/setlink) (.*)')
def link(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if m.text.split()[1]:
            if m.chat.type == "group" or m.chat.type == "supergroup":
                text = m.text.split()[1]
                rediss.set('{}'.format(m.chat.id), '{}'.format(text))
                get = rediss.get('{}'.format(m.chat.id))
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Group link',url= '{}'.format(get)))
                bot.send_message(m.chat.id, '<b>Link :</b> {}'.format(get), parse_mode='HTML', reply_markup=markup)
            if m.chat.type == "private":
                bot.send_message(m.chat.id, 'Just group')
                return

@bot.message_handler(commands=['link'])
def linkget(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if m.chat.type == "group" or m.chat.type == "supergroup":
            get = rediss.get('{}'.format(m.chat.id))
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Group link',url= '{}'.format(get)))
            bot.send_message(m.chat.id, '<b>Link :</b> {}'.format(get), parse_mode='HTML', reply_markup=markup)
        if m.chat.type == "private":
            bot.send_message(m.chat.id, 'Just group')

@bot.inline_handler(lambda q: q.query)
def m(m):
    if m.query.split()[0] == 'wiki':
        try:
            text = m.query.replace('wiki','')
            ny = wikipedia.page("{}".format(text))
            title = ny.title
            url = ny.url
            textt = ny.content
            inline1 = types.InlineQueryResultArticle('1',title='Wiki : '+title+' \xF0\x9F\x9A\xA5',input_message_content=types.InputTextMessageContent('Title : '+title+'\n'+textt+'\nLink : <a href="{}">wiki Link</a>'.format(url), parse_mode='HTML'))
            bot.answer_inline_query(m.id, [inline1], cache_time=1)
        except wikipedia.exceptions.WikipediaException:
            inline1 = types.InlineQueryResultArticle('1','Error',types.InputTextMessageContent('Error'))
            bot.answer_inline_query(m.id, [inline1], cache_time=1)
    if m.query.split()[0] == 'bold':
        text = m.query.replace('bold','')
        news = types.InlineQueryResultArticle('1', 'Bold Your Text', description='Bold : '+text,input_message_content=types.InputTextMessageContent('<b>'+ text + '</b>',parse_mode='HTML'))
        bot.answer_inline_query(m.id, [news], cache_time=1)
    if m.query.split()[0] == 'italic':
        text = m.query.replace('italic','')
        it = types.InlineQueryResultArticle('1',title='Italic Your Text', description='Italic : '+text,input_message_content=types.InputTextMessageContent('<i>'+text+'</i>',parse_mode='HTML'))
        bot.answer_inline_query(m.id, [it], cache_time=1)
    if m.query.split()[0] == 'news':
        url = urllib.urlopen('http://api.khabarfarsi.net/api/news/latest/1?tid=*&output=json')
        data = url.read()
        pa = json.loads(data)
        title = pa['items'][0]['title']
        link = pa['items'][0]['link']
        title2 = pa['items'][1]['title']
        link2 = pa['items'][1]['link']
        title3 = pa['items'][2]['title']
        link3 = pa['items'][2]['link']
        markup = types.InlineKeyboardMarkup()
        li1 = types.InlineKeyboardButton('Link 1.',url=link)
        li2 = types.InlineKeyboardButton('Link 2.',url=link2)
        li3 = types.InlineKeyboardButton('Link 3.',url=link3)
        markup.add(li1)
        markup.add(li2)
        markup.add(li3)
        news = types.InlineQueryResultArticle('1',title='\xD8\xA7\xD8\xAE\xD8\xA8\xD8\xA7\xD8\xB1',input_message_content=types.InputTextMessageContent('\xD8\xA7\xD8\xAE\xD8\xB1\xDB\x8C\xD9\x86\x20\xD8\xA7\xD8\xAE\xD8\xA8\xD8\xA7\xD8\xB1\n1. :'+title+'\n\n2. :'+title2+'\n\n3. :'+title3), reply_markup=markup)
        bot.answer_inline_query(m.id, [news], cache_time=1)
    if m.query.split()[0] == '\xD9\x85\xD8\xB9\xD9\x86\xDB\x8C':
        try:
            text = m.query.replace('\xD9\x85\xD8\xB9\xD9\x86\xDB\x8C','')
            r = req.get('http://api.vajehyab.com/v2/public/?q={}'.format(text))
            json_data = r.json()
            textx = json_data['data']['text']
            s = types.InlineQueryResultArticle('1',title='\xD9\x85\xD8\xB9\xD9\x86\xDB\x8C : '+text,input_message_content=types.InputTextMessageContent(textx))
            bot.answer_inline_query(m.id, [s], cache_time=1)
        except KeyError:
            s = types.InlineQueryResultArticle('1',title='Error',input_message_content=types.InputTextMessageContent('Error'))
            bot.answer_inline_query(m.id, [s], cache_time=1)
    if m.query.split()[0] == 'imdb':
        try:
            text = m.query.replace('imdb','')
            r = urllib.urlopen('http://www.omdbapi.com/?t={}&'.format(text))
            data = r.read()
            pjson = json.loads(data)
            title = pjson['Title']
            year = pjson['Year']
            runtime = pjson['Runtime']
            genre = pjson['Genre']
            language = pjson['Language']
            poster = pjson['Poster']
            inline = types.InlineQueryResultPhoto('1',photo_url=poster,thumb_url=poster,caption='Title : '+title+'\nYear : '+year+'\nRuntime : '+runtime+'\nGenre : '+genre+'\nLanguage : '+language)
            bot.answer_inline_query(m.id, [inline], cache_time=1)
        except KeyError:
            inline = types.InlineQueryResultArticle('1','Error',types.InputTextMessageContent('Error IMDB'))
    if m.query.split()[0] == 'arrow':
        fileid = 'BQADBAADKAYAAqTB2Apq3oIp-bQXUgI'
        sticker = types.InlineQueryResultCachedSticker('1',sticker_file_id=fileid)
        gif_id = 'BQADBAAD2AIAAqTB2Aq63iOGp-8HyQI'
        gif = types.InlineQueryResultCachedGif('2',gif_file_id=gif_id,caption='Arrow Robot Fun\nDeveloper : @Negative')
        con = types.InlineQueryResultContact('3',phone_number='+98 937 909 7344',first_name='Negative')
        bot.answer_inline_query(m.id, [sticker, gif, con])
    if m.query.split()[0] == 'loc':
        try:
            text = m.query.replace('loc','')
            url = urllib.urlopen('http://maps.googleapis.com/maps/api/geocode/json?address={}'.format(text))
            data = url.read()
            js = json.loads(data)
            lat = js['results'][0]['geometry']['location']['lat']
            lng = js['results'][0]['geometry']['location']['lng']
            tmp = 'http://icons.iconarchive.com/icons/pixelkit/swanky-outlines/256/10-My-Location-icon.png'
            locc = types.InlineQueryResultLocation('1',latitude=lat,longitude=lng,title='location :'+text,thumb_url=tmp)
            bot.answer_inline_query(m.id,[locc],cache_time=1)
        except IndexError:
            s = types.InlineQueryResultArticle('1',title='Error',input_message_content=types.InputTextMessageContent('Error'))
            bot.answer_inline_query(m.id, [s], cache_time=1)
        except KeyError:
            s = types.InlineQueryResultArticle('1',title='Error',input_message_content=types.InputTextMessageContent('Error'))
            bot.answer_inline_query(m.id, [s], cache_time=1)
    if m.query.split()[0] == 'calc':
        try:
            text = m.query.replace('calc','')
            encodee = urllib.quote_plus(text)
            url = "http://api.mathjs.org/v1/?expr={}&".format(encodee)
            response = urllib.urlopen(url)
            data = response.read()
            tmp = 'http://icons.iconarchive.com/icons/dtafalonso/android-lollipop/256/Calculator-icon.png'
            calc = types.InlineQueryResultArticle('1',title=text+'='+data,input_message_content=types.InputTextMessageContent('Equation : '+text+'\nAnswer : \n<code>'+data+'</code>', parse_mode='HTML'), thumb_url=tmp)
            bot.answer_inline_query(m.id, [calc], cache_time=1)
        except (KeyError,IndexError):
            s = types.InlineQueryResultArticle('1',title='Error',input_message_content=types.InputTextMessageContent('Error'))
            bot.answer_inline_query(m.id, [s], cache_time=1)
    if m.query.split()[0] == 'time':
        url = "http://api.gpmod.ir/time/"
        response = urllib.urlopen(url)
        data = response.read()
        parsed_json = json.loads(data)
        ENtime = (parsed_json['ENtime'])
        ENdate = (parsed_json['ENdate'])
        tmp = 'http://icons.iconarchive.com/icons/icons8/ios7/512/Time-And-Date-Clock-icon.png'
        time = types.InlineQueryResultArticle('1', title='Time \xE2\x8F\xB1', input_message_content=types.InputTextMessageContent('Time : '+ENtime+'\nDate :'+ENdate), url='http://api.gpmod.ir/time/', hide_url=True, thumb_url=tmp)
        bot.answer_inline_query(m.id, [time], cache_time=1)
    if m.query.split()[0] == 'weather':
        try:
            text = m.query.replace('weather','')
            url = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q={}&appid=269ed82391822cc692c9afd59f4aabba'.format(text))
            d = url.read()
            data = json.loads(d)
            wt = data['main']['temp']
            feshar = data['main']['pressure']
            wind = data['wind']['speed']
            icon = data['weather'][0]['icon']
            wt_data = int(wt)-273.15
            tmp = 'http://openweathermap.org/img/w/{}.png'.format(icon)
            weather = types.InlineQueryResultArticle('1',title='weather '+text,input_message_content=types.InputTextMessageContent('C : {}\nWind Speed : {}\nAir pressure : {}'.format(wt_data,wind,feshar)),thumb_url=tmp)
            bot.answer_inline_query(m.id, [weather], cache_time=1)
        except (KeyError,IndexError):
            s = types.InlineQueryResultArticle('1',title='Error',input_message_content=types.InputTextMessageContent('Error'))
            bot.answer_inline_query(m.id, [s], cache_time=1)

@bot.inline_handler(lambda q: len(q.query) is 0)
def q(m):
    markuploc = types.InlineKeyboardMarkup()
    locm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='loc tehran')
    markuploc.add(locm)
    markupimdb = types.InlineKeyboardMarkup()
    imdbm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='imdb sniper')
    markupimdb.add(imdbm)
    markupwiki = types.InlineKeyboardMarkup()
    wikim = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='wiki [text]')
    markupwiki.add(wikim)
    markupbold = types.InlineKeyboardMarkup()
    boldm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='bold [text]')
    markupbold.add(boldm)
    markupitalic = types.InlineKeyboardMarkup()
    italicm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='italic [text]')
    markupitalic.add(italicm)
    markupnews = types.InlineKeyboardMarkup()
    newsm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='news')
    markupnews.add(newsm)
    markupmean = types.InlineKeyboardMarkup()
    meanm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='\xD9\x85\xD8\xB9\xD9\x86\xDB\x8C [text]')
    markupmean.add(meanm)
    markupcalc = types.InlineKeyboardMarkup()
    calcm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='calc 2+2')
    markupcalc.add(calcm)
    markuptime = types.InlineKeyboardMarkup()
    timem = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='time')
    markuptime.add(timem)
    markupweather = types.InlineKeyboardMarkup()
    weatherm = types.InlineKeyboardButton('switch inline \xE2\x9C\x85',switch_inline_query='weather tehran')
    markupweather.add(weatherm)
    loctmp = 'https://www.solarissport.com/skin/frontend/boilerplate/default/images/media/maps.png'
    loc = types.InlineQueryResultArticle('1',title='loc [name]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot loc [name]</b>', parse_mode='HTML'), reply_markup=markuploc, description='loc [name]', thumb_url=loctmp)
    imdbtmp = 'http://icons.iconarchive.com/icons/danleech/simple/512/imdb-icon.png'
    imdb = types.InlineQueryResultArticle('2',title='imdb [name movie]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot imdb [name movie]</b>', parse_mode='HTML'), reply_markup=markupimdb, description='imdb [name]', thumb_url=imdbtmp)
    wikitmp = 'https://image.freepik.com/free-icon/wikipedia-logotype_318-9923.jpg'
    wiki = types.InlineQueryResultArticle('3',title='wiki [name]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot wiki [text]</b>', parse_mode='HTML'), reply_markup=markupwiki, description='wiki [text]', thumb_url=wikitmp)
    boldtmp = 'https://image.freepik.com/free-icon/bold--b-in-rounded-square_318-9739.jpg'
    bold = types.InlineQueryResultArticle('4',title='bold [text]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot bold [text]</b>', parse_mode='HTML'),reply_markup=markupbold, description='bold [text]', thumb_url=boldtmp)
    italictmp = 'https://image.freepik.com/free-icon/italic-letter-style-interface-symbol_318-53607.png'
    italic = types.InlineQueryResultArticle('5',title='italic [text]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot italic [text]</b>',parse_mode='HTML'),reply_markup=markupitalic,description='italic [text]',thumb_url=italictmp)
    newstmp = 'http://seattlefreepress.org/wp-content/uploads/2015/11/In-the-news-icon.png'
    news = types.InlineQueryResultArticle('6',title='news',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot news</b>', parse_mode='HTML'),reply_markup=markupnews, description='news', thumb_url=newstmp)
    meantmp = 'http://appratech.net/uploads/posts/2015-03/1426246349_icon320x320.jpg'
    mean = types.InlineQueryResultArticle('7',title='\xD9\x85\xD8\xB9\xD9\x86\xDB\x8C [text]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot \xD9\x85\xD8\xB9\xD9\x86\xDB\x8C [text]</b>', parse_mode='HTML'),reply_markup=markupmean, description='\xD9\x85\xD8\xB9\xD9\x86\xDB\x8C [text]', thumb_url=meantmp)
    calctmp = 'http://icons.iconarchive.com/icons/dtafalonso/android-lollipop/256/Calculator-icon.png'
    calc = types.InlineQueryResultArticle('8',title='calc [Equation]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot calc [Equation]</b>', parse_mode='HTML'),reply_markup=markupcalc, description='calc [Equation]', thumb_url=calctmp)
    timetmp = 'http://icons.iconarchive.com/icons/icons8/ios7/512/Time-And-Date-Clock-icon.png'
    time = types.InlineQueryResultArticle('9',title='time',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot time</b>',parse_mode='HTML'),reply_markup=markuptime,description='time',thumb_url=timetmp)
    weathertmp = 'http://www.freeiconspng.com/uploads/weather-icon-13.png'
    weather = types.InlineQueryResultArticle('10',title='weather [City]',input_message_content=types.InputTextMessageContent('<b>@Arrow_robot weather [City]</b>',parse_mode='HTML'),reply_markup=markupweather,description='weather [City]',thumb_url=weathertmp)
    bot.answer_inline_query(m.id, [loc, imdb, wiki, bold, italic, news, mean, calc, time, weather])


@bot.message_handler(commands=['whois'])
def whois(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            cid = m.chat.id
            text = m.text
            input = text.split()[1]
            req = urllib2.Request("http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={}&outputFormat=JSON".format(input))
            opener = urllib2.build_opener()
            f = opener.open(req)
            parsed_json = json.loads(f.read())
            output = parsed_json['WhoisRecord']['rawText']
            bot.send_message(cid,output)
        except KeyError:
            bot.send_message(m.chat.id, 'Error')
        except IndexError:
            bot.send_message(m.chat.id, '/whois [Domain Name]')

@bot.message_handler(commands=['wiki'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            ny = wikipedia.page("{}".format(m.text.replace('/wiki','')))
            title = ny.title
            url = ny.url
            text = ny.content
            bot.send_message(m.chat.id, '<b>Title</b> : {}\n\n{}\n\nLink : {}'.format(title,text,url), parse_mode='HTML')
        except wikipedia.exceptions.WikipediaException:
            bot.send_message(m.chat.id, '<code>Error</code>', parse_mode='HTML')


@bot.message_handler(regexp='^(/github) (.*)')
def git(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.split()[1]
        r = req.get('https://api.github.com/repos/{}'.format(text))
        json_data = r.json()
        if 'id' in json_data:
            name = json_data['name']
            fullname = json_data['full_name']
            avatar = json_data['owner']['avatar_url']
            description = json_data['description']
            clone_url = json_data['clone_url']
            svn_url = json_data['svn_url']
            language = json_data['language']
            forks_count = json_data['forks']
            default_branch = json_data['default_branch']
            watchers = json_data['watchers']
            stargazers_count = json_data['stargazers_count']
            bot.send_message(m.chat.id, """
Name : <b>{}</b> \xC2\xA9

fullname : <b>{}</b> \xE2\x9A\xA1

description :
<i>{}</i>

Clone Url : <b>{}</b>

Url : <b>{}</b>

language : <code>{}</code>

Forks : <code>{}</code> \xF0\x9F\x92\xAC

Default Branch : <code>{}</code>

watchers : <code>{}</code>

Stars : <code>{}</code> \xE2\xAD\x90
        """.format(name,fullname,description,clone_url,svn_url,language,forks_count,default_branch,watchers,stargazers_count), parse_mode='HTML')
            urllib.urlretrieve("{}".format(avatar), "git.jpg")
            bot.send_sticker(m.chat.id, open('git.jpg'))
        if 'message' in json_data:
            bot.send_message(m.chat.id, 'Error \n /github [username][repo]\n')

@bot.message_handler(commands=['stats'])
def check(m):    
    idd = m.from_user.id
    if str(idd) not in is_sudo:
        bot.send_message(m.chat.id, 'Just Sudo @negative_officiall')
        return
    if str(m.from_user.id) == is_sudo:
        msm = rediss.scard('member')
        mesg = rediss.get('hash')
        music = rediss.get('music')
        spotify = rediss.get('spotify')
        bot.send_message(m.chat.id, 'Users : `{}`\n\n*messages* : {}\n\n*SoundCloud Send Music* : `{}`\n\n*Spotify Send Music* : `{}`'.format(msm,mesg,music,spotify), parse_mode='Markdown')

@bot.message_handler(regexp='^(/mean) (.*)')
def mean(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.split()[1]
        r = req.get('http://api.vajehyab.com/v2/public/?q={}'.format(text))
        json_data = r.json()
        textx = json_data['data']['text']
        bot.send_message(m.chat.id, textx)

@bot.message_handler(commands=['arrow'])
def arrow(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        bot.send_message(m.chat.id, """
Arrow Fun Telegram bot
Developer : @negative_officiall
Channel : @taylor_team
    """)
        bot.send_document(m.chat.id, open('shot_bow-and-arrow_01.gif'), caption='@Taylor_Team')

#@bot.message_handler(commands=['bc'])
#def bc(m):
#    if str(m.from_user.id) == is_sudo:
#        text = m.text.replace('/bc ','')
#        ids = rediss.smembers("member")
#        for id in ids:
    #        bot.send_message(id,text)
        #    print("Delevered to "+str(id))

@bot.message_handler(commands=['ban'])
def gb(m):
    if str(m.from_user.id) == is_sudo:
        if not m.reply_to_message:
            ban_id = m.text.split()[1]
            rediss.sadd('banlist_arrow','{}'.format(ban_id))
            bot.send_message(m.chat.id, '*Banned*', parse_mode='Markdown')
        if m.reply_to_message:
            ban_id = m.reply_to_message.from_user.id 
            rediss.sadd('banlist_arrow','{}'.format(ban_id))
            bot.send_message(m.chat.id, '*Banned*', parse_mode='Markdown')

@bot.message_handler(commands=['unban'])
def unban(m):
    if str(m.from_user.id) == is_sudo:
        if not m.reply_to_message:
            unban_id = m.text.split()[1]
            rediss.srem('banlist_arrow',unban_id)
            bot.send_message(m.chat.id, '*Unbanned*', parse_mode='Markdown')
        if m.reply_to_message:
            unban_id = m.reply_to_message.from_user.id 
            rediss.srem('banlist_arrow','{}'.format(unban_id))
            bot.send_message(m.chat.id, '*Unbanned*', parse_mode='Markdown')
            
@bot.message_handler(commands=['get'])
def upload(m):
    try:
        if str(m.from_user.id) == is_sudo:
            text = m.text.split()[1]
            bot.send_document(m.chat.id, open('{}'.format(text)))
    except:
        bot.send_message(m.chat.id, 'Error')

@bot.message_handler(commands=['code'])
def code(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            if m.text.split()[1] == 'base64':
                text = m.text.replace('/code base64','')
                data = base64.b64encode(text)
                bot.send_message(m.chat.id, data)
        except IndexError:
            bot.send_message(m.chat.id, '<b>Error</b>\n<code>Format:\n/code base64 [text]</code>',parse_mode='HTML')

@bot.message_handler(commands=['decode'])
def decode(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            if m.text.split()[1] == 'base64':
                text = m.text.replace('/decode base64','')
                data = base64.b64decode(text)
                bot.send_message(m.chat.id, '<code>' + data + '</code>', parse_mode='HTML')
        except IndexError:
            bot.send_message(m.chat.id, '<b>Error</b>\n<code>Format: \n/decode base64 [text]</code>',parse_mode='HTML')

@bot.message_handler(commands=['uptime'])
def ss(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        tmt = m.from_user.id
        if str(tmt) == is_sudo:
            cc = os.popen("uptime").read()
            bot.send_message(m.chat.id, '`{}`'.format(cc), parse_mode='Markdown')

@bot.message_handler(commands=['cap'])
def mess(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            if m.reply_to_message.document:
                file_id = m.reply_to_message.document.file_id
                text = m.text.split(' ',1)[1]
                bot.send_document(m.chat.id, file_id, caption=text)
            if m.reply_to_message.photo:
                file_id = m.reply_to_message.photo[2].file_id
                text = m.text.split(' ',1)[1]
                bot.send_photo(m.chat.id, file_id, caption=text)
        except (AttributeError,IndexError):
                bot.send_message(m.chat.id, 'Error')
        if not m.reply_to_message:
            msg = bot.send_message(m.chat.id, 'OK send document 50 MB')
            bot.register_next_step_handler(msg, ok)
    def ok(ms):
        if ms.document:
            file_info = bot.get_file(ms.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('./file/{}'.format(ms.document.file_name), 'wb') as new_file:
                new_file.write(downloaded_file)
                rediss.set('file{}'.format(ms.from_user.id), './file/{}'.format(ms.document.file_name))
            mss = bot.send_message(ms.chat.id, 'OK Send Caption')
            bot.register_next_step_handler(mss, okk)
    def okk(mm):
        rediss.set('cp{}'.format(mm.from_user.id), '{}'.format(mm.text))
        bot.send_document(mm.chat.id, open('{}'.format(rediss.get('file{}'.format(mm.from_user.id)))), caption='{}'.format(rediss.get('cp{}'.format(mm.from_user.id))))
        os.remove('{}'.format(rediss.get('file{}'.format(mm.from_user.id))))

@bot.message_handler(commands=['ping'])
def ping(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        bot.send_chat_action(m.chat.id, 'typing')
        bot.send_message(m.chat.id, '*pong :D* \xF0\x9F\x86\x99', parse_mode='Markdown')

@bot.message_handler(regexp='^(/kick) (.*)')
def cap(m):
    if str(m.from_user.id) == is_sudo:
        text = m.text.split()[1]
        bot.kick_chat_member(m.chat.id, text)
        bot.send_message(m.chat.id, 'Kicked {}'.format(text))
        return
    if str(m.from_user.id) not in is_sudo:
        bot.send_message(m.chat.id, 'Just Admin arrow')
        return

@bot.message_handler(commands=['kick'])
def kick(m):    
    if m.from_user.id == is_sudo:
        if m.reply_to_message:
            bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.send_message(m.chat.id, 'kicked <code>{}</code>'.format(m.reply_to_message.from_user.id), parse_mode='HTML')

@bot.message_handler(commands=['leave'])
def leave(m):
    if str(m.from_user.id) == is_sudo:
        bot.leave_chat(m.chat.id)
    if str(m.from_user.id) not in is_sudo:
        bot.send_message(m.chat.id, 'Just Admin arrow')

@bot.message_handler(regexp='^(/voice) (.*)')
def voice(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("http://tts.baidu.com/text2audio?lan=en&ie=UTF-8&text={}&".format(m.text.replace('/voice', '')), "voice.ogg")
        bot.send_voice(m.chat.id, open('voice.ogg'))

@bot.message_handler(commands=['bold'])
def bold(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text1 = m.text.replace('/bold', '')
        bot.send_message(m.chat.id, '<b>{}</b>'.format(text1), parse_mode="HTML")

@bot.message_handler(commands=['italic'])
def italic(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.replace('/italic', '')
        bot.send_message(m.chat.id, '<i>{}</i>'.format(text), parse_mode="HTML")

@bot.message_handler(commands=['cmd'])
def bin(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if str(m.from_user.id) == is_sudo:
            textt = m.text.replace('/cmd', '')
            cmdd = os.popen('{}'.format(textt)).read()
            bot.send_message(m.chat.id, 'Command : {} \n Response : \n{}'.format(textt,cmdd))

@bot.message_handler(commands=['id'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if m.reply_to_message:
            bot.send_message(m.chat.id, m.reply_to_message.from_user.id)

@bot.message_handler(regexp='^(/echo) (.*)')
def echo(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        bot.send_message(m.chat.id, m.text.replace('/echo', ''), parse_mode='Markdown')

#@bot.inline_handler(lambda query: query.query == 'img')
#def qq(q):
    #text = q.query
    #img = 'https://source.unsplash.com/random'
    #gif = types.InlineQueryResultGif('1', '{}'.format(img), '{}'.format(img))
    #bot.answer_inline_query(q.id, [gif], cache_time=1)

@bot.message_handler(regexp='^(/imdb) (.*)')
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            r = urllib.urlopen('http://www.omdbapi.com/?t={}&'.format(m.text.replace('/imdb','')))
            data = r.read()
            pjson = json.loads(data)
            title = pjson['Title']
            year = pjson['Year']
            runtime = pjson['Runtime']
            genre = pjson['Genre']
            language = pjson['Language']
            poster = pjson['Poster']
            urllib.urlretrieve(poster, 'imdb.jpg')
            bot.send_message(m.chat.id, """
<b>Title</b> : {}
<b>Year</b> : {}
<b>Runtime</b> : {}
<b>Genre</b> : {}
<b>Language</b> : {}
            """.format(title,year,runtime,genre,language), parse_mode='HTML')
            bot.send_sticker(m.chat.id, open('imdb.jpg'))
        except IOError:
            bot.send_message(m.chat.id, """
<b>Title</b> : {}
<b>Year</b> : {}
<b>Runtime</b> : {}
<b>Genre</b> : {}
<b>Language</b> : {}
            """.format(title,year,runtime,genre,language), parse_mode='HTML')
        except KeyError:
            bot.send_message(m.chat.id, 'Error')

@bot.message_handler(regexp='^(/git) (.*)')
def gif(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.split()[1]
        r = req.get('https://api.github.com/users/{}'.format(text))
        json_data = r.json()
        if 'id' in json_data:
            url_html = json_data['html_url']
            typee = json_data['type']
            name = json_data['name']
            company = json_data['company']
            blog = json_data['blog']
            location = json_data['location']
            bio = json_data['bio']
            public_repos = json_data['public_repos']
            followers = json_data['followers']
            following = json_data['following']
            avatar_url = json_data['avatar_url']
            urllib.urlretrieve("{}".format(avatar_url), "git.png")
            bot.send_sticker(m.chat.id, open('git.png'))
            bot.send_message(m.chat.id, 'Name : <b>{}</b>\nType : <b>{}</b>\nCompany : <b>{}</b>\nblog : <code>{}</code>\nlocation : <b>{}</b>\nbio : <i>{}</i>\n\nUrl : <code>{}</code>\nfollowers : <code>{}</code>\nfollowing : <code>{}</code>\nRepos : <code>{}</code>\n\xE2\x97\xBC \xE2\x97\xBB \xE2\x97\xBC \xE2\x97\xBB \xE2\x97\xBC \xE2\x97\xBB \xE2\x97\xBC \n@taylor_team'.format(name,typee,company,blog,location,bio,url_html,followers,following,public_repos), parse_mode='HTML')
        if 'message' in json_data:
            bot.send_message(m.chat.id, 'Error \n/git [username]')
            return

@bot.message_handler(commands=['wget'])
def sendadmin(m):
    if str(m.from_user.id) == is_sudo:
        os.popen('wget {}'.format(m.text.replace('/wget', '')))
        bot.send_message(is_sudo, 'ok')

@bot.message_handler(regexp='^(/ip) (.*)')
def ip(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.split()[1]
        r = req.get('http://ip-api.com/json/{}?fields=262143'.format(text))
        json_data = r.json()
        if 'as' in json_data:
            mss = json_data['country']
            isp = json_data['isp']
            timezone = json_data['timezone']
            zipcode = json_data['zip']
            lat = json_data['lat']
            lon = json_data['lon']
            bot.send_message(m.chat.id, 'Country : <b>{}</b>\n\nIsp : <b>{}</b>\n\nTimezone : <code>{}</code>\n\nZip code : <code>{}</code>'.format(mss,isp,timezone,zipcode), parse_mode='HTML')
            bot.send_location(m.chat.id, lat, lon)
            return
        if 'message' in json_data:
            bot.send_message(m.chat.id, 'Error')
            return


@bot.message_handler(commands=['sticker'])
def sticker(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("https://assets.imgix.net/examples/blueberries.jpg?blur=500&fit=crop&w=1200&h=500&trimcolor=ffffff&txt={}&txtsize=150&txtalign=middle%2C%20center&txtline=3".format(m.text.replace('/sticker', '')), "sticker.png")
        bot.send_sticker(m.chat.id, open('sticker.png'))

@bot.message_handler(commands=['tophoto'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            if m.reply_to_message.sticker:
                fileid = m.reply_to_message.sticker.file_id
                get = bot.get_file(fileid)
                dw = bot.download_file(get.file_path)
                with open('sticker.png','wb') as f:
                    f.write(dw)
                bot.send_photo(m.chat.id, open('sticker.png'))
                os.remove('sticker.png')
        except AttributeError:
            bot.send_message(m.chat.id, 'Just Reply Sticker message')

@bot.message_handler(commands=['tosticker'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            if m.reply_to_message.photo:
                fileid = m.reply_to_message.photo[2].file_id
                get = bot.get_file(fileid)
                dw = bot.download_file(get.file_path)
                with open('sticker.png','wb') as f:
                    f.write(dw)
                bot.send_sticker(m.chat.id, open('sticker.png'))
        except AttributeError:
            bot.send_message(m.chat.id, 'Just Reply Photo message')
        except IndexError:
            bot.send_message(m.chat.id, 'Size Error')

@bot.message_handler(commands=['time'])
def sticker(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        url = "http://api.gpmod.ir/time/"
        response = urllib.urlopen(url)
        data = response.read()
        parsed_json = json.loads(data)
        ENtime = (parsed_json['ENtime'])
        FAtime = (parsed_json['FAtime'])
        ENdate = (parsed_json['ENdate'])
        FAdate = (parsed_json['FAdate'])
        url2 = "https://script.googleusercontent.com/macros/echo?user_content_key=ddWxlbLDkPaVRaf5vMzxdD_JWXdhQgylin2z_zcqwQ72ueXte1Wgkk_opdn4cBx1XLLFh44Bs1Dp-6L0L8pGEifJ9hvapYOIm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnJ9GRkcRevgjTvo8Dc32iw_BLJPcPfRdVKhJT5HNzQuXEeN3QFwl2n0M6ZmO-h7C6bwVq0tbM60-cNZSfDuhe8zO39xySBUXxQ&lib=MwxUjRcLr2qLlnVOLh12wSNkqcO1Ikdrk"
        response2 = urllib.urlopen(url2)
        data = response2.read()
        g = json.loads(data)
        ho = g['hours']
        mt = g['minutes']
        sc = g['seconds']
        year = g['year']
        fulldate = g['fulldate']
        urllib.urlretrieve('https://assets.imgix.net/sandbox/sandboxlogo.ai?blur=500&fit=crop&w=1200&h=600&txtclr=black&txt={}&txtalign=middle%2C%20center&txtsize=150&txtline=3'.format(ENtime), 'time.jpg')
        bot.send_message(m.chat.id, """
Time : *{}*

\xD8\xB3\xD8\xA7\xD8\xB9\xD8\xAA : {}

Date : *{}*

\xD8\xAA\xD8\xA7\xD8\xB1\xDB\x8C\xD8\xAE : {}

\xD8\xA8\xD8\xB1\x20\xD8\xA7\xD8\xB3\xD8\xA7\xD8\xB3\x20\xD8\xB3\xD8\xA7\xD8\xB9\xD8\xAA\x20\xDA\xAF\xD9\x88\xDA\xAF\xD9\x84 :

google api time :
{}:{}:{}

Year : {}

fulldate : {}

        """.format(ENtime,FAtime,ENdate,FAdate,ho,mt,sc,year,fulldate), parse_mode='Markdown')
        bot.send_sticker(m.chat.id, open('time.jpg'))

@bot.message_handler(commands=['dog'])
def d(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.replace('/dog', '')
        urllib.urlretrieve("http://dogr.io/{}.png?split=false&s.png".format(text), "s.png")
        bot.send_photo(m.chat.id, open('s.png'))

@bot.message_handler(commands=['qr'])
def qr(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.replace('/qr', '')
        urllib.urlretrieve("https://api.qrserver.com/v1/create-qr-code/?size=1200x800&data={}&bgcolor=ffff00&".format(text), "qr.png")
        bot.send_photo(m.chat.id, open('qr.png'))

@bot.message_handler(commands=['pic'])
def logo(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("https://source.unsplash.com/random", "img.jpg")
        bot.send_chat_action(m.chat.id, 'upload_photo')
        bot.send_photo(m.chat.id, open('img.jpg'), caption='@Arrow_robot')

@bot.message_handler(commands=['wallpaper'])
def wallpaper(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("https://source.unsplash.com/1600x900", "wallpaper.jpg")
        bot.send_photo(m.chat.id, open('wallpaper.jpg'), caption='Wallpaper 1600x900')

@bot.message_handler(commands=['info'])
def info(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if not m.reply_to_message:
            try:
                f_id = bot.get_user_profile_photos(m.from_user.id).photos[0][2].file_id
                f = bot.get_file(f_id)
                downloaded_file = bot.download_file(f.file_path)
                with open('user.png', 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.send_photo(m.chat.id, open('user.png'), caption='Username : @{}\nID : {}'.format(m.from_user.username,m.from_user.id))
            except IndexError:
                bot.send_message(m.chat.id, 'Username : @{}\nID : {}'.format(m.from_user.username,m.from_user.id))
        if m.reply_to_message:
            try:
                f_id = bot.get_user_profile_photos(m.reply_to_message.from_user.id).photos[0][2].file_id
                f = bot.get_file(f_id)
                downloaded_file = bot.download_file(f.file_path)
                with open('user.png', 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.send_photo(m.chat.id, open('user.png'), caption='Username : @{}\nID : {}'.format(m.reply_to_message.from_user.username,m.reply_to_message.from_user.id))
            except IndexError:
                bot.send_message(m.chat.id, 'Username : @{}\nID : {}'.format(m.reply_to_message.from_user.username,m.reply_to_message.from_user.id))
            except KeyError:
                bot.send_message(m.chat.id, 'Error')

@bot.message_handler(commands=['food'])
def food(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("https://source.unsplash.com/category/food", "food.jpg")
        bot.send_sticker(m.chat.id, open('food.jpg'))

@bot.message_handler(commands=['tehran'])
def tr(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        bot.send_location(m.chat.id, 35.6891975, 51.3889736)

@bot.message_handler(commands=['loc'])
def loc(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            url = urllib.urlopen('http://maps.googleapis.com/maps/api/geocode/json?address={}'.format(m.text.replace('/loc','')))
            data = url.read()
            js = json.loads(data)
            lat = js['results'][0]['geometry']['location']['lat']
            lng = js['results'][0]['geometry']['location']['lng']
            bot.send_location(m.chat.id, lat,lng)
        except IndexError:
            bot.send_message(m.chat.id, '/loc [City]')
        except KeyError:
            bot.send_message(m.chat.id, 'Error')


@bot.message_handler(commands=['tr'])
def tre(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20160119T111342Z.fd6bf13b3590838f.6ce9d8cca4672f0ed24f649c1b502789c9f4687a&format=plain&lang=fa&text={}&".format(m.text.replace('/tr', ''))
        response = urllib.urlopen(url)
        data = response.read()
        trr = json.loads(data)
        text = trr['text']
        bot.reply_to(m, text)

@bot.message_handler(regexp='^(/webshot) (.*)')
def web(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("http://api.screenshotmachine.com/?key=b645b8&size=X&url={}".format(m.text.replace('/webshot', '')), "web.jpg")
        bot.send_photo(m.chat.id, open('web.jpg'))

@bot.message_handler(regexp='^(/calc) (.*)')
def web(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
            encodee = urllib.quote_plus(m.text.replace('/calc', ''))
            url = "http://api.mathjs.org/v1/?expr={}&".format(encodee)
            response = urllib.urlopen(url)
            data = response.read()
            bot.reply_to(m, '\xD9\x86\xD8\xAA\xDB\x8C\xD8\xAC\xD9\x87\n  <code>{}</code>'.format(data), parse_mode='HTML')
        except (KeyError,IndexError):
            bot.reply_to(m, 'Error')

@bot.message_handler(content_types=['new_chat_member'])
def new(m):
    name = m.new_chat_member.first_name
    title = m.chat.title
    bot.send_message(m.chat.id, 'Welcome *{}* To `{}`'.format(name,title), parse_mode='Markdown')

@bot.message_handler(content_types=['left_chat_member'])
def new(m):
    name = m.left_chat_member.first_name
    bot.send_message(m.chat.id, 'Bye *{}*'.format(name), parse_mode='Markdown')

@bot.message_handler(content_types=['sticker'])
def m(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if m.chat.type == 'private':
            text = m.sticker.emoji
            bot.reply_to(m, 'Emoji : '+text)

@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'location'])
def us(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        if m.chat.type == "private":
            try:
                hash = 'hash'
                now = rediss.get(hash)
                new = int(now) + 1
                rediss.set(hash,new)
            except :
                print 'not'
        if m.chat.type == "private":
            if m.forward_from:
                name = m.forward_from.first_name
                usr = m.forward_from.username
                idd = m.forward_from.id
                bot.send_message(m.chat.id, """
    From User First Name : {}
    From Username : @{}
    From User ID : {}
                """.format(name,usr,idd))
                    
bot.polling(True)

