import discord
from discord.ext import commands
import requests
import random

class Comic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comic(self, ctx, number=None):
        if number is None:
            number = random.randint(1, 2900)
            response = requests.get(f'https://xkcd.com/{number}/info.0.json')
            data = response.json()
            comic_title = data['title']
            comic_url = data['img']
            embed = discord.Embed(title=comic_title, color=discord.Colour.blue())
            embed.set_image(url=comic_url)
            await ctx.send(embed=embed)
        else:
            try:
                response = requests.get(f'https://xkcd.com/{number}/info.0.json')
                data = response.json()
                comic_title = data['title']
                comic_url = data['img']
                embed = discord.Embed(title=comic_title, color=discord.Colour.blue())
                embed.set_image(url=comic_url)
                await ctx.send(embed=embed)
            except Exception:
                await ctx.send(f'I failed daddy 😔')
async def setup(bot: commands.Bot):
    await bot.add_cog(Comic(bot))