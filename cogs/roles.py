import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        embed = discord.Embed(title="Roles", color=0x00b0f4, description="""
            • Beginner -> Level 1
            • Intermediate -> Level 5
            • Pro -> Level 10, `Unlocks Embed and Attachments`
            • Advance -> Level 20
            • Legend -> Level 30
            • Amazing Member -> Level 50, `You get a custom role of your choice`
            • VIP -> NoobCoder's friends
    """)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))