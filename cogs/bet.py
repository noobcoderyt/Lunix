import discord
from discord.ext import commands
import json
import asyncio
import random


cooldowns = {}
async def get_bank_data():
    with open("./cogs/bank.json", "r") as f:
        users = json.load(f)
    return users

class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def bet(self, ctx, amount: int = None):
        user_id = str(ctx.author.id)
        users = await get_bank_data()
        if user_id in users:
            if amount == None:
                embed = discord.Embed(title="Error",color=0x00b0f4, description=f"""
                <@{user_id}>
                Please enter an amount to bet!
                """)
                await ctx.reply(embed=embed)
            else:
                wallet = users[user_id]["wallet"]
                if amount > wallet:
                    embed = discord.Embed(title="Error",color=0x00b0f4, description=f"""
                    <@{user_id}>
                    You cannot bet money than you have!
                    """)
                    await ctx.reply(embed=embed)
                else:
                    probability = random.randint(0,1)
                    embed = discord.Embed(title="Bet", color=0x00b0f4, description=f"""
                    <@{ctx.author.id}>
                    💵 You betted {amount} Lunuks!
                """)
                    await ctx.reply(embed=embed)
                
                    dot = "."
                    msg = await ctx.send(dot)
                    for n in range(2):
                        dot += "."
                        await asyncio.sleep(0.5)
                        await msg.edit(content=dot)

                    if probability == 0:
                        users[user_id]["wallet"] += amount*2
                        with open("./cogs/bank.json", "w") as f:
                            json.dump(users, f)
                        embed = discord.Embed(title="You Won!",color=0x00b0f4, description=f"""
                                <@{ctx.author.id}>
                                💰 You won the bet! Your amount has been doubled!
                                """)
                        await ctx.reply(embed=embed)

                    elif probability == 1:
                        users[user_id]["wallet"] -= amount
                        with open("./cogs/bank.json", "w") as f:
                            json.dump(users, f)
                        embed = discord.Embed(title="You Lost!",color=0x00b0f4, description=f"""
                        <@{ctx.author.id}>
                        💰 You lost the bet! Your balance has been decreased by {amount} Lunuks!
                        """)
                        await ctx.reply(embed=embed)

                    else:
                        embed = discord.Embed(title="Error",color=0x00b0f4,description=f"""
                        <@{user_id}>
                        An error occurred while betting!
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
async def setup(bot: commands.Bot):
    await bot.add_cog(Bet(bot))