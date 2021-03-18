#!/usr/bin/env python
"""
This is a discord bot which downloads
past papers on command and sends to 
the channel
saves time :)

inspired by https://github.com/Dharisd/pastpaper-bot/ <- Telegram bot
"""

# Imports related to discord
import discord
from discord import message
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
# Imports for Scraping
from scraper import scrape, download, fileName, delete

# Token from .env file 
load_dotenv(".env")

bot = commands.Bot(command_prefix = "$", case_insensitve=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="$help | Doing Pastpapers |"))
    print('Bot Online!')



@bot.command()
async def pp(ctx):
    await ctx.send("Welcome To The Past Paper Wizard :mage:")
    user = ctx.message.author
    
    def check(message: discord.Message):
        return user == message.author

    await ctx.send("`What is your exam name? -> igcse, o level, a level`", delete_after=60.0)
    exmType = await bot.wait_for("message", check=check)
    exmType = exmType.content

    await ctx.send("`What is the name of the subject?`", delete_after=60.0)
    subject = await bot.wait_for("message", check=check)
    subject = subject.content

    await ctx.send("`What is the year of the paper?`", delete_after=60.0)
    year = await bot.wait_for("message", check=check)
    year = year.content

    # Will Remove this soon and be automated based on exmType cuz checking for code is a tedious task 
    await ctx.send("`What is The subject syllabus code? eg: 0620 (This is the syllabus code of IGCSE chemistry)`", delete_after=60.0)
    code = await bot.wait_for("message", check=check)
    code = code.content

    await ctx.send("`What is the type of paper you want? please type `qp` for Question Paper and `ms` for Marking Scheme`", delete_after=60.0)
    ptype = await bot.wait_for("message", check=check)
    ptype = ptype.content

    await ctx.send("`What is the exam session month? -> fm is F/M, mj is M/J, on is O/N `", delete_after=60.0)
    month = await bot.wait_for("message", check=check)
    month = month.content

    output = scrape(str(exmType), str(subject), str(code), str(year), str(ptype), str(month))
    pp = json.dumps(output, indent=4, sort_keys=True)
    sliced = pp.strip("}").strip("{")
    await ctx.send(f"```\n{sliced}```")

    await ctx.send("Select the number of the paper to download :", delete_after=60.0)
    arr = await bot.wait_for('message', check=check)
    download(arr.content)
    await ctx.send(file=discord.File(f"/home/d3crypt360/Desktop/Python/pastpaperdisc/pastdown/{fileName()}"))
    delete()

"""
@bot.command(aliases=['banner', 'aq', 'quote', 'aquote', 'agentq'])
async def agentquote(ctx):
    user = ctx.message.author
    def bar(message: discord.Message):
        return user == message.author
    agents = ["viper", "cypher", "omen", "yoru", "reyna", "raze", "breach", "brimstone", "sova", "sage", "killjoy", "phoenix", "skye", "jett"]
    await ctx.send("Which agent you want for your quote?")
    msg = await bot.wait_for('message', check=bar, timeout=15.0)
    bannerimg = msg.content.lower()
    if msg.content.lower() in agents:
        await ctx.send('What do you want '+bannerimg+ ' to say?')
        txte = await bot.wait_for('message', check=bar, timeout=45.0)
"""


bot.run(os.getenv('DISCORD_TOKEN'))