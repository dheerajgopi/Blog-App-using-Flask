#!flask/bin/python
# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,\
                     render_template, flash

# config
DATABASE = 'db/entries.db'
#DEBUG = True
SECRET_KEY = 'password'
USERNAME = 'admin'
PASSWORD = 'admin'

# creating flask app instance
app = Flask(__name__)
app.config.from_object(__name__)

# for connecting with db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request() :
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception) :
    db = getattr(g, 'db', None)
    if db is not None :
        db.close()

@app.route('/')
def show_entries():
    entries = None
    postcur = g.db.execute('select postid, title, body, user_name from entries order by postid desc')
    entries = [dict(postid=row[0], title=row[1], body=row[2], user_name=row[3]) for row in postcur.fetchall()]
    cmtcur = g.db.execute('select cmtid, cmt, postid, user_name from comments order by cmtid desc')
    comments = [dict(cmtid=row[0], cmt=row[1], postid=row[2], user_name=row[3]) for row in cmtcur.fetchall()]
    return render_template('show_entries.html', entries=entries, comments=comments)

# logging in
@app.route('/login', methods = ['GET', 'POST'])
def login() :
    error = None
    if request.method == 'POST' :
        if request.form['username'] != app.config['USERNAME'] :
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD'] :
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout() :
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('show_entries'))

@app.route('/add', methods = ["POST"])
def add_entry() :
    if not session.get('logged_in') :
        flash('log in to add entries')
        return redirect(url_for('login'))
    g.db.execute('INSERT INTO entries (title, body, user_name) VALUES (?, ?, ?)', [request.form['title'], request.form['body'], app.config['USERNAME']])
    g.db.commit()
    flash('New entry posted')
    return redirect(url_for('show_entries'))

@app.route('/add_cmt', methods = ["POST"])
def add_cmt() :
    postid = request.form.get('postid')
    comment = request.form.get('commentbox')
    if session.get('logged_in') :
        username = app.config['USERNAME']
    else :
        username = 'Guest'
    g.db.execute('INSERT INTO comments (cmt, postid, user_name) VALUES (?, ?, ?)', [comment, postid, username])
    g.db.commit()
    flash('Comment Posted')
    return redirect(url_for('show_entries'))
    return render_template('post.html')

if __name__ == '__main__' :
    app.run(debug = True)
