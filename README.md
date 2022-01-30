# Mitsubot
A basic Discord bot that plays random audios every 20 minutes. It reads files from the `audio` folder and then plays them randonly.

## Built with
- [Discord.py](https://discordpy.readthedocs.io/en/stable/)

## Prerequisites
In order to work with the Discord API and make the bot play audio, you will need:
- [FFmpeg](https://ffmpeg.org/)
- [Discord Bot account](https://discordpy.readthedocs.io/en/stable/discord.html)

```sh
python3 -m pip install -U discord.py[voice] python-dotenv # Unix
py -3 -m pip install -U discord.py[voice] python-dotenv # Windows
```
You can also setup a [virtual environment](https://discordpy.readthedocs.io/en/stable/intro.html#virtual-environments)
