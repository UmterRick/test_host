import requests
import logging
import time
import asyncio
import calendar
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Update
from datetime import datetime, timedelta


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:85.0) Gecko/20100101 Firefox/85.0'}
URL = 'https://meandmyschool.org.ua/ru/'
TOKEN = '1485443475:AAEv-Xl15Xp9Z6sSFyH4tizumu4oeJ3ZtdY'
C_URL = 'https://meandmyschool.org.ua/detalnishe-pro-prohramy/'

DB_NAME = 'test1'
ADMIN_PASSWORD = '1111'
TRAINER_PASSWORD = '2222'

USER_TYPE = None
CHAT_ID = 0
msgID = None
DELAY = 100
DELAY_2 = 30

weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
eng_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

daytimes = []
coursesId = []
list_of_coursesID = []

start_text = 'Привіт! 👋\nЯ бот🤖, який допоможе тобі обрати собі курс у нашому освітньому центрі \n \
        ЯІМОЯШКОЛА🎓\nОбреріть хто ви?👇🏻'


admin_groups_start = "Вітаю, я Бот <i>ЯІМОЯШКОЛА</i>\n " \
                     "Ви додали мене до чату адміністраторів.\n" \
                     "Тут ви зможете отримувати нові заявки до груп\n\n" \
                     "Для доступу до функцій треба <b>ввести пароль</b> адміністраторів!"


def str_to_list(input_str):
    res = []
    if input_str == '[]':
        res = []
    else:
        for i in input_str[1:-1].split(','):
            i = int(i.strip())
            res.append(i)
    return res


def range_to_str_list(my_range_end):
    res = []
    for el in range(my_range_end):
        res.append(str(el))
    return res


old_topics = {1: 'ex1', 2: 'ex2', 3: 'ex3'}
old_courses = [[1, 1, 'name11'], [1, 2, 'name12'], [2, 1, 'name21'], [3, 1, 'name31']]

old_topics1 = [[1, 'ex1'], [2, 'ex2'], [3, 'ex3']]

new_topics = {1: 'ex1',2: 'ex4',3: 'ex2',4: 'ex3',5: 'ex5'}
new_courses = [[1, 1, 'name11'], [1, 2, 'name12'], [2, 1, 'name21'], [3, 1, 'name31'], [4,1,'name41'], [5,1,'name51']]


#
# for name in table1.names:
#     if name in table2.names:
#         'update table1 set id = (select id from table2 where name2 = name) where nam1= name'
#     elif name not in table2.names:
#         a = 'select course_name from table1 where name1 = name'
#         b = 'select course_name from table12 where name2 = name'
#         if a in b or b in a:
#             'update table1 set name = (select name from table2 where name2 = name) where nam1= name'


