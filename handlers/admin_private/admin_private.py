from aiogram import F, Router, types, Bot
from aiogram.filters import Command,StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup , State
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.methods import send_media_group
from aiogram.methods.send_media_group import SendMediaGroup
from aiogram.enums import ParseMode

from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

from midllewares.middle_album import AlbumMiddleware

from typing import Any, Awaitable, Callable, Dict, List, Union

import time
from datetime import datetime
from datetime import timedelta

import ast

from db import DatBase,Add_semester_db

from filters.chat_types import ChatTypeFilter,IsUser,IsAdmin
from keyboards.inline import get_callback_btns,get_inlineMix_btns,create_rat,Paginationdata,del_db_btns,del_db_vse_btns,add_hw,select_all_semester,menu
sem_db = Add_semester_db()
date_b = DatBase()
admin_router = Router()
admin_router.message.middleware(AlbumMiddleware())
admin_router.message.filter(ChatTypeFilter(["private"]),IsAdmin())

subject_ed = []
subject_ed_del = []
semester_ed_del = []

chat_id = -1002168145795


@admin_router.message(StateFilter('*'),Command("admin"))
async def add_product(message: types.Message,state: FSMContext):
    g_state = await state.get_data()

    if g_state is None:
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        await state.clear()
        await message.answer("<<<Меню>>>", reply_markup=menu())

# @admin_router.message(StateFilter('*'),Command("admin2"))
# async def add_product(message: types.Message,state: FSMContext,bot:Bot):
    # chat_members = await bot.get_chat_member(-1002168145795,user_id=message.from_user.id)

    # admins_list = await bot.get_chat_administrators(-1002168145795)
    #
    # admins_list = [
    #     member.user.id
    #     for member in admins_list
    #     if member.status == "creator" or member.status == "administrator"
    # ]
    #



    # admins_list = await bot.get_chat_member(-1002168145795,user_id=message.from_user.id)
    #
    # admins_list = [
    #     member
    #     for member in admins_list
    # ]
    #

@admin_router.message(StateFilter('*'),Command("admin3"))
async def add_product(message: types.Message,bot:Bot):
    await bot.send_message(chat_id=-1002242682010,text='acecqacqcqccqe')


@admin_router.callback_query(F.data == 'назад')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Меню>>>", reply_markup=menu())



@admin_router.callback_query(StateFilter('*'),F.data.lower() == 'отмена')
async def write_date(call: types.CallbackQuery,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.edit_text("<<<Меню>>>", reply_markup=menu())

@admin_router.message(StateFilter('*'),F.text.lower() == 'отмена')
async def write_date(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())


@admin_router.message(F.text.lower() == 'меню')
async def menu_hw(message: types.Message):
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())


@admin_router.callback_query(StateFilter('*'),F.data == 'домашка')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_del.clear()
    subject_ed.clear()

    await callback.message.edit_text("<<<Домашка>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать домашку':'показать домашку',
        'Добавить домашку':'добавить домашку',
        'Изменить домашку': 'изменить лекцию',
        'Удалить домашку':'удалить домашку',
        'Назад':'назад'
    },sizes=(2,2)))


# @admin_router.callback_query(F.data == 'семинар')
# async def menu_hw(callback: CallbackQuery):
#     await callback.message.edit_text("<<<Семинар>>>", reply_markup=get_inlineMix_btns(btns={
#         'Показать семинар':'показать семинар',
#         'Добавить семинар':'добавить семинар',
#         'Изменить семинар': 'изменить семинар',
#         'Удалить семинар':'удалить семинар',
#         'Назад':'назад'
#     },sizes=(2,2)))
#
#
# @admin_router.callback_query(F.data == 'лекция')
# async def menu_hw(callback: CallbackQuery):
#     await callback.message.edit_text("<<<Лекция>>>", reply_markup=get_inlineMix_btns(btns={
#         'Показать лекцию':'показать лекцию',
#         'Добавить лекцию':'добавить лекцию',
#         'Изменить лекцию': 'изменить лекцию',
#         'Удалить лекцию':'удалить лекцию',
#         'Назад':'назад'
#     },sizes=(2,2)))




@admin_router.callback_query(F.data == 'семестр')
async def menu_hw(callback: CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text("<<<Семестр>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать семестр': 'показать семестр',
        'Добавить семестр': 'добавить семестр',
        'Изменить семестр': 'изменить семестр',
        'Удалить семестр': 'удалить семестр',
        'Назад': 'назад'

    }, sizes=(2, 2, 1)))


# Добавить_семестр-----------------------------------------------------
class Add_semester(StatesGroup):
    number_sem = State()
    subject_sem = State()

@admin_router.callback_query(StateFilter(None),F.data == 'добавить семестр')
async def menu_hw(callback: CallbackQuery,state: FSMContext):
    await callback.message.edit_text('Введите номер семестра!\n\nВведите "Отмена" для полной отмены"',reply_markup=None)
    await state.set_state(Add_semester.number_sem)

