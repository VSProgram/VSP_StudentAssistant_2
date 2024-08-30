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

from filters.chat_types import ChatTypeFilter,IsUser
from keyboards.inline import get_callback_btns,get_inlineMix_btns,create_rat,Paginationdata,del_db_btns,del_db_vse_btns,add_hw,select_all_semester,menu,menu_user,Paginationdata2,create_rat_lp,select_other_notes,del_db_btns_user


sem_db = Add_semester_db()
date_b = DatBase()


subject_ed_user = []
subject_ed_lecture_user = []
subject_ed_practice_user = []
subject_ed_record_user = []
subject_ed_other_note_user =[]
chat_id = -1002168145795
user_private_router = Router()
user_private_router.message.middleware(AlbumMiddleware())

user_private_router.message.filter(ChatTypeFilter(['private']),IsUser())


@user_private_router.message(StateFilter('*'),Command("student"))
async def add_product(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        await message.answer("<<<Меню>>>", reply_markup=menu_user())
    else:
        await state.clear()
        await message.answer("<<<Меню>>>", reply_markup=menu_user())



@user_private_router.callback_query(F.data == 'назад_user')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Меню>>>", reply_markup=menu_user())



@user_private_router.callback_query(StateFilter('*'),F.data.lower() == 'отмена_user')
async def write_date(call: types.CallbackQuery,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed_user.clear()
    subject_ed_practice_user.clear()
    subject_ed_lecture_user.clear()
    subject_ed_record_user.clear()

    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.edit_text("<<<Меню>>>", reply_markup=menu_user())


@user_private_router.message(StateFilter('*'),F.text.lower() == 'отмена_user')
async def write_date(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed_user.clear()
    subject_ed_practice_user.clear()
    subject_ed_lecture_user.clear()
    subject_ed_record_user.clear()
    subject_ed_other_note_user.clear()


    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu_user())


@user_private_router.message(F.text.lower() == 'меню_user')
async def menu_hw(message: types.Message):
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu_user())


@user_private_router.callback_query(StateFilter('*'),F.data == 'домашка_user')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_user.clear()


    await callback.message.edit_text("<<<Домашка>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать домашку':'показать домашку_user',
        'Добавить домашку':'добавить домашку_user',
        'Назад':'назад_user'
    },sizes=(2,1)))


@user_private_router.callback_query(StateFilter('*'),F.data == 'лекция_user')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_lecture_user.clear()
    await callback.message.edit_text("<<<Лекция>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать лекцию': 'показать лекцию_user',
        'Добавить лекцию': 'добавить лекцию_user',
        'Назад': 'назад_user'
    }, sizes=(2, 1)))


@user_private_router.callback_query(F.data == 'лекция_user')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Лекция>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать лекцию':'показать лекцию_user',
        'Добавить лекцию':'добавить лекцию_user',
        'Назад':'назад_user'
    },sizes=(2,1)))


@user_private_router.callback_query(StateFilter('*'),F.data == 'семинар_user')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_practice_user.clear()

    await callback.message.edit_text("<<<Семинар>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать семинар': 'показать семинар_user',
        'Добавить семинар': 'добавить семинар_user',
        'Назад': 'назад_user'
    }, sizes=(2, 1)))


@user_private_router.callback_query(F.data == 'семинар_user')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Семинар>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать семинар':'показать семинар_user',
        'Добавить семинар':'добавить семинар_user',
        'Назад':'назад_user'
    },sizes=(2,1)))


@user_private_router.callback_query(StateFilter('*'),F.data == 'заметки_user')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_record_user.clear()
    await callback.message.edit_text("<<<Заметки и справочные материалы>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать заметки': 'показать заметки_user',
        'Добавить заметки': 'добавить заметки_user',
        'Назад': 'назад_user'
    }, sizes=(2, 1)))


@user_private_router.callback_query(F.data == 'заметки_user')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Заметки и справочные материалы>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать заметки': 'показать заметки_user',
        'Добавить заметки': 'добавить заметки_user',
        'Назад': 'назад_user'

    }, sizes=(2, 1)))


@user_private_router.callback_query(StateFilter('*'),F.data == 'инфа_user')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_other_note_user.clear()
    await callback.message.edit_text("<<<Заметки и справочные материалы>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать инфу': 'показать инфу_user',
        'Добавить инфу': 'добавить инфу_user',
        'Назад': 'назад_user'
    }, sizes=(2, 1)))


