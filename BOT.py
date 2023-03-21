import discord
from discord.ext import commands 
import math
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents = intents)

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
    reply_str = ('%.2f' % deg) + u'\N{DEGREE SIGN}'
    await ctx.send(reply_str)

bot.run("MTA4NzU5ODY1MDIxMDkxMDI4OQ.GpcjSn.c2p3XMReBnp9O_Q6WSZYzUbhw-z9eO7CdqYX28")

