# encoding: UTF-8
import random
import shutil
from urllib import request
import os
from flask import Flask, render_template, request, session, redirect, url_for, make_response, send_from_directory
from wtforms import Form
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets
import pymysql
from pymysql import escape_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import MySQLdb
import datetime
import hashlib
from flask_login import login_user, current_user, LoginManager, logout_user
import string
from random import choice
from flask_login import UserMixin
import glob


app = Flask(__name__, template_folder='templates')
# 设置secret值，保护信息不被泄露
app.config['SECRET_KEY'] = 'aasswde'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost:3306/dbname?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
conn = pymysql.connect(host='114.116.88.46', port=3306, user='sibd-test', passwd='Mydb@)!(123', db='image_file', charset='utf8')
cursor = conn.cursor()

image_list1 = []
image_list2 = []
image_name1 = []
image_name2 = []
images = []

files_path = r'/data/bigimg/png'   # 这个是服务器里面的原图片位置
temp_text = r'/usr/local/Image_web/files/'
temp_zip = r'/usr/local/Image_web/files/'

# files_path = r'C:/Users/heizi/Desktop/qwerty'
# temp_text = r'D:/asdfg/'
# temp_zip = r'D:/asdfg/'
for filename in os.listdir(files_path):
    images.append(filename)

app.debug = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

passwordrange = string.ascii_letters + string.digits  # 密码包括数字大小写
usernamerange = string.ascii_lowercase  # 名字只取大写字母

# HOST = "114.115.249.245"         # 定义服务器ip
# PORT = "SIBD@sibd.com"                      # 定义端口号
# addr = (HOST, PORT)               # 由于使用socket进行连接，需要把ip和端口先转换为元组
# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 设定了网络连接方式，以及传输使用的协议
# c.connect(addr)  #连接服务器


def random_passwd(num=8):  # 密码默认取八位数，可以自定义
    return ''.join([choice(passwordrange) for i in range(num)]).encode('utf-8')


def random_name(num=5):  # 名字默认取5位数，可以自定义
    return ''.join([choice(usernamerange) for i in range(num)])


def is_active(self):
    return True


def del_files(temp_text):
    #   read all the files under the folder
    fileNames = glob.glob(temp_text + r'\*')

    for fileName in fileNames:
        try:
            # delete file
            os.remove(fileName)
        except:
            try:
                # delete empty folders
                os.rmdir(fileName)
            except:
                # Not empty, delete files under folders
                del_files(fileName)
                #    now, folders are empty, delete it
                os.rmdir(fileName)


class user(Form, UserMixin):
    # 字段（内部包含正则表达式）
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空.'),
            validators.Length(min=4, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(),  # 页面上显示的插件
        render_kw={'class': 'form-control'}

    )
    # 字段（内部包含正则表达式）
    password = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                              message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')

        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )
    role = simple.BooleanField(label='权限', default=0)
    login = simple.SubmitField('login')
    logout = simple.SubmitField('logout')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        error = None
        cursor.execute(
            "SELECT * FROM user WHERE name = %s", username
        )
        b = cursor.fetchone()
        if b[0] != username:
            error = '用户名错误'
            return render_template('login.html', error=error)
        elif password != b[1]:
            error = '密码错误'
            return render_template('login.html', error=error)
        if error is None:
            session['name'] = username
            return redirect(url_for('pre_download', username=username))

    return render_template('login.html')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(64), unique=True)
    size = db.Column(db.Integer, index=True, unique=True)
    mark_result = db.Column(db.String(255), index=True, unique=True)


