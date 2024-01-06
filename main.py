#!/usr/bin/env -S pipenv run python3 main.py

### First init ###

import csv
import discord
from discord.ext.commands import Bot

with open("token.raw") as ftoken:
    TOKEN = ftoken.read()

intents = discord.Intents.all()
bot = Bot('µ ', intents=intents)
with open("reactions.csv", 'w', encoding='utf-8') as table:
    table.write("")


### Stages and functions ###

async def SETUP_VARS():
    global CHANNEL_ROLES
    global CHANNEL_CHKIN
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
    global CAFEIN

    global PENDING

    CHANNEL_ROLES = bot.get_channel(1143999446070337559)
    CHANNEL_CHKIN = bot.get_channel(1145844239528366161)
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
    CAFEIN = SERVER.get_role(1150683966119084073)

    PENDING = False
    REM_PENDING: list[str] = []

    print("All VARS setup !")


def get_all_scopes() -> list[discord.Message]:
    return [MSG_CGU, MSG_CLASSE, MSG_ROLES]


async def fetch_reaction_db():
    reactions = []
    for scope in get_all_scopes():
        for reac in scope.reactions:
            reactions += [(str(reac), rmember.id) async for rmember in reac.users()]

    with open("reactions.csv", 'a', encoding="utf-8") as table:
        table.write(",".join(["reaction", "member_id"])+'\n')
        for c in reactions:
            c = [str(el) for el in c]
            table.write(",".join(c)+'\n')

    print("All reactions fetched !")


def get_REACT_DICT() -> dict[str, discord.Role]:
    return {
        "✅": CGU_ROOT,
        "<:L1:1144016256001904660>": INTERN,
        "<:L1_plus:1144014333446193275>": INTERN,
        "<:L2:1144016303762460672>": EXTERN,
        "<:L3:1144653440174276719>": EXTERN,
        "<:M1:1144653357001224273>": EXTERN,
        "<:M2:1144653378065027113>": EXTERN,
        "#️⃣": BLABLA,
        "📕": ETUDES,
        "🎮": JEUX_V,
        "☕": CAFEIN  # There's a character
    }


def message_id_to_scope(message_id: int) -> discord.Message:
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
        ETUDES: 2,
        CAFEIN: 2
    }
    return STAGES[role]


async def get_user_reactions(member: discord.Member, scope: discord.Message):  # scope added for perf
    reactions = []
    for reac in scope.reactions:  # [*REAC_CGU,*REAC_CLASSE,*REAC_ROLES]:
        reactions += [reac async for rmember in reac.users() if rmember == member]
    return reactions


async def add_role(member: discord.Member, pretend: discord.Reaction, scope: discord.Message):
    REACT_DICT = get_REACT_DICT()
    if which_stage(REACT_DICT[str(pretend)]) <= check_stages(member.roles):
        await member.add_roles(REACT_DICT[str(pretend)])
    else:
        await pretend.remove(member)

    # for reac in await get_user_reactions(member, scope):
    #    await member.add_roles(REACT_DICT[str(reac)])


async def remove_role(member: discord.Member, pemoji: discord.PartialEmoji):
    # First abtrary remove the role
    REACT_DICT = get_REACT_DICT()
    await member.remove_roles(REACT_DICT[str(pemoji)])
    with open("reactions.csv", 'a', encoding='utf-8') as table:
        table.write(f"del {pemoji},{member.id}\n")

    update = True
    reactions = []
    true_reac = []
    for scope in get_all_scopes():
        for reac in scope.reactions:
            true_reac += [reac]
    with open("reactions.csv", 'r', encoding='utf-8') as table:
        for line in table:
            if "reaction,member_id" in line:
                continue
            if "del " in line:
                reaction, member_id = line[4:].split(',')
                for reac in true_reac:
                    if str(reac) == reaction:
                        reactions.remove(reac)

            reaction, member_id = line.split(',')
            if int(member_id) == member.id:
                for reac in true_reac:
                    if str(reac) == reaction:
                        reactions += [reac]
    # for scope in get_all_scopes():
    #    for reac in scope.reactions:
    #        reactions += [reac async for rmember in reac.users() if rmember == member]
    print(f"User reactions : {reactions}")

    while reactions != [] and update:
        update = False
        for reaction in reactions:
            role = REACT_DICT[str(reaction)]
            if which_stage(role) > check_stages(member.roles):
                await reaction.remove(member)
                await member.remove_roles(role)
                update = True
                reactions.remove(reaction)
                with open("reactions.csv", 'a', encoding='utf-8') as table:
                    table.write(f"del {reaction},{member.id}\n")
    print("Removed role(s) !")


### events and commands ###

@bot.event
async def on_ready():
    print("----------------------")
    print("Logged In As")
    print("Username: %s" % bot.user.name)
    print("ID: %s" % bot.user.id)
    print("----------------------")
    await SETUP_VARS()
    await fetch_reaction_db()


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
    print(f"By: {payload.member}\nReact : {reaction}")

    await add_role(payload.member, reaction, scope)

    with open("reactions.csv", 'a', encoding='utf-8') as table:
        table.write(f"{reaction},{payload.member.id}\n")


@bot.event
async def on_raw_reaction_remove(payload):
    global PENDING
    if PENDING:
        return
    PENDING = True

    print("\nDiscard react")

    # HOTFIX for ctx.member
    payload.member = discord.utils.get(SERVER.members, id=payload.user_id)

    await remove_role(payload.member, payload.emoji)

    PENDING = False


@bot.event
async def on_member_join(member):
    await CHANNEL_CHKIN.send(
        f"Bonjour <@{member.id}> et bienvenue ! \n" \
        "Tu peut dès maintenant lire les règles <#1143999446070337559> \n" \
        "Acceptes les règles, puis choisit une classe, et enfin tes rôles. \n" \
        "Rejoins nous !"
    )


### EXEC ###
bot.run(TOKEN)
