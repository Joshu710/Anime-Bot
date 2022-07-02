
import discord
from AniScrape import *

TOKEN = "insert token here"


client = discord.Client()
asking = False

@client.event
async def on_ready():
    print(f"We are logged in as {client.user}")


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")


    if message.author == client.user:
        return
    user_message = user_message.split(" ",1)

    # Displays the source of the bot profile picture
    if user_message[0].lower() == '!sauce':
        await message.channel.send('Kosaki Onodera from Nisekoi')
        return

    # Allows the user to search for anime
    if user_message[0].lower() == "!ani":
        await animeSearch(message,user_message[1])
        return
    
    # Informs the user how many bitches they have
    if user_message[0].lower() == "!bitches?":
        await message.channel.send("Ya got none my g")


@client.event
async def animeSearch(message, searchTerm):
    res = await get_results(searchTerm)
    mes = "```Search Result\n\n"
    for i in range(len(res)):
        mes += str(i+1) + ": " + res[i].title + "\n"
    mes += "\nSay the number for which you want to see more details (example \'1\')```"
    await message.channel.send(mes)

    def check(m):
        return m.channel == message.channel and m.author == message.author

    msg = await client.wait_for('message',check=check)

    myVal = str(msg.content).split(" ", 1)
    try:
        val = int(myVal[0]) - 1
        if val > len(res) - 1 or val < 0:
            await message.channel.send('Not a valid number, prompt cancelled')
        else:
            await get_embed(res[val], msg)
    except ValueError:
        await message.channel.send('Not a valid number, prompt cancelled')
    return


client.run(TOKEN)
