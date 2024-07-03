import discord
from discord.ext import commands

class Wish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wish(self, ctx, member: str = None):
        if member is None:
            await ctx.send("You can't wish no one")
        elif "@everyone" in member or "@here" in member:
            await ctx.send("Nigga is trying to ping everyone ☠️")
        else:
            await ctx.send(f"Happy Birthday {member}! 🎂🎂🎂")

async def setup(bot: commands.Bot):
    await bot.add_cog(Wish(bot))