@admin_router.message(Add_semester.number_sem,F.text)
async def menu_hw(message: types.Message,state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())
    elif str.isdigit(message.text) == True:
        if int(message.text) in range(1, 20):
            await state.update_data(number_sem=int(message.text))
            await message.answer(
                'Введите предметы этого семестра\n•По порядку\n•Через запятую\n•Без пробелов\n•Название предмета должно содержать менее 34 символов(включая пробелы)\n\nНапример:Иностранный язык,Маркетинг,БЖД,ТВиМС,Программирование,Искусственный интеллект,Базы данных,ИБиЗИ,Операционные системы,Информационный дизайн,Физкультура,Ознакомительная практика\n\n•Введите "Отмена" для полной отмены')
            await state.set_state(Add_semester.subject_sem)
        else:
            await message.answer(f'Введите более корректое число!')
            return
    else:
        await message.answer(f'Введите число!')
        return


@admin_router.message(Add_semester.subject_sem,F.text)
async def menu_hw(message: Message,state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        slov = message.text.split(',')
        for i in slov:
            if len(i)>34:
                await message.answer('Одно из названий превышает 34 символа!')
                return
        await state.update_data(subject_sem = message.text)
        rez_state = await state.get_data()
        turp_rez = tuple(rez_state.values())
        turp_sub = turp_rez[1].split(',')
        sem_db.sem_vse(data=f'{turp_rez[0]}')
        sem_db.create_common(num_sem=turp_rez[0])
        sem_db.create_semester_subject(num_sem=turp_rez[0])
        for i in turp_sub:
            sem_db.add_subject(num_sem=turp_rez[0],data=i)
        await message.answer('Семестр добавлен!')
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())


# Добавить_семестр-----------------------------------------------------


# удалить_семестр-----------------------------------------------------

class DelSemester(StatesGroup):
    number_semester = State()
    yes = State()

@admin_router.callback_query(StateFilter('*'),F.data == 'удалить семестр')
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await state.clear()
    rez_db = sem_db.select_all_semester()
    await call.message.edit_text("Какой семестр удалить?", reply_markup=select_all_semester(rez_db))
    await state.set_state(DelSemester.number_semester)


@admin_router.callback_query(DelSemester.number_semester,F.data)
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await state.update_data(number_semester = call.data)
    rez_db = date_b.select_subject(semester=call.data)
    message_sub = ''
    for i in range(len(rez_db)):
        sub_i = rez_db[i][0]
        message_sub = f'{message_sub + sub_i}\n'
    await call.message.answer(text=f'Вы хотите удалить семестр с этими предметами?\n\nСеместр №{call.data}\n\n{message_sub}',reply_markup=get_inlineMix_btns(btns={
            'Да':'да_семестр',
            'Нет':'удалить семестр',
            'Отмена': 'отмена',
        }, sizes=(1, 1, 1)))
    await state.set_state(DelSemester.yes)

@admin_router.callback_query(DelSemester.yes,F.data == 'да_семестр')
async def menu_hw(call: CallbackQuery,state:FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    await state.clear()
    sem_db.delete_all_table(date_turp[0])

    sem_db.delete_semester_from_vse(date_turp[0])
    await call.message.edit_text('Удалил!')
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())





# удалить_семестр-----------------------------------------------------


# изменить_семестр-----------------------------------------------------


class ChangeSemester(StatesGroup):

    number_semester = State()
    yes = State()
    number_semester_new = State()
    subject_semester = State()

@admin_router.callback_query(StateFilter('*'),F.data == 'изменить семестр')
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await state.clear()
    rez_db = sem_db.select_all_semester()
    await call.message.edit_text('Какой семестр изменить? ', reply_markup=select_all_semester(rez_db))
    await state.set_state(ChangeSemester.number_semester)


@admin_router.callback_query(ChangeSemester.number_semester,F.data)
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await state.update_data(number_semester = call.data)

    rez_db = date_b.select_subject(semester=call.data)
    await state.update_data(subject_semester = rez_db)
    message_sub = ''
    for i in range(len(rez_db)):
        sub_i = rez_db[i][0]
        message_sub = f'{message_sub + sub_i}\n'
    await call.message.answer(text=f'Вы хотите изменить семестр с этими предметами?\n\nСеместр №{call.data}\n\n{message_sub}',reply_markup=get_inlineMix_btns(btns={
            'Да':'да_семестр2',
            'Нет':'изменить семестр',
            'Отмена': 'отмена',
        }, sizes=(1, 1, 1)))
    await state.set_state(ChangeSemester.yes)


