#!/usr/bin/env python3


from asyncio import tasks
import discord
from discord.ext import commands, tasks
import requests
import json
import random as rd
from datetime import datetime
from bs4 import BeautifulSoup as bs

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents, description="$help")

data = json.load(open('config.json'))

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="$help"))

@bot.command(brief="get a wallpaper from a search")
async def wallpaper(ctx, *search):
    search = ' '.join(search)
    if search == None :
        rq = requests.get("https://wallpapersmug.com/")
    else :
        rq = requests.get(f"https://wallpapersmug.com/w/wallpaper?search={search}")
    soup = bs(rq.text, 'html.parser')
    res = soup.find_all("img")
    try : 
        first = res[1]['src']
        sec = first.replace("thumb", "download/1920x1080")
        await ctx.send(sec)
    except IndexError :
        await ctx.send("No result for that research")

@bot.command(brief="random wallpaper")
async def random(ctx):
    rq = requests.get("https://wallpapersmug.com/w/wallpaper/random")
    soup = bs(rq.text, 'html.parser')
    res = soup.find_all("img")
    first = res[1]['src']
    sec = first.replace("thumb", "download/1920x1080")
    await ctx.send(sec)


# @tasks.loop(minutes=1)
# async def send_random_cartoon():
#    pass

bot.run(data['TOKEN'])
