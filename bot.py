from commands.random_audio_player import randomAudioPlayer
from discord.ext import commands
from dotenv import dotenv_values
import discord

config = dotenv_values(".env")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Um bot que toca áudios aleatórios', intents = intents)
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(randomAudioPlayer(bot))
bot.run(config["TOKEN"])
