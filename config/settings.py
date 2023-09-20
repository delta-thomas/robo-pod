import configparser
import os

config = configparser.ConfigParser()

def load_config():
    if os.path.exists('config.ini'):
        config.read('config.ini')
    else:
        print("config.ini not found!")
        exit()

load_config()

def save_config(section, key, value):
    config.set(section, key, value)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get_openai_config():
    return {
        "API_KEY": config.get('OpenAI', 'API_KEY'),
        "MODEL": config.get('OpenAI', 'MODEL'),
        "MAX_TOKENS": config.getint('OpenAI', 'MAX_TOKENS'),
        "TEMPERATURE": config.getfloat('OpenAI', 'TEMPERATURE')
    }

def get_elevenlabs_config():
    return {
        "API_KEY": config.get('ElevenLabs', 'API_KEY'),
        "VOICE_ID": config.get('ElevenLabs', 'VOICE_ID')
    }

def get_texts_config():
    return {
        "prompttweak": config.get('Texts', 'prompttweak'),
        "welcome": config.get('Texts', 'welcome')
    }
