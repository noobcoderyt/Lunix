import discord
from discord.ext import commands
from datetime import timedelta
import re

def parse_duration(duration_str):
    unit_multipliers = {
        's': 1,
        'min': 60,
        'h': 3600,
        'd': 86400,
        'm': 2592000,  # 30 days approximation
        'y': 31536000  # 365 days
    }

    match = re.match(r'(\d+)(s|min|h|d|m|y)', duration_str)
    if not match:
        return None

    amount, unit = match.groups()
    return int(amount) * unit_multipliers[unit]


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member = None, duration: str = None, *, reason: str = None):


        if member is None:
            embed = discord.Embed(title="Mute",
                                description="The mute command can be used to mute a user",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.mute <member> <duration> [reason]`\n*<member>* - The member you want to mute\n*<duration>* - The duration of the mute.\n*[reason]* - The reason for the mute (optional)",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.mute noobcoderyt Loser`\n\n*Noobcoder* will be muted with the reason *Loser*",
                            inline=False)

            await ctx.send(embed=embed)
            return
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(title="Error!",
                              description="You can't mute this user.",
                              colour=0xff0000)

            await ctx.send(embed=embed)
            return
            return

        delay = parse_duration(duration) if duration else None
        if duration and not delay:
            embed = discord.Embed(title="Error!",
                                description="Invalid duration format. Use 's' for seconds, 'min' for minutes, 'h' for hours, 'd' for days, 'm' for months, and 'y' for years.",
                                colour=0xff0000)

        if reason is None:
            reason = "No reason specified"

        try:
            timeout_duration = timedelta(seconds=delay) if delay else None
            await member.edit(timed_out_until=discord.utils.utcnow() + timeout_duration, reason=reason)
            embed = discord.Embed(title="Muted!",
                                description=f"{member.mention} has been muted!",
                                colour=0x00c105)

            embed.add_field(name="Reason",
                            value=f"`{reason}`",
                            inline=True)

            embed.add_field(name="Duration",
                            value=f"`{duration}`",
                            inline=True)

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


    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member = None, *, reason: str = None):


        if member is None:
            embed = discord.Embed(title="Unmute",
                                description="The unmute command can be used to unmute a user",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.unmute <member> <duration> [reason]`\n*<member>* - The member you want to unmute\n*[reason]* - The reason for the unmute (optional)",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.unmute noobcoderyt  Not loser`\n\n*Noobcoder* will be unmuted with the reason *Not loser*",
                            inline=False)

            await ctx.send(embed=embed)
            return
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(title="Error!",
                                description="You can't unmute this user.",
                                colour=0xff0000)

            await ctx.send(embed=embed)
            return
            return



        if reason is None:
            reason = "No reason specified"

        try:
            await member.edit(timed_out_until=None, reason=reason)
            embed = discord.Embed(title="Unmuted!",
                                description=f"{member.mention} has been unmuted!",
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
    await bot.add_cog(Mute(bot))