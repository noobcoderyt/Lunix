import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self, ctx):
        await ctx.send(file=discord.File("media/rules.jpg"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Rules(bot))