class record(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    file_number = db.Column(db.Integer, )
    times = db.Column(db.String(10))  # 下载时间


@app.route('/pre_download/')
def pre_download():
    username = session.get('name')
    return render_template('download_page.html', username=username)


@app.route('/download_page/')
def download_page():
    del_files(temp_text)
    temp_path = ''
    filename1 = ''
    username = session.get('name')
    if request.method == 'GET':
        number1 = request.args.get('number')
        order = request.args.get('order')
        begin = request.args.get('begin')
        print(number1, order, begin)
        # print(number, order, Number)

        cursor.execute(
            'SELECT * FROM user WHERE name = %s', username
        )
        user = cursor.fetchone()
        role = user[2]
        # print(role)
        if number1 is not '全部':
            temp_path, filename1 = download_zip(number1, username, order, begin)
        else:
            if role == 1:
                temp_path, filename1 = download_zip(30000, username, order, begin)
            else:
                error = '您没有下载全部照片的权限'
                return render_template('failure.html', error=error)
    response = make_response(send_from_directory(temp_path, filename1, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(temp_path.encode().decode('utf-8'))
    return send_from_directory(temp_path, filename1, as_attachment=True,)


@app.route('/list/')
def list():
    username = session.get('name')
    cursor.execute(
        'SELECT * FROM user WHERE name = %s', username
    )
    user = cursor.fetchone()
    role = user[2]
    if role == 1:
        cursor.execute(
            'SELECT * FROM user '
        )
        user = cursor.fetchall()
        size = len(user)
        return render_template('list.html', users=user, username=username, size=size)
    else:
        eorror = '对不起你没有权限访问'
        # users是一个列表，数据库里面的所有数据都在users中
        return render_template('failure.html', error=eorror, username=username)


# 必须得判断当前是否在线
@app.route('/delete/<string:name>')
def delete(name):
    username = session.get('name')
    if name == 'root':
        eorror = '超级用户不能被删除'
        return render_template('failure.html', error=eorror, username=username)
    else:
        cursor.execute(
            'DELETE FROM user WHERE name = %s', name
        )
        conn.commit()
    return redirect(url_for('list', username=username))


@app.route('/add/')
def add():
    # 用户名和密码随机生成
    username = session.get('name')
    username_new = random_name(5)
    print(username_new)
    passwords = random_passwd(8)
    cursor.execute('INSERT INTO user (name, password, role) '
                   'VALUE ("%s","%s",%s)', (username_new, passwords, 0))
    conn.commit()
    return redirect(url_for('list', username=username))


def download_zip(number, username, order, begin):
    s1 = datetime.datetime.now().strftime("%f")
    temp_text1 = temp_text + username + '/' + str(s1) + '/'   # 存储临时图片的路径
    os.makedirs(temp_text1)
    # 打.zip包的路径
    s2 = datetime.datetime.now().strftime("%f")
    temp_zip1 = temp_zip + str(s2)
    os.makedirs(temp_zip1)

    temp_zip2 = temp_zip1 + '/' + str(s2)
    # 压缩包名字
    filename1 = '{}.zip'.format(str(s2))
    if order == "顺序":
        # 这个是按照规则进行取得然后放到文件里面，进行压缩，可变的
        for i in range(int(begin), int(begin) + int(number)):
            image_list1.append(images[i])
            image_path = files_path + '/' + images[i]
            shutil.copy(image_path, temp_text1 + images[i])
        # base_name 的意思是在桌面形成一个以a命名的.zip文件  叫a.zip
        shutil.make_archive(base_name=temp_zip2, format='zip', root_dir=temp_text1, )
        print(temp_zip2, temp_text1)
        temp_path = temp_zip1       # zip文件夹
        response = make_response(send_from_directory(temp_path, filename1, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(temp_path.encode().decode('latin-1'))
    else:
        for i in range(int(number)):
            # 这边的30000有点大，测试的时候调小点
            b = random.randint(1, 30000)
            image_list2.append(images[b])
            image_path = files_path + '/' + images[b]      # 原图片路径
            shutil.copy(image_path, temp_text1 + images[b])
            # base_name 的意思是在桌面形成一个以a命名的.zip文件  叫a.zip
        shutil.make_archive(base_name=temp_zip2, format='zip', root_dir=temp_text1, )
        temp_path = temp_zip1      # zip文件夹
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO record (username, file_number,  times) '
                   'VALUE (%s,%s,%s)', (username, number, now_time))
    conn.commit()
    return temp_path, filename1


@app.route('/')
def index():

    return index


if __name__ == '__main__':
    app.run()
