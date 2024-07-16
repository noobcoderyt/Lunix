# Libraries
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from discord.ext import tasks

# APIs
load_dotenv()
discord_api = os.getenv("discord_api")


# Discord API Initialization
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# Starting the bot
@tasks.loop(minutes=1)
async def update_activity():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="TheLinuxHideout"),
        discord.Activity(type=discord.ActivityType.watching, name="Youtube"),
        discord.Activity(type=discord.ActivityType.playing, name="Bedwars")
    ]
    for activity in activities:

        
        await bot.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    files = os.listdir("./cogs")

    for filename in files:
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print(f"Logged in as {bot.user}")
    await update_activity()
 

bot.run(discord_api)