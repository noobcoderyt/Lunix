import discord
from discord.ext import commands
import random

kamehamehagifs = ["https://c.tenor.com/yOej10JYX4sAAAAM/kamehameha-ui-goku.gif",
                  "https://66.media.tumblr.com/40e19795a78fbb4dc5212b0416870bad/tumblr_p262c08aKm1wyh2j4o1_500.gif",
                  "https://media1.tenor.com/images/8f7b25ee13cfd669418c78cd50431de3/tenor.gif?itemid=11539971",
                  "https://4.bp.blogspot.com/-E_BQvOD2TsM/WNKLRZPg3MI/AAAAAAAAZZ8/hdfcuVeBjp88nJQmON6tJyTDvXZhuQtBwCLcB/s1600/Gifs+animados+Kamehameha+11.gif", 
                  "https://media.tenor.com/images/be06b296f1144d9d37dadbd22f46cf54/tenor.gif"]


class KHH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kamehameha(self, ctx):
        await ctx.send(random.choice(kamehamehagifs))

async def setup(bot: commands.Bot):
    await bot.add_cog(KHH(bot))