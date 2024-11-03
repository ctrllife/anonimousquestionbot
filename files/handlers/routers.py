from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from files.keyboards.inline_keyboards import *
import files.database.requests as rq
from resources.config import CHANNELS, NOT_SUB_MESSAGE, ADMIN_IDS
from files.defs import check_sub, GetMessage, send_to_get, SendMessage, re_nick_anonim, send_to_get_answer, Mailing, \
    send_message_to_id

main_router = Router()


@main_router.message(GetMessage.message_text)
async def send_message(message: types.Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    await message.answer(text='<b>Ваше сообщение успешно отправлено ✅</b>', parse_mode='HTML')
    await send_to_get(ref_id=data["ref"], message_text=data["message_text"], sender_id=data["sender_id"])
    await state.clear()


@main_router.message(SendMessage.message_text)
async def send_message(message: types.Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    await send_to_get_answer(ref_id=data["ref"], message_text=data["message_text"], sender_id=data["sender_id"])
    await message.answer(text='<b>Ваше сообщение успешно отправлено ✅</b>', parse_mode='HTML')
    await state.clear()


@main_router.message(CommandStart())
async def start_bot(message: types.Message, state: FSMContext):
    if await check_sub(CHANNELS, message.from_user.id):
        await rq.set_user(message.from_user.id, message.from_user.username)

        if len(message.text) > 6:
            ref = message.text[7:]
        else:
            ref = ''

        if len(ref) > 0:
            if int(ref) == message.from_user.id:
                await message.answer(
                    '❌ <b>Нельзя отправлять сообщения самому себе! Отправьте ссылку другому пользователю, в канал или чат! </b> ❌',
                    parse_mode='HTML')
            else:
                await state.set_state(GetMessage.ref)
                await state.update_data(ref=ref)
                await state.set_state(GetMessage.sender_id)
                await state.update_data(sender_id=message.from_user.id)
                await state.set_state(GetMessage.message_text)
                await message.answer('✍️ <b>Напишите вопрос, который вы хотели задать владельцу этой ссылки:</b>',
                                     parse_mode='HTML')
        else:
            await message.answer_photo(
                photo='AgACAgIAAxkBAAMOZwwYPMiEemup8ly-YkpUxmTiVzQAAmXqMRuBllBI7IT3seTkEKYBAAMCAAN4AAM2BA', caption=f'''
<b>Добро пожаловать, @{message.from_user.username}!
Это бот для отправки анонимных сообщений ✉️</b>

Например, вы публикуете свою ссылку в личном канале, далее ваши подписчики переходят по ней и задают вам вопросы, которые придут в этого бота. 

Потом можете ответить на полученное сообщение, нажав соответствующую кнопку ✨

Нажмите на кнопку 
<b>"🔗 Получить ссылку"</b> для продолжения работы 👇
''', reply_markup=start_kb, parse_mode='HTML')
    else:
        await message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.callback_query(F.data == 'get_link')
async def get_link(callback: types.CallbackQuery):
    if await check_sub(CHANNELS, callback.message.from_user.id):
        await callback.answer('Вы выбрали "🔗 Получить ссылку"')
        await callback.message.answer(f'''
<b>✉️ Ваша ссылка для анонимных сообщений:</b>
    
https://t.me/anonimous_questions_bot?start={callback.from_user.id}
    
Нажмите ниже 
<b>"🔗 Поделиться ссылкой"</b>, чтобы отправить ссылку пользователю, в чат или в канал 🔥
    ''', parse_mode='HTML', reply_markup=await share_link_kb(callback.from_user.id))
    else:
        await callback.message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.callback_query(F.data == 'check_sub')
async def check_sub_channels(callback: types.CallbackQuery):
    if await check_sub(CHANNELS, callback.from_user.id):
        await callback.message.answer(text='''
<b>Всё отлично, все подписки проверены! ✅</b>

Теперь нажмите /start для перезапуска бота 🔄
''', parse_mode='HTML')
    else:
        await callback.message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.callback_query(F.data == 'answer_message')
async def answer_message(callback: types.CallbackQuery, state: FSMContext):
    if await check_sub(CHANNELS, callback.message.from_user.id):
        await state.set_state(SendMessage.ref)
        await state.update_data(ref=await re_nick_anonim(callback.message.text[44:54]))
        await state.set_state(SendMessage.sender_id)
        await state.update_data(sender_id=callback.from_user.id)
        await state.set_state(SendMessage.message_text)
        await callback.message.answer(text='<b>✍️ Напишите ответ на вопрос, который вам задали:</b>', parse_mode='HTML')
    else:
        await callback.message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.callback_query(F.data == 'write_message')
async def write_message(callback: types.CallbackQuery, state: FSMContext):
    if await check_sub(CHANNELS, callback.message.from_user.id):
        await state.set_state(GetMessage.ref)
        await state.update_data(ref=await re_nick_anonim(callback.message.text[52:62]))
        await state.set_state(GetMessage.sender_id)
        await state.update_data(sender_id=callback.from_user.id)
        await state.set_state(GetMessage.message_text)
        await callback.message.answer(text='✍️ <b>Напишите вопрос, который вы хотели задать владельцу этой ссылки:</b>',
                                      parse_mode='HTML')
    else:
        await callback.message.answer(text=f'''
    <b>{NOT_SUB_MESSAGE}</b>''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.message(Command('my_link'))
async def my_link(message: types.Message):
    if await check_sub(CHANNELS, message.from_user.id):
        await message.answer(f'''
<b>Ваша ссылка для анонимных сообщений ✉️:</b>

https://t.me/anonimous_questions_bot?start={message.from_user.id}

Нажмите ниже 
<b>"🔗 Поделиться ссылкой"</b>, чтобы отправить ссылку пользователю, в чат или в канал 🔥
''', parse_mode='HTML', reply_markup=await share_link_kb(message.from_user.id))
    else:
        await message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.message(Command('links'))
async def links(message: types.Message):
    if await check_sub(CHANNELS, message.from_user.id):
        await message.answer(text='''
<b>Здесь вы можете найти канал и сайт разработчика ✨</b>
''', parse_mode='HTML', reply_markup=links_kb)
    else:
        await message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.message(Command('admin'))
async def admin(message: types.Message):
    if await check_sub(CHANNELS, message.from_user.id):
        if str(message.from_user.id) in ADMIN_IDS:
            await message.answer(text='<b>🍺 Админская панель 🍺</b>', reply_markup=admin_kb, parse_mode='HTML')
        else:
            pass

    else:
        await message.answer(text=f'''
<b>{NOT_SUB_MESSAGE}</b>
''', parse_mode='HTML', reply_markup=await sub_channels_kb())


@main_router.callback_query(F.data == 'mailing')
async def mailing_message_text(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Mailing.message_text)
    await callback.message.answer(text='<b>Введите текст сообщения для рассылки с тегами языка разметки HTML:</b>',
                                  parse_mode='HTML')


@main_router.message(Mailing.message_text)
async def mailing_photo(message: types.Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    await state.set_state(Mailing.photo)
    await message.answer(text='<b>Отправьте фото поста для рассылки:</b>', parse_mode='HTML')


@main_router.message(Mailing.photo)
async def mailing_button_text(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(Mailing.button_text)
    await message.answer(text='<b>Введите название inline кнопки для рассылки:</b>',
                         parse_mode='HTML')


@main_router.message(Mailing.button_text)
async def mailing_button_url(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await state.set_state(Mailing.button_url)
    await message.answer(text='<b>Введите URL inline кнопки для рассылки:</b>',
                         parse_mode='HTML')


@main_router.message(Mailing.button_url)
async def mailing_pre_send(message: types.Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    data = await state.get_data()
    await message.answer_photo(photo=data["photo"], caption=data["message_text"], parse_mode='HTML',
                               reply_markup=await create_buttons(data["button_text"], data["button_url"]))
    await state.set_state(Mailing.check)
    await message.answer(
        text='<b>Проверьте корректность поста для рассылки, и если всё верно - введите "1" без кавычек, после чего ваш пост отправится всем пользователям бота</b>',
        parse_mode='HTML')


@main_router.message(Mailing.check)
async def mailing_send(message: types.Message, state: FSMContext):
    await state.update_data(check=message.text)
    data = await state.get_data()
    if data["check"] == '1':
        ids = await rq.all_ids()
        for id in ids:
            await send_message_to_id(id, data["message_text"], data["photo"], data["button_text"], data["button_url"])
    await message.answer('<b>Рассылка успешно проведена ✅</b>', parse_mode='HTML')
    await state.clear()


@main_router.callback_query(F.data == 'statistics')
async def statistics(callback: types.CallbackQuery):
    count = await rq.count_ids()
    await callback.message.answer(text=f'''
📊 <b>Статистика бота:</b>
➖ Количество пользователей: {count} 

Цифра обновляется при каждом запросе, т. е. это на данный момент ✅

<b>@anonimous_questions_bot</b> 💬
''', parse_mode='HTML')



