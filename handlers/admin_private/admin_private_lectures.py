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
from keyboards.inline import get_callback_btns,get_inlineMix_btns,create_rat,Paginationdata,del_db_btns,del_db_vse_btns,add_hw,select_all_semester,menu,create_rat_lp,Paginationdata2
sem_db = Add_semester_db()
date_b = DatBase()
admin_router_2 = Router()
admin_router_2.message.middleware(AlbumMiddleware())
admin_router_2.message.filter(ChatTypeFilter(["private"]),IsAdmin())

subject_ed_lecture = []
subject_ed_del_lecture = []
semester_ed_del = []

chat_id = -1002168145795



@admin_router_2.message(StateFilter('*'),Command("admin"))
async def add_product(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        await state.clear()
        await message.answer("<<<Меню>>>", reply_markup=menu())



@admin_router_2.callback_query(F.data == 'назад')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Меню>>>", reply_markup=menu())



@admin_router_2.callback_query(StateFilter('*'),F.data.lower() == 'отмена')
async def write_date(call: types.CallbackQuery,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed_lecture.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.edit_text("<<<Меню>>>", reply_markup=menu())

@admin_router_2.message(StateFilter('*'),F.text.lower() == 'отмена')
async def write_date(message: types.Message,state: FSMContext):
    g_state = await state.get_data()
    if g_state is None:
        return
    await state.clear()
    subject_ed_lecture.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())


@admin_router_2.message(F.text.lower() == 'меню')
async def menu_hw(message: types.Message):
    rez_db_last_sem = sem_db.select_last_semester()
    await message.answer("<<<Меню>>>", reply_markup=menu())


@admin_router_2.callback_query(StateFilter('*'),F.data == 'лекция')
async def menu_hw(callback: CallbackQuery , state:FSMContext):
    await state.clear()
    subject_ed_del_lecture.clear()
    subject_ed_lecture.clear()
    await callback.message.edit_text("<<<Лекция>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать лекцию': 'показать лекцию',
        'Добавить лекцию': 'добавить лекцию',
        'Изменить лекцию': 'изменить лекцию',
        'Удалить лекцию': 'удалить лекцию',
        'Назад': 'назад'
    }, sizes=(2, 2)))


@admin_router_2.callback_query(F.data == 'лекция')
async def menu_hw(callback: CallbackQuery):
    await callback.message.edit_text("<<<Лекция>>>", reply_markup=get_inlineMix_btns(btns={
        'Показать лекцию':'показать лекцию',
        'Добавить лекцию':'добавить лекцию',
        'Изменить лекцию': 'изменить лекцию',
        'Удалить лекцию':'удалить лекцию',
        'Назад':'назад'
    },sizes=(2,2)))




# Добавить_лекцию-----------------------------------------------------
class AddNote_lecture(StatesGroup):
    subject = State()
    first_date = State()
    name_creator = State()
    id_creator = State()
    second_date = State()
    text_note = State()
    id_photo = State()
    id_doc = State()

@admin_router_2.callback_query(StateFilter(None),F.data.lower() == 'добавить лекцию')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='лекция'))
    await state.set_state(AddNote_lecture.subject)


@admin_router_2.callback_query(AddNote_lecture.subject,F.data)
async def dz2(call: CallbackQuery,  state: FSMContext):
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M")
    await state.update_data(subject = call.data)
    await state.update_data(first_date = formatted_time)
    await state.update_data(name_creator = call.from_user.full_name)
    await state.update_data(id_creator=call.from_user.id)
    await call.message.edit_text(text='Выберете дату лекции!', reply_markup=create_rat_lp())
    await state.set_state(AddNote_lecture.second_date)


@admin_router_2.callback_query(Paginationdata2.filter(F.action.in_(['sled','prosh'])))
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


