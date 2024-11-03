from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from resources.config import CHANNELS

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔗 Получить ссылку', callback_data='get_link')]
])


async def share_link_kb(user_id):
    share_link_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔗 Поделиться ссылкой', switch_inline_query=f'''
Лови мою ссылку для анонимных сообщений 👇
✨ Жду теперь вопросики ✨

https://t.me/anonimous_questions_bot?start={user_id}
''')]
    ])
    return share_link_kb


async def sub_channels_kb():
    keyboard = InlineKeyboardBuilder()
    for e in CHANNELS:
        keyboard.add(InlineKeyboardButton(text=f'➕ {e[0]}', url=e[2]))
    keyboard.add(InlineKeyboardButton(text='✅ Проверить', callback_data='check_sub'))
    return keyboard.adjust(1).as_markup()


async def create_buttons(button_text, button_url):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=button_text, url=button_url))
    return keyboard.adjust(1).as_markup()


answer_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍️ Ответить', callback_data='answer_message')]
])

write_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍️ Написать ещё раз', callback_data='write_message')]
])

links_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='yura_zhukoff', url='https://t.me/yura_zhukoff')],
    [InlineKeyboardButton(text='ctrllife 🌐', url='https://ctrllife.taplink.ws')]
])

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📨 Рассылка', callback_data='mailing')],
    [InlineKeyboardButton(text='📊 Статистика', callback_data='statistics')]
])
