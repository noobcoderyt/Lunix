import discord
from discord.ext import commands
import re
import asyncio


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

class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def ban(self, ctx, member: discord.Member = None, duration: str = None, *, reason: str = None):
        async def unban_after_delay(guild, user_id, delay):
            await asyncio.sleep(delay)
            user = await self.bot.fetch_user(user_id)
            await guild.unban(user)
        if member is None:
            embed = discord.Embed(title="Ban",
                                description="The ban command can be used to ban a user",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.ban <member> <duration> [reason]`\n*<member>* - The member you want to ban\n*[duration]* - Duration of the ban (optional)\n*[reason]* - The reason for the ban (optional)",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.ban noobcoderyt 60 Loser`\n\n*Noobcoder* will be banned for 1 minute with the reason *Loser*",
                            inline=False)

            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(title="Error!",
                                description="You can't ban this user.",
                                colour=0xff0000)

            await ctx.send(embed=embed)
            return

        delay = parse_duration(duration) if duration else None
        if duration and not delay:
            embed = discord.Embed(title="Error!",
                                description="Invalid duration format. Use 's' for seconds, 'min' for minutes, 'h' for hours, 'd' for days, 'm' for months, and 'y' for years.",
                                colour=0xff0000)

            await ctx.send(embed=embed)
            return

        if reason is None:
            reason = "No reason specified."

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="Banned!",
                                description=f"{member.mention} has been banned!",
                                colour=0x00c105)

            embed.add_field(name="Reason",
                            value=f"`{reason}`",
                            inline=True)

            embed.add_field(name="Duration",
                            value=f"`{duration}`",
                            inline=True)

            await ctx.send(embed=embed)

            if delay:
                await unban_after_delay(ctx.guild, member.id, delay)

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
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, userId: str = None, *, reason: str = None):

        if userId is None:
            embed = discord.Embed(title="Unban",
                                description="The unban command can be used to unban a banned user",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.unban <member> [reason]`\n*<member>* - The member you want to unban\n*[reason]* - The reason for the unban (optional)",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.unban 1126807595517227089 Not loser`\n\n*Noobcoder* will be unbanned with the reason *Not loser*",
                            inline=False)

            await ctx.send(embed=embed)
            return

        if reason is None:
            reason = "No reason specified."

        user = await self.bot.fetch_user(userId)

        try:
            await ctx.guild.unban(user, reason=reason)

            embed = discord.Embed(title="Unbanned!",
                                description=f"{user.mention} has been unbanned!",
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

        except discord.NotFound:
            embed = discord.Embed(title="Error!",
                                description="User is not banned.",
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
    @commands.has_permissions(ban_members = True)
    async def softban(self, ctx, member: discord.Member = None, *, reason: str = None):

        if member is None:
            embed = discord.Embed(title="Softban",
                                description="The softban command can be used to ban and quickly unban a user",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.softban <member> [reason]`\n*<member>* - The member you want to softban\n*[reason]* - The reason for the softban (optional)",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.softban noobcoderyt Loser`\n\n*Noobcoder* will be softbanned with the reason *Loser*",
                            inline=False)

            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(title="Error!",
                                description="You can't softban this user.",
                                colour=0xff0000)

            await ctx.send(embed=embed)
            return

        if reason is None:
            reason = "No reason specified."
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.guild.unban(member, reason="Ban was a softban")
            embed = discord.Embed(title="Soft Banned!",
                                description=f"{member.mention} has been soft banned!",
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
    await bot.add_cog(Bans(bot))