import discord
from discord.ext import commands
import random
import string
import aiosqlite

class Warnings(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot
    
    # Warning system
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnadd(self, ctx, member: discord.Member = None, reason: str = None):
        conn = await aiosqlite.connect("warnings.sqlite")
        cursor = await conn.cursor()

        await cursor.execute("""CREATE TABLE IF NOT EXISTS warnings (userid INTEGER, caseid TEXT, reason TEXT, moderatorid INTEGER)""")

        if member is None or member.bot:
            embed = discord.Embed(title="Add warning",
                                description="The add warning command in order to give a user a warning.",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.warnadd <member> <reason>`\n*<member>* - The member you want to add the warning to.\n<reason> - The reason as to why you're warning.",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.warnadd seventothreesorcery stupid`\n\n*SevenToThreeSorcery* will be given a warning for being **stupid**",
                            inline=False)

            await ctx.reply(embed=embed)
        elif reason is None:
            embed = discord.Embed(title="", description="Please provide a **reason**.", color=discord.Color.red())
            await ctx.reply(embed=embed)
        elif member == ctx.author:
            embed = discord.Embed(title="", description="You cannot warn **yourself**.", color=discord.Color.red())
            await ctx.reply(embed=embed)
        elif member.top_role >= ctx.author.top_role or ctx.author != ctx.guild.owner:
            embed = discord.Embed(title="", description="You cannot warn this user as you have the same role as them or it's higher than yours.", color=discord.Color.red())
            await ctx.reply(embed=embed)
        else:
            capitalLetters, numbers = string.ascii_uppercase, string.digits

            warnId = "LX-"
            for n in range(4):
                warnId += random.choice(capitalLetters)
                warnId += random.choice(numbers)

            membertoInt = int(member.id)

            await cursor.execute("""INSERT INTO warnings (userid, caseid, reason, moderatorid) VALUES (?, ?, ?, ?)""", (membertoInt, warnId, reason, ctx.author.id,))
            await conn.commit()
            userWarnEmbed = discord.Embed(title="", description=f"You have received a **warning** from **The Linux Hideout**\n\nReason: ``{reason}``\n\nIf you believe your warning was a mistake, please contact a Moderator and mention this case ID: ``{warnId}``.", color=discord.Color.blue())
            embed = discord.Embed(title="", description=f"{member} has been successfully warned", color=discord.Color.green())
            await member.send(embed=userWarnEmbed)
            await ctx.reply(embed=embed)

            await cursor.execute("""SELECT userid FROM warnings WHERE userid = ?""", (membertoInt,))
            all = await cursor.fetchall()

            if len(all) >= 5:
                await member.send("> 🔨 |  You have been banned as you have received ``5 warnings``")
                await member.ban(reason="This user has reached/exceeded five warnings.")
            else:
                return
            await conn.close()
    

    @warnadd.error
    async def waerror(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="", description="The member you want to warn has not been **found**.", color=discord.Color.red())
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="", description="You do not have enough **permissions** to warn this user.", color=discord.Color.red())
            await ctx.reply(embed=embed)
    


    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnremove(self, ctx, member: discord.Member = None, caseId: str = None):
        conn = await aiosqlite.connect("warnings.sqlite")
        cursor = await conn.cursor()

        if member is None or member.bot:
            embed = discord.Embed(title="Remove warning",
                                description="The remove warning command in order to remove a warning from a user.",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.warnremove <member> <caseID>`\n*<member>* - The member you want to remove the warning from\n<caseId> - The case ID of the warning.",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.warnremove seventothreesorcery LX-W7X1G7O2`\n\n*SevenToThreeSorcery* will have the warning with the case ID **LX-W7X1G7O2** removed.",
                            inline=False)

            await ctx.reply(embed=embed)
        elif caseId is None:
            embed = discord.Embed(title="", description="Please provide a **valid** case ID", color=discord.Color.blue())
            await ctx.reply(embed=embed)
        elif member == ctx.author:
            embed = discord.Embed(title="", description="You cannot warn **yourself**.", color=discord.Color.blue())
            await ctx.reply(embed=embed)
        elif member.top_role >= ctx.author.top_role or ctx.author != ctx.guild.owner:
            embed = discord.Embed(title="", description="You cannot warn this user as you have the same role as them or it's higher than yours.", color=discord.Color.blue())
            await ctx.reply(embed=embed)
        else:
            memberToInt = int(member.id)
            await cursor.execute("""SELECT userid, caseid from warnings WHERE caseid = ? AND userid = ?""", (caseId, memberToInt,))
            check = await cursor.fetchone()

            if check:
                await cursor.execute("""DELETE FROM warnings WHERE caseid = ?""", (caseId,))
                await conn.commit()

                userRmvWarnEmbed = discord.Embed(title="", description=f"> Your warning with the case ID ``{caseId}`` has been removed by {ctx.author}", color=discord.Color.blue())
                await member.send(embed=userRmvWarnEmbed)
                

                embed = discord.Embed(title="", description=f"Warning with the case ID ``**{caseId}**`` has been removed", color=discord.Color.green())
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(title="", description="There is no such case ID in my database.", color=discord.Color.red())
                await ctx.reply(embed=embed)
            await conn.close()

    @warnremove.error
    async def wrerror(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="", description="The member you want to remove the warning from has not been **found**.", color=discord.Color.red())
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="", description="You do not have enough **permissions** to remove the warning of this user.", color=discord.Color.red())
            await ctx.reply(embed=embed)



    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnviewid(self, ctx, caseId: str = None):
        if caseId is None:
            embed = discord.Embed(title="View warning ID",
                                description="The warning ID you want to look at.",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.warnviewid <caseID>`\n**<caseId>** - The case ID of the warning.",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.warnviewid LX-W7X1G7O2`\n\nThe command will look at the details of the warning given its case ID.",
                            inline=False)
            await ctx.reply(embed=embed)
        else:
            conn = await aiosqlite.connect("warnings.sqlite")
            cursor = await conn.cursor()

            await cursor.execute("""SELECT caseid, userid, reason, moderatorid FROM warnings WHERE caseid = ?""", (caseId,))
            case = await cursor.fetchone()

            if case:
                caseEmbed = discord.Embed(title=f"Case {case[0]}", description=f"User warned: <@{case[1]}>\nModerator: <@{case[3]}>\nReason: ``{case[2]}``", color=discord.Color.blue())
                await ctx.send(embed=caseEmbed)
            else:
                embed = discord.Embed(title="", description="There is no such case ID in my database.", color=discord.Color.red())
                await ctx.reply(embed=embed)
            await conn.close()

    @warnviewid.error
    async def wviderror(cself, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="", description="You do not have enough **permissions** to view a case ID.", color=discord.Color.red())
            await ctx.reply(embed=embed)


    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnviewuser(self, ctx, member: discord.Member = None):
        if member is None or member.bot:
            embed = discord.Embed(title="View warning ID",
                                description="The warning ID you want to look at.",
                                colour=0x00b0f4)

            embed.add_field(name="Usage",
                            value="`.warnviewuser <user>`\n<user> - The user who you want to look warnings at.",
                            inline=False)
            embed.add_field(name="Example",
                            value="`.warnviewuser seventothreesorcery`\n\nThe command will look at the warnings of **SevenToThree**.",
                            inline=False)
            await ctx.reply(embed=embed)
        else:
            conn = await aiosqlite.connect("warnings.sqlite")
            cursor = await conn.cursor()

            membertoInt = int(member.id)
            await cursor.execute("""SELECT caseid, moderatorid, reason FROM warnings WHERE userid = ?""", (membertoInt,))
            fetchwarns = await cursor.fetchall()

            if fetchwarns:
                embed = discord.Embed(title="", description=f"**{member}'s warnings**", color=discord.Color.blue())

                for warnings in fetchwarns:
                    embed.add_field(name=f"Case ``{warnings[0]}``", value=f"Moderator: <@{warnings[1]}>\nReason: ``{warnings[2]}``", inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="", description="No warnings have been found.", color=discord.Color.red())
                await ctx.reply(embed=embed)
            await conn.close()

    
    @warnviewuser.error
    async def wvusererror(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="", description="The member you want to views warnings from has not been **found**.", color=discord.Color.red())
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="", description="You do not have enough **permissions** to view the warning of this user.", color=discord.Color.red())
            await ctx.reply(embed=embed)
    
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Warnings(bot))