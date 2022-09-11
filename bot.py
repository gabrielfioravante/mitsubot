from commands.random_audio_player.commands import Commands as RapCommands
from discord.ext import commands
from dotenv import dotenv_values
import discord

config = dotenv_values(".env")

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Um bot que toca áudios aleatórios', intents = intents)
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    await bot.add_cog(RapCommands(bot))

if config['TOKEN'] is not None:
    bot.run(config["TOKEN"])
else:
    print('Could not find Discord Token in .env')