@admin_router_2.callback_query(AddNote_lecture.second_date,F.data.contains('-20'))
async def write_time(callback: types.CallbackQuery,  state: FSMContext):
    await state.update_data(second_date = callback.data)
    await callback.message.edit_text(text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',reply_markup=None)
    await state.set_state(AddNote_lecture.text_note)

@admin_router_2.message(AddNote_lecture.text_note, F.text)
async def c_change3(message: types.Message, state: FSMContext):
        if len(message.text)>3000:
            await callback.message.edit_text(
                text='Введите текст для записи\n•Текст должен содержать не более 3000 символов(включая пробелы)\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены',
                reply_markup=None)
            return
        else:
            await state.update_data(text_note=message.text)
            await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
            await state.set_state(AddNote_lecture.id_photo)


@admin_router_2.message(AddNote_lecture.id_photo,F.photo)
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
    await state.set_state(AddNote_lecture.id_doc)




@admin_router_2.message(AddNote_lecture.id_photo, F.text)
async def c_change3(message: types.Message, state: FSMContext):
    if message.text.lower() =='-':
        await state.update_data(id_photo=message.text)
        await state.set_state(AddNote_lecture.id_doc)
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
    else:
        await message.answer('Отправьте фотографии\n•Максимум 10 фотографий\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

@admin_router_2.message(AddNote_lecture.id_doc,F.document)
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
    await message.answer("<<<Меню>>>", reply_markup=menu())

@admin_router_2.message(AddNote_lecture.id_doc, F.text)
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
        await message.answer("<<<Меню>>>", reply_markup=menu())
    else:
        await message.answer('Отправьте документы\n•Максимум 10 документов\n•Одним сообщением\n•Введите "-",если нечего записывать\n•Введите "Отмена" для полной отмены')
        return

# Добавить_лекцию-----------------------------------------------------


# Показать_лекцию-----------------------------------------------------


class ShowNote_lecture(StatesGroup):
    subject = State()
    how_show = State()
    date_subject = State()



@admin_router_2.callback_query(StateFilter(None),F.data == 'показать лекцию')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!', reply_markup=add_hw(rez_db[0][0],type_note='лекция'))
    await state.set_state(ShowNote_lecture.subject)


@admin_router_2.callback_query(StateFilter('*'),F.data == 'показать лекцию_2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_lecture.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='лекция'))
    await state.set_state(ShowNote_lecture.subject)


@admin_router_2.callback_query(ShowNote_lecture.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_lecture) == 0:
        subject_ed_lecture.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_лекция',
        'По датам': 'по числам_лекция',
        'Назад': 'показать лекцию_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(ShowNote_lecture.how_show)


@admin_router_2.callback_query(StateFilter('*'),F.data == 'назад_лекция_выбор')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_lecture[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все_лекция',
        'По датам': 'по числам_лекция',
        'Назад': 'показать лекцию_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(ShowNote_lecture.how_show)


@admin_router_2.callback_query(StateFilter('*'),F.data == 'все_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    await state.clear()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_lecture) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')
    else:
        rez_db = date_b.check_count(subject=subject_ed_lecture[0], semester=str(rez_db_sem[0][0]), type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text('Лекции нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'показать лекцию_2',
        'Назад':f'назад_лекция_выбор',
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
            'Выбрать по датам': 'ещё_лекция',
            'Выбрать предмет': 'показать лекцию_2',
            'Меню': 'отмена',
        }))


@admin_router_2.callback_query(ShowNote_lecture.how_show,F.data == 'по числам_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Лекции нет!', reply_markup=del_db_btns(rez_db,type_note_2='l'))
    else:
        await call.message.edit_text(text='Вот все лекции по числам!', reply_markup=del_db_btns(rez_db,type_note_2='l'))
        await state.set_state(ShowNote_lecture.date_subject)


@admin_router_2.callback_query(StateFilter('*'),F.data == 'ещё_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_lecture[0])
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Лекции нет!', reply_markup=del_db_btns(rez_db,type_note_2='l'))
    else:
        await call.message.edit_text(text='Какую запись нужно показать?', reply_markup=del_db_btns(rez_db,type_note_2='l'))
        await state.set_state(ShowNote_lecture.date_subject)


@admin_router_2.callback_query(ShowNote_lecture.date_subject,F.data.contains('20'))
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
        'Да': 'ещё_лекция',
        'Нет': 'отмена',
        'Показать все':'все_лекция',
        'Назад':'назад_лекция_выбор'

    }))



# Удалить_домашку-----------------------------------------------------

class DelNote_lecture(StatesGroup):
    subject = State()
    how_show = State()
    del_subject = State()
    del_subject_2 = State()
    del_subject_2_2 = State()
    del_subject_3 = State()
    del_subject_4 = State()





@admin_router_2.callback_query(StateFilter(None),F.data == 'удалить лекцию')
async def dz1(call: CallbackQuery,  state: FSMContext):
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='лекция'))
    await state.set_state(DelNote_lecture.subject)

