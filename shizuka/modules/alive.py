import random
import asyncio
from pyrogram import filters, __version__ as pver
from sys import version_info
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telethon import __version__ as tver
from telegram import __version__ as lver
from shizuka import BOT_USERNAME, OWNER_USERNAME, BOT_NAME, SUPPORT_CHAT, pgram

PHOTO = [
           "https://telegra.ph/file/e1a3bb987e73c3a066dde.jpg",
           "https://telegra.ph/file/41aa5e5bb3dcdc95342fd.jpg",
           "https://telegra.ph/file/6eda47c03eaf8b8c26cc4.jpg",
           "https://telegra.ph/file/804dbd96d120fb7ad7941.jpg",
           "https://telegra.ph/file/a4b421a72f39e6ed158fa.jpg",
]

SHREYXD = [
    [
        InlineKeyboardButton(text="ʜᴇʟᴘ", url=f"https://t.me/{BOT_USERNAME}?start=help"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"http://t.me/{BOT_USERNAME}?startgroup=true"),
    ],
]

@pgram.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("⚡")
    await asyncio.sleep(1)
    await accha.edit("ᴀʟɪᴠɪɴɢ..")
    await asyncio.sleep(0.1)
    await accha.edit("ᴀʟɪᴠɪɴɢ...")
    await accha.delete()
    await asyncio.sleep(0.1)
    umm = await m.reply_sticker("CAACAgUAAxkBAAIaoWLtBw9NLiUAAS4KCEKRIKtsUrakogACRAYAAnQZaVdVqgIhigtQzykE")
    await umm.delete()
    await asyncio.sleep(0.1)
    await m.reply_photo(
        random.choice(PHOTO),
        caption=f"""**ʜᴇʏ​ ɪ ᴀᴍ {BOT_NAME}​**
        ━━━━━━━━━━━━━━━━━━━
        » **ᴍʏ ᴏᴡɴᴇʀ :** [𝚘𝚠𝚗𝚎𝚛](https://t.me/{OWNER_USERNAME})
        
        » **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
        
        » **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
        
        » **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
        
        » **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
        ━━━━━━━━━━━━━━━━━━━""",
        reply_markup=InlineKeyboardMarkup(SHREYXD)
    )
