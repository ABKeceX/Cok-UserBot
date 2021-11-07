#
# 𖣘Recode By @yangmutebabi
#

import requests

from userbot import CMD_HELP, bot
from userbot.events import cok_cmd
from userbot.utils import tools


@bot.on(cok_cmd(outgoing=True, pattern="truth$"))
async def tede_truth(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/truth").json()
        results = resp["message"]
        await edit_or_reply(event, f"**#Truth**\n\n`{results}`")
    except Exception:
        await edit_or_reply(event, "**Ada yang salah Bruh...**")


@bot.on(cok_cmd(outgoing=True, pattern="dare$"))
async def tede_dare(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/dare").json()
        results = resp["message"]
        await edit_or_reply(event, f"**#Dare**\n\n`{results}`")
    except Exception:
        await edit_or_reply(event, "**Ada yang salah Bruh...**")



CMD_HELP.update(
    {
        "truthordare": "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `truthordare`"
        "\n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.truth`"
        "\n↳ : Untuk Tantangan."
        "\n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.dare`"
        "\n↳ : Untuk Kejujuran."})