@admin_router_2.callback_query(StateFilter('*'),F.data == 'удалить лекцию_2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.clear()
    subject_ed_del_lecture.clear()
    rez_db = sem_db.select_last_semester()
    await call.message.edit_text(text='Выберете предмет!',reply_markup=add_hw(rez_db[0][0],type_note='лекция'))
    await state.set_state(DelNote_lecture.subject)


@admin_router_2.callback_query(DelNote_lecture.subject,F.data)
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = call.data)
    if len(subject_ed_del_lecture) == 0:
        subject_ed_del_lecture.append(call.data)

    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все2_лекция',
        'По датам': 'по числам2_лекция',
        'Назад': 'удалить лекцию_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(DelNote_lecture.how_show)

@admin_router_2.callback_query(StateFilter('*'),F.data == 'назад_удалить_выбор_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(subject = subject_ed_del_lecture[0])
    await call.message.edit_text(text='Как лучше её показать?',reply_markup=get_inlineMix_btns(btns={
        'Все': 'все2_лекция',
        'По датам': 'по числам2_лекция',
        'Назад': 'удалить лекцию_2',
        'Отмена': 'отмена'
    }))
    await state.set_state(DelNote_lecture.how_show)

@admin_router_2.callback_query(StateFilter('*'),F.data == 'все2_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del_lecture) == 0:
        rez_db = date_b.check_count(subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')
    else:
        rez_db = date_b.check_count(subject=subject_ed_del_lecture[0],semester=str(rez_db_sem[0][0]),type_note='l')
    if len(rez_db) == 0:
        await call.message.edit_text('Лекции нет!',reply_markup=get_inlineMix_btns(btns={
        'Выбрать предмет': 'удалить лекцию_2',
        'Назад':'назад_удалить_выбор_лекция',
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

            album_builder = MediaGroupBuilder(caption=f'Уникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
                    f'Фотографий к этой записи нет \n\nУникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
              await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',reply_markup=del_db_vse_btns(rez_db,type_note='l'))
        await state.set_state(DelNote_lecture.del_subject_2)

@admin_router_2.callback_query(DelNote_lecture.del_subject_2,F.data)
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
        caption=f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[0][6]}')

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
            f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[0][6]}')
        a = 0
    else:
        await call.message.answer_media_group(album_builder.build())
    if b == 1:
        await call.message.answer('Документов к этой записи нет!')
        b = 0
    else:
        await call.message.answer_media_group(album_builder_2.build())

    await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
        'Да': 'да_лекция',
        'Нет': 'нет_удалить_лекция',
        'Отмена': 'отмена',
    },sizes=(1,1,1,1)))
    await state.set_state(DelNote_lecture.del_subject)


@admin_router_2.callback_query(DelNote_lecture.del_subject_2_2,F.data)
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
        caption=f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[0][6]}')

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
            f'Уникальный номер: {call.data}\n\n{rez_db[0][1]}\n\nДобавил: {rez_db[0][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[0][6]}')
        a = 0
    else:
        await call.message.answer_media_group(album_builder.build())
    if b == 1:
        await call.message.answer('Документов к этой записи нет!')
        b = 0
    else:
        await call.message.answer_media_group(album_builder_2.build())

    await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
        'Да': 'да_по_числам_лекция2',
        'Нет': 'нет_удалить_по_числам_лекция',
        'Отмена': 'отмена',
    },sizes=(1,1,1,1)))
    await state.set_state(DelNote_lecture.del_subject)


@admin_router_2.callback_query(DelNote_lecture.del_subject,F.data == 'нет_удалить_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del_lecture) == 0:
        rez_db = date_b.check_count(subject=data_turp[0], semester=str(rez_db_sem[0][0]), type_note='l')
    else:
        rez_db = date_b.check_count(subject=subject_ed_del_lecture[0], semester=str(rez_db_sem[0][0]), type_note='l')

    await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',
                              reply_markup=del_db_vse_btns(rez_db,type_note='l'))
    await state.set_state(DelNote_lecture.del_subject_2)



@admin_router_2.callback_query(DelNote_lecture.del_subject,F.data == 'нет_удалить_по_числам_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):

    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())


    rez_db_sem = sem_db.select_last_semester()
    if len(subject_ed_del_lecture) == 0:
        rez_db = date_b.select_subject_date(date_subject=data_turp[1], subject=data_turp[0],
                                            semester=str(rez_db_sem[0][0]), type_note='l')
    else:
        rez_db = date_b.select_subject_date(date_subject=data_turp[1], subject=data_turp[0],
                                            semester=str(rez_db_sem[0][0]), type_note='l')

    await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',
                              reply_markup=del_db_vse_btns(rez_db,type_note='l'))
    await state.set_state(DelNote_lecture.del_subject_2_2)

