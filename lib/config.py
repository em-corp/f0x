__all__ = []

import configparser


class ConfigManager:
    config = None
    
    def getConfig():
        if not ConfigManager.config:
            ConfigManager.config = ConfigManager.Configuration()
        return ConfigManager.config

    def load(cfile):
        conf = configparser.ConfigParser()
        conf.read(cfile)
        
        for s in conf.sections():
            for k in conf[s]:
                ConfigManager.getConfig().set(k, conf[s].get(k))

        return ConfigManager.getConfig()

    class Configuration():

        def __init__(self):
            self.properties = {}

        def get(self, key):
            if key in self.properties.keys():
                return self.properties[key]
            else:
                raise self.NoSuchKeyException("No such key `{}` found"
                                              .format(key))

        def set(self, key, value):
            self.properties[key] = value

        def getKeys(self):
            return self.properties.keys()

        class NoSuchKeyException(Exception):
            def __init__(self, message):
                super().__init__(message)
