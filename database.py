import mysql.connector
from bs4 import BeautifulSoup
from mysql.connector import errorcode
from mysql.connector import Error

from config import DB_NAME, datetime, timedelta
from config import *


html = requests.get(C_URL, headers=HEADERS)
def db_connect(db_name):
    db = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        user='root',
        passwd='root',
        database=db_name)
    return db


def db_create_tables(db_name):
    db = db_connect(db_name)
    cursor = db.cursor()
    tables = dict()

    # tables['category'] = ('''
    #     CREATE TABLE IF NOT EXISTS category (
    #     id	INTEGER NOT NULL PRIMARY KEY,
    #     topic_name	TEXT NOT NULL
    #     )
    #     ENGINE = InnoDB
    #     ''')
    tables['courses'] = ('''
        CREATE TABLE IF NOT EXISTS courses (
        id	INTEGER NOT NULL,
        category_id INTEGER NOT NULL ,
        name   TEXT NOT NULL,
        teacher	TEXT NOT NULL,
        description	TEXT,
        price	INTEGER NOT NULL DEFAULT 0,
        category_name VARCHAR(45) NOT NULL,
        PRIMARY KEY(category_id, id)
        )ENGINE = MYISAM;''')

    # tables['course_trigger'] = ('''
    #         CREATE
    #         TRIGGER update_category_in_course AFTER UPDATE
    #         ON category
    #         FOR EACH ROW
    #             BEGIN
    #                UPDATE courses SET category_id = NEW.id WHERE category_id = OLD.id;
    #                UPDATE groups SET category_id = NEW.id WHERE category_id = OLD.id;
    #             END;
    #     ''')

    tables['groups'] = ('''  
            CREATE TABLE IF NOT EXISTS groups (
              id INT(11) NOT NULL AUTO_INCREMENT,
              daytime TEXT NOT NULL,
              offline INT(11) NULL DEFAULT NULL,
              course_id INT(11) NOT NULL,              
              category_id INT(11) NOT NULL,
              course_name VARCHAR(256) NOT NULL,
              category_name VARCHAR(45) NOT NULL,

              PRIMARY KEY (id)
              )ENGINE = InnoDB;
            ''')
    tables['group_trigger'] = ('''
                CREATE
                TRIGGER update_group AFTER UPDATE 
                ON courses
                FOR EACH ROW 
                    BEGIN
                       UPDATE groups SET category_id = NEW.category_id WHERE category_id = OLD.category_id;
                       UPDATE groups SET course_id = NEW.id WHERE course_id = OLD.id;
                    END;
            ''')
    tables['users'] = ('''
        CREATE TABLE  IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
            telegramID VARCHAR(45) NOT NULL UNIQUE,
            name TEXT NOT NULL,
            nickname VARCHAR(45),
            user_type TEXT,
            group_id VARCHAR(45) DEFAULT '[]',
            enroll VARCHAR(45) DEFAULT '[]',
            contacts VARCHAR(45) DEFAULT 'empty_number',
            user_state VARCHAR(45) NOT NULL,
            temp_var TEXT,
            viewing_category INT(11)             
            );  
            ''')
    tables['notifications'] = ('''
        CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
        group_id INTEGER NOT NULL,
        datetime VARCHAR(45) NOT NULL,
        status VARCHAR(45) NOT NULL DEFAULT 'wait');
        ''')
    tables['courses_compare'] = ('''
        CREATE TABLE courses_compare (
        id	INTEGER NOT NULL,
        category_id INTEGER NOT NULL ,
        name   TEXT NOT NULL,
        teacher	TEXT NOT NULL,
        description	TEXT,
        price	INTEGER NOT NULL DEFAULT 0,
        category_name VARCHAR(45) NOT NULL,
        PRIMARY KEY(category_id, id)
        )ENGINE = MYISAM;''')
    for table_name in tables:
        table_description = tables[table_name]
        try:
            cursor.execute(table_description)
            print(f"Creating table {table_name}: ", end='\n')
        except mysql.connector.Error as err:
                print(f'db_create_tables {table_name} err:', err.msg)
    # try:
    #     cursor.execute(
    #         'ALTER TABLE courses ADD CONSTRAINT fk_category_id_in_courses FOREIGN KEY (category_id) '
    #         'REFERENCES category(id) ON UPDATE CASCADE ON DELETE CASCADE')
    # except mysql.connector.Error as err:
    #     print(f'add fk_courses_to_category_id  err:', err.msg)

    # try:
    #     cursor.execute(
    #         'ALTER TABLE groups ADD CONSTRAINT fk_group_to_course_id FOREIGN KEY (course_id) '  #
    #         'REFERENCES courses(id) ON UPDATE CASCADE ON DELETE CASCADE')
    # except mysql.connector.Error as err:
    #     print(f'add fk_course_id err:', err.msg, errorcode, err.msg, err.errno, err.args, err.sqlstate)

    # try:
    #     cursor.execute(
    #         'ALTER TABLE groups ADD  FOREIGN KEY (category_id) '    # CONSTRAINT fk_groups_to_category_id
    #         'REFERENCES courses(category_id) ON UPDATE CASCADE ON DELETE CASCADE')
    # except mysql.connector.Error as err:
    #     print(f'add fk_groups_to_category_id err:', err.msg)


    db.commit()
    cursor.close()
    db.close()


