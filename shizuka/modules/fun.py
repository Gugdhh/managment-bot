import html
import random
import re

import requests as r
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import escape_markdown

import shizuka.modules.fun_strings as fun
from shizuka import DEMONS, DRAGONS, dispatcher
from shizuka.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from shizuka.modules.helper_funcs.alternate import typing_action
from shizuka.modules.helper_funcs.chat_status import (is_user_admin)
from shizuka.modules.helper_funcs.extraction import extract_user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

GN_IMG= "https://telegra.ph/file/52eb0e2a082550fad027a.jpg"
DECIDE_IMG= "https://telegra.ph/file/313cfbc4056bd3b5cd995.jpg"
JUDGE_IMG= "https://telegra.ph/file/a2ebfdd262def30ad42a7.jpg"


@run_async
@typing_action
def goodnight(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"*Hey {escape_markdown(first_name)} \nGood Night! 😴*"
    message.reply_photo(GN_IMG,reply, parse_mode=ParseMode.MARKDOWN)

GM_IMG= "https://telegra.ph/file/9e008ed4dc87b7d155a59.jpg"
@run_async
@typing_action
def goodmorning(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"*Hey {escape_markdown(first_name)} \n Good Morning!☀*"
    message.reply_photo(GM_IMG,reply, parse_mode=ParseMode.MARKDOWN)
    
SHI_IMG= "https://telegra.ph/file/a4b421a72f39e6ed158fa.jpg"
@run_async
@typing_action
def starxboi(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    disable_web_page_preview=True,
    reply = f"✪ ʜɪ ɪᴛ ɪs ᴍᴇ sᴛᴀʀ ʙᴏɪ sʜɪᴢᴜᴋᴀ ᴏᴡɴᴇʀ \n────────────────────────\n✪ {escape_markdown(first_name)} ᴅᴏsᴛ 🥰 ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ\n────────────────────────\n✪ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴀʙᴏᴜᴛ ᴍᴇ ᴠɪsɪᴛ ᴛʜɪs [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/starboihacks369) 🥰\n────────────────────────\n✪ ──『ᴛʜᴀɴᴋs  ғᴏʀ  ᴜsɪɴɢ』"
    message.reply_photo(SHI_IMG,reply, parse_mode=ParseMode.MARKDOWN)
    
@run_async
def gbun(update, context):
    user = update.effective_user
    chat = update.effective_chat

    if update.effective_message.chat.type == "private":
        return
    if int(user.id) in DRAGONS or int(user.id) in DEMONS:
        context.bot.sendMessage(chat.id, (random.choice(fun.GBUN)))


@run_async
def gbam(update, context):
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    message = update.effective_message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        gbam_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(gbam_user.first_name)

    else:
        user1 = curr_user
        user2 = bot.first_name

    if update.effective_message.chat.type == "private":
        return
    if int(user.id) in DRAGONS or int(user.id) in DEMONS:
        gbamm = fun.GBAM
        reason = random.choice(fun.GBAM_REASON)
        gbam = gbamm.format(user1=user1, user2=user2, chatid=chat.id, reason=reason)
        context.bot.sendMessage(chat.id, gbam, parse_mode=ParseMode.HTML)

    
    
@run_async
def judge(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.JUDGE_HANDLER))
    else:
      message.reply_text(fun.JUDGE_STRINGS)
      
      
@run_async
def shizuka(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.SHIZUKA_HANDLER))
    else:
      message.reply_text(fun.SHIZUKA_STRINGS)


@run_async
def decide(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.DECIDE_HANDLER))
    else:
      message.reply_text(fun.DECIDE_STRINGS)

@run_async
@typing_action
def repo(update, context):
    update.effective_message.reply_text(fun.REPO)
  
@run_async
def insult(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.SFW_STRINGS))
    else:
      message.reply_text(random.choice(fun.SFW_STRINGS)) 
    
    
@run_async
def abuse(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(fun.ABUSE_STRINGS))

    
@run_async
def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun.SLAP_SHIZUKA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False))
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun.SLAP_TEMPLATES)
    item = random.choice(fun.ITEMS)
    hit = random.choice(fun.HIT)
    throw = random.choice(fun.THROW)

    if update.effective_user.id == 5463205082:
        temp = "Shizuka Owner @Best_FriendsFor_Ever Slaps You Noob 😁 {user2}"

    reply = temp.format(
        user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)   
    
    
@run_async
@typing_action
def truth(update, context):
    update.effective_message.reply_text(random.choice(fun.TRUTH))


@run_async
@typing_action
def dare(update, context):
    update.effective_message.reply_text(random.choice(fun.DARE))
 
@run_async
def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(fun.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(fun.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(fun.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)
       
    
GOODMORNING_HANDLER = DisableAbleMessageHandler(Filters.regex(r"(?i)(goodmorning|good morning)"), goodmorning, friendly="goodmorning")
STARXBOI_HANDLER = DisableAbleMessageHandler(Filters.regex(r"(?i)(starxboi|asad)"), starxboi, friendly="starxboi")
GOODNIGHT_HANDLER = DisableAbleMessageHandler(Filters.regex(r"(?i)(goodnight|good night)"), goodnight, friendly="goodnight")
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)

REPO_HANDLER = DisableAbleCommandHandler("repo", repo)

GBUN_HANDLER = CommandHandler("gbun", gbun)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
GBAM_HANDLER = CommandHandler("gbam", gbam)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)
TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
INSULT_HANDLER = DisableAbleCommandHandler("insult", insult)
ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
JUDGE_HANDLER = DisableAbleCommandHandler("judge", judge)
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap)
SHIZUKA_HANDLER = DisableAbleCommandHandler("shizuka", shizuka)

dispatcher.add_handler(GOODMORNING_HANDLER)
dispatcher.add_handler(STARXBOI_HANDLER)
dispatcher.add_handler(GOODNIGHT_HANDLER)
dispatcher.add_handler(INSULT_HANDLER)
dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(GBAM_HANDLER)
dispatcher.add_handler(GBUN_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(JUDGE_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(SHIZUKA_HANDLER)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(REPO_HANDLER)
dispatcher.add_handler(DARE_HANDLER)



__mod_name__ = "💞 ғᴜɴ"

__help__ = """
=>> *Fun Module all cmd are given below* 🤫
 /shizuka, /slap, /decide, /judge, /abuse, /insult, /truth, /dare, /gbam, /pat, /gbun, /repo 😊
"""