@user_private_router.callback_query(F.data == 'инфа_user')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Заметки и справочные материалы>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать инфу': 'показать инфу_user',
        'Добавить инфу': 'добавить инфу_user',
        'Назад': 'назад_user'

    }, sizes=(2,1)))

# Добавить_домашку-----------------------------------------------------
class AddNote_user(StatesGroup):
    subject = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    second_date = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@user_private_router.callback_query(StateFilter(None),F.data.lower() == 'добавить домашку_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='домашка_user'))
    await state.set_state(AddNote_user.subject)


@user_private_router.callback_query(AddNote_user.subject,F.data)
async def dz2(call: CallbackQuery,  state: FSMContext):
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M")
    await state.update_data(subject = call.data)
    await state.update_data(first_date = formatted_time)
    await state.update_data(name_creator = call.from_user.full_name)
    await state.update_data(id_creator=call.from_user.id)
    await call.message.edit_text(text='Выберете дату!', reply_markup=create_rat())
    await state.set_state(AddNote_user.second_date)


@user_private_router.callback_query(Paginationdata.filter(F.action.in_(['sled','prosh'])))
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


@user_private_router.callback_query(AddNote_user.second_date,F.data.contains('-20'))
async def write_time(callback: types.CallbackQuery,  state: FSMContext):
    await state.update_data(second_date = callback.data)
    await callback.message.edit_text(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
    await state.set_state(AddNote_user.text_note)

@user_private_router.message(AddNote_user.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_user.id_photo)


@user_private_router.message(AddNote_user.id_photo,F.photo)
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
    await state.set_state(AddNote_user.id_doc)




@user_private_router.message(AddNote_user.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_user.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@user_private_router.message(AddNote_user.id_doc,F.document)
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
    await message.answer("<<<Меню>>>", reply_markup=menu_user())

@user_private_router.message(AddNote_user.id_doc, F.text)
async def c_change3(message: types.Message,bot:Bot, state: FSMContext):

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
        await bot.send_message(chat_id=bot.chat_id, text=f'{data_turp[2]} добавил домашку \n'
                                                     f'{data_turp[0]}\n'
                                                     f'Дата выполнения {dat_2_rez}')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu_user())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_домашку-----------------------------------------------------


# Показать_домашку-----------------------------------------------------


class ShowNote_user(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@user_private_router.callback_query(StateFilter(None),F.data == 'показать домашку_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!', reply_markup=add_hw(rez_db[0][0],type_note='домашка_user'))
    await state.set_state(ShowNote_user.subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'показать домашку_2_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_user.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='домашка_user'))
    await state.set_state(ShowNote_user.subject)


@user_private_router.callback_query(ShowNote_user.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_user) == 0:
        subject_ed_user.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_user',
        'По датам': 'по числам_user',
        'Назад': 'показать домашку_2_user',
        'Отмена': 'отмена_user'
    }))
    await state.set_state(ShowNote_user.how_show)


@user_private_router.callback_query(StateFilter('*'),F.data == 'назад_домашка_выбор_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_user[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_user',
        'По датам': 'по числам_user',
        'Назад': 'показать домашку_2_user',
        'Отмена': 'отмена_user'
    }))
    await state.set_state(ShowNote_user.how_show)


@user_private_router.callback_query(StateFilter('*'),F.data == 'все_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_user) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')
    else:
        rez_db = date_b.check_count(subject=subject_ed_user[0], semester=str(rez_db_sem[0][0]), type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text('Домашки нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'показать домашку_2_user',
        'Назад':f'назад_домашка_выбор_user',
        'Меню': 'отмена_user'
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
            'Выбрать по датам': 'ещё_user',
            'Выбрать предмет': 'показать домашку_2_user',
            'Меню': 'отмена_user',
        }))


@user_private_router.callback_query(ShowNote_user.how_show,F.data == 'по числам_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Домашки нет!', reply_markup=del_db_btns_user(rez_db))
    else:
        await call.message.edit_text(text='Вот все домашние работы по числам!', reply_markup=del_db_btns_user(rez_db))
        await state.set_state(ShowNote_user.date_subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'ещё_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_user[0])
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='h')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Домашки нет!', reply_markup=del_db_btns_user(rez_db))
    else:
        await call.message.edit_text(text='Какую запись нужно показать?', reply_markup=del_db_btns_user(rez_db))
        await state.set_state(ShowNote_user.date_subject)


