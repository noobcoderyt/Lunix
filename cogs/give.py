import discord
from discord.ext import commands
import json
import time

cooldowns = {}
async def get_bank_data():
    with open("./cogs/bank.json", "r") as f:
        users = json.load(f)
    return users


class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def give(self, ctx, member:discord.Member, amount:int):
        cooldown_time = 60
        user_id = ctx.author.id
        if user_id in cooldowns and time.time() < cooldowns[user_id]:
            await ctx.reply("Dont try to spam bozo")
            return
        cooldowns[user_id] = time.time() + cooldown_time

        user_id = str(ctx.author.id)
        member_id = str(member.id)
        users = await get_bank_data()
        wallet = users[user_id]["wallet"]
        if amount > wallet:
            embed = discord.Embed(title="Error",color=0x00b0f4, description=f"""
                <@{user_id}>
                You cannot send more money than you have!
            """)
            await ctx.reply(embed=embed)
        else:
            try:         
                users[user_id]["wallet"] -= amount
                users[member_id]["wallet"] += amount
                with open("./cogs/bank.json", "w") as f:
                    json.dump(users, f)
                embed = discord.Embed(title="Transaction Successful!",color=0x00b0f4,description=f"""
                <@{user_id}>
                🤑 You have successfully transferred {amount} Lunuks to <@{member_id}>
                """)
                await ctx.reply(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Error",color=0x00b0f4,description=f"""
                <@{user_id}>
                An error occurred while performing the transaction!
                Error: {e}
                """)
                await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Give(bot))