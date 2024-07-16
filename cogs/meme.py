import discord
from discord.ext import commands
import json
import aiohttp

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.blue())
                    embed.set_image(url=data['url'])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Error 404: Meme not found')
async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))