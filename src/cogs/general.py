"""Utility commands."""
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Check that the bot is alive")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)} ms")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
