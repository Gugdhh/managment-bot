
from pyrogram import filters #carbon by vegeta
from shizuka import pgram as pbot, BOT_USERNAME, UPDATES_CHANNEL
from shizuka.utils.errors import capture_err
from shizuka.utils.make_carbon import make_carbon

@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("**🙄ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.**")
    if not message.reply_to_message.text:
        return await message.reply_text("**🙄ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.**")
    m = await message.reply_text("**⬇ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("**⬆ᴜᴘʟᴏᴀᴅɪɴɢ...**")
    msg = "**ᴍᴀᴅᴇ ʙʏ @{BOT_USERNAME}}**"
    await pbot.send_photo(message.chat.id, carbon,caption=msg)
    await m.delete()
    carbon.close()
