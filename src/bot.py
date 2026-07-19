import discord
from discord.ext import commands

from config import COMMAND_PREFIX

COGS = ("cogs.music", "cogs.general")


class MusicBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  # required for $-prefix commands
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)

    async def setup_hook(self) -> None:
        for cog in COGS:
            await self.load_extension(cog)
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} slash commands")

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (discord.py {discord.__version__})")

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            await ctx.send(str(error))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: `{error.param.name}`")
            return
        raise error
