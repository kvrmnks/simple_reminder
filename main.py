import flask
import my_database
from flask import request
from flask import session
import datetime
import configparser

app = flask.Flask(__name__)
app.secret_key = '3425u23io4ju2o'
CODE = ''
host = ''
port = 0
user = ''
password = ''
db = ''

'''

'''

def check_session():
    return session.get('code') is None or session['code'] != CODE


@app.route('/', methods=['POST', 'GET'])
def fun():
    if request.method == 'GET' and session.get('code') is None:
        return flask.render_template('login.html')
    elif request.method == 'POST':
        print(request.form.get('code'))
        if request.form.get('code') == CODE:
            session['code'] = CODE
        return flask.redirect('/')
    else:
        return flask.render_template('index.html')


@app.route('/log')
def get_list():
    if check_session():
        return flask.redirect('/')

    data = sql.get_all_content()
    for x in data:
        x['content'] = x['content'].decode('utf-8')
    return flask.render_template('list.html', data=data)


@app.route('/new', methods=['POST', 'GET'])
def insert():
    if check_session():
        return flask.redirect('/')

    if request.method == 'POST':
        content = request.form.get('content')
        if content == '' or content is None:
            pass
        else:
            sql.insert(content)
    return flask.render_template('new.html')


@app.route('/review')
def review():
    if check_session():
        return flask.redirect('/')

    t_delta = [1, 2, 4, 7, 15, 30, 3 * 30, 6 * 30]
    todo_list = []
    # print(datetime.datetime.now())
    for x in t_delta:
        delta = datetime.timedelta(days=x)
        cur = datetime.datetime.now() - delta
        str_cur = cur.strftime('%Y-%m-%d')
        todo_list_cur = sql.get_content_by_date(str_cur)
        if len(todo_list_cur) >= 1:
            todo_list += todo_list_cur
    for x in todo_list:
        x['content'] = x['content'].decode('utf-8')
    # print(todo_list)
    return flask.render_template('review.html', data=todo_list)


if __name__ == "__main__":
    cp = configparser.ConfigParser()
    cp.read('reminder.ini')
    CODE = cp.get('reminder', 'CODE')
    host = cp.get('reminder', 'host')
    port = int(cp.get('reminder', 'port'))
    user = cp.get('reminder', 'user')
    password = cp.get('reminder', 'password')
    db = cp.get('reminder', 'db')
    sql = my_database.my_database(host, port, user, password, db)

    app.run(host="0.0.0.0", port=7000)