@user_private_router.callback_query(ShowNote_user.date_subject,F.data.contains('20'))
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
        'Да': 'ещё_user',
        'Нет': 'отмена_user',
        'Показать все':'все_user',
        'Назад':'назад_домашка_выбор_user'

    }))


# Добавить_лекцию-----------------------------------------------------
class AddNote_lecture_user(StatesGroup):
    subject = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    second_date = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@user_private_router.callback_query(StateFilter(None),F.data.lower() == 'добавить лекцию_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='лекция_user'))
    await state.set_state(AddNote_lecture_user.subject)


@user_private_router.callback_query(AddNote_lecture_user.subject,F.data)
async def dz2(call: CallbackQuery,  state: FSMContext):
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M")
    await state.update_data(subject = call.data)
    await state.update_data(first_date = formatted_time)
    await state.update_data(name_creator = call.from_user.full_name)
    await state.update_data(id_creator=call.from_user.id)
    await call.message.edit_text(text='Выберете дату лекции!', reply_markup=create_rat_lp())
    await state.set_state(AddNote_lecture_user.second_date)


@user_private_router.callback_query(Paginationdata2.filter(F.action.in_(['sled','prosh'])))
async def pagin4ik(call:CallbackQuery,callback_data:Paginationdata2):
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
        await call.message.edit_reply_markup(reply_markup=create_rat_lp(now_m=page_m,now_y=page_y))
    await call.answer()


@user_private_router.callback_query(AddNote_lecture_user.second_date,F.data.contains('-20'))
async def write_time(callback: types.CallbackQuery,  state: FSMContext):
    await state.update_data(second_date = callback.data)
    await callback.message.edit_text(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
    await state.set_state(AddNote_lecture_user.text_note)

@user_private_router.message(AddNote_lecture_user.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_lecture_user.id_photo)


@user_private_router.message(AddNote_lecture_user.id_photo,F.photo)
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
    await state.set_state(AddNote_lecture_user.id_doc)



@user_private_router.message(AddNote_lecture_user.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_lecture_user.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@user_private_router.message(AddNote_lecture_user.id_doc,F.document)
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
    date_b.add_note(data=data_turp,semester=str(sem_last),type_note='l')

    await message.answer(f'Лекция добавлена!')
    dat_2 = str(data_turp[4])
    s = dat_2.split('-')
    dat_2_rez = s[0] + '.' + s[1] + '.' + s[2]
    await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил лекцию \n'
                                                        f'{data_turp[0]}\n'
                                                        f'Состоялась {dat_2_rez}')
    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu_user())

@user_private_router.message(AddNote_lecture_user.id_doc, F.text)
async def c_change3(message: types.Message,bot:Bot, state: FSMContext):

    if message.text.lower() =='-':
        await state.update_data(id_doc=message.text)

        date_zr = await state.get_data()
        data_turp = tuple(date_zr.values())
        sem_last = sem_db.select_last_semester()[0][0]
        date_b.add_note(data=data_turp, semester=str(sem_last), type_note='l')

        await message.answer(f'Лекция добавлена!')
        dat_2 = str(data_turp[4])
        s = dat_2.split('-')
        dat_2_rez = s[0] + '.' + s[1] + '.' + s[2]
        await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил лекцию \n'
                                                     f'{data_turp[0]}\n'
                                                     f'Состоялась {dat_2_rez}')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu_user())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_лекцию-----------------------------------------------------


# Показать_лекцию-----------------------------------------------------


class ShowNote_lecture_user(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@user_private_router.callback_query(StateFilter(None),F.data == 'показать лекцию_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!', reply_markup=add_hw(rez_db[0][0],type_note='лекция_user'))
    await state.set_state(ShowNote_lecture_user.subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'показать лекцию_2_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_lecture_user.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='лекция_user'))
    await state.set_state(ShowNote_lecture_user.subject)


@user_private_router.callback_query(ShowNote_lecture_user.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_lecture_user) == 0:
        subject_ed_lecture_user.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_лекция_user',
        'По датам': 'по числам_лекция_user',
        'Назад': 'показать лекцию_2_user',
        'Отмена': 'отмена_user'
    }))
    await state.set_state(ShowNote_lecture_user.how_show)


