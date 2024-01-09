# This file is in charge of managing the following files:
# - data/settings.json
# - data/data.json

import json

# Settings and Data
def new_guild(guild_id):
    with open('data/settings.json', 'r+') as f:
        # Loads the JSON data from file if not empty
        settings = json.load(f) if f.read().strip() else {"guilds": {}}
        
        if not settings.get(str(guild_id)):
            # Define the default settings for a guild
            default_settings = {
                "welcome_message": "Welcome to the server!",
                "mod_log_channel": "0", # Mod log channel ID
                "levels": {
                    "enabled": False,
                    "level_up_message": "Congratulations {user.mention}! You have reached level {level}!",
                    "excluded_channels": [] # List of channel IDs to exclude from levelling
                }
            }

            # Add the default settings for the guild
            settings[str(guild_id)] = default_settings

            # Write the updated settings back to the file
            f.seek(0)  # Move the cursor back to the start of the file
            json.dump(settings, f, indent=4)
            f.truncate()  # Remove any leftover contents from the previous file

# Settings


# Data




# default_settings = {
#     "guilds": {}
# }
# default_layout = {

# def load_settings():
#     with open('data/settings.json') as f:
#         settings = json.load(f)
#     return settings

# def new_guild(guild_id):
#     with open('data/settings.json', 'r+') as f:
#         # Loads the JSON data from file if not empty, otherwise set to default_layout
#         settings = json.load(f) if f.read().strip() else {}
        
#         if not settings.get(str(guild_id)):
#             # Define the default settings for a guild
#             default_settings = {
#                 "prefix": "!",
#                 "welcome_message": "Welcome to the server!",
#                 # Add more default settings here
#             }

#             # Add the default settings for the guild
#             settings[str(guild_id)] = default_settings

#             # Write the updated settings back to the file
#             f.seek(0)  # Move the cursor back to the start of the file
#             json.dump(settings, f, indent=4)
#             f.truncate()  # Remove any leftover contents from the previous file