@admin_router.callback_query(ChangeSemester.yes,F.data == 'да_семестр2')
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await call.message.edit_text('Введите новый номер семестра\nВведите "-" если хотите оставить номер семестра\n\nВведите "Отмена" для полной отмены')
    await state.set_state(ChangeSemester.number_semester_new)


@admin_router.message(ChangeSemester.number_semester_new,F.text)
async def menu_hw(message: types.Message,state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())
    elif str.isdigit(message.text) == True:
        if int(message.text) in range(1, 20):
            await state.update_data(number_semester_new=int(message.text))
            await message.answer(
                'Введите предметы этого семестра\n•По порядку\n•Через запятую\n•Без пробелов\n•Название предмета должно содержать менее 34 символов(включая пробелы)\n\nНапример:Иностранный язык,Маркетинг,БЖД,ТВиМС,Программирование,Искусственный интеллект,Базы данных,ИБиЗИ,Операционные системы,Информационный дизайн,Физкультура,Ознакомительная практика\n\n•Введите "-" если хотите оставить предметы\n•Введите "Отмена" для полной отмены')
            await state.set_state(ChangeSemester.subject_semester)
        else:
            await message.answer(f'Введите более корректое число!')
            return
    elif message.text == '-':
        await state.update_data(number_semester_new=message.text)
        await message.answer(
            'Введите предметы этого семестра\n•По порядку\n•Через запятую\n•Без пробелов\n•Название предмета должно содержать менее 34 символов(включая пробелы)\n\nНапример:Иностранный язык,Маркетинг,БЖД,ТВиМС,Программирование,Искусственный интеллект,Базы данных,ИБиЗИ,Операционные системы,Информационный дизайн,Физкультура,Ознакомительная практика\n\n•Введите "-" если хотите оставить предметы\n•Введите "Отмена" для полной отмены')
        await state.set_state(ChangeSemester.subject_semester)

    else:
        await message.answer(f'Введите число!')
        return


@admin_router.message(ChangeSemester.subject_semester,F.text)
async def menu_hw(message: types.Message,state: FSMContext):
    await state.update_data(subject_sem=message.text)
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    if (date_turp[2] == '-') and (date_turp[3] == '-'):
        await message.answer('Не изменили ни семестр,ни предметы!')
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())
    elif (date_turp[2] == '-') and (date_turp[3] != '-'):
        sem_db.delete_all_subject(date_turp[0])
        slov = date_turp[3].split(',')
        for i in slov:
            if len(i)>34:
                await message.answer('Одно из названий превышает 34 символа!')
                return
        for i in slov:
            sem_db.add_subject(num_sem=date_turp[0], data=i)

        await message.answer('Изменили только предметы!')
        await state.clear()

        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())

    elif (date_turp[2] != '-') and (date_turp[3] == '-'):
        sem_db.update_semester_vse(number_semester_new=date_turp[2],number_semester_old=date_turp[0])
        sem_db.update_name_table_subject(number_semester_new=date_turp[2],number_semester_old=date_turp[0])
        sem_db.update_name_table_common(number_semester_new=date_turp[2],number_semester_old=date_turp[0])
        await message.answer('Изменили только семестр!')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())

    elif (date_turp[2] != '-') and (date_turp[3] != '-'):
        sem_db.delete_all_subject(date_turp[0])
        slov = date_turp[3].split(',')
        for i in slov:
            if len(i) > 34:
                await message.answer('Одно из названий превышает 34 символа!')
                return
        for i in slov:
            sem_db.add_subject(num_sem=date_turp[0], data=i)
        sem_db.update_semester_vse(number_semester_new=date_turp[2],number_semester_old=date_turp[0])
        sem_db.update_name_table_subject(number_semester_new=date_turp[2],number_semester_old=date_turp[0])
        sem_db.update_name_table_common(number_semester_new=date_turp[2],number_semester_old=date_turp[0])
        await message.answer('Изменили и семестр,и предметы!')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())

# изменить_семестр-----------------------------------------------------


# показать_семестр-----------------------------------------------------
class SelectSemester(StatesGroup):

    number_semester = State()
    yes = State()


@admin_router.callback_query(StateFilter('*'),F.data == 'показать семестр')
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await state.clear()
    rez_db = sem_db.select_all_semester()
    await call.message.edit_text('Какой семестр показать? ', reply_markup=select_all_semester(rez_db))
    await state.set_state(SelectSemester.number_semester)


@admin_router.callback_query(SelectSemester.number_semester,F.data)
async def menu_hw(call: CallbackQuery,state:FSMContext):
    await state.update_data(number_semester = call.data)

    rez_db = date_b.select_subject(semester=call.data)
    await state.update_data(subject_semester = rez_db)
    message_sub = ''
    for i in range(len(rez_db)):
        sub_i = rez_db[i][0]
        message_sub = f'{message_sub + sub_i}\n'
    await call.message.edit_text(text=f'Семестр №{call.data}\n\n{message_sub}',reply_markup=None)

    await call.message.answer(
        text=f'Посмотреть ещё?',
        reply_markup=get_inlineMix_btns(btns={
            'Да': 'показать семестр',
            'Нет': 'отмена',
            'Назад':'показать семестр'
        }, sizes=(1, 1)))

