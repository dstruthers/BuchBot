import ConfigParser, json, re
from SlackBot import SlackBot

config = ConfigParser.RawConfigParser()
config.read('BuchBot.cfg')

SLACK_API_TOKEN = config.get('General', 'api_token')
SLACK_CHANNEL = config.get('General', 'slack_channel')
KEYWORD_FILE = config.get('General', 'keyword_file')
SEND_GREETINGS = config.getboolean('General', 'greet_people')

slack_channel_id = None
keyword_mappings = {}

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

def listen_for_keywords(bot, msg):
    global keyword_mappings
    if msg.channel == slack_channel_id:
        if keyword_mappings == {}:
            load_keywords()
            
        for pattern in keyword_mappings:
            if re.search(pattern, msg.text, re.I):
                bot.say(slack_channel_id, keyword_mappings[pattern])
                break

def listen_for_commands(bot, msg):
    if msg.channel == slack_channel_id:
        if msg.text == '!reload':
            load_keywords()
            bot.say(slack_channel_id, 'OKAY!!!')

def greet_people(bot, msg):
    if msg.user == bot.user_id:
        return
    
    for user in bot.users:
        if user.id == msg.user:
            break
        
    if msg.presence == 'active':
        if user.presence != msg.presence:
            user.presence = 'active'
            bot.say(slack_channel_id, 'HELLO ' + user.username + '!!!')
    else:
        user.presence = msg.presence
            
buch = SlackBot(SLACK_API_TOKEN)
buch.show_typing = True
buch.add_event_listener('open', on_open)
buch.add_event_listener('message', listen_for_keywords)
buch.add_event_listener('message', listen_for_commands)
if SEND_GREETINGS:
    buch.add_event_listener('presence_change', greet_people)

buch.run()
