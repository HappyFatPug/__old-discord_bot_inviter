import discord
from discord.ext import commands
from configparser import ConfigParser

config_file = 'set.ini'
config = ConfigParser()
config.read(config_file)
BOT_TOKEN = config['Bot']['token']

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print('Ready\n ----')

@client.event
async def on_message(message):
    print('message')

client.run(BOT_TOKEN)
