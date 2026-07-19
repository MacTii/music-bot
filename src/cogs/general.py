"""Moderation and utility commands."""
from typing import Optional

import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Check that the bot is alive")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)} ms")

    @commands.hybrid_command(description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str] = None
    ) -> None:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