# показать_семестр-----------------------------------------------------


# Добавить_домашку-----------------------------------------------------
class AddNote(StatesGroup):
    subject = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    second_date = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@admin_router.callback_query(StateFilter(None),F.data.lower() == 'добавить домашку')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='домашка'))
    await state.set_state(AddNote.subject)


@admin_router.callback_query(AddNote.subject,F.data)
async def dz2(call: CallbackQuery,  state: FSMContext):
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M")
    await state.update_data(subject = call.data)
    await state.update_data(first_date = formatted_time)
    await state.update_data(name_creator = call.from_user.full_name)
    await state.update_data(id_creator=call.from_user.id)
    await call.message.edit_text(text='Выберете дату!', reply_markup=create_rat())
    await state.set_state(AddNote.second_date)


@admin_router.callback_query(Paginationdata.filter(F.action.in_(['sled','prosh'])))
async def pagin4ik(call:CallbackQuery,callback_data:Paginationdata):
    now = datetime.now()

    page_num_m = int(callback_data.now_m)
    page_num_y = int(callback_data.now_y)

    if callback_data.action =='prosh':
        if page_num_m + now.month < 2:
            page_m = 12 - now.month
            page_y = page_num_y - 1
        else:
            page_y = page_num_y
            page_m = page_num_m - 1

    if callback_data.action =='sled':
        if page_num_m + now.month > 11:
            page_m = page_num_m - 11
            page_y = page_num_y +1
        else:
            page_y = page_num_y
            page_m = page_num_m + 1

    with suppress(TelegramBadRequest):
        await call.message.edit_reply_markup(reply_markup=create_rat(now_m=page_m,now_y=page_y))
    await call.answer()


@admin_router.callback_query(AddNote.second_date,F.data.contains('-20'))
async def write_time(callback: types.CallbackQuery,  state: FSMContext):
    await state.update_data(second_date = callback.data)
    await callback.message.edit_text(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
    await state.set_state(AddNote.text_note)

@admin_router.message(AddNote.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote.id_photo)


@admin_router.message(AddNote.id_photo,F.photo)
async def c_change3(message: types.Message, state: FSMContext,album: List[Message] = None, phot: types.InputMediaPhoto = None):
    if message.media_group_id == None:
        phot = message.photo[-1].file_id
        await state.update_data(id_photo=phot)
    else:
        group_elements = []
        for element in album:
            input_media = element.photo[-1].file_id
            group_elements.append(input_media)
        await state.update_data(id_photo=str(group_elements))
    await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    await state.set_state(AddNote.id_doc)




@admin_router.message(AddNote.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@admin_router.message(AddNote.id_doc,F.document)
async def c_change3(message: types.Message,bot:Bot, state: FSMContext,album: List[Message] = None,docum : types.InputMediaDocument = None):
    if message.media_group_id == None:
        docum = message.document.file_id
        await state.update_data(id_doc=docum)
    else:
        group_elements = []
        for element in album:
            input_media = element.document.file_id
            group_elements.append(input_media)
            await state.update_data(id_doc=str(group_elements))


    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    sem_last = sem_db.select_last_semester()[0][0]
    date_b.add_note(data=data_turp,semester=str(sem_last),type_note='h')

    await message.answer(f'Домашка добавлена!')
    dat_2 = str(data_turp[4])
    s = dat_2.split('-')
    dat_2_rez = s[0] + '.' + s[1] + '.' + s[2]
    await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил домашку \n'
                                                        f'{data_turp[0]}\n'
                                                        f'Дата выполнения {dat_2_rez}')
    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())

@admin_router.message(AddNote.id_doc, F.text)
async def c_change3(message: types.Message, state: FSMContext,bot:Bot):

    if message.text.lower() =='-':
        await state.update_data(id_doc=message.text)

        date_zr = await state.get_data()
        data_turp = tuple(date_zr.values())

        sem_last = sem_db.select_last_semester()[0][0]
        date_b.add_note(data=data_turp, semester=str(sem_last), type_note='h')

        await message.answer(f'Домашка добавлена!')
        dat_2 = str(data_turp[4])
        s = dat_2.split('-')
        dat_2_rez = s[0] + '.' + s[1] + '.' + s[2]
        await bot.send_message(chat_id=chat_id,text=f'{data_turp[2]} добавил домашку \n'
                                                           f'{data_turp[0]}\n'
                                                           f'Дата выполнения {dat_2_rez}')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_домашку-----------------------------------------------------


# Показать_домашку-----------------------------------------------------


