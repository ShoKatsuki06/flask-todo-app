import datetime
from datetime import date,timedelta
import mysql.connector
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns

def search(id):
     dns = {
    'user': 'b7933a15d37230',
    'host': 'us-cdbr-east-04.cleardb.com', # 各自設定
    'password': 'da33b80d', # 各自設定
    'database': 'heroku_fab7e2e9408003b', # 各自設定
    'port': '3306'}
     db = mysql.connector.connect(**dns)
     cursor = db.cursor(buffered = True)
     cursor.execute('SELECT * FROM todofinish WHERE day = %s LIMIT 1',(id,))
     row = cursor.fetchone()
     cursor.close()
     db.close()
     return row

today = datetime.date.today ()

a = today - timedelta(days=1)
b = today - timedelta(days=2)
c = today - timedelta(days=3)
d = today - timedelta(days=4)
e = today - timedelta(days=5)
f = today - timedelta(days=6)

today_finish = search(today)[1]
a_finish = search(a)[1]
b_finish = search(b)[1]
c_finish = search(c)[1]
d_finish = search(d)[1]
e_finish = search(e)[1]
f_finish = search(f)[1]

#plt.style.use('fivethirtyeight')

y = np.array([today_finish,a_finish,b_finish,c_finish,d_finish,e_finish,f_finish])
x = np.array([today,a,b,c,d,e,f])
plt.figure(figsize=(10, 4))
plt.plot(x,y)
plt.title('最近の達成数の流れ',fontname="MS Gothic")
plt.ylabel('達成数',fontname="MS Gothic")
plt.xlabel('日付',fontname="MS Gothic")
plt.ylim(0, 7)
plt.grid()

#plt.figure(figsize=(9, 9))
plt.savefig('./static/img/f_gragh.png')
#sns.set(plt)
