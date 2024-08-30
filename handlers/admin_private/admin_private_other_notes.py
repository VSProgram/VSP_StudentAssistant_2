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
from keyboards.inline import get_callback_btns,get_inlineMix_btns,create_rat,Paginationdata,del_db_btns,del_db_vse_btns,add_hw,select_all_semester,menu,create_rat_lp,Paginationdata2,select_other_notes
sem_db = Add_semester_db()
date_b = DatBase()
admin_router_5 = Router()
admin_router_5.message.middleware(AlbumMiddleware())
admin_router_5.message.filter(ChatTypeFilter(["private"]),IsAdmin())

subject_ed_other_note = []
subject_ed_del_other_notes = []
semester_ed_del = []

chat_id = -1002168145795


@admin_router_5.message(StateFilter('*'),Command("user"))
async def add_product(message: types.Message,state: FSMContext):
    await message.answer('Yes')


@admin_router_5.message(StateFilter('*'),Command("admin"))
async def add_product(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        await state.clear()
        await message.answer("<<<Меню>>>", reply_markup=menu())



@admin_router_5.callback_query(F.data == 'назад')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Меню>>>", reply_markup=menu())



@admin_router_5.callback_query(StateFilter('*'),F.data.lower() == 'отмена')
async def write_date(call: types.CallbackQuery,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed_other_note.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.edit_text("<<<Меню>>>", reply_markup=menu())

@admin_router_5.message(StateFilter('*'),F.text.lower() == 'отмена')
async def write_date(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed_other_note.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())


@admin_router_5.message(F.text.lower() == 'меню')
async def menu_hw(message: types.Message):
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())


@admin_router_5.callback_query(StateFilter('*'),F.data == 'инфа')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_del_other_notes.clear()
    subject_ed_other_note.clear()
    await callback.message.edit_text("<<<Заметки и справочные материалы>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать инфу': 'показать инфу',
        'Добавить инфу': 'добавить инфу',
        'Изменить инфу': 'изменить инфу',
        'Удалить инфу': 'удалить инфу',
        'Назад': 'назад'
    }, sizes=(2, 2)))


@admin_router_5.callback_query(F.data == 'инфа')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Заметки и справочные материалы>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать инфу': 'показать инфу',
        'Добавить инфу': 'добавить инфу',
        'Изменить инфу': 'изменить инфу',
        'Удалить инфу': 'удалить инфу',
        'Назад': 'назад'

    }, sizes=(2, 2)))




# Добавить_лекцию-----------------------------------------------------
class AddNote_other_note(StatesGroup):
    name_note = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@admin_router_5.callback_query(StateFilter(None),F.data.lower() == 'добавить инфу')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Введите название записи!\n•Название записи должно содержать менее 34 символов(включая пробелы)\n•Максимум может храниться до 95 записей\n•Введите "Отмена" для полной отмены')
    await state.set_state(AddNote_other_note.name_note)




@admin_router_5.message(AddNote_other_note.name_note,F.text)
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
        await state.set_state(AddNote_other_note.text_note)

@admin_router_5.message(AddNote_other_note.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_other_note.id_photo)


@admin_router_5.message(AddNote_other_note.id_photo,F.photo)
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
    await state.set_state(AddNote_other_note.id_doc)




