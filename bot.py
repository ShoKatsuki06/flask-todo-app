#import LineB
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

LINE_ACCESS_TOKEN= "Xm/qqqPXcmUHPfCBqrnT2xmHF3NkL65iqonu85Mxm5B8f1YqwIppIhRBMWRL3iBhbnzcETKXe6wzaOWxdx8tY5HAw738Mm3uPz63eCR9uwVD+JkzSl6aQhghtwj10sa0yfVEhwnUHHuXkf07zUMesQdB04t89/1O/w1cDnyilFU=" # ラインアクセストークン
LINE_USER_ID= "Ueaa310a45e9e48e0109b2025c07e91e4" # ライン

# LINE APIを定義。引数にアクセストークンを与える。
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

text_message ="いき杉乃井ホテル"

def text(text_message):

  try:
    # ラインユーザIDは配列で指定する。
    line_bot_api.multicast(
    [LINE_USER_ID], TextSendMessage(text=text_message))
  except LineBotApiError as e:
    # エラーが起こり送信できなかった場合
    print(e)

text(text_message)
