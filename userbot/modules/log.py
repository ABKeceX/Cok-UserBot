#
# 𖣘Recode By @yangmutebabi
#

import asyncio

from telethon import events

from userbot import BOTLOG, BOTLOG_CHATID
from userbot import CMD_HELP, LOGS, bot
from userbot.events import register, cok_cmd
from userbot.modules.sql_helper import no_log_pms_sql
from userbot.modules.sql_helper.globals import addgvar, gvarstatus
from userbot.utils import format as _format
from userbot.utils.logger import logging
from userbot.utils.tools import media_type, edit_delete

LOGS = logging.getLogger(__name__)


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM: 
                    await LOG_CHATS_.NEWPM.edit(
                        LOG_CHATS_.NEWPM.text.replace(
                            "**💌 #NEW_MESSAGE**",
                            f" 𖣘 `{LOG_CHATS_.COUNT}` **Pesan**",
                        )
                    )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**💌 #MENERUSKAN #PESAN_BARU**\n** 𖣘 Dari : **{_format.mentionuser(sender.first_name , sender.id)}\n** 𖣘 User ID:** `{chat.id}`"f"\n** 𖣘 Username**: {_format.mentionuser(sender.username , sender.id)}",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        BOTLOG_CHATID, event.message, silent=True, 
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.mentioned))
async def log_tagged_messages(event):
    if BOTLOG_CHATID == -100:
        return
    hmm = await event.get_chat()

    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (BOTLOG_CHATID == -100)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(event)
    resalt = f"<b>📥 #TAGS #MESSAGE</b>\n<b> 𖣘 Dari : </b>{_format.htmlmentionuser(full.first_name , full.id)}"
    if full is not None:
        resalt += f"\n<b> 𖣘 Grup : </b><code>{hmm.title}</code>"
    if messaget is not None:
        resalt += f"\n<b> 𖣘 Jenis Pesan : </b><code>{messaget}</code>"
    else:
       resalt += f"\nㅤㅤ╭━━━━━━𖣘━━━━━━╮\n<b> 𖣘 </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'>ㅤㅤㅤLihat Pesanㅤㅤㅤ</a>\nㅤㅤ╰━━━━━━𖣘━━━━━━╯"
    resalt += f"\n<b> 𖣘 Pesan : </b>{event.message.message}"
    if not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@bot.on(cok_cmd(outgoing=True, pattern=r"save(?: |$)(.*)"))
async def log(log_text):
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"**#LOG / Chat ID:** {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await log_text.client.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("**Apa yang harus saya simpan?**")
            return
        await log_text.edit("**Berhasil disimpan di Grup Log**")
    else:
        await log_text.edit("**Module ini membutuhkan LOGGER untuk diaktifkan!**")
    await asyncio.sleep(2)
    await log_text.delete()


@bot.on(cok_cmd(outgoing=True, pattern=r"log$"))
async def set_no_log_p_m(event):
    if BOTLOG_CHATID != -100:
        chat = await event.get_chat()
        if no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.disapprove(chat.id)
            await edit_delete(
                event, "**LOG Chat dari Grup ini Berhasil Diaktifkan**", 15
            )


@bot.on(cok_cmd(outgoing=True, pattern=r"nolog$"))
async def set_no_log_p_m(event):
    if BOTLOG_CHATID != -100:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.approve(chat.id)
            await edit_delete(
                event, "**LOG Chat dari Grup ini Berhasil Dimatikan**", 15
            )


@bot.on(cok_cmd(outgoing=True, pattern=r"pmlog (on|off)$"))
async def set_pmlog(event):
    if BOTLOG_CHATID == -100:
        return await edit_delete(
            event,
            "**Untuk Menggunakan Module ini, Anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**",
            30,
        )
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("**PM LOG Sudah Diaktifkan**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**PM LOG Berhasil Dimatikan**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("**PM LOG Berhasil Diaktifkan**")
    else:
        await event.edit("**PM LOG Sudah Dimatikan**")


@bot.on(cok_cmd(outgoing=True, pattern=r"gruplog (on|off)$"))
async def set_gruplog(event):
    if BOTLOG_CHATID == -100:
        return await edit_delete(
            event,
            "**Untuk Menggunakan Module ini, Anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**",
            30,
        )
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if h_type:
            await event.edit("**Group Log Sudah Diaktifkan**")
        else:
            addgvar("GRUPLOG", h_type)
            await event.edit("**Group Log Berhasil Dimatikan**")
    elif h_type:
        addgvar("GRUPLOG", h_type)
        await event.edit("**Group Log Berhasil Diaktifkan**")
    else:
        await event.edit("**Group Log Sudah Dimatikan**")


CMD_HELP.update(
    {
        "log": f"**Plugin : **`log`\
        \n\n  •  **Syntax :** `.save`\
        \n  •  **Function : **Untuk Menyimpan pesan yang ditandai ke grup pribadi.\
        \n\n  •  **Syntax :** `.log`\
        \n  •  **Function : **Untuk mengaktifkan Log Chat dari obrolan/grup itu.\
        \n\n  •  **Syntax :** `.nolog`\
        \n  •  **Function : **Untuk menonaktifkan Log Chat dari obrolan/grup itu.\
        \n\n  •  **Syntax :** `.pmlog on/off`\
        \n  •  **Function : **Untuk mengaktifkan atau menonaktifkan pencatatan pesan pribadi.\
        \n\n  •  **Syntax :** `.gruplog on/off`\
        \n  •  **Function : **Untuk mengaktifkan atau menonaktifkan tag grup, yang akan masuk ke grup pmlogger."
    }
)
