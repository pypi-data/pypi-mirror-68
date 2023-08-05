import configparser
from pathlib import Path
import os


class Config:
    def __init__(self, location=str(Path.home())):
        self.location = location

    def set_credentials(self, domain, api_key):
        config = configparser.ConfigParser()
        config['config'] = {
            'domain': domain,
            'api_key': api_key
        }
        with open(self.__config_filename(), 'w') as configfile:
            config.write(configfile)

    def get_credentials(self):
        config = configparser.ConfigParser()
        config.read(self.__config_filename())
        if 'config' in config.keys():
            return config['config']
        return None

    def __config_filename(self):
        return os.path.join(self.location, ".voice-transcriber")