class ShowNote(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@admin_router.callback_query(StateFilter(None),F.data == 'показать домашку')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!', reply_markup=add_hw(rez_db[0][0],type_note='домашка'))
    await state.set_state(ShowNote.subject)


@admin_router.callback_query(StateFilter('*'),F.data == 'показать домашку_2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='домашка'))
    await state.set_state(ShowNote.subject)


@admin_router.callback_query(ShowNote.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed) == 0:
        subject_ed.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все',
        'По датам': 'по числам',
        'Назад': 'показать домашку_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(ShowNote.how_show)


@admin_router.callback_query(StateFilter('*'),F.data == 'назад_домашка_выбор')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все',
        'По датам': 'по числам',
        'Назад': 'показать домашку_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(ShowNote.how_show)


@admin_router.callback_query(StateFilter('*'),F.data == 'все')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')
    else:
        rez_db = date_b.check_count(subject=subject_ed[0], semester=str(rez_db_sem[0][0]), type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text('Домашки нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'показать домашку_2',
        'Назад':f'назад_домашка_выбор',
        'Меню': 'отмена'
            }))
    else:
        for i in range(len(rez_db)):

            dat_2 = str(rez_db[i][5])
            s = dat_2.split('-')
            dat_2_rez = s[2]+'.'+s[1]+'.'+s[0]

            dat_1 = str(rez_db[i][2])
            s = dat_1.split(' ')
            t1 = s[1].split(':')
            t2 = t1[0] + ':' + t1[1]
            m1 = s[0].split('-')
            m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
            dat_1_rez = m2 + ' ' + t2

            doc_8 = rez_db[i][8]
            if '[' in doc_8:


                list_doc = list(ast.literal_eval(doc_8))
            else:
                doc_8_new = '[' + '"'+doc_8 +'"'+ ']'


                list_doc = ast.literal_eval(doc_8_new)

            phot_7 = rez_db[i][7]
            if '[' in phot_7:
                list_media = list(ast.literal_eval(phot_7))
            else:
                phot_7_new = '[' + '"'+phot_7 +'"'+ ']'
                list_media = ast.literal_eval(phot_7_new)

            album_builder = MediaGroupBuilder(caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
            a = 0
            for element in range(len(list_media)):
                if list_media[element] != '-':
                    album_builder.add_photo(media=list_media[element])
                else:
                    a += 1

            album_builder_2 = MediaGroupBuilder()
            b = 0
            for element in range(len(list_doc)):
                if list_doc[element] != '-':
                    album_builder_2.add_document(media=list_doc[element])
                else:
                    b+=1
            if a == 1:
                await call.message.answer(f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Куда дальше?', reply_markup=get_inlineMix_btns(btns={
            'Выбрать по датам': 'ещё',
            'Выбрать предмет': 'показать домашку_2',
            'Меню': 'отмена',
        }))


@admin_router.callback_query(ShowNote.how_show,F.data == 'по числам')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Домашки нет!', reply_markup=del_db_btns(rez_db))
    else:
        await call.message.edit_text(text='Вот все домашние работы по числам!', reply_markup=del_db_btns(rez_db))
        await state.set_state(ShowNote.date_subject)


@admin_router.callback_query(StateFilter('*'),F.data == 'ещё')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed[0])
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Домашки нет!', reply_markup=del_db_btns(rez_db))
    else:
        await call.message.edit_text(text='Какую запись нужно показать?', reply_markup=del_db_btns(rez_db))
        await state.set_state(ShowNote.date_subject)


