#Abe(yangmutebabi)
#Ngapain Hayoo?
from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
    PeerChat,
)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Gambar Terlalu Kecil`"
PP_ERROR = "`Gagal Memproses Gambar`"
NO_ADMIN = "`Maaf Anda Bukan Admin:)`"
NO_PERM = "`Maaf Anda Tidak Mempunyai Izin!`"
NO_SQL = "`Berjalan Pada Mode Non-SQL`"

CHAT_PP_CHANGED = "`Berhasil Mengubah Profil Grup Cok`"
CHAT_PP_ERROR = (
    "`Ada Masalah Dengan Memperbarui Foto,`"
    "`Mungkin Karna Anda Bukan Admin,`"
    "`Atau Tidak Mempunyai Izin Cok.`"
)
INVALID_MEDIA = "`Media Tidak Valid`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@register(outgoing=True, pattern=r"^\.cmute(?: |$)(.*)")
async def spider(spdr):
    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await spdr.edit(NO_SQL)

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await spdr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(spdr)
    if not user:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        return await spdr.edit("`Tidak Bisa Membisukan Diri Sendiri..（>﹏<）`")

    if user.id == 1606695293:
        return await spdr.edit("`Gagal Mute Cok, Dia Adalah Pembuat Saya 😎`")

    # If everything goes well, do announcing and mute
    await spdr.edit(
        r"\\**#DMute_User**//"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Mampus Cok:** `DMute by {ALIVE_NAME}`"
    )
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit("`Error! Pengguna Sudah Dibisukan.`")
    try:
        await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

        # Announce that the function is done
        if reason:
            await spdr.edit(
                r"\\**#DMute_User**//"
                f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:** `{user.id}`\n"
                f"**Reason:** `{reason}`"
            )
        else:
            await spdr.edit(
                r"\\**#DMute_User**//"
                f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:** `{user.id}`\n"
                f"**Mampus Cok:** `DMute by {ALIVE_NAME}`"
            )

        # Announce to logging group
        if BOTLOG:
            await spdr.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {spdr.chat.title}(`{spdr.chat_id}`)",
            )
    except UserIdInvalidError:
        return await spdr.edit("`Terjadi Kesalahan Cokk!`")


@register(outgoing=True, pattern=r"^\.uncmute(?: |$)(.*)")
async def unmoot(unmot):
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await unmot.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await unmot.edit(NO_SQL)

    # If admin or creator, inform the user and start unmuting
    await unmot.edit("```Melakukan Unmute Cok...```")
    user = await get_user_from_event(unmot)
    user = user[0]
    if not user:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("**ERROR!** Pengguna Sudah Tidak Dibisukan Cok, Kiww.")
    try:
        await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
        await unmot.edit(
            "**Berhasil Melakukan Unmute Cok! User Sudah Tidak Lagi Dibisukan, Akakwkwkwk**"
        )
        await sleep(3)
        await unmot.delete()
    except UserIdInvalidError:
        return await unmot.edit("**Terjadi ERROR Cok!**")

    if BOTLOG:
        await unmot.client.send_message(
            BOTLOG_CHATID,
            "#UNMUTE\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {unmot.chat.title}(`{unmot.chat_id}`)\n"
            f" HATI2 DIA NGAMOKKKK COKK AKWKAKWK",
        )
