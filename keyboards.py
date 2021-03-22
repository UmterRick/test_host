from database import *
from config import *
from main import bot, create_callback_data, separate_callback_data


def DaysKB():
    days_keyboard = InlineKeyboardMarkup()
    d = datetime(year=2021, month=2, day=1, hour=0)
    for i in range(7):
        if str(calendar.day_name[d.weekday()]) == 'Monday':
            res = 'ПН'
        elif str(calendar.day_name[d.weekday()]) == 'Tuesday':
            res = 'ВТ'
        elif str(calendar.day_name[d.weekday()]) == 'Wednesday':
            res = 'СР'
        elif str(calendar.day_name[d.weekday()]) == 'Thursday':
            res = 'ЧТ'
        elif str(calendar.day_name[d.weekday()]) == 'Friday':
            res = 'ПТ'
        elif str(calendar.day_name[d.weekday()]) == 'Saturday':
            res = 'СБ'
        elif str(calendar.day_name[d.weekday()]) == 'Sunday':
            res = 'ВС'
        else:
            res = str(calendar.day_name[d.weekday()])
        day_btn = InlineKeyboardButton(text=res, callback_data=res)
        d += timedelta(days=1)
        days_keyboard.row(day_btn)
    return days_keyboard


def EngDaysKB():
    days_keyboard = InlineKeyboardMarkup()
    d = datetime(year=2021, month=2, day=1, hour=0)
    for i in range(7):
        res = str(calendar.day_name[d.weekday()])
        day_btn = InlineKeyboardButton(text=res, callback_data=res)
        d += timedelta(days=1)
        days_keyboard.row(day_btn)
    return days_keyboard


def TimeKB():
    global daytimes
    group_time_keyboard = InlineKeyboardMarkup()
    d = datetime(year=2021, month=2, day=5, hour=9, minute=0)
    for i in range(21):
        hour = d.strftime('%H:%M')
        d += timedelta(minutes=30)
        daytimes.append(str(hour))
        gt_btn = InlineKeyboardButton(str(hour), callback_data=hour)
        group_time_keyboard.add(gt_btn)
    return group_time_keyboard


def UserTypeKB():
    keyboard = types.InlineKeyboardMarkup()
    already_user = InlineKeyboardButton('Учень🤓', callback_data='Учень🤓')
    trainer_user = InlineKeyboardButton('Тренер📝', callback_data='Тренер📝')
    admin_user = InlineKeyboardButton('Адміністратор📒', callback_data='Адміністратор📒')
    keyboard.row(already_user)
    keyboard.row(trainer_user, admin_user)
    return keyboard


def ContactKB():
    keyboard = InlineKeyboardMarkup(row_width=1)
    instagram = InlineKeyboardButton('🖼 Instagram', url='https://www.instagram.com/meandmyschoolcenter/')
    insta_kids = InlineKeyboardButton('👶 Instagram Діти', url='https://www.instagram.com/meandmyschoolkids/')
    facebook = InlineKeyboardButton('💙 Facebook',
                                    url='https://www.facebook.com/meandmyschoolcenter/?hc_ref=ARR'
                                        '-D44Bb8Kj9bWSV4DhW3XVZEjkWkIylAy1-aGhlCQ5AkDIx5sUht8hxsN-9MAgXSI&ref'
                                        '=nf_target&__tn__=kC-R')
    viber = InlineKeyboardButton('💜 Viber',
                                 url='https://invite.viber.com/?g2=AQAeAWoOG4gBCEyzb32Jt0WVJ6QTVFi5U8nL%2B'
                                     '%2FWQyjZnLpqtMlWibHHyFvTQ9kce')
    telegram = InlineKeyboardButton('✉️ Telegram', url='https://t.me/meandmyschoolcenter')
    website = InlineKeyboardButton('🌐 Наш сайт', url='https://meandmyschool.org.ua/')
    phone_1 = InlineKeyboardButton('📞 Телефон Kyivstar: +38(097)-270-50-72', callback_data='phone1')
    phone_2 = InlineKeyboardButton('📞 Телефон Vodafone: +38(050)-270-50-72', callback_data='phone2')
    address = InlineKeyboardButton('🏫 Наша адреса : Костомарівська 2', url='https://g.page/meandmyschoolcenter?share')

    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')

    keyboard.row(instagram, insta_kids)
    keyboard.row(telegram, viber)
    keyboard.row(facebook, website)
    keyboard.row(phone_1, phone_2)
    keyboard.row(address)
    keyboard.row(back_btn)

    return keyboard


