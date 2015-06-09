import ConfigParser, re
from SlackBot import SlackBot

config = ConfigParser.RawConfigParser()
config.read('BuchBot.cfg')

SLACK_API_TOKEN = config.get('General', 'api_token')
SLACK_CHANNEL = config.get('General', 'slack_channel')
slack_channel_id = None

buch = SlackBot(SLACK_API_TOKEN)

def on_open(bot):
    global slack_channel_id
    for channel in bot.channels:
        if channel.name == SLACK_CHANNEL:
            slack_channel_id = channel.id
            break
    bot.say(slack_channel_id, 'HELLO CLASS!!!')

def on_message(bot, msg):
    if msg.channel == slack_channel_id:
        if re.search('bab(y|ies)', msg.text, re.I):
            bot.say(slack_channel_id, 'DELICIOUS!!!')
        elif re.search('(bathtub|monster truck tire)', msg.text, re.I):
            bot.say(slack_channel_id, "I'VE BEEN WAITING FOR THIS ALL DAY!!!")
        elif re.search('buchdawg', msg.text, re.I):
            bot.say(slack_channel_id, 'WHO LET THE BUCH OUT, WHO, WHO WHO, WHO WHO')
        elif re.search('cheeseburger', msg.text, re.I):
            bot.say(slack_channel_id, "A MAN'S GOTTA EAT!!!")
        elif re.search('child', msg.text, re.I):
            bot.say(slack_channel_id, 'CHILD?? WHERE???')
        elif re.search('electric', msg.text, re.I):
            bot.say(slack_channel_id, "IF YOU'RE GOOD, I'LL TELL YOU A STORY ABOUT ELECTRICITY!!!")
        elif re.search('fire drill', msg.text, re.I):
            bot.say(slack_channel_id, "CAN SOMEBODY CARRY ME?!?!")
        elif re.search('food', msg.text, re.I):
            bot.say(slack_channel_id, 'SOMEONE SAY FOOD?? I COULD EAT...')
        elif re.search('kinderwurst', msg.text, re.I):
            bot.say(slack_channel_id, "I'M GETTING HUNGRY!!!")
    
buch.add_event_listener('open', on_open)
buch.add_event_listener('message', on_message)
buch.run()