@admin_router.callback_query(ShowNote.date_subject,F.data.contains('20'))
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(date_subject = call.data)

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.select_subject_date(date_subject=data_turp[1],semester=str(rez_db_sem[0][0]),type_note='h',subject=data_turp[0])

    for i in range(len(rez_db)):

        dat_2 = str(rez_db[i][5])
        s = dat_2.split('-')
        dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]

        dat_1 = str(rez_db[i][2])
        s = dat_1.split(' ')
        t1 = s[1].split(':')
        t2 = t1[0] + ':' + t1[1]
        m1 = s[0].split('-')
        m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
        dat_1_rez = m2 + ' ' + t2

        doc_8 = rez_db[i][8]
        if '[' in doc_8:



            list_doc = list(ast.literal_eval(doc_8))
        else:
            doc_8_new = '[' + '"' + doc_8 + '"' + ']'


            list_doc = ast.literal_eval(doc_8_new)

        phot_7 = rez_db[i][7]
        if '[' in phot_7:
            list_media = list(ast.literal_eval(phot_7))
        else:
            phot_7_new = '[' + '"' + phot_7 + '"' + ']'
            list_media = ast.literal_eval(phot_7_new)

        album_builder = MediaGroupBuilder(
            caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
        a = 0
        for element in range(len(list_media)):
            if list_media[element] != '-':
                album_builder.add_photo(media=list_media[element])
            else:
                a += 1

        album_builder_2 = MediaGroupBuilder()
        b = 0
        for element in range(len(list_doc)):
            if list_doc[element] != '-':
                album_builder_2.add_document(media=list_doc[element])
            else:
                b += 1
        if a == 1:
            await call.message.answer(
                f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
            a = 0
        else:
            await call.message.answer_media_group(album_builder.build())
        if b == 1:
            await call.message.answer('Документов к этой записи нет!')
            b = 0
        else:
            await call.message.answer_media_group(album_builder_2.build())

    await state.clear()
    await call.message.answer('Посмотреть ещё?',reply_markup=get_inlineMix_btns(btns={
        'Да': 'ещё',
        'Нет': 'отмена',
        'Показать все':'все',
        'Назад':'назад_домашка_выбор'

    }))



# Удалить_домашку-----------------------------------------------------

class DelNote(StatesGroup):
    subject = State()
    how_show = State()
    del_subject = State()
    del_subject_2 = State()
    del_subject_2_2 = State()
    del_subject_3 = State()
    del_subject_4 = State()





@admin_router.callback_query(StateFilter(None),F.data == 'удалить домашку')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='домашка'))
    await state.set_state(DelNote.subject)

@admin_router.callback_query(StateFilter('*'),F.data == 'удалить домашку_2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_del.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='домашка'))
    await state.set_state(DelNote.subject)


@admin_router.callback_query(DelNote.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_del) == 0:
        subject_ed_del.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все2',
        'По датам': 'по числам2',
        'Назад': 'удалить домашку_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(DelNote.how_show)

@admin_router.callback_query(StateFilter('*'),F.data == 'назад_удалить_выбор')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_del[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все2',
        'По датам': 'по числам2',
        'Назад': 'удалить домашку_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(DelNote.how_show)

@admin_router.callback_query(StateFilter('*'),F.data == 'все2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')
    else:
        rez_db = date_b.check_count(subject=subject_ed_del[0],semester=str(rez_db_sem[0][0]),type_note='h')
    if len(rez_db) == 0:
        await call.message.edit_text('Домашки нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'удалить домашку_2',
        'Назад':'назад_удалить_выбор',
        'Меню': 'отмена',
            }))
    else:
        for i in range(len(rez_db)):

            dat_2 = str(rez_db[i][5])

            s = dat_2.split('-')

            dat_2_rez = s[2]+'.'+s[1]+'.'+s[0]

            dat_1 = str(rez_db[i][2])
            s = dat_1.split(' ')
            t1 = s[1].split(':')
            t2 = t1[0] + ':' + t1[1]
            m1 = s[0].split('-')
            m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
            dat_1_rez = m2 + ' ' + t2

            doc_8 = rez_db[i][8]
            if '[' in doc_8:
                list_doc = list(ast.literal_eval(doc_8))
            else:
                doc_8_new = '[' + '"'+doc_8 +'"'+ ']'
                list_doc = ast.literal_eval(doc_8_new)

            phot_7 = rez_db[i][7]
            if '[' in phot_7:
                list_media = list(ast.literal_eval(phot_7))
            else:
                phot_7_new = '[' + '"'+phot_7 +'"'+ ']'
                list_media = ast.literal_eval(phot_7_new)

            album_builder = MediaGroupBuilder(caption=f'Уникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
            a = 0
            for element in range(len(list_media)):
                if list_media[element] != '-':
                    album_builder.add_photo(media=list_media[element])
                else:
                    a = 1

            album_builder_2 = MediaGroupBuilder()
            b = 0
            for element in range(len(list_doc)):
                if list_doc[element] != '-':
                    album_builder_2.add_document(media=list_doc[element])
                else:
                    b = 1

            if a == 1:
                await call.message.answer(
                    f'Фотографий к этой записи нет \n\nУникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
              await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',reply_markup=del_db_vse_btns(rez_db))
        await state.set_state(DelNote.del_subject_2)

@admin_router.callback_query(DelNote.del_subject_2,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(del_subject = call.data)
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date_del_vse(semester=str(rez_db_sem[0][0]),note_id=call.data)

    dat_2 = str(rez_db[0][5])
    s = dat_2.split('-')
    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]

    dat_1 = str(rez_db[0][2])
    s = dat_1.split(' ')
    t1 = s[1].split(':')
    t2 = t1[0] + ':' + t1[1]
    m1 = s[0].split('-')
    m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
    dat_1_rez = m2 + ' ' + t2

    doc_8 = rez_db[0][8]

    if '[' in doc_8:
        list_doc = list(ast.literal_eval(doc_8))
    else:
        doc_8_new = '[' + '"' + doc_8 + '"' + ']'
        list_doc = ast.literal_eval(doc_8_new)

    phot_7 = rez_db[0][7]
    if '[' in phot_7:
        list_media = list(ast.literal_eval(phot_7))
    else:
        phot_7_new = '[' + '"' + phot_7 + '"' + ']'
        list_media = ast.literal_eval(phot_7_new)

    album_builder = MediaGroupBuilder(
        caption=f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[0][6]}')

    a = 0
    for element in range(len(list_media)):
        if list_media[element] != '-':
            album_builder.add_photo(media=list_media[element])
        else:
            a = 1

    album_builder_2 = MediaGroupBuilder()
    b = 0
    for element in range(len(list_doc)):
        if list_doc[element] != '-':
            album_builder_2.add_document(media=list_doc[element])
        else:
            b = 1

    if a == 1:
        await call.message.answer(
            f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[0][6]}')
        a = 0
    else:
        await call.message.answer_media_group(album_builder.build())
    if b == 1:
        await call.message.answer('Документов к этой записи нет!')
        b = 0
    else:
        await call.message.answer_media_group(album_builder_2.build())

    await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
        'Да': 'да',
        'Нет': 'нет_удалить',
        'Отмена': 'отмена',
    },sizes=(1,1,1,1)))
    await state.set_state(DelNote.del_subject)


