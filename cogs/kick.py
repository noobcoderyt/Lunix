import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):

        if member is None:
            embed = discord.Embed(title="Kick",
                                description="The kick command can be used to kick a user",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.kick <member> [reason]`\n*<member>* - The member you want to kick\n*[reason]* - The reason for the kick (optional)",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.kick noobcoderyt Loser`\n\n*Noobcoder* will be kicked with the reason *Loser*",
                            inline=False)

            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(title="Error!",
                                description="You can't kick this user.",
                                colour=0xff0000)

            await ctx.send(embed=embed)
            return

        if reason is None:
            reason = "No reason specified."
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="Kicked!",
                                description=f"{member.mention} has been kicked!",
                                colour=0x00c105)

            embed.add_field(name="Reason",
                            value=f"`{reason}`",
                            inline=False)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(title="Error!",
                                description="A permission related error has occured.",
                                colour=0xff0000)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            embed = discord.Embed(title="Error!",
                                description="An unknown error has occured",
                                colour=0xff0000)

            embed.add_field(name="Error code",
                            value=f"`{e}`",
                            inline=False)

            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))
