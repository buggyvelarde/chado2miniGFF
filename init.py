import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(sys.path[0] + '/config.ini')

host=config.get('Connection', 'host')
database=config.get('Connection', 'database')
user=config.get('Connection', 'user')
password=config.get('Connection', 'password')