@user_private_router.callback_query(StateFilter('*'),F.data == 'назад_лекция_выбор_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_lecture_user[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_лекция_user',
        'По датам': 'по числам_лекция_user',
        'Назад': 'показать лекцию_2_user',
        'Отмена': 'отмена_user'
    }))
    await state.set_state(ShowNote_lecture_user.how_show)


@user_private_router.callback_query(StateFilter('*'),F.data == 'все_лекция_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_lecture_user) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')
    else:
        rez_db = date_b.check_count(subject=subject_ed_lecture_user[0], semester=str(rez_db_sem[0][0]), type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text('Лекции нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'показать лекцию_2_user',
        'Назад':f'назад_лекция_выбор_user',
        'Меню': 'отмена_user'
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

            album_builder = MediaGroupBuilder(caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
                await call.message.answer(f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Куда дальше?', reply_markup=get_inlineMix_btns(btns={
            'Выбрать по датам': 'ещё_лекция_user',
            'Выбрать предмет': 'показать лекцию_2_user',
            'Меню': 'отмена_user',
        }))


@user_private_router.callback_query(ShowNote_lecture_user.how_show,F.data == 'по числам_лекция_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Лекции нет!', reply_markup=del_db_btns_user(rez_db,type_note_2='l'))
    else:
        await call.message.edit_text(text='Вот все лекции по числам!', reply_markup=del_db_btns_user(rez_db,type_note_2='l'))
        await state.set_state(ShowNote_lecture_user.date_subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'ещё_лекция_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_lecture_user[0])
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Лекции нет!', reply_markup=del_db_btns_user(rez_db,type_note_2='l'))
    else:
        await call.message.edit_text(text='Какую запись нужно показать?', reply_markup=del_db_btns_user(rez_db,type_note_2='l'))
        await state.set_state(ShowNote_lecture_user.date_subject)


@user_private_router.callback_query(ShowNote_lecture_user.date_subject,F.data.contains('20'))
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(date_subject = call.data)

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.select_subject_date(date_subject=data_turp[1],semester=str(rez_db_sem[0][0]),type_note='l',subject=data_turp[0])
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
            caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
                f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
        'Да': 'ещё_лекция_user',
        'Нет': 'отмена_user',
        'Показать все':'все_лекция_user',
        'Назад':'назад_лекция_выбор_user'

    }))



# Показать_лекцию-----------------------------------------------------



# Добавить_семинар-----------------------------------------------------
class AddNote_practice_user(StatesGroup):
    subject = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    second_date = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@user_private_router.callback_query(StateFilter(None),F.data.lower() == 'добавить семинар_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='семинар_user'))
    await state.set_state(AddNote_practice_user.subject)


@user_private_router.callback_query(AddNote_practice_user.subject,F.data)
async def dz2(call: CallbackQuery,  state: FSMContext):
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M")
    await state.update_data(subject = call.data)
    await state.update_data(first_date = formatted_time)
    await state.update_data(name_creator = call.from_user.full_name)
    await state.update_data(id_creator=call.from_user.id)
    await call.message.edit_text(text='Выберете дату семинара!', reply_markup=create_rat_lp())
    await state.set_state(AddNote_practice_user.second_date)


@user_private_router.callback_query(Paginationdata2.filter(F.action.in_(['sled','prosh'])))
async def pagin4ik(call:CallbackQuery,callback_data:Paginationdata2):
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
        await call.message.edit_reply_markup(reply_markup=create_rat_lp(now_m=page_m,now_y=page_y))
    await call.answer()


@user_private_router.callback_query(AddNote_practice_user.second_date,F.data.contains('-20'))
async def write_time(callback: types.CallbackQuery,  state: FSMContext):
    await state.update_data(second_date = callback.data)
    await callback.message.edit_text(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
    await state.set_state(AddNote_practice_user.text_note)

@user_private_router.message(AddNote_practice_user.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_practice_user.id_photo)


@user_private_router.message(AddNote_practice_user.id_photo,F.photo)
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
    await state.set_state(AddNote_practice_user.id_doc)



@user_private_router.message(AddNote_practice_user.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_practice_user.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@user_private_router.message(AddNote_practice_user.id_doc,F.document)
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
    date_b.add_note(data=data_turp,semester=str(sem_last),type_note='p')

    await message.answer(f'Семинар добавлен!')
    dat_2 = str(data_turp[4])
    s = dat_2.split('-')
    dat_2_rez = s[0] + '.' + s[1] + '.' + s[2]
    await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил семинар\n'
                                                        f'{data_turp[0]}\n'
                                                        f'Состоялся {dat_2_rez}')
    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu_user())

@user_private_router.message(AddNote_practice_user.id_doc, F.text)
async def c_change3(message: types.Message,bot:Bot, state: FSMContext):

    if message.text.lower() =='-':
        await state.update_data(id_doc=message.text)

        date_zr = await state.get_data()
        data_turp = tuple(date_zr.values())
        sem_last = sem_db.select_last_semester()[0][0]
        date_b.add_note(data=data_turp, semester=str(sem_last), type_note='p')

        await message.answer(f'Семинар добавлен!')
        dat_2 = str(data_turp[4])
        s = dat_2.split('-')
        dat_2_rez = s[0] + '.' + s[1] + '.' + s[2]
        await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил семинар\n'
                                                     f'{data_turp[0]}\n'
                                                     f'Состоялся {dat_2_rez}')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu_user())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_семинар-----------------------------------------------------

