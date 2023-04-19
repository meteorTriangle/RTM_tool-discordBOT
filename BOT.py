import discord
from discord.ext import commands 
import math
import sys, os, time, atexit
from signal import SIGTERM
import os
from dotenv import load_dotenv
import json
import svgwrite
from svgwrite import image
import cairosvg
self_path = os.path.dirname(__file__) + "\\"
print(self_path)
load_dotenv(dotenv_path=(self_path + ".env"))
token__ = os.getenv("token")
docs_path = self_path + os.getenv("docs_path")
print(docs_path)
docs_file = open(docs_path + "docs.json", encoding="UTF-8")
docs = json.load(docs_file)
curve_data_path = self_path + os.getenv("curve_data_path")

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

@bot.command()
async def tan_v2(ctx, *args):
	arg_name = None
	error = []
	arg_ = {
		"-i": True,                         ###Force_INT
		"-n": 3,                            ###suggest_Size
		"-m": 100,                          ###Max_distance
		"-u": "degree",                     ###unit
		}
	for i in range(len(args)):
		if(args[i][0] == "-"):
			if(args[i] == "-d"):
				arg_["-i"] = False
			elif(args[i] == "-i"):
				arg_["-i"] = True
			elif(args[i] == "-n"):
				arg_name = "-n"
			elif(args[i] == "-m"):
				arg_name = "-m"
			elif(args[i] == "-u"):
				arg_name = "-u"
			else:
				error.append(f"'{args[i]}'不是可選的變數")
		else:
			if(arg_name == "-n"):
				try:
					size = int(args[i])
				except:
					error.append(f"'{args[i]}'不是整數")
				arg_["-n"] = size
				arg_name = None
			elif(arg_name == "-m"):
				try:
					dis = int(args[i])
				except:
					error.append(f"'{args[i]}'不是整數")
				arg_["-m"] = dis
				arg_name = None
			elif(arg_name == "-u"):
				if(args[i] == "degree"):
					arg_["-u"] = "degree"
				elif(args[i] == "radian"):
					arg_["-u"] = "radian"
				error.append(f"'{args[i]}'不是可用的描述")
				arg_name = None
			elif(arg_name == None):
				try:
					num = float(args[i]) 
				except:
					error.append(f"'{args[i]}'不是整數")
				if(arg_["-u"] == "degree"):
					radian = num/180 * math.pi
				else:
					radian = num
	slope = math.tan(radian)
	if(slope == float("inf") or slope == 0):
		error.append(u"角度不能是0\N{DEGREE SIGN}或90\N{DEGREE SIGN}的倍數")
	error_state = len(error) != 0
	if(error_state):
		trans_data = "\n".join(error)
		await ctx.send(trans_data)
	else:
		
		suggest_array_ = []
		distance_over = False
		multiple = 1
		while(not distance_over):
			if(arg_["-i"]):
				offset = multiple
			else:
				offset = multiple*0.5
			distance = offset*(1 / slope)
			suggest_format = {"offset": offset, "F_distance": distance}
			real_distance = math.sqrt( (offset**2) + (distance**2) )
			distance_over = real_distance >= arg_["-m"]
			if((not distance_over) or multiple == 1):
				suggest_array_.append(suggest_format)
			multiple += 1
		main_suggest_array = []
		idd = 0
		over = False
		while(idd < arg_["-n"] and not over):
			## get %
			distance_array_ = []
			distance_array_.clear()
			for sff in range(len(suggest_array_)):
				distance_array_.append(abs((suggest_array_[sff]["F_distance"] % 1) - 0.5))
			min_index = find_min(distance_array_)
			suggest_format = {"offset": offset, "F_distance": distance}
			suggest_format["offset"] = suggest_array_[min_index]["offset"]
			suggest_format["F_distance"] = suggest_array_[min_index]["F_distance"]
			main_suggest_array.append(suggest_format)
			del suggest_array_[min_index]
			if(len(suggest_array_) == 0):
				over = True
			idd += 1
		suggest_data = []
		for hd in range(len(main_suggest_array)):
			distance = round(main_suggest_array[hd]["F_distance"])
			offset = main_suggest_array[hd]["offset"]
			real_degree = 90 - math.atan(distance / offset) * 180 / math.pi
			real_distance = math.sqrt((distance**2) + (offset**2))
			suggest_data.append( f"每往前{distance}格，偏移{offset}格，距離: {'%.3f'%real_distance}，實際角度: {'%.3f'%real_degree} " +  u'\N{DEGREE SIGN}')
		trans_data = ""
		trans_data = trans_data + f"斜率: {slope} \n" + "\n".join(suggest_data)
		await ctx.send(trans_data)
					

		
def find_min(list_):
	min_index = 0
	for fd in range(len(list_)):
		if(list_[min_index] < list_[fd]):
			min_index = fd
	return min_index

@bot.command()
async def test_svg(ctx, x, y):
	data_path = curve_data_path + str(ctx.author.id) + "\\"
	if not os.path.exists(data_path):
		os.makedirs(data_path)
	print(data_path)
	rail_image = svgwrite.Drawing(data_path + "01.svg", size=("200px", "200px"))
	rail_image.add(rail_image.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(255,255,255)'))
	line_x = rail_image.line(start=(int(x), 0), end=(int(x), 200), stroke='green', stroke_width=1)
	line_y = rail_image.line(start=(0, int(y)), end=(200, int(y)), stroke='red', stroke_width=1)
	rail_image.add(line_x)
	rail_image.add(line_y)
	rail_image.save()
	xxml = rail_image.tostring()
	cairosvg.svg2png(bytestring=xxml,write_to=data_path + "01.png")
	imaage = discord.File(data_path + "01.png")
	print(ctx.author.id)
	await ctx.send(file=imaage)
	
	
@bot.group()
async def curve(ctx):
	data_path = curve_data_path + str(ctx.author.id) + "\\"
	t = None
	if not os.path.exists(data_path):
		os.makedirs(data_path)
	if ctx.invoked_subcommand is None:
		try:
			imaage = discord.File(data_path + "01.png")
		except:
			t = True
		if(t == True):
			await ctx.send("You're in fisrt using, cache not existing")
		if(t == None):
			await ctx.send(file=imaage)
	else:
		curve.params.update({"id": str(ctx.author.id)})


@curve.group()
async def rail_1(ctx, x, y, xd, yd):
	await ctx.send(curve.params["id"])

 


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
