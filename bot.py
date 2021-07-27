from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector
import pymysql.cursors
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
import schedule
import time
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

LINE_ACCESS_TOKEN= "Xm/qqqPXcmUHPfCBqrnT2xmHF3NkL65iqonu85Mxm5B8f1YqwIppIhRBMWRL3iBhbnzcETKXe6wzaOWxdx8tY5HAw738Mm3uPz63eCR9uwVD+JkzSl6aQhghtwj10sa0yfVEhwnUHHuXkf07zUMesQdB04t89/1O/w1cDnyilFU=" # ラインアクセストークン
LINE_USER_ID= "Ueaa310a45e9e48e0109b2025c07e91e4" # ライン

# LINE APIを定義。引数にアクセストークンを与える。
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

# データベースの接続設定
dns = {
    'user': 'b7933a15d37230',
    'host': 'us-cdbr-east-04.cleardb.com', # 各自設定
    'password': 'da33b80d', # 各自設定
    'database': 'heroku_fab7e2e9408003b', # 各自設定
    'port': '3306'
}
#db = MySQL(**dns)
db = mysql.connector.connect(**dns)

def a(id,text_message):
    try:
      to = id
      line_bot_api.push_message(to, TextSendMessage(text=text_message))
    except LineBotApiError as e:
      print(e)

if db.is_connected():
    print("データベースへの接続が成功しました。")
else:
    print("データベースへの接続が失敗しました。")
    exit(1)

cursor = db.cursor(buffered=True)
cursor.execute("USE heroku_fab7e2e9408003b")
db.commit()
sql = 'SELECT * FROM dbuser'
db.ping(reconnect=True)
cursor.execute(sql)
users = cursor.fetchall()
db.commit()

for user in users:
    userid = user[3]
    db.ping(reconnect=True)
    cursor.execute('SELECT * FROM todo WHERE (userid = %s) ',(userid,))
    row = cursor.fetchall()
    db.commit()

    text_message = ("あなたの残っているTodoは\r\n----------------\r\n")
    #Todoの書き出し
    for r in row :
        rm = (r[1]+","+r[2]+","+str(r[3]))
        rmessage = ("{}\r\n----------------\r\n".format(rm))
        text_message = text_message + rmessage
    #ラインで送るやつのメソッド定義
    text_message = text_message + "です"

    a(userid,text_message)


    #送信
