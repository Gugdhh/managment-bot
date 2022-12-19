from pyrogram import filters

from shizuka import pgram #pgram
from shizuka.utils.errors import capture_err
from shizuka.modules.MODULESHELPER.carbonfunc import make_carbon


@pgram.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.`"
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.`"
        )
    m = await message.reply_text("`ᴍᴀᴋɪɴɢ ᴄᴀʀʙᴏɴ...`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`ᴜᴘʟᴏᴀᴅɪɴɢ...`")
    await pgram.send_document(message.chat.id, carbon) 
    await m.delete()
    carbon.close()
    
__help__ = """
 *Carbon Maker...*
 - `/carbon` Make carbon of every text.
"""

__mod_name__ = "🌼 ᴄᴀʀʙᴏɴ"

# Roses are red, Violets are blue, A face like yours, Belongs in a zoo
