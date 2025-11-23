from dotenv import load_dotenv
import os
from disnake.ext.commands import InteractionBot
from disnake import Intents


if __name__ == "__main__":
    TOKEN=os.getenv("DISCORD_TOKEN")
    if not TOKEN: raise ValueError("there is no .env")
    bot = InteractionBot()