def MyCoursesKB(name, telegram_id):
    keyboard = InlineKeyboardMarkup()
    user_info = db_get_user_info(name, telegram_id)

    for group in user_info[2]:
        url = C_URL
        group_text, course_text, course_id, category_id = db_get_group_info(name, group)
        courses = db_read_courses(name, category_id)
        for course in courses:
            if course[0] == course_id:
                url = course[4]
        my_course_btn = InlineKeyboardButton('✅ Курс : ' + course_text, url=url, callback_data='ignore')
        my_group_btn = InlineKeyboardButton('▶️ Група : ' + group_text, callback_data=create_callback_data(group, 'my_group'))
        keyboard.row(my_course_btn)
        keyboard.row(my_group_btn)

    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')
    keyboard.row(back_btn)
    return keyboard


def TrainersKB(name):
    keyboard = InlineKeyboardMarkup()
    trainers_names, trainers_dict = db_get_trainer_courses(name)
    for name in trainers_names:
        callback = str(trainers_dict[name])
        trainer_btn = InlineKeyboardButton(name, callback_data=callback)
        keyboard.row(trainer_btn)
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')
    keyboard.row(back_btn)

    return keyboard


def StudentsKB(group_id):
    print('StudentsKB group = ', group_id)
    keyboard = InlineKeyboardMarkup()
    students = db_get_group_students(DB_NAME, int(group_id))
    print('StudentsKB :', students)
    for student in students:
        user_btn = InlineKeyboardButton(student[1], callback_data=create_callback_data(group_id, student[0]))
        delete_user_btn = InlineKeyboardButton('❌', callback_data=create_callback_data(group_id, student[0], 'delete'))
        keyboard.row(user_btn, delete_user_btn)
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data=create_callback_data(group_id, 'stud_back'))
    keyboard.row(back_btn)
    return keyboard


def MenuKB(telegram_id):
    user_type = db_get_save_var(DB_NAME, telegram_id, 'user_type')
    keyboard = InlineKeyboardMarkup(row_width=1)
    if user_type == 'client':
        my_crs_callback = 'my_course'
    else:
        my_crs_callback = 'trainer_course'
    my_courses_btn = InlineKeyboardButton('Мої курси', callback_data=my_crs_callback)
    all_courses_btn = InlineKeyboardButton('Всі курси', callback_data='all_courses')
    contacts_btn = InlineKeyboardButton('Наші контакти', callback_data='contacts')
    if user_type != 'admin':
        keyboard.add(my_courses_btn)
    if user_type != 'trainer':
        keyboard.add(all_courses_btn)
    keyboard.add(contacts_btn)
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')
    keyboard.row(back_btn)
    return keyboard


def TopicKB():
    global TOPICS
    TOPICS = db_read_topics(DB_NAME)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for button in TOPICS.values():
        topic_id = list(TOPICS.keys())[list(TOPICS.values()).index(button)]
        category_btn = InlineKeyboardButton(button, callback_data=topic_id)
        keyboard.row(category_btn)
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')
    keyboard.row(back_btn)
    return keyboard


