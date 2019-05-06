from configparser import ConfigParser


def dealer_check(channel, member, config_file):
    ch_id = str(channel.id)
    mem_id = str(member.id)
    config = ConfigParser()
    config.read(config_file)

    if config.getboolean(ch_id, mem_id):
        return True
    return False



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


def parse_message_args(*args):
    members = []
    pars = []
    for arg in args:
        # print(arg)
        # print(type(arg))
        if arg.startswith('$'):
            pars.append(int(arg[1:]))
        else:
            members.append(arg)
    return members, pars


# @dealer
def check_func(a, b):
    print(a)
    print(b)
    return 'hello'

if __name__ == '__main__':
    # check_func('a', 'b')
    res = parse_message_args('1111', '0111', '2432', '$333', '$228')
    print(res)