@admin_router_5.message(AddNote_other_note.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_other_note.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@admin_router_5.message(AddNote_other_note.id_doc,F.document)
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

@admin_router_5.message(AddNote_other_note.id_doc, F.text)
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

# Добавить_лекцию-----------------------------------------------------


# # Показать_лекцию-----------------------------------------------------
#
#
class ShowNote_other_notes(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@admin_router_5.callback_query(StateFilter(None),F.data == 'показать инфу')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете запись!', reply_markup=select_other_notes())
    await state.set_state(ShowNote_other_notes.subject)


@admin_router_5.callback_query(StateFilter('*'),F.data == 'показать инфу_2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_other_note.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете запись!',reply_markup=select_other_notes())
    await state.set_state(ShowNote_other_notes.subject)



@admin_router_5.callback_query(ShowNote_other_notes.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_other_note) == 0:
        subject_ed_other_note.append(call.data)

    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_other_note) == 0:
        rez_db = date_b.select_all_other_notes(name_note=call.data)
    else:
        rez_db = date_b.select_all_other_notes(name_note=subject_ed_other_note[0])
    if len(rez_db) == 0:
        await call.message.edit_text('Инфы нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать другую инфу': 'показать инфу_2',
        'Меню': 'отмена'
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
            'Выбрать запись': 'показать инфу_2',
            'Меню': 'отмена',
        }))






# Удалить_домашку-----------------------------------------------------

class DelNote_other_note(StatesGroup):
    subject = State()
    how_show = State()
    del_subject = State()
    del_subject_2 = State()
    del_subject_2_2 = State()
    del_subject_3 = State()
    del_subject_4 = State()





@admin_router_5.callback_query(StateFilter(None),F.data == 'удалить инфу')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете запись!',reply_markup=select_other_notes())
    await state.set_state(DelNote_other_note.subject)

@admin_router_5.callback_query(StateFilter('*'),F.data == 'удалить инфу_2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_del_other_notes.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете запись!',reply_markup=select_other_notes())
    await state.set_state(DelNote_other_note.subject)



@admin_router_5.callback_query(DelNote_other_note.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del_other_notes) == 0:
        rez_db = date_b.select_all_other_notes(name_note=data_turp[0])
    else:
        rez_db = date_b.select_all_other_notes(name_note=subject_ed_del_other_notes)
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
                doc_8_new = '[' + '"' + doc_8 + '"' + ']'


                list_doc = ast.literal_eval(doc_8_new)

            phot_7 = rez_db[i][5]
            if '[' in phot_7:
                list_media = list(ast.literal_eval(phot_7))
            else:
                phot_7_new = '[' + '"' + phot_7 + '"' + ']'
                list_media = ast.literal_eval(phot_7_new)

            album_builder = MediaGroupBuilder(
                caption=f'{rez_db[i][7]}\n\nДобавил: {rez_db[i][2]}\nДата добавления: {dat_1_rez}\n\nОписание: {rez_db[i][4]}')
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
                    f'Фотографий к этой записи нет \n\n{rez_db[i][7]}\n\nДобавил: {rez_db[i][2]}\nДата добавления: {dat_1_rez}\n\nОписание: {rez_db[i][4]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
                await call.message.answer_media_group(album_builder_2.build())

    await call.message.answer('Эту запись вы желаете удалить?', reply_markup=get_inlineMix_btns(btns={
        'Да': 'да_инфа',
        'Нет': 'удалить инфу_2',
        'Отмена': 'отмена',
    }, sizes=(1, 1, 1, 1)))
    await state.set_state(DelNote_other_note.del_subject)

