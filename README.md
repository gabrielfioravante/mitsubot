# Mitsubot
A basic Discord bot that plays random audios every N minutes. It reads audio files from the `audio` folder and then plays them randomly. The bot is shipped with only 3 audios by default, but you can add more by simply pasting audio files on the `audio` folder. By default, it plays every 20 minutes.

## Built with
- [Discord.py](https://discordpy.readthedocs.io/en/stable/)

## Prerequisites
In order to work with the Discord API and make the bot play audio, you will need:
- [FFmpeg](https://ffmpeg.org/)
- [Discord Bot account](https://discordpy.readthedocs.io/en/stable/discord.html)
- Create a `.env` file with your bot's token. You can find an example at `sample.env`

```sh
# Python setup:
python3 -m pip install -U discord.py[voice] python-dotenv # Unix
py -3 -m pip install -U discord.py[voice] python-dotenv # Windows
```

You can also setup a [virtual environment](https://discordpy.readthedocs.io/en/stable/intro.html#virtual-environments)

## Default bot commands
You must be connected to a voice channel to run the commands:
- `!start`
- `!start 10` you can also pass a custom time interval(minutes) as an argument
- `!stop`

Instead of using a prefix (e.g.: "!start"), you can mention the bot (e.g.: "@Mitsubot start").

## Todo
- [x] Custom interval support
- [ ] Custom prefix support
