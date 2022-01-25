# Discord-Bots
This project was made just as a way to test and improve my knowledge in both Python as well as accessing various APIs and their features while having some fun at the same time by applying
said features to Discord bots.
I've made 4 bots as of now, and I tried to have a similar logic flow for each. 
That way, even though they all were designed with different purposes in mind, the idea of how each works is still relatively straightforward.

### Daily Wisdom Bot
This bot was the first I made, and it was created from what I read/viewed from various tutorials. It is the simplest of the 4 and accesses ZenQuotes.io's API,
which was rather simple since they don't require a key to use. Being the first one, it is also the least complex in terms of approach, 
as it doesn't use commands to function, but rather the "on_message" event, which has led to a few problems, but nothing program breaking. 
I may change it from event handling to command handling like the rest at some point, which is the beauty of making more complex programs with each iteration of bots I have,
but as mentioned it still works with the same logic, just not as efficiently or easy on the eyes in terms of readability.
This bot also detects when certain keywords are used in the messages being sent between people in the server, and will respond with custom messages I made as an attempt to lighten the mood.

### Youtube Bot
This was my second bot, and my first fully independent attempt to perform what I wanted to accomplish. The general idea of this bot is to access Google's API in order to pull the
necessary Youtube data that was requested. It will perform a Youtube search based on the topic it is given and will display by default 5 videos related to that topic.
The more advanced step in progression for this bot was the attempt to connect it to the voice channel in order to play the audio from the video link given to it. 
This was successful, but it is far from perfect, as one issue I've noticed was it will sometimes stop working if there's an attempt to play a second video after playing the first,
and I believe it may be a TimeoutException, but I'm not entirely sure where or how to catch it currently. This was the only real issue I've noticed with this bot though, as it 
does play, pause, resume, and stop audio as intended, on top of accurately searching for topics inputted. 

### Spotify Bot
This is the third bot created. This one was rather easy to make compared to the Youtube Bot, and I want to believe it was due to the trial and error I came across making the Youtube
Bot turning into avoided mistakes this time around. This bot uses the Spotify API to retrieve songs, albums, and artists for users. 
The teaching aspect of this bot was to improve the search function of the Youtube Bot by making it more advanced and cohesive by parsing the JSON data that Spotify returns and making
it as accurate as I can. There was somewhat of a negligible problem when it came to using the search command, as if there were multiple songs with the same title as the one given, it
will return the most popular one from what I can tell, and although this is a naming issue rather than a bug, it can still be an inconvenience that can be fixed by just asking for the
artist after the name of the song is given, which opens up further parsing of the API data. 

### Meme Bot
This was my final bot as of now, and it came as a derivation from my initial attempt of creating an image search bot. Using GIPHY's API, this bot has the ability to search for 
GIFs based on topics provided, as well as find trending and random GIFs, which was the next area I wanted to learn. An idea given that I may attempt at some point down the line
is to have the bot make custom memes based on the image provided, which will let me learn further about image manipulation by doing it.
