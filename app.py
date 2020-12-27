import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_url
import random

load_dotenv()


machine = TocMachine(
    states=["user", "op1", "run", "help","fsm","translate1","translate2","translate3"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "op1",
            "conditions": "sing_op1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "run",
            "conditions": "sing_run",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "help",
            "conditions": "help_me",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "fsm",
            "conditions": "show_fsm",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "translate1",
            "conditions": "go_to_translate1",
        },
        {
            "trigger": "advance",
            "source": "translate1",
            "dest": "translate2",
            "conditions": "go_to_translate2",
        },      
        {
            "trigger": "advance",
            "source": "translate2",
            "dest": "translate3",
            "conditions": "go_to_translate3",
        }, 
        {
            "trigger": "advance",
            "source": "translate3",
            "dest": "translate1",
            "conditions": "return_translate1",
        }, 
        {"trigger": "go_back", "source": ["op1", "run", "help","fsm","translate2","translate3"], "dest": "user"},
        {"trigger": "return_translate2", "source": "translate3", "dest": "translate2"},
        {"trigger": "return_translate1", "source": "translate3", "dest": "translate1"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False and machine.state == "user" :
            send_text_message(event.reply_token, "WRYYYYYYYY")
        elif response == False and machine.state == "translate1" :
            send_text_message(event.reply_token, "Choose a langeuage\n1.English\n2.Chinese\n3.Japanese\n4.Korean\n5.French\n6.German")
        #elif response == False and machine.state == "translate3" :
        #    send_text_message(event.reply_token, "Enter a string of text or\n[q]uit\n[s]elect language")


    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    
    os.environ["PATH"] += os.pathsep + 'D:\Anaconda3\envs\py37\Lib\site-packages\graphviz'
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")
    

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
