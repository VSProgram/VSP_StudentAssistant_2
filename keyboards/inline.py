from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from datetime import datetime
from datetime import timedelta
from calendar import Calendar
from calendar import monthrange

from db import DatBase
from db import Add_semester_db

date_b = DatBase()
sem_db = Add_semester_db()
def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

def menu():
    rez_db_last_sem = sem_db.select_last_semester()

    builder = InlineKeyboardBuilder()
    builder.button(text= f'Семестр № {rez_db_last_sem[0][0]}',callback_data=f'семестр_{rez_db_last_sem[0][0]}')
    builder.button(text='Домашка',callback_data='домашка')
    builder.button(text='Лекция',callback_data='лекция')
    builder.button(text='Семинар',callback_data='семинар')
    builder.button(text='Семестр',callback_data='семестр')
    builder.button(text='Заметки и справочные материалы',callback_data='заметки')
    builder.button(text='Общая информация',callback_data='инфа')
    builder.button(text='Сообщить об ошибке',url='https://t.me/Sasha_rama')

    builder.adjust(1,2, 2, 1,1,1)
    return builder.as_markup()

def menu_user():
    rez_db_last_sem = sem_db.select_last_semester()

    builder = InlineKeyboardBuilder()
    builder.button(text= f'Семестр № {rez_db_last_sem[0][0]}',callback_data=f'семестр_{rez_db_last_sem[0][0]}')
    builder.button(text='Домашка',callback_data='домашка_user')
    builder.button(text='Лекция',callback_data='лекция_user')
    builder.button(text='Семинар',callback_data='семинар_user')
    builder.button(text='Заметки и справочные материалы',callback_data='заметки_user')
    builder.button(text='Общая информация',callback_data='инфа_user')
    builder.button(text='Сообщить об ошибке',url='https://t.me/Sasha_rama')

    builder.adjust(1,1, 2, 1,1,1)
    return builder.as_markup()
def get_inlineMix_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (1,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()

class Paginationdata(CallbackData,prefix = 'pag2'):
    action:  str
    now_m: int
    now_y: int



class Paginationdata2(CallbackData,prefix = 'pag3'):
    action:  str
    now_m: int
    now_y: int

def create_rat(now_m = 0, now_y = 0):

    builder = InlineKeyboardBuilder ()

    now = datetime.now()

    if now.month + now_m in range(1,13):
        if (now.day == 31) and (now.month in [1, 3, 5, 7, 8, 10, 11]):
            mon_f = now.replace(day=1,month=now.month + now_m)
        else:
            mon_f = now.replace(month=now.month + now_m)

    year_f = now.replace(year=now.year + now_y)

    a = Calendar()
    m = a.monthdays2calendar(year=year_f.year, month=mon_f.month)
    m2 = monthrange(month=now.month,year=now.year)
    print(m2[1])
    mon = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь','Декабрь']

    builder.button(text='Отмена', callback_data='отмена')
    builder.button(text=f'Сегодня - {now.day} {mon[now.month - 1]} {now.year}', callback_data=' ')

    for i in range(len(mon)+1):
        if i == mon_f.month:
            builder.button(text=f'{mon[i - 1]} {year_f.year}',callback_data=' ')

    builder.button(text='Прошлый месяц', callback_data=Paginationdata(action='prosh', now_m=now_m, now_y=now_y).pack())
    builder.button(text='Следующий месяц', callback_data=Paginationdata(action = 'sled',now_m = now_m , now_y = now_y).pack())

    dn = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for i in dn:
        builder.button(text=f'{i}',callback_data=' ')

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j][0] == 0:
                builder.button(text=' ',callback_data=' ')
            elif m[i][j][0] > 0:
                if (now.day == 31) and (now.month in [1, 3, 5, 7, 8, 10, 11]):
                    builder.button(text=f'{m[i][j][0]}', callback_data=f'{m[i][j][0]}-{now.replace(month=now.month + now_m,day=1).strftime("%m")}-{now.replace(year=now.year + now_y).strftime("%Y")}')
                else:
                    builder.button(text=f'{m[i][j][0]}', callback_data=f'{m[i][j][0]}-{now.replace(month=now.month + now_m).strftime("%m")}-{now.replace(year=now.year + now_y).strftime("%Y")}')

    if (now.month == 12) and now.day in [25,26,27,28,29,30,31]:

        len_now_month = m2[1] - now.day
        len_next_month = 7 - len_now_month
        builder.button(text='Через неделю', callback_data=f'{len_next_month}-{now.replace(month=1).strftime("%m")}-{now.replace(year=now.year+1).strftime("%Y")}')

    else:
        if now.day + 7 <= m2[1]:
            builder.button(text='Через неделю', callback_data=f'{now.replace(day=now.day+7).strftime("%d")}-{now.replace(month=now.month).strftime("%m")}-{now.replace(year=now.year).strftime("%Y")}')
        else:
            len_now_month = m2[1] - now.day

            len_next_month = 7 - len_now_month
            builder.button(text='Через неделю', callback_data=f'{len_next_month}-{now.replace(month=now.month + 1).strftime("%m")}-{now.replace(year=now.year).strftime("%Y")}')
    builder.adjust(1,1,1,2,7,7,7,7,7,7,7,1)
    return builder.as_markup()

