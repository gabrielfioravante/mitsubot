import discord, os, random, asyncio
# from time import sleep
from discord.ext import commands, tasks

class playerRoutine:
    def __init__(self, channel_id, ctx, channel):
        self.channel_id = channel_id
        self.ctx = ctx
        self.audios = os.listdir('./audio')
        self.channel = channel
        self.play.start()

    def __select_audio(self):
        selected_audio = random.choice(self.audios)

        if self.audios:
            self.audios.remove(selected_audio)
        else:
            self.audios = os.listdir('./audio')

        return selected_audio

    def after_play(self, error):
        coro = self.ctx.voice_client.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, self.play.loop)
        try:
            fut.result()
        except:
            print("Player error: " + error)

    @tasks.loop(minutes= 20.0)
    async def play(self):
        audio_file = self.__select_audio()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./audio/' + audio_file))            
        if self.ctx.voice_client is None:
           await self.channel.connect()
           self.ctx.voice_client.play(source, after=self.after_play)

    def set_custom_interval(self, custom_interval: float):
        self.play.change_interval(minutes=custom_interval)

    async def cog_unload(self, custom_message):
        if custom_message:
            await self.ctx.send(custom_message)
        self.play.cancel()


class randomAudioPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.routines = []
    
    async def custom_interval_parser(self, instance: playerRoutine, ctx, custom_interval: float):
       if custom_interval != 20.0:
           if custom_interval > 0:
               instance.set_custom_interval(custom_interval)
           else:
               await ctx.send("Formato de tempo inválido. Utilize número positivos...\n Utilizando intervalo padrão (20 minutos)")

    async def create_routine(self, ctx, custom_interval):
        channel_id = ctx.author.voice.channel.id
        channel = ctx.author.voice.channel
        if not any(i.channel_id == channel_id for i in self.routines):
            new_routine = playerRoutine(channel_id, ctx, channel)
            await self.custom_interval_parser(new_routine, ctx, custom_interval)
            self.routines.append(new_routine)   
        else:
            await ctx.send("Eu já fui iniciado, amigão")

    async def remove_routine(self, channel_id, custom_message):
        for instance in self.routines:
            if instance.channel_id == channel_id:
                await instance.cog_unload(custom_message)
                self.routines.remove(instance)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, *_):
            if before.channel is not None and not member.bot:
                if len(before.channel.members) == 0:
                    await self.remove_routine(before.channel.id, 'Não há ninguém no canal. Vou descansar ;)')

    @commands.command()
    async def start(self, ctx, custom_interval: float=20.0):
        if ctx.author.voice:
            await self.create_routine(ctx, custom_interval)
        else:
            await ctx.send("Irmão, você tem que estar conectado a algum canal de voz!")

    @commands.command()
    async def stop(self, ctx):
        await self.remove_routine(ctx.author.voice.channel.id, 'Parando áudios aleatórios no canal')