# Показать_семинар-----------------------------------------------------


class ShowNote_practice_user(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@user_private_router.callback_query(StateFilter(None),F.data == 'показать семинар_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!', reply_markup=add_hw(rez_db[0][0],type_note='семинар_user'))
    await state.set_state(ShowNote_practice_user.subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'показать семинар_2_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_practice_user.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='семинар_user'))
    await state.set_state(ShowNote_practice_user.subject)


@user_private_router.callback_query(ShowNote_practice_user.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_practice_user) == 0:
        subject_ed_practice_user.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_семинар_user',
        'По датам': 'по числам_семинар_user',
        'Назад': 'показать семинар_2_user',
        'Отмена': 'отмена_user'
    }))
    await state.set_state(ShowNote_practice_user.how_show)


@user_private_router.callback_query(StateFilter('*'),F.data == 'назад_семинар_выбор_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_practice_user[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_семинар_user',
        'По датам': 'по числам_семинар_user',
        'Назад': 'показать семинар_2_user',
        'Отмена': 'отмена_user'
    }))
    await state.set_state(ShowNote_practice_user.how_show)


@user_private_router.callback_query(StateFilter('*'),F.data == 'все_семинар_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_practice_user) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='p')
    else:
        rez_db = date_b.check_count(subject=subject_ed_practice_user[0], semester=str(rez_db_sem[0][0]), type_note='p')

    if len(rez_db) == 0:
        await call.message.edit_text('Семинара нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'показать семинар_2_user',
        'Назад':f'назад_семинар_выбор_user',
        'Меню': 'отмена_user'
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

            album_builder = MediaGroupBuilder(caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялся: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
                await call.message.answer(f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялся: {dat_2_rez}\nОписание: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Куда дальше?_user', reply_markup=get_inlineMix_btns(btns={
            'Выбрать по датам': 'ещё_семинар_user',
            'Выбрать предмет': 'показать семинар_2_user',
            'Меню': 'отмена_user',
        }))


@user_private_router.callback_query(ShowNote_practice_user.how_show,F.data == 'по числам_семинар_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='p')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Семинара нет!', reply_markup=del_db_btns_user(rez_db,type_note_2='p'))
    else:
        await call.message.edit_text(text='Вот все семинары по числам!', reply_markup=del_db_btns_user(rez_db,type_note_2='p'))
        await state.set_state(ShowNote_practice_user.date_subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'ещё_семинар_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_practice_user[0])
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='p')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Семинара нет!', reply_markup=del_db_btns_user(rez_db,type_note_2='p'))
    else:
        await call.message.edit_text(text='Какую запись нужно показать?', reply_markup=del_db_btns_user(rez_db,type_note_2='p'))
        await state.set_state(ShowNote_practice_user.date_subject)


@user_private_router.callback_query(ShowNote_practice_user.date_subject,F.data.contains('20'))
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(date_subject = call.data)

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.select_subject_date(date_subject=data_turp[1],semester=str(rez_db_sem[0][0]),type_note='p',subject=data_turp[0])
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
            caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялся: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
                f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялся {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
        'Да': 'ещё_семинар_user',
        'Нет': 'отмена_user',
        'Показать все':'все_семинар_user',
        'Назад':'назад_семинар_выбор_user'

    }))


# Показать_семинар-----------------------------------------------------



# Добавить_заметки-----------------------------------------------------


