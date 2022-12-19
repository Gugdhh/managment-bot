import html
import os
from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from shizuka import DRAGONS, dispatcher
from shizuka.modules.disable import DisableAbleCommandHandler
from shizuka.modules.helper_funcs.chat_status import (bot_admin, can_pin,
                                                           can_promote,
                                                          user_can_changeinfo,
                                                           connection_status,
                                                           user_admin,
                                                           ADMIN_CACHE, )


from shizuka.modules.helper_funcs.extraction import (extract_user,
                                                        extract_user_and_text)
from shizuka.modules.log_channel import loggable
from shizuka.modules.helper_funcs.alternate import send_message


@bot_admin
@user_admin
def set_desc(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("ʏᴏᴜ'ʀᴇ ᴍɪssɪɴɢ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀᴛ ɪɴғᴏ!")

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    else:
        return msg.reply_text("sᴇᴛᴛɪɴɢ ᴇᴍᴘᴛʏ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴡᴏɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ!")
    try:
        if len(desc) > 255:
            return msg.reply_text("ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴍᴜsᴛ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ 𝟸𝟻𝟻 ᴄʜᴀʀᴀᴄᴛᴇʀs!")
        context.bot.set_chat_description(chat.id, desc)
        msg.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ᴄʜᴀᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ɪɴ {chat.title}!")
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")        

@bot_admin
@user_admin
def setchat_title(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    args = context.args

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("𝚢𝚘𝚞 𝚍𝚘𝚗'𝚝 𝚑𝚊𝚟𝚎 𝚎𝚗𝚘𝚞𝚐𝚑 𝚛𝚒𝚐𝚑𝚝𝚜 𝚝𝚘 𝚌𝚑𝚊𝚗𝚐𝚎 𝚌𝚑𝚊𝚝 𝚒𝚗𝚏𝚘!")
        return

    title = " ".join(args)
    if not title:
        msg.reply_text("𝚎𝚗𝚝𝚎𝚛 𝚜𝚘𝚖𝚎 𝚝𝚎𝚡𝚝 𝚝𝚘 𝚜𝚎𝚝 𝚗𝚎𝚠 𝚝𝚒𝚝𝚕𝚎 𝚒𝚗 𝚢𝚘𝚞𝚛 𝚌𝚑𝚊𝚝!")
        return

    try:
        context.bot.set_chat_title(int(chat.id), str(title))
        msg.reply_text(
            f"Successfully set <b>{title}</b> as new chat title!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")
        return
        
        
@bot_admin
@user_admin
def setchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ʏᴏᴜ ᴀʀᴇ ᴍɪssɪɴɢ ʀɪɢʜᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ!")
        return

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ sᴏᴍᴇ ᴘʜᴏᴛᴏ ᴀs ᴄʜᴀᴛ ᴘɪᴄ!")
            return
        dlmsg = msg.reply_text("Just a sec...")
        tpic = context.bot.get_file(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                context.bot.set_chat_photo(int(chat.id), photo=chatp)
                msg.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ᴄʜᴀᴛᴘɪᴄ!")
        except BadRequest as excp:
            msg.reply_text(f"ᴇʀʀᴏʀ! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇ ᴘʜᴏᴛᴏ ᴏʀ ғɪʟᴇ ᴛᴏ sᴇᴛ ɴᴇᴡ ᴄʜᴀᴛ ᴘɪᴄ!")
        
@bot_admin
@user_admin
def rmchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴅᴇʟᴇᴛᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ")
        return
    try:
        context.bot.delete_chat_photo(int(chat.id))
        msg.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄʜᴀᴛ's ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ!")
    except BadRequest as excp:
        msg.reply_text(f"ᴇʀʀᴏʀ! {excp.message}.")
        return
    

@run_async
@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def promote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if not (promoter.can_promote_members or
            promoter.status == "creator") and not user.id in DRAGONS:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ.."
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status == 'administrator' or user_member.status == 'creator':
        message.reply_text(
            "ʜᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ sᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ's ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text(
          "ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴍʏsᴇʟғ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages, )
        
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text(
                "ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ sᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪsɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.")
        else:
            message.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴍᴏᴛɪɴɢ.")
        return

    bot.sendMessage(
        chat.id,
        f"sᴜᴄᴇssғᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ<b>{user_member.user.first_name or user_id}</b>!",
        parse_mode=ParseMode.HTML)

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#PROMOTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message




  
@run_async
@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def demote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ.."
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status == 'creator':
        message.reply_text(
            "ᴛʜɪs ᴘᴇʀsᴏɴ ᴄʀᴇᴀᴛᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ, ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴅᴇᴍᴏᴛᴇ ᴛʜᴇᴍ?")
        return

    if not user_member.status == 'administrator':
        message.reply_text("ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴡʜᴀᴛ ᴡᴀsɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ!")
        return

    if user_id == bot.id:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴍʏsᴇʟғ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ.")
        return

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False)

        bot.sendMessage(
            chat.id,
            f"sᴜᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ <b>{user_member.user.first_name or user_id}</b>!",
            parse_mode=ParseMode.HTML)

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#DEMOTED\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        message.reply_text(
            "ᴄᴏᴜʟᴅ ɴᴏᴛ ᴅᴇᴍᴏᴛᴇ. ɪ ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀᴅᴍɪɴ, ᴏʀ ᴛʜᴇ ᴀᴅᴍɪɴ sᴛᴀᴛᴜs ᴡᴀs ᴀᴘᴘᴏɪɴᴛᴇᴅ ʙʏ ᴀɴᴏᴛʜᴇʀ"
            " ᴜsᴇʀ, sᴏ ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴜᴘᴏɴ ᴛʜᴇᴍ!")
        return


@run_async
@user_admin
def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text("ᴀᴅᴍɪɴs ᴄᴀᴄʜᴇ ʀᴇғʀᴇsʜᴇᴅ!")


@run_async
@connection_status
@bot_admin
@can_promote
@user_admin
def set_title(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ.."
        )
        return

    if user_member.status == 'creator':
        message.reply_text(
            "ᴛʜɪs ᴘᴇʀsᴏɴ ᴄʀᴇᴀᴛᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ, ʜᴏᴡ ᴄᴀɴ ɪ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ʜɪᴍ?")
        return

    if not user_member.status == 'administrator':
        message.reply_text(
            "ᴄᴀɴ'ᴛ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ɴᴏɴ-ᴀᴅᴍɪɴs!\ɴᴘʀᴏᴍᴏᴛᴇ ᴛʜᴇᴍ ғɪʀsᴛ ᴛᴏ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ!"
        )
        return

    if user_id == bot.id:
        message.reply_text(
           "ɪ ᴄᴀɴ'ᴛ sᴇᴛ ᴍʏ ᴏᴡɴ ᴛɪᴛʟᴇ ᴍʏsᴇʟғ! ɢᴇᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴀᴅᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ."
        )
        return

    if not title:
        message.reply_text("sᴇᴛᴛɪɴɢ ʙʟᴀɴᴋ ᴛɪᴛʟᴇ ᴅᴏᴇsɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ!")
        return

    if len(title) > 16:
        message.reply_text(
            "ᴛʜᴇ ᴛɪᴛʟᴇ ʟᴇɴɢᴛʜ ɪs ʟᴏɴɢᴇʀ ᴛʜᴀɴ 𝟷𝟼 ᴄʜᴀʀᴀᴄᴛᴇʀs.\ɴᴛʀᴜɴᴄᴀᴛɪɴɢ ɪᴛ ᴛᴏ 𝟷𝟼 ᴄʜᴀʀᴀᴄᴛᴇʀs."
        )

    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        message.reply_text(
        "ɪ ᴄᴀɴ'ᴛ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ᴀᴅᴍɪɴs ᴛʜᴀᴛ ɪ ᴅɪᴅɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ!")
        return

    bot.sendMessage(
        chat.id,
        f"sᴜᴄᴇssғᴜʟʟʏ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ <code>{user_member.user.first_name or user_id}</code> "
        f"to <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML)


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def pin(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    user = update.effective_user
    chat = update.effective_chat

    is_group = chat.type != "private" and chat.type != "channel"
    prev_message = update.effective_message.reply_to_message

    is_silent = True
    if len(args) >= 1:
        is_silent = not (args[0].lower() == 'notify' or args[0].lower()
                         == 'loud' or args[0].lower() == 'violent')

    if prev_message and is_group:
        try:
            bot.pinChatMessage(
                chat.id,
                prev_message.message_id,
                disable_notification=is_silent)
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#PINNED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def unpin(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user

    try:
        bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNPINNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}")

    return log_message


@run_async
@bot_admin
@user_admin
@connection_status
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat

    if chat.username:
        update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type == chat.SUPERGROUP or chat.type == chat.CHANNEL:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                "ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴛʜᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ, ᴛʀʏ ᴄʜᴀɴɢɪɴɢ ᴍʏ ᴘᴇʀᴍɪssɪᴏɴs!"
            )
    else:
        update.effective_message.reply_text(
            "ɪ ᴄᴀɴ ᴏɴʟʏ ɢɪᴠᴇ ʏᴏᴜ ɪɴᴠɪᴛᴇ ʟɪɴᴋs ғᴏʀ sᴜᴘᴇʀɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs, sᴏʀʀʏ!"
        )


@run_async
@connection_status
def adminlist(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    args = context.args
    bot = context.bot

    if update.effective_message.chat.type == "private":
        send_message(update.effective_message,
                     "This command only works in Groups.")
        return

    chat = update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title

    try:
        msg = update.effective_message.reply_text(
            'Fetching group admins...', parse_mode=ParseMode.HTML)
    except BadRequest:
        msg = update.effective_message.reply_text(
            'Fetching group admins...', quote=False, parse_mode=ParseMode.HTML)

    administrators = bot.getChatAdministrators(chat_id)
    text = "Admins in <b>{}</b>:".format(
        html.escape(update.effective_chat.title))

    bot_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == '':
            name = "☠ Deleted Account"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " +
                                (user.last_name or ""))))

        if user.is_bot:
            bot_admin_list.append(name)
            administrators.remove(admin)
            continue

        #if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "creator":
            text += "\n 👑 Legend:"
            text += "\n<code> • </code>{}\n".format(name)

            if custom_title:
                text += f"<code> ┗━ {html.escape(custom_title)}</code>\n"

    text += "\n🔱 ᴀᴅᴍɪɴs:"

    custom_admin_list = {}
    normal_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == '':
            name = "☠ Deleted Account"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " +
                                (user.last_name or ""))))
        #if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list.update({custom_title: [name]})
            else:
                normal_admin_list.append(name)

    for admin in normal_admin_list:
        text += "\n<code> • </code>{}".format(admin)

    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += "\n<code> • </code>{} | <code>{}</code>".format(
                custom_admin_list[admin_group][0], html.escape(admin_group))
            custom_admin_list.pop(admin_group)

    text += "\n"
    for admin_group in custom_admin_list:
        text += "\n🚨 <code>{}</code>".format(admin_group)
        for admin in custom_admin_list[admin_group]:
            text += "\n<code> • </code>{}".format(admin)
        text += "\n"

    text += "\n🤖 Bots:"
    for each_bot in bot_admin_list:
        text += "\n<code> • </code>{}".format(each_bot)

    try:
        msg.edit_text(text, parse_mode=ParseMode.HTML)
    except BadRequest:  # if original message is deleted
        return


