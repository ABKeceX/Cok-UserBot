# © Credits: @tofik_dn || https://github.com/tofikdn
# @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
# 𖣘Recode By @yangmutebabi

import asyncio

from userbot import pytgcalls
from telethon.tl import types
from telethon.utils import get_display_name
from youtubesearchpython import VideosSearch

from userbot import ALIVE_NAME
from userbot import CMD_HELP, bot, call_py
from userbot.events import cok_cmd
from userbot.utils import edit_delete, edit_or_reply
from userbot.utils.queues.queues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
    pop_an_item,
)


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format, link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        f"{format}",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    return 0, stderr.decode()


async def skip_item(chat_id, h):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    try:
        x = int(h)
        songname = chat_queue[x][0]
        chat_queue.pop(x)
        return songname
    except Exception as e:
        print(e)
        return 0


async def skip_current_song(chat_id):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    if len(chat_queue) == 1:
        await call_py.leave_group_call(chat_id)
        clear_queue(chat_id)
        return 1
    songname = chat_queue[1][0]
    url = chat_queue[1][1]
    link = chat_queue[1][2]
    type = chat_queue[1][3]
    RESOLUSI = chat_queue[1][4]
    if type == "Audio":
        await call_py.change_stream(
            chat_id,
            AudioPiped(
                url,
            ),
        )
    elif type == "Video":
        if RESOLUSI == 720:
            hm = HighQualityVideo()
        elif RESOLUSI == 480:
            hm = MediumQualityVideo()
        elif RESOLUSI == 360:
            hm = LowQualityVideo()
        await call_py.change_stream(
            chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
        )
    pop_an_item(chat_id)
    return [songname, link, type]


@bot.on(cok_cmd(outgoing=True, pattern=r"play(?:\s|$)([\s\S]*)"))
async def vc_play(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.audio
        and not replied.voice
        and not title
        or not replied
        and not title
    ):
        await edit_or_reply(event, "**Silahkan Masukan Judul Lagu**")
    elif replied and not replied.audio and not replied.voice or not replied:
        cok = await edit_or_reply(event, "`Mencari...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await cok.edit(
                "**Tidak Dapat Menemukan Lagu** Coba cari dengan Judul yang Lebih dikenal"
            )
        else:
            songname = search[0]
            url = search[1]
            format = "bestaudio"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await cok.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                await cok.edit(
                    f"🎶 **Lagu Ditambahkan Ke antrian »** `#{pos}`\n\n**🗿 Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            ytlink,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                    await cok.edit(
                        f"🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🏷️ **Status:** `Sedang Memutar`\n🎧 **Atas permintaan:** {from_user}",
                        link_preview=False,
                    )
                except Exception as ep:
                    await cok.edit(f"`{ep}`")

    else:
        cok = await edit_or_reply(replied, "`Downloading`")
        dl = await replied.download_media()
        link = replied.link
        if replied.audio:
            songname = "Telegram Music Player..."
        elif replied.voice:
            songname = "Voice Note"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            await cok.edit(
                f"🎶 **Lagu Ditambahkan Ke antrian »** `#{pos}`\n\n**🗿 Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
            )
        else:
            await call_py.join_group_call(
                chat_id,
                AudioPiped(
                    dl,
                ),
                stream_type=StreamType().pulse_stream,
            )
            add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            await cok.edit(
                f"🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🏷️ **Status:** `Sedang Memutar`\n🎧 **Atas permintaan:** {from_user}",
                link_preview=False,
            )


