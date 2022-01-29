import discord, os, random
from time import sleep
from discord.ext import commands, tasks

class commandInstance:
    def __init__(self, channel_id, ctx):
        self.channel_id = channel_id
        self.ctx = ctx
        self.audios = os.listdir('./audio')
        self.play.start()

    def __select_audio(self):
        selected_audio = random.choice(self.audios)

        if self.audios:
            self.audios.remove(selected_audio)
        else:
            self.audios = os.listdir('./audio')

        return selected_audio

    @tasks.loop(seconds=0.0, minutes=20.0)
    async def play(self):
        audio_file = self.__select_audio()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./audio/' + audio_file))            
        if self.ctx.voice_client is None:
           await self.ctx.author.voice.channel.connect()
           self.ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

           await self.ctx.send('Now playing: {}'.format(audio_file))

           while self.ctx.voice_client.is_playing():
             sleep(1)
           await self.ctx.voice_client.disconnect()

    def cog_unload(self):
        self.play.cancel()


class randomAudioPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.instances = []
    

    @commands.command()
    async def start(self, ctx):
           if ctx.author.voice:
               channel_id = ctx.author.voice.channel.id
               if not any(i.channel_id == channel_id for i in self.instances):
                   new_instance = commandInstance(channel_id, ctx)
                   self.instances.append(new_instance)   
               else:
                await ctx.send("Eu já fui iniciado, amigão")
           else:
               await ctx.send("Irmão, você tem que estar conectado a algum canal de voz!")

    @commands.command()
    async def stop(self, ctx):
        for instance in self.instances:
            if instance.channel_id == ctx.author.voice.channel.id:
                instance.cog_unload()
                self.instances.remove(instance)
                await ctx.send("Tá bom, eu paro")


