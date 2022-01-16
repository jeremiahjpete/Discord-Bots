"""
This bot is designed to perform actions related to Youtube from Discord, such as searching for videos
as well as playing audio from Youtube videos through the voice channels 
"""

import os
import discord
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from googleapiclient.discovery import build

# retrieve discord token and API key from .env file to connect to bot
load_dotenv()
TOKEN = os.getenv("youtubeBotToken")
KEY = os.getenv("apiKey")
channel_id = os.getenv("channelID")
youtubeAPI = build('youtube', 'v3', developerKey=KEY)

bot = commands.Bot(command_prefix="!")

video_list = [] # for storing list of videos that were searched

# get the video that is being searched for
def search_video(searchVal: str):
    videoID = youtubeAPI.search().list(
        part="id",
        type="video",
        q=searchVal,
        videoDefinition="any",
        maxResults=5,
        fields="items(id(videoId))"
    ).execute()

    # retrieve results from API based on searchVal
    baseURL = 'https://www.youtube.com/watch?v='

    for item in videoID['items']:
        # retrieve the ID
        id = item['id']['videoId']
        # combine url and video ID into proper hyperlink and add to list
        hyperlink = baseURL + id
        video_list.append(hyperlink)

# print to stdout when connection is successful
@bot.event
async def on_ready():
    print("Successfully logged in as {0.user}".format(bot))

# function to handle what happens when messages are received
@bot.event
async def on_message(messageVal):
    if messageVal.author == bot.user: # ignore self
        return
    
    message = messageVal.content

    # create a response to being told #hello
    if message.startswith('!hello'):
        await messageVal.channel.send('Hello! I am YoutubeBot! I am here to handle your Youtube needs!!!\n'
        'I perform the following functions:\n\n'
        '!search **insert topic**: I will perform a search for the topic of your choosing and send back 5 videos matching the term\n\n'
        '!play **insert Youtube link**: I will download the audio from the link given and play it in the **General** voice channel\n\n'
        '!pause: I will pause the audio playing in the voice channel\n\n'
        '!resume: I will resume playing audio\n\n'
        '!stop: I will stop audio completely to allow new audio to be chosen\n\n'
        '!leave: I will leave the voice channel\n\n'
        '***Note: !pause, !resume, !stop, and !leave will only work when I am connected to the voice channel***\n\n'
        'I look forward to helping you with all of your Youtube needs!!!')

    # handle what to do when asked to search
    if message.startswith('!search'):
        searchVal = message.split("!search ", 1)[1] # split keyword from query
        search_video(searchVal)
        # notify for successful search
        await messageVal.channel.send('Here are your %s videos!!!' % searchVal)

        for items in range(len(video_list)):
            await messageVal.channel.send(video_list[items])

        # avoid results carrying over into next search
        video_list.clear() 
    
    await bot.process_commands(messageVal)

# command to play video audio
@bot.command()
async def play(ctx, url: str):
    vid_playing = os.path.isfile("video.mp3") # create local file to store audio being played

    try:
        if vid_playing:
            os.remove("video.mp3")
    except PermissionError: # in case command is used while music is playing
        await ctx.send("There is already audio playing, either wait until it is finished or use the '!stop' command")
        return
    
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Video Audio')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    print(str(voice.is_connected()))
    # use the ytdl formatting/ffmpeg tool as a basis in order to convert video to audio bot can play 
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '164'
        }],
    }

    # download video audio as mp3 and rename to "video.mp3" in order to play any inputted youtube video
    with youtube_dl.YoutubeDL(ytdl_opts) as dl:
        await ctx.send("Downloading audio... please wait")
        dl.download([url])
        
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "video.mp3")

    print(str(voice.is_connected()))
    voice.play(discord.FFmpegPCMAudio("video.mp3"))
    await ctx.send("Audio done downloading! Playing in voice channel now!")
    print("Playing Audio...")

# command to resume the audio being played in channel
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Audio is already playing!')

# command to pause the audio being played in channel
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('Audio currently not being played')

# command to leave voice channel
@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Bot is not currently connected")

# command to stop audio but remain in channel
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

# handle various exceptions that appears when inputting messages/commands 
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(TOKEN)