def db_add_category(name, cat_id, cat_name, table_name):
    db = db_connect(name)
    cursor = db.cursor()
    new_category = (f'''
                    INSERT INTO {table_name}
                    (id,topic_name)
                    VALUES(%s,%s) 
                    ''')
    category_data = (cat_id, cat_name)
    try:
        cursor.execute(new_category, category_data)
    except mysql.connector.Error as err:
        print('db_add_category: ', err.msg)
    else:
        pass

    db.commit()
    cursor.close()
    db.close()


def db_add_course(name, course_id, course_name, course_trainer, course_description, category_id, category_name):
    db = db_connect(name)
    cursor = db.cursor()
    new_course = (
        '''
        INSERT INTO courses
        (id, name, teacher,description,category_id, category_name)
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
    )
    course_data = (course_id, course_name, course_trainer, course_description, category_id, category_name)
    try:
        cursor.execute(new_course, course_data)
    except mysql.connector.Error as err:
        #print(f'db_add_course err:', err.msg)
        pass
    else:
        pass
    db.commit()
    cursor.close()
    db.close()


def db_add_group(name, group_datetime, offline_flag, to_course, to_category):
    db = db_connect(name)
    cursor = db.cursor()
    command = f'select name, category_name from courses where id ={to_course} and category_id = {to_category}'

    # new_group = (
    #     '''
    #     INSERT INTO groups
    #     (daytime, offline,course_id, category_id, course_name, category,name)
    #     VALUES (%s, %s, %s, %s);
    #     '''
    # )
    # group_data = (group_datetime, offline_flag, to_course, to_category)
    try:
        cursor.execute(command)
        record = cursor.fetchone()
        print(record)
        command = 'insert into groups' \
                  '(daytime, offline,course_id, category_id, course_name, category_name)' \
                  'values (%s, %s, %s, %s, %s, %s);'
        group_data = (group_datetime, offline_flag, to_course, to_category, record[0], record[1])
        cursor.execute(command, group_data)

    except mysql.connector.Error as err:
        print('add group: ', err.msg)
        pass
    else:
        pass
    db.commit()
    cursor.close()
    db.close()


def db_read_topics(name):
    db = db_connect(name)
    cursor = db.cursor()
    cursor.execute('SELECT category_id,category_name FROM courses')
    topics = {}
    try:
        records = cursor.fetchall()

        for row in records:
            topics[row[0]] = row[1]

    except mysql.connector.Error as err:
        print(f'db_read_topics err:', err.msg)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()

    return topics


def db_read_courses(name, category):
    db = db_connect(name)
    cursor = db.cursor()
    db_read = 'SELECT * FROM courses WHERE category_id = %s'
    cursor.execute(db_read, (category,))
    my_list = []
    try:
        records = cursor.fetchall()
        for row in records:
            my_list.append([row[0], row[1], row[2], row[3], row[4]])  #  id, category_id, name, trainer_name, decription, price
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return my_list


def db_read_groups(name, course_id, category_id):
    db = db_connect(name)
    cursor = db.cursor()
    group_list = []
    db_read = 'SELECT * FROM groups  WHERE course_id = %s AND category_id = %s'
    cursor.execute(db_read, (course_id,category_id,))
    try:
        records = cursor.fetchall()
        for row in records:
            group_list.append([row[0], row[1], row[2], row[3], row[4]])
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return group_list


def db_delete_group(name, group_id):
    db = db_connect(name)
    cursor = db.cursor()
    command = 'DELETE FROM groups  WHERE id = %s'
    try:
        cursor.execute(command, (group_id,))
        command = 'SELECT telegramID,group_id FROM users'
        cursor.execute(command)
        record = cursor.fetchall()
        for row in record:
            groups_list = str_to_list(row[1])
            if group_id not in groups_list:
                continue  # print('deleting group info: this group not found in current user groups')
            else:
                groups_list.remove(group_id)
            new_groups = str(groups_list)
            if len(groups_list) == 0:
                new_groups = '[]'
            db_save_var(name, row[0], 'group_id', new_groups)

        command = 'SELECT telegramID,enroll FROM users'
        cursor.execute(command)
        record = cursor.fetchall()
        for row in record:
            enroll_list = str_to_list(row[1])
            if group_id not in enroll_list:
                continue  # print('deleting enroll from group_delete info: enroll not found in current user groups')
            else:
                enroll_list.remove(group_id)
            new_enrolls = str(enroll_list)
            if len(enroll_list) == 0:
                new_enrolls = '[]'
            db_save_var(name, row[0], 'enroll', new_enrolls)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


def db_edit_group(name, group_id, new_datetime, new_flag):
    db = db_connect(name)
    cursor = db.cursor()
    command = 'UPDATE groups SET daytime = %s, offline = %s WHERE(id = %s)'
    group_new_data = (new_datetime, new_flag, group_id)
    try:
        cursor.execute(command, group_new_data)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to edit record from table: {}".format(error))
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


def db_get_group_info(name, group_id):
    db = db_connect(name)
    cursor = db.cursor()
    command = 'SELECT daytime, course_id, category_id FROM groups WHERE(id = %s)'
    cursor.execute(command, (group_id,))
    course_id = 0
    group_info = 0
    category_id = 0
    course_name = ''
    try:
        records = cursor.fetchall()
        for row in records:
            group_info, course_id, category_id = str(row[0]).lstrip(), row[1], row[2]
    except Error:
        print("Error reading data from MySQL table", Error)

    command = 'SELECT name FROM courses WHERE id = %s AND category_id = %s'
    cursor.execute(command, (course_id, category_id, ))
    try:
        record = cursor.fetchall()
        for row in record:
            course_name = str(row[0]).lstrip()
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return group_info, course_name, course_id, category_id


def db_add_notification(name, group_id, date_time):
    db = db_connect(name)
    cursor = db.cursor()
    command = (
        '''
        INSERT INTO notifications
        (group_id,datetime,status)
        VALUES (%s, %s, %s);
        '''
    )
    notif_data = (group_id, date_time, 'wait')
    try:
        cursor.execute(command, notif_data)
    except mysql.connector.Error as err:
        print('add note: ', err.msg)
        pass
    else:
        pass
    db.commit()
    cursor.close()
    db.close()


def db_delete_notification(name, note_id):
    db = db_connect(name)
    cursor = db.cursor()
    command = f'DELETE FROM notifications WHERE id = {note_id}'
    try:
        cursor.execute(command)
        db.commit()
    except mysql.connector.Error as err:
        print('db_delete_notification err : ', err)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


def db_read_notification(name):
    db = db_connect(name)
    cursor = db.cursor()
    notif_list = []
    command = 'SELECT * FROM notifications'
    cursor.execute(command)
    try:
        records = cursor.fetchall()
        for row in records:
            notif_list.append([row[0], row[1], row[2], row[3]])
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return notif_list


def db_change_notification_status(name, note_id):
    new_status = None
    db = db_connect(name)
    cursor = db.cursor()
    command = 'SELECT * FROM notifications WHERE id = %s'
    cursor.execute(command, (note_id,))
    notif = cursor.fetchall()
    notif = notif[0]

    if notif[3] == 'wait':
        new_status = 'sended'

    elif notif[3] == 'sended':
        new_status = 'wait'
    operation = 'UPDATE notifications SET status = %s WHERE(id = %s)'
    cursor.execute(operation, (new_status, note_id,))
    db.commit()
    cursor.close()
    db.close()


def db_read_users(name):
    db = db_connect(name)
    cursor = db.cursor()
    user_list = []
    command = 'SELECT * FROM users'
    cursor.execute(command)
    try:
        records = cursor.fetchall()
        for row in records:
            user_list.append(
                [row[0], row[1], row[2], row[3], row[4], row[5]])  # id, telegramID, name, nickname,user_type, groups
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return user_list


def db_start_add_user(name, user_info):
    db = db_connect(name)
    cursor = db.cursor()
    command = (
        '''
        INSERT INTO users
        (telegramID, name, nickname, user_state)
        VALUES (%s, %s, %s, %s);
        '''
    )
    try:
        cursor.execute(command, user_info)
    except mysql.connector.Error as err:
        print('add user: ', err.msg)
        pass
    else:
        pass
    db.commit()
    cursor.close()
    db.close()


def db_upd_user_state(name, telegram_id, new_state):
    db = db_connect(name)
    cursor = db.cursor()
    command = 'UPDATE users SET user_state = %s WHERE(telegramID = %s);'
    cursor.execute(command, (new_state, telegram_id,))
    db.commit()
    cursor.close()
    db.close()


def db_get_user_state(name, telegram_id):
    cur_state = None
    db = db_connect(name)
    cursor = db.cursor()
    command = 'SELECT user_state FROM users WHERE(telegramID = %s) LIMIT 1'
    cursor.execute(command, (telegram_id,))
    try:
        records = cursor.fetchone()
        for row in records:
            cur_state = row
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return cur_state


def db_save_var(name, telegram_id, save_to, save_var):
    db = db_connect(name)
    cursor = db.cursor()
    sql = f"UPDATE users SET {save_to}  = %s WHERE telegramID = %s"
    val = (str(save_var), telegram_id)
    try:
        cursor.execute(sql, val)
    except mysql.connector.Error as err:
        print('add temp_var: ', err.msg)
    else:
        pass
    db.commit()
    cursor.close()
    db.close()


def db_get_save_var(name, telegram_id, getting_var):
    var = None
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT {getting_var} FROM users WHERE(telegramID = {telegram_id});'
    cursor.execute(command)
    try:
        records = cursor.fetchall()
        for row in records:
            var = row[0]
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return var


def db_get_admin_group_id(name):
    admin_group_id = None
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT telegramID FROM users WHERE(user_type = %s);'
    cursor.execute(command, ('admin_group',))
    try:
        records = cursor.fetchall()
        for row in records:
            admin_group_id = row[0]
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return admin_group_id


def db_get_user_info(name, telegram_id):
    read_user = None
    enroll_id = None
    list_user_groups = []
    list_user_enrolls = []
    already_learn = []
    enroll_to_group = []
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT * FROM users WHERE(telegramID = %s);'
    cursor.execute(command, (telegram_id,))
    try:
        records = cursor.fetchall()
        row = records[0]
        already_learn = str_to_list(row[5])
        enroll_to_group = str_to_list(row[6])
        for group in already_learn:
            al_group, al_course, course_id, category_id = db_get_group_info(name, group)
            list_user_groups.append([al_course, al_group])
        for enroll_id in enroll_to_group:
            en_group, en_course, course_id, category_id = db_get_group_info(name, enroll_id)
            list_user_enrolls.append([en_course, en_group])
        read_user = [row[2], row[3], row[4], list_user_groups, list_user_enrolls, row[7]]
    except Error:
        print("Error reading data from MySQL table", Error)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()
    return read_user, enroll_id, already_learn, enroll_to_group


def db_accept_enroll(name, telegram_id, enroll):
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT enroll FROM users WHERE(telegramID = {telegram_id});'
    cursor.execute(command)
    try:
        enroll = int(enroll)
        db_enroll = (cursor.fetchall()[0][0])
        db_enroll = str_to_list(db_enroll)
        if enroll in db_enroll:

            db_enroll.remove(enroll)
        else:
            print(f'deleting enroll error: this ({enroll})enroll is not found')
            return

        new_enroll = str(db_enroll)
        if len(db_enroll) == 0:
            new_enroll = '[]'
        command = f"UPDATE users SET enroll = %s WHERE (telegramID = {telegram_id});;"
        cursor.execute(command, (new_enroll,))

        command = f"SELECT group_id FROM users WHERE (telegramID = {telegram_id});"
        cursor.execute(command)
        records = cursor.fetchone()[0]
        groups = str_to_list(records)
        if len(groups) == 0:
            groups = [enroll]
            new_groups = str(groups)

            command = f"UPDATE users SET group_id = %s WHERE (telegramID = {telegram_id});"
            cursor.execute(command, (new_groups,))
            db.commit()
        elif enroll in groups:
            print('db_accept_enroll : enroll are the same with one of student groups')
            return
        else:
            groups.append(enroll)
            new_groups = str(groups)

            command = f"UPDATE users SET group_id = %s WHERE (telegramID = {telegram_id});"
            cursor.execute(command, (new_groups,))
            db.commit()

    except mysql.connector.Error as err:
        print('add db_accept_enroll: ', err.msg)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


def db_delete_enroll(name, telegram_id, enroll):
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT enroll FROM users WHERE telegramID = {telegram_id}'
    cursor.execute(command)
    try:
        records = cursor.fetchone()[0]
        cur_enroll = str_to_list(records)
        if enroll in cur_enroll:
            cur_enroll.remove(enroll)
        else:
            print('db_delete_enroll : enroll are not found in db row')
            return
        db_save_var(name, telegram_id, 'enroll', str(cur_enroll))
        db.commit()
    except mysql.connector.Error as err:
        print('db_delete_enroll: ', err.msg)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


def db_get_group_students(name, group_id):
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT telegramID, group_id FROM users'
    cursor.execute(command)
    matched_users = []
    users_names = []
    try:
        records = cursor.fetchall()
        for row in records:
            user_groups = str_to_list(row[1])
            if group_id in user_groups:
                matched_users.append(row[0])

    except mysql.connector.Error as err:
        print('db_get_group_students read id err:', err.msg)
    for user in matched_users:
        command = f'SELECT name FROM users WHERE telegramID = {user};'
        try:
            cursor.execute(command)
            user_in_group = cursor.fetchone()
            users_names.append((user, user_in_group[0]))

        except mysql.connector.Error as err:
            print(f'db_get_group_students read name of {user} err:', err.msg)
    if db.is_connected():
        db.close()
        cursor.close()

    return users_names


def db_get_trainer_courses(name):
    db = db_connect(name)
    cursor = db.cursor()
    trainers = {}
    all_names = []
    sorted_names = []
    command = f'SELECT id, category_id, teacher FROM courses'
    try:
        cursor.execute(command)
        records = cursor.fetchall()
        for row in records:

            names = row[2].split(',')
            if len(names) > 1:
                for name in names:
                    cur_trainer = str(name).strip()
                    trainers[cur_trainer] = []
            else:
                cur_trainer = str(names[0]).strip()
                trainers[cur_trainer] = []

        for row in records:
            trainer_groups = []

            command = f'SELECT id FROM groups WHERE course_id = {row[0]} AND category_id = {row[1]} '
            cursor.execute(command)
            course_groups = cursor.fetchall()
            if len(course_groups) > 0:
                for groups in course_groups:
                    trainer_groups.append(groups[0])
            else:
                trainer_groups = []
            names = row[2].split(',')
            if len(names) > 1:
                for name in names:
                    cur_trainer = str(name).strip()
                    trainers[cur_trainer] = trainer_groups
            else:
                cur_trainer = str(names[0]).strip()
                trainers[cur_trainer] = trainer_groups

        for i in trainers.keys():
            all_names.append(i)
        sorted_names = sorted(all_names, key=lambda n: n[3:])
    except mysql.connector.Error as err:
        print(f'db_get_trainer_courses err:', err.msg)
    return sorted_names, trainers


def db_delete_student_from_group(name, telegram_id, group_id):
    db = db_connect(name)
    cursor = db.cursor()
    command = f'SELECT group_id FROM users WHERE telegramID = {telegram_id}'
    try:
        cursor.execute(command)
        user_groups = cursor.fetchone()
        user_groups = str_to_list(user_groups[0])
        print('T_ID :', telegram_id, 'User Groups :', user_groups, type(user_groups), 'Delete from:', group_id, )
        user_groups.remove(int(group_id))
        db_save_var(name, telegram_id, 'group_id', str(user_groups))
        db.commit()
    except mysql.connector.Error as err:
        print(f'db_delete_student_from_group err:', err.msg)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


def db_compare_tables(name, html):
    db = db_connect(name)
    cursor = db.cursor()
    soup = BeautifulSoup(html.text, 'html.parser')
    topics = soup.find_all('div', class_='short')
    counter = 1
    for topic in topics:
        print(topic.text)
        db_add_category(DB_NAME, counter, topic.text, 'category_compare')
        counter += 1
    command = '''select topic_name from category;'''
    second_command = 'select topic_name from category_compare'
    try:
        cursor.execute(command)
        first_table = cursor.fetchall()
        cursor.execute(second_command)
        second_table = cursor.fetchall()
        print(first_table)
        print(second_table)
        print(first_table == second_table)
        ReWrite: bool = True if first_table != second_table else False

        if len(first_table) == len(first_table):
            for i in range(1,len(first_table)+1):
                command = f"UPDATE category SET id = {i}, topic_name = '{second_table[i-1][0]}' WHERE id = {i}"

                cursor.execute(command)
        elif len(first_table) > len(second_table):
            pass
        elif len(first_table) < len(second_table):
            pass
        else:
            pass


        db.commit()
    except mysql.connector.Error as err:
        print(f'db_delete_student_from_group err:', err.msg)
    finally:
        if db.is_connected():
            db.close()
            cursor.close()


#
# db_create_tables(DB_NAME)
# db_add_group(DB_NAME,'17:00',1,2,1)
# db = db_connect(DB_NAME)
# cursor = db.cursor()
# command = 'select * from groups'
# cursor.execute(command)
# records = cursor.fetchall()
# for row in records:
#     print(row)
# cursor.execute('drop table courses, groups')
# db.commit()
# db_create_tables(DB_NAME)
#
# for row in records:
#     command ='insert into groups' \
#                   '(id,daytime, offline,course_id, category_id, course_name, category_name)' \
#                   'values (%s, %s, %s, %s, %s, %s, %s);'
#     cursor.execute(command, row)
# db.commit()
# db.close()
# cursor.close()


