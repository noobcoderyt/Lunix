import discord 
from discord.ext import commands
import json
import random
import time

cooldowns = {}
async def get_bank_data():
    with open("./cogs/bank.json", "r") as f:
        users = json.load(f)
    return users

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def beg(self, ctx):
        cooldown_time = 60
        user_id = ctx.author.id
        if user_id in cooldowns and time.time() < cooldowns[user_id]:
            await ctx.reply("Dont try to spam bozo")
            return
        cooldowns[user_id] = time.time() + cooldown_time
        user_id = str(ctx.author.id)
        earning = random.randint(1, 100)
        users = await get_bank_data()

        if user_id in users:
            with open("./cogs/bank.json", "w") as f:
                users[user_id]["wallet"] += earning
                json.dump(users, f)
            embed = discord.Embed(title="Earnings!",color=0x00b0f4,description=f"""
                                <@{user_id}>
                                💸 Someone gave you {earning} Lunuks!
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
    await bot.add_cog(Beg(bot))



