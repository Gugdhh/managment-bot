import asyncio
from asyncio import sleep

from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins

from shizuka import telethn, OWNER_ID, DEV_USERS, DRAGONS, DEMONS

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

OFFICERS = [OWNER_ID] + DEV_USERS + DRAGONS + DEMONS

# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in OFFICERS:
            admin = True
            break
    return admin



@telethn.on(events.NewMessage(pattern=f"^[!/]zombies ?(.*)"))
async def zombies(event):
    """ ғᴏʀ .ᴢᴏᴍʙɪᴇs ᴄᴏᴍᴍᴀɴᴅ, ʟɪsᴛ ᴀʟʟ ᴛʜᴇ ᴢᴏᴍʙɪᴇs ɪɴ ᴀ ᴄʜᴀᴛ. """

    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "ɴᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ғᴏᴜɴᴅ, ɢʀᴏᴜᴘ ɪs ᴄʟᴇᴀɴ."

    if con != "clean":
        find_zombies = await event.respond("Searching For Zombies...")
        async for user in event.client.iter_participants(event.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"ғᴏᴜɴᴅ **{del_u}** ᴢᴏᴍʙɪᴇs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.\
            \nClean Them By Using - `/zombies clean`"
        await find_zombies.edit(del_status)
        return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not await is_administrator(user_id=event.from_id, message=event):
        await event.respond("ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")
        return

    if not admin and not creator:
        await event.respond("ɪ ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ!")
        return

    cleaning_zombies = await event.respond("ᴄʟᴇᴀɴɪɴɢ ᴢᴏᴍʙɪᴇs...")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await cleaning_zombies.edit("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʙᴀɴ ʀɪɢʜᴛs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"ᴄʟᴇᴀɴᴇᴅ `{del_u}` ᴢᴏᴍʙɪᴇs"

    if del_a > 0:
        del_status = f"ᴄʟᴇᴀɴᴇᴅ `{del_u}` ᴢᴏᴍʙɪᴇs \
        \n`{del_a}` Zombie Admin Accounts Are Not Removed!"

    await cleaning_zombies.edit(del_status)



__help__ = """
 *Zombie Remover From Your Group...*
 - `/zombies` remove all deleted account from your group.
 - `/react` react on someone mesg
"""

__mod_name__ = "🧟 ᴢᴏᴍʙɪᴇ"