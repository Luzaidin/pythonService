import configparser

# Config
def read_config():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config