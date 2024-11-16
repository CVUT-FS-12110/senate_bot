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
intents.messages = True
bot = discord.Client(intents=intents)

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
        query = message.content[len('!ask'):].strip()
        if query:
            try:
                # Use the Groq API to get a response
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": query,
                        }
                    ],
                    model="llama3-8b-8192",
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
