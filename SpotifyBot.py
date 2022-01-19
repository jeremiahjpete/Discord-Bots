"""
This bot is designed to use data from Spotify's API to get items on command, such as
artist pages, songs, albums, lyrics, playlists, genres, and various user data
REQUIRED: pip install spotipy
"""

import os
import spotipy
from dotenv import load_dotenv
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

# retrieve values from .env to connect to Spotify API as well as the Discord Bot
load_dotenv()
token = os.getenv("spotify_bot_token")
client_id = os.getenv("spotify_client_id")
client_secret = os.getenv("spotify_client_secret")
spotify_client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=spotify_client_credentials)
bot = commands.Bot(command_prefix="&") # all commands will be prefaced with '&'

music_list = [] # for storing music info that has been requested

# get the proper info link from the name that is being requested
def get_link(name: str, q: str, info_type: str): 
    # perform a search based upon the message received
    results = sp.search(q=q+':'+name, limit=3,type=info_type)
    if q == 'track':
        # retrieve song uri
        song_id = results['tracks']['items'][0]['uri']
        track_info = sp.track(song_id)
        # get the link to the song from the JSON data, which can be fully seen by using print(song_id)
        song_link = track_info['external_urls']['spotify']
        music_list.append(song_link)
    elif q == 'album':
        # retrieve album uri
        album_id = results['albums']['items'][0]['uri']
        album_info = sp.album(album_id)
        album_link = album_info['external_urls']['spotify']
        music_list.append(album_link)
    elif q == 'genre':
        # store the top 3 artist ids in an array
        for item in range(len(results['artists']['items'])):
            artist_id = results['artists']['items'][item]['uri']
            artist_info = sp.artist(artist_id)
            artist_link = artist_info['external_urls']['spotify']
            music_list.append(artist_link)

@bot.event
async def on_ready():
    print("Successfully logged in as {0.user}".format(bot))

# event handling for when bot receives messages
@bot.event
async def on_message(messageInfo):
    if messageInfo.author == bot.user: # ignore self
        return 
    message = messageInfo.content

    # create a response to being told &hello
    if message.startswith('&hello'):
        await messageInfo.channel.send('Hello! I am SpotifyBot! I am here to handle your Spotify needs!!!\n'
        'I perform the following functions:\n\n'
        '&song **insert song name**: I will retrieve a link to the song you have requested\n\n'
        '&album **insert album name**: I will retrieve a link to the album you have requested\n\n'
        '&genre **insert genre**: I will retrieve 3 artists that match the genre criteria\n\n'
        '***Note: Unlike my big brother YoutubeBot, I cannot directly play entire tracks in the voice channel because of Spotify streaming limitations***\n\n'
        'I look forward to helping you with your Spotify needs!!!')

    await bot.process_commands(messageInfo)

# command to get song link
@bot.command(pass_context=True)
async def song(ctx, song_name: str):
    get_link(song_name, 'track', 'track')
    await ctx.send('Here is the link to the song you requested!!!')

    for items in range(len(music_list)):
        await ctx.send(music_list[items])
    # clear the list after sending links to avoid carry over
    music_list.clear()

# command to get album link
@bot.command(pass_context=True)
async def album(ctx, album_name: str):
    get_link(album_name, 'album', 'album')
    await ctx.send('Here is the link to the album you requested!!!')

    for items in range(len(music_list)):
        await ctx.send(music_list[items])
    music_list.clear()

#command to get artists based on genre input
@bot.command(pass_context=True)
async def genre(ctx, genre_name: str):
    get_link(genre_name, q='genre', info_type='artist')
    await ctx.send('Here are links to the top 3 artists in the genre you requested!!!')

    for items in range(len(music_list)):
        await ctx.send(music_list[items])
    music_list.clear()

bot.run(token)