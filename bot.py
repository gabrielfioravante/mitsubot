# import discord
from commands.random_audio_player import randomAudioPlayer
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Um bot que toca áudios aleatórios')
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(randomAudioPlayer(bot))
bot.run(os.environ.get('TOKEN'))
