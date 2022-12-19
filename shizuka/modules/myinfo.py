from telethon import events, Button, custom, version
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import os,re
import requests
import datetime
import time
from datetime import datetime
import random
from PIL import Image
from io import BytesIO
from shizuka import telethn as bot
from shizuka import telethn as tgbot
from shizuka.events import register
from shizuka import dispatcher


edit_time = 5
""" =======================SHIZUKA====================== """
file1 = "https://telegra.ph/file/e1a3bb987e73c3a066dde.jpg"
file2 = "https://telegra.ph/file/804dbd96d120fb7ad7941.jpg"
file3 = "https://telegra.ph/file/41aa5e5bb3dcdc95342fd.jpg"
file4 = "https://telegra.ph/file/6eda47c03eaf8b8c26cc4.jpg"
file5 = "https://telegra.ph/file/1e1d6269dbc443b0e5bd0.jpg"
""" =======================SHIZUKA====================== """


@register(pattern="/myinfo")
async def proboyx(event):
    chat = await event.get_chat()
    current_time = datetime.utcnow()
    firstname = event.sender.first_name
    button = [[custom.Button.inline("information",data="informations")]]
    on = await bot.send_file(event.chat_id, file=file2,caption= f"hello {firstname}, \n Click The Below Button \n To Get Your Info", buttons=button)

    await asyncio.sleep(edit_time)
    ok = await bot.edit_message(event.chat_id, on, file=file3, buttons=button) 

    await asyncio.sleep(edit_time)
    ok2 = await bot.edit_message(event.chat_id, ok, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok3 = await bot.edit_message(event.chat_id, ok2, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok4 = await bot.edit_message(event.chat_id, ok3, file=file2, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok5 = await bot.edit_message(event.chat_id, ok4, file=file1, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok6 = await bot.edit_message(event.chat_id, ok5, file=file3, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
  try:
    boy = event.sender_id
    PRO = await bot.get_entity(boy)
    LILIE = "ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Ayraupdates \n\n"
    LILIE += f"ғɪʀsᴛ ɴᴀᴍᴇ : {PRO.first_name} \n"
    LILIE += f"ʟᴀsᴛ ɴᴀᴍᴇ : {PRO.last_name}\n"
    LILIE += f"ʏᴏᴜ ʙᴏᴛ : {PRO.bot} \n"
    LILIE += f"ʀᴇsᴛʀɪᴄᴛᴇᴅ : {PRO.restricted} \n"
    LILIE += f"ᴜsᴇʀ ɪᴅ : {boy}\n"
    LILIE += f"ᴜsᴇʀɴᴀᴍᴇ : {PRO.username}\n"
    await event.answer(LILIE, alert=True)
  except Exception as e:
    await event.reply(f"{e}")


__command_list__ = [
    "myinfo"
]


__help__ = """
 *Info generator...*
 - `/myinfo` generate your own info.
"""

__mod_name__ = "ℹ️ ᴍʏɪɴғᴏ"

