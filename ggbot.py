import discord
from discord.ext import commands
import os
import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='@', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ggbot(ctx):
    await ctx.send('Hello!')

@bot.command()
async def upload(ctx):
    video_directory = "/home/iwnl/Videos"
    
    try:
        files = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if os.path.isfile(os.path.join(video_directory, f))]
        
        if not files:
            await ctx.send("No files found in the specified directory.")
            return
        
        latest_file = max(files, key=os.path.getmtime)
        
        file_name = os.path.basename(latest_file)
        file_size = os.path.getsize(latest_file)
        
        if file_size > 8 * 1024 * 1024:  # 8MB in bytes
            await ctx.send(f"The file '{file_name}' is too large to upload (size: {file_size / (1024 * 1024):.2f} MB). Maximum size is 8MB.")
            return
        
        with open(latest_file, 'rb') as file:
            await ctx.send(f"Uploading the latest file: {file_name}", file=discord.File(file, filename=file_name))
        
        await ctx.send(f"File '{file_name}' has been uploaded successfully.")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

bot.run('@token')