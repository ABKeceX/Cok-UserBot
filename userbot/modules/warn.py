# credit catuserbot
# 𖣘Recode By @yangmutebabi
#Masih Bug, belum di fix ( ~ < )

from userbot import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import format
from userbot.utils import tools
from userbot.modules.sql_helper import no_log_pms_sql
from userbot.utils.logger import logging
from userbot.modules.sql_helper import warns_sql as sql
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatAdminRights,
)
# =================== CONSTANT ===================
NO_ADMIN = "`Maaf Anda Bukan Admin:)`"
NO_PERM = "`Maaf Anda Tidak Mempunyai Izin!`"
NO_SQL = "`Berjalan Pada Mode Non-SQL`"

# ================================================



@register(outgoing=True, pattern="^.warn(?: |$)(.*)")
async def _(event):
    reply_message = await event.get_reply_message()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await event.edit(NO_ADMIN)

    warn_reason = event.pattern_match.group(1)

    if not warn_reason:
        warn_reason = "No reason"

    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.sender_id, event.chat_id, warn_reason
    )
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            resalt = f"{} warnings, [User](tg://user?id={}) Has to be KICKED!".format(
                limit, reply_message.sender_id
            )
        else:
            logger.info("TODO: ban user")
            resalt += f"{} warnings, [User](tg://user?id={}) Has to be BANNED!".format(
                limit, reply_message.sender_id
            )
    else:
        resalt += f"[User](tg://user?id={}) has {}/{} warnings... Tunggu Sebentar!".format(
            reply_message.sender_id, num_warns, limit
        )
        if warn_reason:
            resalt += f"\nReason warn terakhir:\n{}".format(html.escape(warn_reason))
    await edit_or_reply(event, reply)


@register(outgoing=True, pattern="^.warns(?: |$)(.*)")
async def _(event):
    "Untuk mendapatkan warn list"
    reply_message = await event.get_reply_message()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await event.edit(NO_ADMIN)

    if not reply_message:
        return await event.edit("__Reply to user to get his warns.__")

    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if not result or result[0] == 0:
        return await event.edit("Pengguna Belum Pernah di warn Tod!!")

    num_warns, reasons = result
    limit, soft_warn = sql.get_warn_setting(event.chat_id)

    if not reasons:
        return await event.edit("Pengguna ini memiliki {} / {} Warning, tapi tidak ada alasan atas warn nya.".format(
                num_warns, limit
            ),
        )

    text = "Pengguna ini memiliki {}/{} Warnings, Karena Alasan Berikut:".format(
        num_warns, limit
    )
    text += "\r\n"
    text += reasons
    await event.edit(text)



@register(outgoing=True, pattern="^.rmwarns(?: |$)(.*)")
async def _(event):
    reply_message = await event.get_reply_message()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await event.edit(NO_ADMIN)

    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await event.edit("__Warnings telah di Restart, Kiww__")


CMD_HELP.update(
    {
        "warn": f"**Plugin : **`warn`\
        \n\n  •  **Syntax :** `.warn`\
        \n  •  **Function : **Untuk Warnings Pengguna dari grup.\
        \n\n  •  **Syntax :** `.warns`\
        \n  •  **Function : **Untuk Melihat daftar Warn Pengguna di grup.\
        \n\n  •  **Syntax :** `.rmwarns`\
        \n  •  **Function : **Untuk Menghapus Warns dari grup."})