def create_rat_lp(now_m = 0, now_y = 0):

    builder = InlineKeyboardBuilder ()

    now = datetime.now()

    if now.month + now_m in range(1,13):
        if (now.day == 31) and (now.month in [1, 3, 5, 7, 8, 10, 11]):
            mon_f = now.replace(day=1,month=now.month + now_m)
        else:
            mon_f = now.replace(month=now.month + now_m)

    year_f = now.replace(year=now.year + now_y)

    a = Calendar()
    m = a.monthdays2calendar(year=year_f.year, month=mon_f.month)


    mon = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь','Декабрь']

    builder.button(text='Отмена', callback_data='отмена')
    builder.button(text=f'Сегодня - {now.day} {mon[now.month - 1]} {now.year}', callback_data=' ')

    for i in range(len(mon)+1):
        if i == mon_f.month:
            builder.button(text=f'{mon[i - 1]} {year_f.year}',callback_data=' ')

    builder.button(text='Прошлый месяц', callback_data=Paginationdata2(action='prosh', now_m=now_m, now_y=now_y).pack())
    builder.button(text='Следующий месяц', callback_data=Paginationdata2(action = 'sled',now_m = now_m , now_y = now_y).pack())

    dn = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for i in dn:
        builder.button(text=f'{i}',callback_data=' ')

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j][0] == 0:
                builder.button(text=' ',callback_data=' ')
            elif m[i][j][0] > 0:
                if (now.day == 31) and (now.month in [1, 3, 5, 7, 8, 10, 11]):
                    builder.button(text=f'{m[i][j][0]}', callback_data=f'{m[i][j][0]}-{now.replace(month=now.month + now_m,day=1).strftime("%m")}-{now.replace(year=now.year + now_y).strftime("%Y")}')
                else:
                    builder.button(text=f'{m[i][j][0]}', callback_data=f'{m[i][j][0]}-{now.replace(month=now.month + now_m).strftime("%m")}-{now.replace(year=now.year + now_y).strftime("%Y")}')

    builder.button(text='Сегодня',callback_data=f'{now.day}-{now.month}-{now.year}')

    builder.adjust(1,1,1,2,7,7,7,7,7,7,7,1)
    return builder.as_markup()


def del_db_btns_user(date_db,type_note_2 = None):
    builder = InlineKeyboardBuilder()

    if type_note_2 == 'l':
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='показать лекцию_2_user')

                builder.button(text=f'Назад', callback_data=f'назад_лекция_выбор_user')
                builder.button(text=f'Меню', callback_data=f'отмена_user')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена_user')
                builder.button(text=f'Назад', callback_data=f'назад_лекция_выбор_user')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)
    elif type_note_2 == 'p':
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='показать семинар_2_user')

                builder.button(text=f'Назад', callback_data=f'назад_семинар_выбор_user')
                builder.button(text=f'Меню', callback_data=f'отмена_user')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена_user')
                builder.button(text=f'Назад', callback_data=f'назад_семинар_выбор_user')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)

    else:
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='показать домашку_2_user')

                builder.button(text=f'Назад', callback_data=f'назад_домашка_выбор_user')
                builder.button(text=f'Меню', callback_data=f'отмена_user')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена_user')
                builder.button(text=f'Назад', callback_data=f'назад_домашка_выбор_user')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)


