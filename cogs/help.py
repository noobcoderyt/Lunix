import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def help(self, ctx, arg: str = None):

        if arg == "moderation":
            embed = discord.Embed(title="Moderation commands", color=discord.Color.blue(), description="""
            Run individual commands to find out more about them!
            """)

            embed.add_field(name="Commands", value="""
                            `.mute <member> <duration> [reason]` - The mute command can be used to mute a user
                             `.unmute <member> [reason]` - The unmute command can be used to unmute a user
                             `.ban <member> <duration> [reason]` - The ban command can be used to ban a user
                             `.softban <member> [reason]` - The softban command can be used to ban and quickly unban a user
                             `.unban <userID> [reason]` - The unban command can be used to unban a banned user
                             `.kick <member> [reason]` - The kick command can be used to kick a user
                             `.warnadd <user> <reason>` - Adds a warning to a user.
                             `.warnviewid <caseID>` - Views a warning's case.
                             `.warnviewuser <user>` - Views the warnings of a user.
                             `.warnremove <user> <caseID> - Removes a user's warning

                            """, inline=False)
            await ctx.send(embed=embed)
            return
    
        if arg == "economy":
            embed = discord.Embed(title="Economy commands", color=discord.Color.blue(), description="""
            Run individual commands to find out more about them!
            """)

            embed.add_field(name="Commands", value="""
                             `.open_account` - Open your account
                             `.balance <userID (optional)>` - Check account balance of yourself or any other user
                             `.beg` - Get random amount of Lunuks
                             `.send <user>` - Send money to a user
                             `.bet <amount>` - Bet an amount. If you win then your amount is doubled

                            """, inline=False)
            await ctx.send(embed=embed)
            return


        embed = discord.Embed(title="Commands",color=discord.Color.blue(), description="""
            The prefix is '." """)

        embed.add_field(name="Info", value="""
                     `.help` - This command.
                     `.fact` - Sends a fact.
                     `.info` - Displays information about this bot.
                     `.rules` - Displays *some* rules.
                     `.roles` - Displays the roles a member can get.
                     `.fetchrepos <github username>`- Displays the public repositories of a user.
                     `.fetchcommits <github username> <repository name>`- Displays the recent commits of a repository.

                    """, inline=False)

        embed.add_field(name="Fun", value="""
                     `.kamehameha` - Sends a Kamehameha GIF.
                     `.8ball <statement>` - Predicts a statement.
                     `.prowler` - Sends a Prowler meme.
                     `.meme` - Sends a meme.
                     `.comic` - Sends a comic.
                     `.joke` - Sends a joke
                     `.wish <user>` - Sends a Happy Birthday wish to a user of your choice.
                     `.roll` - Rolls a dice.
                    
                       """, inline=False)

    
    
        embed.set_footer(text="Note: Currently Under Development")

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))