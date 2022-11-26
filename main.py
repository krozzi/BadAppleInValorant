import websocket
import rel
import ssl
import auth
import json

import sendmsg
import os, time

id_seen = []
commands = ['run']

def runapple(cid):
    f = open('jap2.txt', 'r', encoding='utf8')
    frame_raw = f.read()
    f.close()
    frames = frame_raw.split('SPLIT')
    init_time = time.time()
    while time.time() <= init_time + 218:
#         *22 - fill in whitespace @ start
        sendmsg.postNewChatMessage(cid, ("発"*22) + ": " + frames[int((time.time() - init_time) * 20)])

def on_message(ws, message):

    res = json.loads(message)
    juicy = res[2]

    if juicy.get("uri") == "/chat/v6/messages":
        message = juicy['data']['messages'][0]
        print(message)

        if message['id'] not in id_seen:
            id_seen.append(message['id'])
#             check if i sent it
            if message['puuid'] == 'ae32c0ca-3de3-5086-9c69-2d25c8f664fd' and str(message['body']).startswith('.'):
                args = str(message['body']).replace('.', '').split(' ')
                # print(f"User pushed cmd {args[0]} with args {args[1:]}")
                if args[0] in commands:

                    # no switch statements in py3.9 ㅠㅠ
                    if args[0] == 'run':
                        cid = args[1]
                        if cid == 'this':
                            runapple(message["cid"])
                        else:
                            sendmsg.postNewChatMessage(cid, 'bruh')


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Closed connection")


def on_open(ws):
    print("Opened connection")
    ws.send('[5,"OnJsonApiEvent_chat_v6_messages"]')


port = auth.getConfig().get("port")
password = auth.getConfig().get("password")
serv = f'wss://riot:{password}@127.0.0.1:{port}'

websocket.enableTrace(False)
ws = websocket.WebSocketApp(serv,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            header=auth.getHeaders())

ws.run_forever(dispatcher=rel,
               reconnect=5, sslopt={"cert_reqs": ssl.CERT_NONE})

rel.signal(2, rel.abort)
rel.dispatch()
