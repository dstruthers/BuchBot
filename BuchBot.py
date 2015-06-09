import ConfigParser, json, re
from SlackBot import SlackBot

slack_channel_id = None
keyword_mappings = {}

def load_config():
    '''Load bot options from config file'''
    global slack_api_token, slack_channel, keyword_file, send_greetings
    config = ConfigParser.RawConfigParser()
    config.read('BuchBot.cfg')

    slack_api_token = config.get('General', 'api_token')
    slack_channel = config.get('General', 'slack_channel')
    keyword_file = config.get('General', 'keyword_file')
    send_greetings = config.getboolean('General', 'greet_people')
    
def load_keywords():
    '''Load keyword matching patterns from JSON file'''
    global keyword_mappings
    f = open(keyword_file, 'r')
    keyword_mappings = json.loads(f.read())
    f.close()

def on_open(bot):
    global slack_channel_id
    for channel in bot.channels:
        if channel.name == slack_channel:
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
            load_config()
            load_keywords()
            bot.say(slack_channel_id, 'OKAY!!!')

def greet_people(bot, msg):
    if not send_greetings:
        return
    
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

load_config()

buch = SlackBot(slack_api_token)
buch.show_typing = True
buch.add_event_listener('open', on_open)
buch.add_event_listener('message', listen_for_keywords)
buch.add_event_listener('message', listen_for_commands)
buch.add_event_listener('presence_change', greet_people)

buch.run()
