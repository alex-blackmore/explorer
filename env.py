import os
import re

def load_env(filename):
    with open(filename) as file:
        for line in file.read().strip().split("\n"):
            if re.match(r'[a-zA-Z_]+="[^"]*"', line):
                name, value = line.split("=")
                value = value.strip('"')
                os.environ[name] = value

def read_env(name):
    return os.environ[name]