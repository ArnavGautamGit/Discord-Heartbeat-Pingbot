#DHP.py

import discord
from discord.ext import commands, tasks
import os
import webserver

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
heartbeat_task = None
ping_message = "!soul online"  # Default message

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to maintain heartbeats')
    await bot.change_presence(activity=discord.Game(name="Keeping bots alive | !startping"))

@bot.command(name='startping')
async def start_ping(ctx, *, custom_message=None):
    global heartbeat_task, ping_message
    
    # Update ping message if provided
    if custom_message:
        ping_message = custom_message
        await ctx.send(f"Ping message set to: `{ping_message}`")
    else:
        await ctx.send(f"Using default ping message: `{ping_message}`")
    
    # Stop existing task if running
    if heartbeat_task and heartbeat_task.is_running():
        heartbeat_task.cancel()
        await ctx.send("Restarting ping task with new settings.")
    
    # Create new task that pings in the channel where command was used
    heartbeat_task = tasks.loop(seconds=60)(ping_bot)
    heartbeat_task.start(ctx.channel)
    
    await ctx.send(f"Started pinging every 60 seconds in this channel.")

@bot.command(name='stoping')
async def stop_ping(ctx):
    global heartbeat_task
    
    if heartbeat_task and heartbeat_task.is_running():
        heartbeat_task.cancel()
        await ctx.send("Stopped pinging.")
    else:
        await ctx.send("No active pinging to stop.")

async def ping_bot(channel):
    try:
        await channel.send(ping_message)
    except Exception as e:
        print(f'Error sending ping: {e}')

# Keep it alive before running the bot
webserver.keep_alive()
bot.run(os.environ['HEARTBEAT_TOKEN'])