# Credits: @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
# 𖣘Recode By @yangmutebabi

import asyncio

from userbot import pytgcalls
from youtubesearchpython import VideosSearch

from userbot import CMD_HELP, bot, call_py
from userbot.events import cok_cmd
from userbot.utils import edit_or_reply
from userbot.utils.queues.vqueues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
    pop_an_item,
)

from .cokvcgmusik import vcmention


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


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "youtube-dl",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
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


@bot.on(cok_cmd(outgoing=True, pattern=r"vplay(?:\s|$)([\s\S]*)"))
async def vplay(event):
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
        return await edit_or_reply(event, "**Silahkan Masukan Judul Video**")
    if replied and not replied.video and not replied.document:
        xnxx = await edit_or_reply(event, "`Searching...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit("**Tidak Menemukan Video untuk Keyword yang Diberikan**")
        else:
            songname = search[0]
            url = search[1]
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                await xnxx.edit(
                    f"💡 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n**🗿 Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    await xnxx.edit(
                        f"**🗿 Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                        link_preview=False,
                    )
                except Exception as ep:
                    await xnxx.edit(f"`{ep}`")

    elif replied:
        xnxx = await edit_or_reply(replied, "`Downloading`")
        dl = await replied.download_media()
        if len(event.text.split()) < 2:
            RESOLUSI = 720
        else:
            pq = event.text.split(maxsplit=1)[1]
            RESOLUSI = int(pq)
        if replied.video or replied.document:
            songname = "Telegram Video Player..."
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, "Video", RESOLUSI)
            await xnxx.edit(
                f"💡 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
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
            add_to_queue(chat_id, songname, dl, "Video", RESOLUSI)
            await xnxx.edit(
                f"🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                link_preview=False,
            )
    else:
        xnxx = await edit_or_reply(event, "`Searching...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit("**Tidak Menemukan Video untuk Keyword yang Diberikan**")
        else:
            songname = search[0]
            url = search[1]
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                await xnxx.edit(
                    f"🗿 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    await xnxx.edit(
                        f"🗿 **Judul:** [{songname}]({url})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                        link_preview=False,
                    )
                except Exception as ep:
                    await xnxx.edit(f"`{ep}`")


@bot.on(cok_cmd(outgoing=True, pattern="vend$"))
async def vend(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await edit_or_reply(event, "**Menghentikan Streaming**")
        except Exception as e:
            await edit_or_reply(event, f"**ERROR:** `{e}`")
    else:
        await edit_or_reply(event, "**Tidak Sedang Memutar Streaming**")


@bot.on(cok_cmd(outgoing=True, pattern="vskip$"))
async def vskip(event):
    chat_id = event.chat_id
    if len(event.text.split()) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await edit_or_reply(event, "**Tidak Sedang Memutar Streaming**")
        elif op == 1:
            await edit_or_reply(
                event, "`Antrian Kosong, Meninggalkan Obrolan Suara...`"
            )
        else:
            await edit_or_reply(
                event,
                f"**⏭ Melewati Video**\n**🎧 Sekarang Memutar** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**Menghapus Video Berikut Dari Antrian:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await skip_item(chat_id, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.edit(DELQUE)


@bot.on(cok_cmd(outgoing=True, pattern="vpause$"))
async def vpause(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dijeda**")
        except Exception as e:
            await edit_or_reply(event, f"**ERROR:** `{e}`")
    else:
        await edit_or_reply(event, "**Tidak Sedang Memutar Streaming**")


@bot.on(cok_cmd(outgoing=True, pattern="vresume$"))
async def vresume(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dilanjutkan**")
        except Exception as e:
            await edit_or_reply(event, f"**ERROR:** `{e}`")
    else:
        await edit_or_reply(event, "**Tidak Sedang Memutar Streaming**")


@bot.on(cok_cmd(outgoing=True, pattern="vplaylist$"))
async def vplaylist(event):
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
            PLAYLIST = f"**🎧 Sedang Memutar:**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**• Daftaf Putar:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                PLAYLIST = PLAYLIST + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
            await edit_or_reply(event, PLAYLIST, link_preview=False)
    else:
        await edit_or_reply(event, "**Tidak Sedang Memutar Streaming**")


@call_py.on_stream_end()
async def on_end_handler(_, u: Update):
    if isinstance(u, StreamAudioEnded):
        chat_id = u.chat_id
        print(chat_id)
        op = await skip_current_song(chat_id)
        if op == 1:
            await bot.send_message(
                chat_id, "`Antrian Kosong, Meninggalkan Obrolan Suara...`"
            )
        else:
            await bot.send_message(
                chat_id,
                f"**🎧 Sedang Memutar** \n[{op[0]}]({op[1]}) | `{op[2]}`",
                link_preview=False,
            )


CMD_HELP.update(
    {
        "cokvplay": "**Plugin : **`cokvplay`"
        "\n\n  •  **𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.vplay` <judul video/link yt>."
        "\n  •↳ : **Untuk Memutar video di voice chat group dengan akun kamu."
        "\n\n  •  **𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.vend`"
        "\n  •↳ : **Untuk Memberhentikan video yang di putar di voice chat group."
        "\n\n  •  **𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.vskip`"
        "\n  •↳ : **Untuk Melewati video yang sedang di putar di voice chat group."
        "\n\n  •  **𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.vpause`"
        "\n  •↳ : **Untuk Memberhentikan video yang sedang diputar."
        "\n\n  •  **𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.vresume`"
        "\n  •↳ : **Untuk Melanjutkan pemutaran video yang sedang diputar."
        "\n\n  •  **𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.vplaylist`"
        "\n  •↳ : **Untuk Menampilkan daftar putar video akan di putar."
        "\n\n  •  **NOTE :** bila video sudah masuk ke antrian tapi tidak ngeplay silahkan ketik `.vend` atau `.vskip`"
    }
)
