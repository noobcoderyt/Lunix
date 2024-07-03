import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Lunix",color=discord.Color.blue(), description="""
            Whats up! I am Lunix, the offical bot of The Linux Hideout.
            My prefix is '.'""")

    
        embed.add_field(name="Youtube", value="[link](https://youtube.com/@noobcoderyt)", inline=True)
        embed.add_field(name="Github", value="[link](https://github.com/noobcoderyt/Lunix)", inline=True)

        embed.add_field(name="", value="I will also reply to your messages occasionally!", inline=False)

        embed.set_footer(text="Note: Currently Under Development")

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))