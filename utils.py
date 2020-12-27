import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"



def send_image_url(id, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    image_message = ImageSendMessage(original_content_url=img_url,preview_image_url=img_url)
    line_bot_api.reply_message(id, image_message)

    return "OK"

def send_video_url(id, video_url):
    line_bot_api = LineBotApi(channel_access_token)
    video_message = VideoSendMessage(original_content_url=video_url, preview_image_url=video_url)
    line_bot_api.reply_message(id, video_message)

    return "OK"


"""
def send_button_message(id, text, buttons):
    pass
"""
