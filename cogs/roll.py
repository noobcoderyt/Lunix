import discord
from discord.ext import commands
import random
import asyncio

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def roll(self, ctx):
        await ctx.send(f"🎲 {ctx.author} rolled a dice!")
        await asyncio.sleep(0.5)
        msg = await ctx.send("*dice rolls down dramatically*")
        await asyncio.sleep(0.5)

        dot = ""
        for n in range(0, 3):
            dot += "."
            await msg.edit(content=dot)
            await asyncio.sleep(0.5)
        await ctx.send(f"{random.randint(1,6)}!!!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Roll(bot))
