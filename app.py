from flask import Flask,render_template,request,redirect,url_for,session
from datetime import datetime
import datetime
import mysql.connector
import pymysql.cursors
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError,LineBotApiError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,CarouselTemplate, CarouselColumn,ButtonsTemplate,MessageAction)
import schedule
import usergragh
import time
import news
import os


app = Flask(__name__)
app.secret_key = 'hogehoge'

LINE_ACCESS_TOKEN= "Xm/qqqPXcmUHPfCBqrnT2xmHF3NkL65iqonu85Mxm5B8f1YqwIppIhRBMWRL3iBhbnzcETKXe6wzaOWxdx8tY5HAw738Mm3uPz63eCR9uwVD+JkzSl6aQhghtwj10sa0yfVEhwnUHHuXkf07zUMesQdB04t89/1O/w1cDnyilFU=" # ラインアクセストークン
LINE_USER_ID= "Ueaa310a45e9e48e0109b2025c07e91e4" # ライン
YOUR_CHANNEL_SECRET = "9ed08732e0a51e53454e2b4a2ef91207"
# LINE APIを定義。引数にアクセストークンを与える。
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def sendText(id,text_message):
   try:
    # ラインユーザIDは配列で指定する。
    line_bot_api.multicast(
    [id], TextSendMessage(text=text_message))
   except LineBotApiError as e:
    # エラーが起こり送信できなかった場合
    redirect('/')

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

#LINEの送信部分
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    status_msg = profile.status_message
    if status_msg != "None":
        # LINEに登録されているstatus_messageが空の場合は、"なし"という文字列を代わりの値とする
        status_msg = "なし"

    messages = TemplateSendMessage(alt_text="Buttons template",
                                   template=ButtonsTemplate(
                                       thumbnail_image_url=profile.picture_url,
                                       title=profile.display_name,
                                       text=f"User Id: {profile.user_id[:5]}...\n"
                                            f"Status Message: {status_msg}",
                                       actions=[MessageAction(label="成功", text="登録完了")]))
    id = profile.user_id
    name =event.message.text
    slsql = 'SELECT * FROM dbuser'
    rows = selctcommand(dbstart(),slsql)
    uname = []
    for row in rows:
        username = row[1]
        uname.append(username)
    if name in uname:
        sql = 'UPDATE `heroku_fab7e2e9408003b`.`dbuser` SET userid = %s WHERE (name = %s);'
        sqlcommand1(dbstart(),sql,(id,name ))
        print(id)

        line_bot_api.reply_message(event.reply_token, messages=messages)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="その名前はないよ～～"))




#ログイン
@app.route('/login',methods = ['POST'])
def login():
         db = dbstart()
         sql = 'SELECT * FROM dbuser ;'
         users = selctcommand(db,sql)
         print(users)
         for user in users:
             print(user)
             name = user[1]
             pas = user[2]
             userid = user[3]
             if(request.form.get('name')==name and request.form.get('pass') == pas):
                 session['logged_in'] = True
                 session['name'] = name
                 session['userid'] = userid
             elif(request.form.get('name')==name and request.form.get('pass') != pas):
                 return render_template('login.html')
             else:
                 continue
         return redirect('/')

@app.route('/logout')
def logout():
    session.pop('logged_in', False)
    session.pop("name", None)
    return redirect("/")

@app.route('/inpuut')
def inpuut():
    return render_template("input.html")

#登録
@app.route('/input',methods = ['POST'])
def input():
    name = request.form.get('name')
    pas = request.form.get('pass')
    sql = "INSERT INTO dbuser (name,pass) VALUES (%s, %s)";
    try:
        sqlcommand1(dbstart(),sql,(name,pas))
        return redirect("/")
    except:
        return render_template('error.html')




#メインメニュー
@app.route("/",methods = ["GET","POST"])
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == "GET" and session.get('name') == 'sho' :
           import news
           db = dbstart()
           name = session.get('name')
           sql = 'SELECT * FROM todo ;'
           rows = selctcommand(db,sql)
           date = datetime.date.today()
           num = selctcommand1(dbstart(),'SELECT * FROM todofinish WHERE day = %s LIMIT 1;',(date,))
           usergragh.userfinish(name)
           sum=num[1]
           ne =  news.check()
           n = '今日のニュースは'
           for new in ne:
               ne = (new+' ')
               n = n+ne
           print(n)

           return render_template("index.html", posts = rows,n = n,num=sum,name=name)
        elif request.method =='POST':#登録
           name = session.get('name')#これかいたらできるよ
           userid = session.get('userid')
           title = request.form.get('title')
           detail = request.form.get('detail')
           due = request.form.get('due')
           print(due)
           sql = "INSERT INTO todo (title,detail,due,username,userid ) VALUES (%s, %s, %s,%s,%s);"
           sqlcommand1(dbstart(),sql,(title,detail,due,name,userid))
           sendText(userid,"TODOを登録しました\r\n{},{},{},{}".format(title,detail,due,name))
           return redirect('/')
        else:
           import news
           db = dbstart()
           name = session.get('name')
           sql = 'SELECT * FROM todo WHERE username = %s LIMIT 10;'
           date = datetime.date.today()
           rows = selctcommand2(db,sql,(name,))
           num = selctcommand1(dbstart(),'SELECT * FROM todofinish WHERE day = %s LIMIT 1;',(date,))
           usergragh.userfinish(name)
           sum = num[1]
           ne =  news.check()
           n = '今日のニュースは'
           for new in ne:
               ne = (new+' ')
               n = n+ne
           print(n)
           return render_template("index.html", posts = rows,n = n,num = sum,name=name)



#作成画面
@app.route("/create")
def create():
    if not session.get('logged_in'):
      return render_template('login.html')
    else:
      name = session.get('name')
      return render_template("create.html")
#詳細画面
@app.route("/detail/<int:id>")
def read(id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db = dbstart()
        name = session.get('name')
        row = selctcommand1(db,'SELECT * FROM todo WHERE id = %s LIMIT 1',(id,))
        return render_template("detail.html", post = row)

#削除
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name = session.get('name')
        sqlcommand1(dbstart(),'DELETE FROM todo WHERE id= %s',(id,))
        return redirect("/")

#完了
@app.route("/finish/<int:id>")
def finish(id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name = session.get('name')
        date = datetime.date.today()
        sqlcommand1(dbstart(),'DELETE FROM todo WHERE id= %s',(id,))
        print(date)
        num = selctcommand1(dbstart(),'SELECT * FROM todofinish WHERE day = %s LIMIT 1;',(date,))
        sum = num[1]+1
        usernum = selctcommand1(dbstart(),'SELECT * FROM userfinish WHERE day = %s AND username = %s LIMIT 1;',(date,name))
        if usernum == None:
            usum = 1
            sqlcommand1(dbstart(),'UPDATE todofinish SET noa = %s WHERE day = %s;',(sum,date))
            sqlcommand1(dbstart(),'INSERT INTO userfinish (day,noa,username) VALUES (%s, %s, %s);',(date,usum,name))
            import glaph
            usergragh.userfinish(name)
            return redirect("/")
        else:
            usum = usernum[1]+1
            sqlcommand1(dbstart(),'UPDATE todofinish SET noa = %s WHERE day = %s;',(sum,date))
            sqlcommand1(dbstart(),'UPDATE userfinish SET noa = %s WHERE day = %s AND username = %s;',(usum,date,name))
            import glaph
            usergragh.userfinish(name)
            return redirect("/")


#編集""
@app.route("/update/<int:id>",methods = ["GET","POST"])
def update(id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name = session.get('name')
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

#マイページ
@app.route('/mypage')
def mypage():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name = session.get('name')
        finishs = selctcommand2(dbstart(),'SELECT * FROM userfinish WHERE username = %s',(name,))
        number = 0
        for finish in finishs:
            number = number + finish[1]

        if len(finishs)!=0:
            average = number / len(finishs)
            f_average = format(average,'.2f')
            return render_template("mypage.html",name=name,number=number,average=f_average)
        else:
            f_average=0
            usergragh.userfinish(name)
            return render_template("mypage.html",name=name,number=number,average=f_average)







if __name__=="__main__":
    app.run(debug=True)
