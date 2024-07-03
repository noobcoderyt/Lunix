import discord
from discord.ext import commands
import asyncio
import random

class Flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def flip(self, ctx):
        await ctx.send(f"🪙 {ctx.author} flipped a coin!")
        await asyncio.sleep(0.5)
        msg = await ctx.send("*coin falls down dramatically*")
        await asyncio.sleep(0.5)

        dot = ""
        for n in range(0, 3):
            dot += "."
            await msg.edit(content=dot)
            await asyncio.sleep(0.5)
        _8ball_ = ["Heads", "Tails"]
        await ctx.send(f"{random.choice(_8ball_)}!!!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Flip(bot))