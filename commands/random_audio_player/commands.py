from discord.ext import commands
from .audio_routine import AudioRoutine
from .audio_queue import AudioQueue
from .simple_player import SimplePlayer
import os

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_routines: list[AudioRoutine] = []
    
    def get_routine_by_id(self, channel_id) -> AudioRoutine | None:
        for instance in self.audio_routines:
            if instance.channel_id == channel_id:
                return instance
            return None

    async def custom_interval_parser(self, instance: AudioRoutine, ctx, custom_interval: float):
       if custom_interval != 20.0:
           if custom_interval > 0:
               instance.set_custom_interval(custom_interval)
           else:
               await ctx.send("Formato de tempo inválido. Utilize número positivos...\n Utilizando intervalo padrão (20 minutos)")

    async def create_routine(self, ctx, custom_interval):
        channel_id = ctx.author.voice.channel.id
        channel = ctx.author.voice.channel

        if not any(i.channel_id == channel_id for i in self.audio_routines):
            new_routine = AudioRoutine(channel_id, ctx, channel)
            await self.custom_interval_parser(new_routine, ctx, custom_interval)
            self.audio_routines.append(new_routine)   
        else:
            await ctx.send("Eu já fui iniciado, amigão")

    async def remove_routine(self, channel_id, custom_message):
        routine = self.get_routine_by_id(channel_id)

        if routine is not None:
            await routine.cog_unload(custom_message)
            self.audio_routines.remove(routine)

    def get_audio_routine_queue(self, channel_id) -> AudioQueue | None:
        instance = self.get_routine_by_id(channel_id)

        if instance is not None:
            return instance.get_audio_queue()

        return None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, *_):
            if before.channel is not None and not member.bot:
                if len(before.channel.members) == 0:
                    await self.remove_routine(before.channel.id, 'Não há ninguém no canal. Vou descansar ;)')

    @commands.command(name='start')
    async def start(self, ctx, custom_interval: float=20.0):
        if ctx.author.voice:
            await self.create_routine(ctx, custom_interval)
        else:
            await ctx.send("Irmão, você tem que estar conectado a algum canal de voz!")

    @commands.command(name='stop')
    async def stop(self, ctx):
        await self.remove_routine(ctx.author.voice.channel.id, 'Parando áudios aleatórios no canal')

    @commands.command(name='queue')
    async def get_queue(self, ctx):
        routine_queue = self.get_audio_routine_queue(ctx.author.voice.channel.id)

        if routine_queue is not None:
           await ctx.send(routine_queue.get_formatted())

    @commands.command(name='list')
    async def list(self, ctx):
       await ctx.send('\n'.join(os.listdir('./audio')))

    @commands.command(name='play')
    async def play(self, ctx, *, query):
        if ctx.author.voice:
            await SimplePlayer.play(ctx, query)
        else:
            await ctx.send("Irmão, você tem que estar conectado a algum canal de voz!")
