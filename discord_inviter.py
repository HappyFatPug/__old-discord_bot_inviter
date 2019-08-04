import discord
from discord.ext import commands
from configparser import ConfigParser
import asyncio
from utils import save_dealer, get_member, off_dealer, dealer_check
from utils import parse_message_args


config_file = 'set.ini'
config = ConfigParser()
config.read(config_file)
BOT_TOKEN = config['Bot']['token']

client = commands.Bot(command_prefix='.')

INVITE_LIST = {}
MAX_INVITES = 20
MAX_TIMOUT = 300
MIN_TIMOUT = 10


@client.event
async def on_ready():
    print('Ready')
    print('-------\n')


@client.event
async def on_message(message):
    if message.channel.id in INVITE_LIST and not message.author.bot:
        callback_channel = INVITE_LIST[message.channel.id].get(
            'callback', None
        )
        if callback_channel:
            await callback_channel.send(
                f'{message.author.mention} says: {message.content}'
            )
        await message.channel.send('I am done')
        INVITE_LIST.pop(message.channel.id)
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


@client.command(name='dealer')
async def set_dealer(ctx, *targets):
    '''
    gives "dealer" abilities for provided members
    '''
    sender = ctx.message.author
    if await client.is_owner(sender):
        print('dealer add command')
        channel = ctx.channel
        for slug in targets:
            member = get_member(channel, slug)
            if member:
                save_dealer(channel, member, config_file)
                await ctx.send(f'member {member.mention} now has some abilities')


@client.command(name='rm_dealer')
async def remove_dealer(ctx, *targets):
    sender = ctx.message.author
    if await client.is_owner(sender):
        print('dealer off command')
        channel = ctx.channel
        for slug in targets:
            member = get_member(channel, slug)
            if member:
                off_dealer(channel, member, config_file)
                await ctx.send(f'member {member.mention} removed from dealers list')


@client.command(name='invite')
async def invite_member(ctx, *args):
    channel = ctx.channel
    sender = ctx.message.author
    members, pars = parse_message_args(*args)

    if pars[0] > MAX_INVITES:
        pars[0] = MAX_INVITES
    if pars[1] > MAX_TIMOUT:
        pars[1] = MAX_TIMOUT
    if pars[1] < MIN_TIMOUT:
        pars[1] = MIN_TIMOUT

    print('members: ', members)
    print('pars: ', pars)

    if dealer_check(channel, sender, config_file):

        for mem_slug in members:
            target = get_member(channel, mem_slug)

            if not target.dm_channel:
                await target.create_dm()
            p_channel = target.dm_channel

            try:
                await inviter(p_channel, *pars, callback=ctx.channel)

            except discord.errors.Forbidden:
                await ctx.send(f'{target.mention} have blocked me!')


async def inviter(p_channel, count=10, timeout=30, callback=None):

    INVITE_LIST[p_channel.id] = {
        'count': count,
        'callback': callback
    }

    while INVITE_LIST.get(p_channel.id, None):
        counter = INVITE_LIST[p_channel.id]['count']
        await p_channel.send(
            'hello number {}, timeout = {} sec'.format(counter, timeout)
        )
        try:

            if counter <= 1:
                INVITE_LIST.pop(p_channel.id)
                await p_channel.send('I am done')
                return None
            INVITE_LIST[p_channel.id]['count'] -= 1
        except KeyError:
            return None
        await asyncio.sleep(timeout)


client.run(BOT_TOKEN)
