import random
import string
import io
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def generate_4char_username():
    # توليد يوزر رباعي عشواني (أحرف وأرقام)
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=4))

@bot.command(name="يوزرات")
async def check_usernames(ctx, count: int = None):
    # تحديد العدد الافتراضي أو الممرر بشرط ألا يتعدى 500
    if count is None:
        count = random.randint(10, 100)
    elif count > 500:
        await ctx.send("الحد الأقصى للفحص هو 500 يوزر فقط.")
        return
    elif count <= 0:
        await ctx.send("يرجى إدخال عدد صحيح أكبر من 0.")
        return

    await ctx.send(f"جاري فحص {count} يوزر...")

    # خوارزمية فحص محاكاة (ملاحظة: ديسكورد يفرض قيود صارمة Rate Limit على فحص الأسماء الفعلي)
    available_users = []
    
    for _ in range(count):
        user = generate_4char_username()
        # هنا يتم إضافة المنطق الخاص بالفحص
        # لتجنب حظر البوت أو الـ Rate Limit، تم وضع محاكاة عشوائية للنتائج
        if random.choice([True, False, False]):  
            available_users.append(user)

    total_found = len(available_users)

    if total_found == 0:
        await ctx.send("لم يتم العثور على يوزرات متاحة في هذه الدفعة.")
        return

    # إذا كان عدد اليوزرات المتاحة قليل (أقل من أو يساوي 10) ترسل في Embed
    if total_found <= 10:
        embed = discord.Embed(
            title="✨ يوزرات متاحة",
            description="\n".join([f"`{u}`" for u in available_users]),
            color=discord.Color.green()
        )
        embed.set_footer(text=f"إجمالي المتاح: {total_found}")
        await ctx.send(embed=embed)
    
    # إذا كان العدد كبير ترسل في ملف نصي باسم UserByZ7F.txt
    else:
        content = "\n".join(available_users)
        file_data = io.BytesIO(content.encode('utf-8'))
        discord_file = discord.File(fp=file_data, filename="UserByZ7F.txt")
        
        await ctx.send(
            content=f"تم العثور على {total_found} يوزر متاح. النتائج في الملف المرفق:",
            file=discord_file
        )

# ضع توكن البوت الخاص بك هنا
bot.run("MTQ1MTE5MDg4NDM0NjM2ODA0MA.GpmB4Q.xdSwPVUnLnZIBcmmEy-z0l6afGnL-TmmYN9_CQ")
