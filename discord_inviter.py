import discord
from discord.ext import commands
from configparser import ConfigParser
import asyncio

config_file = 'set.ini'
config = ConfigParser()
config.read(config_file)
BOT_TOKEN = config['Bot']['token']

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Ready')
    print('-------\n')

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

@client.command()
async def invite(ctx):
    print(ctx.message)
    author = ctx.author
    if not author.dm_channel:
        print('there is no dm channel with this folk, creating one...')
        await author.create_dm()
        print('done')
    p_channel = author.dm_channel
    print('pm_channel: ', p_channel)
    try:
        await p_channel.send('hello')
        await ctx.send(f'{author.mention} check direct')
    except discord.errors.Forbidden:
        await ctx.send(f'{author.mention} have blocked me!')


@client.command(name='clear')
async def clear_bot_messages(ctx):
    if await client.is_owner(ctx.author):
        mess = list()
        async with ctx.typing():
            async for message in ctx.history(limit=1000):
                if message.author == client.user:
                    mess.append(message)
            await ctx.channel.delete_messages(mess)
            new_mess = await ctx.send('done')
        await asyncio.sleep(3)
        await new_mess.delete()

client.run(BOT_TOKEN)
