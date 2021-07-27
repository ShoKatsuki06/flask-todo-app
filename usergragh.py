import datetime
from datetime import date,timedelta
import mysql.connector
import matplotlib.pyplot as plt
import math
import numpy as np


def search(id,name):
     dns = {
    'user': 'b7933a15d37230',
    'host': 'us-cdbr-east-04.cleardb.com', # 各自設定
    'password': 'da33b80d', # 各自設定
    'database': 'heroku_fab7e2e9408003b', # 各自設定
    'port': '3306'}
     db = mysql.connector.connect(**dns)
     cursor = db.cursor(buffered = True)
     cursor.execute('SELECT * FROM userfinish WHERE day = %s AND username = %s LIMIT 1',(id,name))
     row = cursor.fetchone()
     cursor.close()
     db.close()

     if row == None:
         return 0
     else:
         return row[1]



def userfinish(name):
    today = datetime.date.today ()

    a = today - timedelta(days=1)
    b = today - timedelta(days=2)
    c = today - timedelta(days=3)
    d = today - timedelta(days=4)
    e = today - timedelta(days=5)
    f = today - timedelta(days=6)

    today_finish = search(today,name)
    a_finish = search(a,name)
    b_finish = search(b,name)
    c_finish = search(c,name)
    d_finish = search(d,name)
    e_finish = search(e,name)
    f_finish = search(f,name)

    #plt.style.use('fivethirtyeight')

    y = np.array([today_finish,a_finish,b_finish,c_finish,d_finish,e_finish,f_finish])
    x = np.array([today,a,b,c,d,e,f])
    plt.figure(figsize=(10, 4))
    plt.plot(x,y)
    plt.title('Recent achievements')
    plt.ylabel('Achievements')
    plt.xlabel('day')
    plt.ylim(0, 7)
    plt.grid()

    #plt.figure(figsize=(9, 9))
    plt.savefig('./static/img/f_gragh{}.png'.format(name))

#sns.set(plt)
