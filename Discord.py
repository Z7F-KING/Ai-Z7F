import discord
import random
import string
import asyncio
import io
import aiohttp
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# كل شي مسموح بدسكورد
CHARS_FULL = string.ascii_lowercase + string.digits + "_."

def gen_4_random():
    # نولد يوزر عشوائي بس يطبق قوانين دسكورد حرفيا
    while True:
        s = ''.join(random.choices(CHARS_FULL, k=4))

        # 1- مايبدأ ولا ينتهي بنقطة او شرطة
        if s[0] in "_." or s[-1] in "_.":
            continue
        # 2- ممنوع نقطتين ورا بعض
        if ".." in s:
            continue
        # 3- ممنوع رمز جنب رمز زي _.._ __
        has_bad_combo = False
        for i in range(len(s)-1):
            if s[i] in "_." and s[i+1] in "_.":
                has_bad_combo = True
                break
        if has_bad_combo:
            continue
        # 4- لازم فيه حرف واحد على الاقل عشان دسكورد يقبله
        if not any(c in string.ascii_lowercase for c in s):
            continue

        return s

async def check_discord(session, username):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
    try:
        async with session.post(url, json={"username": username}) as r:
            if r.status == 429:
                data = await r.json()
                await asyncio.sleep(float(data.get("retry_after", 2)))
                return await check_discord(session, username)
            if r.status == 200:
                data = await r.json()
                return not data.get("taken", True) # taken=False = متاح
            return False
    except:
        return False

@bot.event
async def on_ready():
    print(f"جاهز - {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.content.startswith("يوزرات"): return

    parts = message.content.split()
    count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else random.randint(50, 200)
    if count > 500: count = 500

    wait_msg = await message.reply(f"⏳ قاعد افحص {count} يوزر دسكورد رباعي عشوائي...")

    usernames = set()
    while len(usernames) < count:
        usernames.add(gen_4_random())
    usernames = list(usernames)

    available = []
    sem = asyncio.Semaphore(3)

    async with aiohttp.ClientSession() as session:
        async def one(u):
            async with sem:
                if await check_discord(session, u):
                    available.append(u)
                await asyncio.sleep(0.8)

        await asyncio.gather(*[one(u) for u in usernames])

    if not available:
        embed = discord.Embed(title="UserByZ7F", description=f"فحصت {count} وكلها ماخوذة 💀\nالرباعي صار مستحيل", color=0xED4245)
        await wait_msg.edit(content="", embed=embed)
        return

    if len(available) <= 15:
        embed = discord.Embed(title=f"لقيت {len(available)} متاح ✅", description="\n".join([f"`{u}`" for u in available]), color=0x57F287)
        embed.set_footer(text=f"فحصنا {count} | UserByZ7F")
        await wait_msg.edit(content="", embed=embed)
    else:
        file = discord.File(io.BytesIO("\n".join(available).encode()), filename="UserByZ7F.txt")
        embed = discord.Embed(title=f"لقيت {len(available)} متاح 🔥", description="حطيتهم لك بملف", color=0x57F287)
        await wait_msg.edit(content="", embed=embed)
        await message.channel.send(file=file)

bot.run("MTQ1MTE5MDg4NDM0NjM2ODA0MA.GpmB4Q.xdSwPVUnLnZIBcmmEy-z0l6afGnL-TmmYN9_CQ")
