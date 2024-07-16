import discord
from discord.ext import commands
import random

class Prowler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def prowler(self, ctx):
        await ctx.send(file=discord.File("media/Prowler Goku meme.mp4"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Prowler(bot))