# Libraries
import asyncio
import re
import discord
from discord.ext import commands
import time
import random
import aiohttp
import json
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import timedelta
import aiosqlite
import asyncio
import string
import re
from discord.ext import tasks

# APIs
load_dotenv()
ai_api = os.getenv("ai_api")
discord_api = os.getenv("discord_api")
fact_api = os.getenv("fact_api")
github_api = os.getenv("github_api")

# Initializing AI
genai.configure(api_key=ai_api)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="You are a discord bot called Lunix from a discord server named TheLinuxHideout. You talk like people do on whatsapp or discord. You use abbrevations for words like idk, lol, lmao. You also like to roast people. Your answers should be under 200 characters until asked to extend")

# Discord API Initialization
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)


kamehamehagifs = ["https://c.tenor.com/yOej10JYX4sAAAAM/kamehameha-ui-goku.gif","https://66.media.tumblr.com/40e19795a78fbb4dc5212b0416870bad/tumblr_p262c08aKm1wyh2j4o1_500.gif","https://media1.tenor.com/images/8f7b25ee13cfd669418c78cd50431de3/tenor.gif?itemid=11539971","https://4.bp.blogspot.com/-E_BQvOD2TsM/WNKLRZPg3MI/AAAAAAAAZZ8/hdfcuVeBjp88nJQmON6tJyTDvXZhuQtBwCLcB/s1600/Gifs+animados+Kamehameha+11.gif", "https://media.tenor.com/images/be06b296f1144d9d37dadbd22f46cf54/tenor.gif"]
# Cooldowns
cooldowns = {}
cooldown_time = 600

# Moderation functions
async def unban_after_delay(guild, user_id, delay):
    await asyncio.sleep(delay)
    user = await bot.fetch_user(user_id)
    await guild.unban(user)

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

# Starting the bot
@tasks.loop(minutes=1)
async def update_activity():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="TheLinuxHideout"),
        discord.Activity(type=discord.ActivityType.watching, name="Youtube"),
        discord.Activity(type=discord.ActivityType.playing, name="Bedwars")
    ]
    for activity in activities:
        await bot.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await update_activity()

