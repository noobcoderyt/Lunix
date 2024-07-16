import discord
from discord.ext import commands
import json

async def get_stocks_data():
    with open("./cogs/stocks.json", "r") as f:
        stock_prices = json.load(f)
    return stock_prices

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stocks(self, ctx):
        user_id = ctx.author.id
        stock_prices = await get_stocks_data()
        stock_list = '\n'.join([f'**{stock}: {price}**' for stock, price in stock_prices.items()])
        embed = discord.Embed(title="📈 Stocks", color=0x00b0f4, description=f"""
        <@{user_id}>
        The current stock prices are:\n
        {stock_list}
        """)
        await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Stocks(bot))