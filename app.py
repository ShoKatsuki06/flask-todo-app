from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
import datetime
import mysql.connector
import pymysql.cursors
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
import schedule
import time
import os


app = Flask(__name__)

LINE_ACCESS_TOKEN= "Xm/qqqPXcmUHPfCBqrnT2xmHF3NkL65iqonu85Mxm5B8f1YqwIppIhRBMWRL3iBhbnzcETKXe6wzaOWxdx8tY5HAw738Mm3uPz63eCR9uwVD+JkzSl6aQhghtwj10sa0yfVEhwnUHHuXkf07zUMesQdB04t89/1O/w1cDnyilFU=" # ラインアクセストークン
LINE_USER_ID= "Ueaa310a45e9e48e0109b2025c07e91e4" # ライン
# LINE APIを定義。引数にアクセストークンを与える。
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

def sendText(text_message):
   try:
    # ラインユーザIDは配列で指定する。
    line_bot_api.multicast(
    [LINE_USER_ID], TextSendMessage(text=text_message))
   except LineBotApiError as e:
    # エラーが起こり送信できなかった場合
    print(e)

def dbstart():# データベースの接続設定]
     dns = {
    'user': 'b7933a15d37230',
    'host': 'us-cdbr-east-04.cleardb.com', # 各自設定
    'password': 'da33b80d', # 各自設定
    'database': 'heroku_fab7e2e9408003b', # 各自設定
    'port': '3306'}
     db = mysql.connector.connect(**dns)
     return db

def selctcommand(db,sql):
     cursor = db.cursor(buffered = True)
     cursor.execute(sql)#上限は10個
     rows = cursor.fetchall()
     cursor.close()
     db.close()
     return rows

def selctcommand1(db,sql,id):
     cursor = db.cursor(buffered = True)
     cursor.execute(sql,id)#上限は10個
     rows = cursor.fetchone()
     cursor.close()
     db.close()
     return rows

def selctcommand2(db,sql,id):
     cursor = db.cursor(buffered = True)
     cursor.execute(sql,id)#上限は10個
     rows = cursor.fetchall()
     cursor.close()
     db.close()
     return rows

def sqlcommand(db,sql):
    db = mysql.connector.connect(**dns)
    cursor = db.cursor(buffered = True)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

def sqlcommand1(db,sql,id):#値の指定がある場合はこちらのメソッドを使います
    cursor = db.cursor(buffered = True)
    cursor.execute(sql,id)
    db.commit()
    cursor.close()
    db.close()

#完成数の初期化
#date = datetime.date.today()
#sqlcommand1(dbstart(),'INSERT INTO todofinish (day,noa) VALUES (%s, %s);',(date,0))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
#メインメニュー
@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "GET":
       db = dbstart()
       sql = 'SELECT * FROM todo LIMIT 10;'
       rows = selctcommand(db,sql)
       return render_template("index.html", posts = rows )
    else:#登録
       title = request.form.get('title')
       detail = request.form.get('detail')
       due = request.form.get('due')
       print(due)
       sql = "INSERT INTO todo (title,detail,due ) VALUES (%s, %s, %s);"
       sqlcommand1(dbstart(),sql,(title,detail,due))
       sendText("TODOを登録しました\r\n{},{},{}".format(title,detail,due))
       return redirect('/')

#作成画面
@app.route("/create")
def create():
      return render_template("create.html")
#詳細画面
@app.route("/detail/<int:id>")
def read(id):
    db = dbstart()
    row = selctcommand1(db,'SELECT * FROM todo WHERE id = %s LIMIT 1',(id,))
    return render_template("detail.html", post = row)
#削除
@app.route("/delete/<int:id>")
def delete(id):
    sqlcommand1(dbstart(),'DELETE FROM todo WHERE id= %s',(id,))
    return redirect("/")
#完了
@app.route("/finish/<int:id>")
def finish(id):
    date = datetime.date.today()
    sqlcommand1(dbstart(),'DELETE FROM todo WHERE id= %s',(id,))
    print(date)
    num = selctcommand1(dbstart(),'SELECT * FROM todofinish WHERE day = %s LIMIT 1;',(date,))
    sum = num[1]+1
    sqlcommand1(dbstart(),'UPDATE todofinish SET noa = %s WHERE day = %s;',(sum,date))
    #glaph()
    import glaph
    return redirect("/")
#編集""
@app.route("/update/<int:id>",methods = ["GET","POST"])
def update(id):
    row = selctcommand1(dbstart(),'SELECT * FROM todo WHERE id = %s',(id,))
    print(row)
    if request.method =="GET":
        return render_template("update.html",post=row)
    else:
        title = request.form.get("title")
        detail = request.form.get("detail")
        due = request.form.get("due")
        sqlcommand1(dbstart(),'UPDATE todo SET title = %s,detail = %s,due = %s WHERE id= %s',(title,detail,due,id))
        return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
