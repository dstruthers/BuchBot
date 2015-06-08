import ConfigParser, json, re, urllib2, websocket

config = ConfigParser.RawConfigParser()
config.read('BuchBot.cfg')

SLACK_API_TOKEN = config.get('General', 'api_token')
SLACK_API_BASE = config.get('General', 'api_base_uri')
SLACK_CHANNEL = config.get('General', 'slack_channel')

def rtm_call(endpoint, **args):
    '''Make Slack API call via RTM protocol'''
    params = ''
    for key in args:
        if params: params += '&'
        params += key + '=' + args[key]
    url = SLACK_API_BASE + endpoint + '?' + params
    result = json.loads(urllib2.urlopen(url).read())
    return result

channels = {}
users = {}
channel_id = ''
self_user_id = ''
msg_id = 0

start_result = rtm_call('rtm.start', token=SLACK_API_TOKEN)
if not start_result['ok']:
    print 'Could not initiate RTM session!'
    exit(1)

self_user_id = start_result['self']['id']

for channel in start_result['channels']:
    channels[channel['id']] = channel['name']
    if channel['name'] == SLACK_CHANNEL:
        channel_id = channel['id']

for user in start_result['users']:
    users[user['id']] = user['name']
    
# WebSocket callbacks
def on_message(ws, message):
    print message
    msg = json.loads(message)
    if msg['type'] == 'presence_change':
        if msg['presence'] == 'active':
            user_name = users[msg['user']]
            if user_name != 'mr_buchanan':
                #say(ws, 'HELLO ' + user_name + '!')
                print "Presence change:", user_name
    elif msg['type'] == 'message':
        if msg['channel'] == channel_id:
            if re.search('bab(y|ies)', msg['text'], re.I):
                say(ws, 'DELICIOUS!!!')
            elif re.search('(bathtub|monster truck tire)', msg['text'], re.I):
                say(ws, "I'VE BEEN WAITING FOR THIS ALL DAY!!!")
            elif re.search('cheeseburger', msg['text'], re.I):
                say(ws, "A MAN'S GOTTA EAT!!!")
            elif re.search('child', msg['text'], re.I):
                say(ws, 'CHILD?? WHERE???')
            elif re.search('electricity', msg['text'], re.I):
                say(ws, "IF YOU'RE GOOD, I'LL TELL YOU A STORY ABOUT ELECTRICITY!!!")
            elif re.search('food', msg['text'], re.I):
                say(ws, 'SOMEONE SAY FOOD?? I COULD EAT...')
            elif re.search('kinderwurst', msg['text'], re.I):
                say(ws, "I'M GETTING HUNGRY!!!")

def on_error(ws, error):
    print 'Error: ' + error

def on_close(ws):
    say(ws, 'GOOD-BYE!!!')

def on_open(ws):
    say(ws, 'HELLO CLASS!')

def next_id():
    global msg_id
    msg_id += 1
    return msg_id
    
def say(ws, text):
    msg = json.dumps({'id': next_id(), 'type': 'message', 'channel': channel_id, 'text': text})
    ws.send(msg)
    
websocket.enableTrace(True)
ws = websocket.WebSocketApp(start_result['url'],
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            on_open = on_open)

ws.run_forever()

