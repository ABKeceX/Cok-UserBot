""" Userbot module for other small commands. """
from userbot import CMD_HELP, ALIVE_NAME
from userbot.events import register


# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.helpmy$")
async def usit(e):
    await e.edit(
        f"**Hai {DEFAULTUSER} Kalau Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `.rhelp` Atau Bisa `.help` atau Minta Bantuan Ke:\n"
        "\n[『A̶̢͛̐͒͛̐̒̐̌ ̸̝͎̦́̔͠Β̸͌͂̑̆𖣘』](t.me/yangmutebabi)"
        "\n\n[SUPPORT CHANNEL ASUPAN](https://t.me/ExPsychopat)"
        "\n\n[CHANNEL ASUPAN 2](https://t.me/WXShoot)")


@register(outgoing=True, pattern="^.rvars$")
async def var(m):
    await m.edit(
        f"**Disini Daftar Vars Dari {DEFAULTUSER}:**\n"
        "\n[DAFTAR VARS](https://raw.githubusercontent.com/ramadhani892/RAM-UBOT/RAM-UBOT/varshelper.txt)")


CMD_HELP.update({
    "cokhelper":
    "`.helpmy`\
\nPenjelasan: Bantuan Untuk Cok-UserBot.\
\n`.rvars`\
\nPenjelasan: Untuk Melihat Beberapa Daftar Vars."
})
