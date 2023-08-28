#!/usr/bin/env -S pipenv run python3 main.py

### First init ###

from typing import Any, Coroutine
import discord
from discord.ext.commands import Bot

with open("token.raw") as ftoken:
    TOKEN=ftoken.read()


intents = discord.Intents.all()
bot = Bot('µ ',intents=intents)

### Stages and functions ###

async def SETUP_VARS ():
    global CHANNEL_ROLES
    global SERVER
    
    global MSG_CGU
    global MSG_CLASSE
    global MSG_ROLES

    global REAC_CGU
    global REAC_CLASSE
    global REAC_ROLES

    global REACT_DICT

    CHANNEL_ROLES = bot.get_channel(1143999446070337559)
    SERVER = bot.get_guild(1143931284595417140)
    
    MSG_CGU = await CHANNEL_ROLES.fetch_message(1143999517922963466)
    REAC_CGU = MSG_CGU.reactions()
    
    MSG_CLASSE = await CHANNEL_ROLES.fetch_message(1144010479145070673)
    REAC_CLASSE = MSG_CLASSE.reactions()
    
    MSG_ROLES = await CHANNEL_ROLES.fetch_message(1144014029875060897)
    REAC_ROLES = MSG_ROLES.reactions()

    INTERN = SERVER.get_role(1143936334986223789)
    EXTERN = SERVER.get_role(1143937761666158724)
    REACT_DICT: dict[str,discord.Role] = {
        "✅":SERVER.get_role(1143994418559455312),
        "<:L1:1144016256001904660>":INTERN,
        "<:L1_plus:1144014333446193275>":INTERN,
        "<:L2:1144016303762460672>":EXTERN,
        "#️⃣":SERVER.get_role(1144017617938554970),
        "📕":SERVER.get_role(1144017476074602627),
        "🎮":SERVER.get_role(1144012929541357578)
    }

class User_pystatus (Common):
    self.user_id = user_id
    self.member = discord.utils.get(self.SERVER.members, id=user_id)
    self.reactions = [user async for user in self.reactions.users()] #if user == user_id]
    print(self.reactions)

def update_react(user:User_pystatus):
    pass

def add_role(user:User_pystatus, pretend: discord.Reaction):
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
    SETUP_VARS()

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