@bot.on(cok_cmd(outgoing=True, pattern=r"vplay(?:\s|$)([\s\S]*)"))
async def vc_vplay(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.video
        and not replied.document
        and not title
        or not replied
        and not title
    ):
        return await edit_or_reply(event, "**Silahkan Masukan Nama Video**")
    if replied and not replied.video and not replied.document:
        cok = await edit_or_reply(event, "`Mencari...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await cok.edit(
                "**Tidak Dapat Menemukan Video** Coba cari dengan Judul yang Lebih dikenal"
            )
        else:
            songname = search[0]
            url = search[1]
            format = "best[height<=?720][width<=?1280]"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await cok.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                await cok.edit(
                    f"📺 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n**🗿 Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    await cok.edit(
                        f"**🗿 Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🏷️ **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                        link_preview=False,
                    )
                except Exception as ep:
                    await cok.edit(f"`{ep}`")

    elif replied:
        cok = await edit_or_reply(replied, "`Downloading`")
        dl = await replied.download_media()
        link = replied.link
        if len(event.text.split()) < 2:
            RESOLUSI = 720
        else:
            pq = event.text.split(maxsplit=1)[1]
            RESOLUSI = int(pq)
        if replied.video or replied.document:
            songname = "Telegram Video Player..."
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
            await cok.edit(
                f"📺 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
            )
        else:
            if RESOLUSI == 360:
                hmmm = LowQualityVideo()
            elif RESOLUSI == 480:
                hmmm = MediumQualityVideo()
            elif RESOLUSI == 720:
                hmmm = HighQualityVideo()
            await call_py.join_group_call(
                chat_id,
                AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                stream_type=StreamType().pulse_stream,
            )
            add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
            await cok.edit(
                f"🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🏷️ **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                link_preview=False,
            )
    else:
        cok = await edit_or_reply(event, "`Mencari...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await cok.edit("**Tidak Menemukan Video yang Diberikan**")
        else:
            songname = search[0]
            url = search[1]
            format = "best[height<=?720][width<=?1280]"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await cok.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                await cok.edit(
                    f"📺 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    await cok.edit(
                        f"🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🏷️ **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                        link_preview=False,
                    )
                except Exception as ep:
                    await cok.edit(f"`{ep}`")


@bot.on(cok_cmd(outgoing=True, pattern="end$"))
async def vc_end(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await edit_or_reply(event, "**Menghentikan Streaming**")
        except Exception as e:
            await edit_delete(event, f"**ERROR:** `{e}`", 15)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**", 15)


@bot.on(cok_cmd(outgoing=True, pattern=r"skip(?:\s|$)([\s\S]*)"))
async def vc_skip(event):
    chat_id = event.chat_id
    if len(event.text.split()) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await edit_delete(event, "**Tidak Sedang Memutar Streaming**", 15)
        elif op == 1:
            await edit_delete(event, "antrian kosong, meninggalkan obrolan suara", 10)
        else:
            await edit_or_reply(
                event,
                f"**⏭ Melewati Lagu**\n**🎧 Sekarang Memutar** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**Menghapus Lagu Berikut Dari Antrian:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await skip_item(chat_id, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.edit(DELQUE)


@bot.on(cok_cmd(outgoing=True, pattern="pause$"))
async def vc_pause(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dijeda**")
        except Exception as e:
            await edit_delete(event, f"**ERROR:** `{e}`", 15)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**", 15)


@bot.on(cok_cmd(outgoing=True, pattern="resume$"))
async def vc_resume(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dilanjutkan**")
        except Exception as e:
            await edit_or_reply(event, f"**ERROR:** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**", 15)


@bot.on(cok_cmd(outgoing=True, pattern=r"volume(?: |$)(.*)"))
async def vc_volume(event):
    query = event.pattern_match.group(1)
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    chat_id = event.chat_id

    if not admin and not creator:
        return await edit_delete(event, f"**{ALIVE_NAME} Anda Bukan Admin 👮**", 15)

    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(query))
            await edit_or_reply(
                event, f"**Berhasil Mengubah Volume Menjadi** `{query}%`"
            )
        except Exception as e:
            await edit_delete(event, f"**ERROR:** `{e}`", 15)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**", 15)


@bot.on(cok_cmd(outgoing=True, pattern="playlist$"))
async def vc_playlist(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await edit_or_reply(
                event,
                f"**🎧 Sedang Memutar:**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview=False,
            )
        else:
            PLAYLIST = f"**🎧 Sedang Memutar:**\n**• [{chat_queue[0][0]}]({chat_queue[0][2]})** | `{chat_queue[0][3]}` \n\n**• Daftaf Putar:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                PLAYLIST = PLAYLIST + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
            await edit_or_reply(event, PLAYLIST, link_preview=False)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**", 15)


@call_py.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat_id = u.chat_id
    print(chat_id)
    await skip_current_song(chat_id)


@call_py.on_closed_voice_chat()
async def closedvc(_, chat_id: int):
    clear_queue(chat_id)


@call_py.on_left()
async def leftvc(_, chat_id: int):
    clear_queue(chat_id)


@call_py.on_kicked()
async def kickedvc(_, chat_id: int):
    clear_queue(chat_id)


CMD_HELP.update(
    {
        "cokvcgmusik": "**Plugin : **`cokvcgmusik`\
        \n\n  •  **Syntax :** `.play` <Judul Lagu/Link YT>\
        \n  •  **Function : **Untuk Memutar Lagu di voice chat group dengan akun kamu\
        \n\n  •  **Syntax :** `.vplay` <Judul Video/Link YT>\
        \n  •  **Function : **Untuk Memutar Video di voice chat group dengan akun kamu\
        \n\n  •  **Syntax :** `.end`\
        \n  •  **Function : **Untuk Memberhentikan video/lagu yang sedang putar di voice chat group\
        \n\n  •  **Syntax :** `.skip`\
        \n  •  **Function : **Untuk Melewati video/lagu yang sedang di putar\
        \n\n  •  **Syntax :** `.pause`\
        \n  •  **Function : **Untuk memberhentikan video/lagu yang sedang diputar\
        \n\n  •  **Syntax :** `.resume`\
        \n  •  **Function : **Untuk melanjutkan pemutaran video/lagu yang sedang diputar\
        \n\n  •  **Syntax :** `.volume` 1-200\
        \n  •  **Function : **Untuk mengubah volume (Membutuhkan Hak admin)\
        \n\n  •  **Syntax :** `.playlist`\
        \n  •  **Function : **Untuk menampilkan daftar putar Lagu/Video\
    "
    }
)
