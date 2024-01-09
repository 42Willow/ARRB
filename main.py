from typing import Optional
import discord
from discord import app_commands
from dotenv import load_dotenv, find_dotenv
import os
import json

load_dotenv()  # Load variables from .env file
# Your secret Discord token, don't share this with anyone!
TOKEN = os.getenv('DISCORD_TOKEN')
# Your guild where you want to sync commands on each startup
GUILD_ID = discord.Object(id=int(os.getenv('DISCORD_GUILD_ID')))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

# @client.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author.id == client.user.id:
#         return

@client.tree.command()
async def ping(interaction:discord.Interaction):
    """Ping ARRB :3"""
    emoji = client.get_emoji(1166270365627056138)
    await interaction.response.send_message(f'Pong! {emoji}')

class ReportView(discord.ui.View):
    def __init__(self, message: discord.Message):
        super().__init__()
        self.message = message  # Store the message
        self.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))
        
    @discord.ui.button(label='Delete', style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.message.delete()
        await interaction.response.send_message(f"Reported message deleted by {interaction.user.mention}")
        button.disabled = True
        self.stop()
        await interaction.message.edit(view=self)

@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(f"Thanks for reporting this message by {message.author.mention} to our moderators.", ephemeral=True)
    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(1117569068220825741)
    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at
    view = ReportView(message)
    await log_channel.send(embed=embed, view=view)

@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    """Purge messages"""
    await interaction.response.send_message(f"Purged {amount} messages", ephemeral=True)
    await interaction.channel.purge(limit=amount)

@client.tree.command()
@app_commands.default_permissions(manage_guild=True)
@app_commands.checks.has_permissions(manage_guild=True)
async def settings(interaction: discord.Interaction):
    """Setup ARRB settings :)"""
    pages = app_commands.Paginator()

# async def audit_log(embed, view: Optional[discord.View], guild):
#     # Get the log channel from data/settings.json
#     with open('data/settings.json') as f:
#         settings = json.load(f)
#         print(settings)
#     log_channel = guild.get_channel(1117569068220825741)
#     await log_channel.send(embed=embed, view=view)

# @client.tree.command()
# @app_commands.describe(member="Who's social status do I check?")
# async def profile(interaction: discord.Interaction, member: Optional[discord.Member] = None):
#     """Sends social status of a member"""
#     # If no member is explicitly provided then we use the command user here
#     member = member or interaction.user

#     # The format_dt function formats the date time into a human readable representation in the official client
#     await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

client.run(TOKEN)