# @admin_router_5.callback_query(DelNote_other_note.del_subject_2,F.data)
# async def dz1(call: CallbackQuery,  state: FSMContext):
#     await state.update_data(del_subject = call.data)
#     date_zr = await state.get_data()
#     data_turp = tuple(date_zr.values())
#     rez_db_sem = sem_db.select_last_semester()
#     rez_db = date_b.check_date_del_vse(semester=str(rez_db_sem[0][0]),note_id=call.data)
#
#     dat_2 = str(rez_db[0][5])
#     s = dat_2.split('-')
#     dat_2_rez = s[2] + '.' + s[1] + '.' + s[0]
#
#     dat_1 = str(rez_db[0][2])
#     s = dat_1.split(' ')
#     t1 = s[1].split(':')
#     t2 = t1[0] + ':' + t1[1]
#     m1 = s[0].split('-')
#     m2 = m1[2] + '.' + m1[1] + '.' + m1[0]
#     dat_1_rez = m2 + ' ' + t2
#
#     doc_8 = rez_db[0][8]
#
#     if '[' in doc_8:
#         list_doc = list(ast.literal_eval(doc_8))
#     else:
#         doc_8_new = '[' + '"' + doc_8 + '"' + ']'
#         list_doc = ast.literal_eval(doc_8_new)
#
#     phot_7 = rez_db[0][7]
#     if '[' in phot_7:
#         list_media = list(ast.literal_eval(phot_7))
#     else:
#         phot_7_new = '[' + '"' + phot_7 + '"' + ']'
#         list_media = ast.literal_eval(phot_7_new)
#
#     album_builder = MediaGroupBuilder(
#         caption=f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[0][6]}')
#
#     a = 0
#     for element in range(len(list_media)):
#         if list_media[element] != '-':
#             album_builder.add_photo(media=list_media[element])
#         else:
#             a = 1
#
#     album_builder_2 = MediaGroupBuilder()
#     b = 0
#     for element in range(len(list_doc)):
#         if list_doc[element] != '-':
#             album_builder_2.add_document(media=list_doc[element])
#         else:
#             b = 1
#
#     if a == 1:
#         await call.message.answer(
#             f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[0][6]}')
#         a = 0
#     else:
#         await call.message.answer_media_group(album_builder.build())
#     if b == 1:
#         await call.message.answer('Документов к этой записи нет!')
#         b = 0
#     else:
#         await call.message.answer_media_group(album_builder_2.build())
#
#     await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
#         'Да': 'да_заметки',
#         'Нет': 'нет_удалить_заметки',
#         'Отмена': 'отмена',
#     },sizes=(1,1,1,1)))
#     await state.set_state(DelNote_record.del_subject)


@admin_router_5.callback_query(DelNote_other_note.del_subject,F.data == 'да_инфа')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    date_b.delete_other_note(name_note=date_turp[0])
    await call.message.edit_text(f'Удалили запись с названием {date_turp[0]}')
    await call.message.answer("<<<Меню>>>", reply_markup=menu())
    await state.clear()

# @admin_router_5.callback_query(DelNote_other_note.del_subject,F.data == 'нет_удалить_инфа')
# async def dz1(call: CallbackQuery,  state: FSMContext):
#
#     date_zr = await state.get_data()
#     data_turp = tuple(date_zr.values())
#
#     rez_db_sem = sem_db.select_last_semester()
#     if len(subject_ed_del_record) == 0:
#         rez_db = date_b.select_all_other_notes(subject=data_turp[0], semester=str(rez_db_sem[0][0]), type_note='r')
#     else:
#         rez_db = date_b.check_count(subject=subject_ed_del_record[0], semester=str(rez_db_sem[0][0]), type_note='r')
#
#     await call.message.edit_text('Выберете уникальный номер записи,которую собираетесь удалять!',
#                               reply_markup=del_db_vse_btns(rez_db,type_note='r'))
#     await state.set_state(DelNote_other_note.del_subject_2)
#
#
#
# @admin_router_5.callback_query(DelNote_other_note.del_subject,F.data == 'нет_удалить_заметки')
# async def dz1(call: CallbackQuery,  state: FSMContext):
#
#     date_zr = await state.get_data()
#     data_turp = tuple(date_zr.values())
#
#     rez_db_sem = sem_db.select_last_semester()
#     if len(subject_ed_del_record) == 0:
#         rez_db = date_b.check_count(subject=data_turp[0], semester=str(rez_db_sem[0][0]), type_note='r')
#     else:
#         rez_db = date_b.check_count(subject=subject_ed_del_record[0], semester=str(rez_db_sem[0][0]), type_note='r')
#
#     await call.message.edit_text('Выберете уникальный номер записи,которую собираетесь удалять!',
#                               reply_markup=del_db_vse_btns(rez_db,type_note='r'))
#     await state.set_state(DelNote_other_note.del_subject_2)



