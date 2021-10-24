# This is a troll indeed ffs *facepalm*
# Ported from xtra-telegram by @heyworld
from telethon.events import ChatAction
import asyncio
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins
#from userbot.utils import admin_cmd
from userbot.events import register
from userbot import ALIVE_NAME, CMD_HELP, bot, DEVS

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.fgban(?: |$)(.*)")
async def gbun(event):
    if event.fwd_from:
        return
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = f"`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By` {DEFAULTUSER}\n"
    no_reason = "No Reason Given "
    await event.edit("**Memproses Gbanned Wkwkwk**")
    asyncio.sleep(3.5)
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.from_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.from_id
        # make meself invulnerable cuz why not xD
    user, reason = await get_user_from_event(event)
    if not user:
        return

    self_user = await event.client.get_me()

    if user.id == self_user.id:
        return await event.edit("**Tidak Bisa Membisukan Diri Sendiri..（>﹏<）**")

    if user.id in DEVS:
        return await event.edit("**Gagal Cok, Dia Adalah Pembuat Saya 😎**")
    
        else:
            jnl = ("`Warning!!`"
                   "[{}](tg://user?id={})"
                   f"` 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By` {DEFAULTUSER}\n\n"
                   "**Name: ** __{}__\n"
                   "**ID : ** `{}`\n"
                   ).format(firstname, idd, firstname, idd)
            if usname is None:
                jnl += "**Username: ** `Doesn't own a username!`\n"
            elif usname != "None":
                jnl += "**Username** : @{}\n".format(usname)
            if len(gbunVar) > 0:
                gbunm = "`{}`".format(gbunVar)
                gbunr = "**Reason: **" + gbunm
                jnl += gbunr
            else:
                jnl += no_reason
            await reply_message.reply(jnl)
    else:
        mention = (
            f"Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By {DEFAULTUSER} \nReason: {reason}. ")
        await event.reply(mention)
    await event.delete()

CMD_HELP.update({
    "fakegban": "`.fgban`\
    \nUsage: Type .fgban or Reply .fgban reason and see it yourself. "
})
