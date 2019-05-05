from configparser import ConfigParser
import asyncio


def get_member(channel, slug:str):
    try:
        int(slug)
    except ValueError:
        return None
    for member in channel.members:
        if member.discriminator == slug:
            return member


def save_dealer(channel, member, conf_file):
    ch_id = str(channel.id)
    mem_id = str(member.id)
    config = ConfigParser()
    config.read(conf_file)

    if not config.has_section(ch_id):
        config.add_section(ch_id)
    config[ch_id][mem_id] = 'True'
    with open(conf_file, 'w') as f:
        config.write(f)


def off_dealer(channel, member, conf_file):
    ch_id = str(channel.id)
    mem_id = str(member.id)
    config = ConfigParser()
    config.read(conf_file)

    if config.has_section(ch_id):
        if config.has_option(ch_id, mem_id):
            config[ch_id][mem_id] = 'False'
    with open(conf_file, 'w') as f:
        config.write(f)
