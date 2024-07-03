import discord
from discord.ext import commands
import re
import asyncio
from datetime import timedelta
import google.generativeai as genai
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()
ai_api = os.getenv("ai_api")

genai.configure(api_key=ai_api)
model = genai.GenerativeModel("gemini-1.5-flash", 
                              system_instruction="You are a discord bot called Lunix from a discord server named TheLinuxHideout. You talk like people do on whatsapp or discord. You use abbrevations for words like idk, lol, lmao. You also like to roast people. Your answers should be under 200 characters until asked to extend")

cooldowns = {}
cooldown_time = 600

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Message events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.channel.id == 1253742174584180849:
            chat = model.start_chat(history=[])
            response = chat.send_message(message.content)
            if "@" in response.text or "?ban" in response.text or "?kick" in response.text or "?mute" in response.text:
                duration = timedelta(minutes=60)
                await message.author.timeout(duration, reason="trying to be too smart")
                await message.channel.send(f'{message.author.mention} has been timed out for trying to be too smart')
            else:
                await message.reply(response.text)

    
    
        if "kys" in message.content.lower() or message.content == "NI":
            await message.reply("stfu nigga who r u")


        if "socket" in message.content.lower():
            await message.reply("Socket more like Cocket lmfao")

        if "scarry" in message.content.lower():
            await message.reply("Mf be like I have a high end pc while running games in 20fps with 240p")

        if ":trollface:" in message.content.lower():
            await message.channel.send("<:ohwel:1212344068911271936>")
    
        if "hard" in message.content.lower():
            await message.reply("thats what she said")

        user_id = message.author.id
        if "gato" in message.content.lower():
            user_id = message.author.id
            if user_id in cooldowns and time.time() < cooldowns[user_id]:
                await message.channel.send("Dont try to spam bozo")
                return
            cooldowns[user_id] = time.time() + cooldown_time
            for i in range(random.randint(1,5)):
                await message.channel.send("GATO IS BACK")
                asyncio.sleep(0.5)
            await message.channel.send("<:tr:1248294470588563497>")

        if "improved" in message.content.lower():
            await message.reply("<:lie:1220656617691938817>")

        if "new video" in message.content.lower():
            await message.reply("maybe the new video was the friends we made along the way")

        if "mint" in message.content.lower():
            await message.channel.send("Hell yeah Linux Mint")

        if message.content.startswith("?ban <@1126807595517227089>"):
            await message.reply("Major Skill Issue detected ⚠️")

        if "<@1253260636662792213>" in message.content:
            await message.channel.send("I have been summoned")

        if "mrace" in message.content.lower():
            await message.reply("Mr ace more like Mr ass lmfaooooo")

        if message.content.endswith("*"):
            if message.content.startswith("*"):
                return
    
        if re.search("L|LL|LLL", message.content):
            await message.reply("🫵")

    
async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