class AddNote_record_user(StatesGroup):
    subject = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    second_date = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@user_private_router.callback_query(StateFilter(None),F.data.lower() == 'добавить заметки_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='заметки_user'))
    await state.set_state(AddNote_record_user.subject)



@user_private_router.callback_query(AddNote_record_user.subject,F.data)
async def write_time(call: types.CallbackQuery,  state: FSMContext):
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M")
    await state.update_data(subject=call.data)
    await state.update_data(first_date=formatted_time)
    await state.update_data(name_creator=call.from_user.full_name)
    await state.update_data(id_creator=call.from_user.id)
    await state.update_data(second_date = formatted_time)
    await call.message.edit_text(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
    await state.set_state(AddNote_record_user.text_note)

@user_private_router.message(AddNote_record_user.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_record_user.id_photo)


@user_private_router.message(AddNote_record_user.id_photo,F.photo)
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
    await state.set_state(AddNote_record_user.id_doc)


@user_private_router.message(AddNote_record_user.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_record_user.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@user_private_router.message(AddNote_record_user.id_doc,F.document)
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
    # await message.answer(date_zr)
    sem_last = sem_db.select_last_semester()[0][0]
    date_b.add_note(data=data_turp,semester=str(sem_last),type_note='r')

    await message.answer(f'Заметка добавлена!')
    await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил заметку\n'
                                                 f'{data_turp[0]}')
    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu_user())

@user_private_router.message(AddNote_record_user.id_doc, F.text)
async def c_change3(message: types.Message,bot:Bot, state: FSMContext):

    if message.text.lower() =='-':
        await state.update_data(id_doc=message.text)

        date_zr = await state.get_data()
        data_turp = tuple(date_zr.values())
        sem_last = sem_db.select_last_semester()[0][0]
        # await message.answer(date_zr)

        date_b.add_note(data=data_turp, semester=str(sem_last), type_note='r')

        await message.answer(f'Заметка добавлена!')
        await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил заметку\n'
                                                     f'{data_turp[0]}')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu_user())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_заметки-----------------------------------------------------

# Показать_заметки-----------------------------------------------------


