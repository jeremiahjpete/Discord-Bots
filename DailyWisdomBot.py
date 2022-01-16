import discord
import os
import requests
import json
import random
from replit import db
from dotenv import load_dotenv
#from keep_bot_alive import keep_bot_alive

client = discord.Client()

sad_words = [
    "sad", "miserable", "depressed", "depressing", "lonely", "angry", "upset",
    "lonesome", "tired"
]

encourage_list = [
    "Cheer up!", "It'll get better I promise!",
    "Keep it up you can do it I know you can!",
    "I may just be a bot, but I want you to know my creator gave me the ability to care, which I do!!!",
    "Like Tupac said, 'Keep ya head up'!"
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    # retrieve the quote using key 'q'
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def update_encourage(encourage_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encourage_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encourage_message]


def delete_encourage(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


def delete_All():
    encouragements = db["encouragements"]
    for index in encouragements:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:  # ignore messages from self
        return

    msg = message.content

    if msg.startswith('$hello'):
        await message.channel.send('Hello! I am DailyWisdomBot!')

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = encourage_list
        if "encouragements" in db.keys():
            options.extend(db["encouragements"])

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith('$new'):
        encourage_message = msg.split("$new ", 1)[1]
        update_encourage(encourage_message)
        await message.channel.send(
            "New encouragement added. Thanks for the material!")

    if msg.startswith('$del'):
        encouragements = []
        if "encouragements" in db.keys():
            #index = int(msg.split("$del", 1)[1])
            index = 0
            delete_encourage(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith('$removeAll'):
        encouragements = []
        if "encouragements" in db.keys():
          delete_All()
          encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = "false"
            await message.channel.send("Responding is off.")

#keep_bot_alive()
# retrieve token from .env file
load_dotenv()
token = os.getenv("discordBotToken")
client.run(token)
