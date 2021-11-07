# © Credits: @tofik_dn || https://github.com/tofikdn
# @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
# 𖣘Recode By @yangmutebabi

import os
from asyncio import QueueEmpty

from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from telethon.tl import types
from telethon.utils import get_display_name
from youtube_search import YoutubeSearch

from userbot import CMD_HELP, bot, call_py
from userbot.events import cok_cmd
from userbot.utils import download_lagu, edit_or_reply
from userbot.utils.converter import convert
from userbot.utils.queues import queues

LAGI_MUTER = False
NAMA_GC = ""


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


@bot.on(cok_cmd(outgoing=True, pattern=r"play(?:\s|$)([\s\S]*)"))
async def play_musik(event):
    global LAGI_MUTER, NAMA_GC
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    query = event.pattern_match.group(1)
    if not query:
        return await edit_or_reply(event, "**Masukan Judul Lagu Yang Bener Cok!**")
    if LAGI_MUTER and NAMA_GC != event.chat.title:
        return await edit_or_reply(event, f"**Sedang memutar lagu di** `{NAMA_GC}!`")
    xnxx = await edit_or_reply(event, "`Searching...`")
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://www.youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
    except Exception:
        return await xnxx.edit(
            "**Tidak Menemukan Lagu** Coba Play dengan judul yang lebih dikenal"
        )
    await xnxx.edit("`Processing...`")
    file = await convert(download_lagu(link))
    if LAGI_MUTER:
        position = await queues.put(chat_id, file=file)
        capt = (
            f"🏷️ **Lagu ditambahkan ke antrian »** `{position}`\n\n"
            f"🗿 **Judul:** [{title}]({link})\n"
            f"⏱ **Durasi:** `{duration}`\n"
            f"🎧 **Atas permintaan:** {from_user}"
        )
    else:
        LAGI_MUTER = True
        NAMA_GC = event.chat.title
        try:
            await call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
            )
        except Exception as e:
            LAGI_MUTER = False
            NAMA_GC = ""
            return await xnxx.edit(str(e))
        capt = (
            f"🗿 **Judul:** [{title}]({link})\n"
            f"⏱ **Durasi:** `{duration}`\n"
            f"🏷️ **Status:** `Sedang Memutar`\n"
            f"🎧 **Atas permintaan:** {from_user}"
        )

    await xnxx.delete()
    await bot.send_file(chat_id, thumbnail, caption=capt)


@bot.on(man_cmd(outgoing=True, pattern="pause$"))
async def pause_musik(event):
    chat_id = event.chat_id
    if not (LAGI_MUTER and NAMA_GC):
        return await edit_or_reply(event, "**Tidak ada lagu yang sedang diputar!**")
    if NAMA_GC != event.chat.title:
        return await edit_or_reply(event, "**Sedang tidak memutar lagu di grup ini!**")
    try:
        await call_py.pause_stream(chat_id)
    except Exception as e:
        return await edit_or_reply(event, str(e))
    await edit_or_reply(event, "**Paused**")


@bot.on(man_cmd(outgoing=True, pattern="resume$"))
async def resume_musik(event):
    chat_id = event.chat_id
    if not (LAGI_MUTER and NAMA_GC):
        return await edit_or_reply(event, "**Tidak ada lagu yang sedang dijeda!**")
    if NAMA_GC != event.chat.title:
        return await edit_or_reply(event, "**Sedang tidak memutar lagu di grup ini!**")
    try:
        await call_py.resume_stream(chat_id)
    except Exception as e:
        return await edit_or_reply(event, str(e))
    await edit_or_reply(event, "**Resumed**")


@bot.on(man_cmd(outgoing=True, pattern="skip$"))
async def skip_musik(event):
    global LAGI_MUTER, NAMA_GC
    chat_id = event.chat_id
    if not (LAGI_MUTER and NAMA_GC):
        await edit_or_reply(event, "**Tidak ada lagu yang sedang diputar!**")
    if NAMA_GC != event.chat.title:
        return await edit_or_reply(event, "**Sedang tidak memutar lagu di grup ini!**")
    queues.task_done(chat_id)
    if queues.is_empty(chat_id):
        LAGI_MUTER = False
        NAMA_GC = ""
        await call_py.leave_group_call(chat_id)
        return await edit_or_reply(event, "**Menyetop Lagu.**")
    await call_py.change_stream(
        chat_id,
        InputStream(
            InputAudioStream(
                queues.get(chat_id)["file"],
            ),
        ),
    )
    await edit_or_reply(event, "**Melewati lagu saat ini.**")


@bot.on(man_cmd(outgoing=True, pattern="end$"))
async def stop_musik(event):
    global LAGI_MUTER, NAMA_GC
    chat_id = event.chat_id
    if not (LAGI_MUTER and NAMA_GC):
        return await edit_or_reply(event, "**Tidak ada lagu yang sedang diputar!**")
    if NAMA_GC != event.chat.title:
        return await edit_or_reply(event, "**Sedang tidak memutar lagu di grup ini!**")
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    LAGI_MUTER = False
    NAMA_GC = ""
    await call_py.leave_group_call(chat_id)
    os.system("rm ./raw_files/*.raw")
    os.system("rm ./downloads/*.m4a")
    await edit_or_reply(event, "**Menyetop lagu**")


@call_py.on_closed_voice_chat()
async def on_closed_handler(_, chat_id: int):
    global LAGI_MUTER, NAMA_GC
    if LAGI_MUTER and NAMA_GC:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass
        LAGI_MUTER = False
        NAMA_GC = ""


@call_py.on_stream_end()
async def stream_end_handler(_, u: Update):
    global LAGI_MUTER, NAMA_GC
    queues.task_done(u.chat_id)
    if queues.is_empty(u.chat_id):
        LAGI_MUTER = False
        NAMA_GC = ""
        await call_py.leave_group_call(
            u.chat_id,
        )
    else:
        await call_py.change_stream(
            u.chat_id,
            InputStream(
                InputAudioStream(
                    queues.get(u.chat_id)["file"],
                ),
            ),
        )
    os.system("rm ./raw_files/*.raw")
    os.system("rm ./downloads/*.m4a")


CMD_HELP.update(
    {
        "cokvcgmusik": "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `cokvcgmusik`"
        "\n\𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `.play` <Judul Lagu/Link YT>"
        \n↳ : memutar music"
        \n\n**𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.end`"
        \n↳ : **stop lagu yang di putar di voice chat group"
        \n\n**𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.pause`"
        \n↳ : **stop lagu yang sedang diputar"
        \n\n**𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.resume`"
        \n↳ : **lanjutkan pemutaran lagu yang sedang diputar"
        \n\n  •  **NOTE :** Play Music hanya bisa di 1 Grup Chat saja, untuk memutar di GC lain ketik `.end` terlebih dahulu"
    }
)