async def CoursesKB(call, category, state, clicked_course):
    global list_of_coursesID
    list_of_coursesID = []
    course = db_read_courses(DB_NAME, str(category))
    await call.message.delete()
    for cur_course in course:
        keyboard = InlineKeyboardMarkup(row_width=1)
        course_id = cur_course[0]
        course_body = f'✅✅✅\nНазва курсу: {cur_course[2]}\nТренер:{cur_course[3]}'
        clicked_course[course_id] = course_body
        inline_btn = InlineKeyboardButton(f"⚪️Перелік груп️⚪️", callback_data=create_callback_data(course_id, category))
        url_btn = InlineKeyboardButton(text='📄Повний опис курсу📄', url=cur_course[4])

        keyboard.add(inline_btn, url_btn)

        sending_course = await bot.send_message(chat_id=call.from_user.id, text=course_body, reply_markup=keyboard)
        list_of_coursesID.append(sending_course.message_id)

    await state.update_data(msgToDel=list_of_coursesID)

    keyboard = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')
    keyboard.add(back_btn)
    back_btn = await bot.send_message(call.from_user.id, 'Повернутись до категорій', reply_markup=keyboard)
    list_of_coursesID.append(back_btn.message_id)
    db_save_var(DB_NAME, call.from_user.id, 'temp_var', list_of_coursesID)


async def GroupsKB(cur_groups, user_id, course_id, category_id, state):
    user_type = db_get_save_var(DB_NAME, user_id, 'user_type')
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    if len(cur_groups) == 0:
        empty_group_btn = InlineKeyboardButton(text='Очікуйте, запис на курс незабаром почнеться',
                                               callback_data='ignore_callback')
        keyboard.row(empty_group_btn)
    for i in range(len(cur_groups)):
        if cur_groups[i][2] == 1:
            cur_groups[i][2] = 'Офлайн'
        elif cur_groups[i][2] == 0:
            cur_groups[i][2] = 'Онлайн'
        group_body = ('📅(🕒) ' + cur_groups[i][1] + ' 🌐(' + cur_groups[i][2] + ')')

        inline_btn = InlineKeyboardButton(f"{group_body}", callback_data=create_callback_data(cur_groups[i][0], 'clicked'))

        keyboard.row(inline_btn)
        if user_type == 'admin':
            delete_btn = InlineKeyboardButton("❌", callback_data=create_callback_data(cur_groups[i][0], 'del'))
            edit_btn = InlineKeyboardButton("✏️", callback_data=create_callback_data(cur_groups[i][0],course_id, category_id, 'edit'))
            students_btn = InlineKeyboardButton("👨‍ 👩‍", callback_data=create_callback_data(cur_groups[i][0], 'students'))

            keyboard.row(delete_btn, edit_btn)
            keyboard.row(students_btn)
        else:
            enroll_btn = InlineKeyboardButton("Подати заявку у групу️", callback_data=create_callback_data(cur_groups[i][0], 'enroll'))
            keyboard.row(enroll_btn)
    if user_type == 'admin':
        add_btn = InlineKeyboardButton('Додати нову групу', callback_data=create_callback_data(course_id,category_id,'add_group'))
        keyboard.row(add_btn)
        await state.update_data(group_to=create_callback_data(course_id, category_id), editing=False)
        print('GroupsKB group_to =  ',create_callback_data(course_id, category_id), type(create_callback_data(course_id, category_id)))
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data='turn_back')
    keyboard.row(back_btn)
    return keyboard


def NotesKB(group_id):
    keyboard = InlineKeyboardMarkup()
    notifications = db_read_notification(DB_NAME)
    for note in notifications:
        if int(note[1]) == int(group_id):
            print(note[2])
            note_btn = InlineKeyboardButton(text=note[2], callback_data=note[0])
            del_note_btn = InlineKeyboardButton('❌', callback_data=create_callback_data(note[0], 'remove', group_id))

            keyboard.row(note_btn)
            keyboard.row(del_note_btn)

    add_note_btn = InlineKeyboardButton('Додати нагадування', callback_data=create_callback_data(group_id, 'add_note'))
    back_btn = InlineKeyboardButton('⬅️ Назад', callback_data=create_callback_data(group_id, 'turn_back'))
    keyboard.row(add_note_btn)
    keyboard.row(back_btn)
    return keyboard
