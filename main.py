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

    global CGU_ROOT
    global INTERN 
    global EXTERN
    global BLABLA
    global ETUDES
    global JEUX_V

    CHANNEL_ROLES = bot.get_channel(1143999446070337559)
    SERVER = bot.get_guild(1143931284595417140)
    
    MSG_CGU = await CHANNEL_ROLES.fetch_message(1143999517922963466)
    
    MSG_CLASSE = await CHANNEL_ROLES.fetch_message(1144010479145070673)
    
    MSG_ROLES = await CHANNEL_ROLES.fetch_message(1144014029875060897)

    CGU_ROOT = SERVER.get_role(1143994418559455312)
    INTERN = SERVER.get_role(1143936334986223789)
    EXTERN = SERVER.get_role(1143937761666158724)
    BLABLA = SERVER.get_role(1144017617938554970)
    ETUDES = SERVER.get_role(1144017476074602627)
    JEUX_V = SERVER.get_role(1144012929541357578)

    print("All VARS setup !")

def get_REACT_DICT() -> dict[str,discord.Role]:
    return {
        "✅":CGU_ROOT,
        "<:L1:1144016256001904660>":INTERN,
        "<:L1_plus:1144014333446193275>":INTERN,
        "<:L2:1144016303762460672>":EXTERN,
        "#️⃣":BLABLA,
        "📕":ETUDES,
        "🎮":JEUX_V
    }

def message_id_to_scope(message_id:int):
    match message_id:
        case 1143999517922963466:
            return MSG_CGU
        case 1144010479145070673:
            return MSG_CLASSE
        case 1144014029875060897:
            return MSG_ROLES
        case _:
            raise KeyError

def check_stages(roles: list[discord.Role]) -> int:
    ## Stage 1
    stage = 0
    if CGU_ROOT in roles:
        stage = 1
    else:
        return stage
    if INTERN in roles or EXTERN in roles:
        stage = 2
    else:
        return stage
    
    # ...

    return stage

def which_stage(role: discord.Role) -> int:
    STAGES = {
        CGU_ROOT: 0,
        INTERN: 1,
        EXTERN: 1,
        BLABLA: 2,
        JEUX_V: 2,
        ETUDES: 2
    }
    return STAGES[role]
    

async def get_user_reactions(member:discord.Member, scope: discord.Message): # scope added for perf
    reactions = []
    for reac in scope.reactions: #[*REAC_CGU,*REAC_CLASSE,*REAC_ROLES]:
        reactions += [reac async for rmember in reac.users() if rmember == member ]
    return reactions

async def add_role(member:discord.Member, pretend: discord.Reaction, scope:discord.Message):
    REACT_DICT = get_REACT_DICT()
    if which_stage(REACT_DICT[str(pretend)]) <= check_stages(member.roles):
        await member.add_roles(REACT_DICT[str(pretend)])
    else:
        await pretend.remove(member)

    #for reac in await get_user_reactions(member, scope):
    #    await member.add_roles(REACT_DICT[str(reac)])

def remove_role(user_id:int):
    pass

### events and commands ###

@bot.event
async def on_ready():
    print("----------------------")
    print("Logged In As")
    print("Username: %s"%bot.user.name)
    print("ID: %s"%bot.user.id)
    print("----------------------")
    await SETUP_VARS()

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)

@bot.command()
async def ping(ctx):
    """Ping pong"""
    await ctx.send("Pong!")

@bot.event
async def on_raw_reaction_add(payload):
    print("\nReceive react")
    scope = message_id_to_scope(payload.message_id)
    if not (reaction := discord.utils.get(scope.reactions, emoji=payload.emoji)):
        reaction = discord.utils.get(scope.reactions, emoji=str(payload.emoji))
    print(f"By: {member}\nReact : {reaction}")
    await add_role(payload.member, reaction, scope)

@bot.event
async def on_raw_reaction_remove(payload):
    print("\nDiscard react")
    scope = message_id_to_scope(payload.message_id)


### EXEC ###
bot.run(TOKEN)