@admin_router_2.callback_query(DelNote_lecture.del_subject,F.data == 'да_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())

    rez_db_last_sem = sem_db.select_last_semester()
    date_b.del_vse_subject(note_id=date_turp[1],semester=rez_db_last_sem[0][0])
    await call.message.edit_text(f'Удалили запись с уникальным номером: {date_turp[1]}')
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())
    await state.clear()



@admin_router_2.callback_query(StateFilter('*'),F.data == 'по числам2_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())

    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.check_date(subject=data_turp[0], semester=str(rez_db_sem[0][0]), type_note='l')

    if len(rez_db) == 0:
        await call.message.edit_text(text='Лекции нет!', reply_markup=del_db_btns(rez_db,type_note='d',type_note_2='l'))
    else:
        await call.message.edit_text('Вот все лекции по числам!',reply_markup=del_db_btns(rez_db,type_note='d',type_note_2='l'))
        await state.set_state(DelNote_lecture.del_subject_4)

@admin_router_2.callback_query(DelNote_lecture.del_subject_4,F.data.contains('20'))
async def dz1(call: CallbackQuery,  state: FSMContext):
    await state.update_data(del_subject = call.data)
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())


    rez_db_sem = sem_db.select_last_semester()
    rez_db = date_b.select_subject_date(date_subject=data_turp[1],subject=data_turp[0],semester=str(rez_db_sem[0][0]),type_note='l')


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

            await call.message.answer('Эту запись вы желаете удалить?',reply_markup=get_inlineMix_btns(btns={
                'Да': 'да_лекция',
                'Нет': 'по числам2_лекция',
                'Отмена': 'отмена',
            },sizes=(1,1,1)))
            await state.set_state(DelNote_lecture.del_subject_3)
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

            album_builder = MediaGroupBuilder(caption=f'Уникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
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
                    f'Фотографий к этой записи нет \n\nУникальный номер: {rez_db[i][0]}\n\n{rez_db[i][1]}\n\nДобавил: {rez_db[i][3]}\nДата добавления: {dat_1_rez}\n\nСостоялась: {dat_2_rez}\nОписание: {rez_db[i][6]}')
                a = 0
            else:
                await call.message.answer_media_group(album_builder.build())
            if b == 1:
                await call.message.answer('Документов к этой записи нет!')
                b = 0
            else:
              await call.message.answer_media_group(album_builder_2.build())

        await call.message.answer('Выберете уникальный номер записи,которую собираетесь удалять!',reply_markup=del_db_vse_btns(rez_db,type_note='l'))
        await state.set_state(DelNote_lecture.del_subject_2_2)


@admin_router_2.callback_query(DelNote_lecture.del_subject,F.data == 'да_по_числам_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    rez_db_last_sem = sem_db.select_last_semester()
    date_b.del_vse_subject(note_id=date_turp[1],semester=rez_db_last_sem[0][0])
    await call.message.edit_text(f'Удалили запись с уникальным номером: {date_turp[2]}')
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())
    await state.clear()

@admin_router_2.callback_query(DelNote_lecture.del_subject,F.data == 'да_по_числам_лекция2')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    date_turp = tuple(date_zr.values())
    rez_db_last_sem = sem_db.select_last_semester()
    date_b.del_vse_subject(note_id=date_turp[2],semester=rez_db_last_sem[0][0])
    await call.message.edit_text(f'Удалили запись с уникальным номером: {date_turp[2]}')
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())
    await state.clear()



@admin_router_2.callback_query(DelNote_lecture.del_subject_3,F.data == 'да_лекция')
async def dz1(call: CallbackQuery,  state: FSMContext):
    date_zr = await state.get_data()
    data_turp = tuple(date_zr.values())
    rez_db_sem = sem_db.select_last_semester()
    date_b.delete_subject_date(subject=data_turp[0],date_subject=data_turp[1],semester=rez_db_sem[0][0],type_note='l')
    await call.message.edit_text('Удалил!')
    await state.clear()
    rez_db_last_sem = sem_db.select_last_semester()
    await call.message.answer("<<<Меню>>>", reply_markup=menu())









