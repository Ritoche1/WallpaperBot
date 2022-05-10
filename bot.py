#!/usr/bin/env python3


from asyncio import tasks
from dataclasses import replace
import discord
from discord import Embed, Intents, Client
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import requests
import json
import random as rd
from datetime import datetime
from bs4 import BeautifulSoup as bs
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents, description="$help")
# slash = SlashCommand(bot)

# bot = Bot(command_prefix="$", self_bot=True, intents=Intents.default())
# slash = SlashCommand(bot, sync_commands=True)

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
        i = rd.randint(0, len(res)-2)
        first = res[i+1]['src']
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


# @slash.slash(name="test",description="test", guild_ids=[688900872239054888])
# async def _test(ctx: SlashContext):
#     await ctx.send("hello")


# @slash.slash(name="wallpaper", description="get a wallpaper with your search", guild_ids=[688900872239054888, 961541109736177674])
# async def wallpaper(ctx: SlashContext, wanted):
#     key = data['API_KEY_PIXABAY'] 
#     print(wanted)
#     search = wanted.replace(' ', '+')
#     print(search)
#     if search == None :
#         rq = requests.get("https://pixabay.com/api/?key="+key+"&image_type=photo&safe_search=true")
#     else :
#         rq = requests.get(f"https://pixabay.com/api/?key="+key+"&image_type=photo&safe_search=true&q={search}")
#     json = rq.json()
#     try :
#         i = rd.randint(0, len(json['hits'])-1)
#         first = json['hits'][i]['largeImageURL']
#         await ctx.send(first)
#     except IndexError :
#         search = ' '.join(wanted)
#         rq = requests.get(f"https://wallpapersmug.com/w/wallpaper?search={search}")
#         soup = bs(rq.text, 'html.parser')
#         res = soup.find_all("img")
#         try : 
#             first = res[1]['src']
#             sec = first.replace("thumb", "download/1920x1080")
#             await ctx.send(sec)
#         except IndexError :
#             await ctx.send("No result for that research")

# @tasks.loop(minutes=1)
# async def send_random_cartoon():
#    pass

bot.run(data['TOKEN'])
