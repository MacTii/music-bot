"""YouTube playback commands."""
import asyncio
from typing import Optional

import discord
import yt_dlp
from discord.ext import commands

from config import find_ffmpeg

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "default_search": "ytsearch",
    "quiet": True,
    "no_warnings": True,
}
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


async def ensure_voice(ctx: commands.Context) -> Optional[discord.VoiceClient]:
    """Return a voice client, connecting to the author's channel if needed."""
    if ctx.voice_client:
        return ctx.voice_client
    if ctx.author.voice and ctx.author.voice.channel:
        return await ctx.author.voice.channel.connect()
    await ctx.send("Join a voice channel first.")
    return None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ffmpeg = find_ffmpeg()

    @staticmethod
    async def _extract(query: str) -> dict:
        loop = asyncio.get_running_loop()
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = await loop.run_in_executor(
                None, lambda: ydl.extract_info(query, download=False)
            )
        if "entries" in info:
            info = info["entries"][0]
        return info

    @commands.hybrid_command(description="Play audio from a YouTube URL or search phrase")
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        voice = await ensure_voice(ctx)
        if not voice:
            return
        await ctx.defer()
        try:
            info = await self._extract(query)
        except yt_dlp.utils.DownloadError as error:
            await ctx.send(f"Could not load audio: {error}")
            return
        source = discord.FFmpegPCMAudio(info["url"], executable=self.ffmpeg, **FFMPEG_OPTIONS)
        if voice.is_playing() or voice.is_paused():
            voice.stop()
        voice.play(source)
        await ctx.send(f"Now playing: **{info.get('title', query)}**")

    @commands.hybrid_command(description="Join your voice channel")
    async def join(self, ctx: commands.Context) -> None:
        if await ensure_voice(ctx):
            await ctx.send("Joined the voice channel.")

    @commands.hybrid_command(description="Pause the current track")
    async def pause(self, ctx: commands.Context) -> None:
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸")
        else:
            await ctx.send("Nothing is playing.")

    @commands.hybrid_command(description="Resume the paused track")
    async def resume(self, ctx: commands.Context) -> None:
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed ▶")
        else:
            await ctx.send("Nothing is paused.")

    @commands.hybrid_command(description="Stop playback")
    async def stop(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Stopped ⏹")
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.hybrid_command(description="Disconnect from the voice channel")
    async def disconnect(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")
        else:
            await ctx.send("I am not in a voice channel.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
