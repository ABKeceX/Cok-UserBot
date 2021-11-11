# Thanks Full To Team Ultroid
# Re by @yangmutebabi

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from userbot import ALIVE_NAME
from userbot import CMD_HELP, bot
from userbot.events import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, pattern=r"^\.startvc$")
async def start_voice(cok):
    chat = await cok.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await cok.edit(f"**{ALIVE_NAME} Anda Bukan Admin 👮**")
        return
    try:
        await cok.client(startvc(cok.chat_id))
        await cok.edit("`Voice Chat Started...`")
    except Exception as ex:
        await cok.edit(f"**ERROR:** `{ex}`")


@register(outgoing=True, pattern=r"^\.stopvc$")
async def stop_voice(cok):
    chat = await cok.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await cok.edit(f"**{ALIVE_NAME} Anda Bukan Admin 👮**")
        return
    try:
        await cok.client(stopvc(await get_call(cok)))
        await cok.edit("`Voice Chat Stopped...`")
    except Exception as ex:
        await cok.edit(f"**ERROR Brodyh..:** `{ex}`")


@register(outgoing=True, pattern=r"^\.vctitle(?: |$)(.*)")
async def change_title(edan):
    title = edan.pattern_match.group(1)
    chat = await edan.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await edan.edit("**Silahkan Masukkan Title Obrolan Suara Grup**")

    if not admin and not creator:
        await edan.edit(f"**{ALIVE_NAME} Anda Bukan Admin 👮**")
        return
    try:
        await edan.client(settitle(call=await get_call(edan), title=title.strip()))
        await edan.edit(f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await edan.edit(f"**ERROR Brodyh..:** `{ex}`")



@register(outgoing=True, pattern=r"^\.vcinvite")
async def _(cok):
    await cok.edit("`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in cok.client.iter_participants(cok.chat_id):
        if not x.bot:
            users.append(x.id)
    cokubot = list(user_list(users, 6))
    for p in cokubot:
        try:
            await cok.client(invitetovc(call=await get_call(cok), users=p))
            z += 6
        except BaseException:
            pass
    await cok.edit(f"`{z}` **Orang Berhasil diundang ke VCG**")



CMD_HELP.update(
    {
        "cokvcg": "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.startvc`\
         \n↳ : Memulai Obrolan Suara dalam Group.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.stopvc`\
         \n↳ : `Menghentikan Obrolan Suara Pada Group.`\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.vctitle`\
         \n↳ : `Mengubah Title Obrolan Suara Pada Group.`\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.vcinvite`\
         \n↳ : Invite semua member yang berada di group. (Kadang bisa kadang kaga)."
    }
)
