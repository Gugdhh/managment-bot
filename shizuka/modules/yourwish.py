import random
from shizuka import telethn as tbot
from telethon import events

@tbot.on(events.NewMessage(pattern="/wish"))
async def wish(alexa):
   if alexa.is_reply:
         mm = random.randint(1,100)
         lol = await alexa.get_reply_message()
         await tbot.send_message(alexa.chat_id, f"**ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛ.✨**\n\n__ᴄʜᴀɴᴄᴇ ᴏғ sᴜᴄᴄᴇss {mm}%__", reply_to=lol)
   if not alexa.is_reply:
         mm = random.randint(1,100) 
         ALEXA = "https://telegra.ph/file/1e1d6269dbc443b0e5bd0.jpg"
         await tbot.send_file(alexa.chat_id, ALEXA,caption=f"**ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛ.✨**\n\n__ᴄʜᴀɴᴄᴇ ᴏғ sᴜᴄᴄᴇss {mm}%__", reply_to=alexa)
         lol = await alexa.get_reply_message()
         await tbot.send_file(alexa.chat_id, f"**ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛ.✨**\n\n__ᴄʜᴀɴᴄᴇ ᴏғ sᴜᴄᴄᴇss{mm}%__", reply_to=lol, file=ALEXA)
   if not alexa.is_reply:
         mm = random.randint(1,100)
         ALEXA = "https://telegra.ph/file/e831d5e93a836a3c7aa7f.jpg"
         await tbot.send_file(alexa.chat_id,f"**ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛ.✨**\n\n__ᴄʜᴀɴᴄᴇ ᴏғ sᴜᴄᴄᴇss {mm}%__", reply_to=lol, file=ALEXA)
         await tbot.send_file(alexa.chat_id, ALEXA,caption=f"**Your wish has been cast.✨**\n__chance of success {mm}%__", reply_to=alexa)
         lol = await alexa.get_reply_message()
         await tbot.send_file(alexa.chat_id, f"**ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛ.✨**\n__ᴄʜᴀɴᴄᴇ ᴏғ sᴜᴄᴄᴇss {mm}%__", reply_to=lol)
   if not alexa.is_reply:
         mm = random.randint(1,100)
         ALEXA = "https://telegra.ph/file/a4b421a72f39e6ed158fa.jpg"
         await tbot.send_file(alexa.chat_id, ALEXA,caption=f"**ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛ.✨**\n__ᴄʜᴀɴᴄᴇ ᴏғ sᴜᴄᴄᴇss {mm}%__", reply_to=lol,file=alexa)

        
   
