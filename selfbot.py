# -*- coding: utf-8 -*-

import os
import colorama
import discord
import humanize
import jstyleson
import time
import random

from string import ascii_letters as letters
import requests as req
from discord.ext import commands

# Constants
DISCORD_LIMIT = 2000
MAIN_CLR =  colorama.Fore.LIGHTMAGENTA_EX
RESET = colorama.Style.RESET_ALL
CLS = lambda: os.system("cls") if os.name == "nt" else "clear"

def get_mention(id):
    return f"<@!{id}>"

def replace_mention(string, id, name):
    return string.replace(get_mention(id), f"@{name}")

# Format UTC time with humanize
def format_time(time):
    return humanize.naturaltime(time)

if not os.path.exists("mentions.txt"):
    with open("mentions.txt", "w") as f:
        f.write("")

if not os.path.exists("./config.jsonc"):
    with open("./config.jsonc", "w") as f:
        f.write("""{
            "token": "",
            "prefix": "s.",
            "selfbot": true,
            "delete_cmd": false,
            "delete_cmd_output_after": null,
            "spam_chars": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "autoupdate": false,
            "write_mentions": false
        }""")

with open("config.jsonc", "r") as f:
    config = jstyleson.loads(f.read())

__TOKEN__ = config["token"]
__PREFIX__ = config["prefix"]
__SELFBOT__ = config["selfbot"]
__DELETE_CMD__ = config["delete_cmd"] # Deletes the command: for example, if you want to delete the command "?ping"
__DELETE_CMD_OUTPUT_AFTER__ = config["delete_cmd_output_after"] # None = doesnt delete the output
__SPAM_CHARS__ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
__AUTOUPDATE__ = config["autoupdate"]

WRITE_MENTIONS = config["write_mentions"] # If True, all mentions will be saved to mentions.txt

if __AUTOUPDATE__:
    link = "https://raw.githubusercontent.com/HACKERqq420/self/main/selfbot.py?token=GHSAT0AAAAAABRV3PT43C27XG36ST5WJQP6YQ7RQCQ"
    body = req.get(link).text
    with open(__file__, "w") as f:
        code = f.read()
    if code != body:
        with open(__file__, "w") as f:
            f.write(body)
        print(f"Updated {__file__}")
        print(f"Run {__file__} again to use the new version")
        time.sleep(3)
        exit()

# Colors
colorama.init()
red = colorama.Fore.RED
green = colorama.Fore.GREEN
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

bot = commands.Bot(command_prefix=__PREFIX__, self_bot=__SELFBOT__, case_insensitive=True)

# On Online

@bot.event
async def on_ready():
    CLS()
    print(f"{MAIN_CLR}Username {RESET} >>> {str(bot.user)}")
    print(f"{MAIN_CLR}Friends  {RESET} >>> {str(len(bot.user.friends))}")
    print(f"{MAIN_CLR}Blocked  {RESET} >>> {str(len(bot.user.blocked))}")
    print(f"{MAIN_CLR}Servers  {RESET} >>> {str(len(bot.guilds))}")

@bot.event
async def on_message(message):
    if not message.author.id == bot.user.id: return

    if f"<@!{bot.user.id}>" in message.content and not message.author.id == bot.user.id:
        print(f"{blue}[PING]{RESET} ~ " + f"{str(message.author)} >>> {replace_mention(message.content, bot.user.id, bot.user.name)}")
        with open("mentions.txt", "a") as f:
            f.write(f"\n{str(message.author)} >>> {replace_mention(message.content, bot.user.id, bot.user.name)}")

    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    print(f"{green}[COMMAND]{RESET} ~ " + f"{str(ctx.author)} >>> {replace_mention(ctx.message.content, bot.user.id, bot.user.name)}")
    if __DELETE_CMD__: await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{red}Command not found > {ctx.message.content}{RESET}")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"{red}Missing argument > {error}{RESET}")
    elif isinstance(error, commands.MissingPermissions):
        print(f"{red}Missing permissions > {error}{RESET}")
    elif isinstance(error, commands.CommandOnCooldown):
        print(f"{red}Cooldown > {error}{RESET}")
    elif isinstance(error, commands.CheckFailure): 
        print(f"{red}Check failure > {error}{RESET}")
    elif isinstance(error, commands.CommandInvokeError):
        print(f"{red}Command invoke error > {error}{RESET}")
    elif isinstance(error, commands.CommandError):
        print(f"{red}Command error{RESET}")
    elif isinstance(error, commands.BadArgument):
        print(f"{red}Bad argument > {error}{RESET}")
    elif isinstance(error, commands.BotMissingPermissions):
        print(f"{red}Bot missing permissions > {error}{RESET}")
    elif isinstance(error, commands.MissingPermissions):
        print(f"{red}Missing permissions > {error}{RESET}")
    elif isinstance(error, commands.NoPrivateMessage):
        print(f"{red}No private message > {error}{RESET}")
    else:
        print(f"{red}Unknown error in {str(ctx.message.channel)}: {error}{RESET}")
            
