import discord
from discord.ext import commands
import requests

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit")
        data = response.json()
        await ctx.send(f"{data['setup']} - {data['delivery']}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Joke(bot))