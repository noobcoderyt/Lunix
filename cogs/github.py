import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

load_dotenv()
github_api = os.getenv("github_api")

class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fetchrepos(self, ctx, username="noobcoderyt"):
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

    @commands.command()
    async def fetchcommits(self, ctx, username="noobcoderyt", repo_name="Lunix"):
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

async def setup(bot: commands.Bot):
    await bot.add_cog(Github(bot))