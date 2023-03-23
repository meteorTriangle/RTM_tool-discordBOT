import discord
from discord.ext import commands 
import math
import sys, os, time, atexit
from signal import SIGTERM
import os
from dotenv import load_dotenv
load_dotenv()
token__ = os.getenv("token")

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
    M = b_F/a_F
    deg = (math.atan(M) * 180) / math.pi
    reply_str = ('%.2f' % deg) + u'\N{DEGREE SIGN}'
    await ctx.send(reply_str)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.close()

bot.run(token__)