class ShowNote_record_user(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@user_private_router.callback_query(StateFilter(None),F.data == 'показать заметки_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!', reply_markup=add_hw(rez_db[0][0],type_note='заметки_user'))
    await state.set_state(ShowNote_record_user.subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'показать заметки_2_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_record_user.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='заметки_user'))
    await state.set_state(ShowNote_record_user.subject)



@user_private_router.callback_query(ShowNote_record_user.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_record_user) == 0:
        subject_ed_record_user.append(call.data)

    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_record_user) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='r')
    else:
        rez_db = date_b.check_count(subject=subject_ed_record_user[0], semester=str(rez_db_sem[0][0]), type_note='r')

    if len(rez_db) == 0:
        await call.message.edit_text('Заметок нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'показать заметки_2_user',
        'Меню': 'отмена_user'
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

            album_builder = MediaGroupBuilder(caption=f'{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nОписание: {rez_db[i][6]}')
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
                await call.message.answer(f'Фотографий к этой записи нет \n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nОписание: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Куда дальше?', reply_markup=get_inlineMix_btns(btns={
            'Выбрать предмет': 'показать заметки_2_user',
            'Меню': 'отмена_user',
        }))

# Показать_заметки-----------------------------------------------------


# Добавить_инфу-----------------------------------------------------


class AddNote_other_note_user(StatesGroup):
    name_note = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@user_private_router.callback_query(StateFilter(None),F.data.lower() == 'добавить инфу_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Введите название записи!\n•Название записи должно содержать менее 34 символов(включая пробелы)\n•Максимум может храниться до 95 записей\n•Введите "Отмена" для полной отмены')
    await state.set_state(AddNote_other_note_user.name_note)




@user_private_router.message(AddNote_other_note_user.name_note,F.text)
async def write_time(message : Message,  state: FSMContext):
    rez_db = date_b.select_name_note()
    for i in rez_db:
        if message.text == i[0]:
            await message.answer('Это название уже занято!\nВведите другое название!')
            return

    if len(message.text)>34:
        await message.answer(
            text='Введите название записи!\n•Название записи должно содержать менее 34 символов(включая пробелы)\n•Максимум может храниться до 95 записей\n•Введите "Отмена" для полной отмены')
    else:
        now = datetime.now()
        formatted_time = now.strftime("%d-%m-%Y %H:%M")
        await state.update_data(name_note=message.text)
        await state.update_data(first_date=formatted_time)
        await state.update_data(name_creator=message.from_user.full_name)
        await state.update_data(id_creator=message.from_user.id)
        await message.answer(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
        await state.set_state(AddNote_other_note_user.text_note)

@user_private_router.message(AddNote_other_note_user.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_other_note_user.id_photo)


@user_private_router.message(AddNote_other_note_user.id_photo,F.photo)
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
    await state.set_state(AddNote_other_note_user.id_doc)



@user_private_router.message(AddNote_other_note_user.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_other_note_user.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@user_private_router.message(AddNote_other_note_user.id_doc,F.document)
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
    # date_b.add_note(data=data_turp,semester=str(sem_last),type_note='r')
    date_b.add_note_other(data=data_turp[1:7],name_note=data_turp[0])
    await message.answer(f'Инфа добавлена!')
    await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил инфу\n'
                                                 f'{data_turp[0]}')

    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())

@user_private_router.message(AddNote_other_note_user.id_doc, F.text)
async def c_change3(message: types.Message,bot:Bot, state: FSMContext):

    if message.text.lower() =='-':
        await state.update_data(id_doc=message.text)

        date_zr = await state.get_data()
        data_turp = tuple(date_zr.values())
        sem_last = sem_db.select_last_semester()[0][0]
        date_b.add_note_other(data=data_turp[1:7], name_note=data_turp[0])

        await message.answer(f'Инфа добавлена!')
        await bot.send_message(chat_id=chat_id, text=f'{data_turp[2]} добавил инфу\n'
                                                     f'{data_turp[0]}')
        await state.clear()
        rez_db_last_sem = sem_db.select_last_semester()
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_инфу-----------------------------------------------------


# Показать_инфу-----------------------------------------------------
#
#
class ShowNote_other_notes_user(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@user_private_router.callback_query(StateFilter(None),F.data == 'показать инфу_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете запись!', reply_markup=select_other_notes())
    await state.set_state(ShowNote_other_notes_user.subject)


@user_private_router.callback_query(StateFilter('*'),F.data == 'показать инфу_2_user')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_other_note_user.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете запись!',reply_markup=select_other_notes())
    await state.set_state(ShowNote_other_notes_user.subject)



@user_private_router.callback_query(ShowNote_other_notes_user.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_other_note_user) == 0:
        subject_ed_other_note_user.append(call.data)

    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_other_note_user) == 0:
        rez_db = date_b.select_all_other_notes(name_note=call.data)
    else:
        rez_db = date_b.select_all_other_notes(name_note=subject_ed_other_note_user[0])
    if len(rez_db) == 0:
        await call.message.edit_text('Инфы нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать другую инфу': 'показать инфу_2_user',
        'Меню': 'отмена_user'
            }))
    else:
        for i in range(len(rez_db)):


            dat_1 = str(rez_db[i][1])
            s = dat_1.split(' ')
            t1 = s[1].split(':')
            t2 = t1[0] + ':' + t1[1]
            m1 = s[0].split('-')
            m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
            dat_1_rez = m2 + ' ' + t2

            doc_8 = rez_db[i][6]
            if '[' in doc_8:


                list_doc = list(ast.literal_eval(doc_8))
            else:
                doc_8_new = '[' + '"'+doc_8 +'"'+ ']'

                list_doc = ast.literal_eval(doc_8_new)

            phot_7 = rez_db[i][5]
            if '[' in phot_7:
                list_media = list(ast.literal_eval(phot_7))
            else:
                phot_7_new = '[' + '"'+phot_7 +'"'+ ']'
                list_media = ast.literal_eval(phot_7_new)

            album_builder = MediaGroupBuilder(caption=f'{rez_db[i][7]}\n\nДобавил: {rez_db[i][2]}\nДата добавления: {dat_1_rez}\n\nОписание: {rez_db[i][4]}')
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
                await call.message.answer(f'Фотографий к этой записи нет \n\n{rez_db[i][7]}\n\nДобавил: {rez_db[i][2]}\nДата добавления: {dat_1_rez}\n\nОписание: {rez_db[i][4]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Куда дальше?', reply_markup=get_inlineMix_btns(btns={
            'Выбрать запись': 'показать инфу_2_user',
            'Меню': 'отмена_user',
        }))


# Показать_инфу-----------------------------------------------------
