from time import sleep
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern='^.sadboy(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(2)
    await typew.edit("`Pertama-tama kamu cantik`")
    sleep(2)
    await typew.edit("`Kedua kamu manis`")
    sleep(1)
    await typew.edit("`Dan yang terakhir adalah kamu bukan jodohku`")
# Create by myself @localheart


@register(outgoing=True, pattern='^.punten(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`\n┻┳|―-∩`"
                     "`\n┳┻|     ヽ`"
                     "`\n┻┳|    ● |`"
                     "`\n┳┻|▼) _ノ`"
                     "`\n┻┳|￣  )`"
                     "`\n┳ﾐ(￣ ／`"
                     "`\n┻┳T￣|`"
                     "\n**Permisi Aku mau nimbrung Kk..**")


@register(outgoing=True, pattern='^.abe(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("*Abe Ganteng☑️**")
    await typew.edit("**Abe Ganteng✅**")
    sleep(1)
    await typew.edit("**Ganteng Mak☑️**")
    await typew.edit("**Ganteng Maksimal✅**")
    sleep(2)
    await typew.edit("**Gak Pernah Depresi Karena Cewek☑️**")
    await typew.edit("**Alhamdulillah Saya Keren✅**")
    sleep(2)
    await typew.edit("**Solo Bukan Ngejomblo☑️**")
    await typew.edit("**Solo Bukan Ngejomblo, Cewek Sama Saja✅**")
    sleep(2)
    await typew.edit("**Suka Gabut Ngurus Bot😎☑️**")
    await typew.edit("**Suka Gabut Ngurus Bot😎✅**")
    sleep(2)
    await typew.edit("**Mau Bot? Tanyakan 『A̶̢͛̐͒͛̐̒̐̌ ̸̝͎̦́̔͠Β̸͌͂̑̆𖣘』☑️**")
    await typew.edit("**Mau Bot? Tanyakan 『A̶̢͛̐͒͛̐̒̐̌ ̸̝͎̦́̔͠Β̸͌͂̑̆𖣘』✅**")
    sleep(5)
    await typew.edit("**Butuh Bot Link? PC [Orang Ini](https://t.me/OcongVer2)**")
    await typew.edit("**Bot Link Buat CH dan GC ada PC [Orang Ini](https://t.me/OcongVer2)✅**")
    sleep(5)
    await typew.edit("**Yang Make Bot dari Abe, Makasih (Jangan Asal Digunakan)☑️**")
    await typew.edit("**Makasih Lopyu😉😘✅**")
    sleep(3)
    await typew.edit("**GEBLANKK!**")


@register(outgoing=True, pattern='^.lahk(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Lah lah, Lo tolol?`")
    sleep(1)
    await typew.edit("`Apa dongok?`")
    sleep(1)
    await typew.edit("`Gausah sok keras`")
    sleep(1)
    await typew.edit("`Gua ga ketrigger sama bocah kayak Lu!`")


@register(outgoing=True, pattern='^.wah(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wahh, War nya keren bang`")
    sleep(2)
    await typew.edit("`Tapi, Yang gua liat, kok Kaya lawakan`")
    sleep(2)
    await typew.edit("`Oh iya, Kan lo badut 🤡`")
    sleep(2)
    await typew.edit("`Kosa kata pas ngelawak, Jangan di pake war bang`")
    sleep(2)
    await typew.edit("`Kesannya lo ngasih kita hiburan.`")
    sleep(2)
    await typew.edit("`Kasian badut🤡, Ga di hargain pengunjung, Eh lampiaskan nya ke Tele, Wkwkwk`")
    sleep(3)
    await typew.edit("`Dah sana cabut, Makasih hiburannya, Udah bikin Gua tawa ngakak`")

@register(outgoing=True, pattern='^.gombal(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`**JAKA SAMBUNG BAWA GOLOK`")
    sleep(2)
    await typew.edit("`**Ailopyuu Goblokk🙈**`")


CMD_HELP.update({
    "CokUserBot":
    "`.CokBot`\
    \nUsage: menampilkan alive bot.\
    \n\n`.sadboy`\
    \nUsage: hiks\
    \n\n`.punten` ; `.Abe`\
    \nUsage: misi.\
    \n\n`.gombal`\
    \nUsage: Gatau ah akwkakw"
})