### Prefix Commands
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Lunix",color=discord.Color.blue(), description="""
        Whats up! I am Lunix, the offical bot of The Linux Hideout.
        My prefix is '.'""")

    
    embed.add_field(name="Youtube", value="[link](https://youtube.com/@noobcoderyt)", inline=True)
    embed.add_field(name="Github", value="[link](https://github.com/noobcoderyt/Lunix)", inline=True)

    embed.add_field(name="", value="I will also reply to your messages occasionally!", inline=False)

    embed.set_footer(text="Note: Currently Under Development")

    await ctx.send(embed=embed)

@bot.command()
async def roles(ctx):
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
    
@bot.command()
async def rules(ctx):
    await ctx.send(file=discord.File("media/rules.jpg"))

@bot.command()
async def flip(ctx):
    await ctx.send(f"🪙 {ctx.author} flipped a coin!")
    await asyncio.sleep(0.5)
    msg = await ctx.send("*coin falls down dramatically*")
    await asyncio.sleep(0.5)

    dot = ""
    for n in range(0, 3):
        dot += "."
        await msg.edit(content=dot)
        await asyncio.sleep(0.5)
    _8ball_ = ["HEADS", "TAILS"]
    await ctx.send(f"{random.choice(_8ball_)}!!!")

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 {ctx.author} rolled a dice!")
    await asyncio.sleep(0.5)
    msg = await ctx.send("*dice rolls down dramatically*")
    await asyncio.sleep(0.5)

    dot = ""
    for n in range(0, 3):
        dot += "."
        await msg.edit(content=dot)
        await asyncio.sleep(0.5)
    await ctx.send(f"{random.randint(1,6)}!!!")

@bot.command()
async def wish(ctx, member: str = None):
    if member is None:
        await ctx.send("You can't wish no one")
    elif "@everyone" in member or "@here" in member:
        await ctx.send("Nigga is trying to ping everyone ☠️")
    else:
        await ctx.send(f"Happy Birthday {member}! 🎂🎂🎂")

@bot.command()
async def kamehameha(ctx):
    await ctx.send(random.choice(kamehamehagifs))
    
@bot.command(name="8ball")
async def _8ball(ctx):
    await ctx.send(random.choice(["very", "NAWWWWW"]))

@bot.command()
async def prowler(ctx):
    await ctx.send(file=discord.File("media/Prowler Goku meme.mp4"))

@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://meme-api.com/gimme') as response:
            if response.status == 200:
                data = await response.json()
                embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.blue())
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send('Error 404: Meme not found')

@bot.command()
async def comic(ctx, number=None):
    if number is None:
        number = random.randint(1, 2900)
        response = requests.get(f'https://xkcd.com/{number}/info.0.json')
        data = response.json()
        comic_title = data['title']
        comic_url = data['img']
        embed = discord.Embed(title=comic_title, color=discord.Colour.blue())
        embed.set_image(url=comic_url)
        await ctx.send(embed=embed)
    else:
        try:
            response = requests.get(f'https://xkcd.com/{number}/info.0.json')
            data = response.json()
            comic_title = data['title']
            comic_url = data['img']
            embed = discord.Embed(title=comic_title, color=discord.Colour.blue())
            embed.set_image(url=comic_url)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f'I failed daddy 😔')

@bot.command()
async def joke(ctx):
    response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit")
    data = response.json()
    await ctx.send(f"{data['setup']} - {data['delivery']}")

@bot.command()
async def fact(ctx):
    response = requests.get("https://api.api-ninjas.com/v1/facts", headers={'X-Api-Key': fact_api})
    fact_data = json.loads(response.text)
    fact_text = fact_data[0]['fact']
    await ctx.send(fact_text)

@bot.command()
async def help(ctx, arg: str = None):

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
                             `.warnview <caseID>` - Views a warning's case.
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


@bot.command()
async def fetchrepos(ctx, username="noobcoderyt"):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {
        'Authorization': f'token {github_api}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        repo_names = [repo['name'] for repo in repos]
        message = '```\n' + '\n'.join(repo_names) + '\n```'
        await ctx.send(message)
    else:
        await ctx.send(f'I failed daddy 😔')

@bot.command()
async def fetchcommits(ctx,username="noobcoderyt",repo_name="Lunix"):
    url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
    headers = {
        'Authorization': f'token {github_api}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        commits = response.json()
        commit_messages = [commit['commit']['message'] for commit in commits[:10]]
        message = '```\n' + '\n'.join(commit_messages) + '\n```'
        await ctx.send(message)
    else:
        await ctx.send(f'I failed daddy 😔')




### Moderation commands start here

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member = None, *, reason: str = None):

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

@bot.command()
@commands.has_permissions(kick_members = True)
async def ban(ctx, member: discord.Member = None, duration: str = None, *, reason: str = None):

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

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, userId: str = None, *, reason: str = None):

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

    user = await bot.fetch_user(userId)

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

@bot.command()
@commands.has_permissions(ban_members = True)
async def softban(ctx, member: discord.Member = None, *, reason: str = None):

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

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member = None, duration: str = None, *, reason: str = None):


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

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member = None, *, reason: str = None):


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

#Moderation commands end here



#Economy system

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users

@bot.command()
async def open_account(ctx):
    user_id = str(ctx.author.id)
    users = await get_bank_data()
    if user_id in users:
        embed = discord.Embed(title="Error",color=0x00b0f4,description=f"""
            <@{user_id}>
            You already have an account!
""")
        await ctx.reply(embed=embed)
    else:
        with open("bank.json", "w") as f:
            users[user_id] = {}
            users[user_id]["wallet"] = 0
            json.dump(users, f)
            embed = discord.Embed(title="Congratulations!",color=0x00b0f4, description=f"""
            <@{user_id}>
            You have successfully created an account!
            Your current balance is 0 Lunuks
""")
            await ctx.reply(embed=embed)

@bot.command(aliases = ["bal"])
async def balance(ctx, arg:str = None):
    user_id = str(ctx.author.id)
    users = await get_bank_data()
    if arg==None:
        if user_id in users:
            wallet = users[user_id]["wallet"]
            embed = discord.Embed(title="Balance",color=0x00b0f4, description=f"""
            <@{user_id}>
            💸 Wallet: {wallet} Lunuks
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
    else:
        wallet = users[arg]["wallet"]
        embed = discord.Embed(title="Balance",color=0x00b0f4, description=f"""
            <@{arg}>
            💸 Wallet: {wallet} Lunuks
""")
        await ctx.reply(embed=embed)

@bot.command()
async def beg(ctx):
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
        with open("bank.json", "w") as f:
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

