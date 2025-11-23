from disnake.ext import commands
from core.localisation import get_text, set_guild_language, SUPPORTED_LANGUAGES
from disnake.ext.commands import Cog, InteractionBot, slash_command
from disnake import AppCommandInteraction


class PingCog(Cog):

    def __init__(self, bot: InteractionBot):
        self.bot = bot


    @slash_command(name="ping", description="🏓 Check if the bot is alive")
    async def ping(self, inter: AppCommandInteraction):

        try:
            text = get_text(inter.guild_id, "ping_response")
            await inter.response.send_message(text)

        except Exception as e:
            print(f"[ERROR] Ping command failed: {e}")
            await inter.response.send_message("⚠️ Something went wrong.", ephemeral=True)


    @slash_command(name="lang", description="🌐 Set server language")
    async def lang(self, inter: AppCommandInteraction, lang_code: str):

        try:
            if not lang_code:
                raise ValueError("Language code is empty")
            
            if set_guild_language(inter.guild_id, lang_code.lower()):
                text = get_text(inter.guild_id, "language_set")
                await inter.response.send_message(text, ephemeral=True)
            else:
                langs = ", ".join(SUPPORTED_LANGUAGES)
                text = get_text(inter.guild_id, "unknown_language", langs=langs)
                await inter.response.send_message(text, ephemeral=True)


        except Exception as e:
            print(f"[ERROR] Lang command failed: {e}")
            await inter.response.send_message(
                get_text(inter.guild_id, "unknown_language", langs=", ".join(SUPPORTED_LANGUAGES)),
                ephemeral=True
            )

def setup(bot: InteractionBot):
    bot.add_cog(PingCog(bot))