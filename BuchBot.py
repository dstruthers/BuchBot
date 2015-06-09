import ConfigParser, json, re
from SlackBot import SlackBot

config = ConfigParser.RawConfigParser()
config.read('BuchBot.cfg')

SLACK_API_TOKEN = config.get('General', 'api_token')
SLACK_CHANNEL = config.get('General', 'slack_channel')
KEYWORD_FILE = config.get('General', 'keyword_file')

slack_channel_id = None
keyword_mappings = {}

buch = SlackBot(SLACK_API_TOKEN)

def load_keywords():
    global keyword_mappings
    f = open(KEYWORD_FILE, 'r')
    keyword_mappings = json.loads(f.read())
    f.close()

def on_open(bot):
    global slack_channel_id
    for channel in bot.channels:
        if channel.name == SLACK_CHANNEL:
            slack_channel_id = channel.id
            break
    bot.say(slack_channel_id, 'HELLO CLASS!!!')

def on_message(bot, msg):
    global keyword_mappings
    if msg.channel == slack_channel_id:
        if keyword_mappings == {}:
            load_keywords()
            
        for pattern in keyword_mappings:
            if re.search(pattern, msg.text, re.I):
                bot.say(slack_channel_id, keyword_mappings[pattern])
    
buch.add_event_listener('open', on_open)
buch.add_event_listener('message', on_message)
buch.run()
