import discord
from discord.ext import commands
import json

async def get_bank_data():
    with open("./cogs/bank.json", "r") as f:
        users = json.load(f)
    return users


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["bal"])
    async def balance(self, ctx, arg: str = None):
        user_id = str(ctx.author.id)
        users = await get_bank_data()
        if arg is None:
            if user_id in users:
                wallet = users[user_id]["wallet"]
                embed = discord.Embed(title="Balance",color=0x00b0f4, description=f"""
                <@{user_id}>
                💸 Wallet: {wallet} Lunuks
                """)
                await ctx.reply(embed=embed)

            else:
                embed = discord.Embed(title="Error",color=0x00b0f4,description=f"""
                <@{user_id}>
                You don't have an account!
                Type `.open_account` to create one
                Type `.help economy` for more information
                """)
                await ctx.reply(embed=embed)
        else:
            wallet = users[arg]["wallet"]
            embed = discord.Embed(title="Balance",color=0x00b0f4, description=f"""
            <@{arg}>
            💸 Wallet: {wallet} Lunuks
            """)
            await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Balance(bot))