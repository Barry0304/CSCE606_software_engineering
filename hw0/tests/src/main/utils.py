import json, re
import shlex

def load_config():
    with open('src/main/config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

def parse_args(args):
    pairs = args.strip().split('="')
    keys = []
    values = []
    keys.append(pairs[0])
    for pair in pairs[1:-1]:
        value, key = pair.strip().rsplit('" ', 1)
        values.append(value.strip('"'))
        keys.append(key.strip().strip('"'))
    values.append(pairs[-1].strip().strip('"'))
    return dict(zip(keys, values))

def is_valid_username(username):
    return re.match("^[a-zA-Z0-9_]+$", username) is not None