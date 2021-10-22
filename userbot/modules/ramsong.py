# Ported By Vicky / @Vckyouuu From Ultroid
# Jangan Dihapuss!!!
# Thanks Ultroid
# Full Love From Vicky For All Lord
# kontol


import json
import os

import pybase64
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from youtubesearchpython import SearchVideos

from userbot.events import register
from userbot import CMD_HELP


@register(outgoing=True, pattern=r"^\.song (.*)")
async def _(event):
    event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Processing..`")
    elif reply.message:
        query = reply.message
        await event.edit("`Tunggu..! Saya menemukan lagu Anda..`")
    else:
        await event.edit("`Apa yang seharusnya saya temukan?`")
        return

    await getmusic(str(query))
    loa = glob.glob("*.mp3")[0]
    await event.edit("`Yeah.. Mengupload lagu Anda..`")
    c_time = time.time()
    with open(loa, "rb") as f:
        result = await upload_file(
            client=event.client,
            file=f,
            name=loa,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "[UPLOAD]", loa)
            ),
        )
    await event.client.send_file(
        event.chat_id,
        result,
        allow_cache=False,
    )
    await event.delete()
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3", shell=True)


CMD_HELP.update({"song": "**Modules:** __Song__\n\n**Perintah:** `.song <judul>`"
                 "\n**Penjelasan:** Mendownload Lagu"})
