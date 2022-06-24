# coding=utf8

from flask import Flask, render_template, request, json, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

# mysql 设置
# app.secret_key = 'hehe'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{账号}:{密码}@127.0.0.1/users'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True  # 查询时会显示原始SQL语句
# db = SQLAlchemy(app)

# mysql定义一个用户及密码的数据库
# class Users(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     username = db.Column(db.String(10))
#     password = db.Column(db.String(16))

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/resign', methods=['GET','POST'])
def resign():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, password, password2]):
            flash('参数不完整')
        elif password != password2:
            flash('两次密码不一致，请重新输入')
        else:
            # mysql插入数据
            # new_user = Users(username=username, password=password, id=None)
            # db.session.add(new_user)
            # db.session.commit()

            # sqlite3插入数据
            conn = sqlite3.connect("CarAssistantX.db")
            c = conn.cursor()
            data = []
            data.append('"' + username + '"')
            data.append('"' + password + '"')
            sql = '''
                             insert into users(username,password)
                             values (%s)
                        ''' % ",".join(data)
            c.execute(sql)
            print(data)
            conn.commit()
            conn.close()

            return '注册成功'
    return render_template('register.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            flash('参数不完整')
        # mysql 登录
        # user = Users.query.filter(Users.username == username, Users.password == password).first()
        # print(user.username)
        # print(user.password)
        # if user:
        #     return '登录成功'
        # else:
        #     return "login fail"

        # sqlite3登录
        conn = sqlite3.connect("CarAssistantX.db")
        c = conn.cursor()
        data = '"' + username + '"'
        sql = '''
            select password from users where username = %s
            ''' % data
        c.execute(sql)
        p = c.fetchall()
        conn.commit()
        conn.close()
        print(p,password)
        for p1 in p:
            if password in p1:
                return '登录成功'
        return '用户名或密码不正确'
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