def del_db_btns(date_db,type_note=None,type_note_2 = None):
    builder = InlineKeyboardBuilder()

    if type_note_2 == 'l':
        if type_note == 'd':
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='удалить лекцию_2')
                builder.button(text=f'Назад', callback_data=f'назад_удалить_выбор_лекция')
                builder.button(text=f'Меню', callback_data=f'отмена')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена')
                builder.button(text=f'Назад', callback_data=f'назад_удалить_выбор_лекция')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)
        else:
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='показать лекцию_2')

                builder.button(text=f'Назад', callback_data=f'назад_лекция_выбор')
                builder.button(text=f'Меню', callback_data=f'отмена')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена')
                builder.button(text=f'Назад', callback_data=f'назад_лекция_выбор')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)
    elif type_note_2 == 'p':
        if type_note == 'd':
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='удалить семинар_2')
                builder.button(text=f'Назад', callback_data=f'назад_удалить_выбор_семинар')
                builder.button(text=f'Меню', callback_data=f'отмена')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена')
                builder.button(text=f'Назад', callback_data=f'назад_удалить_выбор_семинар')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)
        else:
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет', callback_data='показать семинар_2')

                builder.button(text=f'Назад', callback_data=f'назад_семинар_выбор')
                builder.button(text=f'Меню', callback_data=f'отмена')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена')
                builder.button(text=f'Назад', callback_data=f'назад_семинар_выбор')

                for i in set(date_db):
                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)

    else:
        if type_note == 'd':
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет',callback_data='удалить домашку_2')
                builder.button(text=f'Назад', callback_data=f'назад_удалить_выбор')
                builder.button(text=f'Меню', callback_data=f'отмена')

                builder.adjust(1, 1)
            else:
                builder.button(text='Отмена', callback_data='отмена')
                builder.button(text=f'Назад', callback_data=f'назад_удалить_выбор')

                for i in set(date_db):

                    s = str(i[0]).split('-')
                    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
            return builder.as_markup(resize_keyboard=True)
        else:
            if len(date_db) == 0:
                builder.button(text='Выбрать предмет',callback_data='показать домашку_2')

                builder.button(text=f'Назад', callback_data=f'назад_домашка_выбор')
                builder.button(text=f'Меню', callback_data=f'отмена')

                builder.adjust(1,1)
            else:
                builder.button(text='Отмена', callback_data='отмена')
                builder.button(text=f'Назад', callback_data=f'назад_домашка_выбор')

                for i in set(date_db):

                    s = str(i[0]).split('-')
                    dat_2_rez = s[2]+'.'+s[1]+'.'+s[0]
                    builder.button(text=f'{dat_2_rez}', callback_data=f'{i[0]}')
                builder.adjust(1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3)
            return builder.as_markup(resize_keyboard=True)


def del_db_vse_btns(date_db,type_note = None):
    builder = InlineKeyboardBuilder()

    if type_note == 'l':
        builder.button(text=f'Отмена', callback_data = f'отмена')
        builder.button(text=f'Назад', callback_data = f'назад_удалить_выбор_лекция')
    elif type_note == 'p':
        builder.button(text=f'Отмена', callback_data = f'отмена')
        builder.button(text=f'Назад', callback_data = f'назад_удалить_выбор_семинар')

    elif type_note == 'r':
        builder.button(text=f'Отмена', callback_data = f'отмена')
        builder.button(text=f'Назад', callback_data = f'удалить заметки_2')


    elif type_note == 'on':
        builder.button(text=f'Отмена', callback_data = f'отмена')
        builder.button(text=f'Назад', callback_data = f'удалить инфа_2')
    else:
        builder.button(text=f'Отмена', callback_data = f'отмена')
        builder.button(text=f'Назад', callback_data = f'назад_удалить_выбор')


    for i in range(len(date_db)):
        builder.button(text=f'{date_db[i][0]}', callback_data=f'{date_db[i][0]}')

    builder.adjust(1,1,6,repeat=True)
    return builder.as_markup(resize_keyboard=True)


def add_hw(semester,type_note):
    builder = InlineKeyboardBuilder()
    rez_db = date_b.select_subject(semester)

    builder.button(text=f'Отмена', callback_data = f'отмена')
    builder.button(text=f'Назад', callback_data = f'{type_note}')



    for i in range(len(rez_db)):
        builder.button(text=f'{rez_db[i][0]}',callback_data=f'{rez_db[i][0]}')

    builder.adjust(1,repeat=True)
    return builder.as_markup(resize_keyboard=True)


def select_other_notes():
    builder = InlineKeyboardBuilder()
    rez_db = date_b.select_name_note()

    builder.button(text=f'Отмена', callback_data = f'отмена')
    builder.button(text=f'Назад', callback_data = f'инфа')
    #
    # for i in range(110):
    #     builder.button(text=f'{[i]}',callback_data=f'{i}')


    for i in range(len(rez_db)):
        builder.button(text=f'{rez_db[i][0]}',callback_data=f'{rez_db[i][0]}')

    builder.adjust(1,repeat=True)
    return builder.as_markup(resize_keyboard=True)




def select_all_semester(semester):
    builder = InlineKeyboardBuilder()

    for i in  range(len(semester)):
        builder.button(text=f'{semester[i][0]}',callback_data=f'{semester[i][0]}')

    builder.button(text=f'Назад', callback_data = f'семестр')
    builder.button(text=f'Отмена', callback_data = f'отмена')

    builder.adjust(1, repeat=True)
    return builder.as_markup(resize_keyboard=True)


