import os

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from files.keyboards.inline_keyboards import *
from resources.config import CHANNELS
from run import bot

def_router = Router()


class GetMessage(StatesGroup):
    message_text = State()
    ref = State()
    sender_id = State()


class SendMessage(StatesGroup):
    message_text = State()
    ref = State()
    sender_id = State()


class Mailing(StatesGroup):
    message_text = State()
    photo = State()
    button_text = State()
    button_url = State()
    check = State()


class AddChannel(StatesGroup):
    name = State()
    id = State()
    url = State()
    check = State()


async def check_sub(channels, user_id):
    n = 0
    for channel in channels:

        member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)

        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
            n += 1
    if n == 1:
        return True
    return False


async def re_nick_anonim(username):
    return username[::-1]


async def send_to_get(ref_id, message_text, sender_id):
    nick_anonim = str(sender_id)[::-1]
    await bot.send_message(ref_id, f'''
📨 <b>У тебя новое анонимное сообщение от Anonim{nick_anonim}:</b>

💬 <i>{message_text}</i>''', parse_mode='HTML', reply_markup=answer_kb)


async def send_to_get_answer(ref_id, message_text, sender_id):
    nick_anonim = str(sender_id)[::-1]
    await bot.send_message(ref_id, f'''
📨 <b>У тебя есть ответ на анонимное сообщение от Anonim{nick_anonim}:</b>

💬 <i>{message_text}</i>''', parse_mode='HTML', reply_markup=write_kb)


async def send_message_to_id(id, message_text, photo, button_text, button_url):
    await bot.send_photo(chat_id=int(id), photo=photo, caption=message_text,
                         reply_markup=await create_buttons(button_text, button_url), parse_mode='HTML')
