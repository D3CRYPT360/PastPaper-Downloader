#!/usr/bin/env python3


"""
This is a discord bot which downloads
past papers on command and sends to 
the channel
saves time :)

inspired by https://github.com/Dharisd/pastpaper-bot/ <- Telegram bot
"""

# Imports related to discord
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Downloader
from downloader import Downloader

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
async def test(ctx):
    await ctx.send("15 - 5 = 10 marks in econ")

@bot.command()
async def pp(ctx):
    await ctx.send("Welcome To The Past Paper Wizard :mage:", delete_after=30)

    user = ctx.message.author

    def check(message: discord.Message):
        return user == message.author

    
    async def exam_Board():
        global exmBoard
        await ctx.send("`What is your exam board?\n[1] IGCSE\n[2] GCSE\n[3] A level`", delete_after=10)
        exmBoard = await bot.wait_for("message", check=check)
        try:
            if exmBoard.content == "1":
                exmBoard = "IGCSE"
            
            elif exmBoard.content == "2":
                exmBoard = "O Levels"

            elif exmBoard.content == "3":
                exmBoard = "A levels"

            else:
                await ctx.send("Invalid option chosen. Try again!")
                await exam_Board()
                
        except ValueError:
                await ctx.send("Invalid option chosen. Try again!")
                await exam_Board()

    await exam_Board()
        

    await ctx.send("`Enter the name of the subject (please enter the full form :3)`", delete_after=10)
    subject = await bot.wait_for("message", check=check)
    subject = subject.content

    async def SylCode():
        global sylcode
        await ctx.send("`What is The subject syllabus code? eg: 0620 (This is the syllabus code of IGCSE chemistry)`", delete_after=15)
        sylcode = await bot.wait_for("message", check=check)
        try:

            if len(sylcode.content) < 4 or len(sylcode.content) > 4:
                await ctx.send("Invalid syllabus code entered. Try again!")
                await SylCode()

            else:
                sylcode = sylcode.content

        except ValueError:
            await ctx.send("Invalid syllabus code entered. Try again!")
            await SylCode()

    await SylCode()

    async def Month():
        global month
        await ctx.send("`Choose the exam session\n[1] February / March\n[2] May / June\n[3] October November`", delete_after=15)
        month = await bot.wait_for("message", check=check)
        try:
            if month.content == "1":
                month = "m"

            elif month.content == "2":
                month = "s"
            
            elif month.content == "3":
                month = "w"
            else:
                await ctx.send("Invalid option chosen. Try again!")
                await Month()

        except ValueError:
            await ctx.send("Invalid data entered. Try again!")
            await Month()

    await Month()

    async def Year():
        global year
        await ctx.send("`Enter the year of the paper you want`", delete_after=10)
        year = await bot.wait_for("message", check=check)
        try:
            if len(year.content) < 4 or len(year.content) > 4 or year.content < "2000":
                await ctx.send("Invalid year entered. Try again!")
                await Year()

            else:
                year = year.content

        except ValueError:
            await ctx.send("Invalid year entered. Try again!")
            await Year()

    await Year()
                
    async def Ptype():
        global ptype
        await ctx.send("`Choose the paper type:\n[1] Marking Scheme\n[2] Question Paper\n[3] Insert`", delete_after=10)
        ptype = await bot.wait_for("message", check=check)
        if ptype.content.isdigit():

            if ptype.content == "1":
                ptype = "ms"
            
            elif ptype.content == "2":
                ptype = "qp"

            elif ptype.content == "3":
                ptype = "ir "
                
            else:
                await ctx.send("Invalid option chosen. Try again!")
                await Ptype()
        else:
            await ctx.send("Invalid data entered. Try again!")
            await Ptype()

    await Ptype()

    async def Pnum():
        global pnum
        await ctx.send("`What is the paper number eg: 42`", delete_after=15)
        pnum = await bot.wait_for("message", check=check)
        if pnum.content.isdigit():
            if len(pnum.content) > 2 or len(pnum.content) < 2:
                await ctx.send("Invalid data entered. Try again!")
                await Pnum()
            else:
                pnum = pnum.content
        else:
            await ctx.send("Invalid data entered. Try again!")
            await Pnum()

    await Pnum()


    downloder = Downloader(exmBoard, subject, sylcode, month, year, ptype, pnum)

    filename = downloder.pdfDown()
    await ctx.send(file=discord.File(f"{current_dir}/{filename}"))

bot.run(os.getenv('DISCORD_TOKEN'))