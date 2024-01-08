import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()  # Load variables from .env file

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Sync command tree
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.tree.sync()

@bot.tree.command(name="ping", description="Ping ARRB :3")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(token)