@bot.command()
async def give(ctx, member:discord.Member, amount:int):
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
    if amount>wallet:
        embed = discord.Embed(title="Error",color=0x00b0f4, description=f"""
            <@{user_id}>
            You cannot send more money than you have!
""")
        await ctx.reply(embed=embed)
    else:
        try:         
            users[user_id]["wallet"] -= amount
            users[member_id]["wallet"] += amount
            with open("bank.json", "w") as f:
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


@bot.command()
async def bet(ctx, amount:int=None):
    user_id = str(ctx.author.id)
    users = await get_bank_data()
    if user_id in users:
        if amount == None:
            embed = discord.Embed(title="Error",color=0x00b0f4, description=f"""
                <@{user_id}>
                Please enter an amount to bet!
    """)
            await ctx.reply(embed=embed)
        else:
            wallet = users[user_id]["wallet"]
            if amount > wallet:
                embed = discord.Embed(title="Error",color=0x00b0f4, description=f"""
            <@{user_id}>
            You cannot bet money than you have!
""")
                await ctx.reply(embed=embed)
            else:
                probability = random.randint(0,1)
                embed = discord.Embed(title="Bet", color=0x00b0f4, description=f"""
            <@{ctx.author.id}>
            💵 You betted {amount} Lunuks!

""")
                await ctx.reply(embed=embed)
                await asyncio.sleep(0.5)
                await ctx.send(".")
                await asyncio.sleep(0.5)
                await ctx.send("..")
                await asyncio.sleep(0.5)
                await ctx.send("...")
                await asyncio.sleep(0.5)

                if probability == 0:
                    users[user_id]["wallet"] += amount*2
                    with open("bank.json", "w") as f:
                        json.dump(users, f)
                    embed = discord.Embed(title="You Won!",color=0x00b0f4, description=f"""
            <@{ctx.author.id}>
            💰 You won the bet! Your amount has been doubled!
""")
                    await ctx.reply(embed=embed)

                elif probability == 1:
                    users[user_id]["wallet"] -= amount
                    with open("bank.json", "w") as f:
                        json.dump(users, f)
                    embed = discord.Embed(title="You Lost!",color=0x00b0f4, description=f"""
            <@{ctx.author.id}>
            💰 You lost the bet! Your balance has been decreased by {amount} Lunuks!
""")
                    await ctx.reply(embed=embed)

                else:
                    embed = discord.Embed(title="Error",color=0x00b0f4,description=f"""
            <@{user_id}>
            An error occurred while betting!
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
        




# Message Events
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == 1253742174584180849:
        chat = model.start_chat(history=[])
        response = chat.send_message(message.content)
        if "@" in response.text or "?ban" in response.text or "?kick" in response.text or "?mute" in response.text:
            duration = timedelta(minutes=60)
            await message.author.timeout(duration, reason="trying to be too smart")
            await message.channel.send(f'{message.author.mention} has been timed out for trying to be too smart')
        else:
            await message.reply(response.text)

    
    
    if "kys" in message.content.lower() or message.content == "NI":
        await message.reply("stfu nigga who r u")

    if "socket" in message.content.lower():
        await message.reply("Socket more like Cocket lmfao")

    if "scarry" in message.content.lower():
        await message.reply("Mf be like I have a high end pc while running games in 20fps with 240p")

    if ":trollface:" in message.content.lower():
        await message.channel.send("<:ohwel:1212344068911271936>")
    
    if "hard" in message.content.lower():
        await message.reply("thats what she said")

    user_id = message.author.id
    if "gato" in message.content.lower():
        user_id = message.author.id
        if user_id in cooldowns and time.time() < cooldowns[user_id]:
            await message.channel.send("Dont try to spam bozo")
            return
        cooldowns[user_id] = time.time() + cooldown_time
        for i in range(random.randint(1,5)):
            await message.channel.send("GATO IS BACK")
            asyncio.sleep(0.5)
        await message.channel.send("<:tr:1248294470588563497>")

    if "improved" in message.content.lower():
        await message.reply("<:lie:1220656617691938817>")

    if "new video" in message.content.lower():
        await message.reply("maybe the new video was the friends we made along the way")

    if "mint" in message.content.lower():
        await message.channel.send("Hell yeah Linux Mint")

    if message.content.startswith("?ban <@1126807595517227089>"):
        await message.reply("Major Skill Issue detected ⚠️")

    if "<@1253260636662792213>" in message.content:
        await message.channel.send("I have been summoned")

    if "mrace" in message.content.lower():
        await message.reply("Mr ace more like Mr ass lmfaooooo")

    if message.content.endswith("*"):
        if message.content.startswith("*"):
            return
        else:
            await message.reply("<:Nerd:1156881557680820284>")
    
    if message.content == "L" or message.content == "LL" or message.content == "LLL":
        await message.reply("🫵")

    await bot.process_commands(message)

# Warning system
@bot.command()
@commands.has_permissions(moderate_members=True)
async def warnadd(ctx, member: discord.Member = None, reason: str = None):
    conn = await aiosqlite.connect("warnings.sqlite")
    cursor = await conn.cursor()

    await cursor.execute("""CREATE TABLE IF NOT EXISTS warnings (userid INTEGER, caseid TEXT, reason TEXT, moderatorid INTEGER)""")

    if member is None or member.bot:
            await ctx.send("> ❓ | Please provide a valid member to warn.")
    elif reason is None:
            await ctx.send("> ❓ | Please provide a reason to warn.")
    elif member == ctx.author:
        await ctx.send("> ❌ | You cannot warn yourself.")
    elif member.top_role >= ctx.author.top_role:
        await ctx.send("> ❌ | You can't warn this user as they have a higher role than you or are the same.")
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
        await ctx.send(f"> ✅ | {member} has successfully been warned.")
        await member.send(embed=userWarnEmbed)

        await cursor.execute("""SELECT userid FROM warnings WHERE userid = ?""", (membertoInt,))
        all = await cursor.fetchall()

        if len(all) == 5:
            await member.send("> 🔨 |  You have been banned as you have received ``5 warnings``")
            await member.ban(reason="This user has reached 5 warnings.")
        else:
            return
    

@warnadd.error
async def waerror(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("> ❌ | Please enter a **valid** member to warn.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("> ❌ | You don't have enough permissions to warn.")
    


@bot.command()
@commands.has_permissions(moderate_members=True)
async def warnremove(ctx, member: discord.Member = None, caseId: str = None):
    conn = await aiosqlite.connect("warnings.sqlite")
    cursor = await conn.cursor()

    if member is None or member.bot:
        await ctx.send("> ❓ | Please provide a valid member to remove the warning")
    elif caseId is None:
        await ctx.send("> ❓ | Please provide a case ID")
    elif member == ctx.author:
        await ctx.send("> ❌ | You cannot remove your own warnings.")
    elif member.top_role >= ctx.author.top_role:
        await ctx.send("> ❌ | You can't remove the warning of this user as they have a higher role than you or are the same.")
    else:
        memberToInt = int(member.id)
        await cursor.execute("""SELECT userid, caseid from warnings WHERE caseid = ? AND userid = ?""", (caseId, memberToInt,))
        check = await cursor.fetchone()

        if check:
            await cursor.execute("""DELETE FROM warnings WHERE caseid = ?""", (caseId,))
            await conn.commit()

            userRmvWarnEmbed = discord.Embed(title="", description=f"> Your warning with the case ID ``{caseId}`` has been removed by {ctx.author}", color=discord.Color.blue())
            await member.send(embed=userRmvWarnEmbed)
            await ctx.send(f"> ✅ | {member}'s warning has been removed.")
        else:
            await ctx.send("> ❌ | Nothing found.")
        await conn.close()

@warnremove.error
async def wrerror(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Please provide a **valid** member to warn.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("> ❌ | You don't have enough permissions to remove someone's warning.")



@bot.command()
@commands.has_permissions(moderate_members=True)
async def warnview(ctx, caseId: str = None):
    if caseId is None:
        await ctx.send("> ❓ | Please provide a case ID")
    else:
        conn = await aiosqlite.connect("warnings.sqlite")
        cursor = await conn.cursor()

        await cursor.execute("""SELECT caseid, userid, reason, moderatorid FROM warnings WHERE caseid = ?""", (caseId,))
        case = await cursor.fetchone()

        if case:
            caseEmbed = discord.Embed(title=f"Case {case[0]}", description=f"User warned: <@{case[1]}>\nModerator: <@{case[3]}>\nReason: ``{case[2]}``", color=discord.Color.blue())
            await ctx.send(embed=caseEmbed)
        else:
            await ctx.send("> ❌ | There is no such case ID in my database.")
        await conn.close()

@warnview.error
async def wverror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("> ❌ | You don't have enough permissions view warnings.")
        

bot.run(discord_api)