# Commands

# Ping command: check ping
@bot.command("ping", help="Tells you bot latency")
async def _ping(ctx):
    await ctx.send(f"`{round(bot.latency * 1000)}ms`", delete_after=__DELETE_CMD_OUTPUT_AFTER__)

# Help command: show help
# @bot.command("help", help="Shows this command", alias=["?", "h"])
# async def _help(ctx):
#     txt = ""
#     longest = 0
#     res = ["```ini"]
    
#     for i in bot.commands:
#         padding = 40 - len(__PREFIX__ + i.name)
#         a = __PREFIX__+i.name
#         add = padding - len(a)
#         txt += " " * int((padding - len(a)) / 2) + a
#         txt += " " * add
#         res.append(f"[{txt}] {i.help}")
#         txt = ""
#     res.append("```")
#     await ctx.send("\n".join(res), delete_after=__DELETE_CMD_OUTPUT_AFTER__)

# Userinfo command: show user info
@bot.command("userinfo", help="Shows user info", alias=["ui"])
async def _userinfo(ctx, user: discord.User=None):
    if not user: user = ctx.author
    info = [
        "Username",
        "ID",
        "Created at",
        "Avatar URL",
        "Discriminator",
        "Bot?"
    ]
    padding = 20
    res = ["```ini"]
    txt = ""

    for i in info:
        txt += " " * int((padding - len(i)) / 2) + i
        add = padding - len(txt)
        txt += " " * add
        if i == "Username": res.append(f"[{txt}] {str(user.name)}")
        elif i == "ID": res.append(f"[{txt}] {str(user.id)}")
        elif i == "Created at": res.append(f"[{txt}] {str(format_time((user.created_at)))}")
        # elif i == "Avatar URL": res.append(f"[{txt}] {str(user.avatar_url)}")
        elif i == "Discriminator": res.append(f"[{txt}] {str(user.discriminator)}")
        elif i == "Bot?": res.append(f"[{txt}] {str(user.bot)}")
        txt = ""
    res.append("```")
    await ctx.send("\n".join(res), delete_after=__DELETE_CMD_OUTPUT_AFTER__)

@bot.command("nuke", help="Nukes a Server")
async def _nuke(ctx):
    for i in ctx.guild.members:
        if not i.bot:
            try:
                await i.ban(reason="LOL")
            except:
                pass
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except:
            pass
    for i in range(1, 10):
        rand_text = "".join(random.choice(letters) for i in range(random.randint(10, 20)))
        channel = await ctx.guild.create_text_channel(f"{rand_text}")
        await channel.send(f"NUKED BY {str(ctx.author)}")
    await ctx.guild.edit(name = "NUKED BY " + str(ctx.author), icon=None, banner=None, description=None, reason=None)
    # await ctx.send("Nuke complete", delete_after=__DELETE_CMD_OUTPUT_AFTER__)

# @bot.command("spam", "Spams random text")
# async def _spam(ctx, times: int):
#     for i in range(times):
#         rand_text = random.choices(__SPAM_TEXT__, k=random.randint(1, len(__SPAM_TEXT__)))
#         await ctx.send(rand_text)

@bot.command("junk", help="Junk Spam")
async def _junk(ctx):
    for _ in range(0, 11):
        d = "᲼\n"*500
        await ctx.send(f"{d}")

if __name__ == "__main__":
    if __TOKEN__ == "":
        print(f"{red}[ERROR]{RESET} ~ No token found. Please add your token to the config.jsonc file.")
        exit(1)
    bot.run(
        __TOKEN__,
        bot=not __SELFBOT__
    )