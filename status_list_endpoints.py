# The simple is just the beginning to open your mind of how everything works in a simple way. "GuiDeLuccaDev"

''' A python script to take the status of numerous 
    endpoints asynchronously and return it in a dictionary. '''

import urllib.request as urllib
import threading

responses = {}

# A list of endpoints

list_endpoints = [
    "http://www.google.com/",
    "http://www.youtube.com/"
    ]

opener = urllib.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def response(url):
    try:
        with opener.open(url) as res:
            responses[url] = res.getcode()
            return responses
    except:
        responses[url] = 400
        return responses

def execute():
    for url in list_endpoints:
        threading.Thread(target=response,args=(url,)).start()

    while threading.active_count() > 1:
        pass
    
    return responses

status = execute()
print(status)