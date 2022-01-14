import requests
from decouple import config
import json

def SendMessage():
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config('SLACK_TOKEN')
    }
    
    msg = {
        'channel': 'C02TVSQ9XML',
        'attachments': [
            {
                'mrkdwn_in': ['text'],
                'color': '#000000',
                'title': 'MyTest',
                'footer': 'FLO',
                'footer_icon': 'https://www.music-flo.com/favicon.ico'
            }
        ]
    }
    
    res = requests.post('https://slack.com/api/chat.postMessage', 
        headers = headers, 
        data = json.dumps(msg)
    )
    
    print (res.text);