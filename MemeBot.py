"""
This bot is designed to make custom meme captions. It will start off with a few templates, 
but more can be added by users through commands. The logic of this bot is to take the image/gif/video
and add the text input by the user to the media
"""

import random
import os
import discord
import giphy_client
from dotenv import load_dotenv
from discord.ext import commands

# retrieve values from .env to connect to Discord Bot and GIPHY API
load_dotenv()
token = os.getenv("meme_bot_token")
api_key = os.getenv("giphy_api_key")
bot = commands.Bot(command_prefix="^") # all commands will be prefaced with '^'
giphy_api = giphy_client.DefaultApi()
gifs = [] # for storing gif media

# store the videos that will be used in response to bot being told '^hello'
hello_list = ['GIFs\Flower-Hello.mp4','GIFs\Frog-Hello.mp4','GIFs\Homer-Hello.mp4']

# perform an image search from GIPHY API
def search_giphy(topic, type: str):
    if type == 'topic':
        results = giphy_api.gifs_search_get(api_key=api_key, q=topic, limit=3, rating='r')
        data = results.data
        # get the links to the resulting gifs and store them
        for item in range(len(data)):
            url = data[item].url
            gifs.append(url)
    elif type == 'trend':
        results = giphy_api.gifs_trending_get(api_key=api_key, limit=5, rating='r')
        data = results.data

        for item in range(len(data)):
            url = data[item].url
            gifs.append(url)
    elif type == 'random':
        results = giphy_api.gifs_random_get(api_key=api_key, rating='r')
        data = results.data
        url = data.url
        gifs.append(url)

@bot.event
async def on_ready():
    print("Successfully logged in as {0.user}".format(bot))

# handle when bot receives message
@bot.event
async def on_message(messageInfo):
    if messageInfo.author == bot.user: # ignore self
        return 
    message = messageInfo.content

    # create a response to being told &hello
    if message.startswith('^hello'):
        hello_vid = random.choice(hello_list) # choose a random video from hello_list
        await messageInfo.channel.send(file=discord.File(hello_vid))
        await messageInfo.channel.send('Hello! I am MemeBot! I am here to help you with all of your meme needs!!!\n'
        'I perform the following functions:\n\n'
        '^search **insert topic**: I will search for 3 GIFs that fit your query\n\n'
        '^trending: I will display the top 5 trending GIFs\n\n'
        '^randomize: I will search for a random GIF\n\n')
    await bot.process_commands(messageInfo)

# command to perform search based on user-given topic
@bot.command()
async def search(ctx, topic: str):
    search_giphy(topic, 'topic')
    await ctx.send('Here are your %s GIFs!!!' % topic)
    for item in range(len(gifs)):
        await ctx.send(gifs[item])
    gifs.clear()

# command to get trending gifs
@bot.command()
async def trending(ctx):
    search_giphy(None, 'trend')
    await ctx.send('Here are the GIFs that are trending!!!')
    for item in range(len(gifs)):
        await ctx.send(gifs[item])
    gifs.clear()

# command to get random gifs
@bot.command()
async def randomize(ctx):
    search_giphy(None, 'random')
    await ctx.send(gifs[0]) 
    gifs.clear()

bot.run(token)