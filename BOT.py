import discord
from discord.ext import commands 
import math
import sys, os, time, atexit
from signal import SIGTERM
import os
from dotenv import load_dotenv
load_dotenv()
token__ = os.getenv("token")
file_path = os.getenv("RTM-tools_config")

discord_prefix = "$"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=discord_prefix, intents = intents)

help_mess = {
    "arctan2": discord_prefix + "arctan2 [-r/-d] [-r/-d] <x> <y>",
}

def MissingRequiredArgument_process(message):
    data = message.split(" ")
    arg_num = len(data)
    print(arg_num)
    return data

@bot.event
async def on_ready():
    print("Bot in ready")

@bot.command()
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
        await ctx.send(help_mess["arctan2"] + "\n" + "\n".join(error_message))
    
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
    radians = (90 - float(degree))*math.pi / 180
    M = math.tan(radians)
    await ctx.send("1.00, " + '%.2f'%M)
    pass


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
