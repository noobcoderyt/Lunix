import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
fact_api = os.getenv("fact_api")

class Fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fact(self, ctx):
        response = requests.get("https://api.api-ninjas.com/v1/facts", headers={'X-Api-Key': fact_api})
        fact_data = json.loads(response.text)
        fact_text = fact_data[0]['fact']
        await ctx.send(fact_text)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fact(bot))