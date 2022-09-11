import discord, os, asyncio

class SimplePlayer:

    @staticmethod
    async def play(ctx, audio_file: str):
        channel = ctx.author.voice.channel

        if os.path.exists('./audio/' + audio_file) is False:
            await ctx.send('Não foi possível encontrar arquivo de áudio')
            return

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./audio/' + audio_file))            

        if ctx.voice_client is None:
           await channel.connect()
           ctx.voice_client.play(source, after=lambda _: asyncio.run_coroutine_threadsafe(
                                                         coro=ctx.voice_client.disconnect(),
                                                         loop=ctx.voice_client.loop).result())
