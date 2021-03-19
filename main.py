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

# Directory
current_dir = os.getcwd()

bot = commands.Bot(command_prefix = "$", case_insensitve=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="$help | Doing Pastpapers |"))
    print('Bot Online!')



@bot.command()
async def pp(ctx):
    await ctx.send("Welcome To The Past Paper Wizard :mage:", delete_after=30)
    user = ctx.message.author
    
    def check(message: discord.Message):
        return user == message.author

    await ctx.send("`What is your exam name? -> igcse, o level, a level`", delete_after=30)
    exmType = await bot.wait_for("message", check=check)
    exmType = exmType.content

    await ctx.send("`What is the name of the subject?`", delete_after=30)
    subject = await bot.wait_for("message", check=check)
    subject = subject.content

    await ctx.send("`What is the year of the paper?`", delete_after=30)
    year = await bot.wait_for("message", check=check)
    year = year.content

    await ctx.send("`What is The subject syllabus code? eg: 0620 (This is the syllabus code of IGCSE chemistry)`", delete_after=30)
    code = await bot.wait_for("message", check=check)
    code = code.content

    await ctx.send("`What is the type of paper you want? please type `qp` for Question Paper and `ms` for Marking Scheme`", delete_after=30)
    ptype = await bot.wait_for("message", check=check)
    ptype = ptype.content

    await ctx.send("`What is the exam session month? -> fm is F/M, mj is M/J, on is O/N `", delete_after=30)
    month = await bot.wait_for("message", check=check)
    month = month.content

    output = scrape(exmType, subject, code, year, ptype, month)
    pp = json.dumps(output, indent=4, sort_keys=True)
    sliced = pp.strip("}").strip("{")
    await ctx.send(f"```\n{sliced}```", delete_after=30)

    await ctx.send("Select the number of the paper to download :", delete_after=30)
    arr = await bot.wait_for('message', check=check)

    download(arr.content)
    await ctx.send(file=discord.File(f"{current_dir}/{fileName()}"))
    # Remove {current_dir} if you want to download to a custom directory
    # Don't forget to change it in the scraper.py file as well

    delete()


bot.run(os.getenv('DISCORD_TOKEN'))