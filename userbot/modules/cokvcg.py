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

NO_ADMIN = "**{ALIVE_NAME} Anda Bukan Admin 👮**"


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, groups_only=True, pattern=r"^\.startvc$")
async def start_voice(cok):
    chat = await cok.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await cok.edit(NO_ADMIN)
    try:
        await cok.client(startvc(cok.chat_id))
        await cok.edit("`Memulai VCG/OS...`")
    except Exception as ex:
        await cok.edit(f"`{str(ex)}`")


@register(outgoing=True, groups_only=True, pattern=r"^\.stopvc$")
async def stop_voice(cok):
    chat = await cok.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await cok.edit(NO_ADMIN)
    try:
        await cok.client(stopvc(await get_call(cok)))
        await cok.edit("`Menghentikan VCG/OS, Lanjut Typing...`")
    except Exception as ex:
        await cok.edit(f"`{str(ex)}`")


@register(outgoing=True, groups_only=True, pattern=r"^\.vctitle$")
async def change_title(edan):
    title = edan.pattern_match.group(1)
    chat = await edan.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await edan.edit("**Silahkan Masukkan Title Obrolan Suara Grup**")

    if not admin and not creator:
        return await edan.edit(NO_ADMIN)
    new_rights = ChatAdminRights(invite_users=True)
    try:
        await edan.client(settitle(call=await get_call(edan), title=title.strip()))
        await edan.edit(f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await edan.edit(f"**ERROR Brodyh..:** `{ex}`")



@register(outgoing=True, groups_only=True, pattern=r"^\.vcinvite")
async def vc_invite(cok):
    await cok.edit("`Memulai Invite member group...`")
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


CMD_HELP.update(
    {
        "vcginvite": "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.vcinvite`\
         \n↳ : Invite semua member yang berada di group. (Kadang bisa kadang kaga)."
    }
)
