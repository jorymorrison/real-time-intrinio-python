import websocket
import thread
import time
import requests
import base64
import json
import sys
import os
from requests.auth import HTTPBasicAuth

try:
    print "Using Ticker: " + str(sys.argv[1])
except:
    print "Please include ticker as first argument"
    sys.exit()

auth_url = "https://realtime.intrinio.com/auth";
r=requests.get(auth_url, headers={"Authorization": "Basic %s" % base64.b64encode(os.environ['INTRINIO_USER'] + ":" + os.environ['INTRINIO_PASSWORD'])})

socket_target = "wss://realtime.intrinio.com/socket/websocket?token=%s" % (r.text)

def on_message(ws, message):
    try:
        result = json.loads(message)
        print result["payload"]
    except:
        print message

def on_error(ws, error):
    print "###ERROR### " + error

def on_close(ws):
    print "###CONNECTION CLOSED###"

def on_open(ws):
    def run(*args):
        security = "iex:securities:" + str(sys.argv[1]).upper()
        message = json.dumps({"topic": security,"event": "phx_join","payload": {},"ref": "1"})
        ws.send(message)
    thread.start_new_thread(run, ())


websocket.enableTrace(True)
ws = websocket.WebSocketApp(socket_target, on_message = on_message, on_error = on_error, on_close = on_close)
ws.on_open = on_open
ws.run_forever()