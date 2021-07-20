from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector
import pymysql.cursors

app = Flask(__name__)
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

if db.is_connected():
    print("データベースへの接続が成功しました。")
else:
    print("データベースへの接続が失敗しました。")
    exit(1)

cursor = db.cursor()
cursor.execute("USE heroku_fab7e2e9408003b")
db.commit()
db.ping(reconnect=True)

#class Post(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(30), nullable=False)
    #detail = db.Column(db.String(100))
    #due = db.Column(db.DateTime, nullable=False)"'
#メインメニュー
@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "GET":
       cursor.execute('SELECT * FROM todo;')
       rows = cursor.fetchall()
       #posts = Post.query.all()
       return render_template("index.html", posts = rows )
    else:#登録
       title = request.form.get('title')
       detail = request.form.get('detail')
       due = request.form.get('due')
       print(due)
       #due = datetime.strptime(due, '%Y-%m-%d')
       #new_post = Post(title=title, detail=detail, due=due)
       sql = "INSERT INTO todo (title,detail,due ) VALUES (%s, %s, %s);"
       cursor.execute(sql,(title,detail,due))
       db.commit()
       #db.session.add(new_post)
       #db.session.commit()
       return redirect('/')
#作成画面
@app.route("/create")
def create():
      return render_template("create.html")
#詳細画面
@app.route("/detail/<int:id>")
def read(id):
    cursor.execute('SELECT * FROM todo WHERE id = %s',(id,) )
    row = cursor.fetchone()
    db.commit()
    #post = Post.query.get(id)
    return render_template("detail.html", post = row)
#削除
@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute('DELETE FROM todo WHERE id= %s',(id,))

    #db.commit()
    #post = Post.query.get(id)
    #db.session.delete(post)
    #db.session.commit()
    return redirect("/")
#編集
@app.route("/update/<int:id>",methods = ["GET","POST"])
def update(id):
    cursor.execute('SELECT * FROM todo WHERE id = %s',(id,))
    row = cursor.fetchone()
    db.commit()
    #post = Post.query.get(id)
    if request.method =="GET":
        return render_template("update.html",post=row)
    else:
        title = request.form.get("title")
        detail = request.form.get("detail")
        due = request.form.get("due")
        cursor.execute('UPDATE todo SET title = %s,detail = %s,due = %s WHERE id= %s',(title,detail,due,id))
        db.commit()
        #db.session.commit()
        return redirect("/")


if __name__=="__main__":
    app.run(debug=True)
