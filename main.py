import discord
from discord.ext import commands
import time
import random
import aiohttp
import json
import requests
import google.generativeai as genai
from datetime import timedelta

ai_api = "key"
discord_api = "key"
fact_api = "key"


genai.configure(api_key=ai_api)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="You are a discord bot called Lunix from a discord server named TheLinuxHideout. You talk like people do on whatsapp or discord. You use abbrevations for words like idk, lol, lmao. You also like to roast people.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

coin = ["HEAD", "TAILS"]
_8ball_ = ["very", "NAWWWWW"]
kamehamehagifs = ["https://c.tenor.com/yOej10JYX4sAAAAM/kamehameha-ui-goku.gif","https://66.media.tumblr.com/40e19795a78fbb4dc5212b0416870bad/tumblr_p262c08aKm1wyh2j4o1_500.gif","https://media1.tenor.com/images/8f7b25ee13cfd669418c78cd50431de3/tenor.gif?itemid=11539971","https://4.bp.blogspot.com/-E_BQvOD2TsM/WNKLRZPg3MI/AAAAAAAAZZ8/hdfcuVeBjp88nJQmON6tJyTDvXZhuQtBwCLcB/s1600/Gifs+animados+Kamehameha+11.gif", "https://media.tenor.com/images/be06b296f1144d9d37dadbd22f46cf54/tenor.gif"]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="TheLinuxHideout"))

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
    await ctx.send("""
        > Beginner -> Level 1
        > Intermediate -> Level 5
        > Pro -> Level 10, `Unlocks Embed and Attachments`
        > Advance -> Level 20
        > Legend -> Level 30
        > Amazing Member -> Level 50, `You get a custom role of your choice`
        > VIP -> NoobCoder's friends
""")
    
@bot.command()
async def rules(ctx):
    await ctx.send(file=discord.File("media/rules.jpg"))

@bot.command()
async def flip(ctx):
    await ctx.send(f"🪙 {ctx.author} flipped a coin!")
    time.sleep(0.5)
    await ctx.send("*coin falls down dramatically*")
    time.sleep(0.5)
    await ctx.send(".")
    time.sleep(0.5)
    await ctx.send("..")
    time.sleep(0.5)
    await ctx.send("...")
    time.sleep(0.5)
    await(f"{random.choice(coin)}!!!")

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 {ctx.author} rolled a dice!")
    time.sleep(0.5)
    await ctx.send("*dice rolls down dramatically*")
    time.sleep(0.5)
    await ctx.send(".")
    time.sleep(0.5)
    await ctx.send("..")
    time.sleep(0.5)
    await ctx.send("...")
    time.sleep(0.5)
    await(f"{random.randint(1,6)}!!!")

@bot.command()
async def wish(ctx, arg):
    if "@everyone" in arg or "@here" in arg:
        await ctx.send("Nigga is trying to ping everyone ☠️")
    elif arg == "":
        await ctx.send("You can't wish no one")
    else:
        await ctx.send(f"Happy Birthday {arg}! 🎂🎂🎂")

@bot.command()
async def kamehameha(ctx):
    await ctx.send(random.choice(kamehamehagifs))

@bot.command()
async def calculate(ctx, arg):
    if arg == "":
        await ctx.send("I can't calculate nothing")
    else:
        try:
            await ctx.send(eval(arg))
        except:
            await ctx.send("Nah Im not that good")
    
@bot.command(name="8ball")
async def _8ball(ctx, arg):
    await ctx.send(random.choice(_8ball_))

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
async def comic(ctx):
    response = requests.get('https://xkcd.com/info.0.json')
    data = response.json()
    comic_title = data['title']
    comic_url = data['img']
    embed = discord.Embed(title=comic_title, color=discord.Colour.blue())
    embed.set_image(url=comic_url)
    await ctx.send(embed=embed)

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
async def help(ctx):
    embed = discord.Embed(title="Commands",color=discord.Color.blue(), description="""
        The prefix is '." """)

    embed.add_field(name="Info", value="""
                     `.help` - This command.
                     `.fact` - Sends a fact.    
                     `.calculate <equation>` - Solves an equation.
                     `.info` - Displays information about this bot.
                     `.rules` - Displays *some* rules.
                     `.roles` - Displays the roles a member can get.

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
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == 1253742174584180849:
        chat = model.start_chat(history=[])
        response = chat.send_message(message.content)
        if "@" in response.text or "?ban" in response.text or "?kick" in response.text or "?mute" in response.text or "?obliterate" in response.text or "?eliminate" in response.text:
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

    if "gato" in message.content.lower():
        for i in range(random.randint(1,9)):
            await message.channel.send("GATO IS BACK")
            time.sleep(0.5)
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

    if "discox" in message.content.lower():
        await message.reply(f"Congratulations {message.author}! You are now *an* Member!")

    if message.content.endswith("*"):
        if message.content.startswith("*"):
            return
        else:
            await message.reply("<:Nerd:1156881557680820284>")
    
    if message.content == "LLL" or message.content == "LL" or message.content == "L":
        await message.reply("🫵")

    await bot.process_commands(message)

bot.run(discord_api)
