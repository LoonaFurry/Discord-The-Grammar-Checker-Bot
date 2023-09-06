import discord
from discord.ext import commands
from discord import Activity, ActivityType
import datetime
from textblob import TextBlob

intents = discord.Intents.all()
intents.typing = True  # Enable accessing typing events
intents.message_content = True  # Enable accessing message content
bot = commands.Bot(command_prefix='!', intents=intents)


statuses = [
    Activity(name='Checking Messages', type=ActivityType.playing),
    Activity(name='Grammer Checking', type=ActivityType.listening),
    Activity(name='Watching The Chat', type=ActivityType.watching)
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await update_presence()

async def update_presence():
    now = datetime.datetime.now()
    hour = now.hour

    if 6 <= hour < 12:  # Morning
        activity = statuses[0]
    elif 12 <= hour < 18:  # Afternoon
        activity = statuses[1]
    else:  # Evening/Night
        activity = statuses[2]

    await bot.change_presence(activity=activity)

@bot.event 
async def on_message(message):
    # Ignore bot messages
    if message.author == bot.user:
        return
        
    # Check grammar and spelling 
    text = TextBlob(message.content)
    corrections = text.correct()
    
    if text != corrections:
        
        # Send message back with corrections
        await message.channel.send(
            f"Here are some suggested corrections: {corrections}"
        )

bot.run("Your-Discord-Bot-Token")
