# ARRB

Automated Rice Ranker Bot: A social credit and general purpose Discord bot which focuses on simplicity.

## Background

ARRB was created as a way to have fun whilst refining my Python skills and revisiting `discord.py` (after it was discontinued in 2021).

## Features

- [x] Slash commands
- [x] **Moderation:** Reporting
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
DISCORD_TOKEN="your_token_here"

DISCORD_GUILD_ID="your_main_server_id_here"
```

5. Run the bot

```bash
python main.py
```

## Community (Contributing, Support, etc.)

### Contributing

Contributions are welcome, but please open an [issue](https://github.com/42Willow/ARRB/issues) or [discussion](https://github.com/42Willow/ARRB/discussions) first to discuss what you would like to change.

### Support

Support is done through GitHub discussions. Please open a [discussion](https://github.com/42Willow/ARRB/discussions/categories/support) if you have any questions.
