"""Helpers shared by cogs that play audio."""
from typing import Optional

import discord
from discord.ext import commands


async def ensure_voice(ctx: commands.Context) -> Optional[discord.VoiceClient]:
    """Return a voice client, connecting to the author's channel if needed."""
    if ctx.voice_client:
        return ctx.voice_client
    if ctx.author.voice and ctx.author.voice.channel:
        return await ctx.author.voice.channel.connect()
    await ctx.send("Join a voice channel first.")
    return None
