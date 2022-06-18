#!/usr/bin/env python3
import discord
from discord import Embed, Intents, Client
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord_ui import Components, Button, UI, ButtonInteraction
import json
from discord_slash import SlashCommand, SlashContext


from tools import Photo, getDataFromId

# intents = discord.Intents.default()
# intents.members = True
# bot = commands.Bot(command_prefix='$', intents=intents)
# slash = SlashCommand(bot)

bot = Bot(command_prefix="$", self_bot=True, intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)
ui = UI(bot)

data = json.load(open('config.json'))

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)


photo_data = []


@slash.slash(name="wallpaper", description="Get wallpaper from search")
async def _wallpaper(ctx: SlashContext, search: str):
    photo = Photo()
    photo.setPhotoFromSearch(search)
    embed = photo.getEmbedPhotoFromPage(0)
    button1 = Button(label="Previous", emoji="⬅", custom_id="previous")
    button2 = Button(label="Next", emoji="➡", custom_id="next")
    tmp = await ui.components.send(ctx.channel, embed=embed, components=[button1, button2])
    photo_data.append({
        "message_id": tmp.id,
        "photo" : photo
    })
    await ctx.reply(content="Done", delete_after=1)

@slash.slash(name="random", description="Get random wallpaper")
async def _random(ctx: SlashContext):
    photo = Photo()
    photo.setPhotoRandom()
    embed = photo.getEmbedPhotoFromPage(0)
    await ctx.send(embed=embed)


@bot.listen("on_button")
async def on_button(btn: ButtonInteraction):
    custom_id = btn.data['custom_id']
    photo = getDataFromId(photo_data, btn.message.id)
    tmp_message = btn.message
    if custom_id == "previous":
        if (photo.page - 1) >= 0:
            photo.setPage(photo.getPage() - 1)
            embed = photo.getEmbedPhotoFromPage(photo.getPage())
            await tmp_message.edit(embed=embed)
        else:
            photo.setPage(len(photo.url) - 1)
            embed = photo.getEmbedPhotoFromPage(photo.getPage())
            await tmp_message.edit(embed=embed)
    elif custom_id == "next":
        if (photo.page + 1) < len(photo.url):
            photo.setPage(photo.getPage() + 1)
            embed = photo.getEmbedPhotoFromPage(photo.getPage())
            await tmp_message.edit(embed=embed)
        else:
            photo.setPage(0)
            embed = photo.getEmbedPhotoFromPage(photo.getPage())
            await tmp_message.edit(embed=embed)
    await btn.respond(ninja_mode=True)
    


bot.run(data['TOKEN'])
