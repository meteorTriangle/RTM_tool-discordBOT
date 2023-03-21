from discord.ext import commands 
import discord
import numpy
import math

bot = commands.Bot(command_prefix=">")

@bot.event
async def on_ready():
    print("Bot in ready")

@bot.command()
async def XTD(ctx, a, b):
    try:
        a_F = float(a)
        b_F = float(b)
    except:
        await ctx.send(f"輸入參數錯誤")
    print(a_F)
    print(b_F)
    M = b_F/a_F
    print(M)
    print(math.atan(M))
    deg = (math.atan(M) * 180) / math.pi
    await ctx.send('%.2f' % deg)

bot.run("MTA4NzU5ODY1MDIxMDkxMDI4OQ.GFjleq.p1oH0i-f6ZCnQriL2hlZCWGcHDeHTLLOE0Uv8M")

