import discord
from discord.ext import commands
import random

class _8ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def _8ball(self, ctx):
        await ctx.send(random.choice(["very", "NAWWWWW"]))

async def setup(bot: commands.Bot):
    await bot.add_cog(_8ball(bot))