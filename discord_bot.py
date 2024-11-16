import os
import discord
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Set up Groq API client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Set up Discord client
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Load the minutes from a text file or environment variable
with open("minutes.txt", "r") as file:
    senate_minutes = file.read()

# Load additional data (list of senators and their program)
with open("senators.txt", "r") as file:
    senators_list = file.read()

with open("programmes.txt", "r") as file:
    programmes = file.read()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # If the message starts with '!ask', process it
    if message.content.startswith('!ask'):
        print(f"Received message: {message.content}")
        query = message.content[len('!ask'):].strip()
        if query:
            try:
                # Use the Groq API to get a response, including the senate minutes, list of senators, and programmes as context
                context = ("You have access to the following senate minutes: " + senate_minutes +
                           "\n\nList of senators: " + senators_list +
                           "\n\nSenators' programmes: " + programmes)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": context,
                        },
                        {
                            "role": "user",
                            "content": query,
                        }
                    ],
                    model="llama-3.1-8b-instant",
                    max_tokens=500,
                    temperature=0.1,
                )
                
                response = chat_completion.choices[0].message.content
                await message.channel.send(response)
            except Exception as e:
                await message.channel.send(f"Error: {str(e)}")
        else:
            await message.channel.send("Please provide a question after !ask.")

# Run the bot
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))