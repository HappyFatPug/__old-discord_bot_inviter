import discord
from discord.ext import commands
from configparser import ConfigParser

config_file = 'set.ini'
config = ConfigParser()
config.read(config_file)
BOT_TOKEN = config['Bot']['token']

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Ready\n ----')

@client.event
async def on_message(message):
    print('message')
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    print(f'{member} has joined')

@client.event
async def on_member_remove(member):
    print(f'{member} has left')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

client.run(BOT_TOKEN)
