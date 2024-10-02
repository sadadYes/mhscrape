import discord
import os
from discord import app_commands
from get_command import setup_get
from query_command import setup_query
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class StudentInfoBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.tree.sync()

client = StudentInfoBot()

setup_get(client)
setup_query(client)

client.run(TOKEN)

