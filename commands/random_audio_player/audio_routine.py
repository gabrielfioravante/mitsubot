import discord
from discord.ext import tasks
import asyncio

from .audio_queue import AudioQueue

class AudioRoutine:
    def __init__(self, channel_id, ctx, channel):
        self.channel_id = channel_id
        self.ctx = ctx
        self.audio_queue = AudioQueue()
        self.channel = channel
        self.play.start()

    def get_audio_queue(self) -> AudioQueue:
        return self.audio_queue;

    @tasks.loop(minutes= 20.0)
    async def play(self):
        audio_file = self.audio_queue.front()
        self.audio_queue.dequeue()

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./audio/' + audio_file))            
        if self.ctx.voice_client is None:
           await self.channel.connect()
           self.ctx.voice_client.play(source, after=lambda _: asyncio.run_coroutine_threadsafe(
                                                              coro=self.ctx.voice_client.disconnect(),
                                                              loop=self.ctx.voice_client.loop).result())

    def set_custom_interval(self, custom_interval: float):
        self.play.change_interval(minutes=custom_interval)

    async def cog_unload(self, custom_message):
        if custom_message:
            await self.ctx.send(custom_message)
        self.play.cancel()
