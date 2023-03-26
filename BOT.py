import discord
from discord.ext import commands 
import math
import sys, os, time, atexit
from signal import SIGTERM
import os
from dotenv import load_dotenv
import json
load_dotenv(dotenv_path=".env")
token__ = os.getenv("token")
docs_file = open("docs/docs.json", encoding="UTF-8")
docs = json.load(docs_file)

discord_prefix = "$"
help_mess = {
    "arctan2": discord_prefix + "arctan2 [-r/-d/-r -d] <x> <y>",
    "tan": discord_prefix + "tan <degree>"
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=discord_prefix, intents = intents, help = "\n".join(help_mess))



def MissingRequiredArgument_process(message):
    data = message.split(" ")
    arg_num = len(data)
    print(arg_num)
    return data

@bot.event
async def on_ready():
    print("Bot in ready")

@bot.command()
async def description(ctx, command_):
    help_ = docs["arctan2"]["help"]
    desc = "\n".join(f"{name} {value}"for name, value in docs[command_]["description"].items())
    await ctx.send(help_ + "\n" + desc)

@bot.command(help = docs["arctan2"]["help"])
async def arctan2(ctx, *args):
    error_state = False
    error_message = []
    use = None
    i = int(0)
    arg = list(args)
    isoption = True
    while isoption is True:
        isoption = arg[i][0] == "-"
        print(arg[i][0])
        if(isoption == True):
            if(use == None):
                if(arg[i] == "-r"):
                    use = "Radians"
                if(arg[i] == "-d"):
                    use = "Degrees"
            if(use == "Radians"):
                if(arg[i] == "-r"):
                    use = "Radians"
                if(arg[i] == "-d"):
                    use = "Both"
            if(use == "Degrees"):
                if(arg[i] == "-r"):
                    use = "Both"
                if(arg[i] == "-d"):
                    use = "Degrees"
            del arg[0]
    if use==None:
        use = "Degrees"
    
    ctx.a_F = 1
    ctx.b_F = 1
    argu_error = []
    try:
        ctx.a_F = float(arg[0])
    except:
        argu_error.append("<x>")

    try:
        ctx.b_F = float(arg[1])
    except:
        argu_error.append("<y>")
    if(len(arg) > 2):
        error_message.append("多餘的參數")
        error_state = True
    
    elif(len(arg) < 2):
        err_miss = []
        if(len(arg) == 0):
            err_miss.append("<x>")
        if(len(arg) <= 1):
            err_miss.append("<y>")
        error_message.append("缺少參數" + ", ".join(err_miss))
        error_state = True
    elif(len(argu_error) != 0):
        error_message.append("輸入參數" + ",".join(argu_error) + "不是數字")
        error_state = True
    if(len(error_message) != 0):
        await ctx.send(docs["arctan2"]["help"] + "\n" + "\n".join(error_message))
    
    M = ctx.b_F/ctx.a_F
    rad = math.atan(M)
    deg = (rad * 180) / math.pi
    reply_str = ""
    if (use == "Degrees"):
        reply_str = "degree: " + ('%.3f' % deg) + u'\N{DEGREE SIGN}'
    elif(use == "Radians"):
        reply_str = "Radians: " + ('%.5f' % rad) + ' rad'
    else:
        reply_str = "degree: " + ('%.3f' % deg) + u'\N{DEGREE SIGN}' + "     Radians: " + ('%.4f' % rad) + ' rad'
    print(use)
    print(arg)
    if(not(error_state)):
        await ctx.send(reply_str)

@bot.command()
async def tan(ctx, degree):
    error_state = False
    error_message = []
    deg = 1
    try:
        deg = float(degree)
    except:
        error_message.append("參數<degree>不是數字")
        error_state = True
    if(error_state == False):
        if(deg > 90 or deg < 0):
            error_message.append(u"參數<degree>超出範圍，範圍必須在0~90\N{DEGREE SIGN}之間")
            error_state = True
    radians = (90 - deg)*math.pi / 180
    M = math.tan(radians)
    x = []
    x_Q = []
    for y in range(100):
        if(M*(y+1)>100):
            pass
        else:
            x.append(M*(y+1))
            x_Q.append(abs(((M*(y+1)) % 1) - 0.5))
    min_index = 0
    for i in range(len(x_Q)):
        if(x_Q[i]<x_Q[min_index]):
            min_index = i
    trans_data = []
    trans_data.append("斜率: " + '%.3f'%M)
    sugess_M = round(x[min_index])
    real_deg = math.atan((min_index+1)/sugess_M) * 180 / math.pi
    error_data = help_mess["tan"] + "\n"  + "\n".join(error_message)
    trans_data.append(f"推薦蓋法: 每往前{sugess_M}格，偏移{min_index+1}格，角度{'%.2f'%real_deg}" + u'\N{DEGREE SIGN}' )
    if(error_state):
        await ctx.send(error_data)
    else:
        await ctx.send("\n".join(trans_data))
    pass
"""
@bot.command()
async def help(ctx, command_ = None, page = None):
    trans_data = "\n".join(help_mess)
    await ctx.send(trans_data)
"""

"""
@bot.event
async def on_command_error(ctx, error):
    print(bot.get_command('command name'))
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        print(error)
        error_command = str(error).split("\"")[1]
        await ctx.send("'" + error_command + "'是不支援的命令")
    if isinstance(error, commands.MissingRequiredArgument):
        mesg = ctx.message
        print(mesg.content)
        transdata = str(mesg.content)
        err = MissingRequiredArgument_process(transdata)
        print(err)
        await ctx.send("缺少參數")
##discord.message.Message.content
"""
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.close()

bot.run(token__)
