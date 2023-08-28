#!/usr/bin/env -S pipenv run python3 main.py

### First init ###

import discord
from discord.ext.commands import Bot

with open("token.raw") as ftoken:
    TOKEN=ftoken.read()


intents = discord.Intents.all()
bot = Bot('µ ',intents=intents)

### Stages and functions ###

class Stage1:
    """CGU aggrements"""
    pass

class Stage2:
    """Classe roles"""
    pass

class Stage3:
    """Channel roles"""
    pass

class User_pystatus:
    """backend User object"""
    pass

def update_react(user:User_pystatus):
    pass

def add_role(user:User_pystatus):
    pass

def remove_role(user:User_pystatus):
    pass

def update_status():
    pass

### events and commands ###

@bot.event
async def on_ready():
    print("----------------------")
    print("Logged In As")
    print("Username: %s"%bot.user.name)
    print("ID: %s"%bot.user.id)
    print("----------------------")

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)

@bot.command()
async def ping(ctx):
    """Ping pong"""
    await ctx.send("Pong!")

@bot.event
async def on_raw_reaction_add(payload):
    print("Receive react")
    pass

@bot.event
async def on_raw_reaction_remove(payload):
    print("Discard react")
    pass


### EXEC ###
bot.run(TOKEN)