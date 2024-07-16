import discord
from discord.ext import commands
import json

async def get_bank_data():
    with open("./cogs/bank.json", "r") as f:
        users = json.load(f)
    return users

async def get_stocks_data():
    with open("./cogs/stocks.json", "r") as f:
        stock_prices = json.load(f)
    return stock_prices

async def get_portfolio_data():
    with open("./cogs/portfolios.json", "r") as f:
        portfolio = json.load(f)
    return portfolio

class Buy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def buy(self, ctx, stock:str, amount: int):
        stock_prices = await get_stocks_data()
        user_portfolios = await get_portfolio_data()
        user_id = str(ctx.author.id)
        stock = stock.upper()
        if stock not in stock_prices:
            embed = discord.Embed(title="Error", color=0x00b0f4, description=f"""
            <@{user_id}>
            Stock not found!
            """)
            await ctx.reply(embed=embed)

        else:
            cost = stock_prices[stock] * amount
            users = await get_bank_data()
            wallet = users[user_id]["wallet"]
            if cost > wallet:
                embed = discord.Embed(title="Error", color=0x00b0f4, description=f"""
                <@{ctx.author.id}>
                You don't have enough Lunuks!
                """)
                await ctx.reply(embed=embed)
            else:
                if user_id not in user_portfolios:
                    user_portfolios[user_id] = {}
                if stock in user_portfolios[user_id]:
                    user_portfolios[user_id][stock] += amount
                    users = await get_bank_data()
                    users[user_id]["wallet"] -= cost
                    user_portfolios[user_id][stock] += amount
                else:
                    user_portfolios[user_id][stock] = amount
                    users = await get_bank_data()
                    users[user_id]["wallet"] -= cost
                with open("./cogs/portfolios.json", "w") as f:
                    json.dump(user_portfolios, f)
                with open("./cogs/bank.json", "w") as f:
                    json.dump(users, f)
                    embed = discord.Embed(title="Transaction Successfull!", color=0x00b0f4, description=f"""
                    <@{ctx.author.id}>
                    You have successfully bought {amount} {stock} for {cost}!
                    """)
                await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Buy(bot))