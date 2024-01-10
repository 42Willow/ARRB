# IMPORTANT

ARRB is currently in development and is not ready for use. Please do not use it in production.

----------------

<p align="center">
  <img width="25%" src="https://github.com/42Willow/ARRB/blob/main/assets/ARRB-round.png?raw=true" />
</p>
<p align="center">
  <b> ~ ARRB ~ </b>
</p>

Automated Rice Ranking Bot: A social credit and general purpose Discord bot which focuses on **simplicity**.

## Background

ARRB was created as a way to have fun whilst refining my Python skills and revisiting `discord.py` (after it was discontinued in 2021).

## Features

- [x] Slash commands
- [x] **Moderation:** Reporting
- [x] **Moderation:** Purging messages
- [ ] **Moderation:** Muting
- [ ] Per-guild configuration
- [ ] Per-guild data storage (e.g. user xp)
- [ ] Daily quests
- [ ] Riceboard (starboard equivalent)
- [ ] Shop (eg. roles, colours, etc.)
- [ ] Prestige/level system
- [ ] Chatgames (eg. trivia, maths, etc.)

## Setup

1. Clone the repository

```bash
git clone https://github.com/42willow/ARRB.git
cd ARRB
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add the following:

```env
# You can get this from https://discord.com/developers/applications
DISCORD_TOKEN="your_token_here"

# This is the ID of the guild that the bot will sync to immediately, other guilds will take up to 1 hour to sync.
DISCORD_GUILD_ID="your_main_server_id_here"
```

5. Run the bot

```bash
python main.py
```

### Usage

#### Permissions

Unless changed manually, the following commands are only available to these specified permissions:

- `/settings`: `manage_guild`
- `/purge`: `manage_messages`
- `/mute`: `manage_roles`
- `/unmute`: `manage_roles`

#### Ranking

ARRB uses a ranking system based on rice. The more rice you have, the higher your rank. Rice is earned by being active in the server (sending messages, etc.). Unlike some other bots, ARRB does not level up linearly. Instead, the amount of rice required to level up increases exponentially - and even that formula is configurable!

## Community

### Contributing

Contributions are welcome, but please open an [issue](https://github.com/42Willow/ARRB/issues) or [discussion](https://github.com/42Willow/ARRB/discussions) first to discuss what you would like to change.

### Support

Support is done through GitHub discussions. Please open a [discussion](https://github.com/42Willow/ARRB/discussions/categories/support) if you have any questions.