__help__ = """
 • `/admins`*:* list of admins in the chat

*Admins only:*
 • `/pin`*:* silently pins the message replied to - add `'loud'` or `'notify'` to give notifs to users
 • `/unpin`*:* unpins the currently pinned message
 • `/invitelink`*:* gets invitelink
 • `/promote`*:* promotes the user replied to
 • `/demote`*:* demotes the user replied to
 • `/title <title here>`*:* sets a custom title for an admin that the bot promoted
 • `/admincache`*:* force refresh the admins list
 
 *gorup info changer*:
 - /setgpic*:* reply to the image set chat pic.
 - /delgpic*:* delete a chat pic.
 - /settitle*:* (text) bot can change chat tilte.
 - /setdesc*:* (text) bot can change chat descrepicion.
 
 *Delete messages*:
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it if replied to a message.
"""

ADMINLIST_HANDLER = DisableAbleCommandHandler("admins", adminlist)

PIN_HANDLER = CommandHandler("pin", pin, filters=Filters.group)
SET_DESC_HANDLER = CommandHandler("setdesc", set_desc, filters=Filters.group)
UNPIN_HANDLER = CommandHandler("unpin", unpin, filters=Filters.group)
SETCHATPIC_HANDLER = CommandHandler("setgpic", setchatpic, filters=Filters.group)
RMCHATPIC_HANDLER = CommandHandler("delgpic", rmchatpic, filters=Filters.group)
SETCHAT_TITLE_HANDLER = CommandHandler("setgtitle", setchat_title, filters=Filters.group)


INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote)

DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote)

SET_TITLE_HANDLER = CommandHandler("title", set_title)
ADMIN_REFRESH_HANDLER = CommandHandler(
    "admincache", refresh_admin, filters=Filters.group)

dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(SETCHATPIC_HANDLER)
dispatcher.add_handler(SET_DESC_HANDLER)
dispatcher.add_handler(RMCHATPIC_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)

dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)

__mod_name__ = "👮 ᴀᴅᴍɪɴs"
__command_list__ = [
    "adminlist", "admins", "invitelink", "promote", "demote", "admincache", "setgpic", "delgpic", "setgtitle", "setdesc"
]
__handlers__ = [
    ADMINLIST_HANDLER, PIN_HANDLER, UNPIN_HANDLER, INVITE_HANDLER,
    PROMOTE_HANDLER, DEMOTE_HANDLER, SET_TITLE_HANDLER, SETCHAT_TITLE_HANDLER, ADMIN_REFRESH_HANDLER, SETCHATPIC_HANDLER,
    RMCHATPIC_HANDLER, SET_DESC_HANDLER
]
