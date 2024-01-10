from typing import Optional
import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import json
from discord.ext import tasks
import aiohttp

load_dotenv()  # Load variables from .env file
# Your secret Discord token, don't share this with anyone!
TOKEN = os.getenv('DISCORD_TOKEN')
# Your guild where you want to sync commands on each startup
GUILD_ID = discord.Object(id=int(os.getenv('DISCORD_GUILD_ID')))

##### AUTO SYNC #####
auto_update = os.getenv('GH_AUTO_UPDATE')
repo_owner = os.getenv('GH_REPO_OWNER')
repo_name = os.getenv('GH_REPO_NAME')
branch_name = os.getenv('GH_BRANCH_NAME')

# GitHub API endpoint for obtaining the latest commit hash
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch_name}"

# # Function to check for updates
async def check_for_updates():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                latest_commit_hash = (await response.json())["commit"]["sha"]
                return latest_commit_hash
    except Exception as e:
        print(f"API URL: {api_url}")
        print(f"Error checking for updates: {e}")
        return None

##### BOT #####
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        self.tree.copy_global_to(guild=GUILD_ID)
        self.auto_update.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=20)  # task runs every 20 seconds
    async def auto_update(self):
        print('Updating!...')
        channel = self.get_channel(1166266501133762580)  # channel ID goes here
        try:
            latest_commit_hash = await check_for_updates()
        except Exception as e:
            print(f"Error checking for updates: {e}")
            await channel.send(f"Error checking for updates: {e}")
            return

        if latest_commit_hash:
            try:
                with open("data/last_commit", "r") as file:
                    last_commit_hash = file.read()
            except FileNotFoundError:
                print("File not found. Creating file...")
                with open("data/last_commit", "w") as file:
                    file.write(latest_commit_hash)
                return

            if latest_commit_hash != last_commit_hash:
                print("Update found. Shutting down main.py...")
                await channel.send(f"Update found. Shutting down main.py...")
                with open("data/last_commit", "w") as file:
                    file.write(latest_commit_hash)          
                await client.close()
            else:
                print("No update found.")
                await channel.send(f"No update found.")

    @auto_update.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

@client.tree.command()
async def ping(interaction:discord.Interaction):
    """Ping ARRB :3"""
    emoji = client.get_emoji(1166270365627056138)
    await interaction.response.send_message(f"Pong! {emoji}\nLatency: {round(client.latency * 1000)}ms", ephemeral=True)

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