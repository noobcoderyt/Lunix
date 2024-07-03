import discord
from discord.ext import commands
import json


async def get_bank_data():
    with open("./cogs/bank.json", "r") as f:
        users = json.load(f)
    return users

class openAccount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def open_account(self, ctx):
        user_id = str(ctx.author.id)
        users = await get_bank_data()
        if user_id in users:
            embed = discord.Embed(title="Error",color=0x00b0f4,description=f"""
                <@{user_id}>
                You already have an account!
            """)
            await ctx.reply(embed=embed)
        else:
            with open("./cogs/bank.json", "w") as f:
                users[user_id] = {}
                users[user_id]["wallet"] = 0
                json.dump(users, f)
            embed = discord.Embed(title="Congratulations!",color=0x00b0f4, description=f"""
                                <@{user_id}>
                                You have successfully created an account!
                                Your current balance is 0 Lunuks
                                """)
            await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(openAccount(bot))