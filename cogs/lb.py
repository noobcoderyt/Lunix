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


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        users = await get_bank_data()
        sorted_users = sorted(users.items(), key=lambda x: x[1]["wallet"], reverse=True)
    
        embed = discord.Embed(title="Leaderboard", color=0x00b0f4)
        for i, (user_id, data) in enumerate(sorted_users[:10], 1):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(name=f"{i}. {user.name}", value=f"{data['wallet']} Lunuks", inline=False)
    
        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