@admin_router.callback_query(DelNote.del_subject_2_2,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(del_subject_2_2 = call.data)
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date_del_vse(semester=str(rez_db_sem[0][0]),note_id=call.data)

    dat_2 = str(rez_db[0][5])
    s = dat_2.split('-')
    dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]

    dat_1 = str(rez_db[0][2])
    s = dat_1.split(' ')
    t1 = s[1].split(':')
    t2 = t1[0] + ':' + t1[1]
    m1 = s[0].split('-')
    m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
    dat_1_rez = m2 + ' ' + t2

    doc_8 = rez_db[0][8]

    if '[' in doc_8:
        list_doc = list(ast.literal_eval(doc_8))
    else:
        doc_8_new = '[' + '"' + doc_8 + '"' + ']'
        list_doc = ast.literal_eval(doc_8_new)

    phot_7 = rez_db[0][7]
    if '[' in phot_7:
        list_media = list(ast.literal_eval(phot_7))
    else:
        phot_7_new = '[' + '"' + phot_7 + '"' + ']'
        list_media = ast.literal_eval(phot_7_new)

    album_builder = MediaGroupBuilder(
        caption=f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[0][6]}')

    a = 0
    for element in range(len(list_media)):
        if list_media[element] != '-':
            album_builder.add_photo(media=list_media[element])
        else:
            a = 1

    album_builder_2 = MediaGroupBuilder()
    b = 0
    for element in range(len(list_doc)):
        if list_doc[element] != '-':
            album_builder_2.add_document(media=list_doc[element])
        else:
            b = 1

    if a == 1:
        await call.message.answer(
            f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[0][6]}')
        a = 0
    else:
        await call.message.answer_media_group(album_builder.build())
    if b == 1:
        await call.message.answer('Документов к этой записи нет!')
        b = 0
    else:
        await call.message.answer_media_group(album_builder_2.build())

    await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
        'Да': 'да_по_числам',
        'Нет': 'нет_удалить_по_числам',
        'Отмена': 'отмена',
    },sizes=(1,1,1,1)))
    await state.set_state(DelNote.del_subject)


@admin_router.callback_query(DelNote.del_subject,F.data == 'нет_удалить')
async def dz1(call: CallbackQuery,  state: FSMContext):

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del) == 0:
        rez_db = date_b.check_count(subject=data_turp[0], semester=str(rez_db_sem[0][0]), type_note='h')
    else:
        rez_db = date_b.check_count(subject=subject_ed_del[0], semester=str(rez_db_sem[0][0]), type_note='h')

    await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',
                              reply_markup=del_db_vse_btns(rez_db))
    await state.set_state(DelNote.del_subject_2)


@admin_router.callback_query(DelNote.del_subject,F.data == 'нет_удалить_по_числам')
async def dz1(call: CallbackQuery,  state: FSMContext):

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del) == 0:
        rez_db = date_b.select_subject_date(date_subject=data_turp[1], subject=data_turp[0],
                                            semester=str(rez_db_sem[0][0]), type_note='h')
    else:
        rez_db = date_b.select_subject_date(date_subject=data_turp[1], subject=data_turp[0],
                                            semester=str(rez_db_sem[0][0]), type_note='h')

    await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',
                              reply_markup=del_db_vse_btns(rez_db))
    await state.set_state(DelNote.del_subject_2_2)

@admin_router.callback_query(DelNote.del_subject,F.data == 'да')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    rez_db_last_sem = sem_db.select_last_semester()
    date_b.del_vse_subject(note_id=date_turp[1],semester=rez_db_last_sem[0][0])
    await call.message.edit_text(f'Удалили запись с уникальным номером: {date_turp[1]}')
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())
    await state.clear()



@admin_router.callback_query(StateFilter('*'),F.data == 'по числам2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0], semester=str(rez_db_sem[0][0]), type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Домашки нет!', reply_markup=del_db_btns(rez_db,type_note='d'))
    else:
        await call.message.edit_text('Вот все домашние работы по числам!',reply_markup=del_db_btns(rez_db,type_note='d'))
        await state.set_state(DelNote.del_subject_4)

@admin_router.callback_query(DelNote.del_subject_4,F.data.contains('20'))
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(del_subject = call.data)
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.select_subject_date(date_subject=data_turp[1],subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')
    if len(rez_db) == 1:

        for i in range(len(rez_db)):

            dat_2 = str(rez_db[i][5])
            s = dat_2.split('-')
            dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]

            dat_1 = str(rez_db[i][2])
            s = dat_1.split(' ')
            t1 = s[1].split(':')
            t2 = t1[0] + ':' + t1[1]
            m1 = s[0].split('-')
            m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
            dat_1_rez = m2 + ' ' + t2

            doc_8 = rez_db[i][8]
            if '[' in doc_8:


                list_doc = list(ast.literal_eval(doc_8))
            else:
                doc_8_new = '[' + '"' + doc_8 + '"' + ']'

                list_doc = ast.literal_eval(doc_8_new)

            phot_7 = rez_db[i][7]
            if '[' in phot_7:
                list_media = list(ast.literal_eval(phot_7))
            else:
                phot_7_new = '[' + '"' + phot_7 + '"' + ']'
                list_media = ast.literal_eval(phot_7_new)

            album_builder = MediaGroupBuilder(
                caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
            a = 0
            for element in range(len(list_media)):
                if list_media[element] != '-':
                    album_builder.add_photo(media=list_media[element])
                else:
                    a += 1

            album_builder_2 = MediaGroupBuilder()
            b = 0
            for element in range(len(list_doc)):
                if list_doc[element] != '-':
                    album_builder_2.add_document(media=list_doc[element])
                else:
                    b += 1
            if a == 1:
                await call.message.answer(
                    f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

            await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
                'Да': 'да',
                'Нет': 'по числам2',
                'Отмена': 'отмена',
            },sizes=(1,1,1)))
            await state.set_state(DelNote.del_subject_3)
    else:
        for i in range(len(rez_db)):

            dat_2 = str(rez_db[i][5])

            s = dat_2.split('-')

            dat_2_rez = s[2]+'.'+s[1]+'.'+s[0]

            dat_1 = str(rez_db[i][2])
            s = dat_1.split(' ')
            t1 = s[1].split(':')
            t2 = t1[0] + ':' + t1[1]
            m1 = s[0].split('-')
            m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
            dat_1_rez = m2 + ' ' + t2

            doc_8 = rez_db[i][8]
            if '[' in doc_8:
                list_doc = list(ast.literal_eval(doc_8))
            else:
                doc_8_new = '[' + '"'+doc_8 +'"'+ ']'
                list_doc = ast.literal_eval(doc_8_new)

            phot_7 = rez_db[i][7]
            if '[' in phot_7:
                list_media = list(ast.literal_eval(phot_7))
            else:
                phot_7_new = '[' + '"'+phot_7 +'"'+ ']'
                list_media = ast.literal_eval(phot_7_new)

            album_builder = MediaGroupBuilder(caption=f'Уникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
            a = 0
            for element in range(len(list_media)):
                if list_media[element] != '-':
                    album_builder.add_photo(media=list_media[element])
                else:
                    a = 1

            album_builder_2 = MediaGroupBuilder()
            b = 0
            for element in range(len(list_doc)):
                if list_doc[element] != '-':
                    album_builder_2.add_document(media=list_doc[element])
                else:
                    b = 1

            if a == 1:
                await call.message.answer(
                    f'Фотографий к этой записи нет \n\nУникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nДата выполнения: {dat_2_rez}\nНужно: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
              await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',reply_markup=del_db_vse_btns(rez_db))
        await state.set_state(DelNote.del_subject_2_2)


@admin_router.callback_query(DelNote.del_subject,F.data == 'да_по_числам')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    rez_db_last_sem = sem_db.select_last_semester()
    date_b.del_vse_subject(note_id=date_turp[2],semester=rez_db_last_sem[0][0])
    await call.message.edit_text(f'Удалили запись с уникальным номером: {date_turp[2]}')
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())
    await state.clear()


@admin_router.callback_query(DelNote.del_subject_3,F.data == 'да')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    date_b.delete_subject_date(subject=data_turp[0],date_subject=data_turp[1],semester=rez_db_sem[0][0],type_note='h')
    await call.message.edit_text('Удалил